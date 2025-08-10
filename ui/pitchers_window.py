"""Dialog for viewing pitchers grouped by roster level and role."""

from datetime import datetime
from typing import Dict, Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QVBoxLayout,
)

from models.base_player import BasePlayer
from models.roster import Roster


class PitchersWindow(QDialog):
    """Display all pitchers grouped by roster level with tabs for roles."""

    pitcher_positions = {"SP", "RP", "P"}

    def __init__(self, players: Dict[str, BasePlayer], roster: Roster, parent=None):
        super().__init__(parent)
        self.players = players
        self.roster = roster

        self.setWindowTitle("Pitchers")

        layout = QVBoxLayout()
        layout.addWidget(self._build_level_section("Active (ACT)", roster.act))
        layout.addWidget(self._build_level_section("AAA", roster.aaa))
        layout.addWidget(self._build_level_section("LOW", roster.low))
        layout.addStretch()
        self.setLayout(layout)

        size = self.sizeHint()
        self.resize(size.width() * 2, size.height())

    # ------------------------------------------------------------------
    # Builders
    def _build_level_section(self, title: str, player_ids: Iterable[str]) -> QGroupBox:
        """Create a section showing pitchers for a single level using tabs."""

        group = QGroupBox(title)
        layout = QVBoxLayout()

        groups = {"SP": [], "RP": []}
        for pid in player_ids:
            p = self.players.get(pid)
            if not p or p.primary_position not in self.pitcher_positions:
                continue
            if p.primary_position == "SP":
                groups["SP"].append(p)
            else:
                groups["RP"].append(p)

        tab_widget = QTabWidget()
        for role, players in groups.items():
            if not players:
                continue
            lw = QListWidget()
            for player in players:
                lw.addItem(self._make_pitcher_item(player))
            label = "Starting Pitchers (SP)" if role == "SP" else "Relief Pitchers (RP)"
            tab_widget.addTab(lw, label)

        layout.addWidget(tab_widget)
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

