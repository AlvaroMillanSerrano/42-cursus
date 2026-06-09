from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional, Any


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(None, max_length=200)


if __name__ == "__main__":
    ok_data: dict[str, Any] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2026-05-27",
        "is_operational": True
    }
    ok_station = SpaceStation(**ok_data)
    print(
        "Space Station Data Validation",
        "========================================",
        "Valid station created:",
        f"ID: {ok_station.station_id}",
        f"Name: {ok_station.name}",
        f"Crew: {ok_station.crew_size} people",
        f"Power: {ok_station.power_level}%",
        f"Oxygen: {ok_station.oxygen_level}%",
        f"Status: {'Operational' if ok_station.is_operational else 'Down'}",
        f"notes: {ok_station.notes}\n" if ok_station.notes else "",
        "========================================",
        sep="\n"
    )
    print("Expected validation error:")
    bad_data: dict[str, Any] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 60,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2026-05-27",
        "is_operational": True,
    }
    try:
        bad_station = SpaceStation(**bad_data)
    except ValidationError as e:
        print(e.errors()[0]["msg"])
