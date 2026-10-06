def check_positive_number(number: int) -> str:
    """Завдання 1: Перевірка введеного числа."""
    if not isinstance(number, (int, float)):
        raise TypeError("Введено не число!")
    if number <= 0:
        raise ValueError("Число має бути більшим за нуль!")
    return f"Число {number} є коректним!"


def count_vowels(text: str) -> int:
    """Завдання 2: Підрахунок голосних літер."""
    if not isinstance(text, str):
        raise TypeError("Аргумент має бути рядком")
    vowels_set = set("аеєиіїоуюяaeiouAEIOUАЕЄИІЇОУЮЯ")
    return sum(1 for char in text if char in vowels_set)


class Figure:
    """Завдання 3: Клас для роботи з геометричними фігурами."""
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
        # Виправлена помилка (повертає довжину)
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


def ask_user_age() -> str:
    """Завдання 4: Функція з input() для тестування з mock.patch."""
    age = input("Введіть ваш вік: ")
    if not age.isdigit():
        return "Некоректний вік"
    return f"Ваш вік: {age}"