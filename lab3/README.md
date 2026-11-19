# Звіт до роботи: Покриття коду (Code Coverage)

## Мета роботи
Навчитися вимірювати покриття коду тестами за допомогою `coverage.py` та плагіна `pytest-cov`, аналізувати покриття рядків (line coverage) і розгалужень (branch coverage), налаштовувати пороги якості, генерувати HTML/XML-звіти та розуміти обмеження метрики покриття.

---

## Виконання роботи

### 1. Код програми та тестів (`lab3/test_app.py`)
Для мінімізації кількості файлів основний клас `Figure`, точка входу `main()` та набір тестів `TestFigure` (сумісний одночасно з `unittest` та `pytest`) реалізовані в одному файлі `test_app.py`:

```python
import unittest


class Figure:
    def __init__(self, figure_type: str):
        self.figure_type = figure_type

    @property
    def get_angles(self) -> int:
        if self.figure_type == "triangle":
            return 3
        elif self.figure_type == "square":
            return 4
        elif self.figure_type == "rectangle":
            return 4
        raise ValueError("Невідома фігура")


def main():  # pragma: no cover
    fig = Figure("triangle")
    print(f"Кутів: {fig.get_angles}")


class TestFigure(unittest.TestCase):
    def test_triangle_angles(self):
        self.assertEqual(Figure("triangle").get_angles, 3)

    def test_square_angles(self):
        self.assertEqual(Figure("square").get_angles, 4)

    def test_rectangle_angles(self):
        self.assertEqual(Figure("rectangle").get_angles, 4)

    def test_unknown_figure(self):
        with self.assertRaises(ValueError):
            _ = Figure("circle").get_angles

    def test_without_assert(self):
        # Виконує рядок коду, але не перевіряє результат
        _ = Figure("triangle").get_angles


if __name__ == "__main__":  # pragma: no cover
    main()

```

---

### 2. Окремий запуск через `unittest`

Перед вимірюванням очищено попередні дані (`coverage erase`), виконано тести з увімкненим аналізом розгалужень (`--branch`) та сформовано консольний звіт:

```bash
poetry run coverage erase
poetry run coverage run --branch -m unittest test_app.py
poetry run coverage report -m

```

**Результат виконання:**

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK

Name          Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------
test_app.py      25      0      6      0   100%
---------------------------------------------------------
TOTAL            25      0      6      0   100%

```

---

### 3. Окремий запуск через `pytest` та перевірка порогу покриття

Запущено тестування через `pytest-cov` із перевіркою розгалужень (`--cov-branch`), виводом пропущених рядків (`--cov-report=term-missing`) та мінімальним порогом покриття 90% (`--cov-fail-under=90`):

```bash
poetry run coverage erase
poetry run pytest --cov=test_app --cov-branch --cov-report=term-missing --cov-fail-under=90 -v

```

**Результат виконання:**

```text
================================ tests coverage ================================
_______________ coverage: platform win32, python 3.13.7-final-0 ________________

Name          Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------
test_app.py      25      0      6      0   100%
---------------------------------------------------------
TOTAL            25      0      6      0   100%
Required test coverage of 90% reached. Total coverage: 100.00%
============================== 5 passed in 0.11s ===============================

```

---

### 4. Порівняння покриття до та після додавання тестів

* **До додавання тестів (лише перевірка `"triangle"`):** виконується тільки перша умова `if self.figure_type == "triangle":`. Гілки `elif` для `"square"`, `"rectangle"` та викидання винятку `raise ValueError("Невідома фігура")` залишаються непокритими — у звіті з'являються пропущені оператори (`Miss`) та частково пройдені розгалуження (`BrPart`).
* **Після додавання тестів (`test_square_angles`, `test_rectangle_angles`, `test_unknown_figure`):** пройдені всі умовні переходи та винятки, кількість пропущених рядків і неповних гілок зменшилася до `0`, а загальне покриття досягло **100%**.

---

### 5. Генерація HTML- та XML-звітів

Для формування звітів у різних форматах виконано команди:

```bash
poetry run coverage html
poetry run coverage xml

```

* **HTML-звіт (`htmlcov/index.html`):** призначений **для людей (розробників)**. Зручний для візуального аналізу в браузері: зеленим підсвічуються виконані рядки, червоним — пропущені, жовтим — частково пройдені розгалуження.
* **XML-звіт (`coverage.xml`):** призначений **для автоматизованих інструментів та CI/CD-систем** (GitHub Actions, SonarQube, Codecov тощо) для автоматичного зчитування метрик і контролю якості коду.

---

### 6. Використання `pragma: no cover` та `.gitignore`

* **Виключення коду (`# pragma: no cover`):** застосовано до функції `main()` та блоку `if __name__ == "__main__":`, оскільки це лише точка входу для консольного запуску скрипта, яка не містить бізнес-логіки та не потребує модульного тестування.
* **Налаштування `.gitignore`:** до файлу додано службові артефакти `__pycache__/`, `.coverage`, `htmlcov/`, `coverage.xml` та `.pytest_cache/`, щоб не забруднювати Git-репозиторій тимчасовими файлами звітності.

---

## Відповіді на контрольні питання

1. **У чому різниця між покриттям рядків (Line coverage) і покриттям розгалужень (Branch coverage)?**
* *Line coverage* перевіряє лише факт того, що кожен виконуваний рядок коду був запущений хоча б один раз під час тестування.
* *Branch coverage* контролює, чи пройшли тести всі можливі напрямки умовних конструкцій (`if` / `elif` / `else`) — як у гілку `True`, так і у гілку `False`.


2. **Чому 100% покриття коду не гарантує відсутності багів?**
* Метрика покриття фіксує лише факт виконання рядків коду, але не перевіряє коректність логіки чи очікуваних результатів. Наприклад, тест `test_without_assert` викликає `Figure("triangle").get_angles`, що підвищує відсоток покриття, але без інструкції `assert` він не виявить помилку, якщо метод поверне неправильне число.



---

## Висновок

Під час виконання роботи було освоєно інструменти вимірювання покриття коду `coverage.py` та `pytest-cov`, налаштовано перевірку розгалужень і мінімального порогу покриття (90%), згенеровано HTML- та XML-звіти, а також на практиці перевірено різницю між виконанням коду та валідацією його результатів.