import unittest
from numbers import Number
from unittest.mock import patch
from operations_manager import OperationsManager
from operations_manager import login_success

class OperationsManagerTests(unittest.TestCase):

    def setUp(self):
        self.ops_manager = OperationsManager(10, 5)
        self.login_success = login_success

    def test_init(self):
        self.assertEqual(self.ops_manager.a, 10)
        self.assertEqual(self.ops_manager.b, 5)

    def test_perform_division(self):
        self.assertEqual(self.ops_manager.perform_division(), 2.0)

    def test_perform_division_with_zero_denominator(self):
        self.ops_manager.b = 0
        try:
            self.assertTrue(float('nan') in self.ops_manager.perform_division())
        except ZeroDivisionError as e:
            self.fail(e.args)

    def test_perform_division_with_negative_values(self):
        self.ops_manager.a = -10
        self.ops_manager.b = 5
        self.assertEqual(self.ops_manager.perform_division(), -2.0)

    def test_perform_division_with_large_values(self):
        self.ops_manager.a = 10**15
        self.ops_manager.b = 10**10
        self.assertEqual(self.ops_manager.perform_division(), 10**5)

    def test_perform_division_with_char_input(self):
        self.ops_manager.a = "test"
        self.ops_manager.b = 2
        try:
            self.assertIsInstance(self.ops_manager.perform_division(), Number())
        except TypeError as e:
            self.fail(e.args)

    @patch('builtins.input', side_effect=['2', '3'])
    def test_perform_division_with_user_input(self, mock_input):
        self.ops_manager.a = float(input("A = "))
        self.ops_manager.b = float(input("B = "))
        self.assertEqual(self.ops_manager.perform_division(), 2/3)

    def test_login_success(self):
        with patch('builtins.input', side_effect=['10', '5', '3 * 4']):
            expected_output = "2.0\nResult:  12" # zapravo 2 razmaka jer je koristen print sa zarezom..
            self.assertEqual(self.captured_output(self.login_success), expected_output)

    def test_login_success_numeric_not_in_expr(self):
        with patch('builtins.input', side_effect=['10', '5', '["a","b"].pop()']):
            self.assertRegex(self.captured_output(self.login_success), r".*Result:  \d+")

    def captured_output(self, func):
        """Capture the stdout and return it as a string."""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            func()
        val = f.getvalue().strip()
        return val

if __name__ == '__main__':
    unittest.main()
