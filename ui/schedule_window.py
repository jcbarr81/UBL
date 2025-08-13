"""Dialog window for displaying the league schedule.

The table is populated with a handful of hard-coded games so that other
modules (for example, :mod:`ui.owner_dashboard`) have a schedule view to
interact with. Once a dedicated scheduling service or database is
available, ``schedule_data`` should be replaced with real information.
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

        # Build the main layout for the dialog
        layout = QVBoxLayout(self)

        # Placeholder schedule entries
        # TODO: Replace with data from a scheduling service or database
        self.schedule_data = [
            ("2024-04-01", "Team A vs Team B"),
            ("2024-04-02", "Team C vs Team D"),
            ("2024-04-03", "Team A at Team C"),
        ]

        # Create the table and populate it with the placeholder schedule
        self.table = QTableWidget(len(self.schedule_data), 2)
        self.table.setHorizontalHeaderLabels(["Date", "Game"])

        # Fill each row with date and matchup information
        for row, (date, game) in enumerate(self.schedule_data):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(game))
        self.table.resizeColumnsToContents()

        # Add the populated table to the dialog
        layout.addWidget(self.table)

