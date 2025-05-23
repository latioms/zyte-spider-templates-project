from itemadapter import ItemAdapter
from zyte_common_items import ZyteItemAdapter

ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)

BOT_NAME = "zyte_spider_templates_project"

SPIDER_MODULES = [
    "zyte_spider_templates.spiders",
    "zyte_spider_templates_project.spiders",
]

NEWSPIDER_MODULE = "zyte_spider_templates_project.spiders"

ADDONS = {
    "scrapy_poet.Addon": 300,
    "scrapy_zyte_api.Addon": 500,
    "duplicate_url_discarder.Addon": 600,
    "zyte_spider_templates.Addon": 700,
}

# scrapy-poet
SCRAPY_POET_DISCOVER = [
    "zyte_spider_templates_project.pages",
]

# duplicate-url-discarder
DUD_ATTRIBUTES_PER_ITEM = {
    "zyte_spider_templates_project.items.Company": [
        "detail_url",
        "name",
    ],
}

# Zyte API settings
ZYTE_API_KEY = "dd27d34e811c4d829181b09757e7442a"  # Replace with your actual API key

# Scrapy settings
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
