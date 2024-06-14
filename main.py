import pyotp
import json
import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime

data = None
current_message_box = None

def get_json():
    global data
    # Determine the path to the key.json file
    if hasattr(sys, '_MEIPASS'):
        file_path = os.path.join(sys._MEIPASS, 'key.json')
    else:
        file_path = 'key.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

def get_accounts():
    return get_json()

def get_code(secret_key):
    topt = pyotp.TOTP(secret_key, interval=30)
    code = topt.now()
    return code

class MainWindow(QMainWindow):
    def __init__(self, icon_path):
        super().__init__()
        self.setWindowTitle("Accounts")
        self.setGeometry(300, 300, 300, 200)
        self.setWindowIcon(QIcon(icon_path))
        self.initUI()
    
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.accounts = get_accounts()
        
        for account in self.accounts:
            if isinstance(account, dict):
                button = QPushButton(account['account_name'])
                button.clicked.connect(lambda _, a=account: self.show_totp_screen(a))
                self.layout.addWidget(button)

    def show_totp_screen(self, account):
        self.totp_screen = TOTPWindow(account, self.windowIcon())
        self.totp_screen.show()
        self.hide()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()

class TOTPWindow(QMainWindow):
    def __init__(self, account, icon):
        super().__init__()
        self.account = account
        self.setWindowTitle(account['account_name'])
        self.setGeometry(300, 300, 300, 200)
        self.setWindowIcon(icon)
        self.initUI()
        self.update_totp()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.label_totp = QLabel("")
        self.layout.addWidget(self.label_totp)

        self.label_timer = QLabel("")
        self.layout.addWidget(self.label_timer)
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_to_main)
        self.layout.addWidget(self.back_button)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_totp)
        self.timer.start(1000)
    
    def update_totp(self):
        code = get_code(self.account['secret_key'])
        self.label_totp.setText(f"TOTP: {code}")

        current_time = QTime.currentTime()
        seconds_left = 30 - (current_time.second() % 30)
        self.label_timer.setText(f"Expires in: {seconds_left}s")
        
    def back_to_main(self):
        self.timer.stop()
        self.main_window = MainWindow(self.windowIcon())
        self.main_window.show()
        self.close()

def main():
    global main_window
    app = QApplication(sys.argv)

    # Determine the path to the icon file
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
        icon_path = 'icon.ico'

    tray_icon = QSystemTrayIcon(QIcon(icon_path), parent=app)
    tray_icon.setToolTip("Authentication App")

    menu = QMenu()
    action_show = QAction("Show Accounts", parent=app)
    action_show.triggered.connect(show_main_window)
    menu.addAction(action_show)
    
    exit_action = QAction("Exit", app)
    exit_action.triggered.connect(exit_application)
    menu.addAction(exit_action)
    
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    tray_icon.activated.connect(on_tray_icon_click)

    main_window = MainWindow(icon_path)
    main_window.hide()

    sys.exit(app.exec_())

def show_main_window():
    global main_window
    main_window.show()

def on_tray_icon_click(reason):
    if reason == QSystemTrayIcon.Trigger:
        show_main_window()

def exit_application():
    QApplication.quit()

if __name__ == "__main__":
    main()


''' TODO LIST
see that the same program is not running multiple times
1. Add a feature to add new accounts
2. Add a feature to remove accounts
3. Add a feature to edit accounts
4.Add a feature to copy the TOTP code to the clipboard
'''