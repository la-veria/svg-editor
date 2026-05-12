# SVG Editor

A PyQt6-based vector drawing application for creating and editing polygon shapes with support for transformation and SVG export.

## Features

- **Edit Mode**: Draw polygons point-by-point on a 600×600 canvas
  - Click to place points
  - Live preview line shows the next segment while moving the mouse
  - Close a shape by clicking near its starting point (within ~15 px)
- **Select Mode**: Transform existing shapes
  - Translate (move) shapes by dragging
  - Stretch shapes by dragging corner handles of the bounding box
  - Delete selected shapes with the Delete key
- **SVG Export**: Save all shapes as SVG files with automatic timestamped filenames
- Clean toolbar with mode switching buttons

## Project Structure

- `gui.py`: Application entry point and main window.
- `canva.py`: Canvas widget (`CanvasLabel`) and mouse interaction logic.
- `shape.py`: `Shape` model and final rendering logic.

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **`gui.py`**: Application entry point; creates the main window, menu bar, and toolbar
- **`canva.py`**: Implements the `CanvasLabel` widget that handles all canvas rendering and user interaction (mouse events, shape management, mode switching)
- **`shape.py`**: Defines the `Shape` class (extends `QPolygon`) for storing geometry data and generating SVG configuration
- **`maths.py`**: Provides mathematical utilities for shape transformations:
  - `radius()`: Calculate distance between two points
  - `transform()`: Apply scaling/stretching transformations around a pivot point
  - `translate()`: Move shapes by a translation vector
  - Helper matrix operations for geometric calculations

### Data Flow
1. User mouse events are captured by `CanvasLabel`
2. Depending on the active mode (EDIT or SELECT), the canvas processes the event
3. Shapes are stored in the `shapes` list and rendered to the canvas pixmap
4. On export, shape coordinates and SVG config are extracted and written to an SVG file using `svgwrite`

## Requirements

- Python 3.10+ (tested with Python 3.13)
- `PyQt6`
- `numpy`
- `svgwrite`

## Installation

From the project folder:

```bash
pip install -r requirements.txt
```

## Run

```bash
python gui.py
```

## How to Use

### Edit Mode (Draw Shapes)
1. Click the pen icon in the toolbar to activate Edit mode
2. Click on the canvas to start placing points for a new shape
3. Move the mouse to preview the next line segment
4. Click to add more points to the shape
5. Click near the first point (~15 px) to close and finish the shape
6. Click elsewhere to start a new shape

### Select Mode (Transform Shapes)
1. Click the hand icon in the toolbar to activate Select mode
2. Click on a shape to select it (highlighted in cyan)
3. **Translate**: Click and drag anywhere on the selected shape to move it
4. **Stretch**: Click and drag any corner handle (small squares) of the bounding box to resize the shape
5. Press Delete to remove the selected shape
6. Click outside the shape to deselect

### Export
- Go to File → Export as SVG to save all shapes as an SVG file
- Files are saved with timestamped names (e.g., `ic-1715550000.0.svg`)

## Notes

- Canvas size is 600×600 pixels
- Shapes are rendered with a round-cap pen (width 6) in black
- Selection threshold for closing shapes and selecting handles is ~15 pixels
- SVG export saves all shapes as polygons with black stroke and no fill
- Currently no undo/redo functionality
- The canvas file is named `canva.py` (not `canvas.py`)