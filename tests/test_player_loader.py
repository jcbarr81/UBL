import csv
import pytest
from utils.player_loader import load_players_from_csv


def test_load_player_with_optional_columns_missing(tmp_path):
    file_path = tmp_path / "players.csv"
    fieldnames = [
        "player_id",
        "first_name",
        "last_name",
        "birthdate",
        "height",
        "weight",
        "bats",
        "primary_position",
        "gf",
        "is_pitcher",
        "ch",
        "ph",
        "sp",
        "pl",
        "vl",
        "sc",
        "fa",
        "arm",
    ]
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "player_id": "1",
                "first_name": "John",
                "last_name": "Doe",
                "birthdate": "1990-01-01",
                "height": "72",
                "weight": "180",
                "bats": "R",
                "primary_position": "1B",
                "gf": "50",
                "is_pitcher": "false",
                "ch": "60",
                "ph": "55",
                "sp": "70",
                "pl": "65",
                "vl": "75",
                "sc": "80",
                "fa": "85",
                "arm": "90",
            }
        )
    players = load_players_from_csv(file_path)
    assert len(players) == 1
    player = players[0]
    assert player.other_positions == []
    assert player.injury_description is None
    assert player.potential["ch"] == 60
    assert player.potential["gf"] == 50


def test_missing_required_numeric_field_raises(tmp_path):
    file_path = tmp_path / "players.csv"
    fieldnames = [
        "player_id",
        "first_name",
        "last_name",
        "birthdate",
        "height",
        "weight",
        "bats",
        "primary_position",
        "gf",
        "is_pitcher",
        "ch",
        "ph",
        "sp",
        "pl",
        "vl",
        "sc",
        "fa",
        "arm",
    ]
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "player_id": "1",
                "first_name": "John",
                "last_name": "Doe",
                "birthdate": "1990-01-01",
                "height": "",
                "weight": "180",
                "bats": "R",
                "primary_position": "1B",
                "gf": "50",
                "is_pitcher": "false",
                "ch": "60",
                "ph": "55",
                "sp": "70",
                "pl": "65",
                "vl": "75",
                "sc": "80",
                "fa": "85",
                "arm": "90",
            }
        )
    with pytest.raises(ValueError):
        load_players_from_csv(file_path)
