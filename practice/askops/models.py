"""Domain records. This file is complete - READ it before you change anything else.

Things worth noticing if you come from Java, C# or TypeScript:
  * @dataclass writes __init__, __repr__ and __eq__ for you, from the type-annotated fields.
  * frozen=True makes an instance immutable (a value object); slots=True saves memory.
  * StrEnum members ARE strings, so they compare equal to "high" and serialise as JSON cleanly.
  * `from_dict` is a classmethod: an alternative constructor, the Python stand-in for overloading.
  * Type hints are not enforced at runtime. Nothing stops Runbook(id=42). Validation is your job,
    or pydantic's (mission 3).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class Runbook:
    id: str
    title: str
    service: str
    steps: tuple[str, ...]
    tags: frozenset[str]

    @classmethod
    def from_dict(cls, raw: dict) -> Runbook:
        return cls(
            id=raw["id"],
            title=raw["title"],
            service=raw["service"],
            steps=tuple(raw.get("steps", ())),
            tags=frozenset(t.lower() for t in raw.get("tags", ())),
        )


@dataclass(slots=True)
class Incident:
    id: str
    title: str
    severity: Severity
    service: str
    opened_at: datetime
    runbook_id: str | None = None

    @classmethod
    def from_dict(cls, raw: dict) -> Incident:
        return cls(
            id=raw["id"],
            title=raw["title"],
            severity=Severity(raw["severity"]),          # ValueError on an unknown severity
            service=raw["service"],
            opened_at=datetime.fromisoformat(raw["opened_at"]),
            runbook_id=raw.get("runbook_id"),
        )
