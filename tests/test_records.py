"""Record service rules, independent of the screens."""

import pytest

from app.models import Deal, Property
from app.records import service as records


@pytest.fixture()
def deal(session):
    p = Property(street="1 Test Rd", city="Holmes", zip="12531")
    session.add(p)
    session.flush()
    d = Deal(property_id=p.id)
    session.add(d)
    session.flush()
    return d


def test_only_the_named_client_decides(session, deal):
    cp = records.open_decision(session, deal.id, "CP-05")
    for p in ("presenter", "buyer"):
        with pytest.raises(records.NotYourDecision):
            records.decide(session, cp, persona=p, decision="choose")
    records.decide(session, cp, persona="seller", decision="choose")
    assert cp.status == "done"


def test_joint_decision_needs_both(session, deal):
    cp = records.open_decision(session, deal.id, "CP-17")
    records.decide(session, cp, persona="seller", decision="consent")
    assert cp.status == "pending"
    with pytest.raises(records.GateError):
        records.require(session, deal.id, "CP-17", action="make an in-house offer")
    records.decide(session, cp, persona="buyer", decision="consent")
    assert cp.status == "done"
    records.require(session, deal.id, "CP-17", action="make an in-house offer")


def test_declined_decision_keeps_the_gate_shut(session, deal):
    cp = records.open_decision(session, deal.id, "CP-03")
    records.decide(session, cp, persona="seller", decision="decline")
    with pytest.raises(records.GateError, match="declined"):
        records.require(session, deal.id, "CP-03", action="market the house")


def test_kinds_are_enforced(session, deal):
    with pytest.raises(ValueError):
        records.open_decision(session, deal.id, "CP-02")
    with pytest.raises(ValueError):
        records.mark_law(session, deal.id, "CP-01", reason="x")


def test_per_item_markers_add_records(session, deal):
    records.mark_law(session, deal.id, "CP-09", reason="message 1")
    records.mark_law(session, deal.id, "CP-09", reason="message 2")
    records.mark_law(session, deal.id, "CP-02", reason="once")
    records.mark_law(session, deal.id, "CP-02", reason="again")
    assert len(records.records(session, deal.id, "CP-09")) == 2
    assert len(records.records(session, deal.id, "CP-02")) == 1


def test_human_required_is_simulated(session, deal):
    cp = records.record_human(session, deal.id, "CP-08", reason="Keyed by the MLS participant")
    assert cp.status == "simulated" and not cp.blocking
