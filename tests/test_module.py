import unittest

import stactools.nasa_nex_gddp_cmip6


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.nasa_nex_gddp_cmip6.__version__)
