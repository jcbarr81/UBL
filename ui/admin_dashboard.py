from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QListWidget, QHBoxLayout, QMessageBox
from utils.trade_utils import load_trades, save_trade
from utils.news_logger import log_news_event
from utils.roster_loader import load_roster
from utils.player_loader import load_players_from_csv
from utils.team_loader import load_teams
from models.trade import Trade
import csv

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(200, 200, 500, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Admin Dashboard"))

        self.review_button = QPushButton("Review Trades")
        self.review_button.clicked.connect(self.open_trade_review)
        layout.addWidget(self.review_button)

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
