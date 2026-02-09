# Scraper 

This waitrose scraper scrapes the `Bakery` and the `Fresh & Chilled` categories from the waitrose website.

## Accessing Data & Basic Usage

It is reccomended that you use the scraped data in available in `./data/scraped`. The data is split by categories and is provided in json.

For the json, the following fields are provided for each product:

```json
[
  {
      "id": "id",
      "name": "name",
      "size": "size",
      "price": "price",
      "link": "link",
      "barcode": "barcode"
  },
]
```

### Re-building the data

from the root level of the project run the following command to rebuild the data from scratch. (Warning this might take ~10 minutes, depending on hardware and network)
```sh
# Optional: set up environment if not set up already
python3 -m venv .
pip install -r requirements.txt

# Run the scraper
python3 scraper/main.py
```

## Why Selenium?

The Waitrose website relies on client-side rendering for product listings.
Selenium is used to ensure all dynamic content is fully loaded before scraping.


## Requirements

- Python 3.13
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
