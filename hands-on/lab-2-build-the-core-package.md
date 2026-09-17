# Lab 2 &mdash; Build the core package

**Tier 2 &middot; Structure** &nbsp;|&nbsp; ~25 minutes &nbsp;|&nbsp; Mission 2 &nbsp;|&nbsp; Copilot: **your choice**

## The situation

AskOps needs a core that knows nothing about HTTP: domain errors, a store that loads JSON without falling
over on one bad record, and a keyword search. It is the part every later mission, and the agent brain you
add later in the course, is built on.

## Read first (5 minutes, no editing)

Open these and read them top to bottom. Ask Copilot Chat about anything you would not approve in a review.

- `askops/models.py` &mdash; `@dataclass(frozen=True, slots=True)`, `StrEnum`, a `classmethod` constructor
- `askops/store.py` &mdash; what is done, and the four TODOs
- `askops/search.py` &mdash; the docstring *is* the spec
- `tests/test_m2_core.py` &mdash; especially `caplog` and `tmp_path`, two pytest fixtures you get for free

Answer for yourself: **which module imports which?** Draw it. If `store` ever imports `search`, you have
a cycle.

## Do

1. `askops/errors.py` &mdash; `RunbookNotFound` and `DataError`, both subclasses of `AskOpsError`.
2. `askops/store.py` &mdash; load incidents (skip bad ones with a `WARNING`), `get_runbook`, `incidents`,
   `add_incident`, and turn file problems into `DataError`.
3. `askops/search.py` &mdash; implement `search` from its docstring.

Use inline completions and Chat freely now. Run `python score.py 2` often.

## Notice

- **`raise RunbookNotFound(runbook_id) from None`** hides the `KeyError` from the traceback; `from exc`
  keeps it as the cause. Pick deliberately: would the person on call want to see the original?
- **`logger.warning("skipping incident %s: %s", id, exc)`** passes arguments instead of an f-string.
  The message is only formatted if that level is enabled, and log aggregators can group by the template.
  Copilot will often suggest the f-string. It works. It is still the wrong habit.
- **Sets do the scoring.** `words & title_words` is set intersection. If your search loops over words
  and counts, it passes; compare it with the set version and decide which you would rather review.
- **Returning `sorted(...)`** gives callers a new list, which is why `test_incidents_returns_a_copy` passes
  without an explicit copy.

## Done when

`python score.py 2` shows **Score: 14/14**, and `python score.py 1` is still 19/19. Commit.

## Stretch

Add a `@timed` decorator in `askops/timing.py` that logs how long a function took at `DEBUG`, and put it
on `search`. It is six lines, and it is the pattern behind half the framework decorators you are about to
use: `@router.get`, `@pytest.fixture`, `@tool`.
