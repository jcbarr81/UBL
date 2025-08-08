import csv
import os
from logic.league_creator import create_league


def test_create_league_generates_files(tmp_path):
    divisions = {"East": [("CityA", "Cats"), ("CityB", "Dogs")]}
    create_league(str(tmp_path), divisions, roster_size=10)

    teams_path = tmp_path / "teams.csv"
    players_path = tmp_path / "players.csv"
    rosters_dir = tmp_path / "rosters"

    assert teams_path.exists()
    assert players_path.exists()
    assert rosters_dir.is_dir()

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
