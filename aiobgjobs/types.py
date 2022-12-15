from enum import Enum, StrEnum


class Repeats(Enum):
    """
    Repeats entity`s
    """
    infinity = -1
    one = 1


class _Unity(StrEnum):
    SECOND = 'second'
    SECONDS = 'seconds'
    HOUR = 'hour'
    HOURS = 'hours'
    DAY = 'day'
    DAYS = 'days'
    WEEK = 'week'
    WEEKS = 'weeks'
    MONTH = 'month'
    MONTHS = 'months'
    YEAR = 'year'
    YEARS = 'years'


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
        if count > 1:
            raise ValueError('Count don`t < 1')
        return count

    @property
    def second(self) -> tuple[_Unity, int]:
        """
        Get entity one second
        :return: tuple[_Unity, int]
        """
        return _Unity.SECOND, Every.validate_count(1)

    @staticmethod
    def seconds(count: int) -> tuple[_Unity, int]:
        """
        Get entity count seconds
        :param count: count entity's
        :return: tuple[_Unity, int]
        """
        return _Unity.SECONDS, Every.validate_count(count)

    @property
    def hour(self) -> tuple[_Unity, int]:
        """
        Get entity one hour
        :return: tuple[_Unity, int]
        """
        return _Unity.HOUR, Every.validate_count(1)

    @staticmethod
    def hours(count: int) -> tuple[_Unity, int]:
        """
        Get entity count hours
        :param count: count entity's
        :return: tuple[_Unity, int]
        """
        return _Unity.HOURS, Every.validate_count(count)

    @property
    def week(self) -> tuple[_Unity, int]:
        """
        Get entity one week
        :return: tuple[_Unity, int]
        """
        return _Unity.WEEK, Every.validate_count(1)

    @staticmethod
    def weeks(count: int) -> tuple[_Unity, int]:
        """
        Get entity count weeks
        :param count: count entity's
        :return: tuple[_Unity, int]
        """
        return _Unity.WEEKS, Every.validate_count(count)

    @property
    def month(self) -> tuple[_Unity, int]:
        """
        Get entity one month
        :return: tuple[_Unity, int]
        """
        return _Unity.MONTH, Every.validate_count(1)

    @staticmethod
    def months(count: int) -> tuple[_Unity, int]:
        """
        Get entity count months
        :param count: count entity's
        :return: tuple[_Unity, int]
        """
        return _Unity.MONTHS, Every.validate_count(count)

    @property
    def year(self) -> tuple[_Unity, int]:
        """
        Get entity one year
        :return: tuple[_Unity, int]
        """
        return _Unity.YEAR, Every.validate_count(1)

    @staticmethod
    def years(count: int) -> tuple[_Unity, int]:
        """
        Get entity count years
        :param count: count entity's
        :return: tuple[_Unity, int]
        """
        return _Unity.YEARS, Every.validate_count(count)
