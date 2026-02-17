import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup
import json, re, os
import utils


class WebCrawler:
    def __init__(self, start_url, max_depth=2, max_pages=100, output_dir="output"):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.output_dir = output_dir
        self.visited = set()
        self.request_headers = {"User-Agent": "MySimpleCrawler/1.0"}

    # проверка стартового url
    def is_successful(self):

        try:
            response = requests.get(self.start_url, headers=self.request_headers, timeout=20)
            response.raise_for_status()
            if response.status_code == 200:
                return True

            else:
                print(
                    f"The crawling could not begin because of unsuccessful request to the starting url with the status code of {response.status_code}.")

        except requests.HTTPError as e:
            print(f"HTTP Error occurred: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    # скачивание страницы и сбор всех ссылок на ней
    def process_page(self, url, depth, page_number):
        if depth > self.max_depth or url in self.visited:
            return set(), ''

        self.visited.add(url)
        links = set()
        document_page = ''

        try:
            response = requests.get(url, headers=self.request_headers, timeout=10)
            response.raise_for_status()
            document_page = response.text
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"processing page {url}")

            # находим все ссылки на странице и объединяем их href со стартовой ссылкой
            anchors = soup.find_all('a')
            for anchor in anchors:
                link = requests.compat.urljoin(url,
                                               anchor.get('href'))
                links.add(link)

        except requests.RequestException:
            pass

        return links, document_page

    def crawl(self):
        if self.is_successful():
            downloaded_pages = []
            index = {}
            urls_to_crawl = {self.start_url}
            page_number = 0

            for depth in range(self.max_depth + 1):
                new_urls = set()
                for url in urls_to_crawl:
                    if url not in self.visited and page_number < self.max_pages:
                        page_number += 1
                        links, content = self.process_page(url,
                                                           depth, page_number)
                        decoded_url = unquote(url)
                        downloaded_pages.append([content, decoded_url])
                        index[page_number] = decoded_url
                        new_urls.update(links)

                urls_to_crawl = new_urls

            current_dir = os.getcwd()
            folder_dir = os.path.join(current_dir, self.output_dir)

            if not os.path.isdir(folder_dir):
                os.makedirs(folder_dir)

            # сохраняем каждую страницу в txt файл
            for page, url in downloaded_pages:
                filename = re.sub(r'\W+', '_', url) + '_crawled.txt'
                with open(os.path.join(folder_dir, filename), "w", encoding="utf-8") as file:
                    file.write(page)

            utils.zip_folder(folder_dir, os.path.join(current_dir, f"{self.output_dir}.zip"))

            # записываем в index.txt все ссылки с их номером
            with open(os.path.join(folder_dir, 'index.txt'), "w", encoding="utf-8") as file:
                for number, url in index.items():
                    file.write(f"{number}: {url}\n")

            return page_number
