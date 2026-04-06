from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

import numpy as np
from enum import Enum

from shape import Shape

class CanvaMode(Enum):
    EDIT ='edit'
    SELECT ='select'

class CanvasLabel(QLabel):
    def __init__(self, canvas_size):
        super().__init__()

        self.setMouseTracking(True)

        self.canvas = QPixmap(canvas_size)
        self.canvas.fill(QColor('white'))
        self.setPixmap(self.canvas)

        self._init_list()

    def _init_list(self):
        self.active_shape = None
        self.previousPoint = None
        self.previousCanva = self.canvas
        self.shapes = []
        self.mode = 'select'

    def _init_drawing(self, start_point):
        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        new_shape = Shape(start_point)
        self.active_shape = new_shape
        self.shapes.append(new_shape)

    def export_coordinates(self):
        return list(map(lambda shape: shape.get_coordinates(), self.shapes))

    def export_svg_config(self):
        return list(map(lambda shape: shape.svg_config(), self.shapes))
    
    def change_mode(self, mode):
        if not isinstance(mode, CanvaMode):
            raise TypeError('Mode is not defined')
        
        self.mode = mode

    def mousePressEvent(self, event):
        position = event.pos()

        if self.mode == CanvaMode.EDIT:
            if self.active_shape:
                # check if startpoint of active_shape was clicked
                error = np.sqrt((position.x() - self.active_shape.start_point.x())**2 + (position.y() - self.active_shape.start_point.y())**2)
                threshold = 15

                if error <= threshold:
                    self.canvas = self.previousCanva.copy()
                    self.active_shape.drawShape(self.canvas, self.pen)
                    self.setPixmap(self.canvas)
                    self.active_shape = None
                    self.previousPoint = None
                    self.previousCanva = self.canvas.copy()
                
                else:
                    self._drawPoint(position)
            
            else:
                self._init_drawing(position)
                self._drawPoint(position)

        elif self.mode == CanvaMode.SELECT:
            # check if form was clicked
            # enable delete
            pass

    def _drawPoint(self, position):
        self.previousPoint = position
        self.previousCanva = self.canvas.copy()

        self.active_shape.addPoint(QPoint(position))

        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.drawPolyline(self.active_shape.data_points)
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