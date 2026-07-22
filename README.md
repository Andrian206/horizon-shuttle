<div align="center">

# 🚌 Horizon Shuttle AI

**RAG-Powered AI Chatbot untuk Horizon Shuttle**

*Asisten virtual berbasis AI yang menjawab pertanyaan pelanggan berdasarkan knowledge base perusahaan.*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![AstraDB](https://img.shields.io/badge/AstraDB-Vector-000000?style=for-the-badge)](https://astra.datastax.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

</div>

---

## 📖 Tentang

Horizon Shuttle AI adalah aplikasi **RAG (Retrieval-Augmented Generation)** yang dibangun untuk perusahaan transportasi shuttle "Horizon Shuttle". AI ini menjawab pertanyaan pelanggan secara **otomatis dan akurat** dengan mengambil informasi langsung dari knowledge base perusahaan (SOP, jadwal, harga, FAQ, dll).

### Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🤖 **Public Chat** | Chat tanpa login — tanya tentang layanan, jadwal, harga, dll |
| 💼 **Business Workspace** | Chat berbasis 3 mode (Assistant, Draft, Insight) dengan akses internal |
| 🔐 **JWT Authentication** | Login admin hardcode untuk akses workspace |
| 🧠 **RAG Pipeline** | Gemini embedding + AstraDB vector search → jawaban kontekstual |
| 📱 **Responsive UI** | Glassmorphism design, mobile-friendly, animasi lembut |
| 🐳 **Docker Ready** | DockerFile untuk container deployment |
| ☁️ **Render Deploy** | Konfigurasi siap deploy ke Render.com |

---

## 🏗️ Arsitektur

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND (HTML)                   │
│  index.html → chat.html / login.html → workspace.html│
└──────────────────────┬──────────────────────────────┘
                       │ fetch API
┌──────────────────────▼──────────────────────────────┐
│                FastAPI Backend (main.py)              │
│  POST /api/chat          (public — no auth)         │
│  POST /api/workspace/chat (workspace — JWT auth)    │
│  POST /api/auth/login    (JWT token)                │
└─────┬──────────────────────┬────────────────────────┘
      │                      │
┌─────▼──────┐      ┌───────▼───────┐
│  Gemini AI │      │   AstraDB     │
│ Embedding  │──────▶  Vector DB    │
│ + LLM      │      │ (5 nearest)   │
└────────────┘      └───────────────┘
```

### RAG Pipeline Flow

```
User Query
    │
    ▼
┌──────────────────┐
│  Gemini Embedding │  ← Ubah query jadi vector
│  text-embedding-001│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  AstraDB Query   │  ← Cari 5 chunk paling mirip
│  (vector search) │     dengan filter category
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Build Prompt    │  ← Gabungkan chunks + system prompt
│  + Gemini LLM    │     + user query
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  AI Response     │  ← Jawaban berbasis knowledge base
│  (Markdown)      │
└──────────────────┘
```

---

## 📁 Struktur Proyek

```
horizon-shuttle/
│
├── main.py                    # Backend FastAPI (1 file, ~270 baris)
├── requirements.txt           # Python dependencies
├── DockerFile                 # Docker container config
├── .env                       # Environment variables (secret, gitignored)
├── .env.example               # Template untuk .env
├── .gitignore                 # Git ignore rules
│
├── data/                      # Knowledge base
│   ├── 01_company_profile.txt
│   ├── 02_service_catalog.txt
│   ├── 03_route_schedule.txt
│   ├── 04_fleet_info.txt
│   ├── 05_faq.txt
│   ├── 06_company_policies.txt
│   ├── 07_cs_sop.txt          # Internal — hanya workspace
│   ├── 08_marketing_guideline.txt
│   ├── 09_promotional_campaign.txt
│   ├── 10_business_reports.txt # Internal — hanya workspace
│   ├── 11_customer_reviews.txt # Internal — hanya workspace
│   ├── 12_internal_sop.txt     # Internal — hanya workspace
│   ├── generate_data.py        # Script generate sample data
│   └── ingest.py               # Script chunk → embed → upload ke AstraDB
│
└── static/                    # Frontend
    ├── index.html             # Landing page
    ├── chat.html              # Public chat (tanpa login)
    ├── login.html             # Login page
    ├── workspace.html         # Business workspace (3 mode)
    ├── css/
    │   └── style.css          # Legacy CSS (login form)
    └── js/
        ├── auth.js            # Login/logout + JWT session
        └── workspace.js       # Workspace chat logic + sidebar + markdown
```

---

## 🚀 Setup & Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/Andrian206/horizon-shuttle.git
cd horizon-shuttle
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` dan isi dengan values kamu:

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key

# AstraDB
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your_token
ASTRA_DB_API_ENDPOINT=https://your-db-id-us-east-2.apps.astra.datastax.com
ASTRA_DB_NAMESPACE=default_keyspace
ASTRA_DB_COLLECTION=knowledge_chunks

# Admin Auth (hardcode 1 akun)
ADMIN_USERNAME=admin123
ADMIN_PASSWORD=horizon2026

# JWT Secret
JWT_SECRET=your_32char_random_string_here

# App Config (opsional)
APP_ENV=development
```

### 5. Generate Knowledge Base (opsional)

Kalau belum punya data `.txt`, jalankan script generator:

```bash
python data/generate_data.py
```

Ini akan membuat 12 file knowledge base sample di folder `data/`.

### 6. Ingest ke AstraDB

**Jalankan sekali saja** untuk upload chunks ke vector database:

```bash
cd data
python ingest.py
```

Script ini akan:
1. Membaca semua file `.txt` di folder `data/`
2. Memecah teks jadi chunks (500 karakter + 100 overlap)
3. Embedding via Gemini API
4. Upload ke AstraDB collection

### 7. Jalankan Server

```bash
python main.py
```

Buka browser: **http://localhost:8001**

---

## 🔑 API Endpoints

### `POST /api/auth/login`

Login untuk mendapatkan JWT token.

```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin123", "password": "horizon2026"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {"username": "admin123", "nama": "Admin Horizon"}
}
```

---

### `POST /api/chat`

Public chat tanpa authentication. Hanya bisa akses kategori `public`.

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Apa saja layanan Horizon Shuttle?"}'
```

**Response:**
```json
{
  "reply": "Horizon Shuttle menyediakan dua kelas layanan: Economy Class...",
  "sources": ["service_catalog", "fleet_info", "route_schedule"]
}
```

---

### `POST /api/workspace/chat`

Business workspace chat (perlu JWT token). Bisa akses kategori `public` + `internal`.

```bash
curl -X POST http://localhost:8001/api/workspace/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "Buat draft pengumuman keterlambatan", "mode": "draft"}'
```

**Mode:**
| Mode | Deskripsi |
|------|-----------|
| `assistant` | Tanya jawab umum (SOP, kebijakan, informasi internal) |
| `draft` | Buat materi komunikasi (broadcast, caption, email, pengumuman) |
| `insight` | Analisis data dan rekomendasi bisnis |

---

## 🐳 Docker

### Build Image

```bash
docker build -f DockerFile -t horizon-shuttle .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env horizon-shuttle
```

> **Note:** Pastikan env vars sudah ter-set (baik via `.env` file atau Render dashboard).

---

## ☁️ Deploy ke Render

### 1. Push ke GitHub

```bash
git add .
git commit -m "deploy: siap deploy ke Render"
git push origin main
```

### 2. Buat Web Service di Render

1. Login ke [render.com](https://render.com/)
2. Klik **New → Web Service**
3. Connect repository GitHub: `Andrian206/horizon-shuttle`
4. Isi konfigurasi:

| Field | Value |
|-------|-------|
| **Name** | `horizon-shuttle-ai` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |

### 3. Set Environment Variables di Render

| Variable | Value |
|----------|-------|
| `GEMINI_API_KEY` | Dari Google AI Studio |
| `ASTRA_DB_APPLICATION_TOKEN` | `AstraCS:...` dari AstraDB |
| `ASTRA_DB_API_ENDPOINT` | `https://...` dari AstraDB |
| `ASTRA_DB_NAMESPACE` | `default_keyspace` |
| `ASTRA_DB_COLLECTION` | `knowledge_chunks` |
| `ADMIN_USERNAME` | `admin123` |
| `ADMIN_PASSWORD` | `horizon2026` |
| `JWT_SECRET` | Random string 32+ karakter |
| `APP_ENV` | `production` |

### 4. Deploy

Klik **Create Web Service**. Render akan otomatis build dan deploy. Setelah selesai, app bisa diakses di URL yang diberikan Render.

> **Penting:** Pastikan knowledge base sudah di-ingest ke AstraDB sebelum deploy. Run `python data/ingest.py` dari lokal dulu.

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| **Backend** | FastAPI + Uvicorn |
| **AI Model** | Gemini 3.1 Flash Lite |
| **Embedding** | Gemini Embedding 001 (3072 dim) |
| **Vector DB** | AstraDB (DataStax) |
| **Auth** | JWT (python-jose) |
| **Frontend** | Vanilla HTML + Tailwind CSS |
| **Deploy** | Render (via Dockerfile) |

---

## 📝 Development

### Jalankan secara lokal

```bash
# Pastikan .env sudah diisi
python main.py

# Server jalan di http://localhost:8001
# (atau http://localhost:8000 kalau PORT env diset)
```

### Regenerate Knowledge Base

```bash
# Hapus data lama di AstraDB, lalu re-ingest
cd data
python ingest.py
```

### Tambah Dokumen Knowledge Base

1. Buat file `.txt` baru di folder `data/` (contoh: `13_new_doc.txt`)
2. Tambah mapping di `data/ingest.py`:
   ```python
   FILE_CONFIG = {
       ...
       "13_new_doc.txt": {"source": "new_doc", "category": "public"},
   }
   ```
3. Jalankan ulang `python ingest.py`

---

## ⚙️ Konfigurasi

| Variable | Deskripsi | Default |
|----------|-----------|---------|
| `GEMINI_API_KEY` | API key Google Gemini | — |
| `ASTRA_DB_APPLICATION_TOKEN` | AstraDB application token | — |
| `ASTRA_DB_API_ENDPOINT` | AstraDB database endpoint | — |
| `ASTRA_DB_NAMESPACE` | AstraDB keyspace | `default_keyspace` |
| `ASTRA_DB_COLLECTION` | Nama collection vektor | `knowledge_chunks` |
| `ADMIN_USERNAME` | Username login admin | `admin123` |
| `ADMIN_PASSWORD` | Password login admin | `horizon2026` |
| `JWT_SECRET` | Secret key untuk JWT signing | — |
| `PORT` | Port server | `8000` |
| `APP_ENV` | Mode aplikasi | `development` |

---

## 📄 License

Project ini untuk keperluan Horizon Shuttle.

---

<div align="center">

**Made with ❤️ for Horizon Shuttle**

*Powered by Gemini AI · FastAPI · AstraDB*

</div>
