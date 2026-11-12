GATE B1541: GO WITH FINDINGS @ b34737f on main 60d442e
G2 gate, round 1 of 2, class approved-wording. Date 2026-11-12 ~16:56 AEDT. Head b34737f4f7c076a80e70fe9e5e2b8cbeb334f628, 1 ahead / 0 behind main 60d442e2 (re-read), 9 files, independent clones, Node v24.21.0.

## Findings
| Sev | Finding |
|---|---|
| Minor | pr-body.md (builder) quoted the approval with "a - " (hyphen) and no card id; Kam's text is "a — Approve all three as proposed", card hpsmpoc-three-words-proposal-ok-1112, 14:54:12. Corrected in pr-body.txt. |
| Minor | pr-body.md/STATUS cite four e2e timing reds I did not see; I ran all 8 shards once, all green. pr-body.txt states only what I measured (and drops the unreproduced red claims). |
| Minor | landing.txt of the builder used --body and <PR-NUMBER>; replaced by the exact form the kit asks (--body-file, <N>). |
| Info | Negative assertion in LoadFailed.states.test.tsx and the /HP-aligned/ regex in WalkthroughPanel.test.tsx intentionally contain the old text; not product. Two "HP-backed tools" comments in phase-flow.ts:27 / PhaseFlow.tsx:101 left by design. |
No Blocker, no Major, no security-shaped issue (no G1 needed).

## Measured (this gate)
1. Three strings: extracted PROPOSED blocks from the proposal by program (3 found); each is a literal in head's source (391, 101, 115 chars, ASCII); controls (last char -> '!') all False. Old texts: 0 hits in head web/src product files; at base the old texts are present (positive control, 5 files).
2. Red-first: head's 6 test files over base source (mutant): 53 pass / 5 fail, exactly PhaseFlow note row, PartnerDashboard.text x2, WalkthroughPanel new row, LoadFailed new row. Same six at head: 58/58. Diff read whole (non-chunk lines of the text test; its two hunks are only inside the LOADED/EMPTY literals): m1 name only, m2 closing brace moved, m3 two comments; nothing else.
3. CI predicates at head: npm ci 0; npm audit --omit=dev 0 vulns; audit-dev 0; lint 0 (max-warnings=0); typecheck 0; build 0; e2e --check-shards OK; whole vitest head 292 files 4238 pass 0 fail vs base 4236; names: lost 2 (renamed tiers row, moved steps row), added 4 (their successors + 2 new); control dropping a row: lost 3. e2e all 8 shards whole, all green: playbook-desktop-1 64p/4s, -desktop-2 54p/13s, mobile-1 63p/5s, mobile-2 52p/15s, journey-and-prototype 2+182+14 p, prototype-desktop-2 177p/4s, tablet-1 181p/1s, tablet-2 177p/4s (ports 9950-9953; 0 listeners before/after). test_hidden_characters.py (-W error::ResourceWarning, py 3.14.10): 14 OK.
4. Diff string literals: only the three product lines + tests. No HP-tool integration claimed (F3 says integration is planned). Squash/PR texts true; message has no ticket/brief/seat/names.
5. Commit author and committer email equal the repo's configured email (by program; control False).

## RELAYED (not re-measured)
Builder's rendered-DOM proof at 1280/390 (counts 3/1/1), infra validate.sh/325-test discover, builder's red-reruns; CLARIFICATIONS.md line 3617 landing rule.

## NOT RUN
api and api-on-SQL-Server jobs (no api path changed); infra shellcheck/bicep; CodeQL/hosted CI (Tuesday lands through them); main moved check: re-read at gate end = 60d442e.
