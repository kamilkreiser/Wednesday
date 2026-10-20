# Gate 30 launcher report (2026-10-20, Tuesday's tooling sub-agent)

Launcher: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate30.sh` (692 lines, derived from gate 29's 792).
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B317_SEAT-G13_nexusai-gate-pr98-tier2.md` (not edited, not stamped).
Not done by design: no stamp, no routing line, nothing run without `--check`, no git write, no fetch/checkout/worktree in NexusAI (read verbs with `--no-optional-locks` only).

## CHANGES (also in the launcher header)
1. MODEL: `MODEL (tier 2;` prefix, must equal `levels.sonnet.model_id` (now `claude-sonnet-5-5`). Gate 29: tier 1 / opus.
2. 40: PIN-HEADS rows MAIN + B302 (B302 = branch `b302/test-code-codeql`, head 49ba21e, base 39653db, 8 commits). MAIN-STAMP form `landed since 39653db4: <text>`.
3. 18: the PR ref `refs/pull/98/head` must equal 49ba21e (REFUSE, exit 18). Gate 29 only NOTEd it.
4. 18M: 39653db is-ancestor of M0 (never `--first-parent`); M0 tree = stamped tree; none of the eight commits on M0 (so 49ba21e not on main); mode 0 iff M0 = 39653db (stamp must say `none`). Moved main refuses when what landed touches any of the 34 paths, or when the legacy stdout-only merge-tree shows any conflict marker (gate 29 tolerated the counts file; PR #98 does not touch it).
5. 7/8: eight-row chain (full sha + tree each, parent = previous row, row 1 parent = 39653db), 8 commits, 8 first-parent, merge-base = base.
6. 22: 34 paths = 33 M + 1 A (`__tests__/helpers/html-dom.js`); every path matches `__tests__/ | tests/ | scripts/test-*.js`; zero in the guarded set; sorted path list sha256 pinned (97161ee5…); the four files of the five open RD-786 sites unchanged base..head; html-dom.js blob pinned.
7. 93: lockfile, package.json, deploy-demo.yml, counts file are the same pinned blobs at M0 and head; head counts 4880/302; deploy-demo gates both jobs on `vars.CI_DEPLOY_ENABLED`.
8. 33L: refuses (deferred, last) only while a `qa-g29-*` ticket HOLDS the jest lock. Queued tickets of others pass with a NOTE. A `qa-g30*` holder or queued ticket refuses at once (exit 90).
9. Final refusal order: all three reasons print; exit 32 (SLOT) first, then 40 (route), then 33 (lock). Gate 29 exited 40 first.
10. Prompt rewritten from the kit (tier 2 through code, properties 1-8, rows r0-r9, S1-S7/A-D2, the PARKED line, verdict subject `... GATE VERDICT — gate 30`, g30/* refs, qa-g30- tags).
11. Kit-declaration lists (guards 12/19/53/71/76-82) rewritten to this kit's words; WRONG-list marker test also accepts RELAYED (kit item 6 uses it).
12. Gate-30 report path: `.../reports/<YYYY-MM-DD>-gate30-b302-pr98/report.md` from the kit's §11 line; refuses if it exists; the T4 and §11 dirs must match.

## Guards by disposition
KEPT: lock-tool sha256 pin 3c33f5ae… plus honours-BASE / `--replace` / jest kind / bash -n (90); T9-mounted refusal (18T); Laptop-DEV lock base present (90); load-8 NOTE; C-192 ls-remote retries; main/branch re-pin; report-exists refusal (17); NOT TESTED one-line (71); safe SESSION_SECRET printer (76); H-4/H-7/H-8/H-21 fragments; question/verdict routes and no-wednesday-agent@ (15/20); tuesday/wednesday pane + live negative-control derivation (38R); live-session refusal (86); stamp/route/lock refusals LAST; sqlite3 prebuild and notifier rulings; ANSWER-1 (load 8); gate-25 ADDENDUM-1; gate-27 report COMPLETE; C-190/C-209/C-63/C-192/C-40/C-76/C-112/C-174 quotes checked in CLARIFICATIONS and the kit.
CHANGED: see list above (model, pins, chain, paths, blobs, lock deferral, exit order, prompt, report path, builder panes now include `Datasec/NexusAI-L7`).
DROPPED (no counterpart in this kit): browser/Chrome/Playwright (96) and gate 27's browser instruments; SQL-spy / templates / riskSql blob pins and anchors; UNION/seed notes; C-57 and C-133 pins and the C57 shim (91); lock-file proxy-addr / playwright version checks; the RD-774 READY copy and ANSWER-20/21/23/24; gate 22-26 brief checks; belt, ruling (b), browser-driver and yield-retirement ruling files; PR #97 files and the 8-file list. The retired by-hand-yield phrases are still REFUSED if present, but the kit carries no positive retirement sentence so none is required.
ADDED: PR-ref refusal; per-commit chain; path-set/test-code/guarded classifier; RD-786 sites unchanged; builder STATUS must end with the READY line for 49ba21e (its sha256 is a NOTE only); moved-main overlap check.

## --check outputs (verbatim, trimmed)
`bash -n`: OK.

Real kit, unstamped, run once with `--check`:
```
NOTE: the Laptop-DEV jest lock is held now by 's101o-rd863-verify' (FIFO; the gate queues behind it, never touches it)
NOTE: 1-minute load is 9.89 (not below 8) ...
guards pass (9 40 18T 18 6 18M 7 8 90 22 93 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86); stamp, gate-29 lock hold and/or route NOT complete.
  ls-remote attempts this run: 1 (C-192); origin main 39653db (M0 39653db tree 704c442; ...; MODE 0); B302 49ba21e (tree 8a11504; branch and refs/pull/98/head agree; 34 paths = 33 M + 1 A, all test code, 0 guarded; lockfile/package/workflow/counts blobs = M0's); ...; model claude-sonnet-5-5
  PROVISIONAL (unstamped slots, --check ran against): MAIN(unstamped: ...39653db4b56a) REPORT_DATE(unstamped)
  NEG seats (38R, derived live; coordinator pane 'tuesday'): `78171` (Datasec/NexusAI-O); `6327` (tuesday);
REFUSING (40): no 'QA/NexusAI-gate30|tuesday-agent@agentmail.to|no' line in .../inbox_routing.conf ...
REFUSING (32S): 14 at-sign SLOT placeholder(s) remain in the brief (...)
EXIT=32
```
It is the SLOT refusal (32S), as required. Every other guard passed first (all 36 numbered guards listed), and the route line (40) is also reported because Tuesday has not added it.

RED arm (scratch copies only, in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/1fb5d5dc-d249-42bb-b16e-ea43221cd558/scratchpad/g30/`): kit copy fully stamped with main sha `0000...0001`, launcher copy pointed at it:
```
REFUSING: origin main is '39653db4b56a', not the stamped MAIN pin '000000000000' — main MOVED since stamp; re-stamp the MAIN pin (never sed a sha blindly)
EXIT=18
```
Control (same harness, correct stamp 39653db4 / tree 704c442b): `all guards pass`, EXIT=0, so the earlier refusals are not a harness artefact. A wrong stamped tree (`0000...0002`) refuses on the tree check: `M0 39653db's tree is '704c442b78a3', not the stamped tree '000000000000'`, exit 18.

## Could not derive / for Tuesday
- Not tested: the 33L lock deferral (a `qa-g29-*` holder) and the moved-main overlap/merge-tree branch; no safe way to create those states without writing a lock or moving main. Read-reviewed only.
- Kept the `ultrathink` opener and `--dangerously-skip-permissions` from gate 29; the kit does not say whether a Sonnet tier-2 seat should keep `ultrathink`. Your call.
- The kit's MODEL line is flagged UNVERIFIED by the drafter; the launcher checks it against the file (matches today: claude-sonnet-5-5).
- Builder STATUS sha256 (31c511ce…) is only NOTEd, not pinned. Kit has no "BY-HAND GATE YIELD IS RETIRED" sentence, so that positive guard is gone.
- Today the jest lock is held by `s101o-rd863-verify` (not a gate-29 ticket), so 33L does not trip; `--check` shows a load of 9.9, only a NOTE.
- Stamping reminders: `SLOT:RULING_T0..T5`, `MAIN_SHA` x2, `MAIN_TREE`, `MAIN_LANDED` (`none`), `REPORT_DATE` x2, both SELF-CHECK slots, and the routing line.
