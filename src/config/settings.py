import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    """
    Application settings loaded from environment variables
    """
    # GCP Settings
    PROJECT_ID: str = os.getenv('GCP_PROJECT_ID')
    PUBSUB_TOPIC: str = os.getenv('PUBSUB_TOPIC', 'taxi-rides')
    
    # Data Settings
    DATA_URL: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    BATCH_SIZE: int = 100
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    def validate(self) -> None:
        """Validate required settings"""
        if not self.PROJECT_ID:
            raise ValueError("GCP_PROJECT_ID environment variable is required") 