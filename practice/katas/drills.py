"""Mission 1 - AI-tutored drills.

Each function below is a small, real task an engineer does every week, written the way a
Python developer would write it. The tests in tests/test_m1_drills.py are the spec.

Rules for this mission:
  * Use Copilot in TUTOR mode (type /tutor in Copilot Chat). It will explain and hint,
    it will not write the answer for you. That is the point.
  * Turn off inline completions for this file while you drill (Copilot status bar icon), or you
    will be learning to press Tab, not Python.
  * Run one drill at a time:  python score.py 1

Replace each `raise NotImplementedError` with your implementation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path


# --- 1. Collections -------------------------------------------------------------------------

def word_counts(text: str) -> dict[str, int]:
    """Count words, case-insensitively. Words are separated by whitespace.

    >>> word_counts("Deploy deploy ROLLBACK")
    {'deploy': 2, 'rollback': 1}
    """
    raise NotImplementedError


def unique_services(incidents: list[dict]) -> list[str]:
    """The distinct `service` values across incidents, sorted alphabetically."""
    raise NotImplementedError


def high_severity_titles(incidents: list[dict]) -> list[str]:
    """Titles of incidents whose severity is "high", in their original order.

    Write it as ONE list comprehension.
    """
    raise NotImplementedError


def index_by_id(items: list[dict]) -> dict[str, dict]:
    """Map each item's "id" to the item. Write it as ONE dict comprehension."""
    raise NotImplementedError


def group_by_service(incidents: list[dict]) -> dict[str, list[str]]:
    """Map service -> list of incident ids, in original order."""
    raise NotImplementedError


# --- 2. Functions, defaults and truthiness --------------------------------------------------

def first_or_default(items, default=None):
    """The first element of any iterable, or `default` if it is empty.

    Must work on lists, tuples, generators and sets - not only on things with an index.
    """
    raise NotImplementedError


def add_tag(tag: str, tags=None) -> list[str]:
    """Return `tags` with `tag` appended. Calling it twice without `tags` must NOT share a list.

    The signature is deliberately `tags=None`. Ask your tutor why `tags=[]` would be a bug.
    """
    raise NotImplementedError


def display_name(user: dict) -> str:
    """The user's "name", or their "email" if name is missing OR empty, or "anonymous".

    Hint: in Python, "" and None and [] are all falsy.
    """
    raise NotImplementedError


# --- 3. Errors: ask forgiveness, not permission ---------------------------------------------

def parse_port(value: str) -> int:
    """Parse a TCP port. Raise ValueError("invalid port: <value>") if it is not an int in 1..65535."""
    raise NotImplementedError


def port_or_default(value: str, default: int = 8080) -> int:
    """Like parse_port, but return `default` instead of raising. Reuse parse_port."""
    raise NotImplementedError


# --- 4. Dataclasses -------------------------------------------------------------------------

@dataclass(frozen=True)
class Money:
    """A value object. Two Money instances with the same amount and currency are equal.

    `add` returns a NEW Money; adding different currencies raises ValueError.
    The class is frozen, so `m.amount = ...` must raise.
    """
    amount: Decimal
    currency: str

    def add(self, other: "Money") -> "Money":
        raise NotImplementedError


@dataclass
class Ticket:
    """A mutable record. Fix the two things the tests complain about:

    * every Ticket must get its OWN `watchers` list
    * priority must be 1..4, validated when the object is created
    """
    title: str
    priority: int = 3
    watchers: list[str] = None  # <- not right. What does dataclasses give you for this?

    def __post_init__(self) -> None:
        pass


# --- 5. Files -------------------------------------------------------------------------------

def read_nonblank_lines(path: str | Path) -> list[str]:
    """Lines of a text file, stripped, skipping blank lines and lines starting with '#'.

    The file must be closed afterwards, even if something fails - use `with`.
    """
    raise NotImplementedError
