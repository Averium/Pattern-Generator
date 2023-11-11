from PyQt5.QtCore import Qt
from widgets import *
from newpatterndialog import NewPatternDialog
from filedialog import FileDialog
from colordialog import ColorDialog
from monitor import Monitor
from history import History
from toolbox import Toolbox

# Popup windows ----------------------------------------------------------------


class PrintDialog(QPrintDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.printer = QPrinter()

    def activate(self, pixmap):
        if self.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = pixmap.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(pixmap.rect())
            painter.drawPixmap(0, 0, pixmap)


class ErrorMessage(PopupWindow):
    def __init__(self, main_window):
        super().__init__(main_window, 'Hiba')
        self.setWindowIcon(main_window.style.standardIcon(QStyle.SP_MessageBoxCritical))
        self.vbox = QVBoxLayout()

    def on_activate(self, error):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(Label(error))
        self.setLayout(self.vbox)


class ExitWindow(QMessageBox):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle('Kilépés')
        self.setText('Biztos benne?')
        self.addButton(QPushButton('Igen'), QMessageBox.YesRole)
        self.addButton(QPushButton('Nem'), QMessageBox.NoRole)
        self.addButton(QPushButton('Mégse'), QMessageBox.RejectRole)

        self.setWindowIcon(main_window.style.standardIcon(QStyle.SP_DialogCloseButton))

    def ask(self):
        return self.exec_()


# Main window ------------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self, app, dim, title='Main_window'):
        super().__init__()
        self.app = app
        self.style = QApplication.style()
        self.setGeometry(*dim)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(ICONS['window']))

        self.monitor = Monitor(self)
        self.history = History(self.monitor.canvas)
        self.toolbox = Toolbox(self.monitor.canvas)
        self.color_slots = []

        # init gui #

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Kész')
        self.menubar = self.menuBar()

        self.top_toolbar = QToolBar()
        self.side_toolbar = QToolBar()
        self.side_toolbar2 = QToolBar()

        self.file_dialog = FileDialog(self)
        self.print_dialog = PrintDialog(self)
        self.color_dialog = ColorDialog(self)
        self.new_dialog = NewPatternDialog(self)

        self.color_picker = QColorDialog(self)
        self.settings = PopupWindow(self, "Beállítások")
        self.exit_window = ExitWindow(self)
        self.error_message_window = ErrorMessage(self)

        self.left_dock = Dock(self, self.side_toolbar, Qt.LeftDockWidgetArea)
        self.right_dock = Dock(self, self.monitor, Qt.RightDockWidgetArea)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

        self.setCentralWidget(self.right_dock)

        # init gui actions #

        def dummy_action(): pass

        self.new_action = Action(self, self.new_dialog.activate, 'Új vászon', QIcon(ICONS['new']), "Ctrl+N")
        self.open_action = Action(self, self.open, 'Megnyitás', QIcon(ICONS['open']), "Ctrl+O")
        self.save_action = Action(self, self.save, 'Mentés', QIcon(ICONS['save']), "Ctrl+S")
        self.export_action = Action(self, self.export, 'Exportálás', QIcon(ICONS['export']))
        self.print_action = Action(self, self.print, 'Nyomtatás', QIcon(ICONS['print']))
        self.settings_action = Action(self, self.settings.activate, 'Beállítások', QIcon(ICONS['settings']))
        self.exit_action = Action(self, self.closeEvent, 'Kilépés', None)

        self.undo_action = Action(self, self.history.undo, 'Vissza', QIcon(ICONS['undo']), "Ctrl+Z", text=False)
        self.redo_action = Action(self, self.history.redo, 'Előre', QIcon(ICONS['redo']), "Ctrl+Y", text=False)
        self.colorlist_action = Action(self, dummy_action, 'Színlista', QIcon(ICONS['colorlist']), text=False)
        self.resize_action = Action(self, dummy_action, 'Átméretezés')

        self.paint_action = Action(self, lambda: self.toolbox.pick_tool('point'), 'Szem',
                                   QIcon(ICONS['point']), text=False, checkable=True)
        self.all_action = Action(self, lambda: self.toolbox.pick_tool('all'), 'Váltás',
                                 QIcon(ICONS['all']), text=False, checkable=True)
        self.line_action = Action(self, lambda: self.toolbox.pick_tool('line'), 'Vonal',
                                  QIcon(ICONS['line']), text=False, checkable=True)
        self.measure_action = Action(self, lambda: self.toolbox.pick_tool(
            'measure'), 'Mérés', QIcon(ICONS['measure']), text=False, checkable=True)
        self.select_action = Action(self, lambda: self.toolbox.pick_tool(
            'select'), 'Kijelölés', QIcon(ICONS['select']), text=False, checkable=True)
        self.move_action = Action(self, lambda: self.toolbox.pick_tool('move'), 'Mozgatás',
                                  QIcon(ICONS['move']), text=False, checkable=True)
        self.copy_action = Action(self, self.toolbox.copy, 'Másolás', QIcon(ICONS['copy']), "Ctrl+C", text=False)
        self.cut_action = Action(self, self.toolbox.cut, 'Kivágás', QIcon(ICONS['cut']), "Ctrl+X", text=False)
        self.paste_action = Action(self, self.toolbox.paste, 'Beillesztés', QIcon(ICONS['paste']), "Ctrl+V", text=False)
        self.merge_action = Action(self, self.toolbox.merge, 'Hozzáadás', QIcon(ICONS['merge']), text=False)

        self.color_action = Action(self, self.color_dialog.activate, 'Színek', QIcon(ICONS['colors']), text=False)
        self.color_action.toolbar.setIconSize(QSize(48 * 2 + 12, 48))

        self.enable_actions(
            self.colorlist_action,
            self.measure_action,
            self.select_action,
            self.move_action,
            self.copy_action,
            self.cut_action,
            self.paste_action,
            self.merge_action,
        )

        # init menu #

        self.enable_actions(self.save_action, self.export_action, self.print_action, enabled=False)

        self.file_menu = self.menubar.addMenu('File')
        self.tools_menu = self.menubar.addMenu('Eszközök')
        self.view_menu = self.menubar.addMenu('Nézet')
        self.settings_menu = self.menubar.addAction(self.settings_action.menu)

        self.file_menu.addAction(self.new_action.menu)
        self.file_menu.addAction(self.open_action.menu)
        self.file_menu.addAction(self.save_action.menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.export_action.menu)
        self.file_menu.addAction(self.print_action.menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action.menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action.menu)

        self.tools_menu.addAction(self.undo_action.menu)
        self.tools_menu.addAction(self.redo_action.menu)
        self.tools_menu.addSeparator()
        self.tools_menu.addAction(self.colorlist_action.menu)
        self.tools_menu.addSeparator()

        # init toolbars #

        self.addToolBar(Qt.TopToolBarArea, self.top_toolbar)
        self.addToolBar(Qt.LeftToolBarArea, self.side_toolbar)
        self.top_toolbar.setIconSize(QSize(32, 32))
        self.side_toolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.top_toolbar.addWidget(self.new_action.toolbar)
        self.top_toolbar.addSeparator()
        self.top_toolbar.addWidget(self.open_action.toolbar)
        self.top_toolbar.addWidget(self.save_action.toolbar)
        self.top_toolbar.addWidget(self.export_action.toolbar)
        self.top_toolbar.addSeparator()
        self.top_toolbar.addWidget(self.print_action.toolbar)
        self.top_toolbar.addSeparator()
        self.top_toolbar.addWidget(self.settings_action.toolbar)

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.paint_action.toolbar, 0, 0, 1, 1)
        grid.addWidget(self.line_action.toolbar, 0, 1, 1, 1)
        grid.addWidget(self.all_action.toolbar, 1, 0, 1, 1)
        grid.addWidget(self.measure_action.toolbar, 1, 1, 1, 1)
        grid.addWidget(self.select_action.toolbar, 2, 0, 1, 1)
        grid.addWidget(self.move_action.toolbar, 2, 1, 1, 1)
        grid.addWidget(Space(), 3, 0, 1, 2)
        grid.addWidget(self.cut_action.toolbar, 4, 0, 1, 1)
        grid.addWidget(self.copy_action.toolbar, 4, 1, 1, 1)
        grid.addWidget(self.paste_action.toolbar, 5, 0, 1, 1)
        grid.addWidget(self.merge_action.toolbar, 5, 1, 1, 1)

        grid.addWidget(self.undo_action.toolbar, 6, 0, 1, 1)
        grid.addWidget(self.redo_action.toolbar, 6, 1, 1, 1)
        grid.addWidget(Space(), 7, 0, 1, 2)
        grid.addWidget(self.color_action.toolbar, 8, 0, 1, 2)
        grid.addWidget(Space(), 9, 0, 1, 2)

        colorgrid = QGridLayout()
        for row in range(6):
            for col in range(3):
                slot = ColorSlot(self.monitor.canvas, QColor(*DEFAULT_COLORS[row][col]), row, col)
                self.color_slots.append(slot)
                colorgrid.addWidget(slot.pick, row, col, 1, 1)

        grid.addLayout(colorgrid, 10, 0, 1, 2)

        temp = QWidget()
        temp.setLayout(grid)
        self.side_toolbar.addWidget(temp)

        mode = QButtonGroup(self)
        mode.setExclusive(True)
        mode.addButton(self.paint_action.toolbar)
        mode.addButton(self.all_action.toolbar)
        mode.addButton(self.line_action.toolbar)
        mode.addButton(self.measure_action.toolbar)
        mode.addButton(self.select_action.toolbar)
        mode.addButton(self.move_action.toolbar)

        self.showMaximized()

    @staticmethod
    def enable_actions(*actions, enabled=True):
        for action in actions:
            action.enable(enabled)

    def open(self):
        if self.file_dialog.open():
            self.enable_actions(self.save_action, self.export_action, self.print_action)

    def save(self):
        self.file_dialog.save(self.monitor.canvas.data_image, self.monitor.canvas.lines)

    def export(self):
        self.file_dialog.export(self.monitor.canvas.rgb_image)

    def print(self):
        self.print_dialog.activate(self.monitor.canvas.image_to_pixmap(self.monitor.canvas.rgb_image))

    def debug(self, *args):
        self.setWindowTitle(":".join([str(arg) for arg in args]))

    def closeEvent(self, event):
        try:
            event.ignore()
        except Exception as ERROR:
            print(ERROR)
        finally:
            if not self.exit_window.ask():
                self.app.quit()

    def raise_error(self, error):
        self.error_message_window.activate(error)
