import asyncio
import functools
from typing import Callable, Iterable, Coroutine, Any


class Job(object):
    """
    Base Job
    """

    def __init__(
            self,
            func: Coroutine[Any, Any, Any],
            name: str = None,
    ):
        """
        Create new Job
        :param func:
        :param args:
        :param name:
        """
        self.name = name
        self._func = func

        self.is_done = False

    async def __call__(self, *args, **kwargs):
        await self._func
