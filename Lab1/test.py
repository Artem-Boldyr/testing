import unittest
from unittest.mock import patch
from app import check_positive_number, count_vowels, Figure, ask_user_age


class TestDataValidation(unittest.TestCase):
    """Тести до Завдання 1"""
    def test_positive_number_valid(self):
        self.assertEqual(check_positive_number(10), "Число 10 є коректним!")

    def test_positive_number_invalid(self):
        with self.assertRaises(ValueError):
            check_positive_number(-5)
        with self.assertRaises(ValueError):
            check_positive_number(0)

    def test_positive_number_type_error(self):
        with self.assertRaises(TypeError):
            check_positive_number("abc")


class TestCountVowels(unittest.TestCase):
    """Тести до Завдання 2"""
    def test_standard_string(self):
        self.assertEqual(count_vowels("hello"), 2)

    def test_empty_string(self):
        self.assertEqual(count_vowels(""), 0)

    def test_digits_and_symbols(self):
        self.assertEqual(count_vowels("12345!@#"), 0)

    def test_ukrainian_letters(self):
        self.assertEqual(count_vowels("Привіт Світ"), 3)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            count_vowels(123)


class TestFigure(unittest.TestCase):
    """Тести до Завдання 3"""
    def test_figure_length(self):
        fig = Figure("квадрат", 10)
        self.assertEqual(fig.get_figure_length, 10)

    def test_get_angles(self):
        self.assertEqual(Figure("квадрат", 5).get_angles(), 4)
        self.assertEqual(Figure("прямокутник", 5).get_angles(), 4)
        self.assertEqual(Figure("трикутник", 5).get_angles(), 3)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)
        with self.assertRaises(ValueError):
            Figure("квадрат", -5)

    def test_unknown_figure_type(self):
        fig = Figure("шестикутник", 5)
        with self.assertRaises(ValueError):
            fig.get_angles()


class TestAdvancedUnittest(unittest.TestCase):
    """Тести до Завдання 4 (subTest та mock)"""
    def test_multiple_figures_with_subtest(self):
        data = [
            ("квадрат", 5, 4),
            ("прямокутник", 10, 4),
            ("трикутник", 3, 3),
        ]
        for fig_type, length, expected_angles in data:
            with self.subTest(fig_type=fig_type, length=length):
                fig = Figure(fig_type, length)
                self.assertEqual(fig.get_angles(), expected_angles)

    @patch("builtins.input", return_value="25")
    def test_ask_user_age_valid(self, mock_input):
        result = ask_user_age()
        self.assertEqual(result, "Ваш вік: 25")
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="abc")
    def test_ask_user_age_invalid(self, mock_input):
        result = ask_user_age()
        self.assertEqual(result, "Некоректний вік")


if __name__ == "__main__":
    unittest.main()