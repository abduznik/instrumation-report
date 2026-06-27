from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .measurement import Measurement


@dataclass
class TestTable:
    title: str
    sub_number: str = ""
    measurements: List[Measurement] = field(default_factory=list)

    def add(self, measurement: Measurement) -> None:
        self.measurements.append(measurement)


@dataclass
class Section:
    number: str
    title: str
    subtitle: str = ""
    tables: List[TestTable] = field(default_factory=list)

    def add_table(self, table: TestTable) -> None:
        self.tables.append(table)
