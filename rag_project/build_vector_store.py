"""
Step 3: Embed chunks and store in ChromaDB.
Builds two collections using two different embedding models, so you can compare retrieval quality.
Usage: python build_vector_store.py
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "chunks.json"
CHROMA_DIR = "chroma_db"
CHUNK_STRATEGY = "markdown_header"  # switch to "fixed_size" to compare

# Two embedding models to compare
EMBEDDING_MODELS = {
    "minilm": "all-MiniLM-L6-v2",          # small, fast, 384-dim
    "mpnet": "all-mpnet-base-v2",          # larger, slower, 768-dim, often better quality
}


def load_chunks():
    with open(CHUNKS_FILE, "r") as f:
        data = json.load(f)
    return data[CHUNK_STRATEGY]


def build_collection(client, model_key, model_name, chunks):
    print(f"\nBuilding collection for '{model_key}' ({model_name})...")
    model = SentenceTransformer(model_name)

    collection_name = f"docs_{model_key}"
    # Delete if exists, so re-runs are clean
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    collection = client.create_collection(collection_name)

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    ids = [f"{model_key}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": c["source"], "strategy": c["strategy"]} for c in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )
    print(f"Added {len(texts)} chunks to collection '{collection_name}'")
    return collection


def main():
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks using '{CHUNK_STRATEGY}' strategy")

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    for model_key, model_name in EMBEDDING_MODELS.items():
        build_collection(client, model_key, model_name, chunks)

    print("\nDone. Vector store saved to ./chroma_db/")
    print("You now have two collections: docs_minilm and docs_mpnet")


if __name__ == "__main__":
    main()
