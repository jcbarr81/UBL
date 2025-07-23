import csv
from models.team import Team

def load_teams(file_path="data/teams.csv"):
    teams = []
    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team = Team(
                team_id=row["team_id"],
                name=row["name"],
                city=row["city"],
                abbreviation=row["abbreviation"],
                division=row["division"],
                stadium=row["stadium"],
                primary_color=row["primary_color"],
                secondary_color=row["secondary_color"],
                owner_id=row["owner_id"]
            )
            teams.append(team)
    return teams
