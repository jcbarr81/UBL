from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

from utils.logger import logger


class TransactionsPage(QDialog):
    """Placeholder dialog for team transactions."""

    def __init__(self, team_id: str, parent=None):
        super().__init__(parent)
        logger.info("Transactions page opened")
        self.setWindowTitle("Transactions")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Transactions for {team_id}"))
        self.setLayout(layout)
