import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Install minimal PyQt stubs before importing UI modules
import tests.util.qt_stubs  # noqa: F401

from ui import standings_window


def test_standings_window_creation(dialog_opener):
    dialog = dialog_opener(standings_window.StandingsWindow)
    assert dialog is not None
