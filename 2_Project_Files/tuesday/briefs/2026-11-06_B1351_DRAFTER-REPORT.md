STARTABLE: YES

# B1351 / SEAT-G360 drafter report (drafted 2026-11-06, reads 20:38 to 20:46 AEDT, writes after)

Kit: `2026-11-06_B1351_SEAT-G360_nexusai-roles-inventory-gate.md` (129 lines, 96750 bytes, 8 four-underscore lines: seven slots and the last line; non-ASCII 0; no person name, no card id). Slots: `2026-11-06_B1351_slots.json` (only drafter-measured facts plus `@NOW@`; no `@SEAT@`). Branch `b1344a/nexusai-roles-foundation-inventory` @ `7c5f1a39`, G1 on Opus, ports 9460-9469, pane `Datasec/NexusAI-G360`.

## BLUF
The branch is exactly what the builder says by the file list (six `A`, one `M` counts file, `+1839 -3`, `backend/` and `static/` untouched: `server.js` blob at main is `3a548f44`, the blob the builder says it restored). The gate is built around three risks: (1) the fence (spawn and dial) and what the builder's preload does NOT wrap, (2) the claim that a 205 x 4 table is "measured" when the Build checks only route keys, (3) the counts pair, written by `--update-counts` and never measured plain. Two facts change how the lane lands: main's counts blob equals the merge base's, so today the merge is clean and the pair is 5338/321 on both sides, BUT the log-sink lane will move the counts file and then this branch conflicts on that one file (serial landing, kit MAIN-MOVED rule (ii)). The merge also starts a `Deploy demo` run (scripts and `__tests__` are not ignored), gated by the repo variable.

## Facts re-measured (instrument; control)
- Pins: `ls-remote` branch `7c5f1a39`, main `58d5b616`, no `b1351*` ref. `compare main...head`: ahead 5, behind 2, merge base `e386ada9`; the 2 behind commits (`2f12875c`, `58d5b616`) touch `HISTORY.md` only. Files of `compare`: 6 `added`, `scripts/verify-expected-counts.json` `modified +3 -3`. Branch has a merge commit (`d59d698d`, 2 parents). All five commits carry the machine-default identity (`.localdomain`, unsigned). Main's last 30: 24 no-reply, 4 machine-default, 2 personal.
- Blobs: all six head blobs equal between `gh api` compare `sha` and `git hash-object` of the raw fetch. sha256 of each is in the kit.
- Counts (gh api raw, python): head 5338/321 (`dcac0671`), main 5332/320 (`1f2b1e58`). The census file has 6 `test(` blocks (grep -n lines 76, 82, 87, 96, 104, 117).
- PR #176: files list has no counts file; added lines hold 0 `test(`/`it(`/`describe(` (control: a planted `+  it(...)` line reads 1). Counts-neutral. Shares no path with the seven. It is the only open PR.
- Lock (ls, owner files, 20:41 and 20:45): held by `b1350-gate-verify-merge` since 20:33; queued `b1350-gate-verify-head` (20:15) and `b1340-build-proof` (20:34). Lock script sha256 and fence sha256 equal the sibling kit's. **Header of `nexusai-lock.sh` (MERGE-FIRST paragraph): a tag containing "merge" jumps ahead of the first waiting builder ticket.** The kit forbids that word in this gate's tags. The sibling gate's tag contains it (a fact for Tuesday).
- Panes: `tuesday`, `fleet-monitor`, `Datasec/NexusAI-G359`, `Datasec/NexusAI-N104`. N105A's pane is gone.
- Ports 9460-9469: `lsof` 0 (control: all-listen count 13); `-w -E 946[0-9]` over the 62 non-`.pre-` SEAT kits of 5 and 6 Nov: 0 files (control 945[0-9]: 1). `G360`/`B1351` words: 0 files; `session-tools/b1351`, `worktrees/b1351-*` absent. Hits: none.
- Round count: 160 STATUS files, 55 gate first lines, 12 NO GO, class pattern 0 hits (control line hits). New class, round 1 of 2.
- Model: `model-routing.md:108` is G1 (Opus 1st, Sonnet no), `:109` G2, `:111` G-cap; `models_latest.json:17` `claude-opus-5-5`, `:23` `claude-sonnet-5-5`.
- CI predicate: `build.yml:83-84` (blob `e4e5c095`). Deploy: `deploy-demo.yml:26-32` paths-ignore `**.md`, `docs/**`, `tests/**`; `:53` and `:91` hold the variable. Ruleset types: `deletion`, `non_fast_forward`, `code_scanning`, `required_status_checks`. Variables 0/0, environments `dev`.
- Hygiene (python over bytes; macOS grep has no `-P`): non-ASCII 0, TAB 0, CR 0 in all six; brief-token hits 4, all the sentinel `zz-b1344-none` (tool header `:38` and `:96`, data line 14, page line 10): a Minor by the kit's G-1. Control: `aé` reads 2.
- From the committed data (python, 205 rows): viewer 2xx writes 12, GETs 71; `open != administrator` 16 (14 under `/api/admin/*` at 403, `GET /api/auth/users` 401, `GET /api/user-data/export` 401); gate text but viewer not refused 4; refused with no gate text and no router gate 4 (+9 SCIM). These equal the builder's D8 lists.
- Fence reading (source only, NOT run): the preload patches 7 `child_process` functions and the promisified two, `dns.lookup` and `net.Socket.prototype.connect`. It does not patch `ChildProcess`, `process.binding('spawn_sync')`, `dns.resolve*`, `dgram`, or worker threads. In `server.js` those patterns read 0 and `child_process` is required inside two handlers at call time (`:19188`, `:19232`), so those two get the patched module. The metadata-IP call is `server.js:555` (axios, plain http). The rest of `backend/**` was NOT read: it is kit check C2 (g).
- Environment: the harness copies the caller's whole `process.env` and deletes 12 names; the tool blanks a second closed list. The kit makes that list's completeness a check (C2 f).
- Scan-count cause: the document's counts are at pin `15b1426f`, the builder's at a later base. The kit runs the stated frame at both shas (C5 b); I did not (needs the objects; the shared checkout is stale).

## D-decisions
- D1 The gate's drives always use `--out-dir` scratch (without it the tool overwrites the committed docs files).
- D2 Result tree verified before the head; both are required (Tuesday's ruling), and the kit notes they differ by one markdown file today.
- D3 Safety order for fence plants: spawn plants with canaries first, the dial ledger proved to discriminate with a loopback listener before any off-loopback plant, plants aimed only at `192.0.2.1`, no "without preload" control for a dial, no DNS plant, the restart-services route driven only with fake `bash` etc. first on PATH (control arm uses the fakes too).
- D4 The gate samples with its OWN client, its OWN minimal preload (proved by the same plants first) and a different sentinel, so a pass is not the builder's instrument agreeing with itself. Seed is derived from the predictions hash.
- D5 Y3 is a plant that must stay GREEN: a status edited consistently in the JSON and the page passes the census and `--check`. The kit grades that as a Note (a limit of the Build), because it is what permission work will lean on.
- D6 Counts conflict handling (MAIN-MOVED (ii)): the gate builds a derived resolved tree (main + six files, counts = main + 6 / + 1) and verifies it if the clock allows; the verdict is conditional and landing needs a counts-only re-merge and a new head.
- D7 One jest plants ticket, so the queue is paid once.
- D8 Lock tags `b1351-gate-ci`, `-verify-result`, `-verify-head`, `-plants` (no "merge").

## Q (each with a default)
- Q-1 Tier: the table reads tooling and tests as G2 (`:109`) and security surfaces as G1 (`:108`). Your two reasons (fence run, permission input) justify G1; the G2 note says a Sonnet G2 hands a security-shaped finding to G1. **Default: Opus.**
- Q-2 Clock: kit says wait up to 120 minutes per ticket, 30 s heartbeat, HARD STOP Step 0 + 300 minutes (a 120-minute wait, a 40-minute verify, plants, a drive). The sibling kit used 150. **Default: 300.**
- Q-3 Landing trailer: the kit says `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` because the file-writing seat is Opus. The sibling Sonnet gates use Sonnet 5.5; the branch head carries Sonnet 5.5. **Default: Opus 5.5.**
- Q-4 Is an attempted, refused, in-process dial to `169.254.169.254` (from `GET /api/setup/managed-identity`) a STOP line? The kit treats it as a fact and not a stop provided the dial fence is proved first. **Default: not a stop.**
- Q-5 The sibling gate's lock tag contains "merge", so it may have been placed ahead of the waiting builder. A fact, not a kit action. **Default: leave it.**
- Q-6 The 4 brief-token hits (the sentinel `zz-b1344-none` in committed files) are a Minor. **Default: Minor, not a refine reason by itself.**

## UNMEASURED by the drafter
Every plant colour and fence outcome (nothing was run; the kit's predictions are DERIVED); the duration of one full `--generate` drive; whether `ChildProcess`/`process.binding` are refused; the rest of `backend/**` against the fence's unwrapped forms; the 14+17+1+7 table against a fresh drive; the scan-count cause; the hosted Build and CodeQL (no PR); the Deploy demo run list; open code-scanning alerts on the seven paths; the environment-variable remainder. The Linux/Node 24 census run is unreachable until a PR exists.

## Outside the fences (disclosure)
No `cd` typed (one `(cd_not=1; ...)` subshell assignment, which is not a `cd`). Read-only: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (compare, pulls, files, contents raw, commits, rules, variables, environments, branches); `git ls-remote`; `lsof`, `tmux list-panes`, `ls`/`cat` of the lock directory and owner files, the lock script header; the NexusAI Briefs folder listing and first lines of STATUS files by python; the builder's STATUS-A and kit as instructed; the document `ITEMISED-CHANGES.md` lines by `sed`; `CLARIFICATIONS.md` and `EXPIRING-GRANTS.md` lines by `awk`/`grep`. Raw copies of head files and `server.js`/`build.yml`/`deploy-demo.yml`/harness at main were fetched to the session scratchpad `.../scratchpad/raw/`. I read no `fleet/briefs_staged`, no scoreboard, no ledger, no card, no WEDNESDAY/FRIDAY tree, no other project. Writes: the three files beside this report only.
