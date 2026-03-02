import os
import json
import utils
from collections import defaultdict

LEMMA_FILENAME_SUFFIX = '_леммы.txt'


def build_inverted_index(folder_path):
    inverted_index = defaultdict(set)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(folder_path)

    listed_files = os.listdir(folder_path)
    listed_files.remove("index_леммы.txt")

    lemma_files = filter(lambda x: x.endswith(LEMMA_FILENAME_SUFFIX), listed_files)
    lemma_files = list(lemma_files)

    for filename in lemma_files:
        filepath = os.path.join(folder_path, filename)

        if not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().lower()

                if not line:
                    continue

                lemma = line.split()[0]

                document_name = filename[:-len(LEMMA_FILENAME_SUFFIX)]
                inverted_index[lemma].add(document_name)

    return dict(inverted_index)


def save_index(index, filepath):
    serializable_index = {
        term: list(docs)
        for term, docs in index.items()
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable_index, f, indent=2, cls=utils.SetEncoder, ensure_ascii=False, sort_keys=True)


def load_index(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        term: set(docs)
        for term, docs in data.items()
    }
