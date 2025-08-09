"""Utilities for generating random baseball team names.

This module exposes lists of plausible cities and mascots along with a
helper :func:`random_team` which returns a randomly selected
``(city, mascot)`` pair. The lists are intentionally short but can be
extended as needed and are primarily meant for demo data and quick UI
entry.
"""

import random
from typing import List, Tuple

# Lists of sample cities and mascots.
CITIES: List[str] = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
]

MASCOTS: List[str] = [
    "Bears",
    "Tigers",
    "Eagles",
    "Sharks",
    "Dragons",
    "Wolves",
    "Lions",
    "Hawks",
    "Rockets",
    "Pirates",
]

def random_team() -> Tuple[str, str]:
    """Return a random `(city, mascot)` pair.

    The city is drawn from :data:`CITIES` and the mascot from :data:`MASCOTS`.
    """

    return random.choice(CITIES), random.choice(MASCOTS)
