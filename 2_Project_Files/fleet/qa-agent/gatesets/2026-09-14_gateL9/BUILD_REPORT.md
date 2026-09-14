# BUILD REPORT — QA gate set LANE L9: PR #940 (KS-1075) + #941 (KS-1077, after #940) + #942 (KS-1078) + #887 (KS-961, Peter's re-run posted) — ci-workflows, TIER 2, ONE PASS, FOUR PER-PR VERDICTS, ALL FOUR MERGES ARE KAM'S

Restart/completion drafter for Wednesday, 2026-09-14 11:39–11:56 AEST. The first drafter of this set (same dir,
08:07–~10:36 AEST) died on an Anthropic session limit mid-session with the brief, prompt, launcher, `controls_check.sh`
and `redproof.sh` all SUBSTANTIVELY COMPLETE (all eleven sections present, #887 integrated as a fourth PR, the
M18→M19 develop move already observed and folded into the brief/prompt/redproof at ~09:0x AEST, `redproof.HzmWpi/`
and two kept first/second-run `.out` files showing the drafter iterating the M19 regex to green) — but it died
**before writing `BUILD_REPORT.md` or `SHA256SUMS.txt`, and before develop's second move (M19→M20, landed
2026-09-14T23:18:09Z / 09:18:09 AEST — i.e. mid-drafting, before the drafter's own last 10:36 AEST file
timestamps) was ever observed.** Absence of `BUILD_REPORT.md` was the signal, per brief.

**Nothing was re-used without re-verification.** Nothing launched, nothing mailed, nothing written outside
`gatesets/2026-09-14_gateL9/`. The Secuura checkout was touched with READ verbs only (`ls-remote` · `diff --name-only`
· `diff --numstat` · `log` · `merge-base` · `cat-file` — all via the existing read-only checkout at
`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`); no `fetch`/`pull`/`checkout`/`worktree`/
`merge-tree --write-tree` was needed there because no NEW merge-tree computation was required (see "The re-pin
decision" below) — the drafter's own `model/clone/` was left untouched. Nothing deleted.

## Census: what the dead drafter had finished vs what I completed

**Finished by the dead drafter (verified by reading the files, not assumed):**
- The brief (`2026-09-14_secuura-L9-…tier2.md`, 11 sections: WHY TIER 2 / RULED / TARGET / THE DELTAS / 2a
  LEGITIMATE SHAPES / WHAT THIS GATE MUST ESTABLISH / NOT COMMISSIONED / KNOWN-FRAGILE / BOUNDS / REPORT /
  VERDICT DESTINATION+PROVENANCE) — all four PRs' sections present, all four head SHAs named, the M18→M19 move
  folded in, the "`kam-merges`" / "MERGE… is Kam's" / "the merge seat routes each to Kap with the link" language
  present verbatim at lines 13, 19, 25, 215, 235 (task's required line — already there, verified, not added by me).
- The prompt (`…tier2.prompt.txt`) — `ultrathink` first line, brief path, MAIL YOUR VERDICT, the eleven
  must-not-miss items, the NEVER-push / no-memory-maintenance / no-credential-print lines.
- `launch_qa_secuura_L9_940_941_942_887.sh` (22,632 B) — generated, `bash -n` clean, all 23 distinct exit codes
  wired, the develop-move guard content-based (blob comparison of the three judged workflow files + 8 GUARDED
  path prefixes), NOT a literal-SHA-tracking guard.
- `controls_check.sh` (134 positive controls + `guards_sim.py` 40/0) and three negative-control `.out` files
  (`neg-devas940`, `neg-origas942`, `neg-revas887`) all showing FAILS>0 as designed.
- `redproof.sh` — present, and TWO earlier kept runs (`redproof.first-run-slash-names-and-dev-moved.out`,
  `redproof.second-run-devnote-regex.out`) documenting the drafter's own iteration to fold in the M19 move.
- #887's four-head integration (`brief_patch_887.py`, `gen_patch_887.py`, `gh_read_887.*`, `git_read_887.*`,
  `linear_read_887.out`, `records_887.out`, superseded three-head brief/launcher kept in `superseded_three-head/`).

**NOT done by the dead drafter (what I completed):**
1. The M19→M20 develop move (landed 09:18:09 AEST) was never observed or folded in — every `check.out` /
   `redproof.out` / brief-provenance line on disk still read the M18/M19 state as of ~10:36 AEST.
2. `BUILD_REPORT.md` (this file) and `SHA256SUMS.txt` — absent, per the task's own signal.
3. A live re-run of `--check`, `controls_check.sh` and `redproof.sh` against CURRENT real state.

## The re-pin decision — NOT a blanket M18→M20 substitution, and why

My brief said "every occurrence of the M18 SHA becomes M20, asserted" on the L5 precedent. **That rule does not
apply uniformly here, and applying it literally would have broken the launcher.** Reading the launcher itself
(not assuming) shows `DEVELOP_SHA` is not "develop's current tip" — it is the **live-asserted merge-base** of
#942 and #887 against develop, baked into `CMP_WANT="… #942 mb=$DEVELOP_SHA … #887 mb=$DEVELOP_SHA …"`
(`launch_qa_secuura_L9_940_941_942_887.sh:165`), checked against GitHub's own `merge_base_commit` for
`develop...<head>`. This is not an arbitrary label: **#942's own head IS a `--no-ff` merge of M18** (`git log -1
--format='%H %P' 53b9c3cc1…` → parents `c1676269d…` + `8861e6216…`), and #887's parent `de376a9f1` likewise
merges M18. So `git merge-base(#942, current-develop)` and `git merge-base(#887, current-develop)` are
**structurally pinned to M18 regardless of how far develop's tip moves**, as long as neither branch is rebased
(confirmed unmoved: heads unchanged since the drafter's reads).

**Verified independently, three ways, before touching anything:**
1. `git merge-base 53b9c3cc1a89f513620516c580a5de5bd60c64de a5334350221c819f54d4a20a3308daeb9ca09617` → `8861e6216…` (M18).
2. `git merge-base 3aee3deed2e3ac557f0a52c0797c2a4a8df25f69 a5334350221c819f54d4a20a3308daeb9ca09617` → `8861e6216…` (M18).
3. **Live**, running the REAL launcher's `--check` against current GitHub/git state (no file edits at all at that
   point) — `check.out`, 11:45:48 AEST — printed `all guards pass … compares: … #942 mb=8861e62161466c40f08d2b10a30edeb203123993 ahead=2 files=3 | #887 mb=8861e62161466c40f08d2b10a30edeb203123993 ahead=5 files=2 … origin develop MOVED 8861e62161466c40f08d2b10a30edeb203123993 -> a5334350221c819f54d4a20a3308daeb9ca09617: commits=2 files=6 (.test.sh files 1) — disjoint …`, **rc 0**.

Rewriting `DEVELOP_SHA`/`CMP_WANT`/`BASE_940_941`/`controls_check.sh`'s `DEV` pin to M20 would have made the
launcher assert a merge-base that GitHub's API does NOT report (it still reports M18), causing a **false**
exit-10 refusal. So those pins were **left at M18, verified correct, not substituted** — this is itself the
finding the task asked me to surface rather than assume away.

**What DID need to change:** the brief's and prompt's *narrative* move-log (an observational record of what
develop's tip has done over time), which was current only through M19. I added ONE new bullet to each, via a
counted, asserted-substitution script (`restart_patch_L9.py`, in this dir) — same discipline as `brief_patch_L5.py`:
anchor-count asserted before and after, refuses on any mismatch. Brief: `d0cef8d7b53ca255` → `…` (the M19-move
bullet followed immediately by the new M20-move bullet, +1,415 bytes). Prompt: `23474b7019a48a93` →
`d4d0751d3e1ad9f0` (+213 bytes, one clause). Nothing else in either file was touched — re-verified by the fresh
`--check` (still rc 0, still "all guards pass") and `controls_check.sh` (still FAILS=0) run AFTER the edit.

## The M18→M20 blob table (measured, not assumed)

- `git diff --name-only 8861e6216 a5334350221c819f54d4a20a3308daeb9ca09617` = 2 commits / 6 files total:
  M19 (#982, `services/auth/src/routes/oauth.ts` +23−5, NEW `__tests__/ks790-token-pre-auth-user-lookup.test.ts`
  +249, `__tests__/ks820-821-…test.ts` +8) + M20 (#903, `.githooks/pre-push` +39−1,
  `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` +123−1, `Blockchain/Dev/scripts/preflight/preflight.sh`
  +24). **None of the 6 is under any of the eight GUARDED prefixes** (`.github/workflows/`,
  `Blockchain/Dev/.security/`, `Blockchain/Dev/scripts/audit/`, `scripts/run-shell-suites.sh`,
  `systemTest/__tests__/`, `Blockchain/Dev/docs/DEV-PROCESS.md`, `Blockchain/Dev/package-lock.json`, and the
  launcher's own listed eighth) and none is one of the three judged workflow files.
- The three judged workflow blobs the brief and `controls_check.sh` cite as "develop's blob" —
  `security-scan.yml` `47da5cac9`, `pr-security-gates.yml` `571817703`, `pr-platform-suites.yml` `a509ad793` — are
  **re-read at M20 through the live `--check` run and through `controls_check.sh`'s contents-API reads: IDENTICAL,
  same three blob SHAs.** Verdict: **0 of the cited/guarded blobs moved between M18 and M20.**
- `git merge-base` of #940/#941 vs M20 = `a1e49d151…`, unchanged (unaffected by the develop-M18-M20 question at
  all — they diverged from an earlier common point, per `check.out`'s own unchanged `mb=a1e49d151…` reading).

## TESTED / HOW

- **Live `--check`** (`check.out`, re-run twice — once pre-edit at 11:45:48 to prove the mechanism needed no code
  change, once post-edit at 11:47:29 to prove the narrative edit didn't disturb it): both **rc 0**, "all guards
  pass," 12 guard lines each, develop correctly read as `MOVED 8861e6216 -> a5334350…: commits=2 files=6 (.test.sh
  files 1) — disjoint.`
- **`controls_check.sh`** (fresh run, `controls_check.out`, 11:48 AEST): **134 positive controls `ok`, `guards_sim.py`
  40/0, FAILS=0, rc 0.** The three saved negative-control `.out` files (`neg-devas940` FAILS=9, `neg-origas942`
  FAILS=9, `neg-revas887` FAILS=15) are content-based, not tip-dependent — re-checked as still valid (still FAIL
  as designed) without re-running, since nothing they assert touches the M18↔M20 question.
- **`redproof.sh`** (fresh run, `redproof.out`, work dir kept at `redproof.iAQkDM/`, 11:48:52–11:55:51 AEST):
  **36 cells, FAILS=0.** Cell 0 green first (rc 0, develop note present). Every declared exit code (0–22, the
  full set 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,127) fired at a distinct cell. The
  develop-moved arms (18b/18c/18d, pinned at M15) now read **live against the M20 tip**
  ("`origin develop MOVED 1c38077ba… -> a5334350…: commits=5 files=12 (.test.sh files 3) — disjoint`") —
  keyed on M20 as the task required, with no code change needed (the regex at cell 0 and the arms' printer were
  already tip-generic `[0-9a-f]*`/live-read, which is exactly why the M18 pins didn't need touching). Cell 25
  (green again, pristine sha-identical) confirms the FINAL bytes: launcher `2c69685a668b8886`, brief
  `d0cef8d7b53ca255`, prompt `d4d0751d3e1ad9f0` — matching `SHA256SUMS.txt`. Raw-control-byte census 0 across 12
  files + the synthetic NUL positive control. `bash -n` clean.
- No first-run failures this session (both the narrative patch and both re-runs were clean on the first attempt);
  the drafter's own two earlier kept redproof runs (`.first-run-slash-names-and-dev-moved.out`,
  `.second-run-devnote-regex.out`) are left in place for lineage, unmodified.

## Pins (read 11:39:21 AEST by `ls-remote`; re-read live at 11:45:48, 11:47:29 and 11:48–11:56 during the check/controls/redproof runs; all agree; re-stated at close 11:56 AEST)

- **Heads, unchanged since the dead drafter's reads:** #940 `1aa708be9fcf7a23575398546d84848c967e81c5`; #941
  `d105e07a81c8549b7f47c0542e9594204ce6f599`; #942 `53b9c3cc1a89f513620516c580a5de5bd60c64de`; #887
  `3aee3deed2e3ac557f0a52c0797c2a4a8df25f69`. All four present at their branches on origin (`--check`, both runs).
- **`DEVELOP_SHA` / `CMP_WANT` base / `controls_check.sh`'s `DEV`: stays `8861e62161466c40f08d2b10a30edeb203123993`
  (M18) — asserted correct, not substituted** (see "The re-pin decision" above; git-verified merge-base, live
  API-verified compare, three-way cross-check).
- **Origin develop's actual current tip: M20 `a5334350221c819f54d4a20a3308daeb9ca09617`** (`KS-991: skip a local
  develop that origin/develop provably supersedes (#903)`, 2026-09-14T09:18:09+10:00). M18→M20 = 2 commits / 6
  files, 0 under GUARDED paths, 0 of the 3 judged blobs moved — logged into the brief/prompt as a new bullet,
  not as a pin rewrite.
- `BASE_940_941` = `a1e49d15152102acec7c97d96918211227c7fe1e`, unchanged, independent of the M18/M20 question.

## Deliverables (scratch paths → install targets)

| file | install target | sha256 (16) |
|---|---|---|
| `2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md` — the brief, completed by the dead drafter, +1 narrative bullet by me | `fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md` | `d0cef8d7b53ca255` |
| `…tier2.prompt.txt` — the prompt, completed by the dead drafter, +1 clause by me | `fleet/qa-agent/briefs/…tier2.prompt.txt` | `d4d0751d3e1ad9f0` |
| `launch_qa_secuura_L9_940_941_942_887.sh` — the dead drafter's, UNCHANGED (verified correct at M20, not edited) | `fleet/qa-agent/launchers/launch_qa_secuura_L9_940_941_942_887.sh` | `2c69685a668b8886` |
| `controls_check.sh` (+ fresh `.out`: 134 ok + guards_sim 40/0, FAILS=0, rc 0) + 3 negative-control `.out` (still valid, unedited) — UNCHANGED script | this set | see `SHA256SUMS.txt` |
| `redproof.sh` (+ fresh `.out`: 36 cells, FAILS=0, every exit code fired, develop-moved arms now live-keyed on M20) — UNCHANGED script | this set | see `SHA256SUMS.txt` |
| `restart_patch_L9.py` (+ `.out`) — the one asserted, counted edit this restart made | this set | see `SHA256SUMS.txt` |
| `SHA256SUMS.txt` — sha256 of all 45 top-level files in this set | this set | — |
| everything else (`gh/`, `linear/`, `model/`, `redproof.*/`, `l9sim.*/`, `superseded_three-head/`) — the dead drafter's reads and clone, kept verbatim for lineage | this set | — |

**Install:** copy the brief + prompt into `briefs/`, the launcher into `launchers/`, then
`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_L9_940_941_942_887.sh --check`
(headless-safe, rc 0 expected; the LAUNCH path refuses without a TTY — run it in a pane via `cockpit.sh add`,
never from a Bash tool).

## NOT DONE / could not do

- No vitest/jest/suite run of any kind — this is a drafting/completion pass over the gate SET, not the gate itself;
  the four PRs' live CI runs are the artefact the brief already cites (`check.out`'s "live runs" line, unchanged).
- Did not re-derive `guards_sim.py`'s predictions independently — re-ran it (via `controls_check.sh`) on freshly
  fetched bytes and it holds 40/0; did not re-write its logic.
- Did not re-read Linear or GitHub PR bodies/comments fresh — the dead drafter's 08:1x–08:4x AEST reads stand
  (nothing in this restart's scope touched PR content, only the develop-tip observation).
- Did not touch `model/clone/` (the dead drafter's) or compute any new `merge-tree` — not needed, since
  `--check`'s live compare-API read already proves the merge-base assertion holds at M20 without recomputing a tree.

## UNMEASURED (with the instrument that closes each)

- Whether develop moves again before real launch — the launcher's `--check` re-reads it at install time and at
  start/end of the real run (its own design); a disjoint further move passes, a GUARDED-path move refuses at 18.
- Whether Kam merges #940/#941/#942/#887 mid-pass (each would move develop under a GUARDED path via the workflow
  file itself) — the launcher's LANDED-blob guard (exit 19) catches this before launch; not exercised against a
  real merge in this restart (redproof cell 19 exercises it synthetically, as before).

## Anything I must own

- The one substantive judgment call in this restart — declining the literal "replace every M18 occurrence with
  M20" instruction for `DEVELOP_SHA`/`CMP_WANT`/`BASE_940_941`/`controls_check.sh`'s `DEV` — is mine, made because
  the live mechanism (git merge-base, GitHub compare API, and the launcher's own `--check`) all independently
  confirmed the literal substitution would have been factually wrong and would have broken the compare guard.
  Flagging this explicitly for Wednesday/Kam in case the L9 launcher's "pin = live-merge-base, not tip" design
  should itself be revisited for future lanes — it worked correctly here only because #942/#887 carry M18 as a
  literal merge parent in their own history.
