from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)

from data.ballparks import BALLPARKS


class TeamSettingsDialog(QDialog):
    """Dialog allowing an owner to configure basic team properties."""

    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.team = team
        self.setWindowTitle("Team Settings")

        layout = QVBoxLayout()

        # Colors
        color_row = QHBoxLayout()
        color_row.addWidget(QLabel("Primary Color:"))
        self.primary_edit = QLineEdit(team.primary_color)
        color_row.addWidget(self.primary_edit)
        color_row.addWidget(QLabel("Secondary Color:"))
        self.secondary_edit = QLineEdit(team.secondary_color)
        color_row.addWidget(self.secondary_edit)
        layout.addLayout(color_row)

        # Stadium selection
        stadium_row = QHBoxLayout()
        stadium_row.addWidget(QLabel("Stadium:"))
        self.stadium_combo = QComboBox()
        self.stadium_combo.addItems(sorted(BALLPARKS))
        if team.stadium in BALLPARKS:
            self.stadium_combo.setCurrentText(team.stadium)
        stadium_row.addWidget(self.stadium_combo)
        layout.addLayout(stadium_row)

        # Action buttons
        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def get_settings(self):
        return {
            "primary_color": self.primary_edit.text().strip(),
            "secondary_color": self.secondary_edit.text().strip(),
            "stadium": self.stadium_combo.currentText(),
        }

