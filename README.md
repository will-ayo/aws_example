# NYC Taxi Data Pipeline

A data pipeline that ingests NYC Taxi trip data and publishes it to Google Cloud Pub/Sub. The pipeline includes data validation using Pydantic and supports batch processing with configurable settings.

## Project Structure
```
taxi_data_pipeline/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── publisher/
│   │   ├── __init__.py
│   │   └── taxi_publisher.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── taxi_ride.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Pub/Sub enabled
- Google Cloud credentials configured

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd taxi-data-pipeline
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables:

```bash
# Required
export GCP_PROJECT_ID="your-project-id"

# Optional
export PUBSUB_TOPIC="taxi-rides"  # defaults to 'taxi-rides'
export LOG_LEVEL="INFO"  # defaults to 'INFO'
```

## Usage

Run the pipeline:
```bash
python -m src
```

The pipeline will:
1. Download NYC taxi trip data from the public dataset
2. Validate the data using Pydantic models
3. Publish valid records to Google Cloud Pub/Sub
4. Log progress and any validation errors

## Data Validation

The pipeline validates the following fields for each taxi ride:
- pickup_datetime: Must be a valid datetime
- dropoff_datetime: Must be a valid datetime and after pickup_datetime
- passenger_count: Must be between 1 and 9
- trip_distance: Must be greater than 0
- fare_amount: Must be greater than 0
- pickup_location_id: Must be a valid integer
- dropoff_location_id: Must be a valid integer

## Logging

Logs are written to stdout with the following format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Log levels can be configured using the LOG_LEVEL environment variable.

## Error Handling

- Invalid records are logged and skipped
- Network errors during publishing are logged
- Data source access errors will stop the pipeline
- Missing configuration will raise appropriate errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Contact

[Add your contact information here]