import csv
import os
from typing import List, Tuple


def load_lineup(team_id: str, vs: str = "lhp", lineup_dir: str = "data/lineups") -> List[Tuple[str, str]]:
    """Load a lineup from ``lineup_dir`` for the given team.

    Files are expected to follow the naming pattern
    ``{team_id}_vs_{vs}.csv`` and contain columns
    ``order,player_id,position`` where ``player_id`` uses IDs like
    ``P1000``.
    """
    suffix = f"vs_{vs.lower()}"
    file_path = os.path.join(lineup_dir, f"{team_id}_{suffix}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Lineup file not found: {file_path}")

    lineup: List[Tuple[str, str]] = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player_id = row.get("player_id", "").strip()
            position = row.get("position", "").strip()
            lineup.append((player_id, position))
    return lineup
