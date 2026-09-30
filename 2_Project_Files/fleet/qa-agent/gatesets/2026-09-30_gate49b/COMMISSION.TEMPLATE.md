# gate49b COMMISSION — TWO Secuura PRs, #1357 + #1359 (Seat B 49th, T1 KS-1054), merged by Seat D 1st, + a POST-MERGE AUDIT of #1358 (T2 KS-1380), round 49b

Filled by fill_gate49b.py at {{FILLED_AT}} from pins_gate49b.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-30 (~06:05Z, #1359 added ~06:09Z), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords (each as a token).

## The PRs
{{PIN_TABLE}}

- {{DEVELOP_LINE}} END_TREE `{{END_TREE}}` (`{{SHORTSTAT}}`).
- {{DISJOINT_LINE}}
- {{PERM_LINE}}
- {{SUBSET_LINE}}
- {{STEP_LINE}}
- {{MODE_LINE}}
- {{GOLDEN_LINE}}
- Pane `{{PANE}}`. Report dir `{{REPORT}}`. ITEM 2 (KS-729) is OUT OF SCOPE (Wednesday, ~06:09Z: handed to Seat B 49th's successor).

## The rulings
- **#1357:** Kam's ruling (a) on `secuura-ks1054-f9282-migration-failure-visibility` ("Keep serving, flag it on /health") quoted verbatim in the PR body (claims C1: verbatim); Wednesday's python3 ruling (absent -> rc 1; present-but-broken -> rc 1; non-JSON -> rc 2).
- **#1359:** Wednesday's ADDENDUM 1 (Seat B 49th): the N-1350-7 rc-1 wording in both callers from the two goldens; message text only.
- **#1358:** Wednesday's ADDENDUM 1 (Seat D 1st): Direction B as one PR after the 1356 merge; READY to gate49b.

## What the gate must check (by name)
1. **The batch shape**: each PR alone clean; the three pairwise DISJOINT; END in the merge order and in the reverse order; each author's subset; the per-step trees; modes and exec bits; the collision census. (CLEAN-MERGE, DISJOINT, END-TREE, ORDER-INDEPENDENT, MODES, EXEC-BITS, COLLISION-CENSUS)
2. **#1357**: the predicate executed on every python3 / body case at develop and head; red-first on macOS + python:3.12-slim (reds exactly P10/P10b, fixtures green); how the callers consume it; the ruling verbatim. (BEHAVIOUR-1357, RED-FIRST-1357, PREDICATE-CONTRACT, CALLERS-READ, RULING-VERBATIM)
3. **#1359**: what each caller prints and counts on rc 0/1/2; bytes == goldens; red-first (M1/N1 red at base, M2/M3/N2/N3 green both sides); no counter / rc change; the message true of every rc-1 path. (BEHAVIOUR-1359, GOLDENS-BYTE-EQUAL, RED-FIRST-1359, NO-COUNTER-CHANGE, MESSAGE-TRUE)
4. **POST-MERGE AUDIT of #1358** (separate, non-merge, T2): the statement verbatim; analytics / billing / governance images BUILD at develop (kyc the previously-green control; the merge's first parent FAILS as the control), the landed 15-lock delta == the PR head, ranges, registry, lock agreement green, legs 6/7/contract rc 0, the four suites (shared built first), tsc NOT a red-proof, the #649 census. (POST-MERGE-AUDIT, MERGED-BEFORE-GATE, IMAGE-BUILDS, LOCK-DELTA-15, LANDED-EQUALS-HEAD, DEPENDENT-RANGES, REGISTRY-TRUE, LOCK-AGREEMENT, AUDIT-LEGS-DEVELOP, SUITES, TSC-NOT-A-RED-PROOF)
5. **The shell runner** at END counts the two new suites (shared built FIRST). (SHELL-RUNNER, SHARED-BUILT-FIRST)
6. **Subjects, bodies, branches, commits**: `Refs <own key>` only; lands <= 92; no closing keyword; bodies line by line. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
7. **The five drafted client comments**, sentence by sentence; one verdict per draft; neither KS-1054 draft repeats or contradicts comment `49aff833`. (DRAFTED-COMMENTS, NO-REPEAT-49AFF833)
8. **Follow-ons**, the fuse count, ITEM 2 out of scope. (FOLLOW-ONS, FUSE-COUNT, OUT-OF-SCOPE)
9. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST, ONE line naming each PR's head, declared subject and per-step tree.

## GO
ONE GO string, the SUBJECT of the GO mail: `{{GO}}` — Seat D 1st merges #1357 -> #1359 (Wednesday ~07:40Z re-scope). #1358: {{AUDIT_STATEMENT}} Its audit writes no GO. Per-step trees: {{STEP_LINE}}. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate49b.py -> pin_1.out: END_TREE `{{END_TREE}}`, 6 of 6 orders agree, 0 shared paths.
- lockdelta_gate49b.py -> lockdelta_1.out: {{LOCKDELTA}}
- overlaps_gate49b.py -> overlaps_1.out: {{OVERLAPS}}
- keyscan_gate49b.py -> keyscan_1.out: {{KEYSCAN}}
- claims_gate49b.py -> claims_1.out: {{CLAIMS}}
- gh_read_gate49b.py -> gh_read_1.out: {{CENSUS_LINE}}
- capture_mail_gate49b.py -> capture_1.out: {{CAPTURE_LINE}}
