import csv
from models.player import Player
from models.pitcher import Pitcher

def save_players_to_csv(players, file_path):
    fieldnames = [
        "player_id", "first_name", "last_name", "birthdate", "height", "weight", "bats",
        "primary_position", "other_positions", "is_pitcher",
        "ch", "ph", "sp", "gf", "pl", "vl", "sc", "fa", "arm",
        "endurance", "control", "hold_runner",
        "fb", "cu", "cb", "sl", "si", "scb", "kn",
        "pot_ch", "pot_ph", "pot_sp", "pot_gf", "pot_pl", "pot_vl", "pot_sc", "pot_fa", "pot_arm",
        "pot_control", "pot_endurance", "pot_hold_runner",
        "pot_fb", "pot_cu", "pot_cb", "pot_sl", "pot_si", "pot_scb", "pot_kn",
        "injured", "injury_description", "return_date"
    ]

    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for p in players:
            is_pitcher = isinstance(p, Pitcher)
            row = {
                "player_id": p.player_id,
                "first_name": p.first_name,
                "last_name": p.last_name,
                "birthdate": p.birthdate,
                "height": p.height,
                "weight": p.weight,
                "bats": p.bats,
                "primary_position": p.primary_position,
                "other_positions": "|".join(p.other_positions),
                "is_pitcher": str(is_pitcher),
                "injured": str(p.injured),
                "injury_description": p.injury_description or "",
                "return_date": p.return_date or ""
            }

            if is_pitcher:
                row.update({
                    "gf": p.gf,
                    "endurance": p.endurance,
                    "control": p.control,
                    "hold_runner": p.hold_runner,
                    "fb": p.fb, "cu": p.cu, "cb": p.cb, "sl": p.sl,
                    "si": p.si, "scb": p.scb, "kn": p.kn,
                    "pot_gf": p.potential.get("gf", p.gf),
                    "pot_control": p.potential.get("control", p.control),
                    "pot_endurance": p.potential.get("endurance", p.endurance),
                    "pot_hold_runner": p.potential.get("hold_runner", p.hold_runner),
                    "pot_fb": p.potential.get("fb", p.fb),
                    "pot_cu": p.potential.get("cu", p.cu),
                    "pot_cb": p.potential.get("cb", p.cb),
                    "pot_sl": p.potential.get("sl", p.sl),
                    "pot_si": p.potential.get("si", p.si),
                    "pot_scb": p.potential.get("scb", p.scb),
                    "pot_kn": p.potential.get("kn", p.kn),
                    "pot_arm": p.potential.get("arm", p.arm),
                    "pot_fa": p.potential.get("fa", p.fa)
                })
            else:
                row.update({
                    "ch": p.ch, "ph": p.ph, "sp": p.sp,
                    "gf": p.gf, "pl": p.pl, "vl": p.vl, "sc": p.sc,
                    "fa": p.fa, "arm": p.arm,
                    "pot_ch": p.potential.get("ch", p.ch),
                    "pot_ph": p.potential.get("ph", p.ph),
                    "pot_sp": p.potential.get("sp", p.sp),
                    "pot_gf": p.potential.get("gf", p.gf),
                    "pot_pl": p.potential.get("pl", p.pl),
                    "pot_vl": p.potential.get("vl", p.vl),
                    "pot_sc": p.potential.get("sc", p.sc),
                    "pot_fa": p.potential.get("fa", p.fa),
                    "pot_arm": p.potential.get("arm", p.arm)
                })

            writer.writerow(row)
