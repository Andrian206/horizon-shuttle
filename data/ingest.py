"""
Horizon Shuttle AI — Ingestion Script
Baca file .txt di folder data/, chunk, embed, simpan ke AstraDB.
Jalankan SEKALI sebelum demo.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
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

# ═══════════════════════════════════════════════════════════════
# 2. INIT GEMINI & ASTRADB
# ═══════════════════════════════════════════════════════════════
genai.configure(api_key=GEMINI_API_KEY)
embedding_model = genai.GenerativeModel("models/gemini-embedding-001")

astra_client = DataAPIClient(ASTRA_TOKEN)
db = astra_client.get_database_by_api_endpoint(ASTRA_ENDPOINT)

# Buat collection kalau belum ada
try:
    collection = db.get_collection(ASTRA_COLLECTION)
    print(f"✅ Collection '{ASTRA_COLLECTION}' sudah ada")
except:
    collection = db.create_collection(
        ASTRA_COLLECTION,
        dimension=768,  # Gemini Embedding 001 default
        metric="cosine"
    )
    print(f"✅ Collection '{ASTRA_COLLECTION}' dibuat baru")

# ═══════════════════════════════════════════════════════════════
# 3. KONFIGURASI CHUNKING
# ═══════════════════════════════════════════════════════════════

# Mapping: nama file → metadata
# category: "public" (bisa diakses public AI) atau "internal" (hanya workspace)
FILE_CONFIG = {
    "01_company_profile.txt":        {"source": "company_profile",        "category": "public"},
    "02_service_catalog.txt":        {"source": "service_catalog",        "category": "public"},
    "03_route_schedule.txt":         {"source": "route_schedule",         "category": "public"},
    "04_fleet_info.txt":             {"source": "fleet_info",             "category": "public"},
    "05_faq.txt":                    {"source": "faq",                    "category": "public"},
    "06_company_policies.txt":       {"source": "company_policies",       "category": "public"},
    "07_cs_sop.txt":                 {"source": "cs_sop",                 "category": "internal"},
    "08_marketing_guideline.txt":    {"source": "marketing_guideline",    "category": "internal"},
    "09_promotional_campaign.txt":   {"source": "promotional_campaign",   "category": "public"},
    "10_business_reports.txt":       {"source": "business_reports",       "category": "internal"},
    "11_customer_reviews.txt":       {"source": "customer_reviews",       "category": "internal"},
    "12_internal_sop.txt":           {"source": "internal_sop",           "category": "internal"},
}
"""
Horizon Shuttle AI — Ingestion Script
Baca file .txt di folder data/, chunk, embed, simpan ke AstraDB.
Jalankan SEKALI sebelum demo.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
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

# ═══════════════════════════════════════════════════════════════
# 2. INIT GEMINI & ASTRADB
# ═══════════════════════════════════════════════════════════════
genai.configure(api_key=GEMINI_API_KEY)
embedding_model = genai.GenerativeModel("models/gemini-embedding-001")

astra_client = DataAPIClient(ASTRA_TOKEN)
db = astra_client.get_database_by_api_endpoint(ASTRA_ENDPOINT)

# Buat collection kalau belum ada
try:
    collection = db.get_collection(ASTRA_COLLECTION)
    print(f"✅ Collection '{ASTRA_COLLECTION}' sudah ada")
except:
    collection = db.create_collection(
        ASTRA_COLLECTION,
        dimension=768,  # Gemini Embedding 001 default
        metric="cosine"
    )
    print(f"✅ Collection '{ASTRA_COLLECTION}' dibuat baru")

# ═══════════════════════════════════════════════════════════════
# 3. KONFIGURASI CHUNKING
# ═══════════════════════════════════════════════════════════════

# Mapping: nama file → metadata
# category: "public" (bisa diakses public AI) atau "internal" (hanya workspace)
FILE_CONFIG = {
    "01_company_profile.txt":        {"source": "company_profile",        "category": "public"},
    "02_service_catalog.txt":        {"source": "service_catalog",        "category": "public"},
    "03_route_schedule.txt":         {"source": "route_schedule",         "category": "public"},
    "04_fleet_info.txt":             {"source": "fleet_info",             "category": "public"},
    "05_faq.txt":                    {"source": "faq",                    "category": "public"},
    "06_company_policies.txt":       {"source": "company_policies",       "category": "public"},
    "07_cs_sop.txt":                 {"source": "cs_sop",                 "category": "internal"},
    "08_marketing_guideline.txt":    {"source": "marketing_guideline",    "category": "internal"},
    "09_promotional_campaign.txt":   {"source": "promotional_campaign",   "category": "public"},
    "10_business_reports.txt":       {"source": "business_reports",       "category": "internal"},
    "11_customer_reviews.txt":       {"source": "customer_reviews",       "category": "internal"},
    "12_internal_sop.txt":           {"source": "internal_sop",           "category": "internal"},
}

CHUNK_SIZE = 500      # karakter per chunk
CHUNK_OVERLAP = 100   # overlap antar chunk


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    """
    Potong teks jadi chunk-chunk dengan overlap.
    
    Contoh:
    Teks: "ABCDEFGHIJ", chunk_size=4, overlap=1
    → ["ABCD", "DEFG", "GHIJ"]
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Jangan ambil chunk terlalu pendek di akhir
        if len(chunk) < 100 and chunks:
            # Gabung ke chunk sebelumnya
            chunks[-1] += " " + chunk
            break
            
        chunks.append(chunk.strip())
        start = end - overlap  # overlap untuk konteks
    
    return chunks


def embed_text(text: str) -> list:
    """Ubah teks jadi vector embedding."""
    result = embedding_model.embed_content(content=text)
    return result.embedding


def ingest_file(filepath: Path, config: dict):
    """
    Baca 1 file, chunk, embed, simpan ke AstraDB.
    """
    print(f"\\n📄 Processing: {filepath.name}")
    
    # Baca file
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    if not text.strip():
        print(f"   ⚠️ File kosong, skip")
        return 0
    
    # Chunking
    chunks = chunk_text(text)
    print(f"   📝 {len(chunks)} chunks dibuat")
    
    # Embed & insert ke AstraDB
    inserted = 0
    for i, chunk_text_content in enumerate(chunks):
        try:
            embedding = embed_text(chunk_text_content)
            
            document = {
                "text": chunk_text_content,
                "$vector": embedding,
                "metadata": {
                    "source": config["source"],
                    "category": config["category"],
                    "filename": filepath.name,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            }
            
            collection.insert_one(document)
            inserted += 1
            
        except Exception as e:
            print(f"   ❌ Gagal insert chunk {i}: {e}")
    
    print(f"   ✅ {inserted}/{len(chunks)} chunks berhasil disimpan")
    return inserted


def main():
    """Main ingestion loop."""
    data_dir = Path("data")
    
    if not data_dir.exists():
        print(f"❌ Folder '{data_dir}' tidak ditemukan!")
        print("   Buat folder 'data/' dan isi dengan file .txt")
        return
    
    # Cek file yang ada
    txt_files = sorted(data_dir.glob("*.txt"))
    print(f"📁 Ditemukan {len(txt_files)} file .txt")
    
    total_chunks = 0
    
    for filepath in txt_files:
        filename = filepath.name
        
        if filename not in FILE_CONFIG:
            print(f"\\n⚠️ {filename} tidak ada di config, skip (tambahkan ke FILE_CONFIG)")
            continue
        
        config = FILE_CONFIG[filename]
        inserted = ingest_file(filepath, config)
        total_chunks += inserted
    
    print(f"\\n🎉 SELESAI! Total {total_chunks} chunks disimpan ke AstraDB")
    print(f"   Collection: {ASTRA_COLLECTION}")
    print(f"   Namespace: {ASTRA_NAMESPACE}")


if __name__ == "__main__":
    main()
CHUNK_SIZE = 500      # karakter per chunk
CHUNK_OVERLAP = 100   # overlap antar chunk


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    """
    Potong teks jadi chunk-chunk dengan overlap.
    
    Contoh:
    Teks: "ABCDEFGHIJ", chunk_size=4, overlap=1
    → ["ABCD", "DEFG", "GHIJ"]
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Jangan ambil chunk terlalu pendek di akhir
        if len(chunk) < 100 and chunks:
            # Gabung ke chunk sebelumnya
            chunks[-1] += " " + chunk
            break
            
        chunks.append(chunk.strip())
        start = end - overlap  # overlap untuk konteks
    
    return chunks


def embed_text(text: str) -> list:
    """Ubah teks jadi vector embedding."""
    result = embedding_model.embed_content(content=text)
    return result.embedding


def ingest_file(filepath: Path, config: dict):
    """
    Baca 1 file, chunk, embed, simpan ke AstraDB.
    """
    print(f"\\n📄 Processing: {filepath.name}")
    
    # Baca file
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    if not text.strip():
        print(f"   ⚠️ File kosong, skip")
        return 0
    
    # Chunking
    chunks = chunk_text(text)
    print(f"   📝 {len(chunks)} chunks dibuat")
    
    # Embed & insert ke AstraDB
    inserted = 0
    for i, chunk_text_content in enumerate(chunks):
        try:
            embedding = embed_text(chunk_text_content)
            
            document = {
                "text": chunk_text_content,
                "$vector": embedding,
                "metadata": {
                    "source": config["source"],
                    "category": config["category"],
                    "filename": filepath.name,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            }
            
            collection.insert_one(document)
            inserted += 1
            
        except Exception as e:
            print(f"   ❌ Gagal insert chunk {i}: {e}")
    
    print(f"   ✅ {inserted}/{len(chunks)} chunks berhasil disimpan")
    return inserted


def main():
    """Main ingestion loop."""
    data_dir = Path("data")
    
    if not data_dir.exists():
        print(f"❌ Folder '{data_dir}' tidak ditemukan!")
        print("   Buat folder 'data/' dan isi dengan file .txt")
        return
    
    # Cek file yang ada
    txt_files = sorted(data_dir.glob("*.txt"))
    print(f"📁 Ditemukan {len(txt_files)} file .txt")
    
    total_chunks = 0
    
    for filepath in txt_files:
        filename = filepath.name
        
        if filename not in FILE_CONFIG:
            print(f"\\n⚠️ {filename} tidak ada di config, skip (tambahkan ke FILE_CONFIG)")
            continue
        
        config = FILE_CONFIG[filename]
        inserted = ingest_file(filepath, config)
        total_chunks += inserted
    
    print(f"\\n🎉 SELESAI! Total {total_chunks} chunks disimpan ke AstraDB")
    print(f"   Collection: {ASTRA_COLLECTION}")
    print(f"   Namespace: {ASTRA_NAMESPACE}")


if __name__ == "__main__":
    main()