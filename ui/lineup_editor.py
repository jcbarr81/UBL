from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QPushButton, QWidget, QMessageBox, QScrollArea, QGroupBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation
import os
import csv

class LineupEditor(QDialog):
    def __init__(self, team_id):
        self.team_id = team_id
        super().__init__()
        self.setWindowTitle("Lineup Editor")
        self.setMinimumSize(900, 600)

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Left: Field diagram
        field_container = QWidget()
        field_layout = QVBoxLayout(field_container)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(0)

        self.field_label = QLabel()
        field_path = os.path.join("assets", "field_diagram.png")
        if os.path.exists(field_path):
            pixmap = QPixmap(field_path).scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            self.field_label.setPixmap(pixmap)
        else:
            self.field_label.setText("Field Image Placeholder")
            self.field_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        field_layout.addWidget(self.field_label)

        self.field_overlay = QWidget(self.field_label)
        self.field_overlay.setGeometry(0, 0, 400, 500)
        self.field_overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.position_labels = {}
        position_coords = {
            "C": (160, 481), "1B": (225, 341), "2B": (220, 289), "SS": (98, 289),
            "3B": (62, 340), "LF": (55, 235), "CF": (158, 200), "RF": (230, 235), "DH": (275, 415)
        }
        for pos, (x, y) in position_coords.items():
            label = QLabel("", self.field_overlay)
            label.move(x, y)
            label.setStyleSheet("color: blue; font-size: 9px; font-weight: bold; background-color: rgba(255, 255, 255, 0.6); border-radius: 4px;")
            label.setFixedWidth(100)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self.position_labels[pos] = label

        layout.addWidget(field_container)

        # Right: Batting order and bench
        right_container = QWidget()
        right_panel = QVBoxLayout(right_container)
        right_panel.setContentsMargins(10, 10, 10, 10)
        right_panel.setSpacing(12)

        # View selector for vs LHP / vs RHP
        view_selector_group = QGroupBox("Lineup View Mode")
        view_selector_layout = QHBoxLayout()
        self.view_selector = QComboBox()
        self.view_selector.addItems(["vs LHP", "vs RHP"])
        view_selector_layout.addWidget(QLabel("View Lineup For:"))
        view_selector_layout.addWidget(self.view_selector)
        view_selector_group.setLayout(view_selector_layout)
        right_panel.addWidget(view_selector_group)

        # Batting Order
        order_label = QLabel("Batting Order")
        order_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_panel.addWidget(order_label)

        self.order_grid = QGridLayout()
        self.player_dropdowns = []
        self.position_dropdowns = []

        self.players_dict = self.load_players_dict()
        self.act_players = [
            (pid, pdata["name"]) for pid, pdata in self.players_dict.items()
            if "(P)" not in pdata["name"] and pid in self.get_act_level_ids()
        ]

        for i in range(9):
            spot = QLabel(str(i + 1))
            player_dropdown = QComboBox()
            pos_dropdown = QComboBox()
            pos_dropdown.addItems(["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"])
            pos_dropdown.currentIndexChanged.connect(lambda _, i=i: (self.update_player_dropdown(i), self.update_overlay_label(i), self.update_bench_display()))

            self.order_grid.addWidget(spot, i, 0)
            self.order_grid.addWidget(player_dropdown, i, 1)
            self.order_grid.addWidget(pos_dropdown, i, 2)

            player_dropdown.currentIndexChanged.connect(lambda _, i=i: (self.update_overlay_label(i), self.update_bench_display()))

            self.player_dropdowns.append(player_dropdown)
            self.position_dropdowns.append(pos_dropdown)

        right_panel.addLayout(self.order_grid)

        bench_label = QLabel("Substitute / Bench")
        bench_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        right_panel.addWidget(bench_label)

        self.bench_display = QLabel()
        self.bench_display.setMinimumHeight(100)
        self.bench_display.setStyleSheet("margin-bottom: 10px;")
        self.bench_display.setWordWrap(True)
        self.bench_display.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        right_panel.addWidget(self.bench_display)

        save_button = QPushButton("Save Lineup")
        save_button.clicked.connect(self.save_lineup)
        right_panel.addWidget(save_button)

        autofill_button = QPushButton("Auto-Fill Lineup")
        autofill_button.clicked.connect(self.autofill_lineup)
        right_panel.addWidget(autofill_button)

        clear_button = QPushButton("Clear Lineup")
        clear_button.clicked.connect(self.clear_lineup)
        right_panel.addWidget(clear_button)

        layout.addWidget(right_container)

        self.view_selector.currentIndexChanged.connect(self.switch_view)
        self.current_view = "vs LHP"
        self.load_lineup()
        self.update_bench_display()

    def autofill_lineup(self):
        positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]
        used_players = set()

        for i, position in enumerate(positions):
            self.position_dropdowns[i].setCurrentText(position)
            self.update_player_dropdown(i)
            for index in range(self.player_dropdowns[i].count()):
                player_id = self.player_dropdowns[i].itemData(index)
                if player_id not in used_players:
                    self.player_dropdowns[i].setCurrentIndex(index)
                    used_players.add(player_id)
                    if position in self.position_labels:
                        self.position_labels[position].setText(self.players_dict.get(player_id, {}).get("name", ""))
                    break

    def save_lineup(self):
        # Validate that each player is eligible for their selected position
        for i in range(9):
            player_id = self.player_dropdowns[i].currentData()
            position = self.position_dropdowns[i].currentText()

            if not player_id:
                QMessageBox.warning(self, "Validation Error", f"Lineup slot {i + 1} is empty.")
                return

            pdata = self.players_dict.get(player_id)
            if not pdata:
                QMessageBox.warning(self, "Validation Error", f"Player ID {player_id} not found.")
                return

            primary = pdata.get("primary_position")
            others = pdata.get("other_positions", [])
            if position != primary and position not in others:
                QMessageBox.warning(self, "Validation Error", f"{pdata['name']} is not eligible to play {position}.")
                return

        for lbl in self.position_labels.values():
            lbl.setText("")
        for i in range(9):
            player_id = self.player_dropdowns[i].currentData()
            position = self.position_dropdowns[i].currentText()
            if position in self.position_labels:
                self.position_labels[position].setText(self.players_dict.get(player_id, {}).get("name", ""))

        QMessageBox.information(self, "Lineup Validation", "All players are valid for their selected positions.")

    def load_players_dict(self):
        players_file = os.path.join("data", "players.csv")
        players = {}
        if os.path.exists(players_file):
            with open(players_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    player_id = str(row.get("player_id", "")).strip()
                    name = f"{row.get('first_name', '').strip()} {row.get('last_name', '').strip()}"
                    primary = row.get("primary_position", "").strip()
                    others = row.get("other_positions", "").strip().split("/") if row.get("other_positions") else []
                    players[player_id] = {
                        "name": f"{name} ({primary})",
                        "primary_position": primary,
                        "other_positions": others,
                        "ratings": {
                            "CH": row.get("CH", ""),
                            "PH": row.get("PH", ""),
                            "SP": row.get("SP", "")
                        }
                    }
        return players

    def get_act_level_ids(self):
        act_ids = set()
        act_roster_file = os.path.join("data", "rosters", f"{self.team_id}.csv")
        if os.path.exists(act_roster_file):
            with open(act_roster_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2 and row[1].strip().upper() == "ACT":
                        act_ids.add(row[0].strip())
        return act_ids

    def switch_view(self):
        self.current_view = self.view_selector.currentText()
        self.load_lineup()
        self.update_bench_display()

    def get_lineup_filename(self):
        suffix = "lhp" if self.current_view == "vs LHP" else "rhp"
        return os.path.join("data", "rosters", f"{self.team_id}_{suffix}_lineup.csv")

    def load_lineup(self):
        for lbl in self.position_labels.values():
            lbl.setText("")
        filename = self.get_lineup_filename()
        if not os.path.exists(filename):
            return

        with open(filename, "r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= 9:
                    break
                if len(row) >= 2:
                    player_id = row[0].strip()
                    position = row[1].strip()
                    self.position_dropdowns[i].setCurrentText(position)
                    self.update_player_dropdown(i)
                    for index in range(self.player_dropdowns[i].count()):
                        if self.player_dropdowns[i].itemData(index) == player_id:
                            self.player_dropdowns[i].setCurrentIndex(index)
                            if position in self.position_labels:
                                self.position_labels[position].setText(self.players_dict.get(player_id, {}).get("name", ""))
                            break

    def update_bench_display(self):
        used_ids = set(self.player_dropdowns[i].currentData() for i in range(9))
        act_ids = self.get_act_level_ids()
        bench_players = sorted(
            [pdata["name"] for pid, pdata in self.players_dict.items()
             if pid in act_ids and pid not in used_ids and pdata.get("primary_position") not in ["SP", "RP", "P"]]
        )

        columns = [[], [], []]
        for i, name in enumerate(bench_players):
            columns[i // 5 % 3].append(name)

        formatted = ""
        max_rows = max(len(col) for col in columns)
        for i in range(max_rows):
            row = []
            for col in columns:
                row.append(f"{col[i]:<30}" if i < len(col) else " " * 30)
            formatted += "".join(row).rstrip() + ""

        if not formatted.strip():
            formatted = "(none)"

        self.bench_display.setText(formatted)

    def update_overlay_label(self, index):
        position = self.position_dropdowns[index].currentText()
        player_id = self.player_dropdowns[index].currentData()
        if position in self.position_labels:
            label = self.position_labels[position]
            new_name = self.players_dict.get(player_id, {}).get("name", "")

            animation = QPropertyAnimation(label, b"windowOpacity")
            animation.setDuration(200)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)

            def set_text_and_fade_in():
                label.setText(new_name)
                fade_in = QPropertyAnimation(label, b"windowOpacity")
                fade_in.setDuration(200)
                fade_in.setStartValue(0.0)
                fade_in.setEndValue(1.0)
                fade_in.start()
                label.fade_in_anim = fade_in  # prevent garbage collection

            animation.finished.connect(set_text_and_fade_in)
            animation.start()
            label.fade_out_anim = animation  # prevent garbage collection

    def clear_lineup(self):
        for i in range(9):
            self.player_dropdowns[i].setCurrentIndex(-1)
            self.position_dropdowns[i].setCurrentIndex(0)
        for lbl in self.position_labels.values():
            lbl.setText("")
        self.update_bench_display()

    def update_player_dropdown(self, index):
        selected_pos = self.position_dropdowns[index].currentText()
        dropdown = self.player_dropdowns[index]
        dropdown.clear()
        for pid, pdata in self.players_dict.items():
            if pid not in self.get_act_level_ids():
                continue
            primary = pdata.get("primary_position")
            others = pdata.get("other_positions", [])
            if selected_pos == primary or selected_pos in others:
                dropdown.addItem(pdata["name"], userData=pid)
