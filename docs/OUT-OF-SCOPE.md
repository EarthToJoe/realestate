# Out of scope for the proof of concept

Written so nobody gold-plates. Each line says what the POC will **not** do and what it does instead. Revised
2026-10-23 for decision 21 (the AI is the agent on both sides; no broker or attorney gates in the demo).

| Not in the POC | Instead |
|---|---|
| Real MLS listing entry, or any portal (Zillow, Realtor.com, Redfin, Homes.com) integration | Connector interfaces defined; stubs show "human required here" with the reason from the research; wired up later only where workstream 3 confirms a lawful, automatable path |
| Real public-record or tax-roll lookups | Fictional demo data behind the same interface |
| Real e-signatures or notarisation | Simulated signing screens; the research says which documents could use real e-signature later |
| Sending real email, SMS or social posts | The AI sends on its own into an outbox marked "sent (simulated)"; nothing leaves the system |
| A licensed broker, an attorney, or broker and attorney approval steps in the demo | The AI does every agent act on both sides; a red "NY law today" marker shows each step where New York law today requires a licensed person or a lawyer, with the rule and a link (decision 21); the plan covers the licensing path |
| Payments, escrow, commission disbursement | Shown on the timeline as planned third-party steps (escrow holder, title company) |
| Mortgage, title, insurance, closing services | Named as third parties on the timeline |
| Identity verification of buyers and sellers | Noted as a launch requirement in the plan |
| More than one brokerage or brand | One brokerage, with the brand in one configuration file so a second could follow |
| A native mobile app | A responsive web app |
| Any state other than New York; rentals; commercial property | NY residential sales only |
| Party-specific legal advice (what a clause means for you, whether to sign) | The AI drafts the contract and rider for the parties, with a "NY law today" marker that drafting a contract for another is the practice of law; it declines party-specific legal questions and never says a lawyer is unnecessary (L23) |
| Deeds, transfer-tax forms and other closing papers | Marked as wet-ink / notary items and planned third-party steps |
| Production security hardening, backups, monitoring | A PII baseline (see success criteria) and a login; the plan lists the rest as launch work |
| Market data feeds, automated valuation models | A transparent comparable-sales method on demo data |
| Marketing automation into real ad platforms | Campaign drafts, "published" only inside the demo |
| Training or fine-tuning models | Prompting and retrieval over our own documents |
