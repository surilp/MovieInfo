from util import convert_date
import unittest


class TestUtilMethods(unittest.TestCase):

    def test_convert_date(self):
        self.assertEqual(convert_date("2020-01-01"), 'Jan 01, 2020')


if __name__ == '__main__':
    unittest.main()
