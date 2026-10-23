"""The contract also follows an agreement with the outside buyer's agent (offer A), not only the demo path's B."""

from app.modules.contract import service as contract
from app.web import current_deal
from tests.conftest import as_persona
from tests.flows import offers_advised


def test_contract_after_offer_a(client, session):
    offers_advised(client)
    as_persona(client, "seller")
    client.post("/offers/decide", data={"decision": "counter", "offer": "A", "counter_price": "638000",
                                        "lowest_price": "632000", "closing_days": "60"})
    as_persona(client, "presenter")
    client.post("/offers/negotiate")
    r = client.post("/contract/draft", follow_redirects=False)
    assert r.status_code == 303, r.text[-2000:]
    st = contract.state(current_deal(session))
    assert st["passed"], st["findings"]
