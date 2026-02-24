import argparse
from text_processor import TextProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="tokenization and lemmatization")
    
    parser.add_argument("--input_dir", default="../Task1/Task1Results")
    parser.add_argument("--stopwords", default="stopwords.txt")

    args = parser.parse_args()

    processor = TextProcessor(
        input_dir=args.input_dir,
        stopwords_path=args.stopwords
    )
    processor.process()