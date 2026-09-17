"""Mission 1 - the spec for katas/drills.py."""
from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from katas import drills as d

INCIDENTS = [
    {"id": "INC-1", "title": "502s", "severity": "high", "service": "payments"},
    {"id": "INC-2", "title": "slow login", "severity": "medium", "service": "auth"},
    {"id": "INC-3", "title": "pool exhausted", "severity": "high", "service": "payments"},
]


def test_word_counts_is_case_insensitive():
    assert d.word_counts("Deploy deploy ROLLBACK") == {"deploy": 2, "rollback": 1}
    assert d.word_counts("") == {}


def test_unique_services_sorted():
    assert d.unique_services(INCIDENTS) == ["auth", "payments"]


def test_high_severity_titles_in_order():
    assert d.high_severity_titles(INCIDENTS) == ["502s", "pool exhausted"]


def test_index_by_id():
    idx = d.index_by_id(INCIDENTS)
    assert list(idx) == ["INC-1", "INC-2", "INC-3"]
    assert idx["INC-2"]["service"] == "auth"


def test_group_by_service():
    assert d.group_by_service(INCIDENTS) == {"payments": ["INC-1", "INC-3"], "auth": ["INC-2"]}


def test_first_or_default_works_on_any_iterable():
    assert d.first_or_default([7, 8]) == 7
    assert d.first_or_default((x for x in [])) is None
    assert d.first_or_default(x * 2 for x in [5, 6]) == 10
    assert d.first_or_default([], default="none") == "none"


def test_add_tag_does_not_share_a_default_list():
    assert d.add_tag("a") == ["a"]
    assert d.add_tag("b") == ["b"], "the second call saw the first call's tag - a shared default"
    mine = ["x"]
    assert d.add_tag("y", mine) == ["x", "y"]


def test_display_name_uses_truthiness():
    assert d.display_name({"name": "Asha", "email": "a@x"}) == "Asha"
    assert d.display_name({"name": "", "email": "a@x"}) == "a@x"
    assert d.display_name({"email": "a@x"}) == "a@x"
    assert d.display_name({}) == "anonymous"


@pytest.mark.parametrize("value, expected", [("80", 80), (" 443 ", 443), ("65535", 65535)])
def test_parse_port_valid(value, expected):
    assert d.parse_port(value) == expected


@pytest.mark.parametrize("value", ["0", "65536", "http", ""])
def test_parse_port_invalid_raises_value_error(value):
    with pytest.raises(ValueError, match="invalid port"):
        d.parse_port(value)


def test_port_or_default():
    assert d.port_or_default("9000") == 9000
    assert d.port_or_default("nope") == 8080
    assert d.port_or_default("nope", default=1) == 1


def test_money_is_a_value_object():
    a = d.Money(Decimal("10.50"), "INR")
    assert a == d.Money(Decimal("10.50"), "INR")
    assert a.add(d.Money(Decimal("0.50"), "INR")) == d.Money(Decimal("11.00"), "INR")
    assert a.amount == Decimal("10.50"), "add must not change the original"
    with pytest.raises(ValueError):
        a.add(d.Money(Decimal("1"), "USD"))
    with pytest.raises(FrozenInstanceError):
        a.amount = Decimal("0")


def test_ticket_watchers_not_shared_and_priority_validated():
    t1, t2 = d.Ticket("a"), d.Ticket("b")
    t1.watchers.append("asha")
    assert t2.watchers == []
    with pytest.raises(ValueError):
        d.Ticket("bad", priority=9)


def test_read_nonblank_lines(tmp_path):
    f = tmp_path / "hosts.txt"
    f.write_text("# comment\nweb-1\n\n  web-2  \n")
    assert d.read_nonblank_lines(f) == ["web-1", "web-2"]
    assert d.read_nonblank_lines(str(f)) == ["web-1", "web-2"]
