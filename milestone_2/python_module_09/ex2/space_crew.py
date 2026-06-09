from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Any


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_mission_id(self) -> "SpaceMission":
        if not self.mission_id.startswith('M'):
            raise ValueError(
                "Mission ID must start with 'M'"
            )
        return self

    @model_validator(mode='after')
    def check_leader(self) -> "SpaceMission":
        for member in self.crew:
            if member.rank == Rank.COMMANDER:
                return self
            elif member.rank == Rank.CAPTAIN:
                return self
        raise ValueError(
            "Mission must have at least one Commander or Captain"
        )

    @model_validator(mode='after')
    def check_long_missions(self) -> "SpaceMission":
        if self.duration_days > 365:
            crew_len = len(self.crew)
            crew_exp = 0
            for member in self.crew:
                if not member.years_experience < 5:
                    crew_exp += 1
            if crew_exp < crew_len / 2:
                raise ValueError(
                    "Long missions (> 365 days)"
                    "need 50% experienced crew (5+ years)"
                )
        return self

    @model_validator(mode='after')
    def check_crew(self) -> "SpaceMission":
        for member in self.crew:
            if not member.is_active:
                raise ValueError(
                    "All crew members must be active"
                )
        return self


if __name__ == "__main__":
    crew: list[dict[str, Any]] = [
        {
            "member_id": "C_00",
            "name": "Sarah Connor",
            "rank": "commander",
            "age": 42,
            "specialization": "Mission Command",
            "years_experience": 12
        },
        {
            "member_id": "N_01",
            "name": "John Smith",
            "rank": "lieutenant",
            "age": 36,
            "specialization": "Navigation",
            "years_experience": 8
        },
        {
            "member_id": "E_02",
            "name": "Alice Johnson",
            "rank": "officer",
            "age": 27,
            "specialization": "Engineering",
            "years_experience": 6
        }
    ]
    commander = CrewMember(**crew[0])
    lieutenant = CrewMember(**crew[1])
    officer = CrewMember(**crew[2])
    ok_data: dict[str, Any] = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": "2026-05-28",
        "duration_days": " 900",
        "crew": [commander, lieutenant, officer],
        "budget_millions": "2500"
    }
    ok_mission = SpaceMission(**ok_data)
    print(
        "Space Mission Crew Validation",
        "========================================",
        "Valid mission created:",
        f"Mission: {ok_mission.mission_name}",
        f"ID: {ok_mission.mission_id}",
        f"Destination: {ok_mission.destination}",
        f"Duration: {ok_mission.duration_days} days",
        f"Budget: ${ok_mission.budget_millions}M",
        f"Crew size: {len(ok_mission.crew)}",
        sep="\n"
    )
    for member in ok_mission.crew:
        print(
            f"- {member.name} ({member.rank.value})"
            f" - {member.specialization}"
        )
    print("\n=========================================")
    print("Expected validation error:")
    bad_data: dict[str, Any] = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": "2026-05-28",
        "duration_days": " 900",
        "crew": [lieutenant, officer],
        "budget_millions": "2500"
    }
    try:
        bad_mission = SpaceMission(**bad_data)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
