import math
import os
import itertools
from collections import Counter
from collections import defaultdict

TOKEN_FILENAME_SUFFIX = '_токены.txt'
LEMMA_FILENAME_SUFFIX = '_леммы.txt'


def load_token_documents(folder_path):
    documents = {}

    if not os.path.exists(folder_path):
        raise FileNotFoundError(folder_path)

    listed_files = os.listdir(folder_path)
    listed_files.remove("index_токены.txt")

    token_files = filter(lambda x: x.endswith(TOKEN_FILENAME_SUFFIX), listed_files)
    token_files = list(token_files)
    for filename in token_files:
        path = os.path.join(folder_path, filename)

        with open(path, encoding="utf-8") as f:
            tokens = f.read().lower().split()

        documents[filename] = tokens

    return documents


def load_lemma_documents(folder_path):
    documents = {}

    if not os.path.exists(folder_path):
        raise FileNotFoundError(folder_path)

    listed_files = os.listdir(folder_path)
    listed_files.remove("index_леммы.txt")

    token_files = filter(lambda x: x.endswith(LEMMA_FILENAME_SUFFIX), listed_files)
    token_files = list(token_files)
    for filename in token_files:
        path = os.path.join(folder_path, filename)
        lemmas = []

        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip().lower()

                if not line:
                    continue

                lemma = line.split()
                lemmas.append(lemma)

        documents[filename] = lemmas

    return documents


def compute_tf_for_tokens(documents):
    tf = {}

    for doc, tokens in documents.items():
        counts = Counter(tokens)

        tf[doc] = {
            term: count
            for term, count in counts.items()
        }

    return tf


def compute_tf_for_lemmas(lemma_documents):
    tf = {}

    for doc, lemmas in lemma_documents.items():
        flattened_lemmas = list(itertools.chain.from_iterable(lemmas))
        counts = Counter(flattened_lemmas)
        tf[doc] = {}

        for lemma_with_tokens in lemmas:
            lemma = lemma_with_tokens[0]
            tokens = lemma_with_tokens[1:]
            lemma_counter = 0

            for token in tokens:
                lemma_counter += counts[token]

            tf[doc][lemma] = lemma_counter

    return tf


def compute_idf_for_tokens(documents):
    df = defaultdict(int)

    for tokens in documents.values():
        unique_terms = set(tokens)
        for term in unique_terms:
            df[term] += 1

    n = len(documents)

    idf = {
        term: math.log(n / freq)
        for term, freq in df.items()
    }

    return idf


def compute_idf_for_lemmas(documents):
    df = defaultdict(int)

    for lemmas in documents.values():
        for lemma_with_tokens in lemmas:
            lemma = lemma_with_tokens[0]
            tokens = lemma_with_tokens[1:]

            unique_tokens = set(tokens)
            for _ in unique_tokens:
                df[lemma] += 1

    n = len(documents)

    idf = {
        lemma: math.log(n / freq)
        for lemma, freq in df.items()
    }

    return idf



def calculate_tf_and_idf_for_tokens(input_dir):
    token_documents = load_token_documents(input_dir)
    token_tf = compute_tf_for_tokens(token_documents)
    token_idf = compute_idf_for_tokens(token_documents)

    return token_tf, token_idf


def calculate_tf_and_idf_for_lemmas(input_dir):
    lemma_documents = load_lemma_documents(input_dir)
    lemma_tf = compute_tf_for_lemmas(lemma_documents)
    lemma_idf = compute_idf_for_lemmas(lemma_documents)

    return lemma_tf, lemma_idf
