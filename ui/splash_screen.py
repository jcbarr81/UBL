import os
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from ui.login_window import LoginWindow

class SplashScreen(QWidget):
    """Initial splash screen displaying the UBL logo and login button."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("UBL")

        layout = QVBoxLayout()
        layout.addStretch()

        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "logo",
            "UBL.png",
        )
        self.setStyleSheet(
            f"background-image: url({logo_path}); background-repeat: no-repeat; background-position: center;"
        )

        self.start_button = QPushButton("Start Game")
        self.start_button.setFixedSize(200, 60)
        self.start_button.setStyleSheet("font-size: 20px;")
        self.start_button.clicked.connect(self.open_login)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(layout)
        self.login_window = None

    def open_login(self):
        """Show the login window and close the splash screen."""
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
