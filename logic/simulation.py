from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from models.player import Player
from models.pitcher import Pitcher


@dataclass
class BatterState:
    """Tracks state and statistics for a batter during the game."""

    player: Player
    at_bats: int = 0
    hits: int = 0
    steals: int = 0


@dataclass
class PitcherState:
    """Tracks state for a pitcher."""

    player: Pitcher
    pitches_thrown: int = 0


@dataclass
class TeamState:
    """Mutable state for a team during a game."""

    lineup: List[Player]
    bench: List[Player]
    pitchers: List[Pitcher]
    lineup_stats: Dict[str, BatterState] = field(default_factory=dict)
    pitcher_stats: Dict[str, PitcherState] = field(default_factory=dict)
    batting_index: int = 0
    bases: List[Optional[BatterState]] = field(default_factory=lambda: [None, None, None])

    def __post_init__(self) -> None:
        if self.pitchers:
            starter = self.pitchers[0]
            state = PitcherState(starter)
            self.pitcher_stats[starter.player_id] = state
            self.current_pitcher_state = state
        else:
            self.current_pitcher_state = None


class GameSimulation:
    """A very small game simulation used for tests.

    The goal of this module is not to be feature complete, but to provide
    a minimal game loop that can reason about innings, at-bats and simple
    strategies such as pinch hitting, stealing and pitching changes.  The
    behaviour is heavily driven by values from the parsed PB.INI file so
    that tests can verify that configuration is respected.
    """

    def __init__(
        self,
        home: TeamState,
        away: TeamState,
        pbini: Dict[str, Dict[str, int]],
        rng: Optional[random.Random] = None,
    ) -> None:
        self.home = home
        self.away = away
        self.config = pbini.get("PlayBalance", {})
        self.rng = rng or random.Random()

    # ------------------------------------------------------------------
    # Core loop helpers
    # ------------------------------------------------------------------
    def simulate_game(self, innings: int = 9) -> None:
        """Simulate ``innings`` innings.

        Only very small parts of a real baseball game are modelled – enough to
        exercise decision making paths for the tests.
        """

        for _ in range(innings):
            self._play_half(self.away, self.home)  # Top half
            self._play_half(self.home, self.away)  # Bottom half

    def _play_half(self, offense: TeamState, defense: TeamState) -> None:
        outs = 0
        while outs < 3:
            outs += self.play_at_bat(offense, defense)
        offense.bases = [None, None, None]

    def play_at_bat(self, offense: TeamState, defense: TeamState) -> int:
        """Play a single at-bat.  Returns the number of outs recorded."""

        self._maybe_change_pitcher(defense)

        batter_idx = offense.batting_index % len(offense.lineup)
        batter = self._maybe_pinch_hit(offense, batter_idx)
        offense.batting_index += 1

        batter_state = offense.lineup_stats.setdefault(
            batter.player_id, BatterState(batter)
        )
        pitcher_state = defense.current_pitcher_state
        if pitcher_state is None:
            raise RuntimeError("Defense has no available pitcher")

        pitcher_state.pitches_thrown += 1
        batter_state.at_bats += 1

        outs = 0
        if self._swing_result(batter, pitcher_state.player):
            batter_state.hits += 1
            self._advance_runners(offense, batter_state)
            steal_result = self._attempt_steal(offense, pitcher_state.player)
            if steal_result is False:  # Runner thrown out
                outs += 1
        else:
            outs += 1

        return outs

    # ------------------------------------------------------------------
    # Pinch hitting
    # ------------------------------------------------------------------
    def _maybe_pinch_hit(self, team: TeamState, idx: int) -> Player:
        if not team.bench:
            return team.lineup[idx]
        chance = self.config.get("doubleSwitchPHAdjust", 0) / 100.0
        starter = team.lineup[idx]
        best = max(team.bench, key=lambda p: p.ph, default=None)
        if best and best.ph > starter.ph and self.rng.random() < chance:
            team.bench.remove(best)
            team.lineup[idx] = best
            return best
        return starter

    # ------------------------------------------------------------------
    # Swing outcome
    # ------------------------------------------------------------------
    def _swing_result(self, batter: Player, pitcher: Pitcher) -> bool:
        base = self.config.get("swingSpeedBase", 50)
        pct = self.config.get("swingSpeedPHPct", 0)
        swing_speed = base + pct * batter.ph / 100.0
        hit_prob = max(0.0, min(0.95, swing_speed / 100.0))
        return self.rng.random() < hit_prob

    def _advance_runners(self, team: TeamState, batter_state: BatterState) -> None:
        b = team.bases
        if b[2]:
            b[2] = None
        if b[1]:
            b[2] = b[1]
            b[1] = None
        if b[0]:
            b[1] = b[0]
        b[0] = batter_state

    # ------------------------------------------------------------------
    # Steal attempts
    # ------------------------------------------------------------------
    def _steal_chance(self, runner: Player, pitcher: Pitcher) -> float:
        cfg = self.config
        base = cfg.get("offManStealChancePct", 0) / 100.0
        sp = runner.sp
        if sp <= cfg.get("stealChanceVerySlowThresh", 0):
            adjust = cfg.get("stealChanceVerySlowAdjust", 0)
        elif sp <= cfg.get("stealChanceSlowThresh", 0):
            adjust = cfg.get("stealChanceSlowAdjust", 0)
        elif sp <= cfg.get("stealChanceMedThresh", 0):
            adjust = cfg.get("stealChanceMedAdjust", 0)
        elif sp <= cfg.get("stealChanceFastThresh", 0):
            adjust = cfg.get("stealChanceFastAdjust", 0)
        else:
            adjust = cfg.get("stealChanceVeryFastAdjust", 0)
        chance = base + adjust / 100.0
        return max(0.0, min(1.0, chance))

    def _attempt_steal(self, offense: TeamState, pitcher: Pitcher) -> Optional[bool]:
        runner_state = offense.bases[0]
        if not runner_state:
            return None
        chance = self._steal_chance(runner_state.player, pitcher)
        if self.rng.random() < chance:
            success_prob = 0.7
            if self.rng.random() < success_prob:
                offense.bases[0] = None
                offense.bases[1] = runner_state
                runner_state.steals += 1
                return True
            offense.bases[0] = None
            return False
        return None

    # ------------------------------------------------------------------
    # Pitching changes
    # ------------------------------------------------------------------
    def _maybe_change_pitcher(self, defense: TeamState) -> None:
        state = defense.current_pitcher_state
        if state is None:
            return
        remaining = state.player.endurance - state.pitches_thrown
        thresh = self.config.get("pitcherTiredThresh", 0)
        if remaining <= thresh and len(defense.pitchers) > 1:
            defense.pitchers.pop(0)
            new_pitcher = defense.pitchers[0]
            state = defense.pitcher_stats.setdefault(
                new_pitcher.player_id, PitcherState(new_pitcher)
            )
            defense.current_pitcher_state = state


__all__ = [
    "BatterState",
    "PitcherState",
    "TeamState",
    "GameSimulation",
]
