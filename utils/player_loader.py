import csv
from models.player import Player
from models.pitcher import Pitcher

def load_players_from_csv(file_path):
    players = []
    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            is_pitcher = row["is_pitcher"].lower() == "true"

            common_kwargs = {
                "player_id": row["player_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "birthdate": row["birthdate"],
                "height": int(row["height"]),
                "weight": int(row["weight"]),
                "bats": row["bats"],
                "primary_position": row["primary_position"],
                "other_positions": row["other_positions"].split("|") if row["other_positions"] else [],
                "gf": int(row["gf"]),
                "injured": row["injured"].lower() == "true",
                "injury_description": row["injury_description"] or None,
                "return_date": row["return_date"] or None
            }

            if is_pitcher:
                player = Pitcher(
                    **common_kwargs,
                    endurance=int(row["endurance"]),
                    control=int(row["control"]),
                    hold_runner=int(row["hold_runner"]),
                    fb=int(row["fb"]),
                    cu=int(row["cu"]),
                    cb=int(row["cb"]),
                    sl=int(row["sl"]),
                    si=int(row["si"]),
                    scb=int(row["scb"]),
                    kn=int(row["kn"]),
                    potential={
                        "gf": int(row["pot_gf"]) if row["pot_gf"] else int(row["gf"])
                    }
                )
            else:
                player = Player(
                    **common_kwargs,
                    ch=int(row["ch"]),
                    ph=int(row["ph"]),
                    sp=int(row["sp"]),
                    pl=int(row["pl"]),
                    vl=int(row["vl"]),
                    sc=int(row["sc"]),
                    fa=int(row["fa"]),
                    arm=int(row["arm"]),
                    potential={
                        "ch": int(row["pot_ch"]),
                        "ph": int(row["pot_ph"]),
                        "sp": int(row["pot_sp"]),
                        "gf": int(row["pot_gf"]),
                        "pl": int(row["pot_pl"]),
                        "vl": int(row["pot_vl"]),
                        "sc": int(row["pot_sc"]),
                        "fa": int(row["pot_fa"]),
                        "arm": int(row["pot_arm"]),
                    }
                )

            players.append(player)
    return players
