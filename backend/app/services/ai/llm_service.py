import openai
from app.core.config import settings
from app.services.ai.rag_service import get_rag_context

def process_voice_with_llm(text: str) -> str:
    """Processes transcript plus RAG context using GPT-4o."""
    if not settings.OPENAI_API_KEY:
        return "Warning: OPENAI_API_KEY is missing. But I would have answered: Please proceed to the nearest emergency center."
        
    try:
        # Fetch relevant offline context
        rag_context = get_rag_context(text)
        
        # Build strict system prompt
        system_instruction = (
            "You are Arohan, a concise, highly empathetic Indian Emergency AI Voice Agent. "
            "Respond in the same Indian language the user speaks, but keep answers under 2 sentences to ensure fast voice rendering. "
            f"Use this medical/emergency context if relevant: {rag_context}"
        )
        
        client = openai.Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM Error: {e}")
        return "I am experiencing connectivity issues. Please call emergency services directly."
