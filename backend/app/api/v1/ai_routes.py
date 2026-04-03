from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from app.models.ai_models import VoicePromptPayload, HealthQueryResponse
from app.services.ai.agent_service import process_voice_agent_text
from app.services.ai.speech_service import transcribe_audio
from app.services.ai.tts_service import synthesize_speech
from app.core.config import settings
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/process", response_model=HealthQueryResponse)
def process_text_prompt(payload: VoicePromptPayload):
    """
    Text input → RAG + Gemini Agent → Text response.
    Used when frontend sends already transcribed text.
    """
    try:
        session_id = str(uuid.uuid4())

        response_text = process_voice_agent_text(
            transcript=payload.text,
            session_id=session_id
        )

        return HealthQueryResponse(
            response=response_text,
            status="success" if settings.GEMINI_API_KEY else "warning",
            language=payload.language,
            rag_context_used=True
        )

    except Exception as e:
        logger.error(f"Error in /process: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice-query")
async def full_voice_pipeline(
    audio: UploadFile = File(...),
    language_code: str = "hi-IN",
    session_id: str = None
):
    """
    Full pipeline:
    Audio → Gemini transcription → RAG + Gemini Agent → Sarvam TTS → Audio response
    """
    try:
        # Generate session ID if not provided (for conversation memory)
        if not session_id:
            session_id = str(uuid.uuid4())

        # Step 1: Read audio and transcribe using Gemini
        audio_bytes_data = await audio.read()

        import io
        audio_stream = io.BytesIO(audio_bytes_data)
        transcribed_text = transcribe_audio(audio_stream, audio.filename)
        logger.info(f"Transcribed: {transcribed_text[:100]}")

        # Step 2: RAG + Gemini Agent
        answer_text = process_voice_agent_text(
            transcript=transcribed_text,
            session_id=session_id
        )
        logger.info(f"Agent answer: {answer_text[:100]}")

        # Step 3: Sarvam TTS → Indian voice
        audio_response = synthesize_speech(answer_text, language_code)

        return Response(
            content=audio_response,
            media_type="audio/mpeg",
            headers={
                "X-Session-Id": session_id,
                "X-Transcription": transcribed_text,
                "X-Answer-Text": answer_text
            }
        )

    except Exception as e:
        logger.error(f"Error in /voice-query: {e}")
        raise HTTPException(status_code=500, detail=str(e))