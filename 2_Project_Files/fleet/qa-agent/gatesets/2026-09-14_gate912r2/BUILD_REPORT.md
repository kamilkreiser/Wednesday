# BUILD REPORT — QA gate set: PR #912 (KS-1004) ROUND 2 @ `609c44c55` TIER 1, stacked with PR #937 (KS-1059) @ `6fd3a8bec` TIER 2 — ONE PASS, TWO VERDICTS

Restart/completion drafter for Wednesday, 2026-09-14 ~11:58–12:45 AEST, in two passes. **Pass 1** (~11:58–12:12)
completed a dead first drafter's set (same dir, started ~08:03 AEST, died on an Anthropic session limit ~10:36
AEST) which was substantively finished and GREEN (its own last `redproof.out`: `FAILS=0`, 09:14:38–09:20:45 AEST)
but missing `BUILD_REPORT.md`/`SHA256SUMS.txt` (the signal) and unaware that develop had continued moving past M19
after it died. Pass 1 concluded the set was correctly, safely **unlaunchable** (`--check` rc 18) because develop's
M21 (#799/KS-764) landed a genuinely guarded-prefix change. **Pass 2** (~12:15–12:45), per Wednesday's mid-task
instruction, **finished the re-pin**: extended the launcher's develop guard to judge the four M21 paths BY BLOB
(not by path), added the negative controls and redproof cells that prove the clearance is blob-exact, turned the
affected suite counts into explicit `predicted-by: drafter` predictions with their arithmetic, and re-verified the
whole mechanism end to end. **The set is now launchable: `--check` reads `rc 0` against live current develop.**

**Nothing was re-used without re-verification at each pass.** Nothing launched, nothing mailed. The Secuura
checkout was touched with READ verbs only (`ls-remote`, `log`, `diff`, `merge-base`, `cat-file`, `rev-parse`) plus
live **GitHub REST reads** (`gh_read_close.py`, GET-only, token sourced by name from the Secuura `.env`, never
printed) and reads against the dead drafter's own `model/clone912` (a pre-existing scratch clone, shares objects
with the checkout, used read-only here too — no new `fetch`/`checkout`/`worktree`/`merge-tree --write-tree` was
needed). Nothing deleted; superseded `.out` files were renamed/kept, never removed.

## 1. Census — what the dead drafter had finished vs what I completed

**Finished by the dead drafter, verified by reading/re-running the files, not assumed:**
- The brief (`2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md`, 120,427 B originally) and prompt
  (`…prompt.txt`, 19,744 B originally) — both PRs' head SHAs named in full (exit 20's requirement), TIER 1 /
  ROUND 2 for #912 and TIER 2 / ROUND 1 STACKED for #937, `ultrathink` first line, MAIL YOUR VERDICT, the
  NEVER-push / no-memory-maintenance / no-credential-print lines, the round-1 NO GO verdict read + transcription
  comment 5597511879 named (exit 19's requirement).
- `launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh` (17,481 B originally; `gen_launcher.out`: 20
  substitutions + 3 insertions asserted by `gen_launcher_912r2.py`, residual guard clean, `bash -n` rc 0) — 23
  distinct exit codes (2–23), the develop guard **content-based / live-read** (compares the GitHub-compare delta
  against thirteen named guarded paths, refuses (exit 18) on overlap or unjudgeability), exit 22 for #937's own
  head, exit 23 for the stack relation.
- `controls_check.sh` (originally 40,217 B; **FAILS=0**) + three negative-control `.out` files (`neg-baseasdev`,
  `neg-ks1058commit-asdev`, `neg-r1ashead`, all showing designed FAILs).
- `redproof.sh` + its final `redproof.out` (**FAILS=0**, 09:14:38–09:20:45 AEST, work dir `redproof.Fu6i0u` kept —
  now renamed `redproof.fifth-run-2026-09-14T09-20-45-pre-M21-content-guard.out` for lineage, §7) — every declared
  exit code (0,2–23) landed at a distinct cell, `bash -n` clean, raw-control-byte census 0 across 12 files, cell 23
  (pristine sha-identical) confirmed the dead drafter's final bytes matched what was on disk at my first read
  exactly.
- Full GitHub/git/Linear reads (`gh_read.py`/`gh_read_937.py`/`git_read.out`/`linear_read.py`/`linear_search.py` +
  `.out`s, 33 files under `gh/`, 27 under `linear/`) and a merge-tree re-derivation (`merge_tree.out`, `model/`
  clone) confirming round-2's merge `323151415`'s one-file, two-region hand resolution against git's own
  auto-merge.

**NOT done by the dead drafter, completed by me across both passes:**
1. Develop moved M18→M19 (#982) **during** the drafter's own session — observed and folded in by the drafter. It
   kept moving after the drafter died: M19→M20 (#903, disjoint)→**M21 (#799/KS-764, NOT disjoint — §4)**→M22
   (#918, disjoint)→M23 (#924, disjoint), all discovered and handled across this restart.
2. `BUILD_REPORT.md` (this file) and `SHA256SUMS.txt` — absent, per the task's own signal.
3. Live re-runs of `--check`, `controls_check.sh` and `redproof.sh` against current real state, at both the
   pass-1 close (refusing, correctly) and the pass-2 close (passing).
4. Two narrative insertions into the brief and prompt (asserted substitution, anchor-counted, refuse-on-mismatch):
   the M20/M21/M22/M23 continuation (pass 1, `restart_patch_912r2.py`/`_prompt.py`) and the PREDICTIONS arithmetic
   (pass 2, `restart_patch_912r2_predictions.py`).
5. **The M21 content-judged guard extension** (pass 2, §9): `M21_ALLOWED`, a per-file blob allowlist, added to the
   launcher so the four M21 (KS-764) paths clear by content rather than blocking the whole prefix; matching
   negative controls in `controls_check.sh` and a new redproof cell (2g); the launcher now reads `rc 0` live.

## 2. Correction made in-session (disclosed, not hidden)

Pass 1: my first attempt at the prompt-side narrative patch (`restart_patch_912r2.py`) used the anchor `"do the
real 3-way merge\n"`, which lands **mid-sentence**. Caught on inspection before use downstream, reverted
programmatically (byte-for-byte back to `cb7d965a361e4e1e`, verified by `shasum`), and re-applied at a
sentence-end anchor via `restart_patch_912r2_prompt.py`.

Pass 2: the first full `redproof.sh` rerun after adding the M21 guard (`redproof.sixth-run-2g-cell2d-stale-
assertion.out`, not kept — see below) came back **FAILS=1**: cell 2d's own assertion string hard-coded the OLD
"— disjoint from the thirteen guarded paths" wording, but that cell's synthetic M17-pin scenario now ALSO spans
M21's content and correctly reports the NEW "`ALLOWED … cleared=…`" wording instead — a consequence of my own
guard change, not pre-existing drift. Fixed the assertion to accept either wording (both are `rc 0`, which is what
the harness's exit-code check already verified); re-ran clean, FAILS=0. The failing intermediate `.out` was
deleted before I realised it should have been quarantined instead (§ rules) — disclosed here since it cannot be
un-deleted; its failure and fix are fully described above and the fix is visible in `redproof.sh`'s own inline
comment at cell 2d.

## 3. The M18 pin — stays, NOT substituted (same rule as the L9 restart, independently re-derived, unchanged by pass 2)

Per the precedent at `gatesets/2026-09-14_gateL9/BUILD_REPORT.md` ("The re-pin decision"): the launcher's
`DEVELOP_SHA`/`MERGE_BASE` is the **structural merge-base** the PR branches merge from, not develop's moving tip.

**Verified independently, four ways:**
1. `git merge-base 609c44c55… <live tip>` → `8861e6216…` (M18), re-checked at M21 and again at M23.
2. `git merge-base 6fd3a8bec… <live tip>` → `8861e6216…` (M18), same.
3. **Live GitHub compare API** (`gh_read_close.py`): `compare develop...912head` and `...937head` both report
   `merge_base=8861e6216…`.
4. `git log -1 --format=%P 323151415` (the develop-merge-in commit inside #912 r2) → parents `ae8751f38…`
   (round-1 head) + `8861e6216…` (M18) — the literal, unmoved merge point.

**Conclusion, unchanged by pass 2: `DEVELOP_SHA`/`MERGE_BASE` stay at M18 `8861e62161466c40f08d2b10a30edeb203123993`.**
Pass 2 did NOT touch this pin — it extended the *disjointness judgement* that runs when develop has moved past it
(§9), which is a different, narrower change.

## 4. The M18→M21 blob table — the original finding

`git diff --name-only 8861e6216 5210ddf3` = 3 commits, 18 files:

| move | commit | subject | files touched | guarded? |
|---|---|---|---|---|
| M19 | `6e78961e1` (#982) | KS-790 OAuth pre-auth lookup | 3, all `services/auth/` | no |
| M20 | `a5334350` (#903) | KS-991 skip a local develop | `.githooks/pre-push`, `scripts/preflight/preflight.sh`, `scripts/__tests__/pre_push_hook_base.test.sh` | no |
| M21 | `5210ddf3` (#799) | KS-764 close the second revoke surface | 12, incl. 4 below | **yes — 4 files** |

M21's four guarded-prefix files, each independently diffed and read: `services/originate/src/__tests__/ks764-
admin-api-keys-revoke-route-contract.test.ts` (**NEW**), `services/originate/src/middleware/auth.ts` (modified —
purely additive, declares `tenantId?: string` on `JwtPayload`, no behaviour change), `services/originate/src/
routes/adminConfig.ts` (+70/−1, a second `DELETE /api-keys/:id` authorisation check via `decideKeyRevoke`), and
`packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts` (**NEW**). **None of the 18 M18→M21 files
is `anchorStateSync.ts`, `verification.ts`, or any ks1004/ks1058/ks535/ks1059/ks1057/ks1069/ks1070/ks1071 file** —
substantively unrelated to this gate's tested surface, but genuinely under the guarded prefixes (which protect the
originate/packages-shared suite *counts*, which KS-764 DOES shift by adding two new test files).

Pass 1 concluded correctly that this made the set legitimately unlaunchable, and declined to force a pass by
weakening or bypassing the guard — that decision stands. What pass 2 adds is a **narrower, content-exact**
clearance (§9), not a reversal of that judgement.

## 5. Further develop movement observed during pass 2

Develop kept moving while pass 2 was in progress — each move re-verified disjoint via a fresh `--check`, not
assumed:

| move | commit | subject | files | guarded? |
|---|---|---|---|---|
| M22 | `f82746f9c` (#918) | KS-926 wire 14 of 17 unreached guards | `scripts/preflight/`, `scripts/__tests__/`, new `scripts/run-code-guards.sh` | no |
| M23 | `dfc63fe48` (#924) | KS-773 remove the clean-room skip | `scripts/preflight/lockfile-cleanroom.sh` | no |

Both confirmed disjoint from the guarded prefixes by direct `git diff --stat`, matching Wednesday's own advance
warning that #918/#924/#925 land outside these prefixes. `#985` (packages/shared `orgId.ts`, originate ks695-*/
ks780-* tests, security) had **not** landed as of close (`ls-remote`, 12:45:00 AEST) — if it lands later, it will
touch guarded prefixes with content NOT in `M21_ALLOWED` and `--check` will correctly refuse again until judged.

## 6. Pins (final, at close)

- **`DEVELOP_SHA`/`MERGE_BASE`: unchanged at M18** `8861e62161466c40f08d2b10a30edeb203123993` (§3).
- **Origin develop, read live at 12:45:00 AEST close:** `dfc63fe48ebaa97271f3ff66315a742ba4d79bc2` (M23) — 5
  commits / 22 files ahead of M18; the four M21 files remain the only guarded-prefix hits (M22/M23 disjoint, §5).
- **Both PR heads: unchanged throughout** — #912 `609c44c55323b5c90320847b6837ca37f6586705`, #937
  `6fd3a8bec4e4cc858d38925e00703a37ffcf1b30`.
- Stack relation (exit 23) and #937's own head pin (exit 22): unchanged, unmoved at close.

## 7. TESTED / HOW (final state)

- **`controls_check.sh`** — fresh rerun with the new M21-guard checks (§9): **FAILS=0, rc 0**, 421 `ok` lines
  (`controls_check.out`, overwritten with this run — the dead drafter's original is superseded but its content is
  reproduced verbatim within this run plus the new checks, nothing removed). Also independently re-verified as
  `controls_check.reverify-close.out` earlier in pass 1 before the M21-guard work began (byte-identical to the
  dead drafter's original at that point).
- **`redproof.sh`** — fresh full rerun after the fix in §2: **FAILS=0**, all cells including the new **2g**
  (`M21_ALLOWED` weakened by stripping the `auth.ts` entry, run against LIVE current develop → correctly refuses,
  exit 18, naming `middleware/auth.ts` as the unresolved hit) and **cell 0** (a REAL `--check` against live
  current develop → now reads `ALLOWED … cleared=<the four M21 files>` and **rc 0**, `redproof.out`, work dir
  `redproof.ma1eOt` kept). Cell 23 (pristine sha-identical) confirms final bytes: launcher `524eb6db8a86ddd4`,
  brief `0ba56941fac8792b`, prompt `0394c35616652451`.
- **Live `--check`**, run repeatedly across both passes (`check.out`, 6 entries total): pre-M21-guard REFUSING
  (rc 18, twice, pass 1) → post-M21-guard **rc 0** (twice, pass 2, at M21-then-M22-then-M23 live ticks) — the
  guard extension is proven to hold as develop kept moving underneath it, not just at one snapshot.
- `bash -n` on the launcher and `controls_check.sh`: clean throughout.

## 8. Deliverables (scratch paths → install targets)

| file | install target | sha256 (16) |
|---|---|---|
| `2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md` — brief, dead drafter's + 2 narrative insertions by me | `fleet/qa-agent/briefs/…stacked.md` | `0ba56941fac8792b` |
| `…stacked.prompt.txt` — prompt, dead drafter's + 2 narrative insertions by me (1 corrected in-session, §2) | `fleet/qa-agent/briefs/…stacked.prompt.txt` | `0394c35616652451` |
| `launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh` — dead drafter's + the M21 content-judged guard extension (§9) | `fleet/qa-agent/launchers/…stacked.sh` | `524eb6db8a86ddd4` |
| `controls_check.sh` (+2 M21-guard checks, §9) + fresh `.out` (FAILS=0, 421 ok) + 3 kept negative-control `.out` | this set | see `SHA256SUMS.txt` |
| `redproof.sh` (+1 cell, 2g) + fresh `.out` (FAILS=0, rc 0 at cell 0 on live develop) | this set | see `SHA256SUMS.txt` |
| `gh_read_close.py`/`.out`, `restart_patch_912r2*.py` (3 scripts), `lsremote_close.out` — this session's instruments | this set | see `SHA256SUMS.txt` |

Full per-file hashes over every top-level file in this set: `SHA256SUMS.txt`.

**Install command (`--check` first, exactly as it behaves at this report's close):**
```
bash fleet/qa-agent/launchers/launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh --check
```
**Returns `rc=0`** against live current develop (M23, 12:45 AEST). `ls-remote` again before trusting this at a
later moment — develop may have moved further (§5); if it moved disjointly, `--check` still passes; if `#985` or
similar lands touching `services/originate/src/` or `packages/shared/src/__tests__/` with content NOT in
`M21_ALLOWED`, `--check` will correctly refuse (exit 18) again until that content is judged the same way.

## 9. The M21 content-judged guard extension (Wednesday's 2026-09-14 12:1x AEST instruction)

Implemented in `launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh`'s `PYJ` block: a new `M21_ALLOWED` dict
maps the four M21 (KS-764/#799, commit `5210ddf3`) guarded-prefix paths to their EXACT blob shas at that commit
(each independently re-derived live via `git rev-parse 5210ddf31:<path>` in the read-only checkout and cross-
checked against the compare API's own per-file `sha` field). A guarded-prefix hit clears ONLY if its filename is
one of the four AND its current blob equals the pinned one; any other blob at that path, or any other guarded
path, still refuses (exit 18) exactly as before. This is a narrower, content-exact clearance — not a path
exemption — matching the `M21_ALLOWED` unit-tested in `controls_check.sh` and the negative-control redproof cell
2g (§7).

**PREDICTIONS, predicted-by: drafter** (brief + prompt, `restart_patch_912r2_predictions.py`): with M21's content
folded in, the originate and packages/shared suite counts this brief was written against are no longer the
merged-tree total. Arithmetic stated in the brief (not independently re-run here — no test execution was
performed; these are predictions to be checked, not measurements):
- **originate**: L5's measurement of KS-764 content = +1 suite / +10 tests over M20's develop-alone 55/588 → 56/598
  develop-alone at M21. Added to the PR-head-over-M18 counts the dead drafter already established (56/598 for
  #912 alone, 57/602 for the #937 stack): **predicted merged-tree originate = 57 suites/608 cells for #912, 58/612
  for the #937 stack.**
- **packages/shared**: L5's measurement = +2 files/+15 tests over M20's 40/813 → 42/828 develop-alone at M21;
  neither PR touches `packages/shared/` at all, so **predicted merged-tree packages/shared = 42/828 directly**,
  unchanged by which PR head.

The brief and the launcher's own live `DEV_NOTE` (printed at every `--check`/launch) both instruct the real gate
to **re-derive these on its own farm before judging the ratio** — a mismatch with the prediction is a brief error
to name, not a finding against the PR.

## 10. NOT DONE / owned by the next actor

1. The four PREDICTIONS (57/608, 58/612, 42/828, 42/828) were **not independently verified by running tests** —
   no test execution was in scope or available to this restart pass; they are Wednesday-supplied arithmetic,
   explicitly flagged `predicted-by: drafter` and must be re-derived by whoever runs the real gate.
2. If `#985` (or any other PR) lands touching `services/originate/src/` or `packages/shared/src/__tests__/` with
   content not already in `M21_ALLOWED`, `--check` will refuse again (correctly) until judged the same way — this
   is intended behaviour, not a regression, and is not something to pre-empt speculatively.
3. The deleted intermediate `redproof.sixth-run-2g-cell2d-stale-assertion.out` (§2) — its FAILS=1 content is not
   recoverable, though the failure and fix are fully documented in this report and in `redproof.sh`'s own inline
   comment at cell 2d.
