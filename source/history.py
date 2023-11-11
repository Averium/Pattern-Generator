from settings import*


class History:
    def __init__(self, boss):
        self.boss = boss
        self.history = []
        self.pointer = -1
        self.limit = UNDO_LIMIT

    def undo(self):
        if self.pointer > 0:
            self.pointer -= 1
            self.restore()

    def redo(self):
        if self.pointer + 1 < len(self.history):
            self.pointer += 1
            self.restore()

    def store(self):
        if self.pointer + 1 < len(self.history):
            self.history = self.history[0: self.pointer + 1]

        if self.pointer + 1 >= self.limit:
            self.history = self.history[1:]
            self.pointer -= 1

        element = self.store_element()
        self.history.append(element)
        self.pointer += 1

    def restore(self):
        self.restore_element(self.history[self.pointer])

    def store_element(self):
        if self.boss.data_image is not None:
            return self.boss.data_image.copy()

    def restore_element(self, element):
        self.boss.data_image = element.copy()
        self.boss.update()
