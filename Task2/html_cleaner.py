from bs4 import BeautifulSoup

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser") # представляем текст html в структурированный html со вложенностью
    return soup.get_text(separator=" ") # вытаскивает текстовые узлы