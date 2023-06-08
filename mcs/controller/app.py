from fastapi import FastAPI, status
from fastapi.responses import Response

from mcs.common import SensorMessage

app = FastAPI()

data = []


@app.post("/messages", status_code=status.HTTP_202_ACCEPTED, response_class=Response)
async def update_item(message: SensorMessage):
    data.append(message)
