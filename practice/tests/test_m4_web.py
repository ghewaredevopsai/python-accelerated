"""Mission 4 - the spec for docs/web-spec.md."""

FORM = {"title": "Checkout errors", "severity": "high", "service": "payments"}


def test_home_page_is_html_with_the_htmx_forms(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert 'hx-get="/ui/ask"' in r.text
    assert 'hx-post="/ui/incidents"' in r.text
    assert 'id="incident-rows"' in r.text
    assert "/static/htmx.min.js" in r.text


def test_home_page_lists_incidents_newest_first(client):
    text = client.get("/").text
    assert text.index("INC-9003") < text.index("INC-9002") < text.index("INC-9001")


def test_htmx_is_served_locally(client):
    r = client.get("/static/htmx.min.js")
    assert r.status_code == 200 and "htmx" in r.text


def test_ui_ask_returns_a_fragment_with_hits_and_steps(client):
    r = client.get("/ui/ask", params={"q": "deploy rollback"})
    assert r.status_code == 200
    assert "<html" not in r.text.lower()
    assert "Payments API returns 502 after deploy" in r.text
    assert "Roll back with the release tool" in r.text
    assert "<ol" in r.text


def test_ui_ask_escapes_the_query(client):
    r = client.get("/ui/ask", params={"q": "<script>alert(1)</script> deploy"})
    assert "<script>alert(1)" not in r.text
    assert "&lt;script&gt;" in r.text


def test_ui_ask_short_query_is_a_friendly_message(client):
    r = client.get("/ui/ask", params={"q": "db"})
    assert r.status_code == 200
    assert "at least 3 characters" in r.text


def test_ui_create_incident_returns_a_row(client):
    r = client.post("/ui/incidents", data=FORM)
    assert r.status_code == 200
    assert r.text.lstrip().startswith("<tr")
    assert "INC-9004" in r.text
    assert "Checkout errors" in client.get("/").text


def test_ui_create_incident_invalid_shows_error_and_creates_nothing(client):
    r = client.post("/ui/incidents", data={**FORM, "severity": "urgent"})
    assert r.status_code == 200
    assert 'class="error"' in r.text
    assert "INC-9004" not in client.get("/").text
