<!-- Template for headless research job briefs: replace {DATE}, append the job-specific part. The briefs
     actually sent are kept in docs/research/jobs/. -->
# Your job (headless, launched by the realestate chat session on {DATE})

You are one of seven parallel headless jobs working in /root/projects/realestate. Today is {DATE}.
Joe (the client) reads on his phone; his father-in-law, a New York lawyer who once ran a Hudson Valley
real estate business, will read the deliverables to decide whether to move forward. The project's
CLAUDE.md is already loaded; follow its research rules (cite sources, label every claim [PRIMARY] /
[SECONDARY] / [CLAIMED] / [INFERENCE], date facts that change, never soften a finding, never scrape MLSs
or portals against their terms, never store other people's listing photos or copy).

## Read first
- `docs/BRIEF.md`: Joe's brief, verbatim. Your workstream's exact ask is quoted below; answer it fully.
- `docs/ASSUMPTIONS.md`: assumptions A1 to A11 with kill criteria.
- `docs/DECISIONS.md` and `docs/QUESTIONS-FOR-JOE.md` (Q4 holds the provisional assumptions about the
  father-in-law's status: he holds or gets a broker licence, is broker of record, and does not act as either
  party's lawyer in brokerage deals; analyse the alternatives too where they matter).
- `docs/research/method/researcher.md` (how to research and how notes are formatted) and
  `docs/research/method/report-writer.md` (how the deliverable is written).
- Your notes files (listed below), in full. Paths contain spaces: use the Read tool or quote them.
- You may read other workstreams' notes in `research_notes/` for cross-checks, read-only.
- The kill criteria K1 to K9 at the end of `research_notes/WS5 Competitors/why_attempts_failed_and_niche_evidence.md`.

## Rules for this parallel run (these override any standing instruction to commit or to edit shared files)
- Seven jobs share this working tree. **Do not run `git add`, `git commit`, `git push`, `git stash`,
  `git checkout` or any other git command that changes state.** The orchestrating session reviews and commits.
- **Write only the files named in your job.** Do not edit `docs/QUESTIONS-FOR-JOE.md`, `docs/PROGRESS.md`,
  `docs/ASSUMPTIONS.md`, `docs/DECISIONS.md`, `docs/TRACEABILITY.md`, `docs/SPEND-LOG.md`, `CLAUDE.md`, or
  another workstream's files. Questions for Joe go in your handoff file (step C) with a provisional choice.
- Never edit or delete existing content in the notes files; only append.
- Never wait for a human. If something is unknowable, say so and move on.

## Joe's standard for this research (his words, 2026-10-23)
"We're going to want to make sure our research is rather extensive and not piece and parcel; comprehensive,
accurate, focused on the right things." So: **comprehensive** means every part of the ask is covered in
depth, not only the parts the notes happen to cover; **accurate** means the claims the conclusions rest on
are checked against primary sources, not repeated from the notes; **focused** means effort goes to what
decides whether this venture works and how the product must be shaped, not to trivia.

## Step A: coverage audit, verification, gap fill (fresh web-search budget)
The cloud passes that wrote your notes ran out of shared web-search budget part-way, so every notes section
ends with a "Gaps" list. But the listed gaps are not the only holes. Do all three of these:

1. **Coverage audit.** Break your workstream's exact ask (and the specific requirements below) into its
   individual questions. For each, judge whether the notes answer it fully, partly or not at all. Anything
   partly or not at all answered is a gap even if no Gaps list names it.
2. **Verify the load-bearing claims.** List the 10 to 20 claims your conclusions will rest on (statutes and
   what they say, opinion numbers and holdings, prices, rule texts, company status, key statistics). Open the
   primary source for each and confirm it says what the notes say, as of today. Record each check (confirmed
   / corrected / could not verify) in the gap-fill section. A corrected claim is a finding; flag it.
3. **Close the gaps**: the audit's holes plus the listed Gaps bullets, triaged by whether closing them would
   change a conclusion, a number, a classification or a recommendation. Research those thoroughly with
   WebSearch and WebFetch, following `researcher.md` (short queries, fetch the primary page, prefer primary
   sources, note conflicts). Also look for anything that changed in 2025 or 2026 that the notes predate
   (rule changes, prices, company status, new cases or opinions).

There is no search budget (Joe, 2026-10-23: "shouldn't limit searching arbitrarily. agree you can't
search the whole internet for every nit."). Stop on materiality, as `researcher.md` defines it: keep going while
a question that could change a conclusion, a number, a classification, a recommendation or a kill-criterion
call is open; stop when it is answered from a primary source or searching stops turning up anything new; give
nits one quick look at most and list them as "not pursued: immaterial". Gaps that do not bear on the ask can
stay open; say so.

## Step B: write the deliverable
Write the deliverable named below, following `report-writer.md`, with these adjustments for this project:
- It answers the workstream's exact ask from the brief, every part of it, so a reader can tick each part off.
- It is one integrated answer built from all your notes files and the gap fill together, organised around
  the questions that matter, not a file-by-file summary stitched together. Lead with what decides go/no-go and
  product shape; put detail after.
- Readers: Joe on a phone, and a NY lawyer who knows the business. Plain words; define each piece of
  jargon once; no hype.
- Keep the source label next to each cited claim, e.g. `([NY RPL 440](URL)) [PRIMARY]`, and date facts
  that change (prices, fees, company status, counts).
- Do not soften. If a finding hits a kill criterion (A1 to A11 in `ASSUMPTIONS.md`, or K1 to K9), say so
  plainly in the BLUF paragraph and in the relevant section.
- Tables are expected where the ask is an inventory or a comparison (the method allows them); the
  narrative sections around them stay in prose.
- The method's citation rule holds: a claim with no source URL in the notes or your gap fill stays out.
- Use the notes AND your gap fill; where they disagree, the newer primary source wins and you say so.
- As long as it needs to be to answer completely; no padding, no repetition.
- Add a final short section `## Sources and method` that lists the notes files used and states how many
  gaps were closed and which important ones remain open.

## Step C: write the handoff file for the orchestrator
Write the handoff file named below (plain bullets are fine here). Sections, in this order:
1. **Assumption status lines**: for each of A1 to A11 that your workstream bears on, one line:
   `A<n> | hit / dodged / partly hit / still open | one-sentence reason | link to the deliverable section`.
2. **Kill criteria**: which of K1 to K9 (and the assumption kill criteria) your findings hit, dodge or
   leave open, with one sentence each.
3. **Questions for Joe**: each with a provisional choice and what it unblocks. Only questions that are
   genuinely Joe's or his father-in-law's to answer.
4. **Traceability items**: your IDs (as described in your job) with a one-line product implication each:
   what the POC must do, show, or stop at a human checkpoint because of it.
5. **Open gaps** that still matter, and what would close them (a phone call to whom, a document to buy, etc.).
6. **Contradictions** with other workstreams' notes, if you saw any.

## Done when
Your notes files have the gap-fill section, the deliverable is written, the handoff file is written. Your
final reply (it is logged, keep it under 15 lines): the single most important finding, any kill criterion
hit, gaps closed versus still open, and the paths of the files you wrote.
