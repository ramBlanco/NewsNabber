from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from tp_crawler.spiders.notes import NotesSpider
from tp_crawler.spiders.article import ArticleSpider
import multiprocessing
from utils.util import check_is_dir_exists, get_total_pages
from scrapy.utils.project import get_project_settings
from configs.config_const import DIR_SAVE_PAGE, CATEGORIES, LAST_PAGE_FILE
import json


settings = get_project_settings()


@defer.inlineCallbacks
def start_crawler(page_number: int, category: str):
    runner = CrawlerRunner(
        settings={
            "DOWNLOAD_DELAY": 5,
            "CONCURRENT_REQUESTS": 2,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
            "CONCURRENT_REQUESTS_PER_IP": 2,
            "FEEDS": {
                f"src/data/items-{category}-{page_number}.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "store_empty": False,
                    "indent": 4,
                    "item_export_kwargs": {
                        "export_empty_fields": True,
                    },
                },
            },
        }
    )

    yield runner.crawl(
        NotesSpider,
        page_number=page_number,
        save_pages_in_dir=category,
        category=category,
    )

    with open(
        f"{DIR_SAVE_PAGE}/{category}/{category}?page={page_number}.json"
    ) as json_file:
        url_json_exported = json.load(json_file)

        url_list = list(map(lambda url_item: url_item["url"], url_json_exported))

        yield runner.crawl(
            ArticleSpider,
            save_pages_in_dir=category,
            page_number=page_number,
            start_urls=url_list,
        )

    reactor.stop()


def handler(page_number, category):
    start_crawler(page_number, category)
    reactor.run()


def get_last_page(category: str) -> int:
    try:
        file = open(f'{LAST_PAGE_FILE}-{category}.json')
        last_page = json.load(file)
        return last_page['page']
    except:
        return 0

for category in CATEGORIES:
    check_is_dir_exists(f"{DIR_SAVE_PAGE}/{category}")
    last_page = get_last_page(category)
    for page_number in get_total_pages(last_page):
        process = multiprocessing.Process(
            target=handler,
            args=(page_number, category),
        )
        process.start()
        process.join()

