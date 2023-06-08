from typing import Literal

from pydantic import BaseModel

ManipulatorStatus = Literal["up", "down"]


class ManipulatorMessage(BaseModel):
    datetime: str
    status: ManipulatorStatus
