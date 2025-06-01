# Real Estate Yield Analyzer

This project analyzes real estate yields by scraping data from multiple French real estate websites and processing the information to identify optimal investment locations.

## Project Structure

```
YieldMapper/
├── scrapers/              # Web scraping modules
│   ├── pap_scraper.py
│   ├── oqoro_scraper.py
│   ├── leboncoin_scraper.py
│   └── lacartedescolocs_scraper.py
├── data/                  # Data storage
│   ├── raw/              # Raw scraped data
│   └── processed/        # Processed data
├── analysis/             # Analysis scripts
│   └── yield_calculator.py
├── utils/                # Utility functions
│   ├── database.py      # BigQuery integration
│   └── helpers.py       # Helper functions
├── config/              # Configuration files
│   └── config.py
└── main.py             # Main execution script
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with the following variables:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

3. Configure BigQuery:
- Create a new project in Google Cloud Console
- Enable BigQuery API
- Create a service account and download credentials
- Create a dataset and table for storing the scraped data

## Usage

1. Initial data collection:
```bash
python main.py --mode initial
```

2. Update existing data:
```bash
python main.py --mode update
```

## Data Structure

The scraped data includes:
- Property name
- URL
- Price
- Size
- Description
- Location
- City
- Timestamp

## Analysis

The analysis module calculates:
- Yield potential
- Location scores
- Investment recommendations

## Scheduling

The scrapers can be scheduled to run:
- Weekly updates
- Monthly full refreshes
