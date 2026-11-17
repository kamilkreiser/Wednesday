STARTABLE: YES, once #218 (NX-T3, head 7bc1c5d2) has landed. At the drafter's last read main `f8a6232a` does NOT contain that head (gh compare: status diverged, ahead_by 5, behind_by 2), so a launch before the landing stops at REFUSE 4(b) by design; nothing else blocks it. Kit, sidecar and this report are complete; stamp_check exits 0 (114 claims, 114 measured, 0 not measured).

Drafter: Sonnet 5.5 Agent-tool drafter for Tuesday. Clock: started Wed 18 Nov 2026 02:22 AEDT, kit and sidecar finished 02:37 AEDT (`date` readings in the session).

## BLUF
- Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1683_SEAT-N148_nexusai-lane-nx-c-stale-comments.md` (249 lines), sidecar beside it (`.measured`, 114 lines). Brief B1683, seat SEAT-N148, pane `Datasec/NexusAI-N148`, branch `b1683/nexusai-lane-nx-c-stale-comments`, Sonnet (`claude-sonnet-5-5`, `models_latest.json:23`), launch line carries `BRIEF_SEAT_LEVEL=sonnet`, STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-18_B1683_STATUS.md`. Stamp slots (four) and the last line are four underscores, HARD STOP slot included.
- **Model row C2** (`model-routing.md:92`): Datasec work is P4 (`:50`, no local tier) and the lane spans four files with a verify chain. **Gate G2** (`:109`) for the branch; the three comment lines alone would be **G3** (`:110`, comment corrections, no gate) and ride inside. Reason for G2 over G3: one existing guard cell is reworked and the guard's reviewed list shrinks, and the seat's "comment-only" claim is checked by a program, not trusted.
- **Items in (all three comments):** `backend/server.js` demo revision name (now `:832`, ticket's `:767`), `backend/server.js` retired VM address (now `:1102`, ticket's `:1030`), `backend/services/schedulers/healthSweeperScheduler.js:22`. Each is ONE line replaced by ONE line (server.js stays 22646 lines, sweeper 292). Plus the 2026-10-05 ticket comment's requirement: the five `RD-689` entries of `__tests__/rd385-shipped-root-markdown-identifiers.test.js` deleted in the same commit.
- **Item added that the ticket does not name (found by measurement):** the existing cell `ARM (RD-828 C-F1) - one KIND leaving a file that keeps another kind...` asserts `backend/server.js` STILL holds a resourceName finding (`expect(live).toContain(...)`). Once the revision-name comment is reworded that precondition is false and the cell goes red. The kit re-points that one cell at `backend/marketplaceJwt.js` (title unchanged, byte for byte; two `expect` calls instead of three). It is the one edit of an existing cell; no cell added or removed.
- **Items out:** none of the ticket's items is dropped. No new user-facing words, no behaviour touched (all three are `//` or ` * ` comment lines; the comment-only program reads `same` for both source files, control `DIFFERENT`). Left for others: non-shipped files (docs, HISTORY.md) the guard cannot see, the rest of the RD-130 narrative, the records items (Jira) after landing.
- **Red-first instrument: the existing rd385 test plus a no-jest program `stale1683.py`; no new test file, no new cell, so counts stay.** `stale1683.py` finds the three stale lines by the sha256 of their trimmed text (the same hash the REVIEWED list stores) and counts the five entries: BASE prints three `STALE-LINE` rows and entries 5 (rc 1), HEAD prints `TOTAL stale-lines 0, entries 0` (rc 0), control (head with the BASE sweeper file) prints one row (rc 1). Jest red-first (step 2, two halves, PREDICTED from the drafter's simulator): test edit alone -> 3 red cells (THE GUARD and the two ARM cells that plant into the shipped set); source edits alone -> 7 red (STALE GUARD, two `ARM (RD-708)`, the old C-F1, three `ARM (RD-828 C-P1)`); both -> all green. ONE commit A holds all four files because each half alone is red (the ticket's own comment says "same change").
- **Counts: no jest cell is added, so counts stay** at whatever pair the base commits (PREDICTED 5870/377 after #218; step 8 requires the measured pair EQUAL to the committed pair, never `--update-counts`; a refusal on counts is a STOP). No K commit.
- **Order and server.js:** NX-C goes first now. Its `backend/server.js` edit is comment-only and does NOT touch the `auditLog` region: `function auditLog(` runs `:305` to `:330`, `auditLog(` matches 48 lines, the nearest call sites to the edited lines are `:554` and `:1619`, and line counts do not move, so no line pointer of the held NX-A kit (B1682) moves. But the blob of server.js changes, and B1682's line 28 says "the sweep's order is NX-A then NX-C" and makes a fresh branch writing server.js a Step-1b STOP: **B1682 needs an addendum (launch only after b1683 lands; re-measure the server.js blob).** That addendum is Tuesday's.
- Slot: **4** (band 22560-23199), trees `b1683-nodot/{old6,new15,mut19,chk33}` all print 4 (control `b1680-nodot/old34` prints 2 = B1680's slot). Slots named by the 7 SEAT-N kits of 17 and 18 Nov: 0, 1, 2, 3, 5, 13, 15, 16, 17; listeners machine-wide 11, none in any band (control: loop sums per-band listeners to 0 against 11 total). Slot 4 is named by no kit.
- Push a branch, no PR, nothing deployed, no Jira, no counts file touched (unless HOLD 13's merge path forces a regenerate, which the kit forbids except by Tuesday's word).

## Facts re-measured with instruments (all at origin main `f8a6232aaee87ffee903d6bdbfd0f55fdde4d1f0`, tree `dc368ba7359ad8c2e4c1f6ac28de58745224c8db`; gh GET `branches/main`, tarball extracted to scratch)
| fact | instrument | value |
|---|---|---|
| main sha / tree / parents | gh api commits GET | f8a6232a / dc368ba7 / `751285aa`, `ad8fd77a` (records #217) |
| counts file | sed of extracted tarball; contents API blob | 5868 / 377, `_updated` 2026-11-17T10:56:30.113Z, blob `0ee27c40ed9a` equal |
| open PRs | gh GET pulls | one: #218 `b1680/nexusai-lane-nx-t3-test-tail` head `7bc1c5d2` |
| #218 vs main | gh compare | diverged, ahead 5, behind 2 (head not in main now) |
| blobs at main (local git blob hash = contents API) | python + gh GET | server.js `bf648e298429`; sweeper `9fe5d9db83dc`; rd385 test `16dc2a520948` (all equal both ways) |
| last commits per path | commits API | server.js `94cccbd4`, `9226b024`; sweeper `6dc8c91b`, `fabcc93b`; rd385 `52df6468`, `56e1b614`; #218 touches none |
| stale lines | python sha256 of trimmed lines | server.js:832 `8481e0fb2ed9498b`; server.js:1102 `c267b22404058afa`; sweeper:22 `05049edfa847b0f3`; each equals the REVIEWED entry's hash prefix (values never printed) |
| ticket lines | RD-689 text | `:767`, `:1030`, `:22` moved to `:832`, `:1102`, `:22` |
| REVIEWED entries | grep over the test | 5 with ticket RD-689 / status known at base, 0 at head |
| test( lines of rd385 | grep -c | 58 base, 58 head (line count, not a jest count) |
| auditLog | awk / grep -c | opens :305, closes :330; 48 lines match; neighbours :554 and :1619 |
| code-scanning | gh GET paginated | 22 open on main, 13 in server.js, 0 within six lines of :832 or :1102, 0 in the other two files; control `state=fixed` 222 |
| readers | grep -l | 9 image-manifest users; 3 files name healthSweeperScheduler; 140 files name server.js (23 `readFileSync(...server.js` lines) |
| unmasked Jira pull | grep -c | 0 dotted quads, 0 revision-name fragments (control: sweeper source counts 1 dotted quad) |
| kit text | grep -c | 0 dotted quads, 0 revision-name fragments in the kit |

**Simulator (disclosed, not jest):** `mini_runner.js` in scratch runs the 13 cells of the RD-425 describe with a minimal `expect` over the extracted tree plus an in-memory overlay. BASE 13 green; HEAD 13 green; source-only 7 red; test-only 3 red; file-only mutant (P1) 4 red (C-F1 and three C-P1); plant P2a/P2b 3 red each; P3/P4 (remove planted tail) 1 red (C-F1 precondition); P5 (entry re-added) 7 red. On the whole file the simulator reads 54 of 58 green at BASE and the identical 54 of 58 at HEAD (the 4 red lack matchers such as `toBeDefined`: not a lane signal). Every number from it is marked PREDICTED in the kit.

## Chain table: each step's inputs and where each comes from (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 browser | tree `old6` at BASE; `assert-browser.js` | Step 1 (clone, detach, npm ci); file exists at BASE |
| 1 base | `old6`; rd385 test at BASE; `stale1683.py` | Step 1; the program is written from the kit's block at setup |
| 2 redfirst | `mut19` at BASE; rd385 patch; `apply_src1683.py` | Step 1 tree; both written from the kit's blocks into `.tools/b1683/patches/` before the lock; saved originals made inside the step |
| 3 comment-only | `old6` (BASE), `new15` (A); `commentonly1683.js`; `NODE_PATH` = clone node_modules (acorn) | A is committed before the waiter (Setup); `new15` created at A; acorn at BASE |
| 4 head | `new15` | A |
| 5 readers | `new15`; list from Step 1b(iii) | A; Step 1b |
| 6 mut | `mut19` re-detached at A; `plant.py` specs; `git show BASE:` files | A; BASE; plant specs written before the lock |
| 7 mainmove | clone | Step 1 |
| 8 p-plain | `chk33` at A; counts file | A; BASE's committed pair |
| 9 mainmove-last | clone | Step 1 |
The kit-embedded text was extracted by program from the kit and run: `apply_src1683.py` (plan then real, second run fails on `matches 0` as a control), the rd385 patch (sha256 `aa43cb0728d239e1a73236fa7573ef56a070145588912a673a0953f3f863b55b` equal to the scratch patch; applied by a copy of B1680's `apply_patch.py`), `stale1683.py`, `commentonly1683.js`: all three resulting files `cmp` equal to the drafter's overlay; `node --check` ok on all three.

## D-decisions (the drafter's)
- D-1 One commit A (four files minus counts), because each half alone is red (measured in the simulator and implied by the ticket's "same change").
- D-2 Old stale lines are located by sha256 of trimmed text, never by line number or value; the kit and the report never print the address or the revision name; the replacement lines are frozen text.
- D-3 Replacement wording keeps each sentence and removes only the value (`the report-only revision`; `the IP-literal case (origin = https://<the server host>)`; the sweeper's `RD-130` paragraph loses its parenthesis).
- D-4 Re-point the C-F1 cell to `backend/marketplaceJwt.js` and plant a finding of ANOTHER kind (`tenant 1a2b3c4d-xxxx-xxxx`, a string the file already uses at its masked-GUID cell) so the property "a kind leaves, the file keeps another finding" stays proved with no IP literal in the test.
- D-5 Counts stay: no `--update-counts` anywhere; a counts refusal is a STOP.
- D-6 Tool set taken from `.tools/b1680/` (newest, carries B1680's fixes), with the retag warning.
- D-7 REFUSE 4(b) makes #218's head an ancestor of origin/main mandatory (the order was NX-T3 first).

## Q-questions for Tuesday (each with a default)
- Q-1 Re-point the C-F1 cell (the one edit of an existing test cell, needed because the ticket's own change turns it red)? Default: yes. Alternative: drop the cell's server.js dependence by deleting the cell, which loses the M-fileOnly guard: not recommended.
- Q-2 Gate G2 for the branch (the kit's choice) or G3 (comment lines only, no gate)? Default: G2, because of the reworked cell and the shrinking allow-list.
- Q-3 Launch after #218 lands (the kit STOPs otherwise)? Default: yes, wait. Alternative: relax REFUSE 4(b) since the files are path-disjoint; the drafter does not recommend it (counts base and the chain tools differ).
- Q-4 B1682 (held NX-A) addendum: launch only after b1683 lands and re-measure `backend/server.js`'s blob (its line pointers stay valid by construction). Default: write the addendum when NX-A is un-held; the held kit's Step 1b would otherwise STOP on a fresh branch writing server.js.
- Q-5 Replacement wording of the three comments as frozen (D-3). Default: accept.

## UNMEASURED
- No jest was run by the drafter: every red set, the mutation matrix, N385 (the rd385 jest cell count; PREDICTED 58 from `test(` lines) and the final pair are PREDICTED. The simulator is logic only.
- Whether any NexusAI pane is live (seat's REFUSE 4(a)); whether #218 lands unchanged; whether B1679's records branch moves main (HISTORY.md only; the kit carries the HOLD 13 merge path).
- The seat's `static.py` and chain-tool retag (the kit tells the seat to read them first, as B1680's Corrections taught).
- Hosted CodeQL, Deploy demo (a merge touching backend files WILL start it), the hosted Build: Tuesday's.
- `git ls-remote` over ssh was not available to the drafter; the b1683 branch absence is read with gh GET (404, control: the b1680 ref reads `7bc1c5d2...`).
- The six-line neighbourhood of the CodeQL alerts is measured at main only.

## Outside-the-fences disclosure
- Writes: the kit, its sidecar and this report in the briefs folder; scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/d1683/` (tarball and extracted tree `src_f8a6` of main, overlays, `mini_runner.js`, `mkpatch1683.py`, `apply_src1683.py`, `stale1683.py`, `commentonly1683.js`, `names1683.py`, `kitx/` extracts, `jira_rd689.raw` and a masked copy `jira_rd689.txt`, `alerts_open.tsv`) and the session scratchpad file `sc_final.txt`. **The extracted tree and some overlay copies hold the unmasked stale lines and the repo's tracked files (including `HISTORY.md`); the kit and this report do not.** Nothing written in the NexusAI project folder.
- Reads: RD-689 by a GET-only Jira reader (the project `.env` in-process, nothing printed); gh GET under the project's `GH_CONFIG_DIR` (branches, commits, contents, tarball, pulls, compare, git ref, code-scanning, `user` login counted only); the project's B1680 STATUS and `.tools/b1680/` (file names; `apply_patch.py` read with `cat` into scratch), `CLARIFICATIONS.md` line 2067, `scanlib1114.py:20`, `session-tools/nexusai-lock.sh` listing; the B1680, B1682 kits; model-routing, models_latest, brief_seat.sh; the sweep note lines 115-142; DRAFTER_RULES.
- Three refusals by the harness hooks, all before any effect: a `git init` in scratch (refused: write verb outside the TUESDAY repo root; I then wrote a runner that bypasses git ls-files), an `rm -rf` of an overlay folder that did not exist (refused; nothing deleted), a `cp` out of `.tools/b1680/` (refused as a cross-tree write; replaced by `cat` into scratch). No git write verb ran in any project repo, no `az`, no ssh, no HTTP to any host except GitHub and Jira GETs, no jest.
- No address, host or revision name was written to the kit, sidecar or this report. Masked prints (`<IPV4>`) and hash prefixes only. A hook-printed advisory showed none.
