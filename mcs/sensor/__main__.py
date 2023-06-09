import asyncio
from asyncio import Task
from datetime import datetime
from random import randint
from typing import Callable

from aiohttp.client import ClientSession
from tqdm import tqdm
from mcs.common import SensorMessage, time_format, settings

rps = 400  # Not accurate

counter = tqdm(unit="messages")

url = f"http://{settings.controller_hostname}:{settings.controller_http_port}/messages"


async def send_message(client: ClientSession):
    time = datetime.now()
    message = SensorMessage(
        datetime=time.strftime(time_format), payload=randint(-10, 10)
    ).json()
    await client.post(
        url,
        headers={"Content-Type": "application/json"},
        data=message,
    )


async def keep_rps(create_task: Callable[[], Task]):
    while True:
        task = create_task()
        await asyncio.sleep(1 / rps)
        await task
        counter.update()


async def run():
    async with ClientSession() as client:
        await keep_rps(lambda: asyncio.create_task(send_message(client)))


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
