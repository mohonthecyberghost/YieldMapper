from abc import ABC, abstractmethod
import logging
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class BaseScraper(ABC):
    def __init__(self, base_url: str, name: str):
        self.base_url = base_url
        self.name = name
        self.setup_logging()
        self.setup_driver()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/{self.name}_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.name)

    def setup_driver(self):
        """Setup Selenium WebDriver with Chrome"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={UserAgent().random}')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    @abstractmethod
    def scrape_listings(self, city: Optional[str] = None) -> List[Dict]:
        """Scrape property listings from the website"""
        pass

    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON file"""
        os.makedirs('data/raw', exist_ok=True)
        filepath = f'data/raw/{filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Saved {len(data)} listings to {filepath}")
        return filepath

    def clean_price(self, price_str: str) -> float:
        """Clean and convert price string to float"""
        try:
            return float(''.join(filter(str.isdigit, price_str)))
        except ValueError:
            return 0.0

    def clean_size(self, size_str: str) -> float:
        """Clean and convert size string to float"""
        try:
            return float(''.join(filter(str.isdigit, size_str)))
        except ValueError:
            return 0.0

    def close(self):
        """Close the WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 