from widgets import*

# Dropdowns --------------------------------------------------------------------


class Dropdown(QComboBox):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.generate_content()

    def generate_content(self):
        pass


class UnitDropdown(Dropdown):
    def generate_content(self):
        self.clear()
        for unit in UNIT:
            self.addItem(unit)


class FabricDropdown(Dropdown):
    def generate_content(self):
        self.clear()
        for fabric in FABRIC_DATA:
            self.addItem(fabric)


class HpiDropdown(Dropdown):
    def generate_content(self):
        self.clear()
        unit = self.window.unit_dropdown.currentText()
        fabric = self.window.fabric_dropdown.currentText()
        if unit and fabric:
            for i in range(*FABRIC_DATA[fabric]):
                self.addItem(f"{self.window.round(i / UNIT[unit])} [Öltés/{unit}]")


# Spin boxes -------------------------------------------------------------------

class SpinBox(QSpinBox):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setMaximum(999)

    def generate_value(self):
        pass

    def update(self):
        self.blockSignals(True)
        self.generate_value()
        self.blockSignals(False)


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setMaximum(999)

    def generate_value(self):
        pass

    def update(self):
        self.blockSignals(True)
        self.generate_value()
        self.blockSignals(False)


class HorizontalSize(DoubleSpinBox):
    def generate_value(self):
        given = self.window.hdotsize.value()
        try:
            self.setValue(float(given / self.window.shift_number))
        except Exception as ERROR:
            print(ERROR)


class VerticalSize(DoubleSpinBox):
    def generate_value(self):
        given = self.window.vdotsize.value()
        try:
            self.setValue(float(given / self.window.shift_number))
        except Exception as ERROR:
            print(ERROR)


class HorizontalSquareSize(SpinBox):
    def generate_value(self):
        given = self.window.hsize.value()
        self.setValue(float(given * self.window.shift_number))


class VerticalSquareSize(SpinBox):
    def generate_value(self):
        given = self.window.vsize.value()
        self.setValue(float(given * self.window.shift_number))


# Main window ------------------------------------------------------------------

class NewPatternDialog(PopupWindow):
    def __init__(self, main_window):
        super().__init__(main_window, 'Új vászon')

        self.grid = QGridLayout()

        self.group_1 = QGroupBox()
        self.group_2 = QGroupBox()

        self.unit_dropdown = UnitDropdown(self)
        self.fabric_dropdown = FabricDropdown(self)
        self.HPI_dropdown = HpiDropdown(self)

        self.unit_dropdown.currentIndexChanged.connect(self.update)
        self.fabric_dropdown.currentIndexChanged.connect(self.update)

        self.hsize = HorizontalSize(self)
        self.vsize = VerticalSize(self)
        self.hdotsize = HorizontalSquareSize(self)
        self.vdotsize = VerticalSquareSize(self)

        self.hsize.valueChanged.connect(self.hdotsize.update)
        self.vsize.valueChanged.connect(self.vdotsize.update)
        self.hdotsize.valueChanged.connect(self.hsize.update)
        self.vdotsize.valueChanged.connect(self.vsize.update)

        self.HPI_dropdown.currentIndexChanged.connect(self.hsize.update)
        self.HPI_dropdown.currentIndexChanged.connect(self.vsize.update)

        self.labels = {
            'unit': Label("Mértékegység"),
            'fabric': Label("Vászon típus"),
            'hpi': Label("Sűrűség"),
            'hsize': Label("Vízszintesen"),
            'vsize': Label("Függőlegesen"),
            'size': Label(f"Vászon méret [{self.unit_dropdown.currentText()}]"),
            'dotsize': Label(f"Szemek száma [db]")
        }

        self.update()

        self.grid_1 = QGridLayout()
        self.grid_2 = QGridLayout()
        self.grid_1.setSpacing(20)
        self.grid_2.setSpacing(20)

        self.grid_1.addWidget(self.labels['unit'], 0, 0, 1, 1)
        self.grid_1.addWidget(self.unit_dropdown, 0, 1, 1, 1)
        self.grid_1.addWidget(self.labels['fabric'], 1, 0, 1, 1)
        self.grid_1.addWidget(self.fabric_dropdown, 1, 1, 1, 1)
        self.grid_1.addWidget(self.labels['hpi'], 2, 0, 1, 1)
        self.grid_1.addWidget(self.HPI_dropdown, 2, 1, 1, 1)

        self.grid_2.addWidget(self.labels['size'], 2, 1, 1, 1)
        self.grid_2.addWidget(self.labels['dotsize'], 2, 2, 1, 1)
        self.grid_2.addWidget(self.labels['hsize'], 3, 0, 1, 1)
        self.grid_2.addWidget(self.hsize, 3, 1, 1, 1)
        self.grid_2.addWidget(self.hdotsize, 3, 2, 1, 1)
        self.grid_2.addWidget(self.labels['vsize'], 4, 0, 1, 1)
        self.grid_2.addWidget(self.vsize, 4, 1, 1, 1)
        self.grid_2.addWidget(self.vdotsize, 4, 2, 1, 1)

        self.group_1.setLayout(self.grid_1)
        self.group_2.setLayout(self.grid_2)

        self.grid.addWidget(self.group_1, 0, 0, 1, 3)
        self.grid.addWidget(self.group_2, 1, 0, 1, 3)

        def close():
            self.main_window.monitor.canvas.new_pattern(self.hdotsize.value(), self.vdotsize.value())
            self.close()

        self.close_button = Button('Generálás', close)
        self.grid.addWidget(self.close_button, 3, 2, 1, 1)
        self.setLayout(self.grid)

    def update(self):
        self.HPI_dropdown.generate_content()
        self.labels['size'].setText(f"Vászon méret [{self.unit_dropdown.currentText()}]")
        self.hsize.update()
        self.vsize.update()

    def on_activate(self, size):
        self.hdotsize.setValue(DEFAULT_CANVAS_SIZE[0])
        self.vdotsize.setValue(DEFAULT_CANVAS_SIZE[1])
        self.hsize.update()
        self.vsize.update()

    @property
    def shift_number(self):
        return float(self.HPI_dropdown.currentText().split(' ')[0])

    @staticmethod
    def round(value):
        return '{:g}'.format(round(value, 2))
