from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, \
    QWidget, QGraphicsView, QGraphicsScene, QSpinBox, QFormLayout, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QFont
from geometry import do_intersect


class LineIntersectionApp(QMainWindow):
    def __init__(self):
        super(LineIntersectionApp, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Line Intersection Checker')
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет и макет
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Спин-бокс для количества отрезков
        self.segment_count_spinbox = QSpinBox(self)
        self.segment_count_spinbox.setRange(1, 10)
        self.segment_count_spinbox.setValue(2)
        self.segment_count_spinbox.valueChanged.connect(self.update_input_fields)
        layout.addWidget(QLabel("Количество отрезков:"))
        layout.addWidget(self.segment_count_spinbox)

        # Макет для полей ввода координат
        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)

        # Кнопка для проверки пересечения
        check_button = QPushButton('Проверить пересечение', self)
        check_button.clicked.connect(self.check_intersection_with_messages)
        layout.addWidget(check_button)

        # Кнопка для загрузки из файла
        load_button = QPushButton('Загрузить из файла', self)
        load_button.clicked.connect(self.load_from_file)
        layout.addWidget(load_button)

        # Виджет для отображения графики
        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene()

        # Установка белого фона
        self.scene.setBackgroundBrush(Qt.white)

        self.graphics_view.setScene(self.scene)

        # Контролы для зума
        zoom_layout = QHBoxLayout()

        zoom_in_button = QPushButton('+', self)
        zoom_in_button.clicked.connect(self.zoom_in)

        zoom_out_button = QPushButton('-', self)
        zoom_out_button.clicked.connect(self.zoom_out)

        zoom_layout.addWidget(zoom_in_button)
        zoom_layout.addWidget(zoom_out_button)

        layout.addWidget(self.graphics_view)

        # Добавление контролов зума в основной макет
        layout.addLayout(zoom_layout)

        main_widget.setLayout(layout)

        # Инициализация полей ввода координат
        self.update_input_fields()

    def update_input_fields(self):
        # Очистка существующих полей ввода координат
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Создание новых полей ввода на основе количества отрезков
        self.coord_inputs = []

        for i in range(self.segment_count_spinbox.value()):
            coord_input = QLineEdit(self)
            coord_input.setPlaceholderText(f'Введите координаты отрезка {i + 1}: x1 y1 x2 y2')
            self.form_layout.addRow(f'Отрезок {i + 1}:', coord_input)
            self.coord_inputs.append(coord_input)

    def check_intersection_with_messages(self):

        segments = []  # инициализация списка сегментов

        for coord_input in self.coord_inputs:
            coords = coord_input.text().split()

            if len(coords) != 4:
                QMessageBox.warning(self, "Ошибка", "Введите корректные координаты: x1 y1 x2 y2")
                return

            try:
                x1, y1, x2, y2 = map(float, coords)
                segments.append(((x1, y1), (x2, y2)))
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Ошибка в формате координат.")
                return

        if len(segments) < 2:
            QMessageBox.warning(self, "Ошибка", "Необходимо как минимум два отрезка для проверки пересечения.")
            return

        intersections_found = False
        intersection_pairs = []

        # Проверка каждого отрезка на пересечение с другими
        for i in range(len(segments)):
            for j in range(i + 1, len(segments)):
                if do_intersect(segments[i][0], segments[i][1], segments[j][0], segments[j][1]):
                    intersections_found = True
                    intersection_pairs.append((i + 1, j + 1))

        if intersections_found:
            message = "Пересекаются следующие отрезки:\n" + "\n".join(
                [f"Отрезки {pair[0]} и {pair[1]}" for pair in intersection_pairs])
            QMessageBox.information(self, "Результаты пересечения", message)
        else:
            QMessageBox.information(self, "Результаты пересечения", "Нет пересечений")

        # Отрисовка линий и осей
        self.draw_lines(segments)

    def load_from_file(self):
        options = QFileDialog.Options()

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл с координатами",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if filename:
            with open(filename, 'r') as file:
                lines = file.readlines()

                num_segments = len(lines)
                self.segment_count_spinbox.setValue(num_segments)

                for i in range(num_segments):
                    coords = lines[i].strip()
                    if len(coords.split()) == 4:
                        self.coord_inputs[i].setText(coords)

    def draw_lines(self, segments):

        pen_colors = [Qt.red,
                      Qt.blue,
                      Qt.green,
                      Qt.yellow,
                      Qt.cyan,
                      Qt.magenta,
                      Qt.darkRed,
                      Qt.darkGreen,
                      Qt.darkBlue,
                      Qt.darkCyan]

        font = QFont("Arial", 8)

        self.scene.clear()

        # Отрисовка осей с единицами измерения
        axis_pen = QPen(Qt.black)

        # Ось X с единицами измерения
        for x in range(-400, 401, 50):
            self.scene.addLine(x, -5, x, +5, axis_pen)  # метки единиц на оси X
            if x != 0:  # избегаем двойного отображения (0) в начале координат
                text = self.scene.addText(f"{x}", font)
                text.setPos(x + 5, -20)  # корректировка позиции

        # Ось Y с единицами измерения
        for y in range(-300, +301, +50):
            self.scene.addLine(-5, y, +5, y, axis_pen)  # метки единиц на оси Y
            if y != 0:  # избегаем двойного отображения (0) в начале координат
                text = self.scene.addText(f"{-y}", font)  # инвертируем Y для соответствия направлению системы координат
                text.setPos(+10, -y - 10)  # корректировка позиции

        # Отрисовка линий осей последней для отображения под метками единиц и надписями
        self.scene.addLine(-400,
                           0,
                           400,
                           0,
                           axis_pen)  # ось X

        self.scene.addLine(0, -300,
                           0,
                           300,
                           axis_pen)  # ось Y

        for i, segment in enumerate(segments):
            pen = QPen(pen_colors[i % len(pen_colors)])

            p1, q1 = segment

            # Отрисовка отрезка линии
            line = self.scene.addLine(p1[0], -p1[1], q1[0], -q1[1], pen)

            # Отображение координат точек на каждом конце отрезка линии
            text_p1 = self.scene.addText(f"({p1[0]},{p1[1]})", font)
            text_p2 = self.scene.addText(f"({q1[0]},{q1[1]})", font)

            text_p1.setPos(p1[0] + 5, -p1[1] - 20)  # корректировка позиции чтобы избежать перекрытия с точками/линиями
            text_p2.setPos(q1[0] + 5, -q1[1] - 20)  # корректировка позиции чтобы избежать перекрытия с точками/линиями

    def zoom_in(self):
        """Увеличение масштаба."""
        factor = 1.25
        self.graphics_view.scale(factor, factor)

    def zoom_out(self):
        """Уменьшение масштаба."""
        factor = 0.8
        self.graphics_view.scale(factor, factor)
