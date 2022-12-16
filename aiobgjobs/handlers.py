import asyncio
import datetime as dt

import pytz

from aiobgjobs.jobs import Job
from aiobgjobs.types import Repeats, Every, EveryResult, WeekDayEveryResult


class Handler:
    """
    Handler class

    >>> Handler(job=Job(func=asyncio.sleep, name='Job 1'), count_repeats=Repeats.infinity, )
    """

    def __init__(
            self,
            job: Job,
            count_repeats: int | Repeats = Repeats.infinity,
            every: EveryResult | WeekDayEveryResult | dt.timedelta = None,
            tz=pytz.timezone('Europe/Moscow'),
            datetime_start: dt.datetime = dt.datetime.utcnow()
    ):
        """
        Handler background job constructor
        :param job: Job class instance
        :param count_repeats: Count repeats job. If -1 then infinity repeat
        :param every: The period of operation of the job
        :param datetime_start: Datetime first start job
        """

        assert isinstance(job, Job), 'Job need instance class Job'
        self.job = job

        if every:
            assert isinstance(every, EveryResult) or \
                   (isinstance(every, WeekDayEveryResult) and not datetime_start) or \
                   isinstance(every, dt.timedelta), 'Every bad instance'
            if isinstance(every, WeekDayEveryResult):
                self.datetime_start = tz.localize(every.datetime_start)
            self.every = every

        assert isinstance(datetime_start, dt.datetime)
        assert datetime_start < dt.datetime.utcnow()

        self._local_time_zone = tz
        self.datetime_start = self._local_time_zone.localize(datetime_start)

        if count_repeats:
            if isinstance(count_repeats, Repeats) or isinstance(count_repeats, int):
                assert count_repeats >= -1
            else:
                raise ValueError(f'{count_repeats=} don`t validate')
            self.count_repeats = count_repeats
            self.repeats = 0

        self._date_time_last: dt.datetime | None = None

    async def __call__(self, *args, **kwargs):
        if not self.count_repeats == -1 and self.repeats >= self.count_repeats:
            return
        await self._date_time_last_worker()

    async def _date_time_last_worker(self):
        if not self._date_time_last:
            await self._date_time_start_worker()
        else:
            await self._time_delta_worker()

    async def _time_delta_worker(self):
        if hasattr(self.every, 'delta'):
            _t_d_s = self.every.delta
        else:
            _t_d_s = self.every
        if self._local_time_zone.localize(dt.datetime.utcnow()) \
                - self._date_time_last >= _t_d_s:
            await self._run_task()

    async def _date_time_start_worker(self):
        if not self.datetime_start:
            await self._run_task()
        else:
            if self._local_time_zone.localize(dt.datetime.utcnow()) \
                    >= self.datetime_start:
                await self._run_task()

    async def _run_task(self):
        self._date_time_last = self._local_time_zone.localize(dt.datetime.utcnow())
        self.repeats += 1
        await asyncio.create_task(self.job())

    def __str__(self):
        return f'<Handler is Job: {str(self.job)} | Count repeats:{str(self.count_repeats)} Every {str(self.every)}>'
