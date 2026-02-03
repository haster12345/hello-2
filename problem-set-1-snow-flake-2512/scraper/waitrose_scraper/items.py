import scrapy
from datetime import datetime


class ProductItem(scrapy.Item):
    """
    Defines the structure for a Waitrose product.
    """
    # Unique identifier
    product_id = scrapy.Field()
    
    # Basic product information
    name = scrapy.Field()
    size = scrapy.Field()
    
    # Pricing information
    price = scrapy.Field()
    price_per_unit = scrapy.Field()
    
    # URLs and media
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    
    # Category information
    category = scrapy.Field()
    subcategory = scrapy.Field()
    
    # Metadata
    availability = scrapy.Field()
    on_offer = scrapy.Field()
    sponsored = scrapy.Field()
    
    # Scraping metadata
    scraped_at = scrapy.Field()
    scraper_version = scrapy.Field()