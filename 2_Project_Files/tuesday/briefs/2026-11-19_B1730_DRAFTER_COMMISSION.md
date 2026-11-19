# B1730 drafter commission — NexusAI records pass for pull request 229 (SEAT-R277)

Commissioned by Tuesday (s292), 2026-11-19, after reading the s291 handover (pickup DELTA 1260) and verifying at source:
NexusAI main = 46050e25f8b0b6acc972a0e033ea9a738b57b7d4 (parents 37fb1bcb + 2ec69377), PR 229 MERGED 2026-11-19T00:04:15Z,
0 open PRs (gh as kamilDatasec, NexusAI GH_CONFIG_DIR, read 11:07:50 AEDT).

## The job
Draft ONE records-seat kit, `2_Project_Files/tuesday/briefs/2026-11-19_B1730_SEAT-R277_nexusai-records-229.md`
(+ `.measured` sidecar + `2026-11-19_B1730_DRAFTER-REPORT.md`), in the FORM of
`2_Project_Files/tuesday/briefs/2026-11-19_B1725_SEAT-R276_nexusai-records-227.md` (read it whole; its drafter report
`2026-11-19_B1725_DRAFTER-REPORT.md` shows the expected report shape). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md`
in full (read it whole first; item 6 = atomic temp-file writes for any records file). Tuesday stamps and launches;
you draft only. You write NOTHING to Jira, GitHub or any NexusAI file: GET/read only.

## What the records seat must do (the scope)
1. RD-1005 and RD-1007: ONE comment each (BLUF / Recommendation / Detail) and move each to Testing per NexusAI
   CLAUDE.md's move rule (read the rule lines; B1725 cites them). Read both tickets' descriptions and acceptance lines
   first; if a comment cannot honestly claim an acceptance line, say so in its BLUF (as B1725 D1 did).
2. CLARIFICATIONS.md: one appended entry (C-305 expected; MEASURE the next free number and section) naming:
   both gates (B1727 G1 GO WITH FINDINGS on cd019f38 round 1; B1729 G2 delta GO WITH FINDINGS on 2ec69377 round 2),
   the hosted CodeQL block on round 1 and its MEASURED cause (the hosted PR check reports an existing alert whose
   data-flow path touches a line the PR ADDS; all five paths started at the round-1 rewritten destructure line;
   fingerprints were IDENTICAL on main and the head — NOT re-keyed; see the B1728 drafter report and the Tuesday
   ledger row of 2026-11-19), the round-2 fix shape (main's destructure line restored, a separate early 400 above it),
   landing (merge commit 46050e25, Deploy demo run 44425992477 build + deploy skipped: not deployed).
3. Follow-up tickets (search Jira for duplicates FIRST by symbol/path/error string and state the search; a found
   ticket gets evidence, not a duplicate):
   a. the other unguarded req.body reads (the list of ~30 is in the B1726 STATUS READY section:
      `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1726_STATUS.md`); one Task.
   b. the final error handler sends thrown/parser text in development for an unparsed or malformed body on the
      POST chat routes (B1727 VERDICT follow-up 1); one Bug, Low unless the source says otherwise.
   c. SECURITY: the RD-523 exception keys on the error CODE string, so an AI endpoint's own error body carrying that
      code gets its text into the chat bubble, which renders with innerHTML (B1727 VERDICT follow-up 2; read the
      bubble render code and the rd523 test at source at 46050e25 before writing a sentence about it); one Bug,
      Medium, labels records-pass-1119 + security. Pre-existing, narrowed by #229: say both halves.
4. History PR: one HISTORY.md entry for pull request 229 on a branch `records/b1730-history` (HISTORY.md only),
   as B1725 did; Tuesday opens and lands it.

## Sources to read at source (not from this commission)
- Gate verdicts: `2_Project_Files/tuesday/briefs/2026-11-19_B1727_verify/VERDICT.md`,
  `2_Project_Files/tuesday/briefs/2026-11-19_B1729_verify/VERDICT.md` (+ `pr-body-addendum.md`).
- Builder STATUS: `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1726_STATUS.md` and `..._B1728_STATUS.md`.
- B1728 drafter report: `2_Project_Files/tuesday/briefs/2026-11-19_B1728_DRAFTER-REPORT.md` (the CodeQL measurement).
- GitHub: PR 229 (title, body as merged, commits, files), merge commit 46050e25, check runs on it. NexusAI repo is
  `datasecau/Reporting_Dashboard_Au`; use `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`
  and verify `gh auth status` names kamilDatasec before any call. Read-only git verbs only in the NexusAI checkout
  (`git --no-optional-locks`); write verbs only in a clone under your scratch dir.
- Jira: GET only, credentials by name in-process from the NexusAI project's own `4_Credentials/.env` (never printed,
  never copied), as B1725's jget.py did (`2_Project_Files/fleet/state/s291/d1725/`).

## Rules that bind the kit
- Every frozen sentence that says what code, a test or a gate finding DOES carries its source line in the sidecar;
  every who-decided phrase is grepped: nothing here was ruled by Kam except what a card says (RD-1005/1007 are lane
  work under Tuesday's standing backlog grant; write decisions as Tuesday's or the ticket's proposed default).
- No B-numbers, seat ids, names, at-signs or URLs in client-visible texts (B1725's scan rules).
- Scratch only under `2_Project_Files/fleet/state/s292/d1730/`.
- First line of the report: `STARTABLE: YES|NO - <why>`. Say plainly what you could not measure.
