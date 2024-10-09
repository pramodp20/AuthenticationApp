import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

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

        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("path/to/your/icon.png"))  # Replace with your icon path

        # Create a context menu for the tray icon
        tray_menu = QMenu()

        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show the tray icon
        self.tray_icon.show()

    def closeEvent(self, event):
        # Override the close event to minimize the application to the tray instead of closing it
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()

    def close_application(self):
        # Hide the window without quitting the application
        self.hide()

    def quit_application(self):
        # Hide the tray icon and quit the application
        self.tray_icon.hide()
        QApplication.quit()

    def on_tray_icon_activated(self, reason):
        # Handle the tray icon click event
        if reason == QSystemTrayIcon.Trigger:
            self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Ensure that the tray icon is correctly initialized each time the application starts
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
