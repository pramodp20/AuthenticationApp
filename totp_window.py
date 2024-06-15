from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QTime
from otp_generator import get_code
from main_window import MainWindow

class TOTPWindow(QMainWindow):
    def __init__(self, account, icon):
        super().__init__()
        self.account = account
        self.setWindowTitle(account['account_name'])
        self.setGeometry(300, 300, 300, 200)
        self.setWindowIcon(icon)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.label_totp = QLabel("TOTP: ")
        self.layout.addWidget(self.label_totp)
        
        self.label_timer = QLabel("Expires in: ")
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
