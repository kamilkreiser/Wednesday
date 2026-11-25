IN PROGRESS

# Independent check: CoAgent `policy-notes` (owner ALLOW origin: items 2, 3, 4, 6, 7; item 1 built and reverted)

Checker: QA-POLICY-NOTES, the one independent check. Work dir `/private/tmp/claude-501/qpn` (own clone of the project repository with the GitHub remote added as `gh`, own worktrees and empty target dirs per tree, cargo home with the toolchain LINKED as `coagent_merge_check.sh` does). The project folder was only read (git read verbs with `--no-optional-locks`), except my status file. Copies of every script and harness: `m1_review/gate_policy_notes_tests/`. Tags: TESTED (I ran it), READ.

## 0. Head, base, history (TESTED)
- `git ls-remote gh policy-notes main` (own clone, deploy key, 2026-11-25 12:03): `policy-notes` = `b6af26c592ab2be1a5809e57bd602ad709c8ea11`, `main` = `1b1ac447041ea3df56384cd4547561ec076a3130`, as briefed; the project repo's `origin/policy-notes` and `origin/main` (`rev-parse`) are the same two SHAs.
- `git cat-file -t f193620…` commit; `merge-base --is-ancestor f193620 b6af26c` exit 0; `merge-base f193620 b6af26c` = `f193620c14082df985cff3bb1b96d02575218811`. Main `1b1ac44` descends from `f193620`; not merged into the branch (by rule, not a fault). Every comparison below is against `f193620`.
- `git log f193620..b6af26c` (with parents), oldest first: `6f560cb` (item 6) ← `f193620`; `8c2ebd0` (items 2-4 + FR-2) ; `d9ef9a6` (item 1); `da33437` (item 7); `535b017` (item 5, docs 2-4); `db58c18` (item 5, §11/BACKLOG/M0); `b6af26c` `Revert "policy-notes item 1 (m-1): in the owner origin a terminal command runs unasked only while nothing is excluded"`, ONE parent `db58c18`. Seven commits, linear, as briefed.
- `git diff --stat f193620 b6af26c`: 12 files, +885 −104. `git show --stat b6af26c`: 8 files, +46 −184. Both as briefed.
- Builder's STATUS: 376 lines, ends `Head: b6af26c…` / `READY FOR QA POLICY-NOTES`. As briefed.
- History not rewritten (what could be established): `d9ef9a6` and `b6af26c` are both on the branch; `b6af26c`'s only parent is `db58c18`. The project repo's reflog of `refs/remotes/origin/policy-notes` (read only) shows exactly two updates, both "update by push": `db58c18` (2026-11-25 05:15:51 +1100) then `b6af26c` (09:46:23), a fast-forward (`db58c18` is `b6af26c`'s parent). The builder worktree's reflog of `policy-notes` (read only) is linear: created from `origin/main` (f193620), then the seven commits, no reset/rebase/amend entry. NOT establishable: GitHub's own server-side push log (a push from another clone would not appear in these reflogs).
