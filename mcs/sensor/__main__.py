import asyncio
from asyncio import Task
from datetime import datetime
from typing import Callable

from aiohttp.client import ClientSession
from tqdm import tqdm
from mcs.common import SensorMessage, time_format

rps = 400  # Not accurate

counter = tqdm(unit="messages")


async def send_message(client: ClientSession):
    time = datetime.now()
    message = SensorMessage(
        datetime=time.strftime(time_format),
        payload=42
    ).json()
    await client.post(
        'http://localhost:21234/messages',
        headers={'Content-Type': 'application/json'},
        data=message
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


if __name__ == '__main__':
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
