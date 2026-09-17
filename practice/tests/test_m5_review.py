"""Mission 5 - the failure contract at the bottom of docs/api-spec.md."""
import logging

import pytest

from askops import errors
from askops.store import Store


class WikiDown(Store):
    """A store whose runbook source is unreachable."""

    def runbooks(self, service=None):
        raise errors.DataError("wiki timed out after 30s")


@pytest.fixture
def broken_client(client, store):
    from askops.app import app
    from askops.deps import get_store

    broken = WikiDown(store._runbooks, store._incidents)
    app.dependency_overrides[get_store] = lambda: broken
    return client


def test_ask_is_503_when_a_source_fails(broken_client):
    r = broken_client.get("/api/ask", params={"q": "deploy"})
    assert r.status_code == 503, f"got {r.status_code} - an empty 200 here tells on-call there is no runbook"
    assert r.json() == {"detail": "search unavailable"}


def test_ask_failure_is_logged_with_the_cause(broken_client, caplog):
    with caplog.at_level(logging.ERROR):
        broken_client.get("/api/ask", params={"q": "deploy"})
    errors = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert errors, "nothing was logged at ERROR"
    assert any(r.exc_info for r in errors), "log it with the exception attached (logger.exception)"


def test_empty_result_still_means_nothing_matched(client):
    r = client.get("/api/ask", params={"q": "kubernetes quota"})
    assert r.status_code == 200
    assert r.json()["runbooks"] == []


def test_a_bug_is_not_disguised_as_unavailable(client, store):
    from askops.app import app
    from askops.deps import get_store

    class Buggy(Store):
        def runbooks(self, service=None):
            raise TypeError("a genuine bug")

    app.dependency_overrides[get_store] = lambda: Buggy(store._runbooks, store._incidents)
    with pytest.raises(TypeError):
        client.get("/api/ask", params={"q": "deploy"})
