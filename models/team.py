from dataclasses import dataclass, field
from typing import List

@dataclass
class Team:
    team_id: str
    name: str
    city: str
    abbreviation: str
    division: str
    stadium: str
    primary_color: str
    secondary_color: str
    owner_id: str

    act_roster: List[str] = field(default_factory=list)
    aaa_roster: List[str] = field(default_factory=list)
    low_roster: List[str] = field(default_factory=list)
