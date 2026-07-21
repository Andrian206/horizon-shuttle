from astrapy import DataAPIClient
import os

ASTRA_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE")
COLLECTION = os.getenv("ASTRA_DB_COLLECTION")

client = DataAPIClient(ASTRA_TOKEN)
db = client.get_database_by_api_endpoint(ASTRA_ENDPOINT)
collection = db.get_collection(COLLECTION)

def query_similar_chunks(query_embedding: list, category_filter: list, top_k: int = 5):
    """
    Cari chunk yang mirip dengan query embedding.
    category_filter: ["public"] atau ["public", "internal"]
    """
    results = collection.find(
        filter={"metadata.category": {"$in": category_filter}},
        sort={"$vector": query_embedding},
        limit=top_k,
        include_similarity=True
    )
    return list(results)