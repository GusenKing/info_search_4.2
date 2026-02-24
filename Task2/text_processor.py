import os
import re
import pymorphy3
from html_cleaner import html_to_text


class TextProcessor:
    WORD_RE = re.compile(r"[а-яё]{3,}", re.IGNORECASE) # регулярка для поиска русских слов

    def __init__(self, input_dir, stopwords_path):
        self.input_dir = input_dir
        self.stopwords = self.load_stopwords(stopwords_path)
        self.morph = pymorphy3.MorphAnalyzer() # морфологический анализатор - приводит слово к нормальной форме

    def load_stopwords(self, path):
        with open(path, encoding="utf-8") as f:
            return set(w.strip() for w in f if w.strip())

    def read_files(self):
        texts = []
        for filename in os.listdir(self.input_dir):
            with open(os.path.join(self.input_dir, filename), encoding="utf-8", errors="ignore") as f:
                texts.append(f.read())
        return texts

    def tokenize(self, text):
        tokens = self.WORD_RE.findall(text.lower())
        return [t for t in tokens if t not in self.stopwords]

    def extract_tokens(self):
        all_tokens = set()
        for raw_text in self.read_files():
            clean_text = html_to_text(raw_text)
            tokens = self.tokenize(clean_text)
            all_tokens.update(tokens)

        return sorted(all_tokens)

    def lemmatize(self, tokens):
        lemmas = {}
        for token in tokens:
            lemma = self.morph.parse(token)[0].normal_form
            if lemma not in lemmas:
                lemmas[lemma] = []
            lemmas[lemma].append(token)

        return lemmas

    def save_tokens(self, tokens, path="Task2Results/tokens.txt"):
        with open(path, "w", encoding="utf-8") as f:
            for token in tokens:
                f.write(token + "\n")

    def save_lemmas(self, lemmas, path="Task2Results/lemmas.txt"):
        with open(path, "w", encoding="utf-8") as f:
            for lemma, forms in sorted(lemmas.items()):
                f.write(lemma + " " + " ".join(forms) + "\n")

    def process(self):
        tokens = self.extract_tokens()
        lemmas = self.lemmatize(tokens)

        self.save_tokens(tokens)
        self.save_lemmas(lemmas)