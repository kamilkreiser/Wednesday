# DRAFTER REPORT: Seat G 5th launch brief (KS-1171, G-B), 2026-10-08

**Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatG5_raise_ks1171.md` (224 lines, 67,967 B, sha256/16 `85e9931fcf02ee78`). Staged, NOT sent, NOT launched. The only placeholder tokens are `- @@FILL@@` (`:4`, SEND AMENDMENT) and `| @FILL@` (`:224`, SELF-CHECK), by `grep`. Every remaining angle-bracket token sits inside the verbatim PARALLEL-SEAT block (`:130-135`), which is `cmp`-identical to `0_Brain/learnings/2026-09-09_parallel-seats-on-one-project-grant.md:86-91`.

Nothing was written under `!CODING/`. All write verbs ran in my own `git clone --shared --no-checkout` at `scratchpad/g5/clone` (temp `GIT_INDEX_FILE`; one synthetic commit `1656b9735fbf` written into that clone's own object dir). The lock-`find` control was planted in a `mktemp -d` inside the scratchpad, never in the shared `worktrees/` (STANDING_LINES `:443`).

## Headline findings (each is in the brief)
1. **The handover's pathgate re-key is wrong as written.** Its instruction is to set the range to `0a6177ea5482..64eafead891e` and both `4` counts to `9`. I drove that on a synthetic correct G-B head and it FAILS 2 of 6:
   - G-A and G-B both SHARED-APPEND the two platform docs, so "ZERO of PR 0's files" fires on them.
   - `cotenant()` matches lockfiles, the baseline and timestamping paths, and G-A has none of those, so the co-tenant control reads 0.
   - Adding `--allow` for the two docs still FAILS 1 of 6.
   - The corrected spec PASSES 6/6, and its revert-shaped firing control FAILS naming the 7 G-A paths. That spec is: `PR0_FILES` = G-A's 7 non-doc paths with `== 7`, and a second range (B 56th's) for the co-tenant control with `>= 4`.
2. **`commitg1.sh`: G 4th's six fixes are present.** Two of them are correct only for G 4th: `:33` hard-codes `LOCK_SEAT` to `g4` and still overrides the caller, and the count `9` appears at `:58`, `:117` and `:187`. **A seventh live knob survived every G 4th sweep: `:107-111` `git add`s B 56th's four lockfile/baseline paths.** It was a no-op for G-A. It would stage a dirty `services/anchoring/package-lock.json` into G 5th's test-only PR.
3. **`namecheckg1.py` has no `_FOREIGN_G4_*` forms.** Moving `MINE` to `g5` therefore leaves `s-g4-ks593`, `…-g4-1` and the G 4th quarantine ref reading NEITHER. This is the same hole G 4th closed for `g3`.
4. **Lock slot 1 (`.push-lock-56`) cannot be emptied by an env export.** `${OTHER_LOCK:-…}` treats an empty value as unset; I replicated this in bash. The reconcile has to edit the default in both `lockg1.sh:279` and `pushg1.sh:163`.
5. **#1429 (E 11th, KS-1449) was raised during drafting.** It is a third open PR on the doc tail (`… 26, 38`). `40.` is free at develop and on #1427, #1428 and #1429.

## What I measured (instrument, time UTC 2026-10-08)
- **Origin, by `env -u GIT_SSH_COMMAND git -C <shared checkout> ls-remote git@github.com:Secuura/Distributed_Secuura.git`, rc 0, at 07:38:38Z (2,138 lines) and 07:46:54Z (2,141 lines):**
  - develop `0a6177ea5482227e83d5045b68b8577a56326ffc` (unmoved); main `54b2a5c26d75`.
  - Branch counts: `-g5-` 0, `-g4-` 1, `-ra19-` 0, `-ra18-` 1, `-e11-` 0 then 1 (`1271d9597c43`), `-f5-` 0. Controls: `-ra13-` 2, `-ra16-` 1, `-zzNOTREAL-` 0.
  - Highest `refs/pull` went from 1428 to 1429.
- **Shared store, read verbs only:**
  - `rev-parse --all` 1,640 lines, `305d40f3f5ba601b`.
  - `cat-file -e`: develop rc 0, positive control `ddea005553bf` rc 0, negative `deadbeef…` rc 1.
  - Local seat refs by `for-each-ref`.
  - HEAD, local develop and `origin/develop` all read `ddea005553bf`.
  - `FETCH_HEAD` mtime 13:41:23 local.
- **Locks (`find -maxdepth 1` + `cat holder`, two polls at 07:43:02Z and 07:43:07Z, again at 07:46:54Z):** one lock held, `.push-lock-f3`, holder seat `Secuura/Blockchain-F f5`, pid 57482, started 07:39:51Z. The `mktemp -d` control read 1.
- **Panes (`tmux list-panes -a`, 07:46:54Z):** `%0 wednesday`, `%1 fleet-monitor`, `%97` E, `%98` F, `%99` R. `%96` (G 4th) is gone.
- **Worktrees (`ls`):** `s-g4-ks593`, `s-e11-ks1449`, `s-f5-ks1328`, seven `s-ra*`; 0 `s-g5-*`, 0 `s-ra19-*`.
- **Disk (`df -m`):** 392,816 MB available, 80% used.
- **Payload (`wc -c`, `shasum`):** 4,524 B, `11844b4b45cfdff2`, equal to G 4th's figure.
- **Payload apply, in my scratch clone with a temp index:**
  - Strict forward `--check` rc 0, reverse rc 1, re-apply control rc 1.
  - Tree `29c2837b0c74` on base tree `5f456a0128fe`, equal to G 4th's.
  - It also applies at G-A's head (tree `f6f17cf879fc`).
  - The patch has 0 `diff --git` header lines; there is one `---`/`+++` section.
- **Spark tip `46c3e20cfbd2` against develop (`merge-base`, `rev-list`, `ls-tree`, `diff --stat`):**
  - The tip is an ancestor of develop, 77 commits behind.
  - The four blobs the test imports or pins are byte-identical at the tip and at develop.
  - Three anchoring files moved in between.
- **`anchorSubmission.ts` at develop (`git show`, `sed -n`, `grep -c -F`):**
  - `:345` text read.
  - The tamper anchor is unique (count 1).
  - Constants at `:170-171`.
  - Runner is vitest (`package.json:10`, `:36`).
  - `BACKLOG.md:182` names KS 562.
- **Doc tails (`ls-tree` + `cat-file blob`, my `tails.py` with a newline-tolerant reader and document-shaped controls; both controls read):**
  - develop: flow 30 numbers (the SAME reader gives 25), 0 duplicates, tail ends `26`; cheat 19 sections, tail `… KS-591, KS-1164`.
  - #1427 tail ends `35` / `KS-1274`; #1428 ends `39` / `KS-593`; #1429 ends `38` / `KS-1449`.
  - `KS-1171` appears 0 times in every doc.
- **REVIEW.md** read whole (34 lines, `3fc0a6b5aa748c0f`), plus `checker.out`, `round.json`, `sections.json`, `numstat.out` and `suite_delta.out`.
- **Q-HOLD18 still holds, by `ls`:**
  - The run dir holds no READY file.
  - `local-model/night/` has 10 `READY_KS-1171*` entries (6 live, 4 `.pre-*`), all for other KS-1171 passes. `grep` for `b1|boundary|inclusive` over them returns rc 1.
  - Positive control: `READY_KS-593-SIGNATORIES…` is present.
  - The older passes' tests are already on develop (`ls-tree`).
- **Tools:** 25 of 25 hashes and line counts equal G 4th's `_FINAL_HASHES_g4.txt` and WRAP (`shasum`, `wc -l`). `pathgateg1.py`, `commitg1.sh` and `pushg1.sh` were read whole, along with the relevant regions of `lockg1.sh`.
- **Matcher and namecheck, read with `ast`:**
  - `inbox_matchg1.py`: `MINE` `'g 4th'` at `:102` (double quotes in the file); `OTHER_SEATS` at `:212` has 135 entries, all distinct.
  - `namecheckg1.py`: `MINE` `"g4"` at `:72`; `FOREIGN` has 139 entries.
  - Probes recorded in the brief.
- **Shape sweep (my `shape_sweep.py`) over the 13 RUN tools, 7 patterns:** the planted control fired 7/7. Counts are in the brief as an EXPECTATION only.
- **Project MUST line numbers:** re-read at develop by `git show` + `sed -n`. All hold; SKILL, repo `CLAUDE.md` and `systemTest/CLAUDE.md` blobs equal those in G 4th's brief.
- **Usage gauge (`usage_gate.sh --check`, 07:43:49Z):** 92%. Bare: rc 3. With `WED_USAGE_STOP=100`: rc 0.
- **Hashes of the grant file and the parallel-seat learning:** recorded in the brief. The parallel block is `cmp`-identical to the R 19th brief's copy.

## What I could not measure (and why)
- **Linear state of every ticket:** I have no Linear access. PROVENANCE ticket lines are left as `| to be read by Wednesday at send | —`. The board-guard sentence quoting KS-1171 as "In Progress" is attributed to Wednesday's 18:21 read in the R 19th brief, not to me.
- **PR API state (`mergeable_state`, reviews, Actions) of #1427, #1428 and #1429:** no GitHub token here.
- **G 5th's pane id:** the seat is not launched.
- **The anchoring suite total at develop, and the tamper red at develop:** that needs a worktree plus installs, which belong to the seat.
- **Whether G 4th ran `raiseg1.py` for G-A:** no invocation shows up by `grep` in its record.
- **Whether `r 21st`, `e 12th` or `f 6th` will appear mid-round:** a future event.
- **The R 19th and F 5th payload file lists:** carried from the R 19th brief's partition table, not re-derived from their run dirs. E 11th's anchoring files WERE re-read from its run dir.

## pathgateg1.py re-key spec (exact)
1. `:26-31` `PR0_FILES` → G-A's 7 non-doc paths, all prefixed `Blockchain/Dev/services/originate/src/`:
   - `__tests__/ks1293-originate-suite-is-hermetic.test.ts`
   - `__tests__/ks593-adminconfig-list-refuses-negative-offset.test.ts`
   - `__tests__/ks593-share-refuses-non-object-recipient.test.ts`
   - `__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts`
   - `routes/adminConfig.ts`
   - `routes/documents.ts`
   - `routes/signatories.ts`
2. `:32-33` → `OLD_BASE = "0a6177ea5482227e83d5045b68b8577a56326ffc"`, `NEW_BASE = "64eafead891e81f5adb4e46aaa94ff6a6ace1998"`.
3. Add `CO_OLD = "88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e"` and `CO_NEW = "e6daa806e79a14a580f064db95e797c1fd671dc7"`. Change `:105` to `ctl_co = [p for p in names(wt, CO_OLD, CO_NEW) if cotenant(p)]`.
4. **The two hard-coded `4`s:**
   - `:114` `len(ctl_pr0) == 4` → `== 7`.
   - `:115` `len(ctl_co) >= 4` stays `4`, because it now runs over its own range.
5. Re-key the labels and prose at `:15`, `:21`, `:106-108`, `:112`, `:114`, `:115` and `:131`.
6. Three arms:
   - PASS on the real head.
   - FAIL on a G-A-revert head, naming the 7 paths.
   - FAIL on a dropped declared path.

Trial evidence: `scratchpad/g5/pathgate_trial.sh` and `pathgate_trial.out`.

## commitg1.sh confirmation (`bb2ebab6d661aba3`, 192 lines, read whole)
| # | G 4th's defect | State in the inherited copy |
|---|---|---|
| 1 | `LOCK_SEAT` override | **Still a hard-coded override** (`:33`, `g4`). Fixed only for G 4th; G 5th must re-key it. |
| 2 | Holder-pid dir | FIXED (`:68-70`, `.push-lock-g1`). |
| 3 | Vacuous release test | FIXED (`:85`, `.push-lock-g1`). |
| 4 | Release rc through `echo` | FIXED (`:77-82`, `RELRC=$?` on its own line). The other rc echo pairs print a captured variable. |
| 5 | EXIT trap status | FIXED (`:74` `TRAPPED_RC=$?`, `:88` `exit $(( fail > 0 ? 1 : TRAPPED_RC ))`). |
| 6 | Stale count | `9` at `:58`, `:117` and `:187`. Fixed only for G-A; G 5th needs `3`. |

- **No pre-trap exit after the take:** the only exit between `:62` and `:90` is `:66`, on a failed take.
- **Extra findings:**
  - `:106-111` stage B 56th's four paths.
  - `:130-154` carry G-A's body, including `does not close KS-593`.
- **Adjacent and unchanged in `pushg1.sh`:** `:235` releases with `$$` and never reads the rc; `:197` and `:206` use `|| true`; `:247` exits with the push rc. The brief requires a post-push lock `find`.

## Departures from the predecessor shape, with reasons
- **A "TOOL FIXES" section with sub-parts (a) to (e)** replaces R 19th's single "COMMIT TOOL FIX". G 5th inherits five tool items, two of them load-bearing and measured to be wrong.
- **One raise, not two;** no RESUME stack table. The queue is a single ticket.
- **The branch is `-g5-1`, not G 4th's reserved `-g4-2`.** The reasons are stated in the brief: attribution by namespace, the namecheck `_MINE_BRANCH` rule, and that the `-g4-2` name was only a reservation (0 at origin, 0 local).
- **A pin's red is a reverted tamper** (Q-TAMPER-G5), so the red/green item cites the tamper rules instead of a base red.
- **I did not carry the "RULED BY KAM, NOT YET IN AN ARTEFACT" card list.** Wednesday generates it at send (`decision_queue.sh`); it is not drafter material.
- **The flow tail is shown on THREE open PRs** (R 19th's brief showed one), because #1428 and #1429 now exist.
- **G 4th's planted-in-`worktrees/` lock controls are named as now forbidden,** because of STANDING_LINES `:443`.
- **Squash-subject length is given both ways:** namecheck's `+8` reads LANDS 90, and STANDING_LINES `:319`'s no-append rule gives 82. Both are under 92, and the tool's gate wins for its own check. The two sources disagree; I did not resolve which is current.
