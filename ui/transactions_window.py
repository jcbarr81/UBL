"""Placeholder dialog for future transaction features."""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout


class TransactionsWindow(QDialog):
    """Simple dialog announcing upcoming transaction tools."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Transactions")
        # Match font usage with other roster dialogs
        self.setFont(QFont("Courier New", 9))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Coming soon"))
        layout.addStretch()
        self.setLayout(layout)

        size = self.sizeHint()
        self.resize(size.width() * 2, size.height())

