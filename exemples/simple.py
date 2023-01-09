import asyncio
from datetime import datetime as dt
from datetime import timedelta

from aiobgjobs.dispatcher import BgDispatcher
from aiobgjobs.types import Every, Repeats

bg_dp = BgDispatcher()


@bg_dp.handler_job(
    every=Every.seconds(15),
    count_repeats=3
)
async def simple_func_every_second():
    print('Test')


@bg_dp.handler_job(
    every=Every.weekdays.monday(hour=11, minute=40),
    count_repeats=Repeats.infinity
)
async def simple_func_infinity_monday():
    print('Test2')


@bg_dp.handler_job(
    every=Every.minutes(2),
    count_repeats=Repeats.infinity
)
async def simple_func_every_2_minutes():
    print('Test3')


@bg_dp.handler_job(
    count_repeats=Repeats.one,
    datetime_start=timedelta(minutes=2.0)
)
async def simple_func_delta_to_start():
    print('Test4')


@bg_dp.handler_job(
    every=Every.day(),
    datetime_start=dt.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    ) + timedelta(days=1),
    count_repeats=Repeats.infinity
)
async def every_day():
    print("every day test")


async def main():
    await asyncio.create_task(bg_dp.start(relax=.3))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Goodbye!')
