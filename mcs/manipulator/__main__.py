import asyncio
import logging

from mcs.common import ManipulatorMessage, settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


async def read_message(reader: asyncio.StreamReader):
    data = b""
    while not data.endswith(b"}"):
        new_data = await reader.read(100)
        data += new_data
    message: ManipulatorMessage = ManipulatorMessage.parse_raw(data)
    logger.info(f"Received message: {message}")


async def tcp_client():
    reader, writer = await asyncio.open_connection(
        settings.controller_hostname,
        settings.controller_tcp_port,
    )
    try:
        while True:
            await read_message(reader)
            await asyncio.sleep(0)
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(tcp_client())
