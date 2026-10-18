GO WITH NOTE — PR #1577 (KS-1482) head 83b955a6f8db11ed80af4550b7da2bc4d0203a2a
Fix is correct and fails closed: all 3 sites killed by named cells, no other changed-set read decides a refusal, merge tree 8cda8b91829d confirmed, full runner 91/0; notes are coverage/latent only.
802f84f276c9e9aa

Gate G1, tier 1 FULL, Opus. Round 1 of 2. Live develop re-read at 01:02 and again at close: 8a9970511f22661d92f634058fae8c08c656124f (unchanged). PR head 83b955a6f (ls-remote refs/pull/1577/head), #1578 head 972286126bc6. Clone: --shared from the project checkout into /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/g1/repo, push URL disabled. `npm ci` rc 0 and `npm run build -w packages/shared` rc 0 before any suite.

## FOUND

No defect at BLOCKER, MAJOR or MINOR.

- **N1 (INFO, coverage gap, behaviour verified fail-closed).** Under --no-renames, a rename OUT of a systemTest package now lists the old path, so the KS-989 format gate **selects that package** (`.githooks/pre-push:129/143/252` feeding `systemTest/scripts/check-package-format.sh` selection). In the fixture that means a NEW refusal: `git mv systemTest/pkgA/src/a.ts docs/a.ts` passes on develop (0/0/0/landed) and is REFUSED at the head (pkgA deps absent), on all three base paths. That matches the precedent: develop already refuses a pure delete of the same file the same way (measured, both hooks rc 1, "REFUSED — systemTest/pkgA"). So this is consistent, and it fails closed. But it is a user-visible change that is not named in the PR and has no cell.
- **N2 (INFO, coverage gap).** A rename out of Blockchain/Dev on a ref that is **not HEAD** used to land ungated on develop (0/0/0/1). At the head it is now REFUSED with "check out what you push" (`.githooks/pre-push:351-358`), on all three base paths. This is the correct fail-closed outcome. No cell in the suite pins it.
- **N3 (INFO, latent, decides no refusal).** `Blockchain/Dev/scripts/check-no-demo-mutation.sh:73` `git diff --name-only "$BASE...$HEAD"` is rename-blind in the same way: a demo file renamed away shows only by its new path. It is **not wired** into the push. It is listed only in the not-wired reasons at `Blockchain/Dev/scripts/run-code-guards.sh:116`, and nothing in the hook, preflight or run-code-guards calls it. If it is ever wired, it needs `--no-renames`. (Side note: the reason text at run-code-guards.sh:116 says it defaults to origin/main, but the script now defaults to `origin/develop` at :62. That text is stale and out of scope here.)
- **Census (step 2), complete.** Changed-set reads reachable from the hook:
  - `.githooks/pre-push`: three, at :129, :143 and :252. All three now carry `--no-renames`. The two other `git diff` mentions (:87, :183) are comments.
  - `check-package-format.sh`: no diff, log or diff-tree. It reads `git ls-tree` (:614, :692), `ls-files`/`checkout-index` (:622) and `git show <sha>:package.json` (:685). These are tree and content reads, not changed-set reads.
  - `systemTest/slot-target.sh`: no git diff, log or show.
  - `preflight.sh` and every leg it calls (`preflight/*`, run-shell-suites, run-code-guards and its 13 wired guards, check-shared-relink, audit/*): no git diff, log, diff-tree, `--name-status`, `-C`/`--find-copies` or `--follow`. The wired legs read whole-tree state (`ls-files`, `rev-parse`).
  - `stack_guard.sh:142` `git diff --quiet HEAD` is a dirty-tree probe. Renames do not matter to it, and it is not on the push path.
  - Copies: git's default diff does not detect copies. Even with `diff.renames=copies` set in the repo config, a copy lists only its new path, and the source is unchanged by definition. `--no-renames` also overrides that config, which I measured (row out_copiescfg below).

## TESTED / HOW

1. **Diff by hunk (step 1).** `git diff 8a99705...83b955a6`: 2 files, +35/-3. In `.githooks/pre-push` there are three one-token hunks (+`--no-renames`) at :129, :143 and :252. The rest is the suite: SC22a (new branch, after SC17) and SC22b/SC22c (exists-at-remote, upstream). Each RED cell is paired with a CONTROL. Nothing changed outside the two named files. The head is a merge of develop 8a99705 into a3ceb3fc5.
2. **Red-first, green, mutants, control (step 4).** I ran the head's ks998 suite with HOOK_SH pointed at each variant:
   - develop's hook: **77/3**. The three FAILs are exactly the three RED KS-1482 cells, so the author's red claim is reproduced.
   - head: **80/0**.
   - mut129 (line 129 `--no-renames` removed): 79/1, killed by "RED KS-1482 … pushed to a branch that EXISTS at the remote".
   - mut143: 79/1, killed by "RED KS-1482 … pushed from a branch with an UPSTREAM".
   - mut252: 79/1, killed by "RED KS-1482 … pushed as a NEW branch".
   - comment-only control (one comment line inserted at :130): 80/0.
   - Each mutant differs from the head by exactly 1 line, and each is killed by a different named cell.
3. **Shapes, both ways (step 3).** I used the suite's own `build_fixture` (lines 30-94 of the head suite, sourced) and measured each shape on all three base paths: new branch, exists at remote, upstream. Result columns are rc / preflight ran / REFUSED / landed.

   | shape | develop hook | head hook |
   |---|---|---|
   | rename OUT of B/Dev (100% similar) | 0/0/0/1 **ungated** | 0/1/0/1 preflight runs |
   | rename OUT with `diff.renames=copies` in repo config | 0/0/0/1 ungated | 0/1/0/1 |
   | rename OUT + edit (below the 50% threshold) | 0/1/0/1 | 0/1/0/1 |
   | rename INTO B/Dev | 0/1/0/1 | 0/1/0/1 |
   | rename WITHIN B/Dev | 0/1/0/1 | 0/1/0/1 |
   | copy B/Dev → docs (copies config) | 0/0/0/1 | 0/0/0/1 (correct: B/Dev unchanged) |
   | copy docs → B/Dev (copies config) | 0/1/0/1 | 0/1/0/1 |
   | pure delete in B/Dev | 0/1/0/1 | 0/1/0/1 |
   | rename out of systemTest/pkgA | 0/0/0/1 | 1/0/1/0 (N1) |
   | rename out of B/Dev, ref not HEAD | 0/0/0/1 | 1/0/1/0 (N2) |

   No row in 66 has develop refusing and the head passing. No previously-refused push now passes. The change only adds lines to `all_changed`, so it can only add preflight runs, format-gate selections and not-HEAD refusals. **The author's "fails closed" claim holds.**
4. **Full runner and flakiness (step 5).** On the merge-predicted tree 8cda8b91829d (develop + #1577 + #1578, clean status):
   - `run-shell-suites.sh`: **91 passed, 0 failed, 0 skipped (of 91)**, rc 0, 583 s. The author reported 90/0 on the head alone; #1578 adds one suite.
   - ks998 suite on the same tree, twice: 80/0 and 80/0.
5. **Merge prediction (step 6).**
   - #1577 onto live develop: merge-tree rc 0, tree 6d9f9cb691dc, identical to the head's own tree. It is a fast-forward in content.
   - #1577 then #1578: tree **8cda8b91829d**44b22cdcf28b653c106be6378c87.
   - #1578 then #1577: the same tree. This matches R's prediction.
   - Overlap: #1578 touches `Blockchain/Dev/scripts/prisma-generate.cjs` and its new test. The file-overlap set is empty.
   - Planted conflicting control: develop plus an edit to the same hook line 129, merged with #1577, gave rc 1 with `.githooks/pre-push` conflicted. That shows the probe can detect a conflict.

## NOT tested

- The real 13-leg preflight on a rename-out push. Every fixture uses the suite's stub preflight, which prints a marker. The gate proves the hook now *invokes* the preflight, not what the preflight decides.
- The author's claim that "the push itself ran the patched hook": no artefact for it was available to me. Not verified.
- Linux dash `/bin/sh` execution of the hook. Run on macOS only (bash-as-sh). `--no-renames` is a plain git flag, so there is no shell-portability surface.
- Old git versions. I did not probe below the local git version.
- The Spark patches as drafted. I gated the pushed head only.

## Process notes

- The session scratchpad is shared with the commissioning seat. My first setup script ran against the seat's pre-existing `scratchpad/repo` clone before I noticed it was not mine. It set the origin URL to the same value, set `core.sshCommand` to the project's value, added a `pushurl` and fetched `refs/remotes/pr/{1577,1578}`. I unset the `pushurl` again, so `git remote -v` shows the original push URL. The two fetched remote-tracking refs remain there; I deleted nothing. All gate work then ran in my own `scratchpad/g1/`.
- I made no writes to the project checkout. Its 17 untracked files predate this gate. Its HEAD is 1f73d7ac8, untouched. Nothing was pushed to origin, and I made no GitHub, Linear or Docker calls.
- Scripts are in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/scripts/g1_*.sh`. Logs are in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/g1/runs/`.

## Severities

- BLOCKER: none
- MAJOR: none
- MINOR: none
- INFO:
  - N1: `.githooks/pre-push:129/143/252` → `systemTest/scripts/check-package-format.sh` selection.
  - N2: `.githooks/pre-push:351`.
  - N3: `Blockchain/Dev/scripts/check-no-demo-mutation.sh:73` (unwired, per `run-code-guards.sh:116`).
- Suggested follow-up cells (not required for merge): one for N1 and one for N2.

WALL-CLOCK: 24
