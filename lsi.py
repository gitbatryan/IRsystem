import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

# 1. 문서 읽기
def load_documents(folder_path):
    documents = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                filenames.append(filename)
    return documents, filenames

# 2. TF-IDF 벡터라이즈
def build_tfidf_matrix(documents):
    vectorizer = TfidfVectorizer(lowercase=True, stop_words=None)
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer

# 3. SVD를 통한 LSI (차원 축소)
def apply_lsi(tfidf_matrix, n_components=10):
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    lsi_matrix = svd.fit_transform(tfidf_matrix)
    return lsi_matrix, svd

# 4. 쿼리 처리
def transform_query(query, vectorizer, svd):
    query_vec = vectorizer.transform([query])
    query_lsi = svd.transform(query_vec)
    return query_lsi

# 5. 코사인 유사도 계산 및 정렬
def rank_documents(query_lsi, lsi_matrix, filenames):
    similarities = cosine_similarity(query_lsi, lsi_matrix)[0]
    ranked_indices = np.argsort(similarities)[::-1]
    ranked_files = [(filenames[i], similarities[i]) for i in ranked_indices]
    return ranked_files

# 메인 함수
def main():
    folder_path = os.path.join(os.path.dirname(__file__), 'lsi_dataset', 'test_dataset')
    documents, filenames = load_documents(folder_path)
    tfidf_matrix, vectorizer = build_tfidf_matrix(documents)
    lsi_matrix, svd = apply_lsi(tfidf_matrix, n_components=10)

    print("검색을 시작합니다. (종료하려면 'exit' 입력)")
    while True:
        query = input("\n검색할 쿼리를 입력하세요: ")
        if query.lower() == 'exit':
            print("검색을 종료합니다.")
            break

        query_lsi = transform_query(query, vectorizer, svd)
        ranked_files = rank_documents(query_lsi, lsi_matrix, filenames)

        print("\n검색 결과 : ")
        for rank, (filename, score) in enumerate(ranked_files[:10], start=1):
            print(f"{rank}. {filename}: {score:.4f}")

if __name__ == "__main__":
    main()
