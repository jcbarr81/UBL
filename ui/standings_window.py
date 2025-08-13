from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from utils.logger import logger


class StandingsWindow(QDialog):
    """Simple dialog displaying dummy league standings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Standings window opened")
        self.setWindowTitle("Standings")
        layout = QVBoxLayout(self)

        # Using placeholder data
        layout.addWidget(QLabel("Using placeholder data"))

        table = QTableWidget()
        # TODO: Replace with real league data
        data = [
            ("Team A", 10, 5),
            ("Team B", 8, 7),
            ("Team C", 7, 8),
            ("Team D", 5, 10),
        ]
        table.setColumnCount(3)
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(["Team", "Wins", "Losses"])
        for row, (team, wins, losses) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(team))
            table.setItem(row, 1, QTableWidgetItem(str(wins)))
            table.setItem(row, 2, QTableWidgetItem(str(losses)))
        table.resizeColumnsToContents()
        layout.addWidget(table)
