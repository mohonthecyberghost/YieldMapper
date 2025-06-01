import argparse
import schedule
import time
from datetime import datetime
import logging
from typing import List, Dict

from scrapers.pap_scraper import PAPScraper
from utils.database import BigQueryClient
from config.config import WEBSITES

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def scrape_all_sources(city: str = None) -> List[Dict]:
    """Scrape all configured sources"""
    all_listings = []
    
    # Initialize scrapers
    scrapers = {
        'pap': PAPScraper(),
        # Add other scrapers here as they are implemented
    }
    
    for source, scraper in scrapers.items():
        try:
            logger.info(f"Scraping {source}")
            listings = scraper.scrape_listings(city)
            all_listings.extend(listings)
            logger.info(f"Scraped {len(listings)} listings from {source}")
        except Exception as e:
            logger.error(f"Error scraping {source}: {str(e)}")
        finally:
            scraper.close()
    
    return all_listings

def update_database(listings: List[Dict]):
    """Update BigQuery with new listings"""
    try:
        db = BigQueryClient()
        db.insert_listings(listings)
        logger.info(f"Successfully inserted {len(listings)} listings into BigQuery")
    except Exception as e:
        logger.error(f"Error updating database: {str(e)}")

def run_scraping_job(city: str = None):
    """Run the complete scraping job"""
    logger.info("Starting scraping job")
    listings = scrape_all_sources(city)
    update_database(listings)
    logger.info("Scraping job completed")

def schedule_jobs():
    """Schedule regular scraping jobs"""
    # Weekly update
    schedule.every().monday.at("02:00").do(run_scraping_job)
    
    # Monthly full refresh
    schedule.every().month.at("02:00").do(run_scraping_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    parser = argparse.ArgumentParser(description='Real Estate Yield Analyzer')
    parser.add_argument('--mode', choices=['initial', 'update', 'schedule'],
                      help='Scraping mode: initial (one-time), update (one-time), or schedule (continuous)')
    parser.add_argument('--city', help='Specific city to scrape')
    
    args = parser.parse_args()
    
    if args.mode == 'initial':
        logger.info("Running initial scraping")
        run_scraping_job(args.city)
    elif args.mode == 'update':
        logger.info("Running update scraping")
        run_scraping_job(args.city)
    elif args.mode == 'schedule':
        logger.info("Starting scheduled scraping")
        schedule_jobs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 