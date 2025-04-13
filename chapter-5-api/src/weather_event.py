from dataclasses import dataclass
from typing import Optional

@dataclass
class WeatherEvent:
    location_name: str
    temperature: float
    timestamp: int
    longitude: float
    latitude: float
