# Six labs, one app

Hands-on labs for the **Python Accelerated** module. Every lab builds the same application,
[**AskOps**](../practice/README.md), from a pile of failing tests to a running web app, in about
two and a half hours of hands-on time.

## How these labs work

- **The tests are the spec.** Each mission ships with failing tests. Nobody tells you to "write a
  function that...". You run `python score.py N`, read what is red, and make it green. That is how you
  will work with an AI agent at your desk too.
- **Two Copilot modes, switched on purpose.**
  - **Tutor** (Lab 1): type `/tutor` in Copilot Chat. It explains Python by contrast with the language
    you already know, and it will not write the answer. You are building the reading skill that every
    later lab depends on.
  - **Builder** (Labs 3 and 4): agent mode, driven from a spec. You direct; it types; you review.
- **Read before you run.** Every lab has a *read first* step. Reviewing Python you did not write is the
  skill this module is really about.
- **Nobody falls behind.** Behind at the start of a lab? Ask for the checkpoint (see
  [the practice README](../practice/README.md#stuck)) and start the next mission green.
- **Copilot's output varies.** Two people running the same prompt get different code. The tests decide
  what is correct, not the transcript you are shown.

## The labs

| Lab | Tier | Time | Mission | You leave with |
|---|---|---|---|---|
| [0 &mdash; Set up and meet your tutor](lab-0-set-up-and-meet-your-tutor.md) | T0 | 5 min | &mdash; | A venv, a red scoreboard and a working `/tutor` |
| [1 &mdash; Drills with a tutor](lab-1-drills-with-a-tutor.md) | T1 | 30 min | 1 | Collections, comprehensions, errors, dataclasses in your fingers |
| [2 &mdash; Build the core package](lab-2-build-the-core-package.md) | T2 | 25 min | 2 | A package with errors, logging and search, tested |
| [3 &mdash; The API, spec-first](lab-3-the-api-spec-first.md) | T3 | 35 min | 3 | A FastAPI service with pydantic contracts and concurrent async I/O |
| [4 &mdash; Put a web page on it](lab-4-put-a-web-page-on-it.md) | T4 | 20 min | 4 | A web app that updates without page reloads |
| [5 &mdash; Review, reject, ship](lab-5-review-reject-ship.md) | T5 | 15 min | 5 | A rejected PR, a failure contract, and a PR of your own |

## Getting started

Follow [Make your own copy first](../practice/README.md#make-your-own-copy-first), then Lab 0.

**You need:** Python 3.12 or newer (3.14 recommended), git, VS Code with GitHub Copilot signed in (a seat
that includes agent mode), and access to PyPI for `pip install`. A GitHub account for Lab 5's pull
request is useful but not required.
