"""Temporary dialog window for displaying league standings.

The current implementation uses hard-coded data so that other parts of the
application (for example, :mod:`ui.owner_dashboard`) can open a standings
view.  Once a proper data source exists, the placeholder values below should
be replaced with real standings from the services layer or a database.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class StandingsWindow(QDialog):
    """Simple dialog displaying dummy league standings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Standings")

        # Build the vertical layout for the dialog
        layout = QVBoxLayout(self)

        # Inform the user that the table uses placeholder values
        layout.addWidget(QLabel("Using placeholder data"))

        # Create the table widget that will show standings
        table = QTableWidget()

        # Placeholder standings data
        # TODO: Replace with real league data from a standings service
        data = [
            ("Team A", 10, 5),
            ("Team B", 8, 7),
            ("Team C", 7, 8),
            ("Team D", 5, 10),
        ]

        table.setColumnCount(3)
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(["Team", "Wins", "Losses"])

        # Populate the table with the placeholder data above
        for row, (team, wins, losses) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(team))
            table.setItem(row, 1, QTableWidgetItem(str(wins)))
            table.setItem(row, 2, QTableWidgetItem(str(losses)))

        # Ensure columns are sized to fit their contents
        table.resizeColumnsToContents()

        # Add the populated table to the dialog
        layout.addWidget(table)
