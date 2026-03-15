import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt6.QtCore import Qt, QSize

app = QApplication(sys.argv)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Illustrator Clone')
        self.setFixedSize(400, 400)
        self.init_canvas()

        self.show()

    def init_canvas(self):
        self.label = CanvasLabel()
        self.setCentralWidget(self.label)

    def closeEvent(self, a0):
        print(self.label.data_points)
        return super().closeEvent(a0)


class CanvasLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.canvas = QPixmap(QSize(400, 400))
        self.canvas.fill(QColor('white'))

        self.setPixmap(self.canvas)

        self.init_list()
        self.init_drawing()

    def init_list(self):
        self.previousPoint = None
        self.previousCanva = self.canvas
        self.data_points = []

    def init_drawing(self):
        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    def mousePressEvent(self, event):
        # print(event.pos().x(), event.pos().y())

        position = event.pos()
        self.previousPoint = position
        self.previousCanva = self.canvas.copy()

        self.data_points.append([position.x(), position.y()])

        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.drawPoint(position.x(), position.y())
        painter.end()

        self.setPixmap(self.canvas)

    def mouseMoveEvent(self, event):      
        if not(self.previousPoint): return

        position = event.pos()

        self.canvas = self.previousCanva.copy()

        self.setPixmap(self.canvas)

        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.drawLine(self.previousPoint, position)
        painter.end()
        
        self.setPixmap(self.canvas)
        
w = Window()

sys.exit(app.exec())