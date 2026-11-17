STARTABLE: YES at main `ed3b1aed`: no B1648 STATUS and no `b1648*` branch exist, so the NX-AUTH kit is not launched. If Tuesday launches B1648 first, this kit waits for it (REFUSE 4, one at a time). Q1-Q7 keep B1634's defaults. Q7's wording changed: the lane beside this one is now B1648, not B1633.

# B1652 DRAFTER REPORT (SEAT-N141, NexusAI lane NX-P re-draft, SUPERSEDES the unstamped B1634), drafted Tue 17 Nov 2026 05:31 to 05:42 AEDT (`date` 05:31:00 at the first read, 05:42:24 at the last)

**Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-17_B1652_SEAT-N141_nexusai-lane-nx-p-periphery-codeql.md`.
- 145 lines; sha256 prefix 1458e0bd652da14e at 05:42.
- 5 lines carry the four-underscore pattern: the four slots and the last line.
- 0 non-ASCII characters.
- Person-name scan over kam, kamil, kreiser, paul and peter: 0 hits. The scan is underscore-aware; a planted `x_by_kam_y` fires 1 and `kamikaze` fires 0.
- The card / decision-queue pattern hits 11 times. Every hit is a prohibition or a scan instruction, the same 11 as in B1634. The kit contains no card id and no decision id.

**Sidecar** `.md.measured`, 199 lines:
- 103 claim lines. Each is a real count over the `ed3b1aed` export, my scratch reads and the project docs, with the specific measurement appended.
- 95 `src` lines. Each prints a code, test or finding line that the kit freezes a sentence about.
- `stamp_check.py <kit>` prints `103 claims, 103 measured, 0 not measured`, rc 0.

**Generator:** the kit is B1634's text transformed by `fleet/state/s285/b1652/gen_kit1652.py`. It makes 75 substitutions, and each one asserts its match count. Sentences whose fact changed were rewritten whole. Every part, owned path, fence, HOLD and question of B1634 is carried byte-for-byte unless it is listed under D-decisions. B1634, its sidecar and its report are untouched.

## BLUF
- **The lane's code did not change; the numbers around it did.**
  - All three owned source files, and every file the kit reads or points into, are blob-equal at `dcac002d` and `ed3b1aed`: 16 of 16 by `git hash-object` over both exports.
  - All 49 code lines that B1634 froze print identically at `ed3b1aed` (49 equal, 0 moved).
  - #209 changed `backend/jsonStorage.js`. Four flows start in the settings or risk-condition file. They now begin at `jsonStorage.js:583` (was `:550`) and pass `getSetting` at `:3419-:3453` (was `:3377-:3411`). No step changed its file, text or order.
- **Local CodeQL re-run at `ed3b1aed`:**
  - BASE reads **33 = hosted 33**, row for row by (rule, file, line), in both directions.
  - The scratch CANDIDATE re-applies B1634's candidate edit by program. It reads **29**. Gone: #79, #80, #81 and #82, and nothing else. New rows: 0. #145 and #146 are still reported.
  - B1634's conclusion still holds: Part 1 closes RD-771, and Part 2 is defence in depth that cannot close #145 or #146.
- **Counts:** main reads 5828 / 374 (was 5774 / 369). The PREDICTED pair after this lane is about **5845 / 376** (was about 5791 / 371).
- **Alert states (hosted, 05:31):**
  - RD-771: #79-#82 open.
  - RD-805: #143, #144, #145, #146 and #150 open. #147, #148 and #149 (`emailService.js`) are also open: the NX-S2 seat read them as intended and left them open (B1633 STATUS, PART 7).
  - RD-804: #142 open; #138-#141 fixed on 2026-10-18.
  - All three tickets are To Do, and their `updated` stamps match B1634's read.
- **Sequencing:**
  - NX-S2 has ended (READY B1633) and landed (#209 = `3ba5d004`).
  - The lane beside this one is now NX-AUTH (B1648, RD-999). Its OWNS block and this kit's share only the counts file (printed by program).
  - B1648 is drafted but not launched, and its card is unruled.

## Facts re-measured (instrument; control)
1. **Main and counts.**
   - Main is `ed3b1aed592b0a249c32537c49f390efde9b59d5`, tree `5145e124...`. Its parents are `3ba5d004` (#209) and `89bf3ca1` (#210 records).
   - `gh api -X GET branches/main` read it at 05:31 and again at 05:39, unchanged. Open PRs: 0.
   - `compare dcac002d...ed3b1aed` shows 11 commits and 15 files, exactly the list in Tuesday's commission.
   - The counts file reads 5828 / 374, `_updated` 2026-11-16T11:18:54.126Z.
2. **Alerts.**
   - 33 open (paginated; control: `state=fixed` returned 218 rows, more than one page).
   - Every row's `commit_sha` reads `ed3b1aed`. The javascript-typescript analysis of `ed3b1aed` completed at 2026-11-16T15:33:41Z with `results_count` 33.
   - The lane's ten rows keep their numbers and lines (`alerts_lane.tsv`, all states).
   - The 23 rows outside the lane: #147-#149, #151, `server.js` x13, #73, #74, #112, #235, #113 and #236.
3. **Local CodeQL.** `cq_run1652.sh` ran CLI 2.27.4, security-extended, threads 2.
   - Input: the tarball export of `ed3b1aed` (80 MB, 1039 files, handled as untrusted data).
   - Database create took 14 s and analyze took 44 s; load1 was 4.8 to 5.9.
   - BASE 33, CANDIDATE 29. `rowdiff1652.py` shows the four `js/incomplete-url-substring-sanitization` rows GONE and no NEW rows.
   - `node --check` passed on the three candidate files.
4. **Flows.** `flows1652.py` printed all 10 `file-access-to-http` rows (`flows_fath.txt`). Against B1634's flows, 6 rows are identical and 4 differ only in `jsonStorage.js` line numbers.
5. **Static truth table.** `trutht1652.js` (node v26.13.0) prints output byte-identical to B1634's: 2 of 15 hosts differ, and `127.0.0.1` reads true before and after.
6. **Tests at `ed3b1aed`.**
   - B1634's pattern (`js/(index|settings).js` or the quoted name) finds 33 files naming the pages. A stricter `static/js/...` pattern finds 27, so the kit states which pattern it means.
   - 11 files name the router.
   - `entra-provisioning-setup.test.js` has `jest.mock('axios')` at :27 and 19 `test(` lines.
   - The five tests #209 added name none of the static pages, the router or `entraTenantId` (0 each).
   - All 15 named related suites exist.
7. **Branches.**
   - 46 `heads/b1*` refs. Two are ahead of main: the stale `b1480` pair, now 121 behind.
   - Neither names a code or test path of OWNS-B1652, but **both name the counts file and `backend/server.js`**.
   - `heads/b1652*`, `b1634*` and `b1648*` each read 0 (controls: `b1618` 1, `b1633` 1).
8. **Partition.**
   - A program parsed both OWNS blocks: `OWNS-B1652` and `OWNS-B1648` intersect only in `scripts/verify-expected-counts.json`. `backend/jsonStorage.js` is not in OWNS-B1652 (`partition.txt`).
   - RD-999 is B1648's ticket (Jira GET: To Do, label records-pass-1117).
   - RD-1000 is `POST /api/chat` in `backend/server.js`. That file is not owned, and the kit fences it ("Never: backend/server.js").
9. **Slot and port.**
   - I kept slot 15. `names1652.py` printed its controls equal to the kits' values: b1430/b1 6, b1587/upd23 18, b1563/old12 1, b1603/old13 12, b1634/old49 15, b1648/old8 16, b1633/old22 17.
   - Trees under `b1652-nodot/`: `old1 new7 inv4 mut8 v6 chk33 chk61`, all slot 15. None exists yet.
   - Band 29600-30239 had 0 listeners at 05:34 and 05:36 (machine-wide: 12).
   - Slots named by the 42 SEAT kits of 16 and 17 Nov: 2, 12, 13, 15 (B1634), 16 (B1648), 17 (B1633).
   - No port block is requested.
10. **Jest lock.**
    - The lock base `session-tools/locks-laptop-1017` and `nexusai-lock.sh` both exist.
    - `queue-jest/` was empty at 05:36: no holder, no waiter.
    - The NX-S2 seat held the lock once, for 80 minutes (RELAYED from its STATUS `## CHAIN LOG`; the line is printed in the sidecar).
11. **Toolchain and CI.**
    - node v26.13.0 and npm 11.20.0 at `/opt/homebrew/bin`. CI uses Node 24 (`build.yml:29`).
    - `build.yml:64` and `:92-93` are unchanged (blob equal).
    - Deploy demo: the #209 merge's run 43875455476 reads `completed` / `skipped`. The #210 merge started no Deploy demo run (4 runs on `ed3b1aed`, none of them Deploy demo).
12. **Routing, landing and identity.**
    - C3 is at `model-routing.md:93`, G1 at `:108`, and `claude-opus-5-5` at `models_latest.json:17`.
    - `CLARIFICATIONS.md:2067` is still the merge-path rule.
    - Identity source `.tools/b1633/clone`: name length 12, email length 46, and the email equals `.tools/b1618/clone`'s (values never printed).
    - `gh api user` login contains "datasec" (count 1; control 0).

## D-decisions (what changed versus B1634; everything else is carried)
- **D1-D7 carried unchanged** from B1634: Part 0 reading first, D2 words, D3 inline suffix, D4 vm-cut test, D5 inventory `--check` only, D6 sequencing (now against B1648, see D9), D7 Opus C3.
- **D8 Every frozen number is re-measured at `ed3b1aed`:**
  - alerts 47 -> 33 (local 47 -> 33, candidate 43 -> 29);
  - counts 5774/369 -> 5828/374, and the predicted pair 5791/371 -> 5845/376;
  - flow pointers `jsonStorage.js:550` -> `:583`, plus the `getSetting` steps;
  - census 45 -> 46 refs, behind 110 -> 121;
  - fixed-control 204 -> 218;
  - the load, lsof and clock lines, and the CodeQL timings.
- **D9 REFUSE 4 is rewritten.** B1633 has ended and landed, so its wait is gone. The STOP now fires in two cases:
  - a B1648 STATUS exists and its newest line is not final (one at a time: the two kits share the lock and the counts file);
  - `3ba5d004` is not an ancestor of origin/main.
  
  The header, the Level paragraph, HOLD 20 ("NX-AUTH landing first changes the counts file"), COUNTS and the Stamp's HEADS slot all name B1648 where they named B1633.
- **D10 REFUSE 3 is extended.** Any B1634 artefact is a STOP: its STATUS, `.tools/b1634*`, `b1634-nodot`, or a `b1634*` branch. The superseded kit must never have run beside this one.
- **D11 Census correction.** B1634 said the two `b1480` refs hold none of its paths. They name the counts file and `server.js`. The kit now says so, and the Step 0 control expects both refs to print with the counts file.
- **D12 The tool source is `.tools/b1633/`** in place of `.tools/b1618/` + `.tools/b1603/`. It is the newest complete set, it landed a READY, and B1648 copies it too; all 23 files are present.
  - The trap list is updated: b1633, rd765-769, rd421, slot 17, band 30880-31519, its tree names, and `STOP_EPOCH` taken from the HARD STOP slot.
  - `codeql_run.sh` is read from b1633.
  - The identity source is `.tools/b1633/clone`, with b1618 as the fallback.
- **D13 Step 0 reading adds** the B1633 kit, its STATUS (Corrections S1-S7, PART 7, CHAIN LOG) and its HANDOVER, plus the superseded B1634 kit and report. B1603 and B1618 stay on the list.
- **D14 The partition is now against B1648**, printed by program, and RD-1000 is named as outside OWNS.
  - LEFT FOR OTHERS adds RD-999 and RD-1000.
  - The PRIOR WORK STATUS search starts after B1633 and includes any B1634 or B1648 STATUS.
- **D15 Tree names are re-derived** for `b1652-nodot` at slot 15. B1634's names were hashed under `b1634-nodot`, so they do not carry over.
- **D16 The Deploy demo fact is MEASURED** (run id). It is no longer RELAYED from the pickup.
- **D17 Dated names.** The STATUS, HANDOVER, kit copy and ADDENDUM/ANSWER files are dated 2026-11-17. The poll regex is `^2026-11-1[7-9]_B1652_(ADDENDUM|ANSWER)` (control: `SEAT-N141`).
- **No re-measured fact changed** a part, an owned path, a fence, a HOLD or a question default.

## Chain step inputs (each produced by an earlier step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| 0 browser | head tree `new7`, `scripts/assert-browser.js` | commits A, B; present at BASE |
| 1 red-first (`old1`) | BASE tree; the two new test files copied in | Step 1; commits A, B |
| 2 new-cells (`new7`) | tree at B | commit B |
| 3 related (`new7`) | tree at B; Step 1b's census list | step 2 green; Step 1b |
| 4 inventory `--check` (`inv4`) | tree at B; committed role docs (unchanged) | commit B; present at BASE |
| 5 mut (`mut8`) | tree at B | commit B; step 2 green |
| 6 cq (outside the lock) | clone archives of BASE and head; the CLI | Step 1; commit B; also run at BASE BEFORE any edit (Part 0) |
| 7 mainmove | steps 1-6 green | steps 1-6 |
| 8 plain verify (`chk33`) | head of step 7 | step 7 |
| 9 update-counts (`v6`) | step 8's counts refusal | step 8 |
| 10 K (`wt`) | step 9's counts file | step 9 |
| 11 plain verify (`chk61`) | K | step 10 |

No step reads a file that a later step makes.

## QUESTIONS FOR TUESDAY (each with a default; B1634's carried)
- **Q1 Build Part 2 even though it cannot close #145 and #146?** Re-measured: both are still reported on the `ed3b1aed` candidate. Default: build it as its own droppable commit B, and READY says the two alerts stay open.
- **Q2 Words.** Default: no new words (reuse the not-configured answer and `Invalid Entra group ID`).
- **Q3 No shared helper.** Default: an inline `endsWith` in each page, no new static file.
- **Q4 RD-805 and RD-804 stay open after landing.** Default:
  - the records pass comments the reading on both tickets;
  - it moves only RD-771, and only if main's analysis at the merge commit shows #79-#82 fixed;
  - you decide whether a card goes to the product owner about the "intended" class. That class is now 7 rows: #142, #143, #144 and #150 here, plus #147, #148 and #149 read by NX-S2. I posted no card.
- **Q5 Slot 15, no port block.** Default: confirm both at the stamp. B1648 is slot 16, B1633 was 17, and band 15 has 0 listeners.
- **Q6 `127.0.0.1` reads as production (pre-existing).** Default: report it in READY and change nothing.
- **Q7 Order with B1648 (NX-AUTH).** Default: one at a time.
  - If both are ruled to run, launch whichever you stamp first, and the other only after its STATUS ends. REFUSE 4 enforces this from the B1648 STATUS.
  - The second lander regenerates the counts file (HOLD 20).
  - A B1648 seat that has not yet written its STATUS reads as "not running", so your launch-window slot must say that B1648 is not live.

## UNMEASURED
- Every cell's received value. PREDICTED: rd771 about 8 cells with 3 red at main; rd805 about 9 with 4 red; the pair about 5845 / 376.
- Whether CodeQL at the real head reads the same as the scratch candidate. The seat measures it, running BASE before any edit.
- That no existing test breaks under Part 2. Step 1b and step 3 decide it.
- Browser behaviour on a real host (NOT TESTED by design).
- The lock hold. PREDICTED 1.5 to 2 hours; NX-S2's measured hold was 80 minutes.
- B1648's launch state at your stamp time. It was unlaunched at 05:42.

## Outside-the-fences disclosure
- **Writes:** the kit, its sidecar and this report, plus scratch only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s285/b1652/`. The scratch holds:
  - a `prev/` copy of B1634's scratch, without its 1.1 GB databases but with its two sarif files;
  - the retagged `*1652` scripts;
  - `cq/`: the tarball, the base and candidate source trees, two databases and two sarif files (1.2 GB by `du -sh`, deletable);
  - the reads, saved as files.
- **One stray write.** A shell redirect wrote the kit-list scan to `/tmp/x` (2.7 KB, a file listing). I moved it into my scratch as `stray_tmp_x.txt`. `mv` warned that it could not keep the owner/group; `/tmp/x` no longer exists.
- **This report was written by a python temp file + `os.replace`**, because the Write tool refused a report file (the commission's fallback).
- **Nothing written in the project.** Nothing under `/Volumes/Datasec_DEV/!CODING/` was written. No clone, no fetch, no git write.
- **Reads (all read-only):**
  - GitHub, GET only, under the NexusAI `GH_CONFIG_DIR`: branches/main, pulls, commits (2), compare (1 + 46), code-scanning alerts (open, fixed and dismissed, paginated), analyses, actions runs (2 shas), matching-refs, user (count only), tarball.
  - Jira, GET only, through a copy of `jdesc.py` in my scratch: RD-771, RD-805, RD-804, RD-999, RD-1000. The token was read in-process and never printed; no JQL.
  - Project files: the B1633 STATUS (grep and line reads), the `.tools/{b1603,b1618,b1633}` listings, the identity lengths of three clones (values never printed), and the lock folder listing.
  - `tmux list-panes` (names only).
- **Fences untouched:**
  - no `decision_queue.sh`, no `briefs_staged`, no scoreboard, no `_ledger.md`;
  - no WEDNESDAY or FRIDAY tree, no non-Datasec project;
  - no hosted HTTP beyond the GitHub and Jira GET APIs;
  - no az, ssh or docker;
  - no push, PR, mail, board, Artifact or Docs tool;
  - no `cd` typed.
- **Hook events:**
  - One refusal: a zsh word-split `for` over an unquoted variable. Nothing ran; I re-issued it under `bash`.
  - Advisories on case-sensitive phrase greps and on `grep | cut`. No absence is claimed from a cut view; the sidecar's counts are program counts.

DRAFTED B1652: kit 145 lines, sidecar rc 0, questions 7
