from settings import*
from canvas import Canvas


class Monitor(QLabel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMouseTracking(True)

        self.canvas = Canvas(self)

        self.scale = 30
        self.scroll_value = QPoint(0, 0)
        self.scroll_temp = None

    def visible_rect(self):
        return (int(self.scroll_value.x() / self.scale),
                int(self.scroll_value.y() / self.scale),
                int(self.width() / self.scale),
                int(self.height() / self.scale))

    def scroll(self, dpos):
        self.scroll_value = self.scroll_value + dpos
        max_height = self.canvas.data_image.shape[0] * self.scale - self.canvas.pattern_image.shape[0]
        max_width = self.canvas.data_image.shape[1] * self.scale - self.canvas.pattern_image.shape[1]
        self.scroll_value.setX(min(max(0, self.scroll_value.x()), max_width))
        self.scroll_value.setY(min(max(0, self.scroll_value.y()), max_height))

    def wheelEvent(self, event=None):
        if self.canvas:
            value = 1 + event.angleDelta().y() / WHEEL_CONSTANT
            if SCALE_LIMIT[0] <= self.scale * value <= SCALE_LIMIT[1]:
                self.scale *= value
                # scroll here
            self.canvas.update()

    def mouseMoveEvent(self, event):
        if self.canvas:
            # scroll -----------------------------------------------------------
            if event.buttons() == Qt.MiddleButton:
                if self.scroll_temp:
                    dpos = self.scroll_temp - event.pos()
                    self.scroll(dpos)
                self.scroll_temp = event.pos()

            # tool -------------------------------------------------------------
            x, y, valid = self.transform(event, self.main_window.toolbox.key == 'line')
            if valid:
                self.main_window.toolbox.on_move(x, y, event)
            self.canvas.update()

    def mousePressEvent(self, event):
        if self.canvas:
            self.scroll_temp = event.pos()
            x, y, valid = self.transform(event, self.main_window.toolbox.key == 'line')
            if valid:
                self.main_window.toolbox.on_press(x, y, event)
            self.canvas.update()

    def mouseReleaseEvent(self, event):
        if self.canvas:
            self.main_window.history.store()
            self.scroll_temp = None
            if self.canvas.data_image is not None:
                x, y, valid = self.transform(event, self.main_window.toolbox.key == 'line')
                if valid:
                    self.main_window.toolbox.on_release(x, y, event)

    def transform(self, event, center=False):
        x = (event.x() + self.scroll_value.x()) / self.scale + center / 2
        y = (event.y() + self.scroll_value.y()) / self.scale + center / 2
        h, w, ch = self.canvas.data_image.shape
        return int(x), int(y), (x < w and y < h)
