import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tf-idf for tokens and lemmas")

    parser.add_argument("--input_dir", default="../Task2/Task2Results")

    args = parser.parse_args()
