"""The scoreboard.

    python score.py          every mission
    python score.py 3        one mission

Prints [PASS] / [FAIL] per check and a Score line. It is a thin wrapper over pytest:
`pytest tests/test_m3_api.py` gives you the full failure output when you need it.
"""
import sys

import pytest

MISSIONS = {
    "1": ("tests/test_m1_drills.py", "Mission 1 - Python drills"),
    "2": ("tests/test_m2_core.py", "Mission 2 - AskOps core package"),
    "3": ("tests/test_m3_api.py", "Mission 3 - AskOps API"),
    "4": ("tests/test_m4_web.py", "Mission 4 - AskOps web page"),
    "5": ("tests/test_m5_review.py", "Mission 5 - failure contract"),
}


class Scoreboard:
    def __init__(self):
        self.results = []           # (nodeid, passed, reason)

    def pytest_runtest_logreport(self, report):
        if report.when == "call" or (report.when == "setup" and not report.passed):
            reason = ""
            if not report.passed:
                crash = getattr(report.longrepr, "reprcrash", None)
                reason = crash.message.splitlines()[0] if crash else str(report.longrepr).splitlines()[-1]
            self.results.append((report.nodeid, report.passed, reason))

    def pytest_collectreport(self, report):
        if report.failed:
            self.results.append((report.nodeid, False, "could not import: " + str(report.longrepr).splitlines()[-1]))


def main(argv):
    chosen = argv or list(MISSIONS)
    unknown = [m for m in chosen if m not in MISSIONS]
    if unknown:
        sys.exit(f"unknown mission {unknown[0]} - choose from {', '.join(MISSIONS)}")

    total_passed = total = 0
    for m in chosen:
        path, title = MISSIONS[m]
        board = Scoreboard()
        pytest.main([path, "-p", "no:terminal", "-p", "no:cacheprovider", "-o", "addopts="], plugins=[board])
        print(f"\n{title}")
        for nodeid, passed, reason in board.results:
            name = nodeid.split("::", 1)[-1]
            print(f"  [{'PASS' if passed else 'FAIL'}] {name}" + ("" if passed else f"\n         {reason[:110]}"))
        passed = sum(1 for _, ok, _ in board.results if ok)
        print(f"  Score: {passed}/{len(board.results)}")
        total_passed += passed
        total += len(board.results)

    if len(chosen) > 1:
        print(f"\nScore: {total_passed}/{total}")
    return 0 if total_passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
