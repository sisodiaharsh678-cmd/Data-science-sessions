"""
Real comparison: MiniLM vs MPNet embedding models.
Uses the cross-encoder reranker as an objective relevance judge -
for each test question, retrieves top chunks from BOTH collections,
then scores them with the SAME cross-encoder, so we get a fair,
comparable relevance score for each embedding model.

Usage: python compare_embeddings.py
"""

from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

CHROMA_DIR = "chroma_db"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

MODELS = {
    "minilm": ("all-MiniLM-L6-v2", "docs_minilm"),
    "mpnet": ("all-mpnet-base-v2", "docs_mpnet"),
}

# A handful of realistic test questions about your actual project files
TEST_QUESTIONS = [
    "What accuracy did the Alzheimer's detection model achieve?",
    "What machine learning models were used in this project?",
    "What library was used to build the dashboard?",
    "How was the data preprocessed?",
    "What evaluation metrics were used?",
]

TOP_K = 5


def main():
    print("Loading reranker (objective judge)...")
    reranker = CrossEncoder(RERANKER_MODEL)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    results_by_model = {}

    for model_key, (model_name, collection_name) in MODELS.items():
        print(f"\nLoading embedding model: {model_name}...")
        embed_model = SentenceTransformer(model_name)
        collection = client.get_collection(collection_name)

        all_scores = []

        for question in TEST_QUESTIONS:
            query_embedding = embed_model.encode([question]).tolist()
            retrieved = collection.query(query_embeddings=query_embedding, n_results=TOP_K)
            docs = retrieved["documents"][0]

            if not docs:
                continue

            # Score each retrieved chunk against the question using the SAME reranker
            pairs = [(question, doc) for doc in docs]
            scores = reranker.predict(pairs)

            top_score = max(scores)
            avg_score = sum(scores) / len(scores)
            all_scores.append((question, top_score, avg_score))

        results_by_model[model_key] = all_scores

    # Print comparison
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS (higher cross-encoder score = more relevant)")
    print("=" * 70)

    for question_idx, question in enumerate(TEST_QUESTIONS):
        print(f"\nQ: {question}")
        for model_key in MODELS:
            q, top_score, avg_score = results_by_model[model_key][question_idx]
            print(f"  {model_key:8s} -> top_score: {top_score:.3f} | avg_score: {avg_score:.3f}")

    # Overall averages
    print("\n" + "=" * 70)
    print("OVERALL AVERAGE (across all test questions)")
    print("=" * 70)
    for model_key, scores in results_by_model.items():
        overall_top = sum(s[1] for s in scores) / len(scores)
        overall_avg = sum(s[2] for s in scores) / len(scores)
        print(f"{model_key:8s} -> avg top_score: {overall_top:.3f} | avg avg_score: {overall_avg:.3f}")

    # Declare winner
    minilm_avg = sum(s[1] for s in results_by_model["minilm"]) / len(results_by_model["minilm"])
    mpnet_avg = sum(s[1] for s in results_by_model["mpnet"]) / len(results_by_model["mpnet"])

    print("\n" + "=" * 70)
    if mpnet_avg > minilm_avg:
        diff = ((mpnet_avg - minilm_avg) / abs(minilm_avg)) * 100 if minilm_avg != 0 else 0
        print(f"WINNER: mpnet (higher relevance score by {diff:.1f}%)")
    elif minilm_avg > mpnet_avg:
        diff = ((minilm_avg - mpnet_avg) / abs(mpnet_avg)) * 100 if mpnet_avg != 0 else 0
        print(f"WINNER: minilm (higher relevance score by {diff:.1f}%)")
    else:
        print("TIE: both models performed equally")
    print("=" * 70)


if __name__ == "__main__":
    main()
