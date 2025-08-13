from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from logic.team_name_generator import random_team

from utils.logger import logger


class TeamEntryDialog(QDialog):
    """Dialog for entering team cities and nicknames."""

    def __init__(self, divisions, teams_per_div, parent=None):
        super().__init__(parent)
        logger.info("Team entry dialog opened")
        self.setWindowTitle("Enter Teams")
        self._inputs = {}

        layout = QVBoxLayout()

        for div in divisions:
            layout.addWidget(QLabel(f"{div} Division"))
            self._inputs[div] = []
            for i in range(teams_per_div):
                row = QHBoxLayout()
                city_edit = QLineEdit()
                city_edit.setPlaceholderText("City")
                name_edit = QLineEdit()
                name_edit.setPlaceholderText("Nickname")
                row.addWidget(city_edit)
                row.addWidget(name_edit)
                random_btn = QPushButton("Randomize")
                row.addWidget(random_btn)
                layout.addLayout(row)
                self._inputs[div].append((city_edit, name_edit))
                random_btn.clicked.connect(
                    lambda _, c=city_edit, n=name_edit: self._random_fill(c, n)
                )

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        save_btn.clicked.connect(self._handle_save)
        cancel_btn.clicked.connect(self.reject)

        self.setLayout(layout)

    def _random_fill(self, city_edit: QLineEdit, name_edit: QLineEdit) -> None:
        """Populate the provided fields with a random team name."""
        try:
            city, nickname = random_team()
        except RuntimeError as exc:
            QMessageBox.warning(self, "Names Exhausted", str(exc))
            return
        city_edit.setText(city)
        name_edit.setText(nickname)

    def _handle_save(self):
        for fields in self._inputs.values():
            for city, name in fields:
                if not city.text().strip() or not name.text().strip():
                    QMessageBox.warning(self, "Error", "All fields must be filled.")
                    return
        self.accept()

    def get_structure(self):
        structure = {}
        for div, fields in self._inputs.items():
            teams = []
            for city, name in fields:
                teams.append((city.text().strip(), name.text().strip()))
            structure[div] = teams
        return structure
