from widgets import *


class Canvas:

    def __init__(self, monitor):
        self.monitor = monitor
        self.main_window = monitor.main_window

        self.data_image = None
        self.pattern_image = None
        self.selection_mask = None
        self.lines = set()

        self.colors = [QColor(0, 0, 0), QColor(255, 255, 255)]

    def new_pattern(self, row, col):
        self.data_image = numpy.ones((col, row, 3), numpy.uint8) * 255
        self.selection_mask = numpy.zeros((col, row), numpy.uint8)
        self.lines = set()
        self.main_window.enable_actions(self.main_window.save_action, self.main_window.export_action,
                                        self.main_window.print_action)
        self.main_window.history.store()
        self.update()

    def pattern_from_file(self, data):
        self.data_image = numpy.array(data['image'], numpy.uint8)
        self.selection_mask = numpy.zeros(self.data_image.shape[:-1], numpy.uint8)
        self.lines = set()
        for line in data['lines']:
            new = tuple([tuple(element) for element in line])
            self.lines.add(new)
        self.main_window.history.store()
        self.update()

    def line(self, start, end, color, width, div):
        x1, y1 = start
        x2, y2 = end
        sx, sy = int(self.monitor.scroll_value.x() / div), int(self.monitor.scroll_value.y() / div)
        start = (int((x1 - sx) * div), int((y1 - sy) * div))
        end = (int((x2 - sx) * div), int((y2 - sy) * div))
        cv2.line(self.pattern_image, start, end, color, width, cv2.LINE_AA)

    def render_image(self, x, y, w, h, div):
        last_row = int(min(h + y, self.data_image.shape[0]))
        last_col = int(min(w + x, self.data_image.shape[1]))
        visible_image = self.data_image[int(y): last_row, int(x): last_col]
        self.pattern_image = cv2.resize(visible_image, None, fx=div, fy=div, interpolation=cv2.INTER_NEAREST)
        h, w, ch = self.pattern_image.shape
        return w, h

    def render_lines(self, _x, _y, _w, _h, div):
        if self.main_window.toolbox.key == 'line':
            if self.temp[1] is not None:
                self.line(*self.temp[1], int(div / 8), div)
        for line in self.lines:
            self.line(*line, int(div / 10), div)

    def render_dots(self, _x, _y, w, h, div):
        for col in range(int(w / div) + 1):
            for row in range(int(h / div) + 1):
                center = (int(col * div), int(row * div))
                cv2.circle(self.pattern_image, center, int(div / 8), COLORS['cornermark'], -1, cv2.LINE_AA)
        if self.temp[0] is not None:
            x, y = self.temp[0]
            sx, sy = int(self.monitor.scroll_value.x() / div), int(self.monitor.scroll_value.y() / div)
            cv2.circle(self.pattern_image, (int((x - sx) * div), int((y - sy) * div)), int(div / 5),
                       COLORS['cornerselect'], -1, cv2.LINE_AA)

    def render_grid(self, x, y, w, h, div):
        for col in range(int(w / div) + 1):
            start, end = (int(col * div), 0), (int(col * div), h)
            cv2.line(self.pattern_image, start, end, COLORS['grid'], (2, 1)[bool((col + x) % 10)])
        for row in range(int(h / div) + 1):
            start, end = (0, int(row * div)), (w, int(row * div))
            cv2.line(self.pattern_image, start, end, COLORS['grid'], (2, 1)[bool((row + y) % 10)])

    def render_selection(self, _x, _y, _w, _h, _div):
        if self.selection_mask is not None:
            pass

    def update(self):
        if self.data_image is not None:
            x, y, w, h = self.monitor.visible_rect()
            div = self.monitor.scale
            w, h = self.render_image(x, y, w, h, div)
            if self.main_window.toolbox.key == 'line':
                self.render_dots(x, y, w, h, div)
            else:
                self.render_grid(x, y, w, h, div)
            self.render_lines(x, y, w, h, div)
            self.render_selection(x, y, w, h, div)

            self.monitor.setPixmap(self.image_to_pixmap(self.pattern_image))

    def __bool__(self):
        return self.data_image is not None

    @property
    def temp(self):
        return self.main_window.toolbox.current_tool.temp

    @property
    def rgb_image(self):
        return cv2.cvtColor(self.pattern_image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def image_to_pixmap(image):
        h, w, ch = image.shape
        return QPixmap(QImage(image, w, h, w * 3, QImage.Format_RGB888))
