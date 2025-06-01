import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Scraping settings
SCRAPING_DELAY = 2  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# BigQuery settings
BQ_PROJECT_ID = os.getenv('BQ_PROJECT_ID', 'your-project-id')
BQ_DATASET = os.getenv('BQ_DATASET', 'real_estate')
BQ_TABLE = os.getenv('BQ_TABLE', 'property_listings')

# Data storage
DATA_DIR = 'data'
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Create directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Website configurations
WEBSITES = {
    'pap': {
        'base_url': 'https://www.pap.fr/annonce/location-appartement-maison',
        'name': 'PAP.fr'
    },
    'oqoro': {
        'base_url': 'https://www.oqoro.com/location',
        'name': 'Oqoro'
    },
    'leboncoin': {
        'base_url': 'https://www.leboncoin.fr/locations',
        'name': 'LeBonCoin'
    },
    'lacartedescolocs': {
        'base_url': 'https://www.lacartedescolocs.fr/',
        'name': 'La Carte des Colocs'
    }
}

# Analysis settings
MIN_PROPERTY_SIZE = 20  # m²
MAX_PROPERTY_SIZE = 200  # m²
MIN_PRICE = 300  # €
MAX_PRICE = 5000  # € 