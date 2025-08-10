from datetime import date
import random

from logic.player_generator import generate_player, assign_primary_position


def test_generate_player_respects_age_range():
    age_range = (30, 35)
    player = generate_player(is_pitcher=False, age_range=age_range)
    age = (date.today() - player["birthdate"]).days // 365
    assert age_range[0] <= age <= age_range[1]


def test_primary_position_override():
    # Establish what random selection would yield with this seed
    random.seed(0)
    random_choice = assign_primary_position()
    assert random_choice != "SS"
    # Reset seed so generate_player would have chosen the same random position
    random.seed(0)
    player = generate_player(is_pitcher=False, primary_position="SS")
    assert player["primary_position"] == "SS"
