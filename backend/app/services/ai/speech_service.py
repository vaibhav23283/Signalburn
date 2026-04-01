import google.generativeai as genai
import os
import tempfile
from typing import BinaryIO
from app.core.config import settings

def transcribe_audio(audio_file: BinaryIO, filename: str) -> str:
    """Takes a raw audio stream, saves it temporarily, uploads to Gemini, and returns transcript."""
    if not settings.GEMINI_API_KEY:
        return "Warning: GEMINI_API_KEY is missing."
        
    try:
        # Gemini 1.5 allows inline binary audio injection directly into the prompt up to 20MB
        audio_bytes = audio_file.read()
        
        # Initialize Gemini Flash Latest which has a standard free tier quota
        model = genai.GenerativeModel(model_name="gemini-flash-latest")
        
        prompt = "Listen to this audio. Give me the transcription EXACTLY as it is spoken, in the original Indian language or English. Output ONLY the words spoken in plain text, do not add translation or formatting."
        
        response = model.generate_content([
            prompt, 
            {"mime_type": "audio/mpeg", "data": audio_bytes}
        ])
        
        transcript = response.text.strip()
        return transcript
    except Exception as e:
        print(f"Error in Gemini transcription: {e}")
        return f"Warning: Could not transcribe audio. Defaulting to emergency test mode. The exact error is: {repr(e)}"
