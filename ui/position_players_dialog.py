from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class PositionPlayersDialog(QDialog):
    """Simple placeholder dialog for listing position players."""

    def __init__(self, team_id: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Position Players")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Position players for {team_id}"))
        self.setLayout(layout)
