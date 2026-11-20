from dataclasses import dataclass
from typing import Literal

Level = Literal["medium", "low"]
Source = Literal["model", "check"]


@dataclass
class Flag:
    """A field that needs a look. Low must be reviewed before approval, medium is a warning."""

    field: str  # path like totals.total or lines[2].quantity
    level: Level
    source: Source
    reason: str

    @property
    def line_index(self) -> int | None:
        if self.field.startswith("lines["):
            return int(self.field[6 : self.field.index("]")])
        return None