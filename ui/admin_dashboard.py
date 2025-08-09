from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QDialog,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
    QInputDialog,
    QLineEdit,
    QComboBox,
)
from PyQt6.QtCore import Qt
from utils.trade_utils import load_trades, save_trade
from utils.news_logger import log_news_event
from utils.roster_loader import load_roster
from utils.player_loader import load_players_from_csv
from utils.team_loader import load_teams
from utils.user_manager import add_user
from models.trade import Trade
import csv
import os
from logic.league_creator import create_league

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(200, 200, 500, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("Welcome to the Admin Dashboard")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)

        layout.addStretch()

        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        self.review_button = QPushButton("Review Trades")
        self.review_button.clicked.connect(self.open_trade_review)
        button_layout.addWidget(self.review_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.create_league_button = QPushButton("Create League")
        self.create_league_button.clicked.connect(self.open_create_league)
        button_layout.addWidget(self.create_league_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.open_add_user)
        button_layout.addWidget(self.add_user_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(button_layout)
        layout.addStretch()

        self.setStyleSheet(
            """
            QWidget {background-color: #2c2c2c; color: #f0f0f0; font-size: 14px;}
            QPushButton {
                background-color: #444;
                color: #f0f0f0;
                padding: 8px;
                border: 1px solid #555;
            }
            QPushButton:hover {background-color: #555;}
            """
        )

        self.setLayout(layout)

    def open_trade_review(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Review Pending Trades")
        dialog.setMinimumSize(600, 400)

        trades = load_trades()
        players = {p.player_id: p for p in load_players_from_csv("data/players.csv")}
        teams = {t.team_id: t for t in load_teams("data/teams.csv")}

        layout = QVBoxLayout()

        trade_list = QListWidget()
        trade_map = {}

        for t in trades:
            if t.status != "pending":
                continue
            give_names = [f"{pid} ({players[pid].first_name} {players[pid].last_name})" for pid in t.give_player_ids if pid in players]
            recv_names = [f"{pid} ({players[pid].first_name} {players[pid].last_name})" for pid in t.receive_player_ids if pid in players]
            summary = f"{t.trade_id}: {t.from_team} → {t.to_team} | Give: {', '.join(give_names)} | Get: {', '.join(recv_names)}"
            trade_list.addItem(summary)
            trade_map[summary] = t

        def process_trade(accept=True):
            selected = trade_list.currentItem()
            if not selected:
                return
            summary = selected.text()
            trade = trade_map[summary]

            # Update rosters
            from_roster = load_roster(trade.from_team)
            to_roster = load_roster(trade.to_team)

            for pid in trade.give_player_ids:
                for level in ["act", "aaa", "low"]:
                    if pid in getattr(from_roster, level):
                        getattr(from_roster, level).remove(pid)
                        getattr(to_roster, level).append(pid)
                        break

            for pid in trade.receive_player_ids:
                for level in ["act", "aaa", "low"]:
                    if pid in getattr(to_roster, level):
                        getattr(to_roster, level).remove(pid)
                        getattr(from_roster, level).append(pid)
                        break

            # Save updated rosters
            def save_roster(roster):
                path = f"data/rosters/{roster.team_id}.csv"
                with open(path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["player_id", "level"])
                    writer.writeheader()
                    for lvl in ["act", "aaa", "low"]:
                        for pid in getattr(roster, lvl):
                            writer.writerow({"player_id": pid, "level": lvl.upper()})

            save_roster(from_roster)
            save_roster(to_roster)

            # Update trade status
            trade.status = "accepted" if accept else "rejected"
            save_trade(trade)

            log_news_event(f"TRADE {'ACCEPTED' if accept else 'REJECTED'}: {summary}")
            QMessageBox.information(dialog, "Trade Processed", f"{summary} marked as {trade.status.upper()}.")
            trade_list.takeItem(trade_list.currentRow())

        btn_layout = QHBoxLayout()
        accept_btn = QPushButton("Accept Trade")
        reject_btn = QPushButton("Reject Trade")
        accept_btn.clicked.connect(lambda: process_trade(True))
        reject_btn.clicked.connect(lambda: process_trade(False))
        btn_layout.addWidget(accept_btn)
        btn_layout.addWidget(reject_btn)

        layout.addWidget(trade_list)
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()

    def open_add_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add User")

        layout = QVBoxLayout()

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        team_combo = QComboBox()


        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        teams = load_teams(os.path.join(data_dir, "teams.csv"))
        for t in teams:
            team_combo.addItem(f"{t.name} ({t.team_id})", userData=t.team_id)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(password_input)
        layout.addWidget(QLabel("Team:"))
        layout.addWidget(team_combo)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        def handle_add():
            username = username_input.text().strip()
            password = password_input.text().strip()
            team_id = team_combo.currentData()
            if not username or not password:
                QMessageBox.warning(dialog, "Error", "Username and password required.")
                return
            try:
                add_user(username, password, "owner", team_id)
            except ValueError as e:
                QMessageBox.warning(dialog, "Error", str(e))
                return
            QMessageBox.information(dialog, "Success", f"User {username} added.")
            dialog.accept()

        add_btn.clicked.connect(handle_add)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec()

    def open_create_league(self):
        confirm = QMessageBox.question(
            self,
            "Overwrite Existing League?",
            "Creating a new league will overwrite the current league and teams. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        div_text, ok = QInputDialog.getText(
            self, "Divisions", "Enter division names separated by commas:"
        )
        if not ok or not div_text:
            return
        divisions = [d.strip() for d in div_text.split(",") if d.strip()]
        if not divisions:
            return

        teams_per_div, ok = QInputDialog.getInt(
            self, "Teams", "Teams per division:", 2, 1, 20
        )
        if not ok:
            return

        structure = {}
        for div in divisions:
            teams = []
            for i in range(teams_per_div):
                city, ok = QInputDialog.getText(self, "Team City", f"{div} division - Team {i+1} city:")
                if not ok:
                    return
                name, ok = QInputDialog.getText(self, "Team Name", f"{div} division - Team {i+1} name:")
                if not ok:
                    return
                teams.append((city, name))
            structure[div] = teams

        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        create_league(data_dir, structure)
        QMessageBox.information(self, "League Created", "New league generated.")
