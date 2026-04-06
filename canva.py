from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

import numpy as np
from enum import Enum

from shape import Shape

class CanvaMode(Enum):
    EDIT = 'edit'
    SELECT ='select'

class CanvasLabel(QLabel):
    def __init__(self, canvas_size):
        super().__init__()

        self.setMouseTracking(True)

        self.canvas = QPixmap(canvas_size)
        self.canvas.fill(QColor('white'))
        self.setPixmap(self.canvas)

        self._init_list()
        self._init_drawing()

    def _init_list(self):
        self.current_drawing = []
        self.previousPoint = None
        self.previousCanva = self.canvas
        self.shapes = []
        self.mode = CanvaMode.EDIT

    def _init_drawing(self, start_point):
        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    def export_coordinates(self):
        return list(map(lambda shape: shape.get_coordinates(), self.shapes))

    def export_svg_config(self):
        return list(map(lambda shape: shape.svg_config(), self.shapes))
    
    def change_mode(self, mode):
        canva_mode = CanvaMode(mode)

        if not isinstance(canva_mode, CanvaMode):
            raise TypeError('Mode is not defined')
        
        self.mode = canva_mode

    def mousePressEvent(self, event):
        position = event.pos()

        if self.mode == CanvaMode.EDIT:
            if len(self.current_drawing) > 0:
                # check if startpoint of active_shape was clicked
                start_point = self.current_drawing[0]
                error = np.sqrt((position.x() - start_point.x())**2 + (position.y() - start_point.y())**2)
                threshold = 15

                if error <= threshold:
                    self.canvas = self.previousCanva.copy()

                    new_shape = Shape(self.current_drawing)
                    self._draw_polygon(new_shape)
                    self.shapes.append(new_shape)
                    self.setPixmap(self.canvas)

                    self.current_drawing = []
                    self.previousPoint = None
                    self.previousCanva = self.canvas.copy()
                
                else:
                    self._draw_point(position)
            
            else:
                self._draw_point(position)

        elif self.mode == CanvaMode.SELECT:
            selected_shape = list(filter(lambda s: s.containsPoint(position, Qt.FillRule.OddEvenFill), self.shapes))[-1]
            print(selected_shape)

    def _draw_polygon(self, polygon):
        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.drawPolygon(polygon)
        painter.end()

    def _draw_point(self, position):
        self.previousPoint = position
        self.previousCanva = self.canvas.copy()

        self.current_drawing.append(QPoint(position))

        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.drawPolyline(self.current_drawing)
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