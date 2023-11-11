from settings import *


class Tool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.left_color = lambda: self.canvas.colors[0].getRgb()[:-1]
        self.right_color = lambda: self.canvas.colors[1].getRgb()[:-1]

    def on_pick(self):
        if self.canvas:
            self.canvas.selection_mask = numpy.zeros(self.canvas.data_image.shape[:-1], numpy.uint8)

    def on_set(self):
        pass

    def on_press(self, x, y, event):
        pass

    def on_release(self, x, y, event):
        pass

    def on_move(self, x, y, event):
        pass


class Point(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.on_press = self.on_move

    def on_move(self, x, y, event):
        if event.buttons() == Qt.LeftButton:
            self.canvas.data_image[y, x] = self.left_color()
        elif event.buttons() == Qt.RightButton:
            self.canvas.data_image[y, x] = self.right_color()


class All(Tool):
    def on_press(self, x, y, event):
        temp = self.canvas.data_image.copy()
        old_color = temp[y, x]

        if event.buttons() == Qt.LeftButton:
            new_color = self.left_color()
            temp[numpy.where((temp == old_color).all(axis=2))] = new_color
            self.canvas.data_image = temp
        elif event.buttons() == Qt.RightButton:
            new_color = self.right_color()
            temp[numpy.where((temp == old_color).all(axis=2))] = new_color
            self.canvas.data_image = temp


class Line(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start_pos = QPoint(0, 0)
        self.temp = [None, None]

    def on_set(self):
        self.temp = [None, None]

    def on_move(self, x, y, event):
        self.temp[0] = (x, y)
        if event.buttons() == Qt.LeftButton:
            self.temp[1] = (self.start_pos, (x, y), self.left_color())
        if event.buttons() == Qt.RightButton:
            self.del_lines(self.temp[0])

    def on_press(self, x, y, event):
        if event.buttons() == Qt.LeftButton:
            self.start_pos = (x, y)
        if event.buttons() == Qt.RightButton:
            self.del_lines((x, y))

    def on_release(self, x, y, event):
        if self.temp[1] is not None:
            self.canvas.lines.add(self.temp[1])
        self.temp[1] = None
        self.canvas.update()

    def del_lines(self, node):
        to_remove = set()
        for line in self.canvas.lines:
            if node in line[:2]:
                to_remove.add(line)
        self.canvas.lines = self.canvas.lines - to_remove


class Select(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.on_press = self.on_move

    def on_move(self, x, y, event):
        if event.buttons() == Qt.LeftButton:
            self.canvas.selection_mask[y, x] = 1
        elif event.buttons() == Qt.RightButton:
            self.canvas.selection_mask[y, x] = 0


class Move(Tool):
    pass


class Measure(Tool):
    pass


class Toolbox(dict):
    def __init__(self, canvas):
        dict.__init__(self)
        self.canvas = canvas

        self['point'] = Point(canvas)
        self['all'] = All(canvas)
        self['line'] = Line(canvas)
        self['measure'] = Measure(canvas)
        self['select'] = Select(canvas)
        self['move'] = Move(canvas)

        self.key = DEFAULT_TOOL

        self.on_move = None
        self.on_press = None
        self.on_release = None

        self.pick_tool(self.key)

    @property
    def current_tool(self):
        return self[self.key]

    def pick_tool(self, key):
        self[self.key].on_set()
        self.key = key
        self.on_move = self[self.key].on_move
        self.on_press = self[self.key].on_press
        self.on_release = self[self.key].on_release
        self[self.key].on_pick()
        self.canvas.update()

    def copy(self):
        pass

    def cut(self):
        pass

    def paste(self):
        pass

    def merge(self):
        pass
