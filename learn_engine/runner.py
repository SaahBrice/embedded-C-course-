from __future__ import annotations

from .checkers import CheckerRegistry
from .models import Attempt, Mission, MissionResult


class MissionRunner:
    def __init__(self, registry: CheckerRegistry):
        self.registry = registry

    def test(
        self, mission: Mission, attempt: Attempt, *, include_advisory: bool = True
    ) -> MissionResult:
        selected = tuple(
            spec for spec in mission.checks if include_advisory or spec.required
        )
        results = tuple(self.registry.run(spec, attempt, mission) for spec in selected)
        passed = all(result.passed for spec, result in zip(selected, results) if spec.required)
        return MissionResult(passed=passed, checks=results)
