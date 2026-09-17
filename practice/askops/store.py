"""An in-memory store loaded from JSON files.

Mission 2: finish the TODOs. The tests in tests/test_m2_core.py are the spec.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from askops.models import Incident, Runbook, Severity

logger = logging.getLogger(__name__)


class Store:
    def __init__(self, runbooks: dict[str, Runbook], incidents: list[Incident]) -> None:
        self._runbooks = runbooks
        self._incidents = incidents

    @classmethod
    def from_dir(cls, data_dir: str | Path) -> Store:
        data_dir = Path(data_dir)
        runbooks = {rb.id: rb for rb in map(Runbook.from_dict, _read_json(data_dir / "runbooks.json"))}

        # TODO(mission 2): load incidents.json into Incident objects.
        # A record that cannot be parsed (bad severity, missing field, bad date) must NOT stop the
        # service from starting: skip it and log a WARNING that names the record's id.
        incidents: list[Incident] = []

        logger.info("loaded %d runbooks and %d incidents from %s", len(runbooks), len(incidents), data_dir)
        return cls(runbooks, incidents)

    def runbooks(self, service: str | None = None) -> list[Runbook]:
        """All runbooks, sorted by id, optionally only one service's."""
        return sorted(
            (rb for rb in self._runbooks.values() if service is None or rb.service == service),
            key=lambda rb: rb.id,
        )

    def get_runbook(self, runbook_id: str) -> Runbook:
        # TODO(mission 2): return the runbook, or raise RunbookNotFound.
        raise NotImplementedError

    def incidents(self) -> list[Incident]:
        # TODO(mission 2): newest first (by opened_at). Return a new list - callers must not be
        # able to change the store by mutating what you return.
        raise NotImplementedError

    def add_incident(
        self, title: str, severity: Severity, service: str, runbook_id: str | None = None
    ) -> Incident:
        # TODO(mission 2): create, store and return an Incident.
        #   * id is "INC-" + (highest existing number + 1), e.g. INC-9004 after INC-9003
        #   * opened_at is now
        #   * an unknown runbook_id raises RunbookNotFound
        raise NotImplementedError


def _read_json(path: Path) -> list[dict]:
    # TODO(mission 2): turn a missing file or invalid JSON into DataError, naming the path.
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
