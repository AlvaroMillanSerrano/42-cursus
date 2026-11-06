from typing import Any
from pydantic import BaseModel


class ParamSpec(BaseModel):
    type: str


class FunctionDef(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParamSpec]
    returns: ParamSpec


class PromptItem(BaseModel):
    prompt: str


class CallResult(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]
