from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re
from datetime import datetime

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

print("Testing single category scrape...")

try:
    # Test with Bakery category
    url = "https://www.waitrose.com/ecom/shop/browse/groceries/bakery"
    print(f"\nNavigating to: {url}")
    
    driver.get(url)
    print("Waiting 5 seconds for page to load...")
    time.sleep(5)
    
    print(f"Page title: {driver.title}")
    
    # Find products
    products = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="product-pod"]')
    print(f"\nFound {len(products)} products")
    
    if len(products) > 0:
        print("\nExtracting first 3 products...")
        results = []
        
        for i, product in enumerate(products[:3], 1):
            print(f"\n--- Product {i} ---")
            
            data = {}
            data['product_id'] = product.get_attribute('data-product-id')
            data['name'] = product.get_attribute('data-product-name')
            
            # Price
            try:
                price_elem = product.find_element(By.CSS_SELECTOR, '[data-test="product-pod-price"]')
                price_text = price_elem.get_attribute('textContent')
                price_match = re.search(r'£(\d+\.\d+)', price_text)
                data['price'] = price_match.group(0) if price_match else None
            except:
                data['price'] = None
            
            print(f"ID: {data['product_id']}")
            print(f"Name: {data['name']}")
            print(f"Price: {data['price']}")
            
            results.append(data)
        
        # Save test results
        with open('test_scrape_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print("\n✓ Test successful! Saved to test_scrape_results.json")
        print("\nThe scraper logic works. Issue is with Scrapy integration.")
    else:
        print("\n✗ No products found. Saving page HTML for inspection...")
        with open('test_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Saved to test_page.html")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\nBrowser closed.")