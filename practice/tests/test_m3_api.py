"""Mission 3 - the acceptance criteria for docs/api-spec.md."""
import time


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok", "runbooks": 6}


def test_list_runbooks_filtered_by_service(client):
    body = client.get("/api/runbooks", params={"service": "auth"}).json()
    assert [r["id"] for r in body] == ["RB-201", "RB-202"]
    assert body[0]["tags"] == sorted(body[0]["tags"])
    assert body[0]["steps"][0] == "Check the token cache hit rate"


def test_get_runbook(client):
    r = client.get("/api/runbooks/RB-301")
    assert r.status_code == 200
    assert r.json()["title"] == "Nightly batch job did not finish"


def test_unknown_runbook_is_404_with_detail(client):
    r = client.get("/api/runbooks/RB-999")
    assert r.status_code == 404
    assert r.json() == {"detail": "runbook RB-999 not found"}


def test_list_incidents_newest_first(client):
    body = client.get("/api/incidents").json()
    assert [i["id"] for i in body] == ["INC-9003", "INC-9002", "INC-9001"]
    assert body[2]["runbook_id"] == "RB-101"


def test_create_incident(client):
    r = client.post("/api/incidents", json={"title": "Checkout errors", "severity": "high",
                                             "service": "payments", "runbook_id": "RB-101"})
    assert r.status_code == 201
    assert r.json()["id"] == "INC-9004"
    assert client.get("/api/incidents").json()[0]["id"] == "INC-9004"


def test_create_incident_validates_body(client):
    bad = [
        {"title": "no", "severity": "high", "service": "payments"},           # title too short
        {"title": "Checkout errors", "severity": "urgent", "service": "x"},  # not a Severity
        {"title": "Checkout errors", "severity": "high"},                      # service missing
    ]
    for body in bad:
        assert client.post("/api/incidents", json=body).status_code == 422, body


def test_create_incident_with_unknown_runbook_is_404(client):
    r = client.post("/api/incidents", json={"title": "Checkout errors", "severity": "high",
                                             "service": "payments", "runbook_id": "RB-000"})
    assert r.status_code == 404
    assert r.json() == {"detail": "runbook RB-000 not found"}


def test_ask_returns_runbooks_and_incidents(client):
    body = client.get("/api/ask", params={"q": "payments deploy rollback", "limit": 2}).json()
    assert body["query"] == "payments deploy rollback"
    assert body["runbooks"][0] == {"runbook_id": "RB-101", "title": "Payments API returns 502 after deploy",
                                   "score": 6}
    assert len(body["runbooks"]) <= 2
    assert [i["id"] for i in body["incidents"]] == ["INC-9001"]


def test_ask_rejects_short_query(client):
    assert client.get("/api/ask", params={"q": "db"}).status_code == 422
    assert client.get("/api/ask", params={"q": "a b c d"}).status_code == 422


def test_ask_consults_both_sources_concurrently(client):
    client.get("/api/ask", params={"q": "disk"})            # warm up
    start = time.perf_counter()
    assert client.get("/api/ask", params={"q": "disk"}).status_code == 200
    elapsed = time.perf_counter() - start
    assert elapsed < 0.35, f"/ask took {elapsed:.2f}s - are the two sources awaited one after the other?"
