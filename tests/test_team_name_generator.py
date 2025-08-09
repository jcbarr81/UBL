import random
from logic.team_name_generator import random_team, CITIES, MASCOTS

def test_random_team_returns_valid_members():
    random.seed(0)
    city, mascot = random_team()
    assert city in CITIES
    assert mascot in MASCOTS

def test_random_team_produces_variety():
    random.seed(1)
    results = {random_team() for _ in range(20)}
    assert len(results) > 1
