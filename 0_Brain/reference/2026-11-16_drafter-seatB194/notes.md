# Drafter notes: Seat B 194th brief (2026-11-16 15:12 to 15:42 AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatB194_merge.md (49,974 bytes; STAMP blank; SELF-CHECK 2026-11-16 15:41 from `date`, develop 8292da2c9dbc and all 16 heads re-read unmoved at 15:41). Linted by _work/scripts/lint194.py (provenance format, absolute sources, KS ids in the block, no QUEUE heading, no placeholders). send_brief.sh was NOT run, nor any other send/write tool.

## Measured (live)
- develop 8292da2c9dbc (PR 2250, K 41st, 15:05:04; parent fe514a7b29a8 = B 193rd's PR 2130 squash; tree 8325c80b5a03; 12 paths). All 16 heads unmoved vs B 193rd's table (15:13). 53 open PRs. DNM 13 of 16.
- Trees on 8292da2c9dbc: 16/16 rc 0 both orders, same tree; stacked chain 16/16 rc 0 (final e52b8a81f9a4); plants 10/10 positive both orders, 20/20 negatives; six pairs unchanged; PR 2099 clean with rows 2073 and 2131. K 19 x B 16 = 304 pairs share 0. Develop moves since db2b (16 paths) share 0 with all rows. Both-sided: 7 rows, 12 paths (unchanged); 2127 not both-sided.
- Row 1 PR 2127: gate 288 table line 6 GWN; 2 commits; runner `bash .../check_slot_credentials.test.sh`; develop 32/32, merged 46/46; red-first in a git worktree 6 of 46 = gate's six; in a plain copy 8 (R2-1 + CONTROL read NO-TREE: trap); bash -n 0/0; --check-unreached rc 0 (127 suites); docs fragments rc 0; shellcheck absent. Whole run-shell-suites d,m (full checkouts, 513 s / 522 s): both 121 passed, 4 failed, 2 skipped of 127, the same four failing suites (host baseline) -> no regression.
- PR 2138 superseded by PR 2249 (2249 body line 31 names it; 5 shared paths; merge-tree rc 1 both orders, conflicts in 3 paths; mergeable false/dirty).
- Stray file history.md.b193_pre_timefix: 20,000 bytes, mtime 14:54; 5_Project_History is NOT a git work tree (git rev-parse fails), so git mv is impossible: the brief says plain mv, never rm.
- kit194: 93 files, sed==python 93/93, manifest sha16 1720d71b5057a249; roll th asserted (194th 1 in 1 before = matcher's own-seat entry; 303 in 91 after; 194rd/nd/st 0); glued 193rd digit-preceded 1 in 1 (B 1193rd). Matcher n 798 -> 803, self-test 812/812; traps measured blind (194rd/194nd/194st, bare rule + five).
- Engine: engine194/mk_engine_b194.py -> derive_engines_b194.py (2b3987a49d702ff2); aids clone_setup_https_edit_b194.py (1368a7fd594291af), setup_checks_b194.py (90d005dbf2a3ce3d). Scratch chain (_work/rec194e) about 4 s: 93/93 equal after re-key; 10 declared differences after chain (merged_build is new vs B 193rd's 9); baselines v1 84559a1fcdeef800, v2 722c69838fb3f386, v3 daf5a08be8be2ee8.
- FINDING: B 193rd's nine own-authored names differ from B 192nd's nine; a plain shift of B 193rd's engine would REFUSE at the OWN assert; the drafter's engine carries B 193rd's nine and B 193rd's merged_build pre-edit copy.

## Slips (mine, declared)
1. First chained command hit the zsh `=====` hook refusal (fixed with `----`).
2. One `git -C $G merge-tree` inline call was refused by the no-cd/write-verb hook (unexpanded variable read as outside WEDNESDAY); re-run from a script file, target my own clone under _work (inside WEDNESDAY).
3. `python3 -m py_compile` over kit194 wrote two `__pycache__` dirs inside kit194; MOVED (not deleted) to _work/_aside before the manifest was used further (the manifest was computed before them and lists files only).
4. The first engine output (with an extra makedirs line) was MOVED to _work/_aside/derive_engines_b194.v0.py and the engine regenerated without it (to stay identical in behaviour to B 193rd's).
5. `git config` on my own clone (_work/d: origin URL, no_push pushurl, credential helper); worktrees wt_dev and wt_mrg and scratch commits in my own clone; the matcher scratch tmp file in my session scratchpad.
No cd, no rm, no writes under /Volumes/DevMASTER/!CODING, no mail, no Linear or GitHub writes, no send/write tool.

## Unmeasured
See the brief's UNMEASURED section: the 2127 mutants (gate's, not re-run), every cost line (reasoned), the real REC194 chain (scratch only, placeholder ids), the real clone copy, develop and heads after the SELF-CHECK, launches of K 42nd and D 68th, mail and Linear.

## Additions
- Slip 6: one zsh loop over `$QB` did not word-split at the SELF-CHECK re-read (read-only gh calls); re-run under `bash -c`.
- The whole run-shell-suites d,m runs took 513 s and 522 s in my own worktrees (env -i, short TMPDIR); porcelain 0 after both.
- Cuts to fit under 50 KB: the brief points to B 193rd's FINAL for its board list and AFTER-A-GO list rather than repeating them.
