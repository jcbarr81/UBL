"""Simple dialog for displaying a placeholder schedule.

This window is intentionally lightweight: it merely shows a few hard-coded
games in a table so that the rest of the application can hook into a schedule
view.  Real schedule data can replace ``schedule_data`` in the future.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class ScheduleWindow(QDialog):
    """Dialog displaying a basic placeholder schedule."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the window title if the underlying widget system supports it.
        try:  # pragma: no cover - some test stubs omit this method
            self.setWindowTitle("Schedule")
        except Exception:  # pragma: no cover - defensive: keep tests happy
            pass

        layout = QVBoxLayout(self)

        # TODO: Replace with real league data once available
        self.schedule_data = [
            ("2024-04-01", "Team A vs Team B"),
            ("2024-04-02", "Team C vs Team D"),
            ("2024-04-03", "Team A at Team C"),
        ]

        # Build the table populated with the placeholder schedule
        self.table = QTableWidget(len(self.schedule_data), 2)
        self.table.setHorizontalHeaderLabels(["Date", "Game"])
        for row, (date, game) in enumerate(self.schedule_data):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(game))
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)

