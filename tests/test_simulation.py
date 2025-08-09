from pathlib import Path

import random

from logic.pbini_loader import load_pbini
from logic.simulation import GameSimulation, TeamState
from models.player import Player
from models.pitcher import Pitcher


class MockRandom(random.Random):
    """Deterministic random generator using a predefined sequence."""

    def __init__(self, values):
        super().__init__()
        self.values = list(values)

    def random(self):  # type: ignore[override]
        return self.values.pop(0)


def make_player(pid: str, ph: int = 50, sp: int = 50, ch: int = 50) -> Player:
    return Player(
        player_id=pid,
        first_name="F" + pid,
        last_name="L" + pid,
        birthdate="2000-01-01",
        height=72,
        weight=180,
        bats="R",
        primary_position="1B",
        other_positions=[],
        gf=50,
        ch=ch,
        ph=ph,
        sp=sp,
        pl=0,
        vl=0,
        sc=0,
        fa=0,
        arm=0,
    )


def make_pitcher(pid: str, endurance: int = 100, hold_runner: int = 50) -> Pitcher:
    return Pitcher(
        player_id=pid,
        first_name="PF" + pid,
        last_name="PL" + pid,
        birthdate="2000-01-01",
        height=72,
        weight=180,
        bats="R",
        primary_position="P",
        other_positions=[],
        gf=50,
        endurance=endurance,
        control=50,
        movement=50,
        hold_runner=hold_runner,
        fb=50,
        cu=0,
        cb=0,
        sl=0,
        si=0,
        scb=0,
        kn=0,
        arm=50,
        fa=50,
    )


def load_config():
    return load_pbini(Path("logic/PBINI.txt"))


def test_pinch_hitter_used():
    cfg = load_config()
    bench = make_player("bench", ph=80)
    starter = make_player("start", ph=10)
    home = TeamState(lineup=[make_player("h1")], bench=[], pitchers=[make_pitcher("hp")])
    away = TeamState(lineup=[starter], bench=[bench], pitchers=[make_pitcher("ap")])
    rng = MockRandom([0.0, 0.0, 1.0])  # pinch, swing(hit), steal attempt none
    sim = GameSimulation(home, away, cfg, rng)
    sim.play_at_bat(away, home)
    assert away.lineup[0].player_id == "bench"
    stats = away.lineup_stats["bench"]
    assert stats.at_bats == 1


def test_steal_attempt_success():
    cfg = load_config()
    runner = make_player("run", ph=80, sp=90)
    home = TeamState(lineup=[make_player("h1")], bench=[], pitchers=[make_pitcher("hp")])
    away = TeamState(lineup=[runner], bench=[], pitchers=[make_pitcher("ap")])
    # swing hit -> 0, steal attempt -> 0, steal success -> 0
    rng = MockRandom([0.0, 0.0, 0.0])
    sim = GameSimulation(home, away, cfg, rng)
    outs = sim.play_at_bat(away, home)
    assert outs == 0
    stats = away.lineup_stats["run"]
    assert stats.steals == 1
    assert away.bases[1] is stats


def test_pitcher_change_when_tired():
    cfg = load_config()
    home = TeamState(
        lineup=[make_player("h1")],
        bench=[],
        pitchers=[make_pitcher("start", endurance=5), make_pitcher("relief")],
    )
    away = TeamState(lineup=[make_player("a1")], bench=[], pitchers=[make_pitcher("ap")])
    rng = MockRandom([0.0, 1.0])  # swing result etc.
    sim = GameSimulation(home, away, cfg, rng)
    sim.play_at_bat(away, home)
    assert home.current_pitcher_state.player.player_id == "relief"
