import random
from utils.trade_utils import save_trade
from utils.team_loader import load_teams
from models.trade import Trade
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTabWidget, QListWidget, QTextEdit,
    QPushButton, QHBoxLayout, QComboBox, QMessageBox, QDialog, QListWidgetItem
)
from PyQt6.QtCore import Qt
from ui.lineup_editor import LineupEditor
from ui.pitching_editor import PitchingEditor
from utils.roster_loader import load_roster
from utils.player_loader import load_players_from_csv
from utils.news_reader import read_latest_news
from utils.free_agent_finder import find_free_agents
import csv
import os

class OwnerDashboard(QWidget):
    def __init__(self, team_id):
        super().__init__()
        self.team_id = team_id
        self.setWindowTitle(f"Owner Dashboard - {team_id}")
        self.setGeometry(200, 200, 800, 600)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel(f"Welcome, Owner of {team_id}!"))

        # Load data
        self.players = {p.player_id: p for p in load_players_from_csv("data/players.csv")}
        self.roster = load_roster(team_id)

        # Create tab widget for roster
        self.lineup_button = QPushButton("Manage Lineups")
        self.lineup_button.clicked.connect(self.open_lineup_editor)
        main_layout.addWidget(self.lineup_button)
        self.rotation_button = QPushButton("Manage Pitching Staff")
        self.rotation_button.clicked.connect(self.open_pitching_editor)
        main_layout.addWidget(self.rotation_button)

        self.tabs = QTabWidget()
        self.act_list = self.create_roster_list(self.roster.act)
        self.aaa_list = self.create_roster_list(self.roster.aaa)
        self.low_list = self.create_roster_list(self.roster.low)

        self.tabs.addTab(self.act_list, "Active (ACT)")
        self.tabs.addTab(self.aaa_list, "AAA")
        self.tabs.addTab(self.low_list, "LOW")

        # Move player controls
        move_layout = QHBoxLayout()
        self.move_dropdown = QComboBox()
        self.move_dropdown.addItems(["ACT", "AAA", "LOW"])
        self.move_button = QPushButton("Move Selected Player")
        self.move_button.clicked.connect(self.move_selected_player)
        self.cut_button = QPushButton("Cut Selected Player")
        self.cut_button.clicked.connect(self.cut_selected_player)
        move_layout.addWidget(QLabel("Move to:"))
        move_layout.addWidget(self.move_dropdown)
        move_layout.addWidget(self.move_button)
        move_layout.addWidget(self.cut_button)

        self.news_feed = QTextEdit()
        self.news_feed.setReadOnly(True)
        self.news_feed.setMinimumHeight(100)
        self.load_news_feed()

        # Assemble layout
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(move_layout)
        self.trade_button = QPushButton("Propose Trade")
        self.trade_button.clicked.connect(self.open_trade_dialog)
        main_layout.addWidget(self.trade_button)
        sign_layout = QHBoxLayout()
        self.sign_button = QPushButton("Sign Free Agent")
        self.sign_button.clicked.connect(self.open_sign_dialog)
        sign_layout.addWidget(self.sign_button)
        main_layout.addLayout(sign_layout)
        main_layout.addWidget(QLabel("League News"))
        main_layout.addWidget(self.news_feed)
        self.setLayout(main_layout)

    def open_lineup_editor(self):
        editor = LineupEditor(self.team_id)
        editor.exec()

    def open_pitching_editor(self):
        editor = PitchingEditor(self.team_id)
        editor.exec()

    def create_roster_list(self, player_ids):
        list_widget = QListWidget()
        for pid in player_ids:
            player = self.players.get(pid)
            if player:
                display = f"{pid} - {player.first_name} {player.last_name} - {player.primary_position}"
                list_widget.addItem(display)
            else:
                list_widget.addItem(f"{pid} (Missing)")
        return list_widget

    def load_news_feed(self):
        news_items = read_latest_news(10)
        self.news_feed.setText("\n".join(news_items))

    def move_selected_player(self):
        current_tab = self.tabs.currentIndex()
        current_list = [self.act_list, self.aaa_list, self.low_list][current_tab]
        selected_item = current_list.currentItem()

        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select a player to move.")
            return

        selected_text = selected_item.text()
        player_id = selected_text.split(" - ")[0].strip()

        from_level = ["act", "aaa", "low"][current_tab]
        to_level = self.move_dropdown.currentText().lower()

        if from_level == to_level:
            QMessageBox.information(self, "No Action", "Player is already on that roster.")
            return

        getattr(self.roster, from_level).remove(player_id)
        getattr(self.roster, to_level).append(player_id)
        self.save_roster_to_csv()
        self.refresh_roster_views()
        QMessageBox.information(self, "Success", f"Moved {player_id} to {to_level.upper()}.")

    def save_roster_to_csv(self):
        file_path = f"data/rosters/{self.team_id}.csv"
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["player_id", "level"])
            writer.writeheader()
            for level in ["act", "aaa", "low"]:
                for pid in getattr(self.roster, level):
                    writer.writerow({"player_id": pid, "level": level.upper()})

    def refresh_roster_views(self):
        for tab, player_ids in zip(
            [self.act_list, self.aaa_list, self.low_list],
            [self.roster.act, self.roster.aaa, self.roster.low]
        ):
            tab.clear()
            for pid in player_ids:
                player = self.players.get(pid)
                if player:
                    tab.addItem(f"{pid} - {player.first_name} {player.last_name} - {player.primary_position}")

    def open_sign_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sign Free Agent")
        dialog.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()
        agent_list = QListWidget()
        free_agents = find_free_agents(list(self.players.values()))

        for p in free_agents:
            agent_list.addItem(QListWidgetItem(f"{p.player_id} - {p.first_name} {p.last_name} - {p.primary_position}"))

        sign_button = QPushButton("Sign to LOW")
        sign_button.clicked.connect(lambda: self.sign_agent(agent_list, dialog))

        layout.addWidget(QLabel("Available Free Agents:"))
        layout.addWidget(agent_list)
        layout.addWidget(sign_button)
        dialog.setLayout(layout)
        dialog.exec()

    def sign_agent(self, list_widget, dialog):
        selected = list_widget.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a free agent to sign.")
            return

        player_id = selected.text().split(" - ")[0].strip()
        self.roster.low.append(player_id)
        self.save_roster_to_csv()
        self.refresh_roster_views()
        QMessageBox.information(self, "Signed", f"{player_id} signed to LOW roster.")
        dialog.accept()

    def cut_selected_player(self):
        current_tab = self.tabs.currentIndex()
        current_list = [self.act_list, self.aaa_list, self.low_list][current_tab]
        selected_item = current_list.currentItem()

        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select a player to cut.")
            return

        selected_text = selected_item.text()
        player_id = selected_text.split(" - ")[0].strip()
        level = ["act", "aaa", "low"][current_tab]

        confirm = QMessageBox.question(
            self,
            "Confirm Cut",
            f"Are you sure you want to cut {player_id} from {level.upper()}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            getattr(self.roster, level).remove(player_id)
            self.save_roster_to_csv()
            self.refresh_roster_views()
            QMessageBox.information(self, "Player Cut", f"{player_id} has been released.")

    def open_trade_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Propose Trade")
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout()

        your_list = QListWidget()
        your_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for pid in self.roster.act + self.roster.aaa + self.roster.low:
            p = self.players.get(pid)
            if p:
                your_list.addItem(f"{pid} - {p.first_name} {p.last_name} - {p.primary_position}")

        teams = load_teams("data/teams.csv")
        team_dropdown = QComboBox()
        team_options = [t for t in teams if t.team_id != self.team_id]
        for t in team_options:
            team_dropdown.addItem(f"{t.team_id} - {t.name}")

        opp_list = QListWidget()
        opp_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        def load_opp_roster():
            opp_team_id = team_dropdown.currentText().split(" - ")[0]
            from utils.roster_loader import load_roster
            opp_roster = load_roster(opp_team_id)
            opp_list.clear()
            for pid in opp_roster.act + opp_roster.aaa + opp_roster.low:
                p = self.players.get(pid)
                if p:
                    opp_list.addItem(f"{pid} - {p.first_name} {p.last_name} - {p.primary_position}")

        team_dropdown.currentIndexChanged.connect(load_opp_roster)
        load_opp_roster()

        submit_btn = QPushButton("Submit Trade Proposal")
        def submit_trade():
            from_team = self.team_id
            to_team = team_dropdown.currentText().split(" - ")[0]
            give = [item.text().split(" - ")[0] for item in your_list.selectedItems()]
            receive = [item.text().split(" - ")[0] for item in opp_list.selectedItems()]
            if not give or not receive:
                QMessageBox.warning(dialog, "Incomplete", "Select players to trade and request.")
                return
            trade_id = f"T{random.randint(1000, 9999)}"
            trade = Trade(
                trade_id=trade_id,
                from_team=from_team,
                to_team=to_team,
                give_player_ids=give,
                receive_player_ids=receive,
                status="pending"
            )
            save_trade(trade)
            QMessageBox.information(dialog, "Trade Submitted", f"Trade {trade_id} submitted for review.")
            dialog.accept()

        submit_btn.clicked.connect(submit_trade)

        layout.addWidget(QLabel("Your Players:"))
        layout.addWidget(your_list)
        layout.addWidget(QLabel("Target Team:"))
        layout.addWidget(team_dropdown)
        layout.addWidget(QLabel("Their Players:"))
        layout.addWidget(opp_list)
        layout.addWidget(submit_btn)

        dialog.setLayout(layout)
        dialog.exec()
