import unittest
from calculator import calc


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc(1, 1, "+"), 2)

    def test_subtract(self):
        self.assertEqual(calc(1, 3, "-"), -2)

    def test_multiply(self):
        self.assertEqual(calc(10, 5, "*"), 50)

    def test_divide(self):
        self.assertEqual(calc(10, 5, "/"), 2)

    def test_divide_by_zero(self):
        self.assertEqual(calc(1, 0, "/"), "нельзя делить на 0")

    def test_multiply_by_zero(self):
        self.assertEqual(calc(1, 0, "*"), 0)

    def test_add_with_zero(self):
        self.assertEqual(calc(7, 0, "+"), 7)

    def test_zero_divided_by_number(self):
        self.assertEqual(calc(0, 5, "/"), 0)


if __name__ == "__main__":
    unittest.main()
