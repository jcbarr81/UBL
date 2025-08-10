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


def save_team_settings(team: Team, file_path="data/teams.csv") -> None:
    """Persist updates to a single team's stadium or colors.

    Reads the entire teams file, updates the matching team's fields and
    overwrites the CSV. Only the ``stadium`` and color fields are modified so
    other information remains unchanged.
    """

    teams = []
    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["team_id"] == team.team_id:
                row["stadium"] = team.stadium
                row["primary_color"] = team.primary_color
                row["secondary_color"] = team.secondary_color
            teams.append(row)

    fieldnames = [
        "team_id",
        "name",
        "city",
        "abbreviation",
        "division",
        "stadium",
        "primary_color",
        "secondary_color",
        "owner_id",
    ]
    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(teams)

