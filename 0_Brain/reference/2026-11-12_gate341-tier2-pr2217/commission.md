# Gate 341, TIER 2 (Sonnet; routing v1.0: tier-2 gates run on Sonnet: type-only change to one e2e test fixture, no product byte). Seat R 113th's KS-2029 = PR 2217. Commissioned 2026-11-12 ~22:1x AEDT by the 20:2x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate339-tier2-pr2215/commission.md` (read it and gate 333's verdict.md for the tier-2 output shape and Constraints). Keep the pass LIGHT: this is a two-line type change; do not run whole service suites.

Pins (Wednesday's git ls-remote at 22:14:50 AEDT; RE-READ at start and end): develop bba80c3c8e241570ba21c0cbe47dc75ad4b5fd2c; refs/pull/2217/head 7b77e16a6e34eb0f41594fc16215167f0fabc950 (ONE commit, parent 13e62febfba8; develop has since moved by PR 2212's squash, packages/shared only).

READY (read whole; reproduce, do not trust): `ready_r113_ks2029_mail.txt` in THIS folder.

What the row claims (unverified by Wednesday): tests/e2e/tests/fixtures/test-helpers.ts +4 (two optional members `created_at?: string; timestamp?: string;` on AgentMailMessage, plus a two-line comment) and a flow/cheat fragment pair; 3 files +25 -0. No repo-defined leg type-checks tests/e2e; the seat's proof is an ad-hoc `tsc` leg (two TS2339 at the parent, none at head, a planted third member gives a new TS2339).

Questions:
1. Scope: exactly 3 files; no runtime line, export or product byte changed (read every hunk).
2. Reproduce the ad-hoc tsc leg yourself (tsc from an existing tree's Dev/node_modules/.bin, the flags the READY names, a scratch copy outside every worktree): exactly the two TS2339 at the parent, none at head, plus your own planted control. State the tsc version.
3. Is the change honest about runtime: the mail API's real field names are unmeasured — does the comment or body claim more than the types?
4. Merge: confirm PR 2217 merges cleanly onto develop bba80c3c8e24 (merge-tree in your clone) and no open PR touches the fixture (census with a positive control).
5. Body: tier-2 statement first, Refs KS-2029 only, no close word; the body says no repo leg type-checks tests/e2e; fragment pair present.

OUTPUT: `verdict.md` here. First line: 'PR 2217: GO / GO WITH NOTES / NO GO (at head 7b77e16a6e34; tier 2; round 1)'. Findings G341-2217-N graded. NOT TESTED section. Constraints exactly gate 333's (read-only on the project; clone into scratch/ here; no push, comment, ticket write, merge or mail; never `cd`).
