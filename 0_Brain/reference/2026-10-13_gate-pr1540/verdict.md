# QA gate: Secuura Platform K PR #1540 (KS-998 item 2 + KS-1483 + fixes for Minors 1, 2, 4, 5, 6 of gate 1532), Opus tier 1

**VERDICT: GO WITH NOTE**: 0 Major, 4 Minor, 9 Info. Bound to head `c6d103ffc4692cb075287eb8143715989abeafab` only.
Report sha256/16: `4fea439ae2902148`
Recipe: delete the single line that starts with "Report sha256/16:", run `shasum -a 256` over the rest of the file, and keep the first 16 hex characters.

- **Head under test:** `c6d103ffc4692cb075287eb8143715989abeafab`. I fetched `refs/pull/1540/head` myself into a scratch `clone --shared` (push URL set to `DISABLED`), using the project's `core.sshCommand`. It matches the brief.
- **Develop:** `a7cffc8d9831e67d91f6dd24d0047ffe3e26c97e`, which matches the brief and had not moved when I fetched. PR 1532's squash `0026a43e6033` is an ancestor of develop.
- **Instruments:** macOS 27.0.1, `/bin/bash` 3.2.57(1) (the only bash on PATH; `/bin/sh` is that bash in POSIX mode), `/bin/dash`, perl 5.34.1, node v24.7.0, npm 11.5.1, git 2.51.0, `sandbox-exec`.
- **Load caveat:** two other Opus gates shared this machine the whole time (load average 9 to 13). Every timing below was taken under that load.
- **Write scope:** no git write verb ran in `!CODING`, nothing was pushed, and nothing was written to GitHub or Linear. Everything ran in `scratchpad/g1540/` or in fixtures. I read the author's runners and history in `5_Project_History/2026-10-13_seatK-9th/` and copied them into my scratchpad. I read K's READY mail from `wednesday-agent@` through the API, read-only, and did not touch `newmail.sh`'s seen-ids file.
- **Evidence:** everything is under `evidence/` (`logs/`, `mutants/`, `tools/`). File names below are relative to it.

## Why GO WITH NOTE

The change does what it says, and every author number I re-measured held:
- 306/0 twice, and again with QUIT and INT ignored at entry.
- 50/0 under bash 3.2 and under dash, and every listed side suite green.
- Both merge-ins check out by recomputation.
- Minor 1 is fixed in its real shape. Two real gates racing on one package now give **5 of 5 both rc 0, nothing nested**. Gate 1532 measured 4 of 5 correct pushes refused.
- Minor 2 is fixed. A grandchild that ignores TERM is ended, and with no perl the install is refused by name.
- The per-ref judging closes the false pass gate 1532 recorded: a red commit with its fix left uncommitted is now refused, and a green commit in a dirty tree now passes.

None of the four Minors lets an unformatted pushed commit through on a configuration that exists today, and none reaches production. They are:
1. **False refusals** of refs that add nothing new to the remote.
2. **A latent false pass:** an `export-ignore` attribute hides files from the tree-mode check.
3. **The Minor 1 move-back window** can still delete a foreign non-empty tree. That needs an install shape that has never been reproduced, and the window is about 38 ms, not microseconds.
4. **Six test gaps** shown by my own mutants.

## Measurements (each with its instrument and a control)

| # | What | Result (mine) | Author's claim | Control that can fail |
|---|---|---|---|---|
| 1 | Gate suite on head, run twice | **306/0, 306/0** (77 s, 75 s) | 306/0 | C1, the gate with `exit 0` at line 2: **125 passed / 181 failed** |
| 2 | Gate suite with QUIT and INT ignored at entry (`trap '' QUIT INT; exec bash suite`) | **306/0** | green | (same harness as #1) |
| 3 | Head suite against develop's gate (red), run twice | **259/47, 259/47** | 206/20 against item 1's gate, on the earlier 226-cell suite | — |
| 4 | Head suite against the gate at `3d14856c3` (before the Minors) | **281/25** | 274/24, on the 19f9d6744 suite | — |
| 5 | Hook suite `ks998_pre_push_judges_the_push`, run twice | **50/0, 50/0** | 50/0 | C3 (the hook exits 0): **24/26** |
| 6 | Hook suite, hook copy under `#!/bin/dash` and under `#!/bin/bash` (3.2.57) | **50/0 and 50/0** | 50/0 under dash | A bashism (`[[ ]]`) injected into `_judge_ref` under dash: **25/25** |
| 7 | Hook suite against develop's hook and gate (red), run twice | **29/21, 29/21** | 21/19, on the earlier 40-cell suite | — |
| 8 | Stale-hint suite: head ×2, develop | **21/0 ×3** | 21/0 | C3: 11/10 |
| 9 | `pre_push_hook_base`: head ×2, develop | **33/0 ×3** | 33/0, pin untouched | C3: 16/17 |
| 10 | `fixture_guard`: head ×2, develop | **6/0 ×3** | 6/0 | C3: 5/1 |
| 11 | `ks884`: head ×2, develop | **10/0 ×3** | 10/0 | C3: 6/4 |
| 12 | `current_develop`: head ×2, develop | **4/0 ×3** | 4/0 | C3: **4/0, so this suite cannot fail on a dead hook** (Info 5) |
| 13 | Leg-comment suites: head ×2, develop | **4/0, 4/0** | 4/0, 4/0 | These are text checks. I ran no control. |
| 14 | Real gate, 4 real packages, tree mode, real registry, empty cache | **rc 0, 13.4 s wall**; installs 1.8 / 1.2 / 1.3 / 1.1 s; 0 stage or tree dirs; prettier executable in all 4; **0 marker files**; lockfiles byte-identical; `git status` 0 lines before and after; sizes 168 / 151 / 137 / 120 MB. Installed re-run: tree mode 6.3 s, working tree 5.1 s | 12 s; 6.1 vs 5.2 s | Before the run: 0 `node_modules`, 0 cache entries. A scratch commit holding a misformatted `auth.setup.ts`, with a green working tree: the real gate **FAILED, rc 1, "(in this push)", "then COMMIT it"** (`logs/T12_*`) |
| 15 | The same with the network denied (`sandbox-exec (deny network*)`), empty cache | REFUSED in 0.5 s, 1.3 s wall, 0 dirs left, no `node_modules` | — | `curl` in the sandbox gives `000`; outside it gives `200` |
| 16 | Merge `c6d103ffc`: `git merge-tree --write-tree 33191c75b a7cffc8d9` | **clean, tree `adfa8b9b2e9e…`, equal to the pushed tree** (not an evil merge) | adfa8b9b2e9e | — |
| 17 | Merge `a5dde56de`: auto-merge of `3d14856c3` + `0026a43e6` | **6 conflicts**, exactly the 6 named paths | 6, all item 1's hunks | — |
| 18 | The `a5dde56de` blob claim | The 7 item-2 paths equal item 2's blobs. `diff(0026a43e6, a5dde56de)` is exactly the 7 paths. Item 1's squash equals PR 1532's head `3dbfdf7e` on those paths (empty diff), so `--ours` dropped nothing of item 1 | as claimed | `b28bfaecf..3dbfdf7e` names item 1's 7 paths, so the diff instrument sees changes |
| 19 | Scope | `diff --stat develop..head`: **exactly 7 paths**, +1166/−91. Against `0026a43e`: 33 paths, the extra 26 being develop's 4 commits (KS-1564, 1582, 1009, 1570) | 7 paths | (same instrument as #18) |

Logs: `logs/SUMMARY_suites.txt`, the per-run logs `logs/G_*`, `logs/H_*` and `logs/O_*`, `logs/merge_tree.txt`, `logs/blob_claim.txt`, `logs/T12*`.

## The new refusal and the per-ref judging: real `git push` to a bare remote (`logs/T2_push_matrix_*`)

I ran each row once against head and once against develop as the control (item 1 merged). Both used the real hook and gate, with a preflight stub that prints a marker.

| Row | Head | Develop (item 1) | Judgement |
|---|---|---|---|
| R1 new branch = HEAD, systemTest green | lands | lands | same |
| R2 existing branch fast-forward, RED, HEAD | refused (gate) | refused | same |
| R3 delete an existing branch | lands, nothing gated, silent | lands, but the gate ran on HEAD's diff | KS-1483 fixed |
| R4 **tag on an already-pushed feature commit** (touches Blockchain/Dev), HEAD=main | **REFUSED, "check out what you push"** | lands | **false refusal (Minor 1)** |
| R4b the same tag with that commit checked out | preflight runs, lands | same | — |
| R5 non-HEAD branch changes Blockchain/Dev | **REFUSED** | **lands, no preflight** | false pass fixed |
| R6 non-HEAD branch, docs only | lands | lands | correct |
| R7 three refs: docs, green, RED | refused, the red ref named, nothing lands | **all three land** | false pass fixed |
| R8 `f8:develop`, dst exists, RED, not HEAD | refused | **lands** | false pass fixed |
| R8b the same after a fix commit | lands, judged at the pushed sha | lands | — |
| R9 detached `HEAD:refs/heads/det`, Blockchain/Dev | preflight, lands | same | correct |
| R10 commit GREEN, working tree RED plus an untracked red file | **lands** | **refused** | false refusal fixed |
| R11 commit RED, working tree GREEN | **refused** | **lands** | false pass fixed (the ticket's own case) |
| R12 `git branch rel origin/develop` (tracking set), push rel | lands, nothing judged | same | — |
| R12b **`origin/develop:refs/heads/rel2`** (a new branch at a trunk commit, nothing new), HEAD elsewhere | **REFUSED**, after printing "Running the preflight UNCONDITIONALLY" | lands | **false refusal and contradictory text (Minor 1)** |
| R13 `<sha>:refs/heads/x13`, RED, not HEAD | refused | lands | false pass fixed |
| R14 `ALLOW_FORCE=1 +f14` rewrite to RED, not HEAD | refused | lands | false pass fixed |
| R15 unborn HEAD (orphan), push a Blockchain/Dev branch | refused, "but HEAD is HEAD" | preflight on an empty HEAD, lands | Defensible. The wording is Info 4 |
| R16 push `develop` (fast-forward onto a feature) while on another branch | refused | preflight ran on the wrong tree, then landed | by design |
| R17 / R17b a file deleted / the whole package removed in the push | land, correctly judged | same | — |

**I found no false pass on head in any row.**

**Is "Check out what you push" correct and actionable?** For branches, yes. For a tag or a remote-tracking ref (R4, R12b), `git checkout <branch>` is not the literal remedy (a detached checkout is), and nothing new lands. That is Minor 1.

## Tree mode (`logs/T3_tree_mode.txt`, `logs/T3b_signals_tree_mode.txt`, `logs/T3c_rm_stage.txt`)

**What worked:**
- An untracked red file in the working tree does not change the verdict.
- A red file that is in the commit but deleted from the working tree is caught.
- Symlinks are caught, both one to an outside red file and a dangling one.
- Odd paths are caught: a space, `[x]*`, and a newline in the name.
- A rename is caught.
- A 20,000-file commit with one red file: FAILED correctly.

**Cleanup** of the tree dir and the check's process group, with a check whose child ignores TERM:

| Signal | Exit code | Tree dirs left | Check processes alive | Sentinels (root, package, outside) |
|---|---|---|---|---|
| INT | 130 | 0 | 0 | all kept |
| TERM | 143 | 0 | 0 | all kept |
| HUP | 129 | 0 | 0 | all kept |
| QUIT | 131 | 0 | 0 | all kept |
| USR1 | 158 | 0 | 0 | all kept |
| ALRM | 142 | 0 | 0 | all kept |
| PIPE | 141 | 0 | 0 | all kept |
| `exit 1` mid-check (mutant) | 1 | 0 | 0 | all kept |
| KILL | 137 | **1** | **2** | all kept |

After SIGKILL, the check's process group survives as an orphan (Info 7), and the next run swept the tree dir.

**`_rm_stage` re-attacked** for both prefixes. The function was extracted verbatim and called with each of these:
- an empty argument and a bare prefix
- `prefix..`, `prefix../pkg`, `prefixx/../pkg`, `prefix1/..`
- a symlink stage, a dangling symlink stage, and a regular file
- a real stage holding links to outside and to the package
- a name with a space and a newline
- a relative look-alike path and the repo root

Every refusal held, and every sentinel and link target was kept. The control works: real stages *are* removed (rc 0, gone). The only hole is still both prefixes empty, which deletes a relative directory. It is unreachable (Info 6, unchanged from gate 1532 Info 3).

**Found:** `export-ignore` silently removes files from the check (Minor 2). A non-ASCII package name is not discovered in tree mode (Minor 2). A submodule's files are not checked in tree mode (Info 3). A not-checked-out pushed commit's own `format:check` script runs (Info 2).

## Minor 1 (the rename and the marker) and Minor 2 (process groups): what I measured

**rename(2) errno on APFS:**

| Target | Result |
|---|---|
| A non-empty directory | ENOTEMPTY (n03b's EEXIST is not produced here, so its survival is justified on Darwin) |
| An empty directory | replaced |
| A symlink | ENOTDIR |
| A file | ENOTDIR |

**Window sizes:** the node process that performs the rename takes **33.6 / 37.8 / 40.6 ms** (min / median / max of 30). The control, `/bin/mv`, takes 3.8 ms median. Both windows (look → rename, and marker check → rename back) are therefore about 38 ms wide, not "microseconds" (`logs/T4_minor1.txt`).

**Two real gates, one package,** with real npm, an offline tarball and a 1.x s postinstall: **5 of 5 trials gave both rc 0** (one INSTALLED, one "appeared during the install"). Nothing was nested, no markers or stages were left, and prettier was executable.

**Cell 35e** pins only that an empty directory is replaced, deterministically, through a node shim. No cell covers the move-back window with a non-empty swap, which is Minor 3.

**Process groups** (`logs/T5_pgroup_n15_n17a.txt`): a stub npm whose *grandchild* records TERM and counts survivors.

| Gate | Path | Grandchild got TERM | Survivors |
|---|---|---|---|
| head | watchdog, graceful | **1** | 0 |
| head | SIGTERM, graceful | **1** | 0 |
| head | TERM-ignoring (deaf) child | 0 | **0** (the group KILL ends it) |
| n15 | watchdog, graceful | **0** | 0 |
| n17a | SIGTERM, graceful | **0** | 0 |

So **n15 and n17a are observable**, because the grandchild loses its TERM, but **no ordering I could build leaves a survivor**. "Redundant for survival, not unobservable": that cell distinguishes them (Info 1).

**Without perl** (`logs/T5b_perl_absent_and_spoof.txt`). The instrument was a PATH of symlinks to all of `/usr/bin`, `/bin`, `/usr/sbin` and `/sbin` except `perl*`, plus node and npm. The control is the same PATH with perl added.

| PATH | Normal mode | `--all` | Stage dirs | `node_modules` |
|---|---|---|---|---|
| with perl (control) | INSTALLED, rc 0 | — | 0 | yes |
| without perl | **rc 1, npm never started, the REFUSED line names perl and the process group** | named SKIP, then NOTHING CHECKED, rc 1 | 0 | no |

**Spoofing:** a `perl` earlier on PATH is executed. So is an `npm`, `node` or `git` placed there. This is not a new surface, because the developer controls PATH either way.

**`kill -- -pid` after the leader is reaped:** I did not measure it. The window is microseconds. xnu, like POSIX, does not reuse a pid while a process group with that ID exists, so a group with a live member cannot be recycled. A recycled *empty* group needs pid wrap-around inside that window. I consider it theoretical, as the author does.

## Security of the install surface (brief item 7)

The install still copies only the **working tree's** `package.json`, lock and `.npmrc` into the stage, so a pushed commit's lock cannot change what `npm ci` fetches or runs. The new exposure is in the check:
- In tree mode the gate runs the **pushed commit's** `npm run format:check` script and its JS prettier config.
- For a push of a commit that is not checked out, that is code the developer never had in the working tree. It runs with their environment and credentials.
- Measured with a sentinel (`logs/T3_tree_mode.txt`, T3k): the pushed commit's script ran, and the working-tree control did not.

That is Info 2, not Minor: the pusher is publishing that commit, and before item 2 the same commit would have run the moment it was checked out.

**Minor 3 (not in this PR)** neither worsens nor fixes this. Its lock allowlist reads the working-tree lock the install already uses. Its env scrub, as planned, covers the install and not the tree-mode check. Nothing here makes Minor 3 harder: the scrub goes inside `_run_grouped`'s `exec`.

## Findings

### Minor 1: false refusals of refs that add nothing new to the remote, with contradictory text on the KS-882 path

**Where:** `.githooks/pre-push:257-270` (the tag-only skip, then the KS-882 "UNCONDITIONALLY" branch) and `:340-347` (the not-HEAD refusal).

**Shape:**
- **R4:** `git tag t4 <already-pushed feature commit>; git checkout main; git push origin t4` is REFUSED "changes Blockchain/Dev".
- **R12b:** `git push origin origin/develop:refs/heads/rel2` from another branch first prints "Running the preflight UNCONDITIONALLY", then REFUSES.

Item 1 landed both. Neither lands any commit the remote lacks. This is fail-closed, the bypass works, and item 1 also refused tags, for a different reason (KS-1483 is only partly cured for tags). My mutant **X02 (the refusal skipped for every tag) survives all three hook suites**: no cell pushes a tag on a not-HEAD Blockchain/Dev commit.

**Minimal fix:** before the not-HEAD refusal, skip with a note when the tip is already on the push remote: `git for-each-ref --contains "$_tip" "refs/remotes/<remote>/"` is non-empty. Treat a branch whose every base contains the tip like `tagnobase`, and stop printing the KS-882 "UNCONDITIONALLY" banner on a path that then refuses. Add a cell for a tag on a not-HEAD commit (this kills X02).

### Minor 2: tree mode honours `export-ignore` (and misses non-ASCII package names), a silent false pass

**Where:** `systemTest/scripts/check-package-format.sh:439` (`git archive`) and `:488-498` (discovery through `ls-tree` without `-z`).

**Shape** (T3a, T3b; control in the same fixture):
- A pushed `systemTest/pkgB/.gitattributes` with `src/red.ts export-ignore` gives **format:check OK, rc 0**. Working-tree mode on the same commit: FAILED.
- A developer-local `.git/info/attributes` with `*.ts export-ignore` (or `core.attributesFile`) also gives **OK**. Control without attributes: FAILED.
- `systemTest/pké/` with a red file (T3i): tree mode discovers nothing, prints nothing, rc 0. Working-tree mode: FAILED. The cause is `core.quotePath` quoting the name in `ls-tree` output.

No `.gitattributes` exists under `systemTest/` today, and all package names are ASCII. That is why this is Minor and not Major.

**Minimal fix:** materialise the tree without archive attributes: `GIT_INDEX_FILE="$tree/.idx" git read-tree "$TREE_SHA"`, then `git checkout-index --prefix="$tree/" -- systemTest/$p …`. Alternatively, refuse when `git check-attr export-ignore` is set on any path of the package. Discover with `git ls-tree -z --name-only`.

### Minor 3: the Minor 1 move-back window can still delete a foreign NON-EMPTY tree, and it is about 38 ms, not microseconds

**Where:** `check-package-format.sh:387-396`. The marker check at `:387` and the rename back at `:395` are separate steps. The header at `:136` says "the gate never moves or deletes a tree it did not move".

**Shape** (`logs/T4_minor1.txt` M1c): an install whose prettier is an absolute symlink into the stage takes the mvbroken path. A node shim replaces the package's `node_modules` with a foreign tree holding `FOREIGN_DEVELOPER_TREE` just before the back rename. That tree is moved into the stage and **deleted** (`foreign_tree_survives=NO`). Control SWAP=0: the same refusal, nothing foreign involved.

Reaching it needs an install that embeds its stage path (0 of the 4 real lockfiles do) plus a concurrent replacement inside the node spawn time (median 37.8 ms). It is narrow, but it falsifies an absolute claim, and the PR's text calls the window "microseconds" and "that millisecond".

**Minimal fix:** after the rename back, check for the marker *inside the stage* (`$stage/node_modules/$tag`). If it is absent, do not `_rm_stage` that tree: leave it, report it, and refuse. Correct the window wording.

### Minor 4: six of my mutants survive, and they are test gaps (full table below)

| Mutant | What it shows | Real effect if shipped |
|---|---|---|
| **X02** (refusal skipped for tags) | See Minor 1 | — |
| **X04** (`_head_c` taken from `@{upstream}`) | Every fixture branch is `--no-track`, so no cell pushes HEAD from a branch with an upstream | Every normal HEAD push with a Blockchain/Dev change would be refused |
| **X09** (INT trap exits 0) | No cell asserts the gate's exit code on INT | — |
| **X10** (HUP trap exits 0) | No cell asserts the gate's exit code on HUP | — |
| **X14** (ancestor config read from HEAD, not from the pushed commit) | Every gate-suite tree cell uses `FORMAT_GATE_TREE` = HEAD | — |
| **X15** (the `notintree` remedy prints `npm ci` instead of "check out what you push") | The refusal's remedy line is unpinned | — |

X09 and X10 matter less in practice, because a terminal INT or HUP also stops git.

Relatedly, **X06** (archive HEAD instead of the pushed commit) is killed only by the hook suite. The gate suite alone is 306/0 against it.

**Fix:** one cell each:
- an upstream-tracking HEAD push
- INT/HUP rc (with dispositions reset as in CASE 39)
- a tree cell whose `FORMAT_GATE_TREE` is not HEAD
- the `notintree` remedy text

### Info

1. **n15 and n17a:** no survivor in any ordering I built, but they are observable. The graceful TERM to a grandchild is lost (head 1, mutants 0). The distinguishing cell is the `graceful` row of `tools/pgroup.sh`.
2. **Tree mode executes the pushed commit's `format:check` script and JS prettier config** (T3k). This matters for not-checked-out pushes. It is a stated consequence of judging the commit; see "Security" above.
3. **Submodules:** a submodule under a package is not checked in tree mode (T3h; working-tree mode FAILED on the same red file). None exists today.
4. **Documentation and wording:**
   - `systemTest/CLAUDE.md` says "304 cells"; the suite has 306.
   - It says deleted refs "are named"; the hook skips them silently (correctly).
   - It says "that millisecond"; measured about 38 ms.
   - The refusal reads "but HEAD is HEAD" on an unborn HEAD (R15).
   - The no-perl refusal's remedy, `npm ci`, does not mention perl.
5. **Pre-existing:** `pre_push_hook_current_develop` passes 4/0 against a hook that exits 0 at the top, so it has no positive control. Not this PR's.
6. **Unchanged from gate 1532 Info 3:** `_rm_stage` with both prefixes empty deletes a relative directory. Unreachable. Defence in depth: `[ -n "$STAGE_PREFIX" ]` plus an absolute `$d`.
7. **SIGKILL:** after SIGKILL to the gate, the check's (or npm's) process group lives on, orphaned, because it is no longer in the terminal's group. Expected; the next run sweeps the dir.
8. **Not verified:** I could not read the PR body or the Linear attachment. The repository is private (unauthenticated API: 404), and neither this seat's nor the project's `gh` config is logged in. I checked "no closing keyword" in the 12 commit messages (0 hits) and read K's READY mail, which claims "contributes" and 0 close-family words.
   - The hunk grouping matches the commits:
     - item 2: `24e60acf3`, `3d14856c3`
     - the Minors: `8330c4602`, which also groups item 2's tree-mode check
   - KS-1483 is folded in: deletions now land ungated (R3), and a tag on a trunk commit lands as a note (SC9a). Tags off the trunk are only partly cured (Minor 1).
9. **`tagnobase` also fires when no base resolves at all** (KS-854's condition). A tag carrying a new red commit in a clone with no develop ref is then not gated, while a branch in the same clone runs unconditionally. Edge case.

## Mutants

**Author's runner on the exact head** (`tools/tamper_gate2.py`, 2 shards, each preceded by an unmutated control, 306/0 both times): **90 mutants, 83 KILLED-BY-NAME, 7 SURVIVED-BY-DESIGN, 0 unexplained.**
- **The survivors:** m13a, m23, m25, m35, n03b, n15 and n17a, the same 7 the author names.
- **m23b:** now killed by name, by the CASE 38 USR1/ALRM/PIPE cells. Minor 4 of gate 1532 is closed.
- **Logs:** `mutants/gate_shard{A,B}.log`, `*_results.json`, and the per-mutant `.out` files in `mutants/author_runner_outputs/`.

**Author's hook runner** (`tools/tamper_hook2.py`): control green [(50,0), (21,0), (33,0)], then **19 of 19 KILLED-BY-NAME** (`mutants/hook.log`).

**Mine** (`tools/my_mutants.py`). Gate mutants ran the gate suite plus the hook suite; hook mutants ran the three hook suites (`mutants/mine.log`):

| Mutant | Result, with the first failing cell |
|---|---|
| X00 gate, comment only (CONTROL) | **reddens nothing** (306/0, 50/0) |
| X00 hook, comment only (CONTROL) | **reddens nothing** (50/0, 21/0, 33/0) |
| X01 not-HEAD refusal inverted | KILLED 17: "SC3 a pushed sha that is not HEAD and changes Blockchain/Dev is REFUSED" |
| X02 refusal skipped for tags | **SURVIVED** (Minor 1 / 4) |
| X03 stale flag never passed to the gate | KILLED 2: "...and the hint: your origin/develop may be stale" |
| X04 `_head_c` from `@{upstream}` | **SURVIVED** (Minor 4) |
| X05 archive error falls back to the working tree | KILLED 3: "git archive failing -> the gate FAILS (exit 1), it does not pass" |
| X06 archive HEAD, not the pushed commit | KILLED 7, **hook suite only**: "SC2 pushing a branch that is NOT checked out…" |
| X07 discovery from HEAD's tree | KILLED 5: "a package that exists at the pushed commit but not in the checked-out tree -> exit 1" |
| X08 QUIT trap exits 0 | KILLED 1: "SIGQUIT to the gate mid-install -> exit 131" |
| X09 INT trap exits 0 | **SURVIVED** (Minor 4) |
| X10 HUP trap exits 0 | **SURVIVED** (Minor 4) |
| X11 no perl: silent fallback to pid-only | KILLED 4: "no perl, normal mode -> exit 1, REFUSED naming perl and the process group" |
| X12 marker check reads the wrong name | KILLED 4: "...REFUSED, saying the install embeds its staging path" |
| X13 tree-mode check rc ignored | KILLED 19: "red at the pushed commit, fix uncommitted -> exit 1" |
| X14 ancestor config from HEAD | **SURVIVED** (Minor 4) |
| X15 `notintree` remedy is `npm ci` | **SURVIVED** (Minor 4) |
| X16 move back ignores the rename failure | KILLED 1: "...the refusal says it could not be moved back (not that it was)" |
| n15, n17a (the author's) | survive the suite, but are distinguished by `tools/pgroup.sh` (Info 1) |

## NOT tested, and why

- **Linux / GNU userland / dash as `/bin/sh`:** no Docker (`docker info` failed) and no remote box allowed. I ran the hook under `/bin/dash` on macOS only. GNU `mv` is no longer on the rename path. The perl dependency on a bare Alpine image is reasoned, not run. A Linux errno difference would at most change which raced branch is taken. Both are fail-closed, so I see no hidden Major.
- **Preflight legs 3, 4 and 8, and a full real push through the preflight:** not run. The author's 9 min 9 s push is not re-measured. The preflight is unchanged by this PR except for being reached through the union of `changed`, which R5, R9 and R16 exercise with a stub.
- **A hook invoked by anything other than git** (husky, lefthook, a GUI client): not run. A client that feeds no stdin judges nothing (h18 shows every gate cell then fails), and its exit code is still honoured by git.
- **A real multi-developer fleet push:** not run.
- **pgid recycling:** reasoned, not measured (see the Minor 2 section).
- **A pty Ctrl-C:** emulated by signalling the gate alone with INT reset to default. With npm in its own group, a real terminal Ctrl-C reaches only the gate and git, and the gate's trap ends the group. I did not drive a pty.
- **The PR body and the Linear attachment:** not readable from this seat (Info 8).

None of these could hide a Major on the evidence above. The refusal paths are fail-closed, and the one false-pass class I found (Minor 2) needs a configuration that does not exist in the repository today.

## Recommendation to Wednesday

**GO WITH NOTE** on `c6d103ffc469`. This is developer tooling: merge on Wednesday's head-bound GO, and do not deploy anything.

Minor 2 (materialise the tree without archive attributes, and use `ls-tree -z`) and Minor 1 (do not refuse refs already on the remote, and fix the KS-882 text) are cheap and belong in the stacked Minor 3 PR or a fast follow. Minor 3 is a five-line guard. Minor 4 is one cell each.
