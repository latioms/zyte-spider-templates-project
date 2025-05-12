import string
from typing import AsyncGenerator

from scrapy import Request
from scrapy.http import Response
from web_poet import WebPage
from zyte_spider_templates.spiders.base import BaseSpider

from ..items import Company
from ..pages.doualazoom import DoualazoomListingPage, DoualazoomDetailPage


class DoualazoomSpider(BaseSpider):
    """Spider for scraping company information from doualazoom.com."""

    name = "doualazoom"

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "ZYTE_API_TRANSPARENT_MODE": True,
        "TWISTED_REACTOR": "twisted.internet.asyncio.AsyncioSelectorReactor",
        "ZYTE_API_AUTOMAP": True,
        "ZYTE_API_BROWSER_HTML": True,
        "CONCURRENT_REQUESTS": 10,
        "FEEDS": {
            "companies.jsonl": {
                "format": "jsonlines",
                "encoding": "utf8",
                "indent": 0,
            },
        },
    }

    def __init__(self, start_letter='A', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_letter = start_letter.upper() if start_letter.isalpha() and len(start_letter) == 1 else 'A'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # Permet de passer le paramètre -a start_letter=X à la ligne de commande Scrapy
        start_letter = crawler.settings.get('START_LETTER', 'A')
        return cls(start_letter=start_letter)

    def start_requests(self):
        """Generate start requests for each letter A-Z or from a given letter."""
        base_url = "https://www.doualazoom.com/fr/activite/alpha/{}"
        letters = list(string.ascii_uppercase)
        start_index = letters.index(self.start_letter)
        for letter in letters[start_index:]:
            url = base_url.format(letter)
            yield Request(
                url=url,
                callback=self.parse,
                meta={"zyte_api_browser_html": False},
            )

    async def parse(self, response: Response):
        """Parse the listing page and follow links to company detail pages."""
        page = await self.page_handler.handle_page(DoualazoomListingPage, response)
        for url in page.company_links:
            yield Request(
                url=url,
                callback=self.parse_company,
                meta={
                    "zyte_api_automap": True,
                    "zyte_api_browser_html": True,
                },
            )
        # Pagination: continue if there are companies on the page
        if page.has_companies:
            current_page = int(response.url.split("page=")[-1]) if "page=" in response.url else 1
            next_url = f"{response.url.split('?')[0]}?page={current_page + 1}"
            yield Request(
                url=next_url,
                callback=self.parse,
                meta={"zyte_api_browser_html": False},
            )

    async def parse_company(self, response: Response):
        """Parse a company detail page."""
        page = await self.page_handler.handle_page(DoualazoomDetailPage, response)
        return Company(
            name=page.name,
            phones=page.phones,
            whatsapp=page.whatsapp,
            emails=page.emails,
            website=page.website,
            localisation=page.localisation,
            sectors=page.sectors,
            detail_url=response.url,
        )
