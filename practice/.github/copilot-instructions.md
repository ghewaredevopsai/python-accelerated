# AskOps - house rules for Copilot

AskOps is a small FastAPI service: runbooks, incidents, and keyword search. Python 3.12+.

## How we work
- **The spec is in `docs/`, the acceptance criteria are in `tests/`.** Read both before proposing changes.
  Never edit a test to make it pass; if a test looks wrong, say so and stop.
- Run `python score.py <mission>` after each change and report the score.
- Change only the files the task needs. No new dependencies without asking.

## Python style
- Type hints on every function signature. `X | None`, not `Optional[X]`.
- Domain records are dataclasses in `askops/models.py`; wire shapes are pydantic v2 models in
  `askops/schemas.py`. Use pydantic v2 APIs only (`model_validate`, `ConfigDict`, `Field`), never v1
  (`parse_obj`, `class Config`, `orm_mode`).
- Raise the domain errors in `askops/errors.py`; translate them to HTTP status codes only in `api.py`
  and `web.py`. Never `except Exception:` to hide a failure.
- `logger = logging.getLogger(__name__)`, never `print`. Use %-style arguments in log calls.
- Inside `async def`, never call blocking I/O (`time.sleep`, `requests`, file reads in a loop). Await
  independent calls together with `asyncio.gather`.
- Endpoints get the store through `Depends(get_store)`; no module-level state.
