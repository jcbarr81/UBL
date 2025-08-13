"""Expose core windows at the package level.

This module makes :class:`ScheduleWindow` and :class:`StandingsWindow`
available for convenient importing and to define the public UI API.
"""

from .schedule_window import ScheduleWindow  # noqa: F401
from .standings_window import StandingsWindow  # noqa: F401

__all__ = ["ScheduleWindow", "StandingsWindow"]
