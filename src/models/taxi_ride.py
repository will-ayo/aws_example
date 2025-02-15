from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
import json

class TaxiRide(BaseModel):
    """
    Pydantic model for validating taxi ride data.
    
    Attributes:
        tpep_pickup_datetime: Time when the ride started
        tpep_dropoff_datetime: Time when the ride ended
        passenger_count: Number of passengers (1-9)
        trip_distance: Distance of the trip in miles
        fare_amount: Cost of the trip
        PULocationID: Pickup location ID
        DOLocationID: Dropoff location ID
    """
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: Optional[int] = Field(ge=0, lt=10)
    trip_distance: float = Field(ge=0)
    fare_amount: float = Field(ge=0)
    PULocationID: int
    DOLocationID: int
    
    @validator('tpep_dropoff_datetime')
    def validate_dropoff_time(cls, v, values):
        if 'tpep_pickup_datetime' in values and v < values['tpep_pickup_datetime']:
            raise ValueError('dropoff_datetime must be after pickup_datetime')
        return v

    def dict(self, *args, **kwargs):
        """Convert model to dictionary with ISO format dates"""
        d = super().dict(*args, **kwargs)
        d['tpep_pickup_datetime'] = self.tpep_pickup_datetime.isoformat()
        d['tpep_dropoff_datetime'] = self.tpep_dropoff_datetime.isoformat()
        return d

    class Config:
        # Allow population by field name for flexibility
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 