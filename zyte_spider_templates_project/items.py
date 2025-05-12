import scrapy

class Company(scrapy.Item):
    """Company information from doualazoom.com"""
    name = scrapy.Field()
    phones = scrapy.Field()
    whatsapp = scrapy.Field()
    emails = scrapy.Field()
    website = scrapy.Field()
    localisation = scrapy.Field()
    sectors = scrapy.Field()
    detail_url = scrapy.Field()
