from google.cloud import bigquery
from typing import List, Dict
import pandas as pd
from config.config import BQ_PROJECT_ID, BQ_DATASET, BQ_TABLE

class BigQueryClient:
    def __init__(self):
        self.client = bigquery.Client(project=BQ_PROJECT_ID)
        self.table_id = f"{BQ_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Create the table if it doesn't exist"""
        schema = [
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("price", "FLOAT"),
            bigquery.SchemaField("size", "FLOAT"),
            bigquery.SchemaField("location", "STRING"),
            bigquery.SchemaField("link", "STRING"),
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("description", "STRING"),
        ]

        try:
            self.client.get_table(self.table_id)
        except Exception:
            table = bigquery.Table(self.table_id, schema=schema)
            self.client.create_table(table)

    def insert_listings(self, listings: List[Dict]):
        """Insert listings into BigQuery"""
        if not listings:
            return

        # Convert to DataFrame for easier handling
        df = pd.DataFrame(listings)
        
        # Ensure timestamp is in the correct format
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Upload to BigQuery
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        
        job = self.client.load_table_from_dataframe(
            df, self.table_id, job_config=job_config
        )
        job.result()  # Wait for the job to complete

    def get_latest_listings(self, source: str = None, city: str = None, limit: int = 1000):
        """Get the latest listings from BigQuery"""
        query = f"""
        SELECT *
        FROM `{self.table_id}`
        WHERE 1=1
        """
        
        if source:
            query += f" AND source = '{source}'"
        if city:
            query += f" AND city = '{city}'"
            
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        
        return self.client.query(query).result().to_dataframe()

    def get_average_prices_by_city(self):
        """Get average prices by city"""
        query = f"""
        SELECT 
            city,
            AVG(price) as avg_price,
            AVG(price/size) as avg_price_per_sqm,
            COUNT(*) as listing_count
        FROM `{self.table_id}`
        WHERE city IS NOT NULL
        GROUP BY city
        ORDER BY avg_price_per_sqm DESC
        """
        
        return self.client.query(query).result().to_dataframe() 