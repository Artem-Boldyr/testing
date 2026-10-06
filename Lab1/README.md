# Звіт до лабораторної роботи
## Тема: Загальне тестування та юніт-тести

---

### Покрокове виконання завдань:

#### 1. Перевірка даних (`assert` та `ValueError`)
* **Завдання:** Створити власну перевірку введеного числа за допомогою `assert` або `raise ValueError` та описати у звіті результат для правильного й неправильного введення.
* **Реалізація:**
```
def check_positive_number(number: int) -> str:
    if not isinstance(number, (int, float)):
        raise TypeError("Введено не число!")
    if number <= 0:
        raise ValueError("Число має бути більшим за нуль!")
    return f"Число {number} є коректним!"
```
# Приклади виклику:
print(check_positive_number(10))   # Правильне введення
# check_positive_number(-5)       # Викличе ValueError

* **Результат:** 
  - При передачі правильного значення (`10`) функція повертає підтверджувальний рядок `"Число 10 є коректним!"`.
  - При передачі некоректних даних (`-5` або `0`) програма зупиняє виконання та генерує виняток `ValueError: Число має бути більшим за нуль!`, запобігаючи подальшій роботі з помилковими даними.

---

#### 2. Тестування функцій та перевірка винятків
* **Завдання:** Створити функцію, яка рахує кількість голосних літер у рядку, напишіть щонайменше три тести для неї (включаючи тести для порожнього рядка, цифр та українських літер).
* **Реалізація:**
```
import unittest

def count_vowels(text: str) -> int:
    if not isinstance(text, str):
        raise TypeError("Аргумент має бути рядком")
    vowels_set = set("аеєиіїоуюяaeiouAEIOUАЕЄИІЇОУЮЯ")
    return sum(1 for char in text if char in vowels_set)

class TestCountVowels(unittest.TestCase):
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
```

* **Результат:** Усі 5 unit-тестів успішно виконуються. Функція коректно обробляє звичайні та порожні рядки, ігнорує цифри/символи, розпізнає українські голосні літери та викидає `TypeError` при передачі нестрічкового типу даних.

---

#### 3. Робота з базовим прикладом `Figure`
* **Завдання:** 
  1. Розкоментувати тест довжини, знайти та виправити помилку в реалізації.
  2. Додати метод `get_angles` і тести для квадрата, прямокутника та трикутника.
  3. Додати тести для крайніх випадків (нульова/від'ємна довжина, невідомий тип фігури).

* **Реалізація:**

# app.py
```
class Figure:
    def __init__(self, figure_type: str, length: float):
        if length <= 0:
            raise ValueError("Довжина повинна бути більшою за 0")
        self.figure_type = figure_type.lower()
        self.length = length

    @property
    def get_figure_type(self) -> str:
        return self.figure_type

    @property
    def get_figure_length(self) -> float:
        # Виправлено повернення атрибута length замість помилкової логіки
        return self.length

    def get_angles(self) -> int:
        angles_map = {
            "квадрат": 4,
            "прямокутник": 4,
            "трикутник": 3
        }
        if self.figure_type not in angles_map:
            raise ValueError(f"Невідомий тип фігури: {self.figure_type}")
        return angles_map[self.figure_type]

```
# test.py
```
class TestFigure(unittest.TestCase):
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
```
* **Результат:** 
  - Було виявлено помилку в розкоментованому тесті `get_figure_length`. Після виправлення геттера тест пройшов.
  - Метод `get_angles()` успішно повертає кількість кутів для базових фігур та піднімає `ValueError` для невідомих фігур.
  - Конструктор `Figure` розширено перевіркою від'ємної та нульової довжини.

---

#### 4. Розширені можливості `unittest` (`subTest` та `mock.patch`)
* **Завдання:** 
  1. Додати тест із `subTest` для всіх типів `Figure`.
  2. Створити функцію з `input()` та протестувати її за допомогою `unittest.mock.patch`.

* **Реалізація:**
```
from unittest.mock import patch

def ask_user_age() -> str:
    age = input("Введіть ваш вік: ")
    if not age.isdigit():
        return "Некоректний вік"
    return f"Ваш вік: {age}"

class TestAdvancedUnittest(unittest.TestCase):
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
```
* **Результат:** 
  - `subTest` дозволив виконати перевірку кількох наборів даних у межах одного тестового методу. У разі падіння одного варіанту інші продовжують перевірятися.
  - `@patch("builtins.input")` підмінив інтерактивне введення користувача консолі, дозволивши протестувати функцію `ask_user_age()` повністю в автоматичному режимі.

---

### Висновок та результати виконання:

#### Команди для запуску тестів:
python test.py
python -m unittest -v test.py

#### Результат виконання тестів у консолі (Terminal Output):
test_ask_user_age_invalid (test.TestAdvancedUnittest) ... ok
test_ask_user_age_valid (test.TestAdvancedUnittest) ... ok
test_multiple_figures_with_subtest (test.TestAdvancedUnittest) ... ok
test_figure_length (test.TestFigure) ... ok
test_get_angles (test.TestFigure) ... ok
test_invalid_length (test.TestFigure) ... ok
test_unknown_figure_type (test.TestFigure) ... ok
test_digits_and_symbols (test.TestCountVowels) ... ok
test_empty_string (test.TestCountVowels) ... ok
test_invalid_type (test.TestCountVowels) ... ok
test_standard_string (test.TestCountVowels) ... ok
test_ukrainian_letters (test.TestCountVowels) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.003s

OK

#### Приклад тесту, який спочатку не проходив (до виправлення):
FAIL: test_figure_length (test.TestFigure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test.py", line 12, in test_figure_length
    self.assertEqual(fig.get_figure_length, 10)
AssertionError: None != 10

*Після виправлення повернення значення `return self.length` у властивості `get_figure_length` класів `Figure`, тест перейшов у стан **OK**.*

#### Пояснення призначення `subTest` та `mock`:
1. **`subTest`**: Дозволяє об'єднати серію подібних перевірок у циклі. Головна перевага полягає в тому, що якщо один із наборів даних викликає помилку, виконання тесту **не переривається**, а виводяться деталі для кожного конкретного невдалого випадку.
2. **`unittest.mock (patch)`**: Дозволяє ізолювати тешований код від зовнішніх залежностей (таких як введення з клавіатури `input()`, мережеві запити, робота з базою даних чи файловою системою). Це робить unit-тести швидкими, незалежними та повторюваними.