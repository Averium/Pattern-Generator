import os
import sys
import json
import numpy
import cv2
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QRect, QLineF, QPoint
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QFont, QPalette, QPainter, QIcon, QFont, QPixmap, QImage, QColor

from configparser import ConfigParser

# resolution fix ---------------------------------------------------------------
from ctypes import windll

windll.user32.SetProcessDPIAware()
WIDTH, HEIGHT = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
# ------------------------------------------------------------------------------

CONFIG = ConfigParser()
CONFIG.read('colors.ini')

FONT_NAME = "Courier new"
FONT_SIZE = 10

FONT = QFont(FONT_NAME)
FONT.setStyleHint(QFont.Monospace)
FONT.setPointSize(FONT_SIZE)

SOURCE_FOLDER = os.getcwd()
PATH = os.path.split(SOURCE_FOLDER)[0]
DATA_FOLDER = os.path.join(PATH, "data")
print(DATA_FOLDER)
SAVE_FOLDER = os.path.join(PATH, "patterns")
EXPORT_FOLDER = os.path.join(PATH, "exported")
ICON_FOLDER = os.path.join(DATA_FOLDER, "icons")

COLOR_FILE = os.path.join(DATA_FOLDER, 'colors.json')

EXPORT_EXTENSIONS = "PNG Image (*.png);;JPEG Image (*.jpg)"  # PDF Document (*.pdf);;
SAVE_EXTENSIONS = "Keresztszemes minta (*.csp)"

UNDO_LIMIT = 16
SCALE_LIMIT = (5, 40)
WHEEL_CONSTANT = 2400
DEFAULT_TOOL = 'point'
DEFAULT_CANVAS_SIZE = (80, 80)

DIM = {'dialog': (200, 200, 350, 230),
       'canvas': (220, 60, WIDTH - 230, HEIGHT - 70),
       'window': (50, 50, 1000, 700),
       '': (),
       }

COLORS = {'grid': (100, 100, 100),
          'cornermark': (80, 80, 80),
          'cornerselect': (250, 100, 0),
          'selection': (250, 120, 0),
          '': (),
          }

DEFAULT_COLORS = (
    ((255, 255, 255), (150, 150, 150), (0, 0, 0)),
    ((255, 0, 0), (0, 255, 0), (0, 0, 255)),
    ((255, 255, 0), (255, 0, 255), (0, 255, 255)),
    ((255, 127, 0), (255, 0, 127), (127, 255, 0)),
    ((255, 127, 127), (127, 255, 127), (127, 127, 255)),
    ((0, 255, 127), (127, 0, 255), (0, 127, 255)),
)

FABRIC_DATA = {'Aida': (11, 23),
               'Hardanger': (22, 23),
               'Lenvászon': (25, 37),
               'Hímzővászon': (18, 33),
               }

UNIT = {'cm': 2.54,
        'inch': 1}

ICONS = {'window': (os.path.join(ICON_FOLDER, 'cross_stich.png')),
         'open': (os.path.join(ICON_FOLDER, '138-folder-20.png')),
         'save': (os.path.join(ICON_FOLDER, '013-folder-39.png')),
         'export': (os.path.join(ICON_FOLDER, '084-folder-32.png')),
         'print': (os.path.join(ICON_FOLDER, '221-printer.png')),
         'new': (os.path.join(ICON_FOLDER, '200-clipboard.png')),
         'settings': (os.path.join(ICON_FOLDER, 'support.png')),
         'undo': (os.path.join(ICON_FOLDER, 'undo.png')),
         'redo': (os.path.join(ICON_FOLDER, 'redo.png')),
         'colorlist': (os.path.join(ICON_FOLDER, '208-file-3.png')),
         'point': (os.path.join(ICON_FOLDER, '003-pencil.png')),
         'line': (os.path.join(ICON_FOLDER, '027-sewing-1.png')),
         'all': (os.path.join(ICON_FOLDER, '001-paint-brush.png')),
         'measure': (os.path.join(ICON_FOLDER, 'measuring-tape.png')),
         'select': (os.path.join(ICON_FOLDER, '017-embroidery-1.png')),
         'move': (os.path.join(ICON_FOLDER, 'move.png')),
         'copy': (os.path.join(ICON_FOLDER, '010-cross-stitch.png')),
         'cut': (os.path.join(ICON_FOLDER, '028-scissors.png')),
         'paste': (os.path.join(ICON_FOLDER, '011-patch.png')),
         'merge': (os.path.join(ICON_FOLDER, '022-sewing.png')),
         'colors': (os.path.join(ICON_FOLDER, 'bobbin2.png')),
         'net': (os.path.join(ICON_FOLDER, '012-embroidery2.png')),
         }
