# gate56a COMMISSION — TWO Secuura PRs: KS-528 (PR 3) + KS-769 (PR 4), both T2, round 1; author and merger Seat B 59th

Drafted 2026-10-05 AEDT (work 2026-10-04 23:5xZ – 2026-10-05 00:1xZ UTC) by the gate56a drafter. One requirement per row. **The launch action (`repin_and_launch_gate56a.sh <n3> <head3> <n4> <head4>`) re-reads both PRs from the PULLS API and `ls-remote` at launch;** nothing below is a pin of a PR — neither PR existed at drafting.

## The PRs
| field | PR 3 | PR 4 | source |
|---|---|---|---|
| ticket / key set | KS-528 / {KS-528} | KS-769 / {KS-769} | ANSWER_seatB59_budget (two PRs accepted) |
| PR number, head, branch | UNKNOWN until the READY (placeholders `{{PR3}}` / `{{HEAD3}}` / `{{BRANCH3}}`) | UNKNOWN (`{{PR4}}` / `{{HEAD4}}` / `{{BRANCH4}}`) | — |
| branch rule | carries `ks-528`, not `ks-769` (case-insensitive) | carries `ks-769`, not `ks-528` | kit `branch_rx` (drafter's convention, D7) |
| ONE path | `Blockchain/Dev/scripts/audit/audit-baseline.json` (base blob `8a9178c9eaa4`) | `Blockchain/Dev/scripts/audit/lock-discovery.mjs` (base blob `3dd903b527f2`) | `git rev-parse` at 14d40d4455c7 |
| the edit | `expires` of GHSA-wrjc-x8rr-h8h6 + GHSA-337j-9hxr-rhxg: 2026-10-09 -> **2026-10-31** (card literal); reason may gain an APPENDED note | `:209 expires: '2026-10-19'` -> **`'2027-01-01'`**; comment `:202-:208` may change | ADDENDUM + ANSWER rulings 3/4 |
| valid through (UTC, `<=`) | 2026-10-30 | 2026-12-31 | baseline-contract.mjs:141 |
| subject (exact, no `(#n)`) | `KS-528: the two react-router baseline rows are re-dated to 2026-10-31` (69) | `KS-769: the mobile-tree dormant exclusion is re-dated to 2027-01-01` (67) | seat-measured; `len()` re-measured |
| authority | card `secuura-fuse-1009-measured-1001` ruled **a** 2026-10-02T10:02:04.918726+10:00 | card `secuura-mobile-dormant-fuse-lapses-1019b` ruled **a** 2026-10-05T09:59:45.387494+11:00 (store) / 09:58:44 AEDT (his live-board act); value per his A2 "Valid through 31 Dec -> write 2027-01-01" | decisions.json; ANSWER |
| standing grant | Kam, terminal 2026-10-05: "board taps are enough for audit re-dates" — `0_Brain/learnings/2026-10-05_board-taps-suffice-for-audit-redates.md` (re-dates only; add/remove/widen NOT covered) | same | learning file |
| GO string | `GO (Seat B 59th): merge <n3> on gate56a` | `GO (Seat B 59th): merge <n4> on gate56a` | kit `go_template` |
| tier | T2 date-only config | T2 date-only config | Wednesday |

**Common:** base develop `14d40d4455c7da3c31c71d614fc7c4d1d4ffc2fb` (#1376's squash, tree `6d96b6e81275` == gateD2 END_TREE; read at the stale shared checkout via tree-identical `57fa9e31d7ce`). Pane `QA/Secuura-ks528-769-<n3>`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks528-769-g56a/`. ONE verdict mail FROM coagent@ TO wednesday-agent@, subject per kit `verdict_subject_template`, with a MERGE ADDENDUM line PER PR. Previous round: gateD2's report (hash recorded at fill, not pinned).

## The checks (the tester runs each ONCE PER PR in its OWN scratch clone; each rc on its own line; each with a control that can fail)
- **C1 PIN + PATH** (`c1_pin_gate56a.py`): head == ls-remote (pull/head AND branch) == API; base develop unmoved (or SIBLING-ADVANCE by name); 1 commit; EXACTLY ONE path; 0 trailers (control `bf277eead268`); subject AND title exact, no `(#`; key set == own key; `Refs <own>`; mode 100644 (control 100755); blob at HEAD^ == kit base blob.
- **C2 DIFF SHAPE** (`c2_diffshape_gate56a.py`): PR 3 JSON parsed both sides, 25 == 25 same order, every other row field-and-order equal, only the two `expires` (and an appended reason note) changed, raw line diff confirms; PR 4 every line outside ticket..expires byte-equal, the literal exact, only `//` lines between, one literal; WARN on a stale comment.
- **C3 FROZEN-CLOCK PROOF** (`c3_clock_gate56a.py` + `c3_freeze_clock_gate56a.mjs` + `c3_probe_gate56a.mjs`): the real modules under a pinned Date; A1-A6 table per PR; K0 clock self-test; PR 3 the real audit-gate.mjs with a fake npm (G1-G5); PR 4 the D1 discrimination control.
- **C4 SECURITY** (`c4_security_gate56a.py`): no row / exclusion added or removed; same package / ticket / reason; installed react-router inside both advisories' ranges (controls outside); mobile lock blob unchanged.
- **C5 NOT COVERED + AUTHORITY** (`c5_notcovered_gate56a.py`): ruled card, grant line, value ruling, body statements; the NOT COVERED list.
- **COLLISION-CENSUS** (`gh_census_gate56a.py --exclude n3,n4`): OVERLAP on either path refuses the launch (rc 15); SAME-KEY reported.
- Also: METHOD-STATED, PR-BODY-CLAIMS (D1-D6), NOT-TESTED-LIST, TIERING, DISK-ENOSPC, REPORT-HASH-LAST. **Findings only.**

## Nothing in this gate needs Kam
No deploy, no prod, no live service, no external comms beyond the one verdict mail to Wednesday. X6 (read-only GitHub REST GETs) and X7 (unauthenticated advisory-DB GETs) are the only exceptions.

## GO
Two GO mails, subjects `GO (Seat B 59th): merge <n3> on gate56a` and `GO (Seat B 59th): merge <n4> on gate56a`. Seat B 59th merges each with the head pinned and the subject exact (no suffix). The first to merge lands on HEAD^{tree}; the second lands on its HEAD^{tree} merged with the sibling's one path (the tester quotes it; the paths are disjoint).
