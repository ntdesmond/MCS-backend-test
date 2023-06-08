import asyncio

from mcs.common import ManipulatorMessage


class TcpServer:
    def __init__(self):
        self.__message_event = asyncio.Event()
        self.__message: ManipulatorMessage | None = None
        self.__server_task = asyncio.create_task(self.__run_server())

    async def __run_server(self):
        server = await asyncio.start_server(self.__handler, "127.0.0.1", 21235)
        async with server:
            await server.serve_forever()

    async def __handler(self, _, writer: asyncio.StreamWriter):
        try:
            while True:
                await self.__message_event.wait()
                self.__message_event.clear()
                json: str = self.__message.json()
                writer.write(json.encode("utf8"))
                await writer.drain()
                await asyncio.sleep(0)
        except (ConnectionAbortedError, ConnectionResetError):
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    def send_message(self, message: ManipulatorMessage):
        self.__message = message
        self.__message_event.set()
