from llm_sdk import Small_LLM_Model
from typing import Any


class Encoder:
    """Converts texts and IDs into tokens using LLM SDK."""

    def __init__(self, model: Small_LLM_Model) -> None:
        self.model = model

    def encode(self, text: str) -> Any:
        """Text -> list of IDs."""
        return self.model.encode(text)[0].tolist()
