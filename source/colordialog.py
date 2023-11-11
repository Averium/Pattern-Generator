from widgets import*


class ColorDialog(PopupWindow):
    def __init__(self, main_window):
        super().__init__(main_window, 'Színválasztás')
        self.grid = QGridLayout()
        self.setGeometry(200, 200, 250, 350)
        self.tabs = []

    def generate_tabs(self):
        self.tabs = QTabWidget()
        self.pick_tab()

        self.grid.addWidget(self.tabs, 0, 0, 1, 3)
        self.grid.addWidget(Button('Kész', self.close), 1, 2)
        self.setLayout(self.grid)

    def pick_tab(self):
        tab = QWidget()
        grid = QGridLayout()

        for slot in self.main_window.color_slots:
            slot.set.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            grid.addWidget(slot.set, slot.row, slot.col, 1, 1)

        tab.setLayout(grid)
        self.tabs.addTab(tab, 'Színek kiválasztása')

    def on_activate(self, tab=0):
        self.generate_tabs()
        self.tabs.setCurrentWidget(self.tabs.widget(tab))
