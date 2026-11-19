import unittest


# --- ОСНОВНИЙ КОД ПРОГРАМИ ---
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


# --- ТЕСТИ (СУМІСНІ З UNITTEST ТА PYTEST) ---
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