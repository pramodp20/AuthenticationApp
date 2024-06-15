from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from json_handler import get_accounts
from totp_window import TOTPWindow

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
