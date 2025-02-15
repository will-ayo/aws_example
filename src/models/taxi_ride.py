from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

class TaxiRide(BaseModel):
    """
    Pydantic model for validating taxi ride data.
    
    Attributes:
        pickup_datetime: Time when the ride started
        dropoff_datetime: Time when the ride ended
        passenger_count: Number of passengers (1-9)
        trip_distance: Distance of the trip in miles
        fare_amount: Cost of the trip
        pickup_location_id: ID of pickup location
        dropoff_location_id: ID of dropoff location
    """
    pickup_datetime: datetime
    dropoff_datetime: datetime
    passenger_count: int = Field(gt=0, lt=10)
    trip_distance: float = Field(gt=0)
    fare_amount: float = Field(gt=0)
    pickup_location_id: int
    dropoff_location_id: int
    
    @validator('dropoff_datetime')
    def validate_dropoff_time(cls, v, values):
        if 'pickup_datetime' in values and v < values['pickup_datetime']:
            raise ValueError('dropoff_datetime must be after pickup_datetime')
        return v 