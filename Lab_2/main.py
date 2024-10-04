import sys
from PyQt5.QtWidgets import QApplication
from ui import QuadraticSolver

if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = QuadraticSolver()
    solver.show()
    sys.exit(app.exec_())
