from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon
import main_window


def create_tray_icon(app, icon_path):
    tray_icon = QSystemTrayIcon(QIcon(icon_path), parent=app)
    tray_icon.setToolTip("Authentication App")

    menu = QMenu()
    action_show = QAction("Show Accounts", parent=app)
    action_show.triggered.connect(lambda: main_window.show())
    menu.addAction(action_show)
    
    exit_action = QAction("Exit", app)
    exit_action.triggered.connect(QApplication.quit)
    menu.addAction(exit_action)
    
    tray_icon.setContextMenu(menu)

    return tray_icon
