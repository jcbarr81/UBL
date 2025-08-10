import os
from typing import List, Dict


def load_users(file_path: str = "data/users.txt") -> List[Dict[str, str]]:
    """Load users from a CSV-like text file.

    Each line in the file should have the format:
    username,password,role,team_id
    """
    users: List[Dict[str, str]] = []
    if not os.path.exists(file_path):
        return users

    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            username, password, role, team_id = parts
            users.append(
                {
                    "username": username,
                    "password": password,
                    "role": role,
                    "team_id": team_id,
                }
            )
    return users


def add_user(
    username: str,
    password: str,
    role: str,
    team_id: str = "",
    file_path: str = "data/users.txt",
) -> None:
    """Add a new user to the users file.

    Raises:
        ValueError: If the username already exists or the team is already
        managed by another owner.
    """
    username = username.strip()
    password = password.strip()
    role = role.strip()
    team_id = team_id.strip()

    users = load_users(file_path)

    if any(u["username"] == username for u in users):
        raise ValueError("Username already exists")

    if role == "owner" and team_id:
        if any(u["role"] == "owner" and u["team_id"] == team_id for u in users):
            raise ValueError("Team already has an owner")

    with open(file_path, "a") as f:
        f.write(f"{username},{password},{role},{team_id}\n")


def clear_users(file_path: str = "data/users.txt") -> None:
    """Remove all user accounts by deleting the users file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
