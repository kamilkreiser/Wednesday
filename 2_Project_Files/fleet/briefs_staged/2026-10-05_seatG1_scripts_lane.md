LAUNCH BRIEF (Seat G 1st): script-tooling lanes, eight Internal tooling tickets

# LAUNCH BRIEF: Seat G 1st, Secuura/Blockchain, pane `Secuura/Blockchain-G`. You are a NEW BUILD seat. No earlier Seat G exists, so you inherit no tool generation and no worktree. You work three file-disjoint script-tooling lanes from today's Internal tooling screen. L1 is `run-shell-suites.sh`: KS-1330, then KS-1331, then KS-1325. L2 is `preflight.sh` + `run-code-guards.sh`: KS-1127, KS-1153. L4 is `scripts/audit/*.mjs` + `lockfile-cleanroom.sh`: KS-829, KS-1209, KS-1394. Each PR carries one ticket (`Refs KS-NNNN`). You batch your READYs, merge each PR on a signed GO naming you, and never force-push. Three seats write refs beside you (B 61st, E 3rd, F 2nd). **All three run a lock tool that refuses an unattributed lock in code, and none of them names `.push-lock-g1` (P14).** So you take NO lock until Wednesday's ANSWER quotes their mirror ACKs, or rules each of those seats WRAPPED. From Wednesday

## PROVENANCE (measured 2026-10-05T07:37-07:46Z = 18:37-18:46 AEDT by Wednesday's drafter. Only read-only verbs were used in `!CODING`. Every write ran in the drafter's scratch `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/vclone`, a `git clone --shared --no-checkout` of the checkout. That covers merge-tree, hash-object, read-tree with a temp `GIT_INDEX_FILE`, and commit-tree. Nothing was fetched.)
PROVENANCE:
- P1 develop at origin = **`46c3e20cfbd21acee0c67d544180c33deaa4c8ef`**, unmoved since the screen (18:16 AEDT). Open heads: `refs/pull/1381/head` `82e6bfa9de85` (B lane, KS-1345); `1382` `80bafc849a54` (KS-1005); `1383` `7eccb131f2d6` (F 2nd, KS-1401, == `feature/ks-1401-tenant-isolation-after-039-f2-1`); `1384` `852fc9276320` (E 3rd, KS-1210, == `…-e3-1`). Highest PR is **1384**. 2,073 refs at 07:37:02Z, re-read at 07:45:42Z unmoved, rc 0 each | `GIT_SSH_COMMAND="$(git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" config --get core.sshCommand)" git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin` > `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/lsremote1.txt` | read 2026-10-05
- P2 Your token at origin: `-g1-` matches **1** pre-existing ref, `feature/ks-539-g1-split-ruling` (`47286a41a2ce`, 2026-08-05, "Kam's G-1 split ruling"). It is NOT yours. The segment-anchored `-g1-[0-9]+$` matches **0**. A `g` cannot occur in a hex SHA, so the hex-run trap that B 61st hit with `b61` cannot hit `g1`. Older lane branches exist and are FOREIGN (squash repo, none is an ancestor of develop): `feature/ks-1127-run-shell-suites-skip-tally-l4-skiptally-1` (#1234, merged as `e68e2f0e8`), `feature/ks-1153-l7-gate-records-918924925-run-code-guardssh-check-unreached` (#1056), `feature/ks-1209-preflights-closing-verdict-says-a-run-failed-on-the` (#1041) and `…-n41-3` (#1057). Origin has **0** heads for `ks-1330`, `ks-1331`, `ks-1325`, `ks-829` or `ks-1394` | `/usr/bin/grep -c -i -E` over `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/lsremote1.txt` + `git log -1` + `merge-base --is-ancestor` | read 2026-10-05
- P3 Lane files at develop (mode, blob12, lines): `Blockchain/Dev/scripts/run-shell-suites.sh` 100644 `85920863d704` 300 (== KS-1330's cited blob; `trap` 0, `| tee` at :268, verdict at :291); `scripts/__tests__/run_shell_suites.test.sh` `d000d7b65837` 513; `scripts/preflight/preflight.sh` `270b8913c009` 784 (`step()` :168-:183 with the `_hdr_total` parse at **:173**, not the ticket's :166; `_note_skip` **:204-:209**, not :197-:202; leg 14 :556-:647 calling the runner at **:643**; verdict block from `n_stack=` :693; `PREFLIGHT PASSED` :740; KS-1260's `on leg(s)… - fix` with an ASCII ` - ` at :711); `scripts/run-code-guards.sh` `2f06e19d3d33` 225 (advisory arm :145-:148, nested-basename loop **:197-:211**); `scripts/audit/baseline-contract.mjs` `ef82d7c5211d` 227 (`REQUIRED_FIELDS` :41, distinct malformed-`expires` shape :163-:169); `audit-gate.mjs` `8e236ee70ce1` 233 (`baseline[id]` :194-:198, CLEANUP filter on `scope` :203-:205); `audit-locks.mjs` `aff23b0420ce` 360 (`baseline[id]` :286-:290, regen pointer **:352**); `lock-discovery.mjs` `a2a9d9470ec4` 360 (malformed `expires` pushed into `missing` :282-:283, printed `missing …` :303); `lock-discovery.test.mjs` `f102d9d4c452` 193 (`expires: 'soon'` cell :184) | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-tree` + `show | cat -n | sed -n` | read 2026-10-05
- P4 🔴 **`scripts/lockfile-cleanroom.sh` does NOT exist at develop** (`fatal: path … does not exist`). The file is **`Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh`** (blob `518bffeeaf4a`, 133 lines; regen command printed at :120). So the screen's L4 file and KS-1394's row name a wrong path. L4's second file sits in L2's directory but is not an L2 file. `systemTest/performance/package.json:56` carries `"secuura-observability": "file:../../observability"`, the escaping `file:` link KS-1394 is about | `git ls-tree -r --name-only 46c3e20cfbd2 | /usr/bin/grep -i cleanroom` | read 2026-10-05
- P5 **Census of every origin head against the lane files:** 2,044 heads and pull refs; 1,791 resolvable in the shared store, 253 not. **100** non-ancestor heads touch a lane path. In the squash repo nearly all are merged PRs: #1376-#1379 and older touch `audit-baseline.json` or `lock-discovery.mjs` and are on develop as squashes. **The one recent head on `run-shell-suites.sh` that is NOT on develop is `refs/pull/1250/head` `2b8dcb824dd2`** (`feature/ks-1302-runner-tmpdir-residue-and-orphan-pipe-l5-1`, KS-1302 + KS-1303 RSSTRAP R2b, 2026-09-26): runner blob **`8eef1c4877b3`** (KS-1330's "round-2 runner") and test blob `9c4a87f0a97c`. **#1381-#1384 touch 0 lane paths** (`diff --name-only develop...<head>`). The GitHub open-PR list itself was NOT read | loop `git diff --name-only 46c3e20cfbd2...<sha> -- <lane paths>` over the `ls-remote` heads, output `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/lane_hits.txt` | read 2026-10-05
- P6 **#1250's state, from the board:** KS-1302's comment of 2026-09-25T20:38:33Z says *"CAP — NO GO at round 2 of 2. PR #1250 ships NOTHING and stays OPEN; nothing is built on it."* It names KS-1330 and KS-1331 as the residue. KS-1302 and KS-1303 are In Progress, project **None** (not in Internal tooling). Gate evidence for #1250 round 2 is at `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1250r2-t2d/` (report.md 747 lines; `evidence/1250_shellprobe.out` present) | Linear GraphQL read-only (`LINEAR_API_KEY` by name) + `ls`/`wc` | read 2026-10-05
- P7 **Merge predictions, MEASURED with synthetic commits** (`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/syn.sh`, output `syn.out`). L1 = #1250's two blobs on develop (tree `a3cbf98c0d7b`, == `merge-tree develop 2b8dcb824dd2` rc 0). L2 = edits at preflight.sh:173 and run-code-guards.sh:198. L4 = edits at baseline-contract.mjs:41, lock-discovery.mjs:283, audit-locks.mjs:352 and `scripts/preflight/lockfile-cleanroom.sh`:2. The KS-948 synthetic is B 61st's held payload `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-948-mixed-backtick-r3/out.md.checker/patch.diff` applied by `git apply --cached` (rc 0; its paths: `check_shared_relink.test.sh` + NEW `ks948_backtick_check_sees_mixed_names.test.sh`). **Results:** L1×KS-948, L2×KS-948 and L4×KS-948 each rc 0; L1×L2, L1×L4 and L2×L4 each rc 0; each lane × #1381, #1382, #1383 and #1384 rc 0 (12 pairs). **Firing control:** L1 against a same-file edit at run-shell-suites.sh:268 gives rc 1 naming `run-shell-suites.sh`. The docs were NOT simulated | `git -C /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/vclone merge-tree --write-tree --name-only` | read 2026-10-05
- P8 **Within-lane predictions, MEASURED** (`syn2.sh`, output `syn2.out`, same clone). KS-829 (audit-locks.mjs:287) × KS-1394 (:352) gives rc 0. 🔴 **But KS-829 × KS-1209 and KS-829 × KS-1394 give rc 1 on `Blockchain/Dev/scripts/audit/expected-case-count` whenever both move that one-line file.** KS-1127 (preflight.sh:643, :740) × KS-1153 (:173, :205, run-code-guards.sh:200) gives rc 0 | as P7 | read 2026-10-05
- P9 `scripts/audit/expected-case-count` at develop = **`59`**. Preflight leg 5 compares it with the node `tests N` total (`preflight.sh:386-:413`) and FAILS on MORE with *"update scripts/audit/expected-case-count to N in the same commit"*. `preflight_deps.test.sh:324-:371` pins that leg. Every L4 PR that adds a node test cell must bump this file. Leg 5 also needs `scripts/audit/node_modules` (semver), and FAILS without it (:390-:398) | `git show` + `git grep -n -i expected-case-count 46c3e20cfbd2` | read 2026-10-05
- P10 Doc `<h2>` numbers, flow doc: develop `1.`-`12.` (`</body>` :2067); #1381 head `…13.` (:2158); #1382 `…19.` (:2118); #1383 `…22.` (:2167); #1384 `…18.` (:2151). **`25.` and above appear on no open head.** 🔴 **Precedent: tooling PRs shipped NO doc block.** Neither doc names KS-1127, KS-1209, KS-1153, KS-1302, KS-1089, KS-1046, KS-926 or KS-1135 (0/0 each). #1234 (KS-1127) changed exactly 2 files, the runner and its test | `git show <sha>:"Projects Documents/…" | /usr/bin/grep -o -i -E '<h2[^>]*>[0-9]+\.'` + `/usr/bin/grep -c -i` + `git show --stat e68e2f0e8` | read 2026-10-05
- P11 Skill `.claude/skills/secuura-test-discipline/SKILL.md` at develop, blob `eaf43dfd4d98`. §4 :360-:419: *"Every test change updates its platform's two HTML docs, in the same commit … 'Test change' means backend unit, integration, or systemTest"*; :417-:418 *"If a change genuinely does not affect either doc, say so explicitly and why — do not silently skip."* §5d :507-:516: WHY + ticket on every changed line, ticket URL in the PR summary. §5f :540-:550: a runtime change is not Done on offline green; name what is unverified | `git show 46c3e20cfbd2:… | cat -n | sed -n` | read 2026-10-05
- P12 The eight tickets, read WHOLE (description + every comment + attachments), all assignee `kamil.kreiser@secuura.ai`, project **Internal tooling**: KS-1330 Backlog (3,382 chars, 0 comments); KS-1331 Backlog (1,226, 0); KS-1325 Backlog (3,340, 0); KS-1127 In Progress (2,468, 1 comment 2026-09-25 "#1234 is MERGED … leg-14-quotes bullet … still open", attachment #1234); KS-1153 In Progress (4,757, 0, attachment #1056); KS-829 Backlog (3,739, 0); KS-1209 In Progress (3,385, 1 comment 2026-09-18 "#1041 merged … lock-discovery.mjs Polish item is not addressed", attachments #1041, #1057); KS-1394 Backlog (2,070, 0). Raw JSON is in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/tickets.json` | `python3` urllib POST `https://api.linear.app/graphql` (queries only; one HTTP 503 retried) | read 2026-10-05
- P13 KS-1209's other residues at develop: N41-3 is pinned (`preflight_verdict_names_real_failures.test.sh` names it once); **N41-4's ASCII ` - ` is still at `preflight.sh:711`** (an L2 file). No shell suite calls `python3` (0 of the `scripts/__tests__/*.test.sh` files), and none uses `script -q` (0) | `git grep -l -i -E` at `46c3e20cfbd2` | read 2026-10-05
- P14 🔴 **Co-tenant lock tools, read by grep:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seat{B-61st,E-3rd,F-2nd}/raise/` hold 34, 34 and 8 `.sh`/`.py` files. **Each of the three has `unattributed_absent_or_stop`** (1 `.sh` each). Files naming `push-lock-g1` or `seat g 1st`: **0 / 0 / 0**. Control, `push-lock-e3`: 3 / 3 / 2. So your first take of `.push-lock-g1` is a STOP (E 3rd's rc 15) for every co-tenant | `/usr/bin/grep -l -i -E` | read 2026-10-05
- P15 Seat E 3rd's generation `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatE-3rd/raise/`: 43 entries, of which **34** match `e3(_[0-9a-z]+)?\.(py|sh)$`. Non-tool entries: `__pycache__`, `.my-last-release`, five `s-e2-ks1210-852fc9276320-push.*`/`-stubs.txt`, two `s-e3-ks938-79c87b8aaa48-push.*`. Constants: `locke3.sh` WAIT is **two slots**, `OTHER_LOCK` `.push-lock-56` and `OTHER_LOCK2` `.push-lock-f2` (:275-:276), with an empty-set refusal at :277-:285. STOP is 14 (`-e2 -55 -e1 -f1 -54 -d6 -d5 -c21 -d4 -d3 -d2 -53 -52 -51`), the same in `pushe3.sh:188 STOP_LOCKS_CHK`. The catch-all `unattributed_absent_or_stop` (:332-:353) builds its KNOWN set from `OTHER_LOCK`, `OTHER_LOCK2` and `STOP_LOCKS`, with rc 15. `namechecke3.py:69` has `MINE = "e3"`. `inbox_matche3.py:102` has `MINE = "e 3rd"`, and `:218` has `MY_PANE = "secuura/blockchain-e]"`. The successor fixture `(Seat E 4th)` is at `inbox_matche3.py:333-:334` and `trap4_e3.py:82-:83`. `bannerchecke3.py:78` has `GEN = "e3"`, `residue_audite3.py:89` has `PREV_GEN = "e2"`, and `raisee3.py:43` has `REC` = E 3rd's folder, with `:177` `s-e3-{A.tag}`. 🔴 **Live defaults that point into E 3rd's session:** `armse3.py:65` `ARMS_E3_SCRATCH` default `/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/ef94782d-5409-4df7-b941-7e9eb00bbb67/scratchpad/armse3`, with `:140/:267/:275` setting `MERGE_E3_SCRATCH`; `mergee3.py:119-:120` `MERGE_E3_SCRATCH` default `…/ef94782d-…/scratchpad/mergee3` | `ls -1A` + `/usr/bin/grep -n -i -E` + `sed -n` | read 2026-10-05
- P16 Floor at 07:44:29Z: `worktrees/` 494 entries; **`.push-lock-e3` PRESENT**, holder `{"seat": "Secuura/Blockchain-E e3", "pid": 91512, "branch": "feature/ks-938-mfa-disable-nulls-the-seed-and-backup-codes-e3-2", "started_utc": "2026-10-05T07:37:42Z"}`. pid 91512 is ALIVE (`bash ./pushe3.sh … s-e3-ks938 …`, 08:03 elapsed). No other `.push-lock-*`. `s-e3-ks938` and `s-f2-ks1401` are present; **0 `s-g*`** worktrees. Panes per `tmux list-panes -a`: `%0` `%1` `%26` `%27` `%29` `%30` `%31` (`%31` titled `KS-1401 migration 049 tenant isolation gate61`); which seat holds which pane is UNMEASURED | `ls -1A` + `cat holder` + `ps -p` + `tmux list-panes -a` | read 2026-10-05
- P17 🔴 **Two co-tenants have written handovers.** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatF2-2026-10-05.md` (293 lines, mtime 07:21:07Z) is "#1383 raised, NOT merged … holding for gate61", and `history.md:24` carries F 2nd's entry. `HANDOVER-seatE3-2026-10-05.md` (191 lines, mtime 07:40:20Z) is "(COLD) … TWO PRs RAISED (#1384 KS-1210, and KS-938)", with KS-938 **MUST NOT LAND BEFORE #1382** and KS-1256 the NEXT row. E 3rd was still mid-push at P16. Whether E 3rd and F 2nd are LIVE, WRAPPED or succeeded is UNMEASURED | `wc -l` + `stat` + `sed -n 1,40p` | read 2026-10-05
- P18 Seat name: `history.md` 19,100 lines; bounded `seat g [0-9]` **0** lines (control: `seat e 3rd` 2); 0 `seatG`/`HANDOVER-seatG*` entries in `5_Project_History/`. **You are Seat G 1st** | `/usr/bin/grep -c -i -E` + `ls` | read 2026-10-05
- P19 Seat C 24th's brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatC24_verify_close.md:57` lists **Seat G 1st** with exactly your eight tickets (board-only seat, closes ALREADY-DONE? rows). Seat C 23rd's move list has all eight rows | `/usr/bin/grep -n -E` | read 2026-10-05
- P20 Gate kits `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/`: `2026-10-05_gate58`, `gate59`, `gate60`, `gate61`, `gateD2`. **None is yours.** Your gate number is Wednesday's | `ls` | read 2026-10-05
- P21 Inputs: STANDING_LINES `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` 398 lines, sha256 `ccc5499dd2ed9ac6…`, newest line **:398** "Unattributed push locks … must be CODE in the lock tool"; screen `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-05_internal-tooling-screen/SCREEN.md` sha256 `644311ad1fd6680e…`; `screen.tsv` sha256 `0b1f062c90ddc55b…`; shape briefs `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatE3_successor.md` (260 lines) and `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatB61_successor.md` (amendments A1-A7 at :5-:12) | `wc` + `shasum -a 256` + Read | read 2026-10-05
- P22 `df -m /Volumes/DevMASTER`: **720,363 MiB** free | `df -m` | read 2026-10-05

**UNMEASURED by the drafter:** every suite, red-first, preflight and `check:openapi` figure at any SHA (nothing was executed); the GitHub open-PR list and #1250's current state on GitHub; whether E 3rd and F 2nd are live; which pane each seat holds; your ctx and pane id; whether `/usr/bin/python3` is visible inside the pre-push hook environment.

---

## BLUF
You are **Seat G 1st** (P18). develop is **`46c3e20cfbd2`** (P1). Your three lanes are **file-disjoint** from each other, from #1381-#1384 and from B 61st's held KS-948 payload. The firing control fired (P7). **Two couplings are not textual:**
1. L1 changes the runner that **every seat's pre-push leg 14 runs** (`preflight.sh:643`), and the runner globs `scripts/__tests__/*.test.sh`. B 61st's KS-948 suites and F 2nd's `ks1401_049_tenant_isolation_after_039.test.sh` are therefore run BY your runner. That is a behavioural coupling, not a merge conflict.
2. Inside L4, every PR that adds a node test cell moves `scripts/audit/expected-case-count`. That file conflicts between any two such PRs (P8).

**Your queue: EIGHT PRs, one ticket each.**

| # | Ticket line | Files (develop paths, P3/P4) | Depends on | Tier (PROPOSED, Q-TIER) | Flow `<h2>` |
|---|---|---|---|---|---|
| 1 | `Refs KS-1330` | `Blockchain/Dev/scripts/run-shell-suites.sh`, `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` | — | **T1** (pre-push gate) | **`25.`** |
| 2 | `Refs KS-1331` | the same two | KS-1330 MERGED | **T1** | **`26.`** |
| 3 | `Refs KS-1325` | `run_shell_suites.test.sh` + NEW PTY harness under `Blockchain/Dev/scripts/__tests__/` (name at build) | KS-1330 MERGED | **T2** (ticket's own proposal) | **`27.`** |
| 4 | `Refs KS-1127` | `Blockchain/Dev/scripts/preflight/preflight.sh` (leg 14 :643 + verdict :693-:762) + NEW suite under `scripts/__tests__/` | — | **T1** (pre-push verdict; precedent #1041 tier 1) | **`28.`** |
| 5 | `Refs KS-1153` | `preflight.sh` (:173, :204-:209), `Blockchain/Dev/scripts/run-code-guards.sh` (:197-:211 comment or code), `scripts/__tests__/run_code_guards.test.sh` + a preflight suite cell | — | **T1** | **`29.`** |
| 6 | `Refs KS-829` | `Blockchain/Dev/scripts/audit/audit-gate.mjs` and/or `baseline-contract.mjs` (F1 only, Q-829) + a `.test.mjs` + `expected-case-count` | — | **T1** (audit gate verdict) | **`30.`** |
| 7 | `Refs KS-1209` | `Blockchain/Dev/scripts/audit/lock-discovery.mjs` (:282-:303), `lock-discovery.test.mjs`, `expected-case-count` | — | **T2** (message polish) | **`31.`** |
| 8 | `Refs KS-1394` | `Blockchain/Dev/scripts/audit/audit-locks.mjs` (:352 + a command builder), `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh` (comment only, Q-1394), a `.test.mjs`, `expected-case-count` | — | **T2** | **`32.`** |

- **Doc blocks are numbered by TICKET, in queue order: `25.` KS-1330, `26.` KS-1331, `27.` KS-1325, `28.` KS-1127, `29.` KS-1153, `30.` KS-829, `31.` KS-1209, `32.` KS-1394.** These follow B 61st's `24.`; nobody holds `25.`+ (P10). Nobody renumbers and a gap is never closed. If Wednesday rules Q-DOC (b), the numbers stay reserved and unused. **Precedent (P10): tooling PRs #1234, #1041 and #1056 shipped NO doc block. Q-DOC asks which rule applies.**
- **Build order (PROPOSED, Q-ORDER-G1) differs from number order:** row 1 → rows 4, 5 → rows 6, 7, 8 → rows 2 and 3 only after KS-1330 is ON develop. KS-1331 and KS-1325 both need KS-1330's trap; develop has none (P3). A stacked PR leaves a no-op file in its three-dot set (STANDING_LINES :311), so you do not stack.
- **Budget:** never START a build past **~45%** ctx; hand over COLD at **~62%**. The handover names the NEXT row and records every built commit (head, tree, trailer proof, pathgate) as UNPUSHED unless pushed. Read ctx off your OWN statusline; if you cannot, write "Please read my ctx." Never estimate it. Read files by line range; never `cat` either HTML doc, the YAML or a lockfile. **Never end a turn on a "next up" line with nothing running** (STANDING_LINES :338).
- **READYs are BATCHED:** batch 1 = row 1 + every L2/L4 row built by the ~45% line; batch 2 = rows 2-3 once KS-1330 has merged (likely a successor's).

**The queue:** ITEM 0 plan confirmation (STOP for the ANSWER) → ITEM 1 copy + hand-fix tools → ITEM 2 build row 1 → ITEM 3 build rows 4-5 → ITEM 4 build rows 6-8 → ITEM 5 predict, push, raise, ONE READY (batch 1) → ITEM 6 merge on each GO → ITEM 7 rows 2-3 (when KS-1330 is on develop) → handover + WRAP.

🔴 **ARM `inbox_watchg1.sh` IN THE BACKGROUND AT BOOT, BEFORE ITEM 0's MAIL** (`timeout: 7200000`, as a tracked background job). Re-arm after EVERY match and before the 2 h lapse (:361). The inbox `secuura-blockchain@agentmail.to` is SHARED by every Secuura pane. Before acting on any GO or ruling: list the inbox by API and confirm the subject, the timestamp, and `spf`/`dkim`/`dmarc` pass from the structured `authentication_results` (else UNVERIFIED). One clean poll at the same second as a message proves nothing (:367).

**Authority:**
- **Kam, live board 2026-10-05 18:14:26:** *"run cloud and local agents as hard as possible to action these"* — the 160 Internal tooling tickets (SCREEN.md :3-:4).
- **Kam's 2026-09-13 as-many-agents rule:** run as many seats as there are file-disjoint lanes. The screen's lanes are pairwise disjoint (SCREEN.md :34-:36), re-measured with merge-tree in P7/P8.
- **Kam's delegated-merge grant 2026-09-11** ("We approve and merge our own TESTED Platform K work"). Each merge happens on a gate's GO from Wednesday naming the head SHA (repo `CLAUDE.md` Merge flow :270).

**Seat identity (PROPOSED for ITEM 0 to confirm):**
- **Pane** `Secuura/Blockchain-G`. Subject prefix `[Secuura/Blockchain-G -> Wednesday] `. **Every subject names `(Seat G 1st)`.** Routing tokens appear ONLY as the leading tag, never mid-subject. Read your pane id from `$TMUX_PANE` (:394), never from a bare `tmux display -p`.
- **Record folder** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatG-1st/` (small text files only; it does not exist yet, P18).
- **Token `g1`, tool suffix `g1`, lock `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-g1`.**
- **Branches** `feature/ks-<n>-<slug>-g1-<k>`, with k = the row number (1 KS-1330 … 8 KS-1394). Match your refs ONLY by `-g1-[0-9]+$`; `feature/ks-539-g1-split-ruling` is FOREIGN (P2). **Worktrees** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-g1-ks<n>`, each created with `git worktree add --detach <abs> <base>` (never `-b`), only after the ANSWER, under THE LOCK RULE. **No adoption:** `EXPECTED_ADOPTIONS = 0`, with a tamper (a planted `s-e3-x` reads FOREIGN).
- `lockg1.sh` REFUSES without `LOCK_SEAT` (`'Secuura/Blockchain-G g1'`). Take and release in ONE invocation under a `trap … EXIT`; release with the HOLDER FILE's pid, never `$$`. **`pushg1.sh` takes `.push-lock-g1` ITSELF, so call it BARE** (:373).
- 🔴 **zsh:** read rc on its own line straight after the command (`cmd > "$REC/x.log" 2>&1; rc=$?`), never through a pipe and never after an `echo`. Never `cd`; use absolute paths; `TZ=UTC stat`; never name a zsh variable `path`. **Brace before `:`** (`"${BASE}:Projects Documents/…"`), and quote `Projects Documents` everywhere. **Never build a mail body in an UNQUOTED heredoc.**
- Use `git cat-file -e` with a nonexistent-path control, never `rev-parse <rev>:<path>` (:314). **Never `git push --dry-run`** (:382).
- 🔴 **NO FORCE PUSH, ever; no `ALLOW_FORCE`. Catch up by MERGING develop IN, never by a rebase** (:395; `.githooks/pre-push:46-70`).
- 🔴 **In a fresh worktree, run `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared` and ASSERT `packages/shared/dist/index.js` exists BEFORE the first test AND before any push** (:376, :396). Never trust the rc. Leg 14 runs ALL shell suites inside the pushing worktree, ks949 included. **L4 also runs `npm ci` in `Blockchain/Dev/scripts/audit/`** and asserts `scripts/audit/node_modules/semver` exists, or leg 5 FAILS on the environment (P9).

## 🔴 CO-TENANTS — the partition, from BOTH sides
| | **Seat G 1st (you)** | **Seat B 61st (FOREIGN)** | **Seat E 3rd (FOREIGN)** | **Seat F 2nd (FOREIGN)** |
|---|---|---|---|---|
| pane / tag | `Secuura/Blockchain-G` / `[Secuura/Blockchain-G -> Wednesday] ` | `Secuura/Blockchain` / `[Secuura/Blockchain -> Wednesday] ` | `Secuura/Blockchain-E` / `[Secuura/Blockchain-E -> Wednesday] ` | `Secuura/Blockchain-F` / `[Secuura/Blockchain-F -> Wednesday] ` |
| token / tools / lock | `g1` / `*g1` / `.push-lock-g1` | `b61` / `*56` / `.push-lock-56` | `e3` / `*e3` / `.push-lock-e3` (PRESENT at P16, live pid) | `f2` / `*f2` / `.push-lock-f2` |
| refs | `-g1-<k>`, `s-g1-*` | `-b61-<k>`, `s-b61-*` (0 at P16) | `-e3-<k>`, `s-e3-*` (#1384, KS-938's `-e3-2`) | EXACTLY `feature/ks-1401-tenant-isolation-after-039-f2-1` (#1383) |
| product files | the eight rows' files above, ONLY | merge #1381 (originate `routes/webhooks.ts`); originate `documentRepo.ts`, `routes/documents.ts`, `routes/adminConfig.ts`; root `observability/.env.example` + `observability/config/alerting.env.example` + `scripts/__tests__/prometheus_targets.test.sh`; `anchoring.openapi.ts` + REGENERATED `docs/openapi/secuura-api.yaml`; KS-948 `scripts/__tests__/check_shared_relink.test.sh` + NEW `ks948_…test.sh`; KS-591 `nft-certificate`/`staking`/`billing`/`tenant-provisioning` `*.openapi.ts` carves | auth `routes/oauth.ts`, `routes/mfa.ts`, `routes/users.ts` (disable site), ks1210/431/451/938 tests; api-gateway `routes/verification.ts` (KS-1256, next row) | `Blockchain/Dev/migrations/049_ks1401_tenant_isolation_after_039.sql` + `scripts/__tests__/ks1401_049_tenant_isolation_after_039.test.sh` |
| doc blocks | `25.`-`32.` | `13.`-`17.`, `23.`, `24.` | `18.`, `20.`, `21.` (`19.` = #1382, E lane's to merge) | `22.` |
| your rule toward it | **WAIT on `.push-lock-56`** | — | **WAIT on `.push-lock-e3`** | **WAIT on `.push-lock-f2`** |
| its rule toward you | **today: `.push-lock-g1` = UNATTRIBUTED = STOP (P14)**; needs the mirror (Q-LOCK-G1) | — | the same | the same |

- **Seat D 7th** (`Secuura/Blockchain-D`, token `d7`, NO git lock): kintsugi DEPLOY of develop + live sweep. It writes no refs. A `.push-lock-d7` is UNATTRIBUTED: STOP and mail. Deploying is never yours.
- **Seat C 24th** (`Secuura/Blockchain-C`, token `c24`, no lock): Linear BOARD ONLY. It verifies and closes ALREADY-DONE? rows, and its partition names your eight tickets (P19). **You change NO ticket's state, project, assignee or label.** If one of your tickets moves under you, report it and never revert it. KS-1089, KS-1135 and KS-1302 sit on your runner's history; they are C-lane or Kam's, never yours.
- **Measured disjointness (P5, P7):** no lane path is touched by #1381-#1384 or by the KS-948 payload; every cross pair has merge-tree rc 0, and the same-file control has rc 1. **L1 vs KS-948 is NOT a textual conflict.** `check_shared_relink.test.sh` (B 61st) is RUN by your runner, so a B 61st push runs YOUR runner once KS-1330 lands, and yours runs B 61st's suite. If a co-tenant's suite reads red under the new runner but green under develop's, that is a STOP and a mail (it would be your runner's behaviour, e.g. KS-1330 item 3: suites start with SIGINT ignored and stdin at `/dev/null`).
- **The two platform-k docs are NOT disjoint** if Q-DOC (a) is ruled: every tail block conflicts with every other. Resolution is only by THE DOC PROTOCOL.
- **Not lane-disjoint inside the screen (P5 + `screen.tsv`):** KS-1090 (CLAUDE-LANE `services/*/tsconfig`) also lists `preflight.sh`, and KS-1014 lists "`start-secuura.sh` (or `scripts/preflight/preflight.sh`)". KS-1292 and KS-1300 (`preflight.sh` + `.githooks/pre-push`) wait for Kam's KS-884 card and are **OUT**. None of these is raised (0 origin heads); if one is, STOP and mail before your next ref write.
- **`-E` and `-F` carry older seats' mail.** Everything of B 61st, E 3rd, F 2nd, D 7th, C 24th and the gates is FOREIGN. Never read, edit or quarantine anything in their record folders except the ONE tool copy of ITEM 1.
- **develop is SHARED.** On every move, read WHAT moved first (`git diff --stat old..new` against your paths, :257). Landings ahead of yours: #1381 → #1382 → #1384 → KS-938 is the E-lane order (E 3rd's handover §2); where #1383 falls is UNMEASURED: re-read at every prediction.

## 🔴 THE LOCK RULE (two-way)
- **Every ref write** (a ruled fetch, worktree add/remove, commit, merge-in, push, merge) needs: **`.push-lock-g1` HELD by you; `.push-lock-56`, `.push-lock-e3` AND `.push-lock-f2` ABSENT; NO other `.push-lock-*` (enforced in CODE, STANDING_LINES :398).**
- **Take order:** check all three WAIT locks absent → take yours atomically → RE-CHECK all three → if any appeared, RELEASE yours, back off 30-90 s (randomised) and retry. Never hold yours while waiting.
- **WAIT** on a live `-56`, `-e3` or `-f2`: print the holder record and the wait, **bounded at 20 min per ref write**, then STOP and mail. A stale lock (heartbeat > 5 min AND a dead pid) is a STOP and a mail; **report it, never remove it.**
- **STOP immediately, each with its own rc (14 declared):** `.push-lock-e2`, `-55`, `-e1`, `-f1`, `-54`, `-d6`, `-d5`, `-c21`, `-d4`, `-d3`, `-d2`, `-53`, `-52`, `-51`. **Plus the catch-all in code:** any `.push-lock-*` that is not yours, not one of the three WAIT names and not one of the 14 is UNATTRIBUTED. That includes `-d7`, `-c24`, a successor's `-e4`/`-f3`/`-b62`-generation lock and `-g2`. It gets its own rc, names the dir, and your lock is NOT taken.
- **Hold short:** your lock covers the ref write ONLY, never `npm ci`, a build, a suite or a red-first. Report each push's hold time.
- **Re-prove with `twolockg1.sh` against an EMPTY scratch dir, never the real `worktrees/`.** The arms:
  - nothing planted → taken;
  - each WAIT lock live (`-56`, `-e3`, `-f2`, three arms) → WAITS, then takes when it is removed within the bound;
  - one never removed → STOP at the bound, shortened by a PROVEN env override (set == read);
  - a WAIT lock injected between take and re-check (one arm per WAIT name) → you RELEASE and your file is gone;
  - a stale `-e3` → STOP, and the planted file is still present;
  - each of the 14 STOP locks → refused at the STOP rc naming the file, yours NOT taken;
  - an unknown `.push-lock-zz9` → refused at the UNATTRIBUTED rc, yours NOT taken;
  - a clean floor → passes, printing how many dirs it CHECKED.

  Print the counts CHECKED (14 STOP + 3 WAIT + catch-all). `lockg1.sh` and `pushg1.sh` STOP and WAIT sets must be **byte-identical in the same order**. Drive every refusal.

## 🔴 THE DOC PROTOCOL (applies only if Q-DOC (a) is ruled)
1. **Same commit, never a follow-up** (skill §4 :362). One NEW self-contained block per ticket in BOTH platform-k docs: flow `<h2>` `25.`…`32.` per the mapping, and cheat sheet as unnumbered `&mdash; KS-NNNN</h2>`. Insert immediately before `</body>` (develop flow :2067; re-read at your base). Never write or edit another block.
2. **Timings STATED, not added** (§4 :380-:412): if your change alters what leg 14 runs or how long it takes, state the measured figure with date and HOST, or say "no stated timing covers …" with the grep, the regex printed, and a must-hit control.
3. **Number order on every merge-in, whatever merged first:** `13.`…`24.` sit ABOVE `25.`; your own are in ascending order.
4. **Catch up by MERGING develop IN** (never a rebase, never a force push), ONLY on a ruling naming that PR. Resolve ONLY the two docs (and, in L4, `expected-case-count` by RECOUNT, Q-COUNT), and assert every other path auto-merged (`git merge-tree --write-tree` rc and conflict paths VERBATIM). **Any conflict outside those is a STOP.**
5. **Q-M** (gate57 §3): a merge-in head is covered by its gate when all of these hold:
   - M1: its tree == the prediction computed on ACTUAL develop;
   - M2: it has two parents, [gated head, that develop];
   - M3: `show --remerge-diff --name-only` names only the declared files;
   - M4: 0 trailers;
   - `rev-list --count <new> --not <gated> <develop>` == 1.

   Anything else re-gates.
6. **Predict in your own `git clone --shared` SCRATCH clone** (never the shared store) against develop AS IT STANDS, chained after every open PR ruled to land before yours. Print each predicted tree and the per-doc block order read back from it.

## 🔴 NAMESPACE AND MATCHER, generation `g1`. A NEW letter has NO generation of its own: COPY Seat E 3rd's `*e3`, then HAND-FIX
- **Source (PROPOSED, Q-GEN):** E 3rd's 34 `*e3` tools in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatE-3rd/raise/` (P15). It is the only generation measured to carry the unattributed-lock catch-all **and** to have run against today's co-tenants. **Copy ONLY the 34 tool files** into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatG-1st/raise/`. Do NOT copy `__pycache__`, `.my-last-release` or any `s-e2-*`/`s-e3-*` round record. **Copy after E 3rd's WRAP mail** (its folder was in use at P16). Record the source sha256 of each file at copy, and re-hash after.
- Hand-write `rekeyg1.py`: its own map, no bare literal of either generation, no seat token. Assert coverage BEFORE any write; run refusal controls first. **Lineage ACCUMULATES:** `e3` becomes FOREIGN, not deleted. 🔴 **A blind `e`→`g` map is WRONG here.** `blockchain-e]`, `(Seat E 2nd)`, `(Seat E 3rd)`, `(Seat E 4th)` and the `-e3-<k>` refs are real FOREIGN fixtures that must STAY E. Re-key only what names THE TOOL'S OWNER.
- 🔴 **`rekey_check*` is INERT on a lettered generation** (E 2nd §6; P14 of E 3rd's brief): this re-key has **no independent auditor**. **State that in every READY** (Q-RK).
- **HAND-FIXES no re-key produces. Each needs a before/after in YOUR receipt, and each must be driven:**
  1. 🔴 **THREE-lock WAIT set.** `locke3.sh` has TWO slots (`OTHER_LOCK` `-56`, `OTHER_LOCK2` `-f2`, :275-:276). Add **`OTHER_LOCK3`** and set `-56`, `-e3`, `-f2`. Extend the take/re-check loop, the empty-set refusal (:277-:285, whose prose names "Seat E 3rd has a TWO-LOCK WAIT SET"), the bounded wait and the stale check. **Add `OTHER_LOCK3` to `unattributed_absent_or_stop`'s KNOWN set (:332-:353)**, or a live `-f2` reads UNATTRIBUTED. Mirror all of it in `pushg1.sh`, byte-identical.
  2. `STOP_LOCKS` / `STOP_LOCKS_CHK`: the same 14 as e3, in the same order (`-e3` is now a WAIT, not a STOP); `LOCK` → `.push-lock-g1`.
  3. `namecheckg1.py`: `MINE = "g1"`. FOREIGN keeps every e3 entry and adds **`"e3"`, `"seate3"`, `"c24"`, `"seatc24"`** (and `"d7"`, `"c23"` if absent). Use segment-anchored forms only (`-g1-<n>$`, `s-g1-`, `.push-lock-g1`, `seat g 1st`, `seatg1`). **Add a fixture: `feature/ks-539-g1-split-ruling` must read NOT MINE** (P2).
  4. 🔴 **`inbox_matchg1.py`:** `MINE = "g 1st"`; `MY_PANE = "secuura/blockchain-g]"`. OTHER_SEATS keeps every e3 entry and adds `e 3rd`, `e 4th`, `c 24th`. **Fixtures:** your successor `(Seat G 2nd)` on `[Wednesday -> Secuura/Blockchain-G]` → UNTAGGED; `(Seat E 3rd)` and `(Seat E 4th)` on `-E]` → FOREIGN, kept as E; a `-G]` subject naming `(Seat E 3rd)` → FOREIGN. The same goes for `trap4_g1.py:82-:83`'s successor slot. Run trap-4 on REAL full-length API subjects: E 3rd's `READY FOR QA (Seat E 3rd): #1384 (KS-1210) -> gate60` is FOREIGN; your own LAUNCH BRIEF is FOR ME.
  5. `bannercheckg1.py` `GEN = "g1"`; no `int(GEN)` anywhere. Grep for SPACED banners (`TRAP4 e3`) and BARE quoted tokens (`"e3"`), not only `<stem><gen>`.
  6. `residue_auditg1.py` `PREV_GEN = "e3"` (the generation you copied from), with a comment saying G has no own predecessor.
  7. 🔴 **Live defaults into E 3rd's session (P15):** `mergeg1.py:119-:120` `MERGE_E3_SCRATCH` and default `…/ef94782d-5409-4df7-b941-7e9eb00bbb67/scratchpad/mergee3`; `armsg1.py:65` `ARMS_E3_SCRATCH` and default `…/ef94782d-…/scratchpad/armse3`; `:140/:267/:275` `MERGE_E3_SCRATCH`. Change each to `MERGE_G1_SCRATCH`/`ARMS_G1_SCRATCH` with a default under YOUR session's scratchpad. Prove the override is READ (set == read) and that the default resolves to a directory YOU own.
  8. **Grep EVERY string literal for other sessions' UUIDs and `/private/tmp/` paths.** Classify each as FIXTURE (keep, and say why) or LIVE DEFAULT (re-point). Print the count checked.
  9. `raiseg1.py`: `REC` → YOUR folder (:43); worktree stem `s-g1-{tag}` (:177). 🔴 **Read raisee3's evidence/pathgate assumptions before use:** they were built for vitest auth PRs. Your suites are bash (`run_shell_suites.test.sh` prints its own `N passed, M failed`) and `node --test` (`tests N`). Declare each row's path set from the queue table; pathgate's bite = row 1's head against row 4's declared set → FAIL naming the missing and extra paths.
  10. `watchproofg1.sh`, `r5proofg1.py`, `pushg1_ff.sh` header: re-key their fixtures and add an authorship line, or name them NOT RUN and prove S2/R5 by driven arms.
  11. **Read `raiseproofe3.sh`/`raiseproofg1.sh` before running it.** It builds a real detached worktree and must never land in the real repo.
  12. Per :391-:392, grep the copies for `int(`, `\d\d`, `[0-9]{2}`, `5[0-9]` generation predicates before the first run. Every checker prints how many items it CHECKED; `0 checked` is a FAIL (:335).

## THE PROJECT RULES THAT TOUCH THIS SCOPE (read at YOUR base SHA by line range, quote with blob id at ITEM 0)
- **skill §4 (`:360-:419`, blob `eaf43dfd4d98`), §5d (`:507-:516`), §5f (`:540-:550`)** (P11). §5d: WHY + the ticket on each changed line, stating the prior behaviour; ticket URL `https://linear.app/secuura/issue/KS-NNNN` in the PR summary, the PR's OWN key only. §5f: none of your rows has a runtime PRODUCT surface. **Say so in NOT COVERED** ("no runtime surface; §5f live sweep not applicable"), rather than leaving it silent. Every PR is `Refs KS-NNNN`, never `Closes`/`Fixes`/`Resolves`.
- **A hyphenated foreign key ATTACHES** (:278). The PR's OWN key is hyphenated once; every other key is de-hyphenated (`KS 1302`, `KS 1303`, `KS 884`, `KS 1046`; PR numbers as `#1250`).
- **repo `CLAUDE.md` Pull-request rules (:248) + Merge flow (:270):** `npm run check:openapi` rc 0 at every head. The Test Evidence block is written by whoever ran the tests. **No spec, dependency, lockfile, manifest or `audit-baseline.json` edit in any PR.** `expected-case-count` is a test-count pin owned by the cells you add (P9); it is not a baseline (Q-COUNT).
- **Existing preflight harnesses slice `preflight.sh` by anchors** (`preflight_failure_verdict_keeps_ratio.test.sh`: `^fail=0$`, `^step "1\/`, `n_stack=`). L2 edits must keep every anchor. Run all eight `preflight_*`/`pre_push_*` suites before and after.

## READ FIRST (by line range; keep ctx low)
1. The screen's L1/L2/L4 rows: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-05_internal-tooling-screen/SCREEN.md:32-:51` and the eight `screen.tsv` rows (note P4: `lockfile-cleanroom.sh` is under `scripts/preflight/`).
2. The eight tickets WHOLE at source (Linear, read-only). For KS-1330/1331/1325, also KS-1302's three comments (P6) and the #1250 gate report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1250r2-t2d/report.md` (its verdict + the INT-arm section only).
3. STANDING_LINES (P21): the `## ` headings first, then `:17-:46`, `:76-:115`, `:257`, `:269-:278`, `:311`, `:314-:321`, `:335-:398`.
4. E 3rd's brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatE3_successor.md:94-:125` (lock rule + namespace) and B 61st's amendments `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatB61_successor.md:5-:12`. Read-only; these are the co-tenants' contracts.
5. E 3rd's and F 2nd's handovers (P17), §1 only, to learn whether each is live.

## QUEUE
0. **ITEM 0, plan confirmation (QUESTION `plan confirmation (Seat G 1st)`, then STOP until the ANSWER).** Before the ANSWER: no lock, no fetch, no worktree, no ref write, no install, no ticket write, no repo edit. The mail carries:
   - develop + `refs/pull/138{1,2,3,4}/head` + any `-g1-`/`-e3-`/`-b61-`/F 2nd's exact ref at boot (`ls-remote`, instrument named). If develop moved past `46c3e20c`, list the first-parent commits by PR number and say whether any touches a lane path or `Projects Documents/`.
   - **`b61 + e3 + f2 WAIT, 14 STOP, catch-all (Seat G 1st)`** as its own titled block. It holds:
     - the namecheckg1 / inbox_matchg1 / twolockg1 arms, with controls each way;
     - every real `.push-lock-*`, `s-g1-*`, `s-e3-*`, `s-b61-*`, `s-f2-*` worktree, ATTRIBUTED;
     - **re-measured P14:** do `*56`, `*e3` and `*f2` now name `.push-lock-g1` as a WAIT? Expected NO until Q-LOCK-G1 lands.
   - The re-key receipt with all twelve hand-fixes driven.
   - Each lane file re-read at develop by line range (P3/P4 sites); anything that contradicts this brief.
   - The KS-948 coupling re-measured (P7 shape) if B 61st has pushed KS-948; else "not pushed at boot".
   - §4, §5d and §5f quoted from the base tree with blob id; the eight tickets' state/project/newest comment re-read.
   - Your watcher pid READ from a ps FILE; every launcher preflight warning VERBATIM; `df -m`; your ctx or "Please read my ctx."
   - Your restatement of the OPEN questions below.
1. **ITEM 1: tools.** Copy (Q-GEN) and hand-fix, drive `twolockg1.sh`, and send ONE STATUS `tools ready (Seat G 1st)`. **No lock is taken before Wednesday's ANSWER quotes the mirror ACKs (Q-LOCK-G1).**
2. **ITEM 2: row 1, KS-1330 (T1), worktree `s-g1-ks1330` at develop.**
   - **Fix shape:** bring #1250's runner blob `8eef1c4877b3` and test blob `9c4a87f0a97c` onto develop. They merge clean (P7: tree `a3cbf98c0d7b`). Use `git checkout 2b8dcb824dd2 -- <the two paths>` in YOUR worktree, which needs no fetch because the commit is in the store (`cat-file -e` first). Then:
     - **Item 1:** gate the suite's SIGINT-to-pid arm by `sig_installable` ONLY (rule 1), at the round-2 test's `:624-:666` (`signal_run` :592, `sig_installable` :643, the constant UNREACHABLE at :637/:663), and correct the matrix comment (rule 2 holds only WITHOUT `set -m`).
     - **Item 2:** add a kill-to-exit latency bound relative to the fixture suite's sleep.
     - **Item 3:** document (runner header + one cell) that background-launched suites start with SIGINT ignored and stdin at `/dev/null`, or preserve both (Q-1330-3).
   - **Red-first by assertion (EXPECTED, UNMEASURED):** with the corrected arm, at develop's runner a lone SIGINT to the runner pid exits rc 0 with a green verdict (KS-1330 states this, from #1250's evidence). At the head it exits rc 130, prints no verdict, leaves no `/tmp/rss.*` dir, and the in-flight suite is gone. Control: the TERM arms pass on both the round-2 runner and the head. Tamper: revert the gate to the constant → the cell reads UNREACHABLE.
   - Whole runner before/after from a cwd outside any repo under `/bin/bash` 3.2.57 (the #1234 merge condition, P12): `N passed, M failed, S skipped (of K)` on develop vs head, by NAMED binary. `run_shell_suites.test.sh` alone, before/after.
   - **Body:** `Refs KS-1330`. Credit #1250's round-2 work by blob ids. **#1250 stays OPEN and is not touched (Q-1250).** KS 1302 / KS 1303 de-hyphenated. NOT COVERED: no live sweep (no runtime surface); `script`/PTY foreground INT is KS 1325's.
   - ONE commit, 0 trailers, subject ≤ 92 as it LANDS. Then STATUS.
3. **ITEM 3: rows 4-5 (L2), each only if ctx < ~45% when it STARTS.**
   - **KS-1127** (open bullet only; the tally itself is DONE, P12). Fix shape: leg 14 (`preflight.sh:643`) keeps the runner's `shell suites: N passed, M failed, S skipped (of K)` line. Capture it via a temp file, not by losing the live stream. The closing verdict (every branch from :693, including the KS-1260 failure line :711 and INCOMPLETE :755) quotes it as `leg 14: shell suites: …`. When the runner printed no tally line (interrupted: KS-1330's runner prints none by design), it says so instead.
   - **KS-1127 red-first (EXPECTED, UNMEASURED):** in the existing slicing harness shape (`preflight_failure_verdict_keeps_ratio.test.sh`), a stubbed leg 14 whose runner prints `…, 1 skipped (of 3)`. Base verdict: no `skipped` text (red). Head: the line quoted. Control: a runner printing `0 skipped` is quoted unchanged. Tamper: drop the quote → red.
   - **KS-1153.** Fix shapes:
     - R-925-A: `:173` `${_hdr_total%% *}` → strip at the first whitespace of ANY kind. Red-first: a header `"3/15\tx"` ABORTs at base (false ABORT) and passes at head; control `"3/15  x"` passes on both.
     - F-925-4: `_note_skip` (:204-:209) dedupes per LIST only, so a leg in both `SKIPPED_STACK` and `SKIPPED_ADVISORY` counts twice in `n_skipped` (:693-:695). Make it dedupe across both lists. Red-first: drive one leg through `skip_stack` AND `skip_advisory` and assert `n_skipped` 1 at head vs 2 at base.
     - R-918-B: the basename loop (:197-:211) is a pre-existing design note. PROPOSED: accept-with-a-line (a comment in run-code-guards.sh + the PR body), no behaviour change (Q-1153).
     - R-924-A: a body edit of merged PR #924 is OUT (Q-1153).
     - R-918-A: already pinned (`run_code_guards.test.sh:156-:164`, CASE 9): cite it, do not rebuild it.
   - KS-1209's N41-4 (`:711` ASCII ` - `) is NOT yours in either L2 PR (one ticket per PR): name it in the KS-1209 PR as not fixed.
4. **ITEM 4: rows 6-8 (L4), each only if ctx < ~45% when it STARTS.** `npm ci` in `scripts/audit/` first (P9).
   - **KS-829: F1 only (PROPOSED, Q-829).** Fix shape: the root gate's CLEANUP (`audit-gate.mjs:203-:205`) must not list a row it cannot positively attribute. Equivalently, `validateBaseline` refuses a row with neither `scope` nor a root-reported id. **Run each hypothesis against the unfixed instrument first** (the ticket's own instruction).
   - **KS-829 regression (the ticket's):** a locks-only advisory baselined without `scope` must NOT appear in CLEANUP. Red at base, green at head. Control: a scoped row stays excluded, and an unscoped root-stale row is still listed.
   - **KS-829 other findings:** F2 (versions on rows) needs `audit-baseline.json` data and is OUT pending a ruling. F3 is record wording. F4 is MOOT: the `GHSA-rgwj-5xj2-c3m3` row is gone (0 matches at develop), so say so.
   - **KS-1209 Polish.** Fix shape: `lock-discovery.mjs:282-:283` reports a PRESENT malformed `expires` distinctly ("malformed expires (not an ISO …)"), not under `missing` (:303). That is baseline-contract.mjs's own reasoning at :164-:167. Red-first: `expires: 'soon'` → base message contains `missing expires (not an ISO` (red); head does not, and still throws (fail-closed control). The existing `:184` cell is still green.
   - **KS-1394.** Fix shape: `audit-locks.mjs:352` prints a per-lock command:
     - mount the lock's PARENT when the manifest has a `file:` link escaping its dir (`systemTest/performance/package.json:56`, P4);
     - use `npm update <pkg> --package-lock-only` for an advisory-driven move;
     - keep the per-dir form otherwise.

     Add one comment line in `scripts/preflight/lockfile-cleanroom.sh` noting that no preflight leg clean-rooms `systemTest/` locks (Q-1394).
   - **KS-1394 red-first:** a fixture lock with an escaping `file:` link → base prints the per-dir mount (red), head the parent mount. Control: a lock without one keeps the per-dir form. **Whether the printed command WORKS is UNMEASURED and not yours (no Docker):** name it in NOT COVERED.
   - **Every L4 row bumps `expected-case-count`** by exactly its new cells, stated as `59 + n`. Leg 5's own check at head prints `OK — N audit-contract cases pass (expected N)`.
5. **ITEM 5: PREDICT, PUSH, RAISE, ONE READY (batch 1).**
   - Re-read develop and read what moved. STOP and mail if anything touches a lane path.
   - Predict per THE DOC PROTOCOL step 6, chained after every open PR ruled to land before yours (#1381, #1382, #1384, KS-938, #1383 as they then stand). **Order your own L4 PRs and name the `expected-case-count` RECOUNT each later one needs** (P8).
   - Push each ONCE with `pushg1.sh` BARE, under THE LOCK RULE. Quote the preflight ratio and skipped legs EXACTLY from the in-hook `<tag>-push.out` (:119-:150, :272). Report each hold time.
   - Raise each by REST: HTTP 201, head == origin, body sha256 read back.
   - **ONE READY `READY FOR QA (Seat G 1st): #<a> (KS-1330) [+ #<b> (KS-1127) …] -> gate<NN>`**, per PR: head and develop read from origin in the SAME action; END_TREE; the predicted chained merge-in tree; trailer proof; pathgate with its firing control; lock census; "no independent re-key auditor".
   - HOLD with the watcher armed.
6. **ITEM 6: MERGE ON EACH GO, ONE AT A TIME.**
   - Act only on `GO (Seat G 1st): merge <n> on gate<NN>`, confirmed by API, with Seat G 1st as the subject's addressee.
   - Before each merge: re-read head and develop at origin. Merge develop IN first per THE DOC PROTOCOL, under THE LOCK RULE. Assert the new head's tree == the tree the GO names (print both). Confirm 0 trailers, then push with `pushg1.sh`.
   - Run `mergeg1.py --dry` first. Read its argparse flags at ITEM 0 and name them. Read the `.DRY` body: subject as the GO composes it (no `(#n)`), own key only hyphenated, 0 trailers, ONE `Merged by ` naming Seat G 1st.
   - Merge with the head PINNED. Verify by `ls-remote` against the GitHub URL AND the API. Send STATUS `merged` after each.
7. **ITEM 7: rows 2-3, only once KS-1330 is ON develop and ctx < ~45%; else name them NEXT in the handover.**
   - **KS-1331.** Fix shape: forward the runner's signal to the suite's PROCESS GROUP. Launch each suite as its own group (job control around the background launch), then `kill -<sig> -- -<pgid>` in the handler. Kill our own group by pgid, never by name.
   - **KS-1331 red-first (EXPECTED, UNMEASURED):** a fixture suite forks an untrapped `sleep 300 &` grandchild and records its pid; TERM to the runner. Base: the grandchild is alive (red). Head: it is gone. Control: a suite without a grandchild has an unchanged verdict and rc.
   - **KS-1325.** Fix shape: a PTY harness that runs the runner in the FOREGROUND of a pseudo-terminal (mechanism Q-1325). **The acceptance is the ticket's discriminating pair:** the same harness gives rc 130 on a foreground INT, and shows the arm reporting UNREACHABLE when SIGINT is ignored on entry. A harness that produces only one of those fails.

## QUESTIONS for ITEM 0 (each with a PROPOSED answer; Wednesday rules in the ANSWER)
- **Q-LOCK-G1 (BLOCKING, Wednesday's):** P14 measured all three co-tenant generations refusing an unattributed lock in code, and none names `-g1`. **PROPOSED:**
  - Wednesday sends a mirror ADDENDUM to every co-tenant still LIVE (B 61st; E 3rd and F 2nd only if not WRAPPED, P17): add `.push-lock-g1` to its WAIT set with the 20-min bound and take/re-check order; `g1`/`s-g1-`/`-g1-<n>$`/`g 1st` become FOREIGN, segment-anchored. Each seat ACKs with its proofs re-run.
  - **You take NO lock until the ANSWER quotes each ACK, or rules that seat WRAPPED.** A wrapped seat's lock moves from your WAIT set to your STOP set (`-e3`/`-f2` → STOP, rc of its own).
- **Q-SET:** WAIT = `-56`, `-e3`, `-f2` as commissioned. E 3rd and F 2nd have both written handovers (P17). **PROPOSED:** keep both in WAIT until Wednesday names each WRAPPED. A successor (E 4th, F 3rd) gets its own token, which your catch-all refuses until a ruling adds it.
- **Q-DOC:** (a) blocks `25.`-`32.` per §4 :362's literal text (shell suites are "backend unit" tests), or (b) §4 :417's route, "does not affect either doc, and why", on the precedent that #1234, #1041 and #1056 shipped no block (P10). **PROPOSED: (a), as commissioned**, with numbers by ticket. If (b), the numbers stay reserved and unused, and every doc conflict disappears from your lanes.
- **Q-GEN:** copy E 3rd's `*e3` (P15) after its WRAP, with the twelve hand-fixes. **PROPOSED: yes.**
- **Q-ORDER-G1:** numbers by ticket, build order KS-1330 → KS-1127 → KS-1153 → KS-829 → KS-1209 → KS-1394, then KS-1331 → KS-1325 after KS-1330 merges. **PROPOSED: yes; no stacked PRs.**
- **Q-TIER:** T1 for KS-1330, KS-1331, KS-1127, KS-1153 and KS-829 (each changes what the pre-push gate every seat runs does or prints; precedent #1041 tier 1, #1234 tier 1c). T2 for KS-1325, KS-1209 and KS-1394 (message/test-infra only). **PROPOSED as listed.**
- **Q-1250:** #1250 (KS-1302 round 2) is OPEN with NO-GO at cap (P6). Its branch `…-l5-1` is FOREIGN. **PROPOSED:** you build fresh from #1250's blobs on your own branch; never push to `…-l5-1`; never close or comment on #1250. Its disposition is Wednesday's/Kam's after KS-1330 merges.
- **Q-1330-3:** item 3. **PROPOSED: document** the SIGINT-ignored/stdin-`/dev/null` launch in the runner header + one cell, rather than revert.
- **Q-1325:** mechanism. 0 suites use `python3` or `script -q` today (P13). **PROPOSED:** `python3`'s `pty` module (one code path on macOS and Linux). When `python3` is absent, the suite prints `SKIP — …` and exits 0, which KS-1127's tally counts as skipped, never passed. Whether `python3` is on PATH inside the hook is to be measured at ITEM 7.
- **Q-1153:** R-918-B accepted with a line, R-924-A OUT (a merged PR's body), R-918-A cite-only. **PROPOSED: yes.** Each "accepted with a line" on the ticket is a COMMENT, posted only on a GO's relay.
- **Q-829:** F1 only; F2 OUT (needs `audit-baseline.json` data, a HOLD); F3 record-only; F4 moot. **PROPOSED: yes.** If F1's fix needs a baseline edit, STOP and mail.
- **Q-1394:** `lockfile-cleanroom.sh` gets a comment line only, no behaviour change. **PROPOSED: yes** (its regen command at :120 is a separate surface; changing it widens the PR).
- **Q-COUNT:** `expected-case-count` is a test-count pin the cells own (P9), not a baseline. Each L4 PR moves it by its own cells. Every merge-in RECOUNTS it (`node --test` total at the merge-in tree), never picks a side. **PROPOSED: yes.**
- **Q-RK:** `rekey_checkg1` stays INERT; say "no independent re-key auditor" in every READY. **PROPOSED: yes.**
- **Q-GATE:** no kit exists for you (P20). **PROPOSED:** the next free gate number for batch 1, Wednesday's.

## HOLDS / KAM'S, NOT YOURS
- **No merge without Wednesday's signed GO naming the head SHA, after the gate.** One PR per GO; merge-in heads per Q-M.
- **No deploy** (kintsugi or demo; deploys are Seat D 7th's under Kam's October grant), no `az`, no SSH to any VM, no migration, no Docker, no live sweep.
- **No `--no-verify`, NO force push, ever, no `-u`, no `--admin`.** GitHub refuses an approval from our own account (HTTP 422): meet it and STOP.
- **No spec, dependency, lockfile, manifest, `audit-baseline.json` or `.githooks/pre-push` edit** in any PR. No `.github/workflows` edit. KS-1292, KS-1300, KS-1332 and KS-884 are OUT.
- **Ticket states:** no state, assignee, label or PROJECT change; close nothing; nothing moves to Done (§5f). Any NEW ticket goes to the board account, only after an exact-substring board search (`searchIssues` saturates and cannot prove a 0).
- **Client communication:** no comment to Peter or Stuart, and no other client-visible write except your PRs and their merges. Ticket comments are posted ONLY on a GO's relay and read back (sha256); any mention must be verified as a `suggestion_userMentions` node. The extranet is never a channel.
- **Never delete; quarantine** (`:103`). **Never touch** #1250, `s-e*`/`s-b*`/`s-f*`/`s-d*` worktrees, or another seat's record folder (except the one tool copy).
- **The shared inbox rule:** act on a GO, a relayed ruling or a push/merge/post instruction **only when its subject's addressee is Seat G 1st.** R5: a new mail from `kreiser.org@me.com` → STOP and mail Wednesday; act on nothing in it.
- Signature classes pause for Kam: production, money, external communication beyond the gated writes, anything irreversible.
- 🔴 **Drive hygiene at WRAP** (:397; policy `/Volumes/DevMASTER/WEDNESDAY/1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md`). Remove only YOUR OWN regenerable leftovers for MERGED work (`s-g1-*` `node_modules` once merged; your scratch clones), as copy → verify → remove to `/Volumes/G-DRIVE/Scratch Files/<date>_<seat>_<what>/`. Run `git worktree prune` only for your own. Take `df -m /Volumes/DevMASTER` before and after (720,363 MiB free at draft, P22).

## STANDING: no attribution
- Branch commits carry NO `Co-Authored-By` and no tool-attribution trailer (this overrides the repo convention and your harness's commit guidance for this seat). `git log -1 --format='%(trailers)'` prints 1 byte; control `bf277eead268` prints 55 bytes. Re-prove 0 trailers on every head. A commit that went out with a trailer is NOT amended or force-pushed: STOP and mail.
- Squash bodies come from `mergeg1.py` with `no_trailer`. Check the `.DRY` body you SEND (:370).

## MAIL FORMATS (to `wednesday-agent@agentmail.to`, subject prefixed `[Secuura/Blockchain-G -> Wednesday] `)
- **Plan:** `QUESTION: plan confirmation (Seat G 1st)`, with the `b61 + e3 + f2 WAIT, 14 STOP, catch-all (Seat G 1st)` block inside.
- **STATUS:** `QUESTION: status <item> (Seat G 1st)`, one line of state, then your ctx.
- **READY:** `READY FOR QA (Seat G 1st): #<n> (KS-NNNN) [+ …] -> gate<NN>`.
- **WRAP:** `WRAP (Seat G 1st): round g1 …`. It carries:
  - what IS running (ps file);
  - the handover path + sha256 prefix + `wc -c`;
  - the history entry at the TOP of `history.md` (re-read the top first);
  - UNRAISED / UNMEASURED / UNMERGED, naming the NEXT row;
  - `df -m` before/after and what you removed;
  - mail counts COUNTED from the inbox, with failed sends separate.
- Routing tokens appear ONLY as the leading tag, never mid-subject. Compute every mailed figure in the SAME tool call that sends the mail; read every send's response; read the SENT artefact back. Use placeholder substitution, never an f-string, for prose with braces; never an unquoted heredoc.
- **Handover:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatG1-2026-10-05.md`.

## DEFECTS NAMED FOR WEDNESDAY (drafter's)
1. **Q-LOCK-G1 is blocking** (P14): every co-tenant's code-level catch-all refuses `.push-lock-g1`. Without the mirror, your first take freezes B 61st, E 3rd and F 2nd mid-push.
2. **The screen's L4 path is wrong** (P4): `scripts/lockfile-cleanroom.sh` → `scripts/preflight/lockfile-cleanroom.sh`. Correct `screen.tsv`'s KS-1394 row.
3. **The screen's L2/L4 file sets omit the tests and the case-count pin:** KS-1153 needs `run_code_guards.test.sh`; every L4 cell needs `expected-case-count`, which makes L4's PRs pairwise conflicting on that file (P8).
4. **KS-1127's and KS-1209's screen rows cite stale line numbers** (`preflight.sh:166`→`:173`, `:197-202`→`:204-:209`, P3). KS-1127's title describes the DONE runner half; its open half is preflight-only.
5. **KS-1090 and KS-1014 also name `preflight.sh`** (`screen.tsv`): L2 is disjoint only while neither is launched.
6. **E 3rd and F 2nd have handovers on disk** (P17) while the commission keeps both in the WAIT set (Q-SET).
7. **KS-1302 and KS-1303 are project None** (P6), not in Internal tooling, although they own #1250, the PR KS-1330 re-lands. That is C 24th's/Wednesday's to read, not yours to move.
8. **The doc-block requirement contradicts the tooling precedent** (P10, Q-DOC).

## UNMEASURED (not provenance)
- Every red-first, suite, `check:openapi` and preflight figure at any SHA; the "EXPECTED" red cells above are the drafter's reading of the tickets and code, not runs.
- The GitHub open-PR list (P5 used refs only); #1250's current state on GitHub.
- Whether E 3rd and F 2nd are LIVE or WRAPPED; which pane each seat holds; B 61st's progress (0 `s-b61-*` at P16).
- Whether `python3` is visible inside the pre-push hook; whether KS-1394's printed commands work (Docker, not yours).
- Your ctx and pane id.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam, live board 2026-10-05 18:14:26: "run cloud and local agents as hard as possible to action these" (the 160 Internal tooling tickets).
- Kam's 2026-09-13 as-many-agents rule (as many seats as there are file-disjoint lanes); the 2026-09-11 TESTED merge grant (merge on a gate GO from Wednesday); drive hygiene 2026-10-05 12:13:55 (:397).
- The 2026-10-05 16:21-16:22 live-board cards of the 16:30 partition:
  - the 192 tooling tickets → "Internal tooling" = a (C lane);
  - KS-1256 = b with the October deploy grant (D 7th's to execute);
  - KS-1401 migration = a;
  - kintsugi deploy now = a.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **For Seat G 1st (with this brief):** NEW seat on `Secuura/Blockchain-G`. Token `g1`, tools `*g1`, lock `worktrees/.push-lock-g1`. WAIT `-56`, `-e3`, `-f2`; STOP the 14 older locks + every unattributed lock. The eight tickets one per PR, in lane order L1 → L2 → L4. Batched READYs. Never start a build past ~45%; cold handover at ~62%. KS-1292, KS-1300 and KS-1332 wait for Kam's KS-884 card (OUT).
- The 16:30 partition (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_wave_1630_partition.md`) and B 61st's amendments A1-A7. Doc numbers are by ticket (Q-E1): `13.`-`17.`, `23.`, `24.` B; `18.`-`21.` E; `22.` F. Merge order #1381 → #1382 (A4); KS-938 after #1382 (E 3rd's handover §1).
- Q-M as gate57 §3 states it (M1-M4 + one new commit). No force push, ever. Catch up by merging develop IN, on a ruling naming that PR.
- Standing: no attribution. A gate that trips on the INSTRUMENT is fixed and resumed; one that trips on a READING is a STOP and a mail. Any red that is not red at develop is a STOP. The GO composes squash subjects (no `(#n)`). Merge only on a signed GO whose subject's addressee is Seat G 1st.

| Partition / identity | Value |
|---|---|
| Seat | G 1st (P18) |
| Pane / tag | `Secuura/Blockchain-G` / `[Secuura/Blockchain-G -> Wednesday] ` |
| Token / tools / lock | `g1` / `*g1` (copied from `*e3`) / `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-g1` |
| Record folder | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatG-1st/` |
| Worktrees | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-g1-ks{1330,1331,1325,1127,1153,829,1209,1394}`; no adoption |
| Branches | `feature/ks-<n>-<slug>-g1-<k>`, k = 1..8 by row; match `-g1-[0-9]+$` only |
| WAIT set | `.push-lock-56` (B 61st), `.push-lock-e3` (E 3rd), `.push-lock-f2` (F 2nd), each bounded 20 min |
| STOP set (14 + catch-all) | `-e2`, `-55`, `-e1`, `-f1`, `-54`, `-d6`, `-d5`, `-c21`, `-d4`, `-d3`, `-d2`, `-53`, `-52`, `-51` + any unattributed (incl. `-d7`, `-c24`, successors) |
| FOREIGN | `e3`, `e2`, `e1`, `b61`, `b60`…, `b6` (anchored), `f2` (exact-name only), `f1`, `d2`…`d7`, `c21`…`c24`, `l4`, `l5`, `n41`, `m1`; `feature/ks-539-g1-split-ruling` |
| Doc blocks | `25.` KS-1330, `26.` KS-1331, `27.` KS-1325, `28.` KS-1127, `29.` KS-1153, `30.` KS-829, `31.` KS-1209, `32.` KS-1394 (Q-DOC) |
| Gate / GO | gate<NN> per batch (Q-GATE) / `GO (Seat G 1st): merge <n> on gate<NN>` |

VERIFIED BEFORE SENDING (Wednesday's drafter, 2026-10-05)
PROVENANCE P1-P22 was measured 2026-10-05T07:37-07:46Z by read-only verbs in the project: ls-remote with the project's sshCommand, cat-file, ls-tree, log, show, diff, merge-base, grep; ls, stat, ps, tmux list-panes, df; Linear GraphQL queries. Every merge-tree, hash-object, read-tree and commit-tree ran in the drafter's own `git clone --shared` scratch clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g1/vclone`. Nothing was fetched, locked, written or sent in the target project, its object store, its board or GitHub.
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-05 18:51
