from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, chat_public, chat_workspace, admin
from models.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Horizon Shuttle AI")

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS (kalau frontend terpisah nanti)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_public.router, prefix="/api/chat", tags=["chat-public"])
app.include_router(chat_workspace.router, prefix="/api/workspace", tags=["chat-workspace"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Horizon Shuttle AI API"}