from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class PitchersWindow(QDialog):
    """Placeholder window for managing pitchers."""

    def __init__(self, team_id: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pitchers")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Pitchers for {team_id}"))
        self.setLayout(layout)
