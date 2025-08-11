import os
import csv
import shutil
from typing import Dict, List, Tuple
from models.player import Player
from models.pitcher import Pitcher
from utils.player_writer import save_players_to_csv
from logic.player_generator import generate_player
from utils.user_manager import clear_users


def _abbr(city: str, name: str, existing: set) -> str:
    base = (city[:1] + name[:2]).upper()
    candidate = base
    i = 1
    while candidate in existing:
        candidate = f"{base}{i}"
        i += 1
    existing.add(candidate)
    return candidate


def _dict_to_model(data: dict):
    potentials = {k[4:]: v for k, v in data.items() if k.startswith("pot_")}
    other_pos = data.get("other_positions")
    common = dict(
        player_id=data.get("player_id"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        birthdate=str(data.get("birthdate")),
        height=data.get("height", 0),
        weight=data.get("weight", 0),
        bats=data.get("bats", "R"),
        primary_position=data.get("primary_position", ""),
        other_positions=other_pos if isinstance(other_pos, list) else (other_pos.split("|") if other_pos else []),
        gf=data.get("gf", 0),
        injured=bool(data.get("injured", 0)),
        injury_description=data.get("injury_description"),
        return_date=data.get("return_date"),
    )
    if data.get("is_pitcher"):
        arm = data.get("arm") or data.get("fb", 0)
        potentials.setdefault("arm", arm)
        return Pitcher(
            **common,
            endurance=data.get("endurance", 0),
            control=data.get("control", 0),
            movement=data.get("movement", 0),
            hold_runner=data.get("hold_runner", 0),
            fb=data.get("fb", 0),
            cu=data.get("cu", 0),
            cb=data.get("cb", 0),
            sl=data.get("sl", 0),
            si=data.get("si", 0),
            scb=data.get("scb", 0),
            kn=data.get("kn", 0),
            arm=arm,
            fa=data.get("fa", 0),
            potential=potentials,
        )
    else:
        return Player(
            **common,
            ch=data.get("ch", 0),
            ph=data.get("ph", 0),
            sp=data.get("sp", 0),
            pl=data.get("pl", 0),
            vl=data.get("vl", 0),
            sc=data.get("sc", 0),
            fa=data.get("fa", 0),
            arm=data.get("arm", 0),
            potential=potentials,
        )


def create_league(base_dir: str, divisions: Dict[str, List[Tuple[str, str]]], league_name: str):
    os.makedirs(base_dir, exist_ok=True)
    rosters_dir = os.path.join(base_dir, "rosters")
    if os.path.exists(rosters_dir):
        shutil.rmtree(rosters_dir)
    os.makedirs(rosters_dir, exist_ok=True)

    clear_users()

    teams_path = os.path.join(base_dir, "teams.csv")
    players_path = os.path.join(base_dir, "players.csv")
    league_path = os.path.join(base_dir, "league.txt")

    team_rows = []
    all_players = []
    existing_abbr = set()

    def generate_roster(num_pitchers: int, num_hitters: int, age_range: Tuple[int, int], ensure_positions: bool = False):
        players = []
        for _ in range(num_pitchers):
            data = generate_player(is_pitcher=True, age_range=age_range)
            data["is_pitcher"] = True
            players.append(data)
        if ensure_positions:
            positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
            for pos in positions:
                data = generate_player(is_pitcher=False, age_range=age_range, primary_position=pos)
                data["is_pitcher"] = False
                players.append(data)
            remaining = num_hitters - len(positions)
        else:
            remaining = num_hitters
        for _ in range(remaining):
            data = generate_player(is_pitcher=False, age_range=age_range)
            data["is_pitcher"] = False
            players.append(data)
        return players

    for division, teams in divisions.items():
        for city, name in teams:
            abbr = _abbr(city, name, existing_abbr)
            team_rows.append({
                "team_id": abbr,
                "name": name,
                "city": city,
                "abbreviation": abbr,
                "division": division,
                "stadium": f"{name} Stadium",
                "primary_color": "#0000FF",
                "secondary_color": "#FFFFFF",
                "owner_id": "",
            })

            act_players = generate_roster(11, 14, (21, 38), ensure_positions=True)
            aaa_players = generate_roster(7, 8, (21, 38))
            low_players = generate_roster(5, 5, (18, 21))

            roster_levels = {"ACT": act_players, "AAA": aaa_players, "LOW": low_players}

            for level_players in roster_levels.values():
                all_players.extend(level_players)

            roster_file = os.path.join(rosters_dir, f"{abbr}.csv")
            with open(roster_file, "w", newline="") as f:
                writer = csv.writer(f)
                for level, players in roster_levels.items():
                    for p in players:
                        writer.writerow([p["player_id"], level])

    player_models = [_dict_to_model(p) for p in all_players]
    save_players_to_csv(player_models, players_path)

    with open(teams_path, "w", newline="") as f:
        fieldnames = [
            "team_id","name","city","abbreviation","division","stadium","primary_color","secondary_color","owner_id"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(team_rows)
    with open(league_path, "w", newline="") as f:
        f.write(league_name)
