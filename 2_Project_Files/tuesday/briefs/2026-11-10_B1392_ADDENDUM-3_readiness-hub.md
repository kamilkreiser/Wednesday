From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-3 to your kit B1392 (SEAT-H142). It goes on the SAME branch as ADDENDUM-2 (`b1392/hpsmpoc-caveat-reword`), as a separate forward commit. Every rule of the kit stands. HARD STOP 10:30 AEDT.

## Why
The product owner (board 09:05 today): "I could not see the partner readiness changes live. These include a new heading and completely new questions ... make sure its deployed properly". An investigator measured the cause:
- The 16 new statements and the 4 areas ARE in UAT's bundle.
- But `/assessments` ("My readiness", `web/src/components/.../AssessmentsHub.tsx:61-68, :83` at 0820efe9; re-print them) leads with the NEWEST COMPLETED run, drawn with the questions it was answered against. On UAT that run is on the old deck, so the page shows the old questions.
- The H1 and browser tab still read "My readiness" (`AssessmentsHub.tsx:95`, `app/(app)/assessments/page.tsx:4`), although his 2026-11-09 20:19 instruction (B1380 kit:6) was, verbatim: "change the partner readiness questions and change title to Playbook Partner Readiness".

## The change (one commit)
1. **When the newest completed run is on an OLDER content version than the current readiness set**, the hub leads with the CURRENT questions (the 16 statements in 4 areas, with the "Start a self-assessment" action) and keeps the old run in the list below, still viewable. When the newest completed run IS on the current version, behaviour is unchanged.
2. **The page H1 and the browser tab title become "Playbook Partner Readiness".** The SIDEBAR label stays "My readiness": the layout v2.1 names it so, and it is not part of his instruction. The walkthrough's link text is already "Playbook Partner Readiness".
3. **No data write, no reset, no API change, no migration.** Only files under your OWNS (`web/src/components/**`, `web/src/app/**`, `web/src/content/**`).

## Prove it (in STATUS under `## ADDENDUM-3`)
- **Test rows, each red at 0820efe9 and green at your head:**
  - (a) newest completed run on the old version: the hub's first panel shows the current set title and the current statements, not the old ones;
  - (b) newest completed run on the current version: the old behaviour holds;
  - (c) the H1 and tab read "Playbook Partner Readiness";
  - (d) the sidebar still reads "My readiness".
- **Full suite:** `npm test` counts, lint and typecheck rc 0, and the e2e shards that hold the readiness and walkthrough specs (find them with `--list`) green.
- **Any existing test that pins the old H1** is updated in the same commit and named in STATUS.
- **NEW WORDS:** list every customer-facing string you add or change, one per line, as `NEW WORDS: <text>`.
- **Commit message** in plain ASCII, ending with your attribution line. Then push the branch.

**Last line**, after BOTH ADDENDUM-2 and ADDENDUM-3 are done: `READY B1392-2: <head sha40>`. If only ADDENDUM-2 could be done by the HARD STOP, push it and end with `READY B1392-2: <sha> (ADDENDUM-3 NOT DONE: <why>)`.
