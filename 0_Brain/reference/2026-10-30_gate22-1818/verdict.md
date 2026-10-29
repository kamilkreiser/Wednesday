## QA GATE - TIER 2, round 1: GO WITH NOTES

Counts: blocker 0 / major 0 / minor 1 / info 3

PR Secuura/Distributed_Secuura #1818, vite 6.4.4 -> 6.4.5 lock-only. Through-code only. Findings only; nothing fixed, commented or pushed.

### Findings

**F1 (minor) - claim (d) "byte-identical dist" is supported only by a summary, not by hash lists.**
- `evidence/itemB/dist_compare.txt` is 2 lines (194 bytes): "demo-overlay names identical: yes; bytes before 417847 after 417847; byte-identical files: 1" and "outlook-addin ... 443076 / 443076; byte-identical files: 14".
- No per-file hash list, before or after, exists in itemB (grep for sha256/shasum/md5 finds nothing relevant).
- `builds_summary.txt` is consistent with it: all four builds rc 0, and the container vite is 6.4.4 before and 6.4.5 after (so the bump really was exercised). File counts are 1 and 14 both sides.
- This is the author's measurement and I did not rebuild, as instructed. The counts, sizes and an author-reported file-by-file comparison support the claim. The hash lists that would let a reader re-verify it are absent.

**F2 (info) - claim (a): CONFIRMED.**
- Exactly 3 files change: `Blockchain/Dev/package-lock.json` (6/6), `frontend/demo-overlay/package-lock.json` (3/3), `frontend/outlook-addin/package-lock.json` (3/3). That is +12/-12 and no package.json.
- Every changed line is a `version`, `resolved` or `integrity` line of a vite entry (4 of each, with 4 matching removed lines).

**F3 (info) - claim (b): CONFIRMED.**
- Four rows move, each 6.4.4 -> 6.4.5: root lock `frontend/demo-overlay/node_modules/vite` and `frontend/outlook-addin/node_modules/vite`, plus `node_modules/vite` in each frontend lock.
- Row counts are unchanged: 1943/1943, 181/181, 210/210.
- Non-`packages` top-level content is identical in all three.
- The author's before/after TSV files diff to exactly those four rows.

**F4 (info) - claim (c): CONFIRMED, with notes.**
- At head: `audit:gate` rc 0 ("OK - no advisories outside the triaged baseline") and `audit:locks` rc 0.
- At parent 7152ac669 (control): `audit:gate` rc 1, "1 NEW advisory ... GHSA-8g5g-mxqh-grgj [moderate] vite"; `audit:locks` rc 1, GHSA-8g5g-mxqh-grgj pinned 6.4.4 in demo-overlay and outlook-addin.
- Both audits query the live advisory database, so they need network. Their result can change with advisory data over time.
- Both gate runs print an advisory-only CLEANUP note that baseline entry GHSA-vfj7-8cjw-p6xm (braces, KS-1403) is no longer reported. It is pre-existing and also shows at parent, so it is not caused by this PR. A tidy-up ticket would remove it.

**Hook verdict:** "PREFLIGHT INCOMPLETE - 13/16 legs ran, 3 SKIPPED. Nothing failed." is present verbatim at `evidence/itemB/push_real/push.out` line 2780. The only skipped item I could attribute is the shell suite `ks949_main_seed_idempotence.test.sh` (no PostgreSQL on the box; the runner notes the skip is ruled non-failing). I did not identify the other skipped legs and did not investigate. For a lock-only change this is low risk.

### Checks

1. **Refs.** `ls-remote` on develop and `refs/pull/1818/head` in one call returned develop 84ddbd63c00864eba1dc955cc86199fb0c2d17d0 and pull/1818/head 00211c7cabde8f38a828d669ec415fb7fe962342. Fetched into my clone, the head's parent is exactly 7152ac669d2d6af08be5b9dcd35132818377155d (one parent). All match the brief.
2. **Diff and registry.** Hunks touch only the vite version, resolved and integrity lines. For all 4 changed entries, `integrity` equals `npm view vite@6.4.5 dist.integrity` (sha512-4enwjFfi4IwtEh0w+jPzpLVOFQiPHmmzPxcHXQOyEur47o6u0jE573DmGpjA+7irXoMLYRZD5ZaFUEneS3abPg==). `resolved` equals `https://registry.npmjs.org/vite/-/vite-6.4.5.tgz`.
3. **No other package changed.** Parsed `packages` maps, parent vs head, keyed by path: only the vite paths above differ. Entries are compared whole (all fields), not just version.
4. **Audits.** As in F4. `npm ci --ignore-scripts` succeeded at both head and parent (1806 packages each, rc 0).
5. **Merge prediction.** `git merge-tree --write-tree 00211c7c 84ddbd63` returned rc 0 and tree **f31f11a258715a01977ed28f43c2de7b162ce86b**, with no conflict listed. Merge base is 7152ac669. The only paths in which that tree differs from develop are the three lock files (3 files, +12/-12). Develop's #1814 touches no lock file, so there is no overlap.
6. **(d) evidence.** As in F1. The author's measurement, not re-run.

### TESTED / NOT TESTED / HOW

TESTED, with controls:
- Head, parent and develop refs: ls-remote and fetched PR ref agree. Control: the head's parent hash in my clone equals the brief's hash.
- Lock diff scope: numstat, then a normalised hunk-line count.
- Integrity vs registry. Planted control: the last character of the integrity string was altered and reported as a mismatch against the registry value. Weakness: this control tests my comparison logic, not an independent source. The genuine 4 comparisons all reported equal, so the instrument can say both outcomes.
- No other lock change. Planted control: a fake 7.29.7 -> 9.9.9 change on `node_modules/@babel/code-frame` in a scratch copy was detected by the same comparator.
- Audits at head (expect rc 0) and at parent (control, rc 1 naming the GHSA). The control can fail and did fire, which shows the audit actually sees the advisory.
- Merge prediction. Control: a scratch commit on the parent that edits the same demo-overlay lock `resolved` line differently gave rc 1 and a conflict on that lock file, so merge-tree does report lock conflicts. The real merge gave rc 0.

NOT TESTED:
- Frontend builds and dist bytes (not rebuilt, per instruction; author's counts only).
- The author's 16-leg preflight (read as a record only; the 3 skipped legs are unidentified).
- Runtime behaviour of vite 6.4.5 (no dev server or tests run).
- Whether npm's advisory data keeps flagging 6.4.4 and clearing 6.4.5 in future.
- GitHub CI status on the PR.

HOW: a `git clone --shared` of the Blockchain checkout into the scratch dir `.../scratchpad/gate22/clone` (`rev-parse --show-toplevel` equals that path). Its origin was set to `git@github.com:Secuura/Distributed_Secuura.git` with the shared checkout's `core.sshCommand`. I fetched only there. Detached worktrees `wt_head`, `wt_par` and `wt_ctl` sit in the scratch dir. Comparator script: `.../gate22/cmp.js`; its outputs are in `cmp_out.txt`, `audit_*_{head,par}.txt` and `ci_*.txt` in the same directory. I started no long-running processes.

### Instrument errors of my own

- My first fetch call was refused by a hook because the command used a `$C` variable path. I reissued it with literal paths in my scratch clone, with no effect on the result.
- The scratch-dir creation and the first lock-extraction attempt hit hook refusals for `cd` and zsh word-splitting. Both were fixed by rewriting the commands, and no check results were affected.
- The wrong-integrity control exercises my own comparison (see above), not an external oracle.
