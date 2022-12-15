import asyncio
import datetime

from aiobgjobs.jobs import Job
from aiobgjobs.types import Repeats, _Unity


class Handler:

    def __init__(
            self,
            job: Job,
            interval: datetime.timedelta | None = None,
            count_repeats: int | Repeats = Repeats.infinity,
            every: tuple[_Unity, int] | None = None,
            datetime_start: datetime.datetime | None = datetime.datetime.utcnow()
    ):
        assert job
        assert isinstance(job, Job), 'Job need instance class Job'
        self.job = job

        assert not interval and every, 'You don`t use interval and every'
        assert count_repeats < -1

        if every:
            assert isinstance(every, tuple)
            self.every = every
        else:
            assert isinstance(interval, datetime.timedelta)
            self.interval = interval

        if datetime_start:
            assert datetime_start < datetime.datetime.utcnow()
            assert isinstance(datetime_start, datetime.datetime)
            self.datetime_start = datetime_start
        if count_repeats:
            assert isinstance(count_repeats, int) or isinstance(count_repeats, Repeats)
            self.count_repeats = count_repeats
            self.repeats = 0

        self._date_time_last: datetime.datetime | None = None

    async def __call__(self, *args, **kwargs):
        if self.repeats >= self.count_repeats:
            return
        elif self.every:
            await self._date_time_last_worker(datetime.datetime.utcnow() - self._date_time_last)
        else:
            await self._date_time_last_worker(self.interval)

    async def _date_time_last_worker(self, _t_d: datetime.timedelta):
        if not self._date_time_last:
            await self._date_time_start_worker()
        else:
            await self._time_delta_worker(_t_d)

    async def _time_delta_worker(self, _t_d_f: datetime.timedelta):
        if self.every:
            _u, _c = self.every
            if _c > 1:
                _u = _u.removesuffix('s')
            _t_d_s = datetime.timedelta(**{_u.name: _c})
        else:
            _t_d_s = self.interval
        if _t_d_f >= _t_d_s:
            await asyncio.create_task(self.job())

    async def _date_time_start_worker(self):
        if not self.datetime_start:
            await self._run_task()
        else:
            if datetime.datetime.utcnow() <= self.datetime_start:
                await self._run_task()

    async def _run_task(self):
        await asyncio.create_task(self.job())
        self._date_time_last = datetime.datetime.utcnow()
        self.repeats += 1

    def __str__(self):
        return f'Handler is {self.job=} {self.count_repeats=} {self.interval=}'
