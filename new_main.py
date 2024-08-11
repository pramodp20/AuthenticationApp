import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image, ImageDraw
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('System Tray Example')
        self.setGeometry(100, 100, 400, 300)
        
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)
        
    def close_application(self):
        self.close()

def create_image():
    # Create an image for the system tray icon
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def on_quit(icon, item):
    icon.stop()
    sys.exit()

def setup_tray_icon():
    image = create_image()
    menu = Menu(
        Item('Quit', on_quit)
    )
    icon = Icon("test_icon", image, "System Tray", menu)
    icon.run()

def start_tray_icon():
    threading.Thread(target=setup_tray_icon, daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Start system tray icon
    start_tray_icon()

    window.show()
    sys.exit(app.exec_())
