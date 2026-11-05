STARTABLE: YES (kit 36 long lines, 8 empty slots; ports 9250-9259 free; head is W5 33e39ab6 and PR #286 open, all read 10:05-10:07 AEDT 2026-11-05)
BLUF: a tier-2 Sonnet gate of 5 test/CI paths (171-line diff, read whole by the drafter). Judges scope, partition of the 686 test ids over 8 shards, 3 plants for the stat tile, a plateau sweep for the rail cell, one local run of 4 shards, and names the hosted facts Tuesday reads. Class is new (round 1 of 2).

## Facts re-measured (instrument; clock)
- Refs: gh api -X GET, 10:05:04: branch = 33e39ab68291e7949853864e760340b1aad2bcaf, parent fb84db8da91b..., main fc2bc2fc..., PR 286 open, 12 commits, open PRs 1. Files and +/-: the five paths as given, matched exactly.
- Class census, 10:07:03: 691 STATUS files, 158 with line 1 "GATE VERDICT", 2 name "visual round" (B1280, B1289), 0 name "CI fit". New class confirmed.
- Pointers at W5 (raw blobs by contents API, grep -n at 10:05-10:06): ci.yml:494 matrix, :487 timeout 20, timeout-minutes line count equal at both shas; e2e.mjs:52/:53; e2e-runner.test.ts:201 (toHaveLength(5) became toEqual of 8 names, stronger); mock-rows.spec.ts:78 test, :31, :37, :26 (one waitForTimeout left, in frame()); shell-sidebar.spec.ts:813 (470), siblings :807, :861; retries playwright.config.ts:50 (not in diff).
- Ports: 9250-9259 zero listeners (control 12 total listeners); word-boundary scan of 50 non-.pre- SEAT kits hit 0 (control 924x hit 1). Model: model-routing.md:109 G2 row printed; cap row :111; models_latest.json:23 claude-sonnet-5-5.
- Landing convention: main's last commits end "(#NNN)"; PR title is 129 chars with " (#286)".
- Builder STATUS exists (120 lines, first line READY @ 33e39ab6); the drafter read only its first 400 bytes; the kit tells the gate to read it only after predictions are hashed.

## D-decisions
- D-1: kit is 36 long lines (under the 50-70 target in count, over in width); each numbered step is one property with a control.
- D-2: the 45-minute budget is met by judging only deltas: no re-measure of the 11 earlier commits' round results.
- D-3: the gate re-sweeps 440-510 (not the builder's 462-484) so both plateau edges show.
- D-4: noted in the kit: the old "17 px shortens by 28" height claim is gone; now 17 px is caught by the computed-style assertion (P-C), 80 px by the height compare. The gate must say whether that is the same claim.

## Q for Tuesday (default)
- Q-1: may the gate read the builder STATUS after predictions? default YES.
- Q-2: squash subject 129 chars exceeds the usual 100 limit; kit keeps the PR title as instructed. default: keep, gate records length.
- Q-3: trailer on the squash body is Opus 5.5 though the seat is Sonnet (as instructed); default keep.

## UNMEASURED
Whether per-shard `--list` equals the unsplit list (the gate's step 3b); local wall time per shard; whether tablet twins pass; whether 470 is a plateau; runner fonts and CPU; the builder STATUS claims; CodeQL.

## Outside the fences
None. Reads: DRAFTER_RULES, the B1298 kit, B1289 kit and slots, G335 landing line (grep), model-routing.md, models_latest.json, gh api -X GET (commit, diff, contents, pulls, refs), STATUS first lines under Briefs, lsof, tmux list-panes. Scratch copies of W5 blobs are in the session scratchpad. No decision_queue, no ledger, no briefs_staged.
