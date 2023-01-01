import datetime
import sys
from enum import IntEnum
from typing import Any


class Repeats(IntEnum):
    """
    Repeats entity`s
    """
    infinity = -1
    one = 1


try:
    from enum import StrEnum

    class _Unity(StrEnum):
        MILLISECONDS = 'milliseconds'
        MICROSECONDS = 'microseconds'
        MINUTES = 'minutes'
        SECONDS = 'seconds'
        HOURS = 'hours'
        DAYS = 'days'
        WEEKS = 'weeks'

except ImportError:
    from enum import Enum


    class _Unity(str, Enum):
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

    def __add__(self, other: Any):
        """
        Add timedelta to timedelta
        :param other: timedelta
        :return: timedelta

        >>> td = EveryResult(unity=_Unity.SECONDS, count=1) + EveryResult(unity=_Unity.SECONDS, count=1)
        >>> if td == datetime.timedelta(seconds=2): print(True)
        True
        """
        assert isinstance(other, datetime.timedelta)

        return self.delta + other


class _WeekDaysUnity(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class WeekDayEveryResult(EveryResult):
    __slots__ = (
        'delta',
        'datetime_start'
    )

    def __init__(self, unity: _Unity, count: int, datetime_start: datetime.datetime, tz=None):
        assert datetime_start > datetime.datetime.now(tz)
        self.datetime_start = datetime_start

        super().__init__(unity, count)

    def __str__(self):
        return f'{self.delta.days=} {self.delta.seconds=} {self.datetime_start}'


class Every:
    """
    Static class Every
    """

    @staticmethod
    def validate_count(count: int) -> int:
        """
        Validate count entity
        :param count: Count entity. Must not be less than -1.
        :return: int
        :raise: ValueError('Count don`t < 1')

        >>> Every.validate_count(-10)
        Traceback (most recent call last):
        ...
        ValueError: Count don`t < 1
        >>> Every.validate_count(10)
        10
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
    def day(hour: int, minute: int, tz=None) -> EveryResult:
        """
        Get entity one day
        :param hour: Hours
        :param minute: Minutes
        :param tz: TimeZone
        :return: Every.EveryResult
        """
        return Every.weekdays.__call__(
            day=_WeekDaysUnity(datetime.date.today().weekday()),
            hour=hour,
            minute=minute,
            tz=tz
        )

    @staticmethod
    def days(count: int) -> EveryResult:
        """
        Get entity count days
        :param count: count entity's
        :return: Every.EveryResult
        """
        return EveryResult(_Unity.WEEKS, Every.validate_count(count))

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

    class weekdays:
        """Weekdays class"""

        @staticmethod
        def __call__(day: _WeekDaysUnity, hour: int, minute: int, tz=None) -> WeekDayEveryResult:
            """

            :rtype: WeekDayEveryResult

            >>> Every.weekdays.friday(hour=10, minute=30)
            """

            datetime_now = datetime.datetime.now(tz)

            today_week_day = datetime_now.weekday() + 1

            if today_week_day == day and \
                    (datetime_now.hour < hour or
                     (datetime_now.hour == hour and datetime_now.minute <= minute)):
                datetime_start = datetime.datetime(
                    year=datetime_now.year,
                    month=datetime_now.month,
                    day=datetime_now.day,
                    hour=hour,
                    minute=minute
                )

                return WeekDayEveryResult(
                    unity=_Unity.WEEKS,
                    count=1,
                    datetime_start=datetime_start
                )
            elif today_week_day > day:
                datetime_start = datetime.datetime.today() + datetime.timedelta(
                    days=today_week_day - day,
                    hours=hour,
                    minutes=minute
                ) + Every.week().delta
                return WeekDayEveryResult(
                    unity=_Unity.WEEKS,
                    count=1,
                    datetime_start=datetime_start
                )
            else:
                datetime_start = datetime.datetime.today() + datetime.timedelta(
                    days=today_week_day + day,
                    hours=hour,
                    minutes=minute
                ) + Every.week().delta
                return WeekDayEveryResult(
                    unity=_Unity.WEEKS,
                    count=1,
                    datetime_start=datetime_start
                )

        @staticmethod
        def _validate_hour_and_minute(hour, minute):
            assert isinstance(hour, int) and 23 >= hour >= 0
            assert isinstance(minute, int) and 59 >= hour >= 0

        @staticmethod
        def monday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Понедельник
            :param hour:
            :param minute:
            :return: WeekDayEveryResult
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            return Every.weekdays.__call__(
                _WeekDaysUnity.MONDAY,
                hour,
                minute
            )

        @staticmethod
        def tuesday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Вторник
            :param hour:
            :param minute:
            :return:
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            return Every.weekdays.__call__(
                _WeekDaysUnity.TUESDAY,
                hour,
                minute
            )

        @staticmethod
        def wednesday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Среда
            :param hour:
            :param minute:
            :return:
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            return Every.weekdays.__call__(
                _WeekDaysUnity.WEDNESDAY,
                hour,
                minute
            )

        @staticmethod
        def thursday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Четверг
            :param hour:
            :param minute:
            :return:
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            return Every.weekdays.__call__(
                _WeekDaysUnity.WEDNESDAY,
                hour,
                minute
            )

        @staticmethod
        def friday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Пятница
            :param hour:
            :param minute:
            :return:
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            result = Every.weekdays.__call__(
                _WeekDaysUnity.WEDNESDAY,
                hour,
                minute
            )

            print(result)

            return result

        @staticmethod
        def saturday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Суббота
            :param hour:
            :param minute:
            :return:
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            return Every.weekdays.__call__(
                _WeekDaysUnity.SATURDAY,
                hour,
                minute
            )

        @staticmethod
        def sunday(hour: int = 0, minute: int = 0) -> WeekDayEveryResult:
            """
            Воскресенье
            :param hour:
            :param minute:
            :return:
            """
            Every.weekdays._validate_hour_and_minute(hour, minute)

            return Every.weekdays.__call__(
                _WeekDaysUnity.SUNDAY,
                hour,
                minute
            )
