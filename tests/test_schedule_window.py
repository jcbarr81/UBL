import importlib
import ui.schedule_window as schedule_window


def test_schedule_window_shows_table(dialog):
    importlib.reload(schedule_window)
    window = dialog(schedule_window.ScheduleWindow)
    assert window.isVisible()
    assert window.table.item(0, 0).text() == "2024-04-01"
    assert window.table.item(0, 1).text() == "Team A vs Team B"
