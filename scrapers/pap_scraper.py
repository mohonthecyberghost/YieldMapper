from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import time
from .base_scraper import BaseScraper

class PAPScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://www.pap.fr/annonce/location-appartement-maison",
            name="pap"
        )

    def scrape_listings(self, city: Optional[str] = None) -> List[Dict]:
        """Scrape property listings from PAP.fr"""
        listings = []
        page = 1
        
        while True:
            url = f"{self.base_url}?page={page}"
            if city:
                url += f"&ville={city}"
            
            self.logger.info(f"Scraping page {page}")
            self.driver.get(url)
            time.sleep(2)  # Respect the website's rate limits
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            property_cards = soup.find_all('div', class_='search-list-item')
            
            if not property_cards:
                break
                
            for card in property_cards:
                try:
                    listing = self._parse_listing(card)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    self.logger.error(f"Error parsing listing: {str(e)}")
            
            page += 1
            
        self.logger.info(f"Scraped {len(listings)} listings from PAP.fr")
        return listings

    def _parse_listing(self, card) -> Optional[Dict]:
        """Parse individual property listing"""
        try:
            title_elem = card.find('h2', class_='item-title')
            price_elem = card.find('span', class_='item-price')
            location_elem = card.find('div', class_='item-location')
            size_elem = card.find('div', class_='item-criteria')
            
            if not all([title_elem, price_elem, location_elem]):
                return None
            
            # Extract link
            link = title_elem.find('a')['href']
            if not link.startswith('http'):
                link = f"https://www.pap.fr{link}"
            
            # Extract size from criteria
            size = 0
            if size_elem:
                size_text = size_elem.text
                if 'm²' in size_text:
                    size = self.clean_size(size_text.split('m²')[0])
            
            return {
                'source': 'pap',
                'title': title_elem.text.strip(),
                'price': self.clean_price(price_elem.text),
                'size': size,
                'location': location_elem.text.strip(),
                'link': link,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing listing: {str(e)}")
            return None 