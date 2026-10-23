"""T3: python-statemachine on the deal lifecycle, to compare with the record gates in app/records/service.py."""
from statemachine import State, StateMachine


class DealLifecycle(StateMachine):
    intake = State(initial=True)
    listed = State()
    priced = State()
    marketed = State()
    under_offer = State()
    in_contract = State()
    closed = State(final=True)

    sign_listing = intake.to(listed, cond="agency_acknowledged")
    choose_price = listed.to(priced, cond="listing_signed")
    publish = priced.to(marketed, cond="price_chosen")
    accept_offer = marketed.to(under_offer, cond="seller_accepted")
    sign_contract = under_offer.to(in_contract, cond="pcds_delivered")
    close = in_contract.to(closed)

    def __init__(self, decisions):
        self.decisions = decisions
        super().__init__()

    def agency_acknowledged(self):
        return "CP-01" in self.decisions

    def listing_signed(self):
        return "CP-03" in self.decisions

    def price_chosen(self):
        return "CP-05" in self.decisions

    def seller_accepted(self):
        return "CP-12" in self.decisions

    def pcds_delivered(self):
        return "CP-04" in self.decisions


decisions: set[str] = set()
m = DealLifecycle(decisions)
try:
    m.sign_listing()
    print("unexpected: transition allowed")
except Exception as e:
    print("refused as expected:", type(e).__name__, "-", e)
decisions.add("CP-01")
m.sign_listing()
print("state:", m.current_state.id)
