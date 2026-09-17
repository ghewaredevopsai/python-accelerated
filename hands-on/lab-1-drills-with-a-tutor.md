# Lab 1 &mdash; Drills with a tutor

**Tier 1 &middot; Data** &nbsp;|&nbsp; ~30 minutes &nbsp;|&nbsp; Mission 1 &nbsp;|&nbsp; Copilot: **tutor mode**

## The situation

Before you let an agent write Python for you, you need to be able to *read* Python fast enough to catch
it. Fifteen drills, each one a real task you meet in every service: counting, grouping, parsing, value
objects, reading a file. None is hard. Each one has a Python-specific way to get it wrong.

## Rules

- **Turn inline suggestions off for this lab.** Click the Copilot icon in the status bar and disable
  completions. Tab-completing a kata teaches you to press Tab.
- Use **`/tutor`** in Copilot Chat when you are stuck. Ask it *why*, not *what*.
- Work top to bottom in `katas/drills.py`. Run the scoreboard after every function:

  ```bash
  python score.py 1
  ```

## Do

1. **Collections (5 drills).** `word_counts` to `group_by_service`. Two of them must be *one*
   comprehension. If yours is a `for` loop that appends, it passes, but ask the tutor to show you the
   comprehension shape on a different example, and rewrite it.
2. **Functions and truthiness (3 drills).** `first_or_default` must work on a generator, which has no
   index and no length. `add_tag` is the most famous bug in Python; the test is written to catch it.
3. **Errors (2 drills).** `parse_port` raises; `port_or_default` must *reuse* it. Ask the tutor what
   *EAFP* means and why Python code prefers `try` over checking first.
4. **Dataclasses (2 drills).** `Money` is frozen; `Ticket` is not, and has two bugs in its field
   declarations. Read `askops/models.py` for a hint about both.
5. **Files (1 drill).** `read_nonblank_lines`, with `with`.

## Notice

- **`tags=[]` as a default is created once**, when the function is defined, and then shared by every
  call. The same trap is `watchers: list = []` in a class. In Java or C# the equivalent would be a
  static field; nobody would write it by accident. In Python everyone does, once.
- **Truthiness:** `user.get("name") or user.get("email") or "anonymous"` is idiomatic, and it treats
  `""`, `0`, `[]` and `None` alike. That is exactly what you want here, and exactly the bug when `0` is a
  valid value.
- **Type hints are not checked at runtime.** `Money("10", 5)` constructs happily. Hints are for readers,
  your editor and tools like mypy, not for the interpreter.

## Done when

`python score.py 1` shows **Score: 19/19**. Commit:

```bash
git add -A && git commit -m "Mission 1: drills"
```

## Stretch

Ask the tutor: *"Review my drills.py as a senior Python reviewer. What is not idiomatic?"* Then ask
yourself which of its suggestions you would have caught in a PR an hour ago.
