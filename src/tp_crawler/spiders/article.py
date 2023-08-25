import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pathlib import Path
from scrapy.http.response.html import HtmlResponse
from configs.config_const import DIR_SAVE_PAGE
from configs.elements_dom import ARTICLE_DESCRIPTION, ARTICLE_DATE
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from utils.util import check_is_dir_exists
from tp_crawler.items.article_item import ArticleItem


class ArticleSpider(CrawlSpider):
    name = "article"
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
                "cdr",
                "dmg",
                "ico",
                "iso",
                "tar",
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

    def get_name_page(self, response: HtmlResponse) -> str:
        page = response.url.split("/")[-1]
        return page

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

    def save_current_page(self, response: HtmlResponse) -> str:
        name_page = self.get_name_page(response)

        dir_details = Path(
            DIR_SAVE_PAGE, self.save_pages_in_dir, f"details_pag_{self.page_number}"
        )
        check_is_dir_exists(dir_details)

        Path(
            dir_details,
            f"{name_page}.html",
        ).write_bytes(response.body)

    def get_description(self, response: HtmlResponse) -> str:
        paragraphs = Selector(response).css(ARTICLE_DESCRIPTION).getall()
        description = ""
        for paragraph in paragraphs:
            soup = BeautifulSoup(paragraph, "html.parser")
            description = description + soup.p.get_text()

        return description

    def get_date(self, response) -> str:
        date_element = Selector(response).css(ARTICLE_DATE).get()
        soup = BeautifulSoup(date_element, "html.parser")
        return soup.time.get("datetime")

    def get_title(self, response) -> str:
        return ""

    def parse(self, response: HtmlResponse):
        self.save_current_page(response)

        description = self.get_description(response)
        publication_date = self.get_date(response)
        title = self.get_title(response)
        article = ArticleItem(
            description=description, date=publication_date, title=title, category=self.save_pages_in_dir
        )

        return article
