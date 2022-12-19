import asyncio
import datetime as dt
import logging
import pytz
from typing import Callable

from aiobgjobs.handlers import Handler
from aiobgjobs.jobs import Job
from aiobgjobs.types import Repeats, Every, EveryResult, WeekDayEveryResult

log = logging.getLogger(__name__)


class BgDispatcher(object):
    """
    Dispatcher jobs
    """

    def __init__(self, ):
        """
        Create new BgDispatcher
        """

        self._register_handlers: list[Handler] = list()

    def __len__(self, not_done: bool = False) -> int:
        """
        :param: not_done: True if you need count not done workers
        :return: Count jobs
        """
        count = 0
        if not_done:
            for _handler in self._register_handlers:
                if not _handler.job.is_done: count += 1
            else:
                return count
        else:
            count = len(self._register_handlers)
        self._debug_msg(f'Count handlers {count=}. Is not done jobs {not_done}')
        return count

    def __getitem__(self, item: str) -> Job | None:
        for _handler in self._register_handlers:
            if _handler.job.name == item: return _handler.job
        else:
            return

    def __iter__(self):
        yield [handler for handler in self._register_handlers]

    @staticmethod
    def _debug_msg(message: str):
        log.debug(message)

    async def __call__(self, *args, **kwargs):
        for handler in self._register_handlers:
            await handler()

    async def start(self, relax: float | int | None = .1):
        while True:
            await self()
            if relax:
                await asyncio.sleep(relax)

    def register_handler(
            self, handler: Handler,
    ):
        self._register_handlers.append(handler)

    def handler_job(
            self,
            *,
            every: EveryResult | WeekDayEveryResult | dt.timedelta | None = None,
            count_repeats: int | Repeats,
            datetime_start: dt.datetime | dt.timedelta = (dt.datetime.now() + dt.timedelta(seconds=1)),
            tz: pytz.UTC = pytz.timezone('Europe/Moscow'),
            name: str = None
    ):
        """
        Decorator for registration handler
        :param tz: Time zone
        :param name: Name job
        :param count_repeats: Count repeats job. If -1 then infinity repeat
        :param every: The period of operation of the job
        :param datetime_start: Datetime first start job

        >>> bg_dp = BgDispatcher()
        >>> @bg_dp.handler_job(count_repeats=Repeats.infinity, every=Every.weekdays.friday(), name='Job-1')
        >>> async def job1():
        >>>     await asyncio.sleep(3)
        >>>     print("Job 1 done %s" % dt.datetime.now())
        """

        def decorator(callback: Callable, **kwargs):
            _h = Handler(
                job=Job(
                    func=callback,
                    name=name,
                    kwargs=kwargs
                ),
                count_repeats=count_repeats,
                every=every,
                datetime_start=datetime_start,
                tz=tz
            )
            self.register_handler(
                handler=_h
            )
            self._debug_msg(f'Registered handler {str(_h)}')
            return callback

        return decorator
