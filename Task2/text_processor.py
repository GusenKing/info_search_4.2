import os
import re
import pymorphy3
from html_cleaner import html_to_text


class TextProcessor:
    word_reg_expression = re.compile(r"[а-яё]{3,}", re.IGNORECASE) # регулярка для поиска русских слов

    def __init__(self, input_dir, stopwords_path):
        self.input_dir = input_dir
        self.stopwords = self.load_stopwords(stopwords_path)
        self.morph = pymorphy3.MorphAnalyzer() 

    def load_stopwords(self, path):
        with open(path, encoding="utf-8") as f:
            return set(w.strip() for w in f if w.strip())

    # def read_files(self):
    #     texts = []
    #     for filename in os.listdir(self.input_dir):
    #         with open(os.path.join(self.input_dir, filename), encoding="utf-8", errors="ignore") as f:
    #             texts.append(f.read())
    #     return texts

    def read_files(self):
        result = []
        for filename in os.listdir(self.input_dir): 
            full_path = os.path.join(self.input_dir, filename)
            with open(full_path, encoding="utf-8", errors="ignore") as f:
                result.append((filename, f.read()))
        return result

    def tokenize(self, text):
        tokens = self.word_reg_expression.findall(text.lower())
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
        for filename, raw_text in self.read_files():
            clean_text = html_to_text(raw_text)
            tokens = self.tokenize(clean_text)
            lemmas = self.lemmatize(tokens)
            file_name = os.path.splitext(filename)[0]   
            self.save_tokens(sorted(tokens), f"Task2Results/{file_name}_токены.txt")
            self.save_lemmas(lemmas, f"Task2Results/{file_name}_леммы.txt")
