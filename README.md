# Python Accelerated

A **four-hour crash course** for experienced software engineers who do not write Python yet. You leave able to
read Python, review a Python pull request, and build a tested Python web app with GitHub Copilot &mdash; and the
app is running on your own machine before the session ends.

**Start at [`index.html`](index.html)** &mdash; open it in a browser from your clone.

```
python-accelerated/
  index.html                         module home: tiers, labs, what is covered
  python-learning-outcomes.md        what you will be able to do
  presentation/                      6 slide decks, one per tier
  hands-on/                          6 labs - start with hands-on/README.md
  practice/                          AskOps, the application every lab builds (copy it out first)
  solutions/                         one working solution per mission - try first, compare after
  assets/                            slide theme and runner
```

## The tiers

| Tier | Deck | Talk | Lab |
|---|---|---|---|
| 0 &mdash; You already know this | [`t0-you-already-know-this.html`](presentation/t0-you-already-know-this.html) | 15 min | [Lab 0](hands-on/lab-0-set-up-and-meet-your-tutor.md) &middot; 5 min |
| 1 &mdash; Data | [`t1-data.html`](presentation/t1-data.html) | 15 min | [Lab 1](hands-on/lab-1-drills-with-a-tutor.md) &middot; 30 min |
| 2 &mdash; Structure | [`t2-structure.html`](presentation/t2-structure.html) | 15 min | [Lab 2](hands-on/lab-2-build-the-core-package.md) &middot; 25 min |
| *Break* | | *15 min* | |
| 3 &mdash; Service | [`t3-service.html`](presentation/t3-service.html) | 20 min | [Lab 3](hands-on/lab-3-the-api-spec-first.md) &middot; 35 min |
| 4 &mdash; Web app | [`t4-web-app.html`](presentation/t4-web-app.html) | 5 min | [Lab 4](hands-on/lab-4-put-a-web-page-on-it.md) &middot; 20 min |
| 5 &mdash; Review and ship | [`t5-review-and-ship.html`](presentation/t5-review-and-ship.html) | 10 min | [Lab 5](hands-on/lab-5-review-reject-ship.md) &middot; 15 min |

## Get started

```bash
git clone https://github.com/ghewaredevopsai/python-accelerated.git
cd python-accelerated
python3 -m http.server 8080          # then open http://localhost:8080 for the decks
```

Then follow [`hands-on/README.md`](hands-on/README.md). Decks: arrow keys or space to move, **T** for the slide
index, **N** for notes, **F** for fullscreen, **Esc** to close an overlay.

## You need

- **Python 3.12 or newer** (3.14 recommended) and **git**
- **VS Code with GitHub Copilot** signed in, on a plan that includes agent mode
- **Access to PyPI** for `pip install` &mdash; check this before the session; everything else works offline
- A GitHub account, for the optional pull request in Lab 5

## How the labs work

- **The tests are the spec.** Each mission ships failing tests; `python score.py` is your scoreboard.
- **Copilot as tutor, then as builder.** A `/tutor` prompt explains Python against the language you already know
  and will not write the answer. From Lab 3 you direct agent mode from a written spec and review what it writes.
- **Read the PR.** Every tier ends with a short diff hiding one Python trap. Decide merge or block before anyone
  explains it.
- **Nobody falls behind.** A solution for every mission is in [`solutions/`](solutions/README.md). Try first,
  then compare, or copy the earlier missions to start the next one green.

---

&copy; Gheware DevOps &amp; Agentic AI &middot; [devops.gheware.com](https://devops.gheware.com) &middot; training@gheware.com
