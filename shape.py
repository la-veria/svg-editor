from PyQt6.QtGui import QPainter

class Shape():
    def __init__(self, start_point):
        self.data_points = []
        self.start_point = start_point

    def addPoint(self, point):
        self.data_points.append(point)

    def drawShape(self, canvas, pen):      
        painter = QPainter(canvas)
        painter.setPen(pen)
        (painter.drawPolygon if len(self.data_points) >= 3 else painter.drawPolyline)(self.data_points)
        painter.end()