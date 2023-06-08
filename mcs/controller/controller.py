import asyncio
import logging
from datetime import datetime

from mcs.common import SensorMessage, ManipulatorStatus, ManipulatorMessage, time_format
from mcs.controller.signal import Signal
from mcs.controller.tcp_server import TcpServer

logger = logging.getLogger("uvicorn.error")


class Controller:
    def __init__(self, tcp_server: TcpServer):
        self.__tcp_server = tcp_server
        self.__messages: list[SensorMessage] = []
        self.__signals: list[Signal] = []
        self.__signals_merged: list[Signal] = []
        self.__last_time = datetime.now()
        self.__signals_task = asyncio.create_task(self.__emit_signals())

    def __get_next_status(self) -> ManipulatorStatus:
        count = len(self.__messages)
        if count == 0:
            return "down"
        if sum(message.payload for message in self.__messages) / count > 0:
            return "down"
        return "up"

    def __update_merged_signals(self, new_signal: Signal):
        if (
            len(self.__signals_merged) > 0
            and self.__signals_merged[-1].status == new_signal.status
        ):
            self.__signals_merged[-1].end_time = new_signal.end_time
            return
        self.__signals_merged.append(new_signal)

    def add_message(self, message: SensorMessage):
        self.__messages.append(message)

    async def __emit_signals(self):
        try:
            while True:
                await asyncio.sleep(5)
                await self.__emit_signal()
        finally:
            pass

    async def __emit_signal(self):
        logger.info(f"{len(self.__messages)} messages received")
        end_time = datetime.now()
        status = self.__get_next_status()
        signal = Signal(
            start_time=self.__last_time,
            end_time=end_time,
            status=status,
        )
        self.__messages.clear()
        self.__last_time = end_time

        self.__signals.append(signal)
        self.__update_merged_signals(signal)

        self.__tcp_server.send_message(
            ManipulatorMessage(
                datetime=end_time.strftime(time_format),
                status=status,
            )
        )

        logger.info(signal.to_display_value())

    @property
    def signals(self):
        return self.__signals

    @property
    def signals_merged(self):
        return self.__signals_merged
