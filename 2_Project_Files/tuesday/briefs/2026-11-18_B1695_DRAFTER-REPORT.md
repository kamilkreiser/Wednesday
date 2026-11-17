STARTABLE: YES

# Drafter report B1695 | SEAT-H181 | HPSM-POC | picomatch dev-audit exception (HPSM half only)
Drafted 2026-11-18, `date` printed 08:37:42 at first read and 08:45:54 at the last check. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1695_SEAT-H181_hpsmpoc-picomatch-dev-audit-exception.md` (246 lines, 0 non-ASCII bytes, 0 four-underscore runs outside the Stamp slots, 7 slots). `stamp_check.py <kit>` rc 0: 41 claims, 41 measured. Sidecar beside it.

## BLUF
- One data entry in `web/scripts/audit-dev.mjs` (`GHSA-fc5q-39xc-vjpf`, picomatch, `<=4.0.7`, last day 2026-12-18, ruling text "the product owner's 2026-11-18 ruling"), the comment in `ci.yml` lines 391-393, and the tests (one replaced row, five new rows, one argument added to the zod row). Sonnet builder, row L3; gate argued as G1.
- Verified by the drafter in a scratch folder with main's lockfile (not in the repo): the REAL audit step is red on this one advisory alone (rc 1); with the entry it is green (rc 0, one ALLOWED line); three planted copies (date, id, range) each rc 1 with the expected text. The production audit is clean (`found 0 vulnerabilities`).
- No fixed picomatch exists: GitHub advisory API `first_patched_version` null, not withdrawn; npm `latest` is 4.0.7.

## Facts re-measured with instruments (details in the sidecar S01-S19)
- origin main is `36c557ad9255125793bfeb99abdea3b0b4d988e2` (the B1675 landing; one test file differs from `6c1aa32e`, so the three owned files equal those at `6c1aa32e`; blobs read through `gh api contents ... --jq .sha`). Open PRs 0; `b1695` refs 0 (control `b1639` 2). 348 branches; 11 older audit/braces/advisory branches, none new.
- Real red: `npm audit --json` on main's lockfile: 17 nodes high, exactly 1 advisory object; main's script rc 1 with `FAIL GHSA-fc5q-39xc-vjpf ...`. npm's own "fix" is a vitest 3.1.4 downgrade (semver-major): the kit names it as text, never an instruction.
- The seat's new test rows were checked against a node harness of `evaluate()` with the entry (allowed through 2026-12-18 23:59 Sydney; lapse text on 2026-12-19 00:01 Sydney which is still 2026-12-18 in UTC; other advisory, second advisory on picomatch, changed range, other package, braces not allowed, note when not reported). All expectations held. The drafter did NOT run vitest, lint, typecheck or the infra scans (no repo tree touched).
- Test-file consequences found at source: `ships no exception` (lines 50-54) pins the empty list and must be replaced; the zod row (lines 56-62) calls `evaluate` with the shipped list, so it would gain a "no longer reported" note (harness: notes 1 with the entry, 0 with `[]`): the kit passes `[]` (Q-3). Line 41's row still holds (DERIVED; the seat's run is the proof). Step name and run line of the audit step are pinned by `AUDIT_STEPS` (test line 180) and `infra/tests/test_ci_workflow.py:110`, so only the comment above the step changes.
- Model row: `fleet/specs/model-routing.md` lines printed: L3 (82, "Two- or three-file fix, spelled out", S55 "1st"), L1 (80, gate "tier-1 gate if the file is auth/security"), C3 (93, security DESIGN builds: not applicable, the decision is the product owner's and the edits are spelled out), G1 (108), G2 (109). Model id `claude-sonnet-5-5` at `models_latest.json:23`. Launch level `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes.
- Ports: no server; lsof 9900-9929 0 rows (control :5000 3 rows); live panes: tuesday, fleet-monitor, Datasec/MPS-M157, Datasec/NexusAI-N150 (no HPSM pane). Load1 12.44 at 08:4x. Toolchain by path: node24 v24.21.0, npm 11.20.0, python3.14 3.14.10 (system 3.9.6), bicep present.
- Rule 8: the kit's Step 4 runs the infra repo-wide scans (hidden characters, the whole `test_*.py`, `validate.sh`); `test_ci_workflow.py` reads ci.yml.

## D-decisions (mine)
- D-1: last day `2026-12-18` (the mechanism's lapse rule is `today > lastDay`, so it allows all of 18 Dec Sydney and fails from 19 Dec); follows the braces precedent ("lapses 31 Oct" was `lastDay` 2026-10-31).
- D-2: ruling string in the data is "the product owner's 2026-11-18 ruling" (the output line quotes it); no card id or name anywhere in committed text.
- D-3: the new rows use the shipped list (no third argument), the old mechanism rows keep the synthetic braces entry; no existing mechanism row is touched except the zod argument and the replaced `ships no exception` row.
- D-4: the kit makes the real step, not only unit rows, the red-first control, plus three plants on scratch copies (never the tracked file).

## Q-questions for Tuesday (each with a default)
- Q-1: is 2026-12-18 the last ALLOWED day (default, as drafted) or should it fail on the 18th (then `lastDay` is 2026-12-17)? The ruling text says "lapses 18 Dec".
- Q-2: gate G1 (Opus) or G2 (Sonnet)? Default G1: it relaxes a security control for 30 days; G2 row says "1st if the follow-up's mechanism sits on a G1 surface". Tuesday may rule G2 at the Stamp.
- Q-3: zod row takes the empty list (default) rather than expecting the picomatch note.
- Q-4: the record of the ruling (a CLARIFICATIONS entry, the braces precedent had C-44 and C-99) is not in this lane (default: a records seat, yours to commission).
- Also for you: `#219` and `#220` in the ruling are old merged HPSM-POC PRs (merged true), so they belong to the NexusAI half. And a calendar item for 2026-12-18 (not built).

## UNMEASURED
- When the hosted audit began failing (main's check-runs at `36c557ad` read success; the audit step's own line was not read). Whether hosted CI is red on main today (not read).
- Lint, typecheck, the whole vitest, infra scans at head (the seat's runs; the kit gives the expected counts only as RELAYED guides: 304 files, 4340 passed at main).
- That E3/E6 compile under `tsc` (the fixture is typed with `unknown`; the kit lets the seat fix the fixture at source, never an expectation).
- The advisory data moves: a later `npm audit` can differ (the kit has REFUSE 5 for that).

## Inputs table (rule 4, each input exists at BASE or is made by an earlier step)
Step 0 -> `.tools/b1695/**`, clone `head`, `main-tree` (made by Step 0). Step 1 reads GitHub only. Step 2 reads `main-tree` (Step 0) -> `out/step2-*.log`, `base-unit.json`. Step 3.1 reads D2 (kit) in `head` (Step 0) -> `step3-tests-red.log`; 3.2 reads D1 (kit) -> green log; 3.3 reads the real lockfile at BASE; 3.4 reads `head/web/scripts/audit-dev.mjs` after D1 (3.2) -> scratch plant copies; 3.5 applies D3. Step 4 reads `base-unit.json` (Step 2), `compare.py` and `env.sh` from `.tools/b1675/scripts/` (exist at BASE of the machine). Step 5 reads the commit (made in Step 6?) - note: Step 5(a) is run on the working tree before the commit and re-run after it; the kit says "after the commit" for (a): the seat commits in Step 6 after Steps 3-5, so (a) must run on the staged diff first (the B1675 seat did the same: pre and post runs).

## Outside-the-fences disclosure
- Wrote only the kit, the report and the sidecar; scratch files under the session scratchpad only (the audit scratch folder with main's package.json and package-lock.json copies, sed copies of the script, a node harness). No repo tree edited; no ref written; `git` reads only via `git --no-optional-locks` (grep and show at `.tools/b1675/head`, which holds `6c1aa32e`); one read of the project's `2_Project_Files` checkout `git log` and a failed `ls-remote` through its stale key (read-only, printed "Permission denied"; no state changed).
- `gh api -X GET` only (commits, compare, contents, advisories, pulls, branches, check-runs). `npm view`, `npm audit` (read the live registry) in the scratch folder. No Jira, no card store, no hosted host, no az, no ssh beyond that failed ls-remote, no docker.
