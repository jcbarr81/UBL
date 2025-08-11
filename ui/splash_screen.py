from pathlib import Path
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from ui.login_window import LoginWindow

class SplashScreen(QWidget):
    """Initial splash screen displaying the UBL logo and login button."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("UBL")

        self.setObjectName("splash_screen")

        layout = QVBoxLayout()
        layout.addStretch()

        logo_path = Path(__file__).resolve().parents[1] / "logo" / "UBL.png"
        logo_url = logo_path.as_posix()
        self.setStyleSheet(
            f"""
            #splash_screen {{
                border-image: url('{logo_url}') 0 0 0 0 stretch stretch;
            }}
            """
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
