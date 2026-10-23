# Out of scope for the proof of concept

Written so nobody gold-plates. Each line says what the POC will **not** do and what it does instead.

| Not in the POC | Instead |
|---|---|
| Real MLS listing entry, or any portal (Zillow, Realtor.com, Redfin, Homes.com) integration | Connector interfaces defined; stubs show "human required here" with the reason from the research; wired up later only where workstream 3 confirms a lawful, automatable path |
| Real public-record or tax-roll lookups | Fictional demo data behind the same interface |
| Real e-signatures or notarisation | Simulated signing screens; the research says which documents could use real e-signature later |
| Sending real email, SMS or social posts | An outbox view where drafts wait for approval; "send" is simulated |
| Payments, escrow, commission disbursement | Shown on the timeline as human and attorney steps |
| Mortgage, title, insurance, closing services | Named as third parties on the timeline |
| Identity verification of buyers and sellers | Noted as a launch requirement in the plan |
| More than one brokerage or brand | One brokerage, with the brand in one configuration file so a second could follow |
| A native mobile app | A responsive web app |
| Any state other than New York; rentals; commercial property | NY residential sales only |
| Legal advice | Drafts for attorney review; the UI says so |
| Production security hardening, backups, monitoring | A PII baseline (see success criteria) and a login; the plan lists the rest as launch work |
| Market data feeds, automated valuation models | A transparent comparable-sales method on demo data |
| Marketing automation into real ad platforms | Campaign drafts only |
| Training or fine-tuning models | Prompting and retrieval over our own documents |
