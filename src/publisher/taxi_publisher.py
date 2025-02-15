from google.cloud import pubsub_v1
import pandas as pd
import logging
from typing import List, Optional
import json
import time

from src.models.taxi_ride import TaxiRide
from src.config.settings import Settings

logger = logging.getLogger(__name__)

class TaxiDataPublisher:
    """
    Handles the ingestion and publishing of taxi ride data to Google Pub/Sub
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.settings.validate()
        
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            self.settings.PROJECT_ID, 
            self.settings.PUBSUB_TOPIC
        )

    def read_data(self) -> pd.DataFrame:
        """Read taxi data from the source"""
        logger.info(f"Reading data from {self.settings.DATA_URL}")
        try:
            df = pd.read_parquet(self.settings.DATA_URL)
            logger.info(f"Successfully read {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error reading data: {str(e)}")
            raise

    def validate_and_transform_batch(self, records: List[dict]) -> List[dict]:
        """Validate records using Pydantic model"""
        valid_records = []
        for record in records:
            try:
                validated_record = TaxiRide(**record)
                valid_records.append(validated_record.dict())
            except Exception as e:
                logger.warning(f"Invalid record: {str(e)}")
        return valid_records

    def publish_messages(self, records: List[dict]) -> None:
        """Publish messages to Pub/Sub"""
        for record in records:
            try:
                data = json.dumps(record).encode('utf-8')
                future = self.publisher.publish(self.topic_path, data)
                future.result()  # Wait for message to be published
            except Exception as e:
                logger.error(f"Error publishing message: {str(e)}")

    def process_data(self) -> None:
        """Main processing function"""
        try:
            df = self.read_data()
            total_records = len(df)
            processed_records = 0

            logger.info("Starting data processing and publishing")
            
            for i in range(0, total_records, self.settings.BATCH_SIZE):
                batch = df.iloc[i:i + self.settings.BATCH_SIZE].to_dict('records')
                valid_records = self.validate_and_transform_batch(batch)
                
                if valid_records:
                    self.publish_messages(valid_records)
                
                processed_records += len(valid_records)
                logger.info(f"Processed {processed_records}/{total_records} records")
                
                # Add a small delay to avoid hitting rate limits
                time.sleep(0.1)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}")
            raise 