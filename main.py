"""
Horizon Shuttle AI — MVP Minimal Backend
1 file, 3 endpoint, no database, hardcode login
"""

import os
from datetime import datetime, timedelta
from typing import Optional, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError

import google.generativeai as genai
from astrapy import DataAPIClient

# ═══════════════════════════════════════════════════════════════
# 1. LOAD ENV
# ═══════════════════════════════════════════════════════════════
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ASTRA_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE", "horizon_shuttle")
ASTRA_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "knowledge_chunks")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "horizon2026")
JWT_SECRET = os.getenv("JWT_SECRET", "ganti-ini-dengan-string-panjang-32-karakter")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 8

# ═══════════════════════════════════════════════════════════════
# 2. INIT GEMINI
# ═══════════════════════════════════════════════════════════════
genai.configure(api_key=GEMINI_API_KEY)

embedding_model = genai.GenerativeModel("models/gemini-embedding-001")
chat_model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ═══════════════════════════════════════════════════════════════
# 3. INIT ASTRADB
# ═══════════════════════════════════════════════════════════════
astra_client = DataAPIClient(ASTRA_TOKEN)
db = astra_client.get_database_by_api_endpoint(ASTRA_ENDPOINT)
collection = db.get_collection(ASTRA_COLLECTION)

# ═══════════════════════════════════════════════════════════════
# 4. FASTAPI APP
# ═══════════════════════════════════════════════════════════════
app = FastAPI(title="Horizon Shuttle AI", version="mvp-1.0")

# Serve static files (frontend HTML/JS/CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS (allow all for MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# 5. PYDANTIC SCHEMAS
# ═══════════════════════════════════════════════════════════════
class LoginRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "assistant"  # assistant | draft | insight

class ChatResponse(BaseModel):
    reply: str
    sources: Optional[List[str]] = None

# ═══════════════════════════════════════════════════════════════
# 6. SYSTEM PROMPTS (3 Mode)
# ═══════════════════════════════════════════════════════════════
SYSTEM_PROMPTS = {
    "assistant": """Kamu adalah Horizon AI, asisten customer service Horizon Shuttle.
Jawab berdasarkan informasi yang diberikan di KNOWLEDGE BASE.
Gunakan bahasa Indonesia yang ramah, profesional, dan mudah dipahami.
Jika informasi tidak tersedia di KNOWLEDGE BASE, katakan dengan sopan bahwa kamu belum memiliki informasi tersebut.
Jangan menjawab berdasarkan pengetahuan umum di luar KNOWLEDGE BASE.""",

    "draft": """Kamu adalah Horizon AI Draft Writer, penulis materi komunikasi untuk Horizon Shuttle.
Tugasmu membuat draft materi promosi dan komunikasi sesuai kebutuhan user.
Ikuti BRAND VOICE Horizon Shuttle: ramah, profesional, trustworthy, approachable.
Format output sesuai jenis materi yang diminta (broadcast WhatsApp, email, caption IG, pengumuman, dll).
Gunakan bahasa Indonesia yang natural dan engaging.""",

    "insight": """Kamu adalah Horizon AI Business Advisor, konsultan bisnis Horizon Shuttle.
Analisis data dan berikan rekomendasi strategis dalam bentuk narasi yang mudah dipahami.
Sertakan insight actionable, bukan sekadar angka.
Gunakan bahasa Indonesia profesional tapi tidak kaku.
Berikan rekomendasi konkret yang bisa langsung dijalankan."""
}

# ═══════════════════════════════════════════════════════════════
# 7. HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def create_jwt_token(username: str) -> str:
    """Buat JWT token untuk session login."""
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> Optional[str]:
    """Verifikasi JWT token, return username kalau valid."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Dependency: verifikasi JWT dari header Authorization."""
    username = verify_jwt_token(credentials.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="Token tidak valid atau sudah expired")
    return username


def embed_text(text: str) -> list:
    """Ubah teks jadi vector embedding pakai Gemini Embedding 001."""
    try:
        result = embedding_model.embed_content(content=text)
        return result.embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal embed teks: {str(e)}")


def query_astra(vector: list, category_filter: List[str], top_k: int = 5):
    """Cari chunk yang mirip di AstraDB dengan filter kategori."""
    try:
        results = collection.find(
            filter={"metadata.category": {"$in": category_filter}},
            sort={"$vector": vector},
            limit=top_k,
            include_similarity=True
        )
        return list(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal query AstraDB: {str(e)}")


def build_prompt(query: str, chunks: list, mode: str) -> str:
    """Gabungkan system prompt + konteks chunks + pertanyaan user."""
    system = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["assistant"])
    
    # Format chunks jadi string
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        text = chunk.get("text", "")
        source = chunk.get("metadata", {}).get("source", "unknown")
        context_parts.append(f"[DOKUMEN {i} - {source}]\\n{text}")
    
    context = "\\n\\n".join(context_parts) if context_parts else "Tidak ada dokumen relevan ditemukan."
    
    prompt = f"""{system}

═══════════════════════════════════════════════════════════════
KNOWLEDGE BASE:
═══════════════════════════════════════════════════════════════
{context}

═══════════════════════════════════════════════════════════════
PERTANYAAN USER:
═══════════════════════════════════════════════════════════════
{query}

═══════════════════════════════════════════════════════════════
JAWABAN:"""
    
    return prompt


def generate_reply(prompt: str) -> str:
    """Generate jawaban pakai Gemini 2.5 Flash-Lite."""
    try:
        response = chat_model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal generate jawaban: {str(e)}")


# ═══════════════════════════════════════════════════════════════
# 8. RAG PIPELINE (Public & Workspace)
# ═══════════════════════════════════════════════════════════════

def rag_pipeline(query: str, mode: str, user_type: str = "public") -> dict:
    """
    Pipeline RAG lengkap:
    1. Embed query
    2. Query AstraDB (filter by permission)
    3. Build prompt
    4. Generate reply
    """
    # Step 1: Embed query
    query_embedding = embed_text(query)
    
    # Step 2: Tentukan filter kategori
    if user_type == "public":
        category_filter = ["public"]
    else:
        category_filter = ["public", "internal"]
    
    # Step 3: Retrieve chunks dari AstraDB
    chunks = query_astra(query_embedding, category_filter, top_k=5)
    
    # Step 4: Build prompt dengan konteks
    prompt = build_prompt(query, chunks, mode)
    
    # Step 5: Generate jawaban
    reply = generate_reply(prompt)
    
    # Step 6: Extract sources
    sources = list(set(
        chunk.get("metadata", {}).get("source", "unknown") 
        for chunk in chunks
    ))
    
    return {
        "reply": reply,
        "sources": sources if sources else None
    }


# ═══════════════════════════════════════════════════════════════
# 9. API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "message": "Horizon Shuttle AI API",
        "version": "mvp-1.0",
        "status": "running"
    }


@app.post("/api/auth/login")
def login(request: LoginRequest):
    """
    Login hardcode — cuma 1 akun dari .env.
    Return JWT token kalau sukses.
    """
    if request.username != ADMIN_USERNAME or request.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    token = create_jwt_token(request.username)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": ADMIN_USERNAME,
            "nama": "Admin Horizon"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat_public(request: ChatRequest):
    """
    PUBLIC CHAT — no auth required.
    Selalu pakai mode "assistant" dan filter "public" chunks.
    """
    result = rag_pipeline(
        query=request.message,
        mode="assistant",  # Public selalu assistant
        user_type="public"
    )
    
    return ChatResponse(reply=result["reply"], sources=result["sources"])


@app.post("/api/workspace/chat", response_model=ChatResponse)
def chat_workspace(
    request: ChatRequest,
    username: str = Depends(get_current_user)
):
    """
    WORKSPACE CHAT — requires JWT auth.
    Support 3 mode: assistant, draft, insight.
    Filter chunks: public + internal.
    """
    # Validate mode
    if request.mode not in ["assistant", "draft", "insight"]:
        raise HTTPException(status_code=400, detail="Mode harus: assistant, draft, atau insight")
    
    result = rag_pipeline(
        query=request.message,
        mode=request.mode,
        user_type="business"
    )
    
    return ChatResponse(reply=result["reply"], sources=result["sources"])


# ═══════════════════════════════════════════════════════════════
# 10. RUN (for local development)
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)