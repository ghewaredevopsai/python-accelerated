# Solutions

One working solution per mission. **Try the mission first.** The labs teach by making you read failing
tests and work out the Python, and a solution you read before trying teaches far less than one you compare
against afterwards.

Use this folder when:

- **you are stuck** and the tutor's hints have run out;
- **you fell behind** and want to start the next mission green;
- **you finished** and want to compare. Yours does not have to match: the tests decide what is correct, and
  there is more than one good answer.

## Layout

Each folder holds only the files that mission changes, laid out exactly as in `practice/`:

| Folder | Files | Mission |
|---|---|---|
| [`mission-1/`](mission-1/) | `katas/drills.py` | Python drills |
| [`mission-2/`](mission-2/) | `askops/errors.py`, `store.py`, `search.py` | Core package |
| [`mission-3/`](mission-3/) | `askops/schemas.py`, `api.py` | JSON API |
| [`mission-4/`](mission-4/) | `askops/web.py`, `askops/templates/` | Web page |
| [`mission-5/`](mission-5/) | `askops/api.py` (mission 3's, plus the failure contract) | Review and ship |

## Compare with yours

Read side by side in the editor, or from your `askops` copy:

```bash
git diff --no-index askops/store.py <repo>/solutions/mission-2/askops/store.py
```

`<repo>` is where you cloned this repository.

## Catch up to a mission

The solutions stack: to start mission 4 green you need missions 1 to 3. Copying **replaces your files**, so
commit your own work first, and do it on a branch:

```bash
cd ~/askops
git add -A && git commit -m "my work so far"
git switch -c catch-up
for m in 1 2 3; do cp -r <repo>/solutions/mission-$m/. .; done      # everything before mission 4
python score.py                                                       # missions 1-3 green
```

On Windows, copy the contents of each `mission-N` folder over your copy the same way, in order.

Expected scoreboard after copying missions 1 to N: **20, 34, 47, 54, 56** of 56.

## Mission 5

Look at `mission-5/` only after you have reviewed PR #42 yourself and run the scoreboard on it
(Lab 5, steps 1 and 2). It shows the fix, and that gives the review away.
