# UBL Simulation

UBL (Ultimate Baseball League) Simulation is a Python project that models a small baseball league with a graphical interface.

## Features
- **PyQt6 interface:** run `main.py` to launch the login window and access administrative tools.
- **League management:** classes for players, teams, trades and rosters in `models/` with supporting services and UI dialogs.
- **Game simulation:** `logic/simulation.py` provides a minimal engine for at-bats, pitching changes and base running.
- **Data files:** example data lives in the `data/` directory including rosters, lineups and configuration values.

## Lineup CSV Format
Lineup files live in `data/lineups/` and are named `<TEAM>_vs_lhp.csv` or `<TEAM>_vs_rhp.csv`.
Each file contains the columns:

```csv
order,player_id,position
```

`player_id` uses the internal IDs such as `P1000`.

## Development
Install the dependencies (see `requirements.txt` if present) then run:

```bash
python main.py
```

### Running tests
Tests are located in the `tests/` directory and can be executed with:

```bash
pytest
```

