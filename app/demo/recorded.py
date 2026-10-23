"""In a recorded demo, the free figures are the recorded ones (fresh-eyes audit 4; decision 48).

The recorded run has the AI's answers for the figures and choices it was recorded with. A different figure would
reach a model the recordings do not cover, so in replay mode it is refused here, in plain words, before anything is
saved or any model is asked, with a way to put the recorded figure back. The deal is never left stuck. With the live
AI (model mode "live") any figure works, within the app's spend cap.
"""

from __future__ import annotations

from fastapi import Request

NOTE = "This recorded demo uses the figures it was recorded with; any figure works in the live demo."


class OffScript(Exception):
    """A figure the recordings do not cover. `back` puts the recorded figure back (the screen, re-filled)."""

    def __init__(self, message: str, back: str, label: str = "Put the recorded figure back"):
        super().__init__(message)
        self.message = message
        self.back = back
        self.label = label


def is_recorded(request: Request) -> bool:
    return request.app.state.provider.mode == "replay"


def _norm(v) -> str:
    s = str(v if v is not None else "").strip().lower().replace(",", "").replace("$", "")
    try:
        f = float(s)
        return str(int(f)) if f == int(f) else str(f)
    except ValueError:
        return s


def check(request: Request, given: dict, recorded: dict, *, back: str, what: str = "figure",
          label: str = "Put the recorded figure back") -> None:
    """Refuse, in replay mode, any of `given` that differs from `recorded` (only the keys in `recorded`)."""
    if not is_recorded(request):
        return
    off = [k for k, v in recorded.items() if _norm(given.get(k)) != _norm(v)]
    if off:
        raise OffScript(f"This recorded demo has the AI's answers only for the {what}s it was recorded with, so a "
                        f"different {what} cannot go on from here: nothing was saved and no AI was asked. Put the "
                        f"recorded {what} back, or try any {what} in the live demo.", back, label)
