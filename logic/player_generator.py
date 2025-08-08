# ARR-inspired Player Generator Script
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
# pandas is optional; fall back to simple names if unavailable
try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - handled by fallback
    pd = None
import os

# Constants
base_dir = os.path.dirname(os.path.abspath(__file__))
NAME_PATH = os.path.join(base_dir, "..", "data", "names.csv")
if pd is not None and os.path.exists(NAME_PATH):
    name_df = pd.read_csv(NAME_PATH)
    grouped_names = name_df.groupby("ethnicity")
else:  # pragma: no cover - fallback when pandas or file missing
    grouped_names = None

    
# Helper Functions

def generate_birthdate(age_range=(18, 38)):
    today = datetime.today()
    age = random.randint(*age_range)
    days_old = age * 365 + random.randint(0, 364)
    birthdate = (today - timedelta(days=days_old)).date()
    return birthdate, age

def bounded_rating(min_val=10, max_val=99):
    return random.randint(min_val, max_val)

def bounded_potential(actual, age):
    if age < 22:
        pot = actual + random.randint(10, 30)
    elif age < 28:
        pot = actual + random.randint(5, 15)
    elif age < 32:
        pot = actual + random.randint(-5, 5)
    else:
        pot = actual - random.randint(0, 10)
    return max(10, min(99, pot))

def generate_name() -> tuple[str, str]:
    if grouped_names is not None:
        ethnicity = random.choice(list(grouped_names.groups.keys()))
        subset = grouped_names.get_group(ethnicity)
        row = subset.sample(1).iloc[0]
        return row["first_name"], row["last_name"]
    else:
        return "John", "Doe"

def assign_primary_position():
    weights = {
        "C": 10, "1B": 10, "2B": 12, "3B": 10,
        "SS": 12, "LF": 12, "CF": 12, "RF": 12
    }
    return random.choices(list(weights.keys()), weights=weights.values())[0]

def assign_secondary_positions(primary):
    weights = {
        "C": 10, "1B": 10, "2B": 12, "3B": 10,
        "SS": 12, "LF": 12, "CF": 12, "RF": 12
    }
    return "|".join(
        random.sample([pos for pos in weights if pos != primary], k=random.choice([0, 1, 2]))
    )

def generate_pitches(bats: str, role: str, age: int):
    base_pitches = ["fb", "cu", "cb", "sl", "si"]
    rare_pitches = []
    if bats == "L" and random.random() < 0.10:
        rare_pitches.append("scb")
    if random.random() < 0.02:
        rare_pitches.append("kn")

    count = random.choices([2, 3, 4], weights=(0.1, 0.7, 0.2) if role == "SP" else (0.7, 0.2, 0.1))[0]
    selected = ["fb"]
    pool = list(set(base_pitches) - {"fb"})
    random.shuffle(pool)
    selected.extend(pool[:count - len(selected)])

    if len(selected) < count and rare_pitches:
        selected.append(random.choice(rare_pitches))

    all_pitches = base_pitches + ["scb", "kn"]
    ratings = {p: bounded_rating() if p in selected else 0 for p in all_pitches}
    potentials = {f"pot_{p}": bounded_potential(ratings[p], age) if p in selected else 0 for p in all_pitches}
    return ratings, potentials

def generate_player(is_pitcher: bool, for_draft: bool = False) -> Dict:
    birthdate, age = generate_birthdate((17, 21) if for_draft else (18, 38))
    first_name, last_name = generate_name()
    player_id = f"P{random.randint(1000, 9999)}"
    bats = random.choice(["L", "R", "S"])
    height = random.randint(68, 78)
    weight = random.randint(160, 250)

    if is_pitcher:
        role = random.choice(["SP", "RP"])
        delivery = random.choice(["overhand", "sidearm"])
        arm = bounded_rating()
        fa = bounded_rating()
        control = bounded_rating()
        endurance = bounded_rating()
        hold_runner = bounded_rating()
        pitch_ratings, pitch_pots = generate_pitches(bats, role, age)

        player = {
            "first_name": first_name,
            "last_name": last_name,
            "injured": 0,
            "injury_description": 0,
            "return_date": 0,
            "player_id": player_id,
            "is_pitcher": True,
            "birthdate": birthdate,
            "bats": bats,
            "arm": arm,
            "fa": fa,
            "control": control,
            "endurance": endurance,
            "hold_runner": hold_runner,
            "role": role,
            "delivery": delivery,
            "height": height,
            "weight": weight,
            "primary_position": "P",
            "other_positions": "",
            "pot_control": bounded_potential(control, age),
            "pot_endurance": bounded_potential(endurance, age),
            "pot_hold_runner": bounded_potential(hold_runner, age),
            "pot_arm": bounded_potential(arm, age),
            "pot_fa": bounded_potential(fa, age),
        }
        player.update(pitch_ratings)
        player.update(pitch_pots)
        for key in list(pitch_ratings.keys()) + list(pitch_pots.keys()):
            player.setdefault(key, 0)
        return player

    else:
        ch = bounded_rating()
        ph = bounded_rating()
        sp = bounded_rating()
        gf = bounded_rating()
        pl = bounded_rating()
        vl = bounded_rating()
        sc = bounded_rating()
        fa = bounded_rating()
        arm = bounded_rating()
        primary_pos = assign_primary_position()
        other_pos = assign_secondary_positions(primary_pos)

        player = {
            "first_name": first_name,
            "last_name": last_name,
            "injured": 0,
            "injury_description": 0,
            "return_date": 0,
            "player_id": player_id,
            "is_pitcher": False,
            "birthdate": birthdate,
            "bats": bats,
            "ch": ch,
            "ph": ph,
            "sp": sp,
            "gf": gf,
            "pl": pl,
            "vl": vl,
            "sc": sc,
            "fa": fa,
            "arm": arm,
            "height": height,
            "weight": weight,
            "primary_position": primary_pos,
            "other_positions": other_pos,
            "pot_ch": bounded_potential(ch, age),
            "pot_ph": bounded_potential(ph, age),
            "pot_sp": bounded_potential(sp, age),
            "pot_fa": bounded_potential(fa, age),
            "pot_arm": bounded_potential(arm, age),
            "pot_sc": sc,
            "pot_gf": gf
        }
        all_keys = ["ch", "ph", "sp", "gf", "pl", "vl", "sc", "fa", "arm",
                     "pot_ch", "pot_ph", "pot_sp", "pot_fa", "pot_arm", "pot_sc", "pot_gf"]
        for key in all_keys:
            player.setdefault(key, 0)

        return player


def generate_draft_pool(num_players: int = 75) -> List[Dict]:
    players = []
    for _ in range(num_players):
        is_pitcher = random.random() < 0.45  # roughly 45% pitchers, 55% hitters
        players.append(generate_player(is_pitcher=is_pitcher, for_draft=True))
    # Ensure all players have all keys filled
    all_keys = set(k for player in players for k in player.keys())
    for player in players:
        for key in all_keys:
            player.setdefault(key, 0)

    return players

if __name__ == "__main__":
    draft_pool = generate_draft_pool()
    df = pd.DataFrame(draft_pool)
    df.to_csv("draft_pool.csv", index=False)
    print(f"Draft pool of {len(draft_pool)} players saved to draft_pool.csv")
