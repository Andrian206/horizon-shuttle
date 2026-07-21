import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

embedding_model = genai.GenerativeModel("models/gemini-embedding-001")
chat_model = genai.GenerativeModel("gemini-2.5-flash-lite")

def embed_text(text: str) -> list:
    """Ubah teks jadi vector embedding."""
    result = embedding_model.embed_content(content=text)
    return result.embedding

def generate_response(prompt: str) -> str:
    """Generate jawaban dari Gemini."""
    response = chat_model.generate_content(prompt)
    return response.text