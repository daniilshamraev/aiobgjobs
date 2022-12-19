import asyncio
import functools
from typing import Callable, Iterable, Coroutine, Any


class Job(object):
    """
    Base Job
    """

    def __init__(
            self,
            func: Callable,
            kwargs: dict | None = None,
            name: str = None,
    ):
        """
        Create new Job
        :param func:
        :param args:
        :param name:
        """
        self.name = name
        self._func = functools.partial(func, **kwargs if kwargs else {})

        self.is_done = False

    def __str__(self):
        return f'<Job is Name: {self.name} | Func name: {self._func.__class__.func.__class__.__name__}>'

    async def __call__(self, *args, **kwargs):
        await self._func()
