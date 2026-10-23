"""`PortalConnector.status(listing)`. Portals are fed from the MLS (WS3-C4, C8 to C10, C12): no API call is made
and nothing is scraped (WS3-D7). `SimulatedPortals` reports what would happen, and when, from the MLS entry."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

PORTALS = [
    # name, WS3 ID, note shown on the card, one-time "human required" step (or None)
    ("Zillow / Trulia", "WS3-C4", "Buyer enquiries on Zillow go to the agents who pay Zillow, not to the listing firm.",
     "Claim the firm's agent profile (one time)"),
    ("Realtor.com", "WS3-C8", "Fed through OneKey's syndication settings.",
     "Turn on the Keystone Realtor.com switches (one time)"),
    ("Redfin", "WS3-C9", "Fed from OneKey; status only.", None),
    ("Homes.com", "WS3-C10", "Your buyer leads come to you here: Homes.com routes enquiries to the listing firm.",
     None),
    ("OneKeyMLS.com and Cribio", "WS3-C12", "OneKey's own public sites; tied to the Keystone switch.", None),
]


@dataclass
class PortalStatus:
    name: str
    ws3_id: str
    status: str
    detail: str
    human_step: str | None


class SimulatedPortals:
    def status(self, mls_entered_at: datetime | None, exposure: str | None) -> list[PortalStatus]:
        out = []
        for name, ws3, note, human in PORTALS:
            if exposure and exposure != "Publish to Internet":
                st, detail = "not shown", f"The seller chose \"{exposure}\": portals do not receive the listing."
            elif mls_entered_at is None:
                st, detail = "waiting for the MLS entry", ("Appears automatically from OneKey about 24 to 48 hours "
                                                           "after the listing is keyed in. " + note)
            else:
                due = mls_entered_at + timedelta(hours=48)
                st, detail = "fed from the MLS (simulated)", (f"Syndicating from OneKey; expected by "
                                                             f"{due.strftime('%a %d %b %H:%M')} UTC. " + note)
            out.append(PortalStatus(name=name, ws3_id=ws3, status=st, detail=detail, human_step=human))
        return out
