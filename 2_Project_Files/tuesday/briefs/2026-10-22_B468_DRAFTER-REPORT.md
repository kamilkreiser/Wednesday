# B468 drafter report (Tuesday s142, read-only, 2026-10-22 16:56-17:05 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B468_SEAT-G38_hpsmpoc-b461-296-297-gate-tier2.md` (43 lines, unstamped: 5 four-underscore slots, no READ-WHOLE line; Tuesday fills the Stamp and appends the line).

## Measured (how)
- `ls-remote origin` (16:57): main `a93b926a`; `b461/hpsmpoc-296-297-live-api-e2e` = `52bd6e7c` (matches READY); `b429` `473bfaca`; `b459` `26460869`; `b460` `b9fd28ed`; NO `b462*`, NO `b468*` ref (the only other `b46*` line is `b46/contract-fold-rest-stale-card`).
- `rev-list --count` main..head 1, head..main 0; `diff --numstat main...head`: 14 paths, all under `web/` (10 specs, `live-api-preconditions.mjs` +98, `scripts/e2e.mjs` +234 -2, `e2e-runner.test.ts` +184 -2, `README.md` +1 -1). Commit trailer: Sonnet 5.5 co-author line. Added lines matching skip/only/fixme/todo: 3 (old skip re-stated in content-050; NEW `apiMode()` skip in playbook-live; the unit row's regex text). Control: `test\.skip` over +/- lines also matched 3.
- `gh api` GETs: check-runs total 0, open PRs 0, required contexts (5, printed in the kit); compare main...b429 = 40 files, 0 under `web/e2e|web/scripts|e2e-runner|web/README`, control `web/src/instrumentation.ts` count 1; b459 = 2 UatStartScreen paths; b460 = 1 api test path; b462 compare = 404.
- Source read at `52bd6e7` via `git show`: `web/scripts/e2e.mjs` whole, `live-api-preconditions.mjs` whole, `playbook-live` / `override` / `README` diffs, the other specs' `-U0` diffs, `e2e-runner.test.ts` titles and the four spec-text rows; `ReportingEndpoints.cs` at main :385-540 (Demo branch :414, gate/`DemoRenditionAsync`, Digest :418 and :501). Reading agrees with the builder's 297 mechanism: Demo caller -> alias copy with its own Digest; others -> stored bytes. Not probed (the drafter ran no test, API, build or HTTP).
- Refusal count: `liveApiRefusals` pushes 8 strings (the "not fresh" and "seed ran" arms are `if / else if`); order check adds 5 own refusals. Anchor counts for E1-E22/S1-S2 all measured = 1 at the head via `git show | grep -c -F` (positive control in the same run: each printed 1; none 0).
- B465/B466/B467 briefs exist; their Yours lists have 0 e2e live-api paths; B465 names `playbook-action-plan-live-api.spec.ts:155` ("Partner Dashboard" -> "Home" after B461). B461 changed only that file's line 6 (a comment), so line 155 is untouched.
- Ports 8210-8219: `lsof` rc 1 (0 listeners); `.tools/b468` absent; `.tools/node24`, `.tools/b198` present; `dotnet` not on the drafter's PATH; node on PATH v26.8.1 (CI is 24); load1 10.75 at 16:58.

## Premises of the prompt found wrong or loose
1. "12 specs": it is TEN specs (+ preconditions + 3 others = 14). The kit says ten.
2. "`b462/*` if on origin": absent (404); the kit falls back to B462's brief Yours list, labelled as the brief's.
3. "no `.skip` added except any the brief allowed": 3 matches, not 1: one is the old skip re-stated, one the allowed new skip, one is test text. The kit quotes all.
4. The builder's `playwright.config.ts` was claimed untouched: confirmed (not in the 14).
5. Hard stop in the prompt 21:00; kit target verdict left to Tuesday's stamp.

## Things the kit adds beyond the prompt (flag if unwanted)
- Shared-path hazard: the runner's seed marker and the order check's default data dir live in `os.tmpdir()`, shared across seats; the kit forces `E2E_LIVE_API_MARKER` and `--data-dir` under `.tools/b468/`.
- Port map inside 8210-8219 (8210/8211 head web/API, 8212/8213 base, 8214/8215 order check).
- Independent order instrument (reverse run with direct playwright calls) in addition to the builder's `--live-api-order-check`, plus a planted-dependence control and the builder's own "one seed, both viewports" failure as a control.
- E22 (the `204` check) is predicted a unit-test survivor; the kit kills it by a live probe.
- Four of the 27 new unit rows are source-text greps of spec files; the kit tells the gate to class them as wording pins.
- Tier-1 triggers for 297 are spelled out (owner not served stored bytes; Demo body names the customer; Digest vs body mismatch; Demo copy after override without 409).
- B466 (customer-name validation) and B467 (report wording) interactions to report, not fail.

## UNMEASURED
- Whether anything runs at all: no unit, build, API, Playwright or order-check run (no dotnet, load 10+). The builder's 297 hashes, 32/2/0 per order, 2083 tests are RELAYED only.
- Whether the 297 base test is really red on a fresh showcase seed here, and whether the owner stays on stored bytes after an override while Demo gets 409 (builder DESIGN 1 claim, code reading agrees, not probed).
- Whether `E16` (`some` -> `every`) and `E22` are survivors, and which unit row each of E1-E21 would turn red (predictions only).
- Whether `readiness-first-start` still exercises its race on the showcase seed; whether B465's branch exists to run the merge-tree interaction (not on origin at 16:57); the content of `report-withheld` (+33 -23, unread beyond stats) and the B276/B279 STATUS files (the kit sends the gate to read them).
