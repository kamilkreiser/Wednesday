STARTABLE: YES (after Tuesday stamps the 7 slots and the last line; 8 four-underscore lines in the kit, counted with the split pattern; load1 2.52 at 08:43; launch only through launch_when_cool)

# B881 drafter report (Tuesday's kit drafter), 2026-10-28 08:32 to about 08:46 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B881_SEAT-G196_nexusai-138-rd897-retire-gate-tier2.md` (112 lines). Shape copied from B870, the gate of #136: STATUS channel, REFUSE AT ONCE, SEATS, INSTRUMENTS, THE WORK C1-C10, MAIN-MOVED RULE, GRADING, ROUND COUNT, LOAD, NOT TESTED, HOLDS, PARTITION, VERDICT, LANDING, Stamp, last line.

## BLUF
- **Seat G196, ports 9820-9829.** B878 = `SEAT-G194` (Composer, ports 9010-9019) and B879 = `SEAT-G195` (Composer, ports 9980-9989). Both are now live panes. Neither kit names G196 or B881. B879 mentions 9820 only inside its list of "free decades" (sentence read), not as its own block.
- **Main moved while I was drafting.** PR #137 (`records/b875`, `HISTORY.md` only) merged at 08:34 AEDT, so main is now `bdb9c170`. PR #138 is ahead 1 and behind 2. At 08:43 the merge ref was still `ff87d722`, over the old main, and `mergeable_state` read `unstable`. GitHub will recompute the merge ref and re-run the checks. The kit expects the new merge ref, and its tree will be the head tree plus `HISTORY.md`.
- **CI at 08:43:** the three `Analyze` runs completed/success with 0 results each, and CodeQL reads success. These checks are on the old merge ref. `build` is in progress. 0 open alerts on the PR ref.
- **Deploy switch:** variables 0, environments [dev]. A merge starts `Deploy demo`, whose two jobs skip while the switch is unset. The precedent run 40573355386 skipped, 0 steps.
- The builder's "two reds, one cause" claim is checked twice:
  - **C5 (a)** diffs `jsCorpus()` with the project's own helper.
  - **C5 (c)** runs four fixture variants: FX1 and FX2 each lower only one count, FX3 lowers one count too far, and FX4 runs the head fixture against the base `index.js`. Together they prove 5/5 is the only value that goes green.

## Facts re-measured (instrument, control)
- **Pins:** `ls-remote` at 08:32:56 and 08:43:03 (control: `b881*` reads nothing). Head `939d5c5a` both times. Main `79addb5a`, then `bdb9c170`.
- **Main move:** `compare/79addb5a...main` = ahead 2, `HISTORY.md` only. `git/commits/bdb9c170`: parents `79addb5a` and `cd94c760`. `pulls/137`: merged.
- **PR #138:** `pulls/138` + `/files`: open, non-draft, 1 commit, 2 files, +2 / -84. Blobs: `5db46946` (fixture), `61e57274` (`index.js`).
- **Trees:** the head tree and the merge-ref `ff87d722` tree are both `333e0741`, with parents (79addb5a, 939d5c5a).
- **Range proof:** raw `contents?ref=` copies at base, head and merge, each `git hash-object` equal to the expected blob. Run with `python3 -I`:
  - Dropping 9223-9264 and 9421-9460 compares equal.
  - Four controls compare unequal.
  - **NEW:** dropping 9420-9459 ALSO compares equal, because base 9420 and 9460 are both blank. This is the builder's 9222/9264 observation on the second range. The kit makes the gate's controls move a non-blank boundary.
- **Fixture:** the object diff is exactly entries[21] and entries[53], count 6 to 5; sum 144 to 142; text lines 176 and 437. Colour-literal lines in the ranges: exactly 9250 and 9252.
- **rd200 test** (blob `5219fd51`) read whole at 40-156. REPORTS asserts `remaining` against the manifest sum, which explains the builder's second red. RESOLVES fails when a count is set too low, which is the basis for FX3 and FX4.
- **Script scope:** `static/index.html:21` loads `index.js` as a classic script, so its top-level functions are globals. `csp-helpers.js:97` resolves handler names through `window[fnName]`. `index.html:289` gives the dropdown `data-csp-fn="handleFilterChange"`.
- **CI and the deploy trigger:**
  - Blobs and lines: `deploy-demo.yml` `597b3487` (26-31, 53, 91, 95), `build.yml` `e4e5c095` (29, 83-84), `verify-suite.sh` `eb9731f5` (91-92, 366), counts file `38c0ae66` (5223/310).
  - `deploy.yml` is dispatch-only. `arm-ttk` is path-filtered and does not match this PR.
  - Main's own push runs on `79addb5a`: Build success, Deploy demo skipped (jobs deploy and build both skipped, 0 steps).
  - Open alerts on main: 124.
- **Jira** (read module loaded in-process; control: RD-zzz returns 404): RD-897 is To Do with 0 comments. The reachability JQL (with parentheses) returns RD-897 only.
- **HISTORY.md at `bdb9c170`:** 4 lines match the two names, against 2 at `79addb5a`. The kit warns the gate.
- **Plumbing and environment:**
  - Lock tool sha256 `cf01bafb...` and fence `55eaafcb...`, both equal to the template.
  - `queue-jest/` empty at 08:35.
  - No `worktrees/b881*` or `session-tools/b881*`.
  - `lsof` on 9820-9829: rc 1 (control: the unrestricted listing shows `*:7000`).
- **Routing:** `model-routing.md:109` (G2), `:108` (G1), `:111` (G-cap). `models_latest.json:23` = `claude-sonnet-5-5`.
- **Round count:** STATUS grep `939d5c5|#138|b877|RD-897` hits B854, B855, B856, B875 and B877. No gate verdict names #138. The NO GO census finds 3 files (B592, B647, B667), none of them this class.

## D-decisions
- **D1 Merge tree.** The gate runs on the fetched merge ref, as B870 did. Fetch names are `pr138head` and `pr138merge`, which avoids B870's `origin/b862` collision between a ref file and a directory.
- **D2 Censuses go wider than the builder's.** The acorn census covers every `static/js/*.js` and inline HTML script, not only `index.js`. It prints each declaration's ancestor chain. Computed lookups are extended to `globalThis`, `self`, `top`, `parent` and `Reflect`. There is also a reading-only (e) for function names arriving from data. Plant controls sit outside the trees.
- **D3 Grading.** A caller at base is a Blocker (the PR would remove live code), and the gate finishes rather than STOPs. If that caller is reached through data, it is a hand-up STOP. `clearAnomalyTables` is a Note with ticket text, per scope.
- **D4 Fixture variants FX1-FX4** are the tier-2 "named mutants". They prove the two counts are forced by the deletion, not just sufficient.
- **D5 Target and hard stop:** 150 and 240 minutes after the gate's own Step 0, as in the template.

## Q-questions for Tuesday (each with a default)
- **Q1 Tier.** This PR changes a product byte, and row G2's text lists "tests-only ... follow-ups whose mechanism a prior gate already measured". The tier comes from your B877 stamp (Q-5). Default: accept tier 2, with the security hand-up in place.
- **Q2 Main moved (#137).** The kit expects a recomputed merge ref. If the gate fetches a stale `ff87d722`, it says so and the hosted facts belong to that ref. Default: accept. Landing waits for the refreshed `build` and `Analyze` runs.
- **Q3 FX1-FX4.** Four extra small rd200 runs. Default: keep them.
- **Q4 The stray comment** at base 9265: fold it into the `clearAnomalyTables` follow-up ticket. Default: yes.
- **Q5 G196 / 9820-9829.** Default: accept. Re-run the port scan at the stamp.

## UNMEASURED
- The recomputed merge ref, its tree and its hosted checks (not yet present at 08:43).
- Whether `build` passes on either merge ref.
- Every jest figure, the 49-file neighbour set and the verify. These are RELAYED from the builder.
- The acorn counts (296 / 294) and the dispatch-census counts. These are RELAYED; I did not run acorn.
- What `pulls/138` reads for `mergeable_state` after the recompute.

## Outside-the-fences disclosure
**Read:**
- `DRAFTER_RULES.md`; the B870 kit (stamped and `.pre-stamp` Stamp section) and its drafter report; the B870 STATUS (first line, section heads and Corrections only).
- The B877 kit and STATUS, both whole; the B878 addendum; the B878, B879 and B880 kits (port and seat lines only).
- The decision card, via `decision_queue.sh show <exact id>` into a scratch file, checked with an id filter (count 1). No `list`.
- `model-routing.md` rows, `models_latest.json`, and the `launch_when_cool.sh` and `brief_seat.sh` headers.
- `CLARIFICATIONS.md`, by grep only.
- `b774lib.py` function list. Jira GETs ran in-process through its `get` and `search`, and no token was printed.

**Network and system calls:**
- `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`. `ls-remote` on the shared repo.
- `tmux list-panes`, `lsof`, `shasum`, and `ls` of tree names.

**Not done:** no clone, fetch, install, jest, acorn, az, ssh or hosted HTTP. Nothing written in the project.

**Hooks:** one `=` separator was refused by the hook and redone with `----`. Some grep-case advisories fired; the counts that mattered were re-run with controls.

**Scratch** (session scratchpad, `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2a96b7d2-d53a-41cf-bf98-7cf754ae785e/scratchpad/`):
- raw file copies, `card.txt`, `jira.py`, `portscan.py`, `rangedrop.py`, `fix.py`, `fix2.py`;
- a pre-edit kit copy, `kit_before_mainmove.md`.

**Writes:** only the kit and this report.
