import argparse
import inverted_index_builder as builder
import boolean_search as search


def build_mode(build_args):
    print("Building inverted index...")
    index = builder.build_inverted_index(build_args.tokens_folder)
    builder.save_index(index, build_args.output_filepath)
    print(f"Index saved to {build_args.output_filepath}")


def search_mode(search_args):
    print("Loading index...")
    index = builder.load_index(search_args.index_file)

    print("Boolean search ready (type 'exit' to quit)\n")

    while True:
        query = input("Query> ")

        if query.lower() == "exit":
            break

        results = search.boolean_search(query, index)

        print("Results:")
        if results:
            for r in sorted(results):
                print(" ", r)
        else:
            print("  No matches")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Inverted index builder and boolean search engine")

    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("index_build", help="Build inverted index")
    build_parser.add_argument("--tokens_folder", default="Task2/Task2Results", help="Folder with tokenized files")
    build_parser.add_argument("--output_filepath", default="Task3/Task3Results/inverted_index.json",
                              help="Output index file (json)")
    build_parser.set_defaults(func=build_mode)

    search_parser = subparsers.add_parser("search", help="Search using index")
    search_parser.add_argument("--index_file", default="Task3/Task3Results/inverted_index.json",
                               help="Path to saved index")
    search_parser.set_defaults(func=search_mode)

    args = parser.parse_args()
    args.func(args)
