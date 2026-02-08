import asyncio
import json
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Source - https://stackoverflow.com/a/64030200
# Posted by mrkiril
# Retrieved 2026-02-08, License - CC BY-SA 4.0
def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        "Exception thrown when attempting to run %s, attempt "
                        "%d of %d" % (func, attempt, times)
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return newfn

    return decorator


def set_cookies(driver: WebDriver):
    cookie_dict = {
        "kacd_mfe_phased_release_prod": "3947080448~rv=3~id=1ca9d4cae820fb5c7116dcc69d3d7e9f",
        "wtr_uuid": "8e3e12029b0f380004607a69c70200000c4c0100",
        "wtr_cookies_functional": "1",
        "wtr_cookies_analytics": "1",
        "wtr_cookies_advertising": "1",
        "wtr_cookie_consent": "1",
    }

    for key, value in cookie_dict.items():
        try:
            driver.add_cookie({"name": key, "value": value})
        except Exception as e:
            raise RuntimeError(f"unable to add cookie: {key, value}") from e
    return


def get_products(driver: WebDriver, unique_products) -> tuple[list[dict], set]:
    links = driver.find_elements(
        By.CSS_SELECTOR, """article[data-testid="product-pod"]"""
    )

    if not links:
        print("no product pods found")
    else:
        print(f"found {len(links)} products")

    items_data = []
    for items in links:
        item_id = items.get_attribute("data-product-id")

        if item_id in unique_products:
            continue

        items_data.append(
            {
                "id": item_id,
                "name": items.find_element(
                    By.CSS_SELECTOR, '[data-testid="product-pod-name"] span'
                ).text,
                "size": items.find_element(
                    By.CSS_SELECTOR, '[data-testid="product-size"]'
                ).text,
                "price": items.find_element(
                    By.CSS_SELECTOR, '[data-test="product-pod-price"] span'
                ).text,
                "link": items.find_element(
                    By.CSS_SELECTOR, '[data-testid="product-pod-header"] a'
                ).get_attribute("href"),
            }
        )
        unique_products.add(item_id)

    for product in items_data:
        link_to_product = product["link"]
        product["barcode"] = get_barcode(driver, link_to_product)

    return items_data, unique_products


def get_barcode(driver: WebDriver, link_to_product: Optional[str]) -> Optional[str]:
    if not link_to_product:
        return None
    driver.get(link_to_product)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, """//*[@id="main"]"""))
    )

    script = driver.find_element(By.XPATH, "/html/body/script[1]")
    if not script:
        print(f"warning: barcode not found for product link {link_to_product}")
        return

    script_text = script.get_attribute("innerHTML")
    if not script_text:
        print(f"warning: barcode not found for product link {link_to_product}")
        return

    data = json.loads(script_text)
    barcode = data["props"]["pageProps"]["product"]["barCodes"][0]
    if not barcode:
        print(f"warning: barcode not found for product link {link_to_product}")
        return None
    return barcode


def load_all_pages(driver: WebDriver):
    i = 0
    while btn := driver.find_element(By.XPATH, """//*[@id="tSr"]/div/div[2]/button"""):
        btn.click()
        i += 1
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, """//*[@id="tSr"]/div/div[2]/button""")
                )
            )
        except TimeoutException:
            print(f"could not find 'Load More' button after {i} clicks")
            break


def write_to_json(data: list[dict], category: str):
    try:
        with open(f"data/scraped/{category}.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise RuntimeError(f"could not write to json for category: {category}") from e
    return


# TODO: change this to 3
@retry(0, RuntimeError)
def main():
    try:
        driver = webdriver.Chrome(options=Options())
        driver.get("https://www.waitrose.com/")
        set_cookies(driver)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        driver.get("https://www.waitrose.com/ecom/shop/browse/groceries")
        categories = [
            "bakery",
            "fresh_and_chilled",
        ]

        unique_products = set()
        for category in categories:
            driver.get(
                f"https://www.waitrose.com/ecom/shop/browse/groceries/{category}"
            )

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, """article[data-testid="product-pod"]""")
                )
            )

            load_all_pages(driver)
            data, unique_products = get_products(driver, unique_products)

            write_to_json(data, category)

    except Exception as e:
        raise RuntimeError("an error occured while getting products") from e
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
