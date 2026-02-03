# Scrapy settings for waitrose_scraper project

BOT_NAME = "waitrose_scraper"

SPIDER_MODULES = ["waitrose_scraper.spiders"]
NEWSPIDER_MODULE = "waitrose_scraper.spiders"

# Crawl responsibly by identifying yourself
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 1  # Be polite - scrape one page at a time

# Configure a delay for requests (in seconds)
DOWNLOAD_DELAY = 3  # 3 second delay between requests
RANDOMIZE_DOWNLOAD_DELAY = True  # Randomize the delay

# Disable cookies (we don't need them for this scraper)
COOKIES_ENABLED = False

# Disable Telnet Console (not needed)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    "waitrose_scraper.middlewares.WaitroseScraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#    "waitrose_scraper.middlewares.WaitroseScraperDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
ITEM_PIPELINES = {
   "waitrose_scraper.pipelines.JsonWriterPipeline": 300,
   "waitrose_scraper.pipelines.DeduplicationPipeline": 400,
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable showing throttling stats
AUTOTHROTTLE_DEBUG = False

# Set settings whose default value is deprecated
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Logging
LOG_LEVEL = "INFO"  # Change to DEBUG for more verbose output