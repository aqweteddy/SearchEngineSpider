from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import Function
from parser import HtmlParser


class PageItem:
    main_content: str = None
    url: str = None
    domain: str = None
    title: str = None
    depth_from_root: int = None
    a: List[str] = None
    ip: str = None


class ResponseItem:
    resp_code: int = None
    html: str = None
    url: str = None
    depth_from_root: int = 0
    drop: bool = False

    def convert_to_page(self):
        item = PageItem()
        
        item.url = self.url
        item.depth_from_root = self.depth_from_root

        parser = HtmlParser(self.html)

        item.title = parser.get_title()
        item.domain = Function.get_domain(item.url)
        item.main_content = parser.get_main_content()
        item.a = []
        for href in parser.get_hrefs():
            if not href:
                continue
            item.a.append(urljoin(item.url, href))
        return item

    def __repr__(self):
        return f"""
                resp_code: {self.resp_code}
                url: {self.url}
                """


if __name__ == '__main__':
    print(Function.get_domain('https://google.com/'))
