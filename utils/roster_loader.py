import csv
import os
from models.roster import Roster

def load_roster(team_id, roster_dir="data/rosters"):
    act, aaa, low = [], [], []
    file_path = os.path.join(roster_dir, f"{team_id}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Roster file not found: {file_path}")

    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pid = row["player_id"]
            level = row["level"].upper()
            if level == "ACT":
                act.append(pid)
            elif level == "AAA":
                aaa.append(pid)
            elif level == "LOW":
                low.append(pid)

    return Roster(team_id=team_id, act=act, aaa=aaa, low=low)
