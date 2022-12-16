import datetime
import functools
from dataclasses import dataclass
from enum import StrEnum, IntEnum


class Repeats(IntEnum):
    """
    Repeats entity`s
    """
    infinity = -1
    one = 1


class _Unity(StrEnum):
    MILLISECONDS = 'milliseconds'
    MICROSECONDS = 'microseconds'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    HOURS = 'hours'
    DAYS = 'days'
    WEEKS = 'weeks'


class EveryResult:
    __slots__ = (
        'delta'
    )

    def __init__(self, unity: _Unity, count: int):

        assert isinstance(unity, _Unity)
        assert isinstance(count, int)

        self.delta = datetime.timedelta(**{unity: count})


class Every:
    """
    Static class Every
    """

    @staticmethod
    def validate_count(count: int) -> int:
        """
        Validate count entity
        :param count: count entity
        :return: int
        :raise: ValueError('Count don`t < 1')
        """
        if count < 1:
            raise ValueError('Count don`t < 1')
        return count

    @staticmethod
    def millisecond() -> EveryResult:
        """
        Get entity one millisecond
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.MILLISECONDS, Every.validate_count(1))

    @staticmethod
    def milliseconds(count: int) -> EveryResult:
        """
        Get entity count milliseconds
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.MILLISECONDS, Every.validate_count(count))

    @staticmethod
    def microsecond() -> EveryResult:
        """
        Get entity one microsecond
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.MICROSECONDS, Every.validate_count(1))

    @staticmethod
    def microseconds(count: int) -> EveryResult:
        """
        Get entity count microseconds
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.MICROSECONDS, Every.validate_count(count))

    @staticmethod
    def second() -> EveryResult:
        """
        Get entity one second
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.SECONDS, Every.validate_count(1))

    @staticmethod
    def seconds(count: int) -> EveryResult:
        """
        Get entity count seconds
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.SECONDS, Every.validate_count(count))

    @staticmethod
    def minute() -> EveryResult:
        """
        Get entity one minute
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.MINUTES, Every.validate_count(1))

    @staticmethod
    def minutes(count: int) -> EveryResult:
        """
        Get entity count minutes
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.MINUTES, Every.validate_count(count))

    @staticmethod
    def hour() -> EveryResult:
        """
        Get entity one hour
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.HOURS, Every.validate_count(1))

    @staticmethod
    def hours(count: int) -> EveryResult:
        """
        Get entity count hours
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.HOURS, Every.validate_count(count))

    @staticmethod
    def week() -> EveryResult:
        """
        Get entity one week
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.WEEKS, Every.validate_count(1))

    @staticmethod
    def weeks(count: int) -> EveryResult:
        """
        Get entity count weeks
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.WEEKS, Every.validate_count(count))

    class WeekDays:
        pass
