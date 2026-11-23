# B1977R DRAFTER COMMISSION (Sonnet, in-session, READ-ONLY): re-cut NexusAI kit B1977 (RD-1032 light-mode toner fills, seat N167) onto the new main

Commissioned by Tuesday (s316), written at 2026-11-23 13:17:02 +1100 (clock printed by `date`). Return a 10-line summary with `STARTABLE: YES` or `NO` as line 1.

## WHY
Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1977_SEAT-N167_nexusai-rd1032-build.md` (+ `.measured`, drafter report `2026-11-23_B1977_DRAFTER-REPORT.md`, original commission `2026-11-23_B1977-B1978_NEXUSAI-RD1032-BUILD-AND-DEPLOY-ROUTE_COMMISSION.md`) was drafted on main `3c3be156e8ea36ad297fdadd3055c6e00252ba38`, and its HEADS AT LAUNCH slot requires that sha. Main has moved twice since (read by Tuesday with `gh api -X GET` at 13:16:21, NexusAI GH_CONFIG_DIR):
- PR 243 (NX-SR) landed as merge commit `df72a283d38c1261344f3dbd8c9d14b86c776833`: `__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js` +8 -2 and `__tests__/rd711-audit-flush-serialised.test.js` +8 -2 (no test added or removed; counts 6235/394 unchanged).
- PR 242 (RD-1030) landed as merge commit `85b39c77b84573757d26113cf094325b5b80c182` (parents df72a283 + 27d49f70): `backend/services/capabilities.js`, `__tests__/rd1011-four-routes-administrator-only.test.js`, `__tests__/rd929-capability-design-census.test.js`, and **`scripts/verify-expected-counts.json` (the file this kit's K commit also edits)**; its hosted build on the merge with df72a283 read `Tests: 6237 passed, 6237 total`, `Test Suites: 394 passed, 394 total`.

## WHAT TO DO
Re-cut the kit in place of a new number (keep B1977, seat N167, the product owner's ruling and the option-a choice exactly as the original), against main `85b39c77`:
1. Re-measure every BASE fact the kit freezes at `85b39c77` (file hashes, line numbers, the counts pair, the anchors the patches touch); every one that changed is named in a CHANGED-SINCE-3c3be156 table with old and new value.
2. Rebuild the K commit's `scripts/verify-expected-counts.json` edit on the new file (6237/394 plus this lane's tests: measure, never add up blind), and every patch whose anchor moved.
3. Check that no path of OWNS-B1977 was touched by PR 242 or 243 other than the counts file; if one was, say so as line 2 of the summary.
4. Run every STOP-severity check once on a scratch prototype at `85b39c77` (push URL `invalid://no-push`), PASS with its control fired, or mark it never run; `stamp_check.py` on the re-cut kit exits 0.
5. The HEADS AT LAUNCH slot's required main becomes `85b39c77b84573757d26113cf094325b5b80c182`. Who decided lines name the coordinator, and the ruling is the product owner's card `nexusai-rd1032-pick-toner-fill-1123` = a (his note "looks great.  please build and deploy", 11:06:40).

## FORM AND RULES
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` binds you. Write the re-cut kit to the SAME path (build it whole, write a temp file beside it, then `os.replace`; first copy the current kit to `...build.md.pre-1123-recut` and `cmp` it); the sidecar likewise; report `2026-11-23_B1977R_DRAFTER-REPORT.md` (first line `STARTABLE: YES` or `NO`); scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1977r/`. NexusAI's jest lock: one heavy job at a time through the kit's own runner; never break another holder's lock. READ-ONLY toward the project, Jira and GitHub (`gh api -X GET` only under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`); no `cd`; one simple command per Bash call; never delete (quarantine); `python3 -I`; every count by program with a positive control; no deploy, no Azure, no Jira write; nothing to any human.
