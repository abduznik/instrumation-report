from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Union

Condition = Union[Callable[[float], bool], tuple[float, float], float, None]


@dataclass
class Measurement:
    name: str
    value: float
    unit: str = ""
    condition: Condition = None
    test_number: str = ""
    expected: str = ""
    notes: str = ""
    description: str = ""

    def evaluate(self) -> Optional[bool]:
        if self.condition is None:
            return None
        if callable(self.condition):
            return bool(self.condition(self.value))
        if isinstance(self.condition, tuple):
            lo, hi = self.condition
            return lo <= self.value <= hi
        if isinstance(self.condition, (int, float)):
            return self.value >= float(self.condition)
        raise TypeError(f"Unsupported condition type: {type(self.condition)}")

    @property
    def status(self) -> str:
        r = self.evaluate()
        if r is True:
            return "PASS"
        if r is False:
            return "FAIL"
        return "N/A"
