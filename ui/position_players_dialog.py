"""Dialog for viewing position players grouped by roster level and position."""

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


class PositionPlayersDialog(QDialog):
    """Display all position players grouped by roster level and position."""

    pitcher_positions = {"SP", "RP", "P"}

    def __init__(self, players: Dict[str, BasePlayer], roster: Roster, parent=None):
        super().__init__(parent)
        self.players = players
        self.roster = roster

        self.setWindowTitle("Position Players")

        layout = QVBoxLayout()
        layout.addWidget(self._build_level_section("ACT", roster.act))
        layout.addWidget(self._build_level_section("AAA", roster.aaa))
        layout.addWidget(self._build_level_section("LOW", roster.low))
        layout.addStretch()
        self.setLayout(layout)

    # ------------------------------------------------------------------
    # Section builders
    def _build_level_section(self, label: str, player_ids: Iterable[str]) -> QGroupBox:
        """Create a section showing position players for a single level."""

        level_box = QGroupBox(label)
        layout = QVBoxLayout()

        groups = {}
        for pid in player_ids:
            p = self.players.get(pid)
            if not p or p.primary_position in self.pitcher_positions:
                continue
            groups.setdefault(p.primary_position, []).append(p)

        for position, players in sorted(groups.items()):
            group_box = QGroupBox(position)
            gb_layout = QVBoxLayout()
            lw = QListWidget()
            for player in players:
                lw.addItem(self._make_player_item(player))
            gb_layout.addWidget(lw)
            group_box.setLayout(gb_layout)
            layout.addWidget(group_box)

        layout.addStretch()
        level_box.setLayout(layout)
        return level_box

    # ------------------------------------------------------------------
    # Helpers
    def _make_player_item(self, p: BasePlayer) -> QListWidgetItem:
        """Format a player entry similar to OwnerDashboard._make_player_item."""

        age = self._calculate_age(p.birthdate)
        is_pitcher_role = (p.primary_position in self.pitcher_positions) or hasattr(p, "endurance")
        if is_pitcher_role:
            core = f"AS:{getattr(p, 'arm', 0)} EN:{getattr(p, 'endurance', 0)} CO:{getattr(p, 'control', 0)}"
        else:
            core = f"CH:{getattr(p, 'ch', 0)} PH:{getattr(p, 'ph', 0)} SP:{getattr(p, 'sp', 0)}"
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

