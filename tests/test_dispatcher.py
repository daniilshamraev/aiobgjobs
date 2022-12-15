import sys
import unittest
import logging
from aiobgjobs.dispatcher import BgDispatcher


class TestBgDispatcher(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.logger = logging.Logger(name=__name__)
        self.logger.setLevel(logging.DEBUG)
        super().__init__(*args, **kwargs)

    def test_len(self):
        dp = BgDispatcher()

        self.assertEqual(
            first=0,
            second=dp.__len__(),
            msg='Fail len'
        )

    def test_error_logger(self):
        dp = BgDispatcher(logger=self.logger)

        self.assertEqual(
            first=0,
            second=dp.__len__(),
            msg='Fail len'
        )


