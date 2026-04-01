from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from app.services.ai.speech_service import transcribe_audio
from app.services.ai.agent_service import process_voice_agent_text
from app.services.ai.tts_service import synthesize_speech
from app.core.config import settings
import io

router = APIRouter()

@router.post("/process")
async def process_voice_pipeline(
    audio: UploadFile = File(...),
    session_id: str = Form("default_session")
):
    """
    Complete Pipeline:
    1. Whisper extracts text from uploaded audio file.
    2. LangGraph Agent (GPT + RAG Memory) processes context.
    3. Sarvam outputs final Indian Language TTS Audio.
    """
    try:
        # 1. Read Audio File
        audio_content = await audio.read()
        audio_stream = io.BytesIO(audio_content)
        
        # 2. Whisper (Speech to Text)
        transcript = transcribe_audio(audio_stream, audio.filename)
        
        # 3. LangGraph Agent + RAG Memory (Text Processing)
        gpt_response_text = process_voice_agent_text(transcript, session_id=session_id)
        
        # 4. Sarvam AI (Text to Speech)
        # In a real app, detect the user's language via frontend metadata or LLM detection.
        audio_bytes = synthesize_speech(gpt_response_text, language_code="hi-IN")
        
        # If no keys or TTS failed, fallback to returning JSON so the app doesn't crash completely.
        if not audio_bytes:
            return JSONResponse({
                "response_text": gpt_response_text,
                "status": "warning_no_audio",
                "transcript": transcript,
                "session_id": session_id
            })
            
        # 5. Native Audio Stream Output
        return Response(content=audio_bytes, media_type="audio/mpeg", headers={
            "X-Conversation-Session": session_id
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice pipeline failed: {str(e)}")
