"""Mission 2 - the spec for askops/errors.py, askops/store.py and askops/search.py."""
import json
import logging

import pytest

from askops import errors
from askops.models import Severity
from askops.search import search
from askops.store import Store


def test_get_runbook(store):
    assert store.get_runbook("RB-201").service == "auth"


def test_missing_runbook_raises_domain_error(store):
    with pytest.raises(errors.AskOpsError) as info:
        store.get_runbook("RB-999")
    assert isinstance(info.value, errors.RunbookNotFound)
    assert info.value.runbook_id == "RB-999"
    assert "RB-999" in str(info.value)


def test_incidents_loaded_newest_first(store):
    assert [i.id for i in store.incidents()] == ["INC-9003", "INC-9002", "INC-9001"]
    assert store.incidents()[0].severity is Severity.LOW


def test_incidents_returns_a_copy(store):
    store.incidents().clear()
    assert len(store.incidents()) == 3


def test_bad_incident_is_skipped_and_logged(tmp_path, caplog):
    (tmp_path / "runbooks.json").write_text("[]")
    (tmp_path / "incidents.json").write_text(json.dumps([
        {"id": "INC-1", "title": "ok", "severity": "low", "service": "a", "opened_at": "2026-09-01T10:00:00"},
        {"id": "INC-2", "title": "bad", "severity": "apocalyptic", "service": "a", "opened_at": "2026-09-01T10:00:00"},
    ]))
    with caplog.at_level(logging.WARNING, logger="askops.store"):
        s = Store.from_dir(tmp_path)
    assert [i.id for i in s.incidents()] == ["INC-1"]
    assert any("INC-2" in r.getMessage() and r.levelno == logging.WARNING for r in caplog.records)


def test_missing_file_raises_data_error_naming_the_path(tmp_path):
    with pytest.raises(errors.DataError, match="runbooks.json"):
        Store.from_dir(tmp_path)


def test_invalid_json_raises_data_error(tmp_path):
    (tmp_path / "runbooks.json").write_text("[{not json")
    with pytest.raises(errors.DataError, match="runbooks.json"):
        Store.from_dir(tmp_path)


def test_add_incident_assigns_next_id(store):
    inc = store.add_incident("Checkout errors", Severity.HIGH, "payments", runbook_id="RB-101")
    assert inc.id == "INC-9004"
    assert store.incidents()[0].id == "INC-9004"


def test_add_incident_with_unknown_runbook_raises(store):
    with pytest.raises(errors.RunbookNotFound):
        store.add_incident("Checkout errors", Severity.HIGH, "payments", runbook_id="RB-000")
    assert len(store.incidents()) == 3


def test_search_ranks_tags_above_title_words(store):
    hits = search(store, "rollback after deploy")
    assert hits[0].runbook_id == "RB-101"
    assert hits[0].score == 6   # "after", "deploy" in title (1 + 1) + tags "deploy", "rollback" (2 + 2)


def test_search_is_case_insensitive_and_ignores_short_words(store):
    assert search(store, "LOGIN is up") == search(store, "login")


def test_search_respects_limit(store):
    assert len(search(store, "timeout")) == 2
    assert len(search(store, "timeout", limit=1)) == 1


def test_search_without_usable_words_raises(store):
    with pytest.raises(ValueError):
        search(store, "  a to ")


def test_search_logs_a_debug_line(store, caplog):
    with caplog.at_level(logging.DEBUG, logger="askops.search"):
        search(store, "disk")
    assert any("hits=1" in r.getMessage() for r in caplog.records)
