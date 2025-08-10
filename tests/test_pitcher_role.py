import pytest

from models.pitcher import Pitcher
from utils.pitcher_role import get_role, ENDURANCE_THRESHOLD


def make_pitcher(**kwargs):
    defaults = dict(
        player_id="p1",
        first_name="A",
        last_name="B",
        birthdate="2000-01-01",
        height=70,
        weight=180,
        bats="R",
        primary_position="P",
        other_positions=[],
        gf=0,
        endurance=50,
        control=0,
        movement=0,
        hold_runner=0,
        role="",
    )
    defaults.update(kwargs)
    return Pitcher(**defaults)


def test_explicit_role_overrides_primary_and_endurance():
    p = make_pitcher(role="SP", primary_position="RP", endurance=0)
    assert get_role(p) == "SP"


def test_primary_position_used_when_role_missing():
    p = make_pitcher(primary_position="RP")
    assert get_role(p) == "RP"


def test_endurance_high_yields_sp():
    p = make_pitcher(endurance=ENDURANCE_THRESHOLD + 1)
    assert get_role(p) == "SP"


def test_endurance_low_yields_rp():
    p = make_pitcher(endurance=ENDURANCE_THRESHOLD)
    assert get_role(p) == "RP"


def test_returns_empty_for_non_pitcher():
    hitter = {"primary_position": "CF"}
    assert get_role(hitter) == ""


def test_accepts_dict_objects():
    pdata = {"role": "RP", "endurance": 10, "primary_position": "P"}
    assert get_role(pdata) == "RP"
