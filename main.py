"""
Horizon Shuttle AI — MVP Minimal Backend
astrapy 2.3.1 compatible | 1 file, 3 endpoint, no database, hardcode login
"""

import os
from datetime import datetime, timedelta
from typing import Optional, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
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
ASTRA_NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE", "default_keyspace")
ASTRA_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "knowledge_chunks")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 8

# ═══════════════════════════════════════════════════════════════
# 2. INIT GEMINI
# ═══════════════════════════════════════════════════════════════
genai.configure(api_key=GEMINI_API_KEY)

chat_model = genai.GenerativeModel("gemini-3.1-flash-lite")

# ═══════════════════════════════════════════════════════════════
# 3. INIT ASTRADB (astrapy 2.3.1)
# ═══════════════════════════════════════════════════════════════
# astrapy v2: token bisa di client ATAU di get_database
astra_client = DataAPIClient()

db = astra_client.get_database(
    ASTRA_ENDPOINT,
    token=ASTRA_TOKEN,
    keyspace=ASTRA_NAMESPACE
)

collection = db.get_collection(ASTRA_COLLECTION)

# ═══════════════════════════════════════════════════════════════
# 4. FASTAPI APP
# ═══════════════════════════════════════════════════════════════
app = FastAPI(title="Horizon Shuttle AI", version="mvp-1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

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
    mode: Optional[str] = "assistant"

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
Gunakan format **Markdown** untuk mempercantik jawaban: **bold** untuk poin penting, --- untuk pemisah, - untuk bullet list, dan 1. untuk nomor urut.
Jika informasi tidak tersedia di KNOWLEDGE BASE, katakan dengan sopan bahwa kamu belum memiliki informasi tersebut.
Jangan menjawab berdasarkan pengetahuan umum di luar KNOWLEDGE BASE.""",

    "draft": """Kamu adalah Horizon AI Draft Writer, penulis materi komunikasi untuk Horizon Shuttle.
Tugasmu membuat draft materi promosi dan komunikasi sesuai kebutuhan user.
Ikuti BRAND VOICE Horizon Shuttle: ramah, profesional, trustworthy, approachable.
Format output sesuai jenis materi yang diminta (broadcast WhatsApp, email, caption IG, pengumuman, dll).
Gunakan format **Markdown** agar output rapi: judul pakai ##, poin pakai -, bold untuk penekanan.
Gunakan bahasa Indonesia yang natural dan engaging.""",

    "insight": """Kamu adalah Horizon AI Business Advisor, konsultan bisnis Horizon Shuttle.
Analisis data dan berikan rekomendasi strategis dalam bentuk narasi yang mudah dipahami.
Sertakan insight actionable, bukan sekadar angka.
Gunakan format **Markdown** agar output rapi: ## untuk subjudul, **bold** untuk sorotan, --- untuk pemisah.
Gunakan bahasa Indonesia profesional tapi tidak kaku.
Berikan rekomendasi konkret yang bisa langsung dijalankan."""
}

# ═══════════════════════════════════════════════════════════════
# 7. HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def create_jwt_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    username = verify_jwt_token(credentials.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="Token tidak valid atau sudah expired")
    return username


def embed_text(text: str) -> list:
    try:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_query"
        )
        return result["embedding"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal embed teks: {e}")


def query_astra(vector: list, category_filter: List[str], top_k: int = 5):
    """Cari chunk yang mirip di AstraDB dengan filter kategori."""
    try:
        # astrapy v2: find() returns cursor, convert to list
        cursor = collection.find(
            filter={"metadata.category": {"$in": category_filter}},
            sort={"$vector": vector},
            limit=top_k,
            include_similarity=True
        )
        return list(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal query AstraDB: {str(e)}")


def build_prompt(query: str, chunks: list, mode: str) -> str:
    system = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["assistant"])
    
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        text = chunk.get("text", "")
        source = chunk.get("metadata", {}).get("source", "unknown")
        context_parts.append(f"[DOKUMEN {i} - {source}]\n{text}")

    context = "\n\n".join(context_parts) if context_parts else "Tidak ada dokumen relevan ditemukan."
    
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
    try:
        response = chat_model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal generate jawaban: {str(e)}")


# ═══════════════════════════════════════════════════════════════
# 8. RAG PIPELINE
# ═══════════════════════════════════════════════════════════════

def rag_pipeline(query: str, mode: str, user_type: str = "public") -> dict:
    query_embedding = embed_text(query)
    
    if user_type == "public":
        category_filter = ["public"]
    else:
        category_filter = ["public", "internal"]
    
    chunks = query_astra(query_embedding, category_filter, top_k=5)
    prompt = build_prompt(query, chunks, mode)
    reply = generate_reply(prompt)
    
    sources = list(set(
        chunk.get("metadata", {}).get("source", "unknown") 
        for chunk in chunks
    ))
    
    return {"reply": reply, "sources": sources if sources else None}


# ═══════════════════════════════════════════════════════════════
# 9. API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/api/auth/login")
def login(request: LoginRequest):
    if request.username != ADMIN_USERNAME or request.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    token = create_jwt_token(request.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"username": ADMIN_USERNAME, "nama": "Admin Horizon"}
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat_public(request: ChatRequest):
    result = rag_pipeline(query=request.message, mode="assistant", user_type="public")
    return ChatResponse(reply=result["reply"], sources=result["sources"])


@app.post("/api/workspace/chat", response_model=ChatResponse)
def chat_workspace(request: ChatRequest, username: str = Depends(get_current_user)):
    if request.mode not in ["assistant", "draft", "insight"]:
        raise HTTPException(status_code=400, detail="Mode harus: assistant, draft, atau insight")
    
    result = rag_pipeline(query=request.message, mode=request.mode, user_type="business")
    return ChatResponse(reply=result["reply"], sources=result["sources"])


# ═══════════════════════════════════════════════════════════════
# 10. RUN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("APP_ENV", "development") == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
