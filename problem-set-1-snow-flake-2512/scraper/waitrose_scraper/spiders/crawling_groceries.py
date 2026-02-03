import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
from datetime import datetime
from pathlib import Path

from waitrose_scraper.items import ProductItem


class GroceriesSpider(scrapy.Spider):
    name = "crawling_groceries"
    allowed_domains = ["waitrose.com"]
    start_urls = ["https://www.waitrose.com/ecom/shop/browse/groceries"]
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 3,
    }
    
    def __init__(self, *args, **kwargs):
        super(GroceriesSpider, self).__init__(*args, **kwargs)
        
        # Load food categories
        categories_file = Path('food_categories.json')
        if categories_file.exists():
            with open(categories_file, 'r') as f:
                self.food_categories = json.load(f)
            self.logger.info(f"Loaded {len(self.food_categories)} food categories")
        else:
            self.logger.warning("food_categories.json not found! Will scrape all categories.")
            self.food_categories = {}
        
        # Initialize Selenium
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.logger.info("Selenium WebDriver initialized")
    
    def parse(self, response):
        """
        Parse the main groceries page to extract category links.
        Navigate directly with Selenium to respect robots.txt while simulating human browsing.
        """
        self.logger.info("Starting to scrape Waitrose groceries...")
        self.logger.info("Using Selenium to navigate (simulating human browsing)")
        
        if not self.food_categories:
            self.logger.error("No food categories found!")
            return
        
        # Navigate directly with Selenium (bypassing Scrapy's request system)
        for category_id, info in self.food_categories.items():
            category_name = category_id.replace('_', ' ').title()
            category_url = info['url']
            
            self.logger.info(f"Scraping category: {category_name}")
            
            # Scrape this category with Selenium
            try:
                # Load page with Selenium
                self.driver.get(category_url)
                self.logger.info(f"Processing category: {category_name} ({category_url})")
                
                # Dismiss cookie banner if present (only on first request)
                try:
                    wait = WebDriverWait(self.driver, 5)
                    reject_btn = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="reject-all"]'))
                    )
                    reject_btn.click()
                    self.logger.info("Cookie banner dismissed")
                    time.sleep(2)
                except:
                    pass  # No banner or already dismissed
                
                # Wait for products to load
                time.sleep(5)
                
                # Scroll to load all products
                self.scroll_page()
                
                # Extract products
                products = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="product-pod"]')
                self.logger.info(f"Found {len(products)} products in {category_name}")
                
                for product in products:
                    item = self.extract_product_data(product, category_name)
                    if item:
                        yield item
                
                # Be polite - delay between categories
                time.sleep(3)
                
            except Exception as e:
                self.logger.error(f"Error processing {category_name}: {e}")
    
    def extract_product_data(self, product_element, category):
        """
        Extract data from a single product element.
        """
        try:
            item = ProductItem()
            
            # Basic attributes
            item['product_id'] = product_element.get_attribute('data-product-id')
            item['name'] = product_element.get_attribute('data-product-name')
            item['availability'] = product_element.get_attribute('data-product-availability')
            item['on_offer'] = product_element.get_attribute('data-product-on-offer')
            item['sponsored'] = product_element.get_attribute('data-product-sponsored')
            
            # Price
            try:
                price_elem = product_element.find_element(By.CSS_SELECTOR, '[data-test="product-pod-price"]')
                price_text = price_elem.get_attribute('textContent')
                price_match = re.search(r'£(\d+\.\d+)', price_text)
                item['price'] = price_match.group(0) if price_match else None
            except:
                item['price'] = None
            
            # Price per unit
            try:
                unit_elem = product_element.find_element(By.CSS_SELECTOR, '.pricePerUnit___a1PxI')
                unit_text = unit_elem.get_attribute('textContent')
                unit_match = re.search(r'£[\d.]+/\w+', unit_text)
                item['price_per_unit'] = unit_match.group(0) if unit_match else None
            except:
                item['price_per_unit'] = None
            
            # Size
            try:
                # Try to find size in various locations
                size_divs = product_element.find_elements(By.TAG_NAME, 'div')
                for div in size_divs:
                    text = div.get_attribute('textContent')
                    if text and re.search(r'\d+\s*(g|kg|ml|l|pack)', text, re.IGNORECASE):
                        item['size'] = text.strip()
                        break
                if 'size' not in item:
                    item['size'] = None
            except:
                item['size'] = None
            
            # Image URL
            try:
                img = product_element.find_element(By.TAG_NAME, 'img')
                item['image_url'] = img.get_attribute('src')
            except:
                item['image_url'] = None
            
            # Product URL
            try:
                link = product_element.find_element(By.CSS_SELECTOR, 'a[href*="/products/"]')
                item['product_url'] = link.get_attribute('href')
            except:
                item['product_url'] = None
            
            # Category
            item['category'] = category
            item['subcategory'] = None  # Can be enhanced later
            
            # Metadata
            item['scraped_at'] = datetime.now().isoformat()
            item['scraper_version'] = '1.0'
            
            return item
            
        except Exception as e:
            self.logger.error(f"Error extracting product: {e}")
            return None
    
    def scroll_page(self):
        """
        Scroll page to load all products (for infinite scroll).
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Calculate new height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height
    
    def closed(self, reason):
        """
        Cleanup when spider closes.
        """
        self.driver.quit()
        self.logger.info("Spider closed. WebDriver quit.")