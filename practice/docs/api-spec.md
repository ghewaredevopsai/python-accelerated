# AskOps API &mdash; specification

Mission 3 builds this. Mission 5 adds the failure contract at the bottom. The tests are the
acceptance criteria; this page is the intent behind them.

## Rules for every endpoint

- Mounted under `/api` (already done in `askops/app.py`).
- Every endpoint gets the store with `store: Store = Depends(get_store)` from `askops/deps.py`. **No module-level
  store**, or the tests cannot give each test its own.
- Request and response bodies are **pydantic models in `askops/schemas.py`**, declared with
  `response_model=` so `/docs` shows the contract.
- Domain errors become HTTP errors at this edge and nowhere else: `RunbookNotFound` &rarr; **404** with
  `{"detail": "runbook <id> not found"}`.
- Log with the module's `logger`, never `print`.

## Endpoints

| Method | Path | Success | Errors |
|---|---|---|---|
| GET | `/api/health` | `200 {"status": "ok", "runbooks": <count>}` | |
| GET | `/api/runbooks?service=<name>` | `200` list of **RunbookOut**, sorted by id; `service` optional | |
| GET | `/api/runbooks/{runbook_id}` | `200` **RunbookOut** | `404` unknown id |
| GET | `/api/incidents` | `200` list of **IncidentOut**, newest first | |
| POST | `/api/incidents` | `201` **IncidentOut** | `422` invalid body &middot; `404` unknown `runbook_id` |
| GET | `/api/ask?q=<text>&limit=<n>` | `200` **AskOut** | `422` if `q` is shorter than 3 characters, or has no word of 3+ characters |

## Models

**RunbookOut** &mdash; `id: str`, `title: str`, `service: str`, `tags: list[str]` (sorted), `steps: list[str]`

**IncidentIn** &mdash; what a client sends
- `title: str`, 5 to 120 characters
- `severity: Severity` (the enum in `askops/models.py`; anything else is a 422)
- `service: str`, at least 1 character
- `runbook_id: str | None = None`

**IncidentOut** &mdash; `id`, `title`, `severity`, `service`, `opened_at: datetime`, `runbook_id: str | None`

**HitOut** &mdash; `runbook_id: str`, `title: str`, `score: int`

**AskOut** &mdash; `query: str`, `runbooks: list[HitOut]`, `incidents: list[IncidentOut]`

## `/api/ask` must be concurrent

`/ask` consults two slow sources in `askops/sources.py`: `runbook_hits(store, q, limit)` and
`incident_hits(store, q)`. Each takes about 0.2 s. Make the endpoint `async def` and **await both at
the same time** (`asyncio.gather`), so the whole request takes about 0.2 s, not 0.4 s. A test times it.
`limit` defaults to 5, between 1 and 20.

---

## Mission 5 &mdash; the failure contract

Added after an incident in which `/ask` returned `200` with empty results while the wiki was down, and
the on-call engineer concluded there was no runbook.

- If either source raises an `AskOpsError`, `/api/ask` returns **503** with
  `{"detail": "search unavailable"}`.
- It logs the underlying error at **ERROR** level, with the exception attached (`logger.exception`).
- **An empty result must only ever mean "nothing matched"**, never "something broke".
- Anything that is *not* an `AskOpsError` is a bug. Let it propagate: FastAPI turns it into a 500 and
  it shows up in the logs.
