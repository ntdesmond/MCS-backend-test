from pydantic import BaseModel


class SensorMessage(BaseModel):
    datetime: str
    payload: int
