import sys
from PyQt5.QtWidgets import QApplication
from ui import LineIntersectionApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LineIntersectionApp()
    ex.show()
    sys.exit(app.exec_())
