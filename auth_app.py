import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from main_window import MainWindow
from tray_icon import create_tray_icon

def main():
    app = QApplication(sys.argv)

    # Determine the path to the icon file
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
        icon_path = 'icon.ico'

    tray_icon = create_tray_icon(app, icon_path)
    tray_icon.show()

    main_window = MainWindow(icon_path)
    main_window.hide()

    tray_icon.activated.connect(lambda reason: on_tray_icon_click(reason, main_window))

    sys.exit(app.exec_())

def on_tray_icon_click(reason, main_window):
    if reason == QSystemTrayIcon.Trigger:
        main_window.show()

def exit_application():
    QApplication.quit()

if __name__ == "__main__":
    main()
