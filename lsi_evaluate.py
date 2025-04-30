import os
import json
from lsi import load_documents, build_tfidf_matrix, apply_lsi, transform_query, rank_documents

GT_PATH = os.path.join(os.path.dirname(__file__), 'ground_truth_Korea')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'lsi_dataset', 'Korea')

def load_ground_truth(query):
    filename = query.strip().replace(" ", "_") + ".txt"
    gt_file = os.path.join(GT_PATH, filename)
    if not os.path.exists(gt_file):
        return None
    with open(gt_file, 'r', encoding='utf-8') as f:
        return set(json.load(f))

def evaluate(retrieved, ground_truth):
    retrieved_set = set([doc for doc, _ in retrieved])
    relevant = set(ground_truth)

    tp = len(retrieved_set & relevant)
    fp = len(retrieved_set - relevant)
    fn = len(relevant - retrieved_set)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
    return precision, recall, f1, tp, fp, fn

def main():
    print("📌 LSI 모델입니다.")
    print("type 'exit' to quit")

    documents, filenames = load_documents(DATASET_PATH)
    tfidf_matrix, vectorizer = build_tfidf_matrix(documents)
    lsi_matrix, svd = apply_lsi(tfidf_matrix, n_components=2)

    while True:
        query = input("\nEnter query (ex: apple banana): ").strip()
        if query.lower() in ('exit', 'quit'):
            print("Bye!")
            break

        try:
            query_lsi = transform_query(query, vectorizer, svd)
            ranked_files = rank_documents(query_lsi, lsi_matrix, filenames)

            # top-k 문서 선택 및 점수 필터링
            top_docs = ranked_files[:10]
            result_docs = [(doc, score) for doc, score in top_docs if score > 0]

            print(f"\n🔍 Retrieved {len(result_docs)} document(s) with similarity scores:")
            for rank, (doc, score) in enumerate(result_docs, 1):
                print(f" {rank:2d}. {doc:50s} (score: {score:.4f})")

            # 정답 불러오기
            gt = load_ground_truth(query)
            if gt is None:
                print("\n⚠️ Ground truth not found for this query.")
            else:
                matched = sorted(set([doc for doc, _ in result_docs]) & gt)
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
