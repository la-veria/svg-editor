import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize

from canva import CanvasLabel

app = QApplication(sys.argv)
canvas_size = QSize(800, 800)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Illustrator Clone')
        self.setFixedSize(canvas_size)
        self._init_canvas()

        self.show()

    def _init_canvas(self):
        self.label = CanvasLabel(canvas_size)
        self.setCentralWidget(self.label)

    def closeEvent(self, a0):
        return super().closeEvent(a0)

w = Window()

sys.exit(app.exec())