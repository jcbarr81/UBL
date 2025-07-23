from dataclasses import dataclass, field
from typing import List, Optional
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
    potential: dict = field(default_factory=dict)
