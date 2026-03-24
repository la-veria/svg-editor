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
        painter.drawPolygon(self.data_points)
        painter.end()

    def get_coordinates(self):
        return list(map(lambda i: (i.x(), i.y()), self.data_points))
    
    def svg_config(self):
        args = {
            "points": self.get_coordinates(),
            "stroke": "black",
            "stroke_width": 2,
            "fill": "none"
        }
        return args