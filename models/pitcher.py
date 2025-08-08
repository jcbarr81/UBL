from dataclasses import dataclass, field
from models.base_player import BasePlayer

@dataclass
class Pitcher(BasePlayer):
    endurance: int = 0
    control: int = 0
    hold_runner: int = 0

    fb: int = 0
    cu: int = 0
    cb: int = 0
    sl: int = 0
    si: int = 0
    scb: int = 0
    kn: int = 0

    # Core physical/fielding ratings
    arm: int = 0
    fa: int = 0

    # Extended potential ratings
    pot_control: int = 0
    pot_endurance: int = 0
    pot_hold_runner: int = 0

    pot_fb: int = 0
    pot_cu: int = 0
    pot_cb: int = 0
    pot_sl: int = 0
    pot_si: int = 0
    pot_scb: int = 0
    pot_kn: int = 0

    pot_arm: int = 0
    pot_fa: int = 0

    potential: dict = field(default_factory=dict)  # Optional legacy fallback
