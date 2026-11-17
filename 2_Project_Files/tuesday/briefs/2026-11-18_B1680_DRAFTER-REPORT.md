STARTABLE: YES - the kit is complete against main `751285aa` (counts 5868/377), all four tickets were read whole, and the three in-lane parts need no product file and no word from the product owner; only RD-729 is cut to its A-F1 finding (A-F2 to A-F4 are out of the lane, see below).

Drafter report for kit B1680 (seat N146, NexusAI lane NX-T3). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1680_SEAT-N146_nexusai-lane-nx-t3-test-tail.md` (342 lines, 4 slots + last line = 5 four-underscore hits, `grep -c` printed 5), sidecar `.measured` beside it. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/d1680/`. Clock: drafting began 00:04 AEDT and the last read was 00:18 by `date`.

## BLUF
- One branch `b1680/nexusai-lane-nx-t3-test-tail`, four test files + the counts file, Sonnet (row L6, `model-routing.md:85`; model `claude-sonnet-5-5`, `models_latest.json:23`), gate G2 (`:109`); the RD-1002 part alone is G3 (`:110`, no gate) and rides in the G2 branch. Pane `Datasec/NexusAI-N146`, slot 2 band 21280-21919, trees `b1680-nodot/{old34,new17,mut9,v1,chk9,chk34}`, push a branch, no PR, nothing deployed, HARD STOP slot left as underscores (the seat's PREDICTED need is about 1 h setup + about 1.7 h lock hold; Tuesday's 05:30 AEDT fits).
- Parts: A RD-1002 (rd969 header comment: no count, H6/H7/H8 added to the index), B RD-734 (rd638: `E2_STOP_MS` 20000 and the comment), C RD-730 (handover-gate-table: B-F1 read-past-blank-line, B-F3 `gitState` + a third title, two new pure cells), D RD-729 A-F1 (rd648 H1 bound, made INSIDE the chain after a measurement), K counts. PREDICTED +2 tests / +0 suites: 5868/377 -> 5870/377.
- RD-730 stays IN: both functions are inside the test file (`gateRows` `:33`, `shaFormatProblems` `:52`), so the sweep's "may be a product or tooling file" is answered: it is not.
- Partition with the sibling records kit B1679 (Jira, CLARIFICATIONS, a HISTORY.md branch, no code file): B1680 owns the five OWNS paths only; B1679 owns Jira, `CLARIFICATIONS.md`, `HISTORY.md`. B1679's kit file did not exist yet in the briefs folder (no `2026-11-18_*` file), so the partition is from the commission and UNMEASURED by program; the seat re-prints it at Step 1b. A HISTORY.md-only main move is treated as a clean HOLD 20 event inside the same lock acquisition.

## Keys in and out
- IN: RD-1002 (whole), RD-734 (whole), RD-730 B-F1 and B-F3, RD-729 A-F1.
- OUT, with why: RD-729 A-F2 (an always-slow health answer: changes `__tests__/helpers/rd395-server-harness.js`, which 58 test files require, and picks between two behaviours); A-F3 (floor cell) and A-F4 (leaked tmp dir) are Polish, not in the ticket's fix shape. RD-729 therefore stays open after landing. RD-730 B-F2/B-N1 ask nothing.
- No ticket needs the product owner's words; no ticket touches a product file. I wrote nowhere that the product owner decided anything.

## Facts re-measured (instrument; control)
- Main: `gh api -X GET .../branches/main` -> `751285aa138f366e44d0ef97e1464dc6bf52c436`, tree `edec1b1769c230958498dcb35473f6d443777598`; open pulls 0. Counts file `scripts/verify-expected-counts.json:3-5` = 5868 / 377, `_updated` 2026-11-17T10:56:30.113Z (extracted tarball, `sed -n 1,8p`). True jest totals UNMEASURED (no jest run).
- Blobs by `git hash-object` AND the contents API, equal: rd969 `8503b2a86893`, rd638 `fc121f5d2959`, rd648 `40d8692f71de`, handover `58d39943bd50`, counts `0ee27c40ed9a`, doc `d42f9779e390`, harness `a49d3f383ad8`; last two commits per path by the commits API (in the kit).
- Alerts in the four files: 0 (22 open on main, none in them; control: `state=fixed` paginates to 222).
- Census of `heads/b1*`: 50 refs, 48 behind/0 ahead, 2 diverged (`b1480/...`), each touching only the counts file; `b1680`/`b1679` refs 0 (control `refs/heads/main` 1 of 476).
- Step 1b(ii) reader list at `751285aa`: same 10 files as B1667 (8 tests + 2 helpers) plus `jsdom-instrument-limits`.
- Ports: names program `names1680.py` with the 4 controls (16, 16, 17, 12) equal to earlier kits; slots named by kits of 17 and 18 Nov: 0, 1, 5, 13, 15, 16, 17; slot 2 free; `lsof -nP -iTCP:21280-21919 -sTCP:LISTEN` 0 rows (control: 11 listeners machine-wide); no `b1680-nodot` or `.tools/b1680` exists; no Datasec/NexusAI pane live (tmux list).
- Behaviour I measured WITHOUT jest, with plain node on the raw files: `sim1680.js` (functions extracted from the base and head files): base `shaFormatProblems` returns `[]` for the real doc AND for a copy with a malformed row planted after a blank line (the blind spot); head returns `[]` for the real doc and `["`not-a-sha`"]` for the planted copy; `gitState` returns checkout / no git / archive for the three probes. `probe1680.js` (node v26.13.0): git present outside a repository raises `status` 128 with no `code`; a PATH with no git raises `code` ENOENT; so `e.code === 'ENOENT'` separates them. A plain child with the `survive-term.js` preload is alive 1 s after SIGTERM (empty preload: not alive); the server's only SIGTERM registrations are `process.once` at `backend/server.js:22589` and `backend/bootPreflight.js:325`.
- RD-1002 predicate by program over the raw rd969 file: cell ids `E1 H1 H2 H3 H3b H4 H5 H6 H7 H8 M1`; header index ids at base `E1 H1 H2 H3 H3b H4 H5 M1` (missing `H6 H7 H8`); after the frozen patch none missing.
- All four frozen patches were applied by `mkpatch1680.py` with `count == 1` asserted for every old text, `node --check` passes on all four, and the added lines hold 0 non-ASCII characters (program print). Diffs generated by `git diff --no-index` into `patch/*.diff` and embedded in the kit by program (no hand copy).
- `stamp_check.py` on the kit: **132 claims, 132 measured, 0 not measured, exit 0** (first run `--init` wrote 132 TODO; every line filled; many are "not a literal the seat matches: a command/instruction" lines, as in B1667's sidecar; real literals carry a grep/awk/gh print).

## Corrections of B1667 / B1670 applied (consciously, no blanket rename)
B1667 STATUS: patch hunks all have unique anchors (Correction 1); judge counts passed/failed only (3); no shell-variable commands, use functions (5); predicted delta printed once at K (6). B1670 STATUS: no `cd` even in a subshell (1); browser check in any existing tree, here `old34` (2); local census (3); identifiers added minus removed (5); `--plan` stub proof (6); main moving mid-chain: `mstep` + `p-plain-M` appended to the SAME acquisition from new script files, plus a last chain step `mainmove-last` that looks once more before the lock is released (7). References to B1667/N144/B1670/N145/rd452/rd770/rd929 were rewritten by hand; the kit lists the strings a copied tool must not still name.

## Chain input table (rule 4: each input is made by an EARLIER step or exists at BASE)
| step | inputs | source |
|---|---|---|
| 0 browser | any existing tree (`old34`) | made in Step 1 trees |
| 1 base-counts | the four files at BASE | exist at BASE |
| 2 measure | `mut9` at BASE; harness at BASE; new `survive-term.js`, `stopms.js`, `margin.py` | tree from Step 1; the two JS files are frozen in the kit and written before the waiter; margin.py by the seat |
| 3 dstep | step 2's margin; commits A, B, C | A, B, C made before the waiter |
| 4 a-alone | `new17` at D; a-pred program | D from step 3; program frozen in the kit |
| 5 new-cells | step 1 and 4 JSONs | steps 1 and 4 |
| 5b no-git | `new17` | step 4 |
| 6 scanners | `new17`; Step 1b(ii) list | Step 1b |
| 7 mut | `mut9` re-detached at D; harness blob | step 3 |
| 8 mainmove | fetch | none |
| 9 p-plain | `chk9` at D | step 3 |
| 10 u-update | `v1` at D | step 3 |
| 11 kstep | regenerated counts from `v1` | step 10 |
| 12 p-plain-K | `chk34` at K | step 11 |
| 13 mainmove-last | fetch | none |

## D-decisions (mine)
- D1: RD-729 follows the ticket's fix shape (tighten H1, 0 new cells); the sweep wrote "a new cell". Counts differ by 1 if Tuesday wants a new cell instead.
- D2: the H1 margin is chosen by a rule from ten measured times (keep the ticket's 1500 if base max <= 4000 and flat min >= 5000, else midpoint, else STOP), because from the code the base time is expected near 3.8-4.6 s and the ticket's 4.5 s bound may sit inside it. That is why part D is made in the chain.
- D3: RD-734 gets no new cell (the ticket asks for none); its proof is a measured `h.stop()` (`stopms`, 20000-30000 ms) and the constant-sum arithmetic (158000 at base, 168000 true and at head). The plant for this is not run, said plainly in the kit.
- D4: B-F3 adds a third title `GIT NOT AVAILABLE - ...` in ASCII (the older title keeps its em dash and is not renamed).

## Q-questions for Tuesday (each with a default)
- Q-1: keep B-F3 and its third title? Default YES (ticket's own phrase; costs one `else if` and one cell). If NO, part C loses `gitState` and one cell (+1 test instead of +2).
- Q-2: RD-729 A-F1 as "tighten H1" (0 cells, default) or add a new cell as the sweep said (+1)?
- Q-3: leave RD-729 A-F2, A-F3, A-F4 for a later harness lane, ticket stays open? Default YES.
- Q-4: add a pin cell tying `E2_STOP_MS` to the harness's `stopBy` source line? Default NO (text-scrape of a helper; ticket does not ask).
- Q-5: gate: whole branch G2 (default), RD-1002 part is G3 and rides along.

## UNMEASURED
Any jest result (per-file cell counts, the 5870 prediction, H1's real times, `stopms`, step 5b, the plant colours); the real `h.stop()` time; whether jest starts with a git-less PATH; the sibling B1679 kit's content; the wider census of 426 other heads; the hosted Deploy demo state after a landing; whether the main will move before launch.

## Outside-the-fences disclosure
Writes: only the kit, sidecar, this report, and scratch under `s287/d1680/` (tarball extract of main at the pinned sha via `gh api -X GET .../tarball/<sha>`, patch copies, node probes, `claims.json`). Reads: Jira GET of the four tickets via a copy of B1667's reader (token never printed); `gh api -X GET` for branches, commits, contents, code-scanning, matching-refs and about 50 compare calls; two landed STATUS files and kits read whole or in part; nothing from the forbidden folders. Ran plain node one-liners (probes, a plain-child spawn of 1 s, `sim1680.js`), no jest, no project server, no clone, nothing in the NexusAI project folder written. One first Bash call contained a `cd` and the hook refused it; nothing ran. One `sed -i ''` edited my own scratch copy `names1680.py`.
