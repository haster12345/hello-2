import json
import os
from datetime import datetime
from pathlib import Path
from itemadapter import ItemAdapter


class JsonWriterPipeline:
    """
    Pipeline to save scraped products to JSON files organized by category.
    """
    
    def open_spider(self, spider):
        """Initialize storage when spider opens."""
        self.files = {}
        self.items_count = {}
        
        # Create data/scraped directory if it doesn't exist
        self.output_dir = Path('../data/scraped')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        spider.logger.info(f"Output directory: {self.output_dir.absolute()}")
    
    def close_spider(self, spider):
        """Close all open files when spider closes."""
        for file_handle in self.files.values():
            file_handle.write('\n]')
            file_handle.close()
        
        spider.logger.info(f"Scraping completed. Total categories: {len(self.files)}")
        for category, count in self.items_count.items():
            spider.logger.info(f"  {category}: {count} products")
    
    def process_item(self, item, spider):
        """Process each scraped item."""
        adapter = ItemAdapter(item)
        category = adapter.get('category', 'unknown').replace(' ', '_').lower()
        
        # Open file for this category if not already open
        if category not in self.files:
            filepath = self.output_dir / f'{category}.json'
            self.files[category] = open(filepath, 'w', encoding='utf-8')
            self.files[category].write('[\n')
            self.items_count[category] = 0
        
        # Add comma if not first item
        if self.items_count[category] > 0:
            self.files[category].write(',\n')
        
        # Write item
        line = json.dumps(dict(adapter), ensure_ascii=False, indent=2)
        self.files[category].write(line)
        self.items_count[category] += 1
        
        return item


class DeduplicationPipeline:
    """
    Pipeline to remove duplicate products based on product_id.
    """
    
    def open_spider(self, spider):
        """Initialize deduplication set when spider opens."""
        self.seen_ids = set()
        self.duplicates_count = 0
    
    def close_spider(self, spider):
        """Log deduplication stats when spider closes."""
        spider.logger.info(f"Duplicates removed: {self.duplicates_count}")
        spider.logger.info(f"Unique products: {len(self.seen_ids)}")
    
    def process_item(self, item, spider):
        """Check for duplicates and drop if already seen."""
        adapter = ItemAdapter(item)
        product_id = adapter.get('product_id')
        
        if product_id in self.seen_ids:
            self.duplicates_count += 1
            spider.logger.debug(f"Duplicate found: {product_id} - {adapter.get('name')}")
            raise DropItem(f"Duplicate product: {product_id}")
        else:
            self.seen_ids.add(product_id)
            return item


from scrapy.exceptions import DropItem