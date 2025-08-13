import importlib
import ui.standings_window as standings_window


def test_standings_window_opens(dialog):
    importlib.reload(standings_window)
    window = dialog(standings_window.StandingsWindow)
    assert window.isVisible()
    assert window.windowTitle() == "Standings"
