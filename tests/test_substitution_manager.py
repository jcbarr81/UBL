from pathlib import Path

import random

from logic.pbini_loader import load_pbini
from logic.simulation import BatterState, TeamState
from logic.substitution_manager import SubstitutionManager
from models.player import Player
from models.pitcher import Pitcher


class MockRandom(random.Random):
    """Deterministic random generator using a predefined sequence."""

    def __init__(self, values):
        super().__init__()
        self.values = list(values)

    def random(self):  # type: ignore[override]
        return self.values.pop(0)


def make_player(
    pid: str, ph: int = 50, sp: int = 50, gf: int = 50, ch: int = 50
) -> Player:
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
        gf=gf,
        ch=ch,
        ph=ph,
        sp=sp,
        pl=0,
        vl=0,
        sc=0,
        fa=0,
        arm=0,
    )


def make_pitcher(pid: str, endurance: int = 100) -> Pitcher:
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
        hold_runner=50,
        fb=50,
        cu=0,
        cb=0,
        sl=0,
        si=0,
        scb=0,
        kn=0,
        arm=50,
        fa=50,
        role="SP",
    )


def load_config():
    return load_pbini(Path("logic/PBINI.txt"))


def test_pinch_hit():
    cfg = load_config()
    cfg["PlayBalance"].update({"doubleSwitchPHAdjust": 100})
    bench = make_player("bench", ph=80)
    starter = make_player("start", ph=10)
    team = TeamState(lineup=[starter], bench=[bench], pitchers=[make_pitcher("p")])
    mgr = SubstitutionManager(cfg, MockRandom([0.0]))
    player = mgr.maybe_pinch_hit(team, 0, [])
    assert player.player_id == "bench"
    assert team.lineup[0].player_id == "bench"


def test_pinch_run():
    cfg = load_config()
    cfg["PlayBalance"].update({"pinchRunChance": 100})
    runner = make_player("slow", sp=10)
    fast = make_player("fast", sp=90)
    team = TeamState(lineup=[runner], bench=[fast], pitchers=[make_pitcher("p")])
    state = BatterState(runner)
    team.bases[0] = state
    team.lineup_stats[runner.player_id] = state
    mgr = SubstitutionManager(cfg, MockRandom([0.0]))
    mgr.maybe_pinch_run(team, log=[])
    assert team.bases[0].player.player_id == "fast"
    assert team.lineup[0].player_id == "fast"


def test_defensive_sub():
    cfg = load_config()
    cfg["PlayBalance"].update({"defSubChance": 100})
    weak = make_player("weak", gf=10)
    strong = make_player("strong", gf=90)
    team = TeamState(lineup=[weak], bench=[strong], pitchers=[make_pitcher("p")])
    mgr = SubstitutionManager(cfg, MockRandom([0.0]))
    mgr.maybe_defensive_sub(team, log=[])
    assert team.lineup[0].player_id == "strong"


def test_double_switch():
    cfg = load_config()
    cfg["PlayBalance"].update({"doubleSwitchChance": 100, "doubleSwitchPHAdjust": 100})
    bench_hitter = make_player("bench", ph=80)
    starter = make_player("start", ph=10)
    offense = TeamState(lineup=[starter], bench=[bench_hitter], pitchers=[make_pitcher("op")])
    defense = TeamState(
        lineup=[make_player("d")],
        bench=[],
        pitchers=[make_pitcher("p1", endurance=5), make_pitcher("p2")],
    )
    mgr = SubstitutionManager(cfg, MockRandom([0.0]))
    player = mgr.maybe_double_switch(offense, defense, 0, log=[])
    assert player.player_id == "bench"
    assert offense.lineup[0].player_id == "bench"
    assert defense.current_pitcher_state.player.player_id == "p2"


def test_change_pitcher():
    cfg = load_config()
    defense = TeamState(
        lineup=[make_player("d")],
        bench=[],
        pitchers=[make_pitcher("p1", endurance=5), make_pitcher("p2")],
    )
    mgr = SubstitutionManager(cfg, MockRandom([]))
    assert mgr.maybe_change_pitcher(defense, log=[])
    assert defense.current_pitcher_state.player.player_id == "p2"

