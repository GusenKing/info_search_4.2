import argparse
import crawler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple web crawler")

    parser.add_argument("--start_url", type=str, required=True, )
    parser.add_argument("--max_depth", type=int)
    parser.add_argument("--max_pages", type=int)
    parser.add_argument("--output_dir", type=str)

    args = parser.parse_args()

    crawler = crawler.WebCrawler(
        args.start_url,
        args.max_depth,
        args.max_pages,
        args.output_dir)
    crawler.crawl()
