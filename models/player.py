from dataclasses import dataclass, field
from typing import Optional
from models.base_player import BasePlayer

@dataclass
class Player(BasePlayer):
    ch: int = 0
    ph: int = 0
    sp: int = 0
    pl: int = 0
    vl: int = 0
    sc: int = 0
    fa: int = 0
    arm: int = 0

    # Extended potential ratings
    pot_ch: int = 0
    pot_ph: int = 0
    pot_sp: int = 0
    pot_fa: int = 0
    pot_arm: int = 0
    pot_sc: int = 0
    pot_gf: int = 0  # Only if GF is part of your hitting model

    potential: dict = field(default_factory=dict)  # Optional legacy fallback
