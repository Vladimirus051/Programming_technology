from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from solver import solve_quadratic


class QuadraticSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Решение квадратного уравнения')

        self.label_a = QLabel('Коэффициент a:', self)
        self.input_a = QLineEdit(self)
        self.input_a.textChanged.connect(self.update_formulas)

        self.label_b = QLabel('Коэффициент b:', self)
        self.input_b = QLineEdit(self)
        self.input_b.textChanged.connect(self.update_formulas)

        self.label_c = QLabel('Коэффициент c:', self)
        self.input_c = QLineEdit(self)
        self.input_c.textChanged.connect(self.update_formulas)

        self.formula_label = QLabel('', self)  # Для отображения уравнения
        self.discriminant_formula_label = QLabel('', self)  # Для отображения формулы дискриминанта
        self.update_formulas()  # Инициализация формул

        self.solve_button = QPushButton('Решить', self)
        self.discriminant_label = QLabel('', self)
        self.result_label = QLabel('', self)

        self.solve_button.clicked.connect(self.on_solve_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.label_a)
        layout.addWidget(self.input_a)
        layout.addWidget(self.label_b)
        layout.addWidget(self.input_b)
        layout.addWidget(self.label_c)
        layout.addWidget(self.input_c)
        layout.addWidget(self.formula_label)  # Добавляем формулу уравнения в макет
        layout.addWidget(self.discriminant_formula_label)  # Добавляем формулу дискриминанта в макет
        layout.addWidget(self.solve_button)
        layout.addWidget(self.discriminant_label)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def update_formulas(self):
        a_text = self.input_a.text() or 'a'
        b_text = self.input_b.text() or 'b'
        c_text = self.input_c.text() or 'c'

        # Формируем строку с формулой уравнения
        formula_text = f"{a_text}x² + {b_text}x + {c_text} = 0"

        # Формируем строку с формулой дискриминанта
        discriminant_formula_text = f"D = {b_text}² - 4*{a_text}*{c_text}"

        # Обновляем текст меток
        self.formula_label.setText(f"Уравнение: {formula_text}")
        self.discriminant_formula_label.setText(f"Формула дискриминанта: {discriminant_formula_text}")

    def on_solve_clicked(self):
        try:
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            c = float(self.input_c.text())

            discriminant, result_text = solve_quadratic(a, b, c)

            self.discriminant_label.setText(f"Дискриминант: {discriminant:.2f}")
            self.result_label.setText(result_text)

        except ValueError:
            self.discriminant_label.setText("")
            self.result_label.setText("Пожалуйста, введите числовые значения для коэффициентов.")
