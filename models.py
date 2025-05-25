from pydantic import BaseModel
from typing import Optional


class LocationOut(BaseModel):
    id: int
    city: str
    lat: float
    lon: float


class LatestForecastOut(BaseModel):
    city: str
    date: str
    temperature: float
    humidity: Optional[float] 


class AverageTempOut(BaseModel):
    city: str
    date: str
    avg_temperature: float


class TopLocationOut(BaseModel):
    city: str
    avg_metric: float