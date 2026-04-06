from PyQt6.QtGui import QPolygon

class Shape(QPolygon):
    def __init__(self, data_points=None):
        super().__init__(data_points)

    def get_coordinates(self):
        return list(map(lambda i: (i.x(), i.y()), self))
    
    def svg_config(self):
        args = {
            "points": self.get_coordinates(),
            "stroke": "black",
            "stroke_width": 2,
            "fill": "none"
        }
        return args