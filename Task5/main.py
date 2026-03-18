from vector_search import load_all_lemma_files, vector_search_multi

if __name__ == '__main__':
    tf_idf, idf = load_all_lemma_files("../Task4/Task4Results/lemmas")

    while True:
        query = input("\nВведите запрос (или пусто для выхода): ").strip()
        if not query:
            break

        vector_search_multi(
            queries=[query],
            tf_idf=tf_idf,
            idf=idf
        )