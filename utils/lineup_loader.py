import csv
import os
from typing import List, Tuple, Iterable

from logic.simulation import TeamState
from models.player import Player
from models.pitcher import Pitcher
from .player_loader import load_players_from_csv
from .roster_loader import load_roster
from .pitcher_role import get_role


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


def _separate_players(players: Iterable[Player]) -> Tuple[List[Player], List[Pitcher]]:
    """Return hitters and pitchers from ``players``.

    Pitchers are identified using :func:`utils.pitcher_role.get_role`.  Players
    for which ``get_role`` returns ``"SP"`` or ``"RP"`` are treated as
    pitchers, everything else is considered a position player.
    """

    hitters: List[Player] = []
    pitchers: List[Pitcher] = []
    for p in players:
        role = get_role(p)
        if role in {"SP", "RP"}:
            pitchers.append(p)  # type: ignore[arg-type]
        else:
            hitters.append(p)
    return hitters, pitchers


def _build_default_lists(team_id: str, players_file: str, roster_dir: str) -> Tuple[List[Player], List[Player], List[Pitcher]]:
    """Return ``(lineup, bench, pitchers)`` for ``team_id``.

    The active roster is loaded from ``roster_dir`` and players are resolved via
    ``players_file``.  Nine position players are selected for the lineup based
    on descending ``ph`` (power hitting) rating.  Pitchers are ordered with a
    single starter first followed by the remaining bullpen arms.
    """

    all_players = {
        p.player_id: p for p in load_players_from_csv(players_file)
    }
    roster = load_roster(team_id, roster_dir)

    active = [all_players.get(pid) for pid in roster.act]
    active = [p for p in active if p is not None]

    hitters, pitchers = _separate_players(active)

    hitters.sort(key=lambda p: getattr(p, "ph", 0), reverse=True)
    lineup = hitters[:9]
    bench = hitters[9:]

    starter_candidates = [p for p in pitchers if get_role(p) == "SP"]
    if starter_candidates:
        starter = max(starter_candidates, key=lambda p: getattr(p, "endurance", 0))
        bullpen = [p for p in pitchers if p is not starter]
        pitchers_sorted = [starter] + bullpen
    else:
        pitchers.sort(key=lambda p: getattr(p, "endurance", 0), reverse=True)
        pitchers_sorted = pitchers

    return lineup, bench, pitchers_sorted


def build_default_game_state(
    team_id: str,
    players_file: str = "data/players.csv",
    roster_dir: str = "data/rosters",
) -> TeamState:
    """Return a :class:`~logic.simulation.TeamState` for ``team_id``.

    The state uses nine best hitters for the lineup, remaining hitters as the
    bench and pitchers ordered with a starter first followed by the bullpen.
    """

    lineup, bench, pitchers = _build_default_lists(team_id, players_file, roster_dir)

    if len(lineup) < 9:
        raise ValueError(f"Team {team_id} does not have enough position players")
    if not pitchers:
        raise ValueError(f"Team {team_id} does not have any pitchers")

    return TeamState(lineup=lineup, bench=bench, pitchers=pitchers)
