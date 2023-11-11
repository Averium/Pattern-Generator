from settings import*


class Action:
    def __init__(self, boss, action, name, icon=None, shortcut='', statustip='', checkable=False, group=None, text=True):
        self.menu = QAction(name, boss)
        self.menu.setShortcut(shortcut)
        self.menu.setStatusTip(statustip)
        self.menu.triggered.connect(action)

        if icon is None:
            self.toolbar = None
        else:
            self.toolbar = QToolButton()
            self.toolbar.setCheckable(checkable)
            self.toolbar.setIcon(icon)

            self.toolbar.clicked.connect(action)

            if group is not None:
                pass

            if text:
                self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                self.toolbar.setText(name)
            else:
                self.toolbar.setIconSize(QSize(48, 48))
                self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
                self.toolbar.setToolTip(name)

    def enable(self, enabled):
        self.menu.setEnabled(enabled)
        self.toolbar.setEnabled(enabled)


class Dock(QDockWidget):
    def __init__(self, boss, widget, area):
        super().__init__(boss)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setWidget(widget)
        self.setAllowedAreas(area)
        self.setTitleBarWidget(QWidget())


class Line(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Space(QLabel):
    def __init__(self, height=20):
        super().__init__()
        self.setFixedHeight(height)


class Label(QLabel):
    def __init__(self, text, bold=False):
        super().__init__(text)
        if bold:
            font = FONT
            font.setWeight(QFont.Black)
            self.setFont(font)
        self.setWordWrap(True)


class Button(QPushButton):

    def __init__(self, text, action=lambda: None):
        super().__init__(text)
        self.clicked.connect(action)


class Input(QHBoxLayout):
    def __init__(self, text):
        super().__init__()
        self.line = QLineEdit()
        self.name = text
        self.addWidget(QLabel(text))
        self.addWidget(self.line)

    @property
    def text(self):
        return self.line.text()


class PopupWindow(QWidget):

    def __init__(self, main_window, title, icon=None):
        super().__init__()
        self.main_window = main_window
        self.setGeometry(*DIM['dialog'])
        self.setWindowTitle(title)

        if icon is None:
            icon = main_window.style.standardIcon(QStyle.SP_FileIcon)

        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

    def activate(self, *args, **kwargs):
        self.on_activate(*args, **kwargs)
        self.show()
        self.raise_()
        self.activateWindow()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def on_activate(self, *args, **kwargs):
        pass


class ColorButton(Button):
    def __init__(self, slot, color, pick=True):
        super().__init__('')
        self.slot = slot
        self.color = color
        self.setStyleSheet(f'background-color:{self.slot.color.name()}; border:1px solid #666666')
        self.mousePressEvent = (self.pick, self.set)[pick]

    def pick(self, event):
        if event.buttons() == Qt.LeftButton:
            self.slot.canvas.colors[0] = QColor(self.slot.color)
        if event.buttons() == Qt.RightButton:
            self.slot.canvas.colors[1] = QColor(self.slot.color)

    def set(self, _):
        color = self.slot.canvas.main_window.color_picker.getColor(self.slot.color)
        if color.isValid():
            self.slot.color = color
            self.slot.update_colors()

    def contextMenuEvent(self, event):
        pass


class ColorSlot:
    def __init__(self, canvas, color, row, col):
        self.color = color
        self.canvas = canvas
        self.row, self.col = row, col
        self.pick = ColorButton(self, color)
        self.pick.setFixedWidth(35)
        self.set = ColorButton(self, color, True)

    def update_colors(self):
        self.pick.setStyleSheet(f'background-color:{self.color.name()}; border:1px solid #666666')
        self.set.setStyleSheet(f'background-color:{self.color.name()}; border:1px solid #666666')
