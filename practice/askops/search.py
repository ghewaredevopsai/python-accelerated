"""Keyword search over runbooks. No AI yet - that arrives when AskOps gets an agent brain.

Mission 2: implement `search`. The tests in tests/test_m2_core.py are the spec.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from askops.store import Store

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Hit:
    runbook_id: str
    title: str
    score: int


def search(store: Store, query: str, limit: int = 5) -> list[Hit]:
    """Rank runbooks against a free-text query.

    * Iterate `store.runbooks()`.
    * Query words are compared case-insensitively; words shorter than 3 characters are ignored.
    * Score per runbook = 1 for each query word found in the title's words,
                          + 2 for each query word that is one of its tags.
    * Runbooks scoring 0 are left out. Sort by score, highest first; ties by runbook id.
    * Return at most `limit` hits.
    * A query with no usable words raises ValueError.
    * Log one DEBUG line: 'search q=%r hits=%d'.
    """
    raise NotImplementedError
