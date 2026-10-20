# Gate 29 launcher RE-PIN report (4c9b0d3 -> 278afc2), 2026-10-20

Launcher: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate29.sh` (sha256 `b5431fcb75c6b008359616fc2420e9b69115c7355d6d16652c383b4ee4a7471e`).
Backup: `launch_qa_nexusai_gate29.sh.pre-repin-278afc2` (cp -p; `cmp` printed CMP_EQUAL; sha256 `c6b7da0e4a9f4e74956acf1bbf3379375600a43bf47d2dafbb8b63e8862bf320`).
READY copy: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-20_nexusai-gate29-READY-pr97-278afc2.txt`, 6572 bytes, **sha256 `da8baec1ceda051af1e8ca083e8c697eb76440ebeece4c9c2fcb6860bc55ec06`** (stdout of `inbox_digest.sh full` for the 010001a156fe... message, verbatim: From/To/Date/Subject, `---`, body; no key in it, grep-checked). It is NOT byte-identical to the seat's `mail-39-pr97-newhead.txt` (6352 bytes): the 220-byte difference is the digest's header lines.
The kit was not edited (sha256 `2e519e89...ccd`, unchanged). Reads of the NexusAI repo: `git --no-optional-locks` read verbs only (cat-file, rev-parse, show, hash-object --stdin without -w, merge-base, rev-list, log, diff --name-only).

## 1. Every pin changed (old -> new)

| pin | old | new |
|---|---|---|
| H774 (head) | `4c9b0d36993f1e78c8f23cd9e1216200550324b8` | `278afc25dda22ed8511d33e3e1cd12b0afde3487` |
| T774 (head tree) | `26f5dd7e632649c2ef33a97a5a73de1cf908975f` | `ee819f2126593465b352d91ae293fb3c55b9a75b` |
| FLOOR_MAIN (base / mode-0 main) | `7700cafd33ca8a329e1e7905081d869e83c6ccb5` | `39653db4b56adb6d4e526c90531cd4cdf23022e0` |
| FLOOR_TREE | `ba9581ab6d779e867edc066895f8481e5580691a` | `704c442b78a36baea66fef2349a5acbdbff114b5` |
| 7700caf kept as M7700 / T7700 | (was FLOOR_MAIN) | 360cd82's second parent, tree `ba9581ab...` |
| PIN-HEADS RD774 base / count | 7700caf / 3 | 39653db / 7 |
| MAIN-STAMP regex | `landed since 7700caf` | `landed since 39653db` |
| head chain | 4c9b0d3 <- 360cd82 <- 63bef65 <- 888203c | 278afc2 <- f1a2e76 (e884516 + 39653db) <- e884516 <- 2566713 (4c9b0d3 + 29c5ee8) <- 4c9b0d3 <- 360cd82 (63bef65 + 7700caf) <- 63bef65 <- 888203c |
| new chain members (full sha / tree) | - | f1a2e762215baf2ebf79b588747eaeff6c6af342 / 5c80bbcf1abc678a08fc6b51bd067d51111c59ee; e884516b719c1d6f37b377bd553cbcd1b9dd97c7 / 3571969baa7bc2fdbec8364a26750fc1ebd4618f; 25667136c22d308823f9e71e1295bc5e886decf6 / f5322b49a61c5269a0b4f9fbd194b72c27a68bfe; 29c5ee8f5fe42ec37b08c86ea5db20e8018182ab (2566713's second parent); 4c9b0d3 now H4C9 (previous head, tree 26f5dd7e) |
| commit counts | 3 over 7700caf, 5 over 888203c, 3 first-parent | 7 over 39653db, 21 over 888203c, 7 first-parent |
| GATED_774 list | 8 paths | unchanged (same 8; `diff --name-only 39653db 278afc2`) |
| paths_of base | 7700caf | 39653db |
| server.js blob | `05af86ceabfd0b012cdab6d75a1c4c3570212552` | `5fdf2912eceb186066e8c297c5234540eeaba25c` |
| rd774 test blob | `3a62151eab3e6261a27e8e84fa47bf23ffb99d95` | `0cfd42ee6fd1b8ae32c659f430cbcf9372e56321` |
| simpleDb / validators / riskSqlTemplates / spy / security-fixes / logSafe / package.json / lock / deploy-demo blobs | - | UNCHANGED (each re-read at 278afc25 with `git show | git hash-object --stdin`, also equal to `rev-parse`) |
| new equal-to-main blob guards (head AND 39653db) | - | authEnforcement.js `ca764a4b2c1f0349cf5891d71559d693c1104ec7`, jsonStorage.js `2abb5cf4...`, settings.js `adaa3400...`, testing.js `2b8af34f...`, testing.html `376bfee8...` |
| counts at main | 7700caf 4676/292 (`c1363118...`) | 39653db 4880/302 (`2cc094855c1215299ac15373262241dd71c64bff`); 7700caf kept as CB_7700 |
| counts at head | 4700/293 (`ff5f5d7e...`) | 4910/303 (`57659c6cfc51d7ddffeb3e8ed31f1b7db4ef901c`, same blob at f1a2e76); 4c9b0d3's ff5f5d7e kept as CB_4C9 with 4700/293; CB_360 unchanged |
| mode-a prediction | M0 + 24/+1 | M0 + 30/+1; mode 0 line "the head's own 4910/303" |
| ancestry / mode-0 | 7700caf + 888203c in M0's ancestry | 888203c, 7700caf, 39653db in M0's ancestry; **new: 39653db must be an ancestor of the head (exit 18)**; none of the 7 PR commits on M0; stamped-mode-0 requires "landed ... none" |
| anchors | settings route `(req, res)` without gate ~1 | gated form ~1 and old ungated form ~0; new `if (saveToDatabase && !(await requireAdminFor(req, res))) return;` ~1; `logSafe(` on 24 lines |
| READY_774 path / sha256 | `2026-10-19_...-READY-pr97.txt` / `ee6d589c...` | new file / `da8baec1...ec06`; content greps: head sha, `verify PASS 4910/4910 across 303 suites`, `PR #97 new head 278afc2` (old subject `READY FOR QA: ...` is not in the new mail) |
| other | - | ANSWER-26 and ANSWER-28 must exist; kit-declared strings `THE LOG LINE` -> `LOG SINKS`, added `THE NEW GATES`; brief must name the new trees/blobs in full and 2566713, e884516, f1a2e76, 29c5ee8 by 7-char short sha; WRONG-item marker filter also allows "drafter's actions"; prompt rewritten for head, chain, six routes, 23 log sinks, 4910/303, M1-M16, READY name, gate 28 complete |

A CHANGES block is in the launcher header.

## 2. Proofs

- `bash -n`: SYNTAX_OK.
- **`--check` on the real kit** (output trimmed; load/tmux NOTE lines omitted):
```
guards pass (9 40 18T 18 6 18M 7 8 90 91 22 93 96 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86); stamp, gate-28 lock release and/or route NOT complete.
  ls-remote attempts this run: 1 (C-192); origin main 39653db (M0 39653db tree 704c442; ancestry carries 888203c, 7700caf and 39653db; PR #97 not on M0; 39653db an ancestor of the head; MODE 0); RD-774/836 278afc2 (tree ee819f2; 7-commit chain ...); predicted verify mode 0: the head's own 4910/303; lock tool 3c33f5ae58e1...; c57 1ae84a108334...; c133 6f938bfcf255...; READY copy sha256 matches; Chrome 155.0.8059.84; model claude-opus-5-5
  PROVISIONAL (unstamped slots, --check ran against): MAIN(unstamped...) READY_SHA(the kit does not yet name da8baec1...) REPORT_DATE(unstamped)
REFUSING (32S): 20 at-sign SLOT placeholder(s) remain in the brief (...)
REFUSING (32S/READY): the kit does not yet name the new-head READY copy's sha256 da8baec1... (FILL AT STAMP ...)
REFUSING (40): no 'QA/NexusAI-gate29|tuesday-agent@agentmail.to|no' line in .../inbox_routing.conf ...
exit=40
```
  Every guard before the slot refusal passed (the whole 9...86 list above), including the ls-remote re-pin (main = origin 39653db, branch and PR ref = 278afc2), chain and trees, counts, blobs, anchors, READY sha/content, the gate-28/lock check (jest lock held by an `s101o-` hold, not gate 28), and the 38R negative controls (3 seats derived). Three refusals remain, all stamp-class: unstamped slots (32S), the kit not yet naming the READY sha (new, see 3), and the missing route line (40, Tuesday adds it).
- **RED arm** (scratchpad `.../scratchpad/red/kit_wronghead.md`: a copy of the kit whose PIN-HEADS RD774 head is `4c9b0d36...`; launcher copy `.../scratchpad/red/launch_red.sh` with only `BRIEF=` re-pointed):
```
REFUSING: PIN-HEADS RD774 is not rd-774-risk-sql-templates-s101o @ 278afc2, base 39653db (main at the 2026-10-20 re-pin), 7 commits — re-pin kit AND launcher
RED exit=40
```
  It refused on the head guard (40), as required.
- Extra arm (not asked): a scratch kit copy with the READY sha appended and a scratch launcher with all brief paths re-pointed drops the READY refusal and leaves only 32S and 40, so the deferral works.
- The `--check` was run several times while developing (syntax slips of mine, then two kit-text mismatches: the `drafter's actions` WRONG-item marker and renamed strings); the output above is the final run. `exit=40` was re-confirmed after the last one-word message fix.

## 3. Judgement calls and what was not derivable

1. **READY-sha-in-kit is deferred, not refused at guard 31.** The amended kit does not name `da8baec1...` (it cannot: the copy is saved now); FILL AT STAMP says Tuesday stamps it in. As a hard guard 31 refusal it would have hidden every later guard. It now sets STAMP_OK=0 with its own "32S/READY" message, so launch is still refused until the kit names the sha. The same file's content is checked (head, verify line, subject).
2. **The 2 forward merges' conflict sets are not measured by the launcher.** Only 360cd82's counts-only legacy merge-tree (guard 22) is kept. 2566713 and f1a2e76 are guarded by parents, trees and counts blobs; their merge-tree is the kit's r1 job (no `merge-tree` was run: the commission said read verbs, and the amend report left it unmeasured).
3. **Slot count reads 20, not 17.** The launcher counts every `@SLOT` text in the kit (as before); three are in explanatory prose. Unchanged method.
4. **Counts of 2566713 / e884516** (4757/296, 4763/296) are the amend report's, not guarded (my command to re-read them failed on a shell quoting slip; they are not needed by any guard).
5. **Kit shows only short shas for 2566713, e884516, f1a2e76, 29c5ee8**; the launcher requires the short forms in the kit and the full ones in its own pins (read from `cat-file -p` today).
6. **Still needed from Tuesday (unchanged):** stamp the 20 slots (MAIN pin probably `39653db4...`, tree `704c442b...`, landed `none`), name the READY sha in the kit, add the route line `QA/NexusAI-gate29|tuesday-agent@agentmail.to|no` after gate 28's in `inbox_routing.conf`. The `--check` NOTE "1-minute load 10+" means the gate would queue; the launcher does not refuse on it.
