# AskOps &mdash; the practice codebase

**AskOps** is an internal engineering assistant: a store of runbooks and incidents, and a way to ask
*"what do I do about this?"*. By the end of the module it is a working FastAPI service with a JSON API
and a web page. Every lab in this module is done here, in your own editor, with GitHub Copilot.

It starts **unfinished on purpose**. Five missions finish it, and each one has failing tests that
describe what "done" means:

| Mission | Copilot writes, you review | Spec | Score |
|---|---|---|---|
| 1 &mdash; Python drills | `katas/drills.py` | the docstrings | `python score.py 1` |
| 2 &mdash; Core package | `askops/errors.py`, `store.py`, `search.py` | the TODOs | `python score.py 2` |
| 3 &mdash; JSON API | `askops/schemas.py`, `api.py` | [`docs/api-spec.md`](docs/api-spec.md) | `python score.py 3` |
| 4 &mdash; Web page | `askops/web.py`, `askops/templates/` | [`docs/web-spec.md`](docs/web-spec.md) | `python score.py 4` |
| 5 &mdash; Review and ship | review [`review/PR-42.md`](review/PR-42.md), then finish `api.py` | the bottom of `api-spec.md` | `python score.py 5` |

Already complete, and worth reading: `askops/models.py`, `deps.py`, `sources.py`, `app.py`,
`templates/base.html`.

## Make your own copy first

Do not work in this folder. Copy it out once, make it a git repository, and open **the copy** as the
workspace:

```bash
cp -r practice ~/askops                  # Windows PowerShell: Copy-Item -Recurse practice $HOME\askops
cd ~/askops
git init -b main
python -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
git add -A && git commit -m "AskOps starter"
code .
```

Copilot reads `.github/copilot-instructions.md` and `.github/prompts/` from the workspace root, so the
tutor and the house rules only work when the copy is the folder you open.

## Everyday commands

```bash
python score.py                      # the scoreboard: [PASS] / [FAIL] per check
python score.py 3                    # one mission
pytest tests/test_m3_api.py -x       # full failure output, stop at the first
uvicorn askops.app:app --reload      # run it: http://127.0.0.1:8000  and the API docs at /docs
```

## Stuck?

Paste the failing check into Copilot Chat and ask it to explain the cause before it fixes anything. If you are
still stuck, or you have fallen behind, a working solution for every mission is in
[`../solutions/`](../solutions/README.md). Copy the missions before the one you are starting,
and it starts green:

```bash
git add -A && git commit -m "my work so far"
git switch -c catch-up
for m in 1 2 3; do cp -r <repo>/solutions/code/mission-$m/. .; done      # ready for mission 4
```

Nobody has to fall behind. Solve each mission with Copilot first, though: the solutions teach most when you
compare them with what your agent produced.
