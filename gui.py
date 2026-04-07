import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QToolBar
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon

import svgwrite
import datetime as dt
from pathlib import Path

from canva import CanvasLabel

app = QApplication(sys.argv)
canvas_size = QSize(800, 800)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Illustrator Clone')
        self.setFixedSize(canvas_size)
        self._init_canvas()
        self._create_actions()
        self._create_menubar()
        self._create_toolbar()

        self.show()

    def _init_canvas(self):
        self.label = CanvasLabel(canvas_size)
        self.setCentralWidget(self.label)
        self.mode = 'edit'

    def _create_menubar(self):

        menuBar = QMenuBar(self)
        menuBar = self.menuBar()
        
        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.exportAction)

        menuBar.addMenu(fileMenu)

    def _create_actions(self):
        self.exportAction = QAction(self)
        self.exportAction.setText('&Export as SVG')
        self.exportAction.triggered.connect(self.export_svg)
        
        self.editMode = QAction(self)
        self.editMode.setIcon(QIcon('./icons/pen.svg'))
        self.editMode.triggered.connect(lambda: self.label.change_mode('edit'))
        
        self.selectMode = QAction(self)
        self.selectMode.setIcon(QIcon('./icons/hand.svg'))
        self.selectMode.triggered.connect(lambda: self.label.change_mode('select'))

    def _create_toolbar(self):
        toolbar = QToolBar(self)

        toolbar.addAction(self.editMode)
        toolbar.addAction(self.selectMode)

        self.addToolBar(toolbar)

    def export_svg(self):
        shapes = self.label.export_svg_config()

        timestamp = dt.datetime.now().timestamp()
        filename = f"ic-{timestamp}.svg"

        svg_document = svgwrite.Drawing(
            filename = filename,
            size=(canvas_size.width(), canvas_size.height()),
        )

        for config in shapes:
            svg_document.add(
                svg_document.polygon(**config)
            )

        svg_document.save()
        saved_path = Path(filename).resolve()
        print(f'svg file saved in {saved_path}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.label.delete_event()

    def closeEvent(self, a0):
        return super().closeEvent(a0)

w = Window()

sys.exit(app.exec())