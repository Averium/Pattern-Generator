from widgets import *


class FileDialog(QFileDialog):
    def __init__(self, main_window):
        super().__init__(caption='Dialog')
        self.main_window = main_window

    def export(self, data):
        filename, description = self.getSaveFileName(self.main_window, "Export", EXPORT_FOLDER, EXPORT_EXTENSIONS)
        if filename: cv2.imwrite(filename, data)

    def save(self, image, lines):
        filename, description = self.getSaveFileName(self.main_window, "Save", SAVE_FOLDER, SAVE_EXTENSIONS)
        if filename:
            data = {
                "image": image.tolist(),
                "lines": list(lines),
            }

            with open(filename, 'w') as F:
                json.dump(data, F)

    def open(self):
        filename, description = self.getOpenFileName(self.main_window, "Save", SAVE_FOLDER, SAVE_EXTENSIONS)
        if filename:
            # self.main_window.monitor.canvas.data_image=cv2.imread(filename)
            # self.main_window.monitor.canvas.update()
            # return
            with open(filename, 'r') as F:
                data = json.load(F)
                self.main_window.monitor.canvas.pattern_from_file(data)
            return True
        else:
            return False
