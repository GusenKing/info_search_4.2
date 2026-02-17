import crawler

if __name__ == '__main__':
    crawler = crawler.WikipediaCrawler(
        "https://ru.wikisource.org/wiki/Категория:Литература_XX_века",
        1,
        3)
    crawler.crawl()
