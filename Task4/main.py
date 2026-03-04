import argparse
import os
import tf_idf_calculator as calc


def write_statistics_for_documents_to_files(tf, idf, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for doc, terms_tf in tf.items():
        output_path = os.path.join(output_dir, doc)
        with open(output_path, "w", encoding="utf-8") as f:
            for term, tf_value in terms_tf.items():
                idf_value = idf.get(term, 0.0)
                tf_idf = tf_value * idf_value
                f.write(f"{term} {idf_value} {tf_idf}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tf-idf for tokens and lemmas")

    parser.add_argument("--input_dir", default="Task2/Task2Results")
    parser.add_argument("--tokens_output_dir", default="Task4/Task4Results/tokens")
    parser.add_argument("--lemmas_output_dir", default="Task4/Task4Results/lemmas")

    args = parser.parse_args()

    tokens_tf, token_idf = calc.calculate_tf_and_idf_for_tokens(args.input_dir)
    lemmas_tf, lemmas_idf = calc.calculate_tf_and_idf_for_lemmas(args.input_dir)

    write_statistics_for_documents_to_files(tokens_tf, token_idf, args.tokens_output_dir)
    write_statistics_for_documents_to_files(lemmas_tf, lemmas_idf, args.lemmas_output_dir)
