# AskOps web page &mdash; specification

Mission 4 builds this. **No JavaScript framework and no build step**: server-rendered Jinja2 templates,
and [htmx](https://htmx.org) attributes that swap HTML fragments into the page. htmx is already vendored
at `askops/static/htmx.min.js`, and `askops/templates/base.html` already loads it and carries the styling.

## Routes (in `askops/web.py`, no prefix)

| Method | Path | Returns |
|---|---|---|
| GET | `/` | The full page, extending `base.html` |
| GET | `/ui/ask?q=<text>` | An HTML **fragment** (no `<html>`), swapped into `#results` |
| POST | `/ui/incidents` | An HTML **fragment**: one `<tr>` for the new incident, added to the top of the table |

Every route gets the store with `Depends(get_store)`, exactly like the API.

## The page (`GET /`)

1. **Ask** &mdash; a form with one text input named `q` and the attributes
   `hx-get="/ui/ask" hx-target="#results"`, and an empty `<div id="results"></div>` under it.
2. **Open an incident** &mdash; a form with `hx-post="/ui/incidents" hx-target="#incident-rows" hx-swap="afterbegin"`
   and fields `title`, `severity` (a `<select>` of the four severities) and `service`.
3. **Incidents** &mdash; a table of every incident, newest first (id, title, severity, service), whose
   `<tbody>` has `id="incident-rows"`.

## `GET /ui/ask`

- Shows `Results for "<q>"`, then each runbook hit (title, score, and its steps as an ordered list), then
  the matching incidents. Reuse `sources.runbook_hits` and `sources.incident_hits`, concurrently.
- If `q` has fewer than 3 characters, return a fragment saying **Type at least 3 characters** (status 200,
  so htmx swaps it in).
- **The query is user input, echoed back into HTML.** It must be escaped. Jinja2 autoescapes `.html`
  templates; do not build HTML with f-strings.

## `POST /ui/incidents`

- Form fields arrive with `title: str = Form(...)` and so on (`python-multipart` is already installed).
- Validate with **the same `IncidentIn` model the API uses**: one contract, two front ends.
- Success: return the new row. Invalid input: return `<tr class="error"><td colspan="4">...message...</td></tr>`
  with status 200 and create nothing.

## Done means

`uvicorn askops.app:app --reload`, open <http://127.0.0.1:8000>, ask *"deploy rollback"*, open an
incident, and watch both update **without a page reload**.
