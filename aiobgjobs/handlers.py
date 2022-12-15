import asyncio
import datetime

from aiobgjobs.jobs import Job
from aiobgjobs.types import Repeats, _Unity, Every


class Handler:

    def __init__(
            self,
            job: Job,
            interval: datetime.timedelta | None = None,
            count_repeats: int | Repeats = Repeats.infinity,
            every: Every | None = None,
            datetime_start: datetime.datetime | None = datetime.datetime.utcnow()
    ):
        assert job
        assert isinstance(job, Job), 'Job need instance class Job'
        self.job = job

        assert not (bool(interval) and bool(every)), 'You don`t use interval and every'

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
            if isinstance(count_repeats, Repeats) or isinstance(count_repeats, int):
                assert count_repeats <= -1
            else:
                raise ValueError(f'{count_repeats=} don`t validate')
            self.count_repeats = count_repeats
            self.repeats = 0

        self._date_time_last: datetime.datetime | None = None

    async def __call__(self, *args, **kwargs):
        if not self.count_repeats == -1 and self.repeats >= self.count_repeats:
            return
        elif hasattr(self, 'every'):
            await self._date_time_last_worker(datetime.datetime.utcnow() - self._date_time_last)
        elif hasattr(self, 'interval'):
            await self._date_time_last_worker(self.interval)

    async def _date_time_last_worker(self, _t_d: datetime.timedelta):
        if not self._date_time_last:
            await self._date_time_start_worker()
        else:
            await self._time_delta_worker(_t_d)

    async def _time_delta_worker(self, _t_d_f: datetime.timedelta):
        if hasattr(self, 'every'):
            _u, _c = self.every
            if _c > 1:
                _u = _u.removesuffix('s')
            _t_d_s = datetime.timedelta(**{_u.name: _c})
        else:
            _t_d_s = datetime.datetime.utcnow() - self._date_time_last
        if _t_d_f <= _t_d_s:
            await self._run_task()

    async def _date_time_start_worker(self):
        if not self.datetime_start:
            await self._run_task()
        else:
            if datetime.datetime.utcnow() >= self.datetime_start:
                await self._run_task()

    async def _run_task(self):
        self._date_time_last = datetime.datetime.utcnow()
        self.repeats += 1
        await asyncio.create_task(self.job())

    def __str__(self):
        return f'<Handler is Job: {str(self.job)} | Count repeats:{str(self.count_repeats)} | Interval: {str(self.interval)}>'
