import os
import pytest
from utils.user_manager import load_users, add_user


def test_add_user(tmp_path):
    users_file = tmp_path / "users.txt"
    users_file.write_text("admin,pass,admin,\n")

    add_user("newuser", "pw", "owner", "LAX", file_path=str(users_file))

    users = load_users(str(users_file))
    assert any(u["username"] == "newuser" and u["team_id"] == "LAX" for u in users)


def test_duplicate_username(tmp_path):
    users_file = tmp_path / "users.txt"
    users_file.write_text("admin,pass,admin,\nuser1,pw,owner,LAX\n")

    with pytest.raises(ValueError):
        add_user("user1", "pw", "owner", "ARG", file_path=str(users_file))


def test_duplicate_team(tmp_path):
    users_file = tmp_path / "users.txt"
    users_file.write_text("admin,pass,admin,\nuser1,pw,owner,LAX\n")

    with pytest.raises(ValueError):
        add_user("user2", "pw", "owner", "LAX", file_path=str(users_file))
