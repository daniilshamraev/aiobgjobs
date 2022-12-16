import asyncio
import datetime
import logging

from aiobgjobs.dispatcher import BgDispatcher
from aiobgjobs.types import Every

logger = logging.Logger(name=__name__, level=logging.DEBUG)

bg_dp = BgDispatcher()


@bg_dp.handler_job(
    every=Every.seconds(5)
)
async def simple_func_every_second():
    print('Test')


@bg_dp.handler_job(
    every=Every.hour(),
    count_repeats=5
)
async def simple_func_every_second():
    print('Test2')


async def main():
    await asyncio.create_task(bg_dp.start(relax=None))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except* KeyboardInterrupt:
        print('Goodbye!')
