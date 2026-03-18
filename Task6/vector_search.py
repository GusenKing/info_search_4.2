import math
import re
from collections import Counter
from pymystem3 import Mystem
from pathlib import Path

mystem = Mystem()
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+")

def load_all_lemma_files(folder="../Task4/Task4Results/lemmas"):
    tf_idf: dict[str, dict[str, float]] = {}
    idf: dict[str, float] = {}

    folder_path = Path(folder)

    for file_path in folder_path.glob("*_леммы.txt"):
        # print("Нашли файл лемм:", file_path)
        doc_name = file_path.stem  # имя файла без .txt
        doc_vector: dict[str, float] = {}

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) < 3:
                    continue

                lemma = parts[0]
                idf_value = float(parts[1])     # 2-й столбец
                tf_idf_value = float(parts[2])  # 3-й столбец

                doc_vector[lemma] = tf_idf_value

                # idf для термина одинаковый во всех документах, достаточно взять один раз
                if lemma not in idf:
                    idf[lemma] = idf_value

        tf_idf[doc_name] = doc_vector

    # print("Всего документов:", len(tf_idf))
    # print("Всего термов в idf:", len(idf))
    return tf_idf, idf



def lemmatize_query(text: str) -> list[str]:
    clean_text = " ".join(WORD_RE.findall(text.lower()))
    lemmas = mystem.lemmatize(clean_text)

    result = []
    for lemma in lemmas:
        lemma = lemma.strip()
        if lemma:
            result.append(lemma)

    return result


def build_query_vector(query: str, idf: dict[str, float]) -> dict[str, float]:
    terms = lemmatize_query(query)
    counts = Counter(term for term in terms if term in idf)

    total = sum(counts.values())
    if total == 0:
        return {}

    query_vector = {}
    for term, count in counts.items():
        tf = count / total
        query_vector[term] = tf * idf[term]

    return query_vector


def compute_cosine_similarity(doc: str, doc_vector: dict[str, float], query_vector: dict[str, float]) -> float:
    if not doc_vector or not query_vector:
        return 0.0

    common_words = set(doc_vector.keys()) & set(query_vector.keys())
    dot_product = sum(doc_vector[word] * query_vector[word] for word in common_words)

    norm_query = math.sqrt(sum(v * v for v in query_vector.values()))
    norm_doc = math.sqrt(sum(v * v for v in doc_vector.values()))

    if norm_query == 0 or norm_doc == 0:
        return 0.0

    return dot_product / (norm_query * norm_doc)

def search_one_query(query: str, tf_idf: dict[str, dict[str, float]], idf: dict[str, float]):
    query_vector = build_query_vector(query, idf)
    scores: dict[str, float] = {}

    for doc, doc_vector in tf_idf.items():
        score = compute_cosine_similarity(doc, doc_vector, query_vector)
        scores[doc] = score

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = [(doc, score) for doc, score in sorted_scores if score > 0][:10]
    return results
