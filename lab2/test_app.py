import pytest


# Клас Figure визначено прямо тут, щоб не потрібен був окремий файл app.py
class Figure:
    FIGURES = ["квадрат", "трикутник", "прямокутник"]

    def __init__(self, figure_type: str, length: int | float):
        if figure_type not in self.FIGURES:
            raise ValueError(f"Неприпустимий тип фігури: {figure_type}")
        if length <= 0:
            raise ValueError("Довжина повинна бути більше 0")

        self.type = figure_type
        self.length = length

    @property
    def get_figure_length(self):
        return self.length


# ==============================================================================
# ЧАСТИНА 1: Параметризація та Fixtures
# ==============================================================================

# ⭐ Завдання 1: Параметризований тест для всіх дозволених фігур
@pytest.mark.parametrize("figure_type", Figure.FIGURES)
def test_all_allowed_figures(figure_type):
    fig = Figure(figure_type, 1)
    assert fig.type == figure_type


# ⭐ Завдання 2: Fixture, яка повертає фігуру з довжиною 10
@pytest.fixture
def figure_length_10():
    return Figure("квадрат", 10)


def test_figure_length_10_properties(figure_length_10):
    assert figure_length_10.get_figure_length == 10
    assert figure_length_10.type == "квадрат"


# 🔥 Завдання 3: Тести для НЕправильних типів та НЕправильних значень довжини
@pytest.mark.parametrize("invalid_type", ["круг", "ромб", "", 123, None])
def test_invalid_figure_type(invalid_type):
    with pytest.raises((ValueError, AssertionError)):
        Figure(invalid_type, 5)


@pytest.mark.parametrize("invalid_length", [0, -5, -100])
def test_invalid_figure_length(invalid_length):
    with pytest.raises((ValueError, AssertionError)):
        Figure("квадрат", invalid_length)


# ==============================================================================
# ЧАСТИНА 2: Розширені можливості pytest
# ==============================================================================

# ⭐ Завдання 7: Позначення двох тестів маркером unit
@pytest.mark.unit
def test_triangle_creation():
    fig = Figure("трикутник", 4)
    assert fig.type == "трикутник"


@pytest.mark.unit
def test_square_creation():
    fig = Figure("квадрат", 5)
    assert fig.type == "квадрат"


# ⭐ Завдання 8: Fixture зі scope="module"
@pytest.fixture(scope="module")
def shared_allowed_figures():
    return Figure.FIGURES


def test_check_allowed_contains_square(shared_allowed_figures):
    assert "квадрат" in shared_allowed_figures


def test_check_allowed_contains_triangle(shared_allowed_figures):
    assert "трикутник" in shared_allowed_figures


# 🔥 Завдання 9: Навмисно зламаний тест
def test_intentional_failure():
    assert 1 == 2, "Навмисна помилка для перевірки прапорців pytest"