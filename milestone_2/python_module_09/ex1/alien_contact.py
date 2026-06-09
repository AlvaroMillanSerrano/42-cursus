from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional, Any


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check_contact_id(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact id must start with 'AC'")
        return self

    @model_validator(mode='after')
    def check_physica_type(self) -> "AlienContact":
        if self.contact_type == ContactType.PHYSICAL:
            if not self.is_verified:
                raise ValueError("Physical contacts must be verified")
        return self

    @model_validator(mode='after')
    def check_telephatic_type(self) -> "AlienContact":
        if self.contact_type == ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError(
                    "Telephatic contacts need at least 3 witnesses"
                )
        return self

    @model_validator(mode='after')
    def check_signal(self) -> "AlienContact":
        if self.signal_strength > 7.0:
            if not self.message_received:
                raise ValueError(
                    "signal > 7.0 should include recieved message"
                )
        return self


if __name__ == "__main__":
    ok_data: dict[str, Any] = {
        "contact_id": "AC_2024_001",
        "timestamp": "2026-05-27",
        "location": "Area 51, Nevada",
        "contact_type": "radio",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
    }
    ok_contact = AlienContact(**ok_data)
    print(
        "Alien Contact Log Validation",
        "========================================",
        "Valid contact report:",
        f"ID: {ok_contact.contact_id}",
        f"Type: {ok_contact.contact_type}",
        f"Location: {ok_contact.location}",
        f"Signal: {ok_contact.signal_strength}/10",
        f"Duration: {ok_contact.duration_minutes} minutes",
        f"Witnesses: {ok_contact.witness_count}",
        f"Message: {ok_contact.message_received}\n"
        if ok_contact.message_received else "",
        "======================================",
        sep="\n"
    )
    print("Expected validation error:")
    bad_data: dict[str, Any] = {
        "contact_id": "AC_2024_001",
        "timestamp": "2026-05-27",
        "location": "Area 51, Nevada",
        "contact_type": "telepathic",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 2,
        "message_received": "Greetings from Zeta Reticuli",
    }
    try:
        bad_contact = AlienContact(**bad_data)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
