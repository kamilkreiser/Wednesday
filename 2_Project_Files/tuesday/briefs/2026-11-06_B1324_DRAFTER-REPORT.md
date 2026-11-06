STARTABLE: YES, after Tuesday fills the slots (S2 = the head sha40, S3 = MAIN plus the base sha40 and the main sha40 read at the stamp). The builder has READY (its STATUS last lines, read at 13:04 as the REFUSE check only; the STATUS body was not read) and the branch is at origin.

# Drafter report: B1324 SEAT-G352, tier-2 gate of b1312/hpsmpoc-mock-rows-wait (drafted 13:04-13:12 AEDT 2026-11-06)

## BLUF
Kit `2026-11-06_B1324_SEAT-G352_hpsmpoc-mock-rows-wait-gate.md` (56 lines, ASCII; 8 lines carry a four-underscore run: seven slots and the last line) plus `2026-11-06_B1324_slots.json`. Sonnet, G2 (`model-routing.md:109`, cap `:111`), round 1 of 2 on a new class, one file `mock-rows.spec.ts` (+64 -24). The gate weighs: each of 7 waits at source and under lag, its own in-flight audit, the ADDENDUM-1 documents reasoning judged by its own body-HTML diff, builder plants P1-P7 plus 5 own, shard counts and time against `timeout-minutes: 20`, then the two shards that hold the file. Two things the commissioning note did not have: the hosted `prototype-tablet-2` job took 18.0 min (90 percent of 20) on main `6d592ede`, and the ticket's fix-shape says to keep `frame()`'s argument optional while the branch made it required.

## Facts re-measured (instrument; control)
1. Refs 13:05 (`gh api -X GET`): main `6d592edea47c1595f1438f8060a8ccac59efd629`; `matching-refs/heads/b1312` one row `d6c040ea5cb303ad133b3c85ba91e18fe59cbdc2`; open PRs 0; commit: one parent `13ac7d7e`, one file +64 -24; message 1494 chars, subject 104 (`wc -c`), one trailer; non-ASCII in message and file 0 (`LC_ALL=C grep -c -v -x -E '[ -~]*'`; planted control not run by me, left to the gate).
2. Main moved (`compare/13ac7d7e...main`: ahead 2, 4 paths: ci.yml, e2e-runner.test.ts, reviewDoor.ts, reviewDoor.test.ts). The gate's judged paths are untouched: `mock-rows` count 0 in runner test, ci.yml, e2e.mjs, playwright.config.ts at main (control `markerStep` 15); blobs of playwright.config.ts, e2e.mjs, playbook.ts, package-lock.json equal base and main (`contents --jq .sha`); `ci.yml` non-comment lines equal base vs main (diff rc 0; control planted line rc 1); 0 files under `web/e2e`, `web/src/app`, `web/src/components` (control `^web/src/server` prints 2). The kit lists the STOP paths.
3. Head file (raw, `grep -n`): `frame` `:20`, `await ready(page)` `:26`, waits `:31 :38 :46 :54 :61 :67 :72`, 19 `frame(page` calls and 19 `^test(` rows; `waitForTimeout` 1 at base, 0 at head; forbidden-token scan of the head 0 lines (control: base hits `waitForTimeout`); removed 24, added 64 (`diff | grep -c`); 19 call lines removed (patch).
4. Ticket HPSMPOC-445 (Jira GET through the project's helper, `fields=description`): done-when reads "each of the 19 calls waiting on its own page's data or on a condition the page shows"; fix-shape reads "keep the optional argument of frame()". The head makes `ready` required (`:20`). Printed 13:05.
5. CI step: `web-e2e` `ci.yml:483`, `timeout-minutes: 20` `:487`, shard list `:494`, `node scripts/e2e.mjs --shard "$SHARD"` `:518`; `--check-shards` `:426`; `half()` `e2e.mjs:52`, the two holding shards `:55` and `:57`; `--check-shards` exit `:544-551`; config has no `expect` key (`grep -c` 0), `retries` `:50` CI 1, local 0.
6. Hosted shard time (`actions/workflows/ci.yml/runs?branch=main` then `runs/<id>/jobs`): `prototype-tablet-2` 18.0 (run 42142695658 on `6d592ede`), 10.1, 10.6, 10.4, 8.1 min on four earlier main runs; `prototype-desktop-2` 10.8, 9.9, 7.8, 9.9, 7.6; `prototype-tablet-1` 15.0, 6.0, 7.6, 7.5, 6.7. All 8 jobs of the latest run succeeded (control: 8 e2e rows counted). The builder's 7.8 and 10.6 came from the older run.
7. Documents page source (`DocumentGeneration.tsx` at head): `useCustomer :71`, `useCustomerResult :74`, `useAsync(... listNarratives ...) :83`, loading status `:155`. The addendum counts one in-flight call; the narratives call (`:83`) is another candidate, and the gate is told to count by its own audit. I did not run a browser, so which calls are really in flight is UNMEASURED.
8. Round count (loop over first lines of 711 `*STATUS.md`, 164 `GATE VERDICT`): matches for `mock-rows|visual|settle|e2e wait|frame\(` are B1280 (NO GO 1/2), B1289 (NO GO 2/2, the visual-round cap) and B1299 (GO WITH FINDINGS); control B1280 appears. No gate of this class.
9. Ports: `lsof` 9380-9399 listeners 0 (control all listeners 11); word-boundary scan of 34 non-.pre SEAT kits (14 of 6 Nov, 20 of 5 Nov) for `939[0-9]` 0 hits, `938[0-9]` 6 lines (the builder's own kit, the control); panes: `%43 Datasec/HPSM-POC-H130`, `%48 Datasec/NexusAI-G351`, no H128. Assigned 9390-9399.
10. Model/landing: `model-routing.md:109` G2, `:111` cap; `models_latest.json:23` `claude-sonnet-5-5`; landing `CLARIFICATIONS.md:3617`, `:5636` (C-299), `:5114` (C-263), records main `f529d3b4af20922b7504af36e11a6fe7478abac1`, 5669 lines. Last closed PR titles read (#281-#290).

## D-decisions
- D-1 New class "mock-rows e2e waits (a named wait per page)", NO GO 0 of 2: the visual-round class is at its cap and landed (C-296), but this branch is a tests-only follow-up of a different mechanism.
- D-2 The builder's file-second saving (about 12 s per project) is tiny against hosted job variance (tablet-2 8.1 to 18.0), so the time predicate is: test count per shard equal, head file seconds <= base, projection against the median of five main runs; a 90 percent main run is a Note for Tuesday, not this branch's defect.
- D-3 ADDENDUM-1 is relayed in the kit with the exact ticket clause, and the gate judges the reasoning with its own body-HTML diff and in-flight audit; it does not inherit Tuesday's acceptance.
- D-4 The gate runs the two shards that hold the file at the head (the e2e file changed, unlike B1322); the six other shards are not run.
- D-5 Own plants Y1-Y5 target per-condition necessity, the documents call, the required argument, and the status-count trap.

## Q-questions for Tuesday (each with a default)
- Q-1 Port block 9390-9399 (the builder's 9380-9389 also free)? Default: 9390-9399.
- Q-2 Tier 2 Sonnet (tests only, one file)? Default: yes.
- Q-3 Class name and "NO GO 0 of 2 before"? Default: yes, new class.
- Q-4 Hard stop Step 0 + 120, target + 90 (browser runs, two shards)? Default: yes.
- Q-5 Run the two holding shards at the head only? Default: yes.
- Q-6 Time predicate against the median of five main runs, and the 90 percent tablet-2 run a Note? Default: yes. Open point for Tuesday outside this gate: main's tablet-2 shard is near its 20-minute limit on some runs.
- Q-7 Documents frame accepted only if the gate's body-HTML diff holds? Default: yes.
- Q-8 `ready` required and `width` moved, against the ticket's "keep the optional argument": Note only? Default: yes (accepted in the builder's kit as D-1).
- Q-9 Main moved onto the review-door files and ci.yml comments: fine, as the kit's STOP list says? Default: yes.

## UNMEASURED
Which calls are in flight per frame (no browser run); the builder's 18/1/0 and 14/5/0 lag counts, plant results and file seconds; the shard counts at base and head; whether any status outside `main` holds "Loading the customer"; whether the `:83` narratives call changes the screen; the hosted time of the head's shards; the builder's STATUS body (only its last lines and line count were read); the planted controls for the ASCII and U+200B counts; the fetch of main by the gate's own trees.

## Outside the fences
One point: to read the ticket text I imported the project's own read helper `.tools/b1266/jira.py` (a builder-era tree under the project, GET only, token never printed) by `importlib` from a scratch script; the kit marks `.tools/b1312` and `wt-b1312-*` read-forbidden, but b1266 is an older seat's tree, so this reads outside the "project's own read helpers" in a loose sense. Everything else: DRAFTER_RULES, the B1322 and B1312 kits, report and slots, ADDENDUM-1, the builder STATUS tail and line count, `model-routing.md`, `models_latest.json`, STATUS first lines, `gh api -X GET` (ref, matching-refs, commit and patch, compare, raw contents, tree, actions runs and jobs, pulls, records CLARIFICATIONS), `lsof`, `tmux list-panes`, `df`, `uptime`. Wrote only the three B1324 files and scratch files in the session scratchpad. No decision_queue, no ledger, no briefs_staged, no Artifact, no mail, no az, no docker, no ssh, no HTTP to a hosted host.
