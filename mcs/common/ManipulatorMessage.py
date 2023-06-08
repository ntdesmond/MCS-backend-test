from typing import Literal

from pydantic import BaseModel


class ManipulatorMessage(BaseModel):
    datetime: str
    status: Literal["up", "down"]
