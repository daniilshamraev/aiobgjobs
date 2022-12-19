# AIOBGJOBS DOCS

## En - docs

This library is designed for asynchronous 
execution of scheduled tasks.

Simple example:
```python
import asyncio
import datetime

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
    datetime_start=datetime.timedelta(minutes=2.0)
)
async def simple_func_delta_to_start():
    print('Test4')


async def main():
    await asyncio.create_task(bg_dp.start(relax=.3))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Goodbye!')
```

Example without using decorators:
```python
import asyncio
import datetime

from aiobgjobs.dispatcher import BgDispatcher
from aiobgjobs.handlers import Handler
from aiobgjobs.jobs import Job
from aiobgjobs.types import Every, Repeats

bg_dp = BgDispatcher()

async def simple_func_every_seconds():
    print('Test')

async def simple_func_infinity_monday():
    print('Test2')

async def simple_func_every_2_minutes():
    print('Test3')

async def simple_func_delta_to_start():
    print('Test4')


bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_every_seconds,
            name='Job - 1',
            kwargs=None
        ),
        count_repeats=3,
        every=Every.seconds(15)
    )
)

bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_infinity_monday,
            name='Job - 2',
            kwargs=None
        ),
        count_repeats=Repeats.infinity,
        every=Every.weekdays.monday()
    )
)

bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_every_2_minutes,
            name='Job - 3',
            kwargs=None
        ),
        count_repeats=Repeats.infinity,
        every=Every.minutes(2)
    )
)

bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_delta_to_start,
            name='Job - 4',
            kwargs=None
        ),
        count_repeats=Repeats.one,
        datetime_start=datetime.timedelta(minutes=2)
    )
)


async def main():
    await asyncio.create_task(bg_dp.start(relax=.3))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Goodbye!')
```

 ## Ru - docs

Эта библиотека предназначена для асинхронного 
выполнения задач по расписанию.

Простой пример:
```python
import asyncio
import datetime

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
    datetime_start=datetime.timedelta(minutes=2.0)
)
async def simple_func_delta_to_start():
    print('Test4')


async def main():
    await asyncio.create_task(bg_dp.start(relax=.3))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Goodbye!')
```

Пример без использования декораторов:
```python
import asyncio
import datetime

from aiobgjobs.dispatcher import BgDispatcher
from aiobgjobs.handlers import Handler
from aiobgjobs.jobs import Job
from aiobgjobs.types import Every, Repeats

bg_dp = BgDispatcher()

async def simple_func_every_seconds():
    print('Test')

async def simple_func_infinity_monday():
    print('Test2')

async def simple_func_every_2_minutes():
    print('Test3')

async def simple_func_delta_to_start():
    print('Test4')


bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_every_seconds,
            name='Job - 1',
            kwargs=None
        ),
        count_repeats=3,
        every=Every.seconds(15)
    )
)

bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_infinity_monday,
            name='Job - 2',
            kwargs=None
        ),
        count_repeats=Repeats.infinity,
        every=Every.weekdays.monday()
    )
)

bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_every_2_minutes,
            name='Job - 3',
            kwargs=None
        ),
        count_repeats=Repeats.infinity,
        every=Every.minutes(2)
    )
)

bg_dp.register_handler(
    Handler(
        job=Job(
            func=simple_func_delta_to_start,
            name='Job - 4',
            kwargs=None
        ),
        count_repeats=Repeats.one,
        datetime_start=datetime.timedelta(minutes=2)
    )
)


async def main():
    await asyncio.create_task(bg_dp.start(relax=.3))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Goodbye!')
```