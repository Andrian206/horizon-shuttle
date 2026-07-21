from services.gemini_service import embed_text, generate_response
from services.astra_service import query_similar_chunks

SYSTEM_PROMPTS = {
    "assistant": """Kamu adalah Horizon AI, asisten customer service Horizon Shuttle.
Jawab berdasarkan informasi yang diberikan. Gunakan bahasa Indonesia ramah dan profesional.
Jika informasi tidak tersedia, katakan dengan sopan.""",
    
    "draft": """Kamu adalah Horizon AI Draft Writer.
Buat materi komunikasi untuk Horizon Shuttle mengikuti brand voice: ramah, profesional, trustworthy.
Format sesuai kebutuhan user.""",
    
    "insight": """Kamu adalah Horizon AI Business Advisor.
Analisis data dan berikan rekomendasi strategis dalam bahasa narasi yang mudah dipahami.
Sertakan insight actionable, bukan sekadar angka."""
}

def build_prompt(query: str, chunks: list, mode: str) -> str:
    """Gabungkan system prompt + konteks + pertanyaan user."""
    system = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["assistant"])
    
    context = "\n\n".join([
        f"[Sumber: {chunk.get('metadata', {}).get('source', 'unknown')}]\n{chunk.get('text', '')}"
        for chunk in chunks
    ])
    
    prompt = f"""{system}

BERIKUT INFORMASI DARI KNOWLEDGE BASE:
{context}

PERTANYAAN USER:
{query}

JAWABAN:"""
    
    return prompt

def rag_query(query: str, mode: str = "assistant", user_type: str = "public") -> dict:
    """
    Pipeline RAG lengkap:
    1. Embed query
    2. Cari chunk mirip (filter by permission)
    3. Build prompt
    4. Generate response
    """
    # Step 1: Embed query
    query_embedding = embed_text(query)
    
    # Step 2: Tentukan filter kategori
    if user_type == "public":
        category_filter = ["public"]
    else:
        category_filter = ["public", "internal"]
    
    # Step 3: Retrieve chunks
    chunks = query_similar_chunks(query_embedding, category_filter, top_k=5)
    
    # Step 4: Build prompt
    prompt = build_prompt(query, chunks, mode)
    
    # Step 5: Generate
    reply = generate_response(prompt)
    
    # Step 6: Return dengan sources
    sources = [chunk.get("metadata", {}).get("source", "unknown") for chunk in chunks]
    
    return {
        "reply": reply,
        "sources": list(set(sources))  # Hapus duplikat
    }