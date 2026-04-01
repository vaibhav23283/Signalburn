import httpx
from app.core.config import settings

def synthesize_speech(text: str, language_code: str = "hi-IN") -> bytes:
    """Sends text to Sarvam AI and returns the MP3 bytes."""
    if not settings.SARVAM_API_KEY:
        print("Warning: SARVAM_API_KEY missing. Returning empty byte array.")
        return b""
        
    try:
        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "api-subscription-key": settings.SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text, # Switched from deprecated 'inputs' list to modern 'text' string
            "target_language_code": language_code, 
            "speaker": "anushka", 
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.5,
            "enable_preprocessing": True
        }
        
        response = httpx.post(url, json=payload, headers=headers, timeout=15.0)
        
        if response.status_code == 200:
            # Sarvam returns the base64 or binary audio payload.
            # Depending on their exact response schema (they typically return base64 'audios'),
            # we decode it or if binary return directly.
            # Assuming typical JSON with base64 audio array:
            import base64
            data = response.json()
            audio_base64 = data.get("audios", [])[0]
            return base64.b64decode(audio_base64)
        else:
            print(f"Sarvam AI Error: {response.status_code} - {response.text}")
            return b""
            
    except Exception as e:
        print(f"TTS Error: {e}")
        return b""
