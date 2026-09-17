# Lab 5 &mdash; Review, reject, ship

**Tier 5 &middot; Review and ship** &nbsp;|&nbsp; ~15 minutes &nbsp;|&nbsp; Mission 5 &nbsp;|&nbsp; Copilot: **reviewer, not author**

## The situation

After last week's wiki outage, a teammate asked the Copilot coding agent to make `/ask` "resilient". It
opened [**PR #42**](../practice/review/PR-42.md). The description is reasonable, the diff is small, and a
colleague has already written *"LGTM"*.

## Do

1. **Review on paper first (5 minutes).** Read `review/PR-42.md`, then
   `review/pr-42-ask-resilience.diff`. Do not run anything yet. Write down every problem you would block the
   merge for, and why.
2. **Accept it, as the engineer who clicked Merge would.** On a branch:

   ```bash
   git switch -c pr-42
   git apply review/pr-42-ask-resilience.diff    # if it does not apply to your code, make the same
                                                 # four changes by hand - the point is the behaviour
   python score.py
   ```

   Compare the red tests with your list. **Which of your problems did the tests catch, and which did
   they not?**
3. **Reject it.** Leave a one-paragraph review comment in `review/my-review.md`: what is wrong, the test
   that proves it, and what to do instead. Then throw the change away:

   ```bash
   git switch main && git branch -D pr-42
   ```

4. **Do it properly.** Read *Mission 5 &mdash; the failure contract* at the bottom of `docs/api-spec.md`,
   and implement it in `api.py` yourself (about six lines). `python score.py` must be **56/56**.
5. **Ship it with git hygiene.**

   ```bash
   git switch -c fix/ask-failure-contract
   git add askops/api.py review/my-review.md
   git commit -m "Return 503 when an /ask source fails, instead of an empty 200"
   ```

   If you have a GitHub account: create a private repository, push, open a pull request, and request a
   review from Copilot. Compare its comments with yours.

## Notice

**Do steps 1 and 2 before you open this.** It discusses what is wrong with PR #42.

<details>
<summary>After you have run the scoreboard on PR #42</summary>

- **Tests caught three of the four problems. The fourth was yours to catch.** No test bounds `limit`,
  so `?limit=1000000` sails through. Tests are a guardrail, not a reviewer.
- **`except Exception` turned an outage into a wrong answer.** An empty 200 told the on-call engineer
  there was no runbook. That is worse than a 500, because nobody gets paged.
- **The cache bug is two Python traps in one line:** a mutable default argument (shared across every
  call and every store), keyed on the query but not the `limit`.
- **"Easier to read" doubled the latency.** The comment in the diff sounds like a reason. It is a regression.

</details>

## Done when

`python score.py` shows **Score: 56/56**, your review is committed on a branch with a message that
explains the *why*, and you can say which of your review findings no test would have caught.

## Stretch

Write the missing test: `limit` above 20 must be a 422. Watch it fail on PR #42's version.
