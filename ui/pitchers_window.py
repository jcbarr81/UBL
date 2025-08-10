"""Dialog for viewing pitchers grouped by roster level and role."""

from datetime import datetime
from typing import Dict, Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from models.base_player import BasePlayer
from models.roster import Roster


class PitchersWindow(QDialog):
    """Display all pitchers grouped by roster level and role."""

    pitcher_positions = {"SP", "RP", "P"}

    def __init__(self, players: Dict[str, BasePlayer], roster: Roster, parent=None):
        super().__init__(parent)
        self.players = players
        self.roster = roster

        self.setWindowTitle("Pitchers")

        layout = QVBoxLayout()
        layout.addWidget(self._build_level_group("Active (ACT)", roster.act))
        layout.addWidget(self._build_level_group("AAA", roster.aaa))
        layout.addWidget(self._build_level_group("LOW", roster.low))
        layout.addStretch()
        self.setLayout(layout)

    # ------------------------------------------------------------------
    # Builders
    def _build_level_group(self, title: str, player_ids: Iterable[str]) -> QGroupBox:
        """Create a group showing pitchers for a single level."""

        group = QGroupBox(title)
        layout = QVBoxLayout()

        sp_box = QGroupBox("Starting Pitchers (SP)")
        sp_layout = QVBoxLayout()
        sp_list = QListWidget()

        rp_box = QGroupBox("Relief Pitchers (RP)")
        rp_layout = QVBoxLayout()
        rp_list = QListWidget()

        for pid in player_ids:
            p = self.players.get(pid)
            if not p or p.primary_position not in self.pitcher_positions:
                continue
            item = self._make_pitcher_item(p)
            if p.primary_position == "SP":
                sp_list.addItem(item)
            else:
                rp_list.addItem(item)

        sp_layout.addWidget(sp_list)
        sp_box.setLayout(sp_layout)
        rp_layout.addWidget(rp_list)
        rp_box.setLayout(rp_layout)

        layout.addWidget(sp_box)
        layout.addWidget(rp_box)
        group.setLayout(layout)
        return group

    # ------------------------------------------------------------------
    # Helpers
    def _make_pitcher_item(self, p: BasePlayer) -> QListWidgetItem:
        age = self._calculate_age(p.birthdate)
        core = f"AS:{getattr(p, 'arm', 0)} EN:{getattr(p, 'endurance', 0)} CO:{getattr(p, 'control', 0)}"
        label = f"{p.first_name} {p.last_name} ({age}) - {p.primary_position} | {core}"
        item = QListWidgetItem(label)
        item.setData(Qt.ItemDataRole.UserRole, p.player_id)
        return item

    def _calculate_age(self, birthdate_str: str):
        try:
            birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
            today = datetime.today().date()
            return today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
            )
        except Exception:
            return "?"

