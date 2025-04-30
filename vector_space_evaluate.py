# evaluate.py
import os
import json
from vector_space import load_documents, compute_tfidf, build_query_vector, cosine_similarity

GT_PATH = os.path.join(os.path.dirname(__file__), 'ground_truth_test')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'lsi_dataset', 'test_dataset')

def load_ground_truth(query):
    filename = query.strip().replace(" ", "_") + ".txt"
    gt_file = os.path.join(GT_PATH, filename)
    if not os.path.exists(gt_file):
        return None
    with open(gt_file, 'r', encoding='utf-8') as f:
        return set(json.load(f))

def evaluate(retrieved, ground_truth):
    retrieved = set(retrieved)
    relevant = set(ground_truth)

    tp = len(retrieved & relevant)
    fp = len(retrieved - relevant)
    fn = len(relevant - retrieved)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
    return precision, recall, f1, tp, fp, fn

def main():
    print("Vector Space Model입니다.")
    print("type 'exit' to quit")

    documents, df = load_documents(DATASET_PATH)
    N = len(documents)
    tfidf_vectors = compute_tfidf(documents, df, N)

    while True:
        query = input("\nEnter query (ex: apple banana): ").strip()
        if query.lower() in ('exit', 'quit'):
            print("Bye!")
            break

        try:
            query_vector = build_query_vector(query, df, N)
            scores = []
            for doc_name, doc_vector in tfidf_vectors.items():
                sim = cosine_similarity(query_vector, doc_vector)
                scores.append((doc_name, sim))

            # top-k 문서 선택
            top_docs = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
            result_docs = [doc for doc, score in top_docs]  # 무조건 10개 출력

            print(f"\n🔍 Retrieved top {len(result_docs)} document(s) with similarity scores:")
            for rank, (doc, score) in enumerate(top_docs, 1):
                print(f" {rank:2d}. {doc:50s} (score: {score:.4f})")

            # 정답 불러오기
            gt = load_ground_truth(query)
            if gt is None:
                print("\n⚠️ Ground truth not found for this query.")
            else:
                matched = sorted(set(result_docs) & gt)
                if matched:
                    print(f"\n✅ Matched {len(matched)} document(s):")
                    for doc in matched:
                        print(f" ✔ {doc}")
                else:
                    print("\n❌ No matched documents with ground truth.")

                precision, recall, f1, tp, fp, fn = evaluate(result_docs, gt)
                print("\n📊 Evaluation:")
                print(f" - TP: {tp}")
                print(f" - FP: {fp}")
                print(f" - FN: {fn}")
                print(f" - Precision: {precision:.4f}")
                print(f" - Recall:    {recall:.4f}")
                print(f" - F1 Score:  {f1:.4f}")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()