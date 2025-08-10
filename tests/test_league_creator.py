import csv
import os
from logic.league_creator import create_league, _dict_to_model
from models.pitcher import Pitcher
from logic.player_generator import reset_name_cache
import random


def test_create_league_generates_files(tmp_path):
    divisions = {"East": [("CityA", "Cats"), ("CityB", "Dogs")]}
    create_league(str(tmp_path), divisions, "Test League", roster_size=10)

    teams_path = tmp_path / "teams.csv"
    players_path = tmp_path / "players.csv"
    rosters_dir = tmp_path / "rosters"
    league_path = tmp_path / "league.txt"

    assert teams_path.exists()
    assert players_path.exists()
    assert rosters_dir.is_dir()
    assert league_path.exists()

    with open(teams_path, newline="") as f:
        teams = list(csv.DictReader(f))
    assert len(teams) == 2

    with open(players_path, newline="") as f:
        players = list(csv.DictReader(f))
    assert len(players) == 20

    for t in teams:
        r_file = rosters_dir / f"{t['team_id']}.csv"
        assert r_file.exists()
        with open(r_file) as f:
            lines = [line for line in f.read().strip().splitlines() if line]
        assert len(lines) == 10
    with open(league_path) as f:
        assert f.read() == "Test League"


def test_create_league_uses_unique_names(tmp_path):
    reset_name_cache()
    random.seed(0)
    divisions = {"East": [("CityA", "Cats")]}  # single team for simplicity
    create_league(str(tmp_path), divisions, "Test League", roster_size=10)

    players_path = tmp_path / "players.csv"
    with open(players_path, newline="") as f:
        players = list(csv.DictReader(f))

    names = {(p["first_name"], p["last_name"]) for p in players}
    assert ("John", "Doe") not in names
    assert len(names) == len(players)

    with open("data/names.csv", newline="") as f:
        allowed = {(r["first_name"], r["last_name"]) for r in csv.DictReader(f)}
    assert names <= allowed


def test_dict_to_model_defaults_pitcher_arm_to_fastball():
    data = {
        "player_id": "p1",
        "first_name": "Pitch",
        "last_name": "Er",
        "birthdate": "1990-01-01",
        "height": 72,
        "weight": 180,
        "bats": "R",
        "primary_position": "P",
        "other_positions": "",
        "gf": 5,
        "is_pitcher": True,
        "endurance": 50,
        "control": 60,
        "movement": 55,
        "hold_runner": 40,
        "fb": 70,
        "cu": 60,
        "cb": 50,
        "sl": 55,
        "si": 45,
        "scb": 65,
        "kn": 40,
    }
    pitcher = _dict_to_model(data)
    assert isinstance(pitcher, Pitcher)
    assert pitcher.arm == 70
    assert pitcher.potential["arm"] == 70
