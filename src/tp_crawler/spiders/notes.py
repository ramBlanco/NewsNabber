import scrapy
import json
from configs.elements_dom import ARTICLE_ITEM
from configs.config_const import DIR_SAVE_PAGE, LAST_PAGE_FILE
from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from typing import List


class NotesSpider(CrawlSpider):
    name = "notes"
    allowed_domains = ("www.pagina12.com.ar", "pagina12.com.ar")

    Rule(
        LinkExtractor(
            allow=r".+/secciones/.+",
            deny=".+(/catamarca12|/dialogo).+",
            deny_domains=["auth.pagina12.com.ar"],
            canonicalize=True,
            deny_extensions=[
                "7z",
                "7zip",
                "apk",
                "bz2",
                "cdr," "dmg",
                "ico," "iso," "tar",
                "tar.gz",
                "pdf",
                "docx",
                "jpg",
                "png",
                "css",
                "js",
            ],
        ),
        callback="parse",
        follow=True,
    )

    def __init__(self, save_pages_in_dir=".", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_pages_in_dir = save_pages_in_dir

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://www.pagina12.com.ar/secciones/{self.category}?page={self.page_number}",
            callback=self.parse,
        )

    def get_articles(self, response: HtmlResponse) -> List[str]:
        return Selector(response).css(ARTICLE_ITEM).getall()

    def get_name_page(self, response: HtmlResponse) -> str:
        page = response.url.split("/")[-1]
        return page

    def save_current_page(self, response: HtmlResponse) -> str:
        name_page = self.get_name_page(response)

        Path(DIR_SAVE_PAGE, self.save_pages_in_dir, f"{name_page}.html").write_bytes(
            response.body
        )

        self.save_number_page()

    def save_number_page(self):
        try:

            dict_page = {"page": self.page_number}
            jsonString = json.dumps(dict_page)

            file = open(Path(f'{LAST_PAGE_FILE}-{self.save_pages_in_dir}.json'),"w")
            file.write(jsonString)
            file.close()
        except Exception as e:
            print("No se pudo actualizar el numero de pagina")
            print(e)

    def save_urls_articles(self, name_page: str, url_articles: list):
        jsonString = json.dumps(url_articles)

        jsonFile = open(
            Path(
                DIR_SAVE_PAGE,
                self.save_pages_in_dir,
                f"{name_page}.json",
            ),
            "w",
        )
        jsonFile.write(jsonString)
        jsonFile.close()

    def parse(self, response: HtmlResponse):
        name_page = self.get_name_page(response)
        self.save_current_page(response)
        articles = self.get_articles(response)

        url_articles = list()

        for article in articles:
            soup = BeautifulSoup(article, "html.parser")
            url_articles.append(
                {"url": f'https://www.pagina12.com.ar{soup.a.get("href")}'}
            )

        self.save_urls_articles(name_page, url_articles)
