"""
Step 4 + 5: Retrieval, re-ranking, and generation pipeline.
Usage: python rag_pipeline.py "your question here"
"""

import sys
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "docs_mpnet"       # the better-performing embedding model, decide after comparison
EMBEDDING_MODEL = "all-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"  # swap to a smaller model if this is too heavy locally

TOP_K_RETRIEVE = 8   # how many chunks to pull initially
TOP_K_RERANK = 3     # how many to keep after re-ranking


def retrieve(question, embed_model, collection, top_k=TOP_K_RETRIEVE):
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    return list(zip(docs, metadatas))


def rerank(question, retrieved, reranker, top_k=TOP_K_RERANK):
    pairs = [(question, doc) for doc, _ in retrieved]
    scores = reranker.predict(pairs)
    scored = list(zip(scores, retrieved))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def generate_answer(question, context_chunks, tokenizer, llm):
    context_text = "\n\n".join([f"[Source: {meta['source']}]\n{doc}" for doc, meta in context_chunks])

    prompt = f"""You are a helpful assistant answering questions about a machine learning project called "alzheimer-app".
Use ONLY the context below to answer. If the answer isn't in the context, say you don't know.

Context:
{context_text}

Question: {question}

Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    with torch.no_grad():
        output = llm.generate(**inputs, max_new_tokens=200, temperature=0.3, do_sample=True)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    # Strip the prompt echo, keep only the generated part
    answer = answer.split("Answer:")[-1].strip()
    return answer


def main():
    if len(sys.argv) < 2:
        print('Usage: python rag_pipeline.py "your question here"')
        sys.exit(1)

    question = sys.argv[1]
    print(f"Question: {question}\n")

    print("Loading models (first run downloads them, may take a few minutes)...")
    embed_model = SentenceTransformer(EMBEDDING_MODEL)
    reranker = CrossEncoder(RERANKER_MODEL)
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    llm = AutoModelForCausalLM.from_pretrained(LLM_MODEL, torch_dtype=torch.float32)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    print("Retrieving relevant chunks...")
    retrieved = retrieve(question, embed_model, collection)

    print("Re-ranking...")
    reranked = rerank(question, retrieved, reranker)

    print("\nTop chunks used for answer:")
    for score, (doc, meta) in reranked:
        print(f"  [{score:.3f}] {meta['source']}: {doc[:80]}...")

    print("\nGenerating answer...")
    context_chunks = [(doc, meta) for _, (doc, meta) in reranked]
    answer = generate_answer(question, context_chunks, tokenizer, llm)

    print(f"\n{'='*50}\nANSWER:\n{answer}\n{'='*50}")


if __name__ == "__main__":
    main()
