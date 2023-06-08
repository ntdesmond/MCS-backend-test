from fastapi import FastAPI, status
from fastapi.responses import Response

from mcs.common import SensorMessage
from mcs.controller.controller import Controller
from mcs.controller.tcp_server import TcpServer

app = FastAPI(title="MCS backend test")
controller: Controller


@app.on_event("startup")
async def on_start():
    global controller
    tcp_server = TcpServer()
    controller = Controller(tcp_server)


@app.post("/messages", status_code=status.HTTP_202_ACCEPTED, response_class=Response)
async def submit_sensor_message(message: SensorMessage):
    controller.add_message(message)


@app.get("/signals")
async def list_sent_signals() -> list[str]:
    return [signal.to_display_value() for signal in controller.signals_merged]
