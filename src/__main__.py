import logging
from src.publisher.taxi_publisher import TaxiDataPublisher
from src.config.settings import Settings

def configure_logging(log_level: str) -> None:
    """Configure logging for the application"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main entry point for the application"""
    settings = Settings()
    configure_logging(settings.LOG_LEVEL)
    
    publisher = TaxiDataPublisher(settings)
    publisher.process_data()

if __name__ == "__main__":
    main() 