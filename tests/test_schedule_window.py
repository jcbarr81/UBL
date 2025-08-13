"""Tests for the placeholder schedule dialog."""

import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import tests.util.qt_stubs  # noqa: F401

from ui import schedule_window


def test_schedule_window_creation(dialog_opener):
    dialog = dialog_opener(schedule_window.ScheduleWindow)
    assert dialog.table.item(0, 0).text() == "2024-04-01"
    assert dialog.table.item(0, 1).text() == "Team A vs Team B"
