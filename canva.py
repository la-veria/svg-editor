from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint
from enum import Enum

from shape import Shape

from maths import radius, transform, translate

class CanvaMode(Enum):
    EDIT = 'edit'
    SELECT ='select'

class TransformationTypes(Enum):
    TRANSLATE = 'translate'
    STRETCH = 'stretch'

class CanvasLabel(QLabel):
    # region init
    def __init__(self, canvas_size):
        super().__init__()

        self.setMouseTracking(True)

        self.canvas_size = canvas_size

        self._init_canva()
        self._init_list()
        self._init_transformation()
        self._init_drawing()

    def _init_canva(self):
        self.canvas = QPixmap(self.canvas_size)
        self.canvas.fill(QColor('white'))
        self.setPixmap(self.canvas)

    def _init_list(self):
        self.current_drawing = []
        self.previousPoint = None
        self.previousCanva = self.canvas
        self.shapes = []
        self.mode = CanvaMode.EDIT
        self.threshold = 15

    def _init_drawing(self):
        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.highlight_pen = QPen()
        self.highlight_pen.setWidth(2)
        self.highlight_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.highlight_pen.setColor(QColor('cyan'))

    def _init_transformation(self):
        self.selected_shape = None
        self.transition_start = None
        self.transition_origin = None
        self.translated_shape = None
        self.current_action = None

    # endregion init

    # region svg

    def export_coordinates(self):
        return list(map(lambda shape: shape.get_coordinates(), self.shapes))

    def export_svg_config(self):
        return list(map(lambda shape: shape.svg_config(), self.shapes))
    
    # endregion svg
    
    # region draw

    def change_mode(self, mode):
        canva_mode = CanvaMode(mode)

        if not isinstance(canva_mode, CanvaMode):
            raise TypeError('Mode is not defined')
        
        self.mode = canva_mode

        # reset selection
        self._init_transformation()
        self._draw_shapes()

        if self.mode == CanvaMode.EDIT:
            self.setMouseTracking(True)
        else: 
            self.setMouseTracking(False)

    def _draw_polygon(self, polygon, pen = None):
        if not pen:
            pen = self.pen
        
        painter = QPainter(self.canvas)
        painter.setPen(pen)
        painter.drawPolygon(polygon)
        painter.end()

        self.setPixmap(self.canvas)

    def _draw_point(self, position):
        self.previousPoint = position
        self.previousCanva = self.canvas.copy()

        self.current_drawing.append(QPoint(position))

        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.drawPolyline(self.current_drawing)
        painter.end()
        
        self.setPixmap(self.canvas)

    def _draw_shapes(self):
        for shape in self.shapes:
            self._draw_polygon(shape)

    # endregion draw

    def _transform_shape(self, endpoint):
        startpoint = self.transition_start

        if startpoint == endpoint: return

        transformed_shape = transform(self.translation_original, self.transition_origin, startpoint, endpoint)

        self.shapes[self.shapes.index(self.selected_shape)] = transformed_shape
        self.selected_shape = transformed_shape

        self._init_canva()
        self._draw_shapes()


    def _translate_shape(self, endpoint):
        startpoint = self.transition_start

        if startpoint == endpoint: return
    
        self.translated_shape = translate(self.translation_original, startpoint, endpoint)

        self.shapes[self.shapes.index(self.selected_shape)] = self.translated_shape
        self.selected_shape = self.translated_shape

        self._init_canva()
        self._draw_shapes()

    # region events

    def mousePressEvent(self, event):
        position = event.pos()

        if self.mode == CanvaMode.EDIT:
            if len(self.current_drawing) > 0:
                # check if startpoint of active_shape was clicked
                error = radius(self.current_drawing[0], position)

                if error <= self.threshold:
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
            selected_shape = next(iter([s for s in self.shapes if s.containsPoint(position, Qt.FillRule.OddEvenFill)]), None)

            if self.selected_shape:
                # check if a selected shape allready exists

                corners = self.selected_shape.data_points
                selected_corner = next(iter([c for c in corners if radius(c, position) <= self.threshold]), None)

                if selected_corner:
                    # check if click is on corner of selected shape => stretch

                    self.current_action = TransformationTypes.STRETCH
                    self.transition_start = selected_corner
                    self.transition_origin = self.translation_original.boundingRect().center()

                    painter = QPainter(self.canvas)
                    painter.setPen(self.pen)
                    painter.drawPoint(self.transition_origin)
                    painter.end()

                    self.setPixmap(self.canvas)

                    print('stretch start')
                    return
            
                elif self.selected_shape == selected_shape:
                    # check if click is within selected shape => translate

                    self.current_action = TransformationTypes.TRANSLATE
                    self.transition_start = position
                    print('translation start')
                    return

                else:
                    # check if click is outside the selected shape => deactivate transformation

                    self.selected_shape = None
                    self._init_transformation()
                    self._draw_shapes()


            if selected_shape:
                # check if a new shape is selected => activate shape

                self.selected_shape = selected_shape
                self._draw_polygon(self.selected_shape, self.highlight_pen)
                self.translation_original = self.selected_shape
    
    def mouseMoveEvent(self, event):
        position = event.pos()

        if self.mode == CanvaMode.EDIT:
            if not(self.previousPoint): return

            self.canvas = self.previousCanva.copy()

            self.setPixmap(self.canvas)

            painter = QPainter(self.canvas)
            painter.setPen(self.pen)
            painter.drawLine(self.previousPoint, position)
            painter.end()
            
            self.setPixmap(self.canvas)

        elif self.mode == CanvaMode.SELECT:
            if self.current_action == TransformationTypes.TRANSLATE:
                self._translate_shape(position)

            elif self.current_action == TransformationTypes.STRETCH:
                self._transform_shape(position)


    def mouseReleaseEvent(self, event):
        if self.current_action:
            # reset transformed shape to original

            self.translation_original = self.selected_shape
            self._draw_polygon(self.selected_shape, self.highlight_pen)

    def delete_event(self):
        if self.selected_shape:
            self.shapes.remove(self.selected_shape)
            self.selected_shape = None
            self._init_canva()
            self._draw_shapes()

    # endregion events