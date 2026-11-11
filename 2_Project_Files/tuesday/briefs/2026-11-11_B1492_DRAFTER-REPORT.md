STARTABLE: YES

# B1492 DRAFTER REPORT - SEAT-N123, NexusAI rd407-r2 "counted, not timed"

Drafter: Agent-tool drafter for Tuesday, 2026-11-11, reads 12:52:48 to 13:03:21 AEDT (`date`). Kit: `2026-11-11_B1492_SEAT-N123_nexusai-rd407-r2-counted-not-timed.md`, 125 lines, sha256 prefix `5a42308f7477`, `.pre-stamp` identical (`cmp` equal), four-underscore count 5 (four slots + last line).

## BLUF
- **The kit is a one-file, test-only fix.** M2, R1 and R3 keep the settings name missing for the whole call (`forMs: Infinity`, then `restore()`), and M2's "spent the budget" check counts the `Atomics.wait` timeouts the product asked for instead of timing it. `PAST_BUDGET_MS` is deleted. The 17 test titles stay byte-identical, so the counts file does not change and no counts commit is needed.
- **The proofs the kit requires:**
  - (a) 20 of 20 single-suite runs green with no shim, and 20 of 20 green under a 3x slow-sleep shim. Under that same shim the OLD cells must fail exactly M2, R1 and R3, 3 of 3. That is the control showing the old test depends on timing and the new one does not.
  - (b) Three planted product mutations in a scratch tree. P1 (missing read as absent) must turn M2, R1 and R3 red. P2 (unreadable read as absent in the auth snapshot) must turn R1 red. P3 (the retry loop cut to 2 steps) must turn M2 red on the counted budget.
  - (c) One full plain verify, from a non-dot tree, on the branch merged with main.
- **Finding for Tuesday (not acted on by the kit; it affects B1484):** a shim loaded with `NODE_OPTIONS=--require` does not reach the code jest tests. jest-environment-node 29.7.0 runs tests in a `vm` context that has its own `Atomics`. So ANSWER-3's exact-sleep shim was probably never live inside rd407-r2. That predicts:
  - "csp failed UNDER the shim" is not evidence that something beyond `Atomics.wait` runs long.
  - u-ci's pass "under the shim" was a near-threshold pass.

  The `shim live: true` line in `.tools/b1484/chain.sh:69` checks the outer realm only. This is PREDICTED inside jest, and MEASURED in a bare `vm` probe (below). The kit loads its shim with `--setupFiles`, the route the diagnosis used, and requires a liveness check inside the test realm on every shimmed run.
- **Model: Sonnet, row C2** (`model-routing.md:92`). The gate after this seat should be Opus (G2's "1st if ... a G1 surface", `:109`) because the cells pin a fail-closed auth decision. D1 has the alternative.

## Facts re-measured (instrument; control)
1. Origin main `0ab365b1db62c2b60cb63de9deb1ceccb0b1c4c9`.
   - Read by `gh api -X GET .../branches/main` at 12:52:48 and 12:59:48.
   - Tree `e828b519`; counts 5536/331 (`git show 0ab365b1:scripts/verify-expected-counts.json` in `.tools/b1484/clone`, which holds the commit; `cat-file -t` = commit).
   - The landed PRs #187 to #190 are listed. Open PRs: 0.
2. Test file at main: 540 lines, blob `faa6db5c`.
   - `PAST_BUDGET_MS` appears 4 times: `:45`, `:245`, `:319`, `:344` (`git grep -n -i`).
   - 17 `test(` lines and 5 top-level `describe(` lines (`/usr/bin/grep -c -E`).
   - The helper's defaults are `observations = Infinity, forMs = Infinity` (`:128`), and the window test is at `:138` (Read).
   - M3/M4 already spy on `Atomics.wait` (`:269`, `:292`) with the comment "Counted, not timed" (`:263-264`, `:288-290`, `awk NR`).
3. Product retry code at main (`git show | awk NR`), PRINTED:
   - `MISSING_RETRY_DELAYS_MS` at `:536`; `sleepSync` uses `Atomics.wait` at `:543-545`.
   - `_readRawWithEvidence` at `:2974`: the loop is at `:2991`, `waitedMs += delay` at `:2993`, and the two `return { missing: true, ...}` are at `:2987` and `:3008` (a fixed-string count gave 2).
   - The second loop of the same shape is `_stillAbsentAfterRetry` at `:3077`.
   - `authEnforcement.js` `settingsSnapshot` returns `{ state: 'unreadable' }` at `:86`, inside the readStoreStrict catch, and at `:93`, in the fallback path. The `createAuthEnforcedReader` null path is at `:809-815`, and `authGateDecision` at `:889-897`.
4. The `_refuseProtectedKeyLoss` re-read (`:3170-3179`) returns on `absent`. So under P1, M2's write goes ahead and changes the copies. That is the basis for "P1 makes M2 red" (PREDICTED).
5. **Shim realm probe**, PRINTED 12:5x with node v26.13.0, no jest and no files written: `node --require .tools/b1484/exactsleep.cjs -e` with a `vm.createContext()` printed:
   - outer `Atomics.wait` patched: true
   - the context's `Atomics.wait` patched: **false**
   - the context has its own `Atomics`: true
   - same object: false

   Source: `node_modules/jest-environment-node/build/index.js:85-93` (v29.7.0) copies only globals the context does not have. Control: the outer check reads true, so the shim itself loads.

   `chain.sh:69` (b1484) tests `Atomics.wait.toString().includes('hrtime')` in a plain `node -e`, which is the outer realm. `jest.config.js` has no `testEnvironment` key, so it is the jest 29 default, node (`grep -n -i` at main; control: `transform` 6 hits).
6. **verify-suite.sh predicate at main** (`git show | awk`):
   - A plain run fails if measured < committed (`:343`) or > committed (`:354`). So a plain PASS means the pair is equal.
   - `--update-counts` rewrites `_updated` every time (`:333`), which is why the kit forbids it in a tree the seat pushes from.
   - `--update-counts` is refused when `MIN_TESTS`/`MIN_SUITES` are set (`:234`).
7. **PENDING census**, 12:57:52 to 12:58:01: `gh api -X GET compare/main...<ref>` for each of 12 refs under `heads/b14`.
   - No ref touches the test file or `authEnforcement.js`.
   - revoke (`b1480/...session-revocation-clarification`) changes `jsonStorage.js` by +5/-1, in hunks at `:4066-4081` of base `3929b794`. A grep of that diff for `Atomics|MISSING_RETRY|_readRawWithEvidence|readStoreStrict` gives 0. The control: the same names occur at main (fact 3).
   - viewer-write-gates and setup-column-mapping change the counts file.
8. **Worktree slots** (helper formula, `test-server.js:89-93`, `SLOT_COUNT` 19; control `b1430-nodot/b1` = 6):
   - Slots in use: 0, 1, 5, 6, 7, 8 (10 trees, all b1484), 10, 12, 17 and 18.
   - Free: 2, 3, 4, 9, 11, 13, 14, 15 and 16.
   - Chosen: slot 14 (`old3`, `new44`, `mut24`, `v20`), band 28960-29599, which had 0 listeners at 12:56:41. The fallback `new12` is slot 4.
9. **Ports:** block 9940-9949 has 0 listeners (`lsof -nP -iTCP:9940-9949 -sTCP:LISTEN`; control: all listeners = 11).
   - The word-boundary scan of SEAT kits from 11-10 and 11-11 found 994x in 8 HPSM-POC kits of 11-10 and in none of 11-11's. Their panes are not live.
   - 9900-9909 belongs to live N122. The kit starts no server.
10. **Lock** (`ls` of the lock base, 12:56:54 and 12:59:50): held by `b1484-csp2`, pid 94198, since 01:54:36Z; queue 0.
    - Load: 3.29 at 12:56 and 3.20 at 12:59, on 18 CPUs.
    - Live panes: wednesday, NexusAI-N122, fleet-monitor, and two unnamed bash panes.
11. **Watcher:** sample lines `READY B1492: ...`, `HANDOVER B1492: ...` and `STOPPED: ...` fire a copy of `status_watch.sh:56`'s arms; `WORKING:` does not (`bash -c case`). The file is 64 lines, `284aa913306a`.
12. **Model ids** from `models_latest.json` (checked 07:13:31, warnings []): sonnet `claude-sonnet-5-5`, opus `claude-opus-5-5`. `brief_seat.sh:24` defaults to opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
13. **Identity** (lengths only):
    - The project checkout's repo-local email is 18 characters, contains "datasec" 0 times, and equals 1 of main's last 10 non-merge authors.
    - The b1484/b1480 clones' email is 46 characters, contains "datasec" once, and equals 6 of those 10 authors.
    - The kit copies the b1484 clone's identity (Q2).
14. **Name scan of the kit** (scanlib1114 person class, the underscore-aware form): 0 hits. Control: a planted `_by_<name>_` fired for each name.

## D-decisions (made at source; Tuesday may overrule)
- **D1 Sonnet (C2) rather than Opus.**
  - For: the table puts Opus on C3/C4 only. This seat makes no design decision, and the product is untouched. The mutation step guards against a weakened test.
  - Against: Datasec has no Sonnet trial rows yet (`model-routing.md:146`), and the seat must run a lock chain on a machine with odd timing.
  - **Recommendation: Sonnet, with an Opus gate.** Switch to Opus by changing the level word in the launch line and the Level paragraph.
- **D2 M2 counted instead of timed.** This tightens M2 rather than loosening it: P3 shows a cut-short loop is caught deterministically.
  - Cost: if the optional product hardening ever replaces `Atomics.wait` with a deadline loop, M2 (and M3/M4) must change with it. The kit says this in its out-of-scope line.
  - Alternative: keep `elapsed >= BUDGET`. It is one-sided and cannot fail on a slow host, but it cannot see P3 either.
- **D3 `forMs: Infinity` rather than a counted `observations: N`.** A counted N has to exceed every read the product makes, which is a number the product can change under the test.
- **D4 No new cells, and no budget assertion added to R1/R3.** This keeps the counts unchanged and the diff small. A later ticket could add counted waits to R1/R3.
- **D5 Main-moved handling:** merge main into the branch (no rebase), re-run steps 3 and 4 if the retry or auth files moved (C-68), then verify at M.

## Q-questions for Tuesday (each with a default)
- **Q1 (ANSWER-3 premise).** Should Tuesday re-read B1484's shim runs in light of fact 5? Default: yes, before any further ANSWER relies on "under the shim". After this fix lands, rd407-r2 should no longer need a shim at all.
- **Q2 Identity source.** Is the b1484 clone's identity the right one for this commit? It is the 46-character noreply address matching most landed lane commits. The project checkout's local one is 18 characters. Default: b1484 clone's, as the kit says.
- **Q3 HARD STOP.** Default: Tuesday stamps a clock at least 2 hours after launch. The FIFO is empty but N122 holds the lock; its csp2 run started at 12:54 and takes about 20 minutes.
- **Q4 Order against N122.** If N122 hands over (`HANDOVER B1484: next csp M after rd407 fix`), main will not move until this lands. Default: launch N123 now, so it queues behind csp2.

## UNMEASURED
- **Not run by the drafter:** any jest run (forbidden to a drafter; the lock is not the drafter's), the new cells themselves, and the shim inside jest. Every pass/fail in the kit's tables is PREDICTED. P2's effect on R3 and P3's effect on R1/R3 are UNMEASURED.
- **Load not exercised:** whether the new cells stay green under full-suite load on this machine. Only the one step-6 verify exercises that; 20/20 is single-suite.
- **Machine cause:** why this Mac's sleeps overshoot since the reboot (diagnosis: not proven).
- **Prebuilt binding:** whether a fresh `npm ci` gets a prebuilt sqlite3 binding. N122's did (RELAYED); the kit STOPs if not.
- **Watcher arms:** the `status_watch.sh` test used a copy of three arms, not the live script.

## Outside-the-fences disclosure
- **Reads:**
  - Read-only reads of Tuesday's briefs, the NexusAI B1484 STATUS, the B1480 kit, CLARIFICATIONS (grep), and `.tools/b1484` scripts and clone.
  - Git read verbs only (`show`, `log`, `grep`, `rev-parse`, `diff`, `merge-base`, `cat-file`, `config --get`) with `--no-optional-locks`.
  - `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`.
  - `ls` of the lock base, `lsof`, `tmux list-panes`, `uptime` and `sysctl`.
- **One `node` probe** (fact 5): an in-memory `vm` context with the b1484 shim `--require`d. It ran no jest, wrote no file and took no lock. It is a measurement, not a tool invocation for usage.
- **Two Bash calls the hooks refused** (a `cd` and an unquoted `====`), each re-issued without them; neither ran anything.
- **Writes:** only this report, the kit, and the kit's `.pre-stamp`. No Jira, mail, Artifact or publish.
