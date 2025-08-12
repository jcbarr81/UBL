"""Utilities for generating player avatar images.

Creates simple illustrated headshots for each player using the
:mod:`images.avatars` module. Avatars are written to ``images/avatars``
relative to the repository root and named after the player's ID.
"""
from __future__ import annotations

import os
from typing import Dict

from PIL import Image

from images.avatars import generate_player_headshot
from utils.player_loader import load_players_from_csv
from utils.team_loader import load_teams
from utils.roster_loader import load_roster


def generate_player_avatars(out_dir: str | None = None, size: int = 512) -> str:
    """Generate avatar images for all players and return the output directory.

    Parameters
    ----------
    out_dir:
        Optional output directory. Defaults to ``images/avatars`` relative to
        the project root.
    size:
        Pixel size for the generated square avatars.
    """

    players = {p.player_id: p for p in load_players_from_csv("data/players.csv")}
    teams = load_teams("data/teams.csv")

    # Map each player ID to their team ID via roster files
    player_team: Dict[str, str] = {}
    for t in teams:
        try:
            roster = load_roster(t.team_id)
        except FileNotFoundError:
            continue
        for pid in roster.act + roster.aaa + roster.low:
            player_team[pid] = t.team_id

    if out_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        out_dir = os.path.join(base_dir, "images", "avatars")
    os.makedirs(out_dir, exist_ok=True)

    team_map = {t.team_id: t for t in teams}
    for pid, player in players.items():
        team_id = player_team.get(pid)
        if not team_id:
            continue
        team = team_map.get(team_id)
        if not team:
            continue
        name = f"{player.first_name} {player.last_name}"
        img = generate_player_headshot(
            player_name=name,
            team_primary_hex=team.primary_color,
            team_secondary_hex=team.secondary_color,
            size=size,
        )
        img.save(os.path.join(out_dir, f"{pid}.png"))
        # Smaller version for UI thumbnails
        thumb = img.resize((150, 150), resample=Image.LANCZOS)
        thumb.save(os.path.join(out_dir, f"{pid}_150.png"))

    return out_dir
