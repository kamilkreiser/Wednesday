# BUILD REPORT — QA gate set for Secuura/Blockchain PR #939 (KS-1068) — a widened blockchain-blob type + a comment clause + a compile-time contract test, TIER 2, ROUND 1, ONE VERDICT

Drafter for Wednesday, 2026-09-14 17:1x–17:34 AEST. This is the THIRD gate set of this commission, added
mid-session (Wednesday, 17:04 AEST) alongside gate919 and gate916, same shape and END STATE. Built entirely by
this drafter in one continuous pass (no prior partial work existed for this PR).

Nothing launched, nothing mailed, nothing installed, nothing committed. The Secuura checkout was touched with
READ verbs only (`ls-remote`, `log`, `show`, `diff`, `ls-tree`, `merge-base` — all via the existing read-only
checkout at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`); no `fetch`/`checkout`/`worktree`/
`merge-tree --write-tree` was used anywhere. Every write this session made lives under
`gatesets/2026-09-14_gate939/`. Nothing deleted.

## FOUND

- PR #939 (KS-1068), branch `feature/ks-1068-threadtoken-confidence-blockchain-blob-type`, head
  `284661efe262b825d83b31b875020ff7765757b8` — chain `481e0267f` (the PR's own 09-10 commit) → `91fb13c6e`
  (`--no-ff` merge of develop M38) → `284661efe` (the R2 comment-clause commit, current head).
- Base: origin develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`. Live compare (`develop...head`):
  `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=4 files=3` (measured live via the GitHub compare API).
- The three files, their blobs and numstat, and the audit-baseline control row, all independently re-derived via
  `git diff --name-only`/`--numstat` and `git ls-tree` in the checkout — matches the s226 READY mail
  (`ready_939.txt`) exactly, including the type-widening's exact new fields (`simulatedTxRef`, `threadToken`,
  `confidence`) and the R2 clause's exact comment text at `documentRepo.ts`, both read via `git show`/`git diff`.
- **Confirmed disjoint from sibling PR #919** in the same shared file `documents.ts`: #939's hunks at `:766`,
  `:774`, `:1310`, `:1368-1372`; #919's ONE hunk at `:1657-1699` (`git diff -U0`, both against develop M38).

## TESTED / HOW

- **The reach question, as Wednesday framed it** — `tsc --noEmit -p services/originate` on the merged tree,
  re-derived by this gate with `packages/shared` freshly rebuilt, is the central item the brief commissions;
  the two traps (a stale `packages/shared` dist gives a false red; `tsconfig.json:19` excludes `src/__tests__`
  so `tsc`'s silence is never test-file coverage) are stated explicitly in the brief's opening section, not
  buried — this is the item most likely to be skipped or under-stated by a gate under time pressure, so it is
  named twice (WHY TIER 2 section and THE DELTAS section) with the exact command sequence.
- **`launch_qa_secuura_939_ks1068.sh`** — same guard family as gate919's launcher (dir/file existence exit 2-5,
  head-at-branch exit 6, compare-API match exit 10/13, develop judged BY CONTENT via `GUARDED`/`LANDED_OK` exit
  18/19/rc-0-disjoint, tier/round agreement exit 7/15, ultrathink/brief-path/head-SHA/MAIL/never-push/no-memory/
  never-print-credential exits 8/9/20/12/11/14/17, env-override exit 16, no-TTY exit 21). GUARDED prefixes are
  scoped to #939's OWN three files + `packages/shared/` + the audit baseline + the root lockfile — deliberately
  NOT a blanket `originate/src/` refusal, since PR #919 and other L2 lane siblings touch that prefix routinely
  and disjointly (stated in-file as a comment, per the brief's KNOWN-FRAGILE section). The launcher does **not**
  reference or depend on PR #919's live state anywhere — per Wednesday's explicit instruction that the merge
  order is informational only, never a gate precondition. `bash -n` clean.
- **`controls_check.sh`** (`controls_check.out`): fetches the 3 files + the audit-baseline control row at both
  head and develop via the GitHub contents API (with the same 1MB-cap blob-API fallback built for gate919,
  though none of these three files needed it). Asserts every blob, the fetched bytes against `model/` copies,
  the type-widening anchors (`threadToken?: {` count 1 at head / 0 at develop, `simulatedTxRef?: string | null;`
  count 1/0, `confidence?: string;` present, `txHash?: string | null;` at head vs `txHash: string | null;` at
  develop), the R2 clause's exact text (`Carried forward on a HASHED anchor_failed write` and
  `anchorStateSync.ts's reconcile carry`, both present at head, absent at develop — verified byte-for-byte
  including the straight-apostrophe character, checked via `hexdump` during authoring to rule out a curly-quote
  mismatch), and a raw-control-byte census with a synthetic NUL positive control. **Result: FAILS=0, rc 0.**
- **`redproof.sh`** (`redproof.out`, work dir kept at `redproof.PtcNjv/`): **22 cells (0–21), FAILS=0**, first
  run clean (no debugging needed — this drafter re-used gate919's freshly-corrected pattern directly: the
  compare-API-unreadable arm at exit 13, the M37-repin-with-CMP_WANT-re-aimed disjoint arm, and the
  GUARDED/LANDED arms on the real, measured `BACKLOG.md` blob at M38, exactly as gate919's redproof
  established). Every guard fires at its own distinct exit code (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
  20,21) plus 0 (green first and last, pristine sha-identical).
- **`--check` against the LIVE current develop tip and the live PR head**, run fresh as the final close-out
  step (17:34 AEST): **rc 0**, "all guards pass," 11 guard lines, reading `compare: mb=0e78c7270… ahead=4
  files=3` and `origin develop still 0e78c7270… (M38, git ls-remote)`.

## PINS (re-read live at 17:34 AEST close-out)

- Head: `284661efe262b825d83b31b875020ff7765757b8` (`git ls-remote origin refs/pull/939/head`).
- Base: develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d` — unmoved throughout this drafting session.
- Compare: `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=4 files=3` (GitHub compare API, live).
- PR #919's head, checked for reference only (never a gate condition): `4736e22771c12e56d004f58a67f960ddbc0b0508`
  — unmoved.

## `--check` RETURN CODE: **0** (live develop tip, live PR head, no env overrides).

## Deliverables (this dir → install targets)

| file | install target |
|---|---|
| `2026-09-14_secuura-939-ks1068-tier2.md` | `fleet/qa-agent/briefs/2026-09-14_secuura-939-ks1068-tier2.md` |
| `2026-09-14_secuura-939-ks1068-tier2.prompt.txt` | `fleet/qa-agent/briefs/2026-09-14_secuura-939-ks1068-tier2.prompt.txt` |
| `launch_qa_secuura_939_ks1068.sh` | `fleet/qa-agent/launchers/launch_qa_secuura_939_ks1068.sh` |
| `controls_check.sh` (+ `controls_check.out`: FAILS=0, rc 0) | this set |
| `redproof.sh` (+ `redproof.out`: 22 cells, FAILS=0; work dir `redproof.PtcNjv/`, kept) | this set |
| `model/` (fetched-bytes copies the controls check compares against) | this set |
| `check.out` (final `--check`, rc 0) | this set |
| `SHA256SUMS.txt` (sha256 of every top-level file in this set) | this set |

**Not installed** — every path above is the eventual install target, per the exemplar sets' own convention. The
launcher's `BRIEF`/`PROMPT_FILE`/`REAL_BRIEF` defaults point at THIS gateset directory, so
`bash launch_qa_secuura_939_ks1068.sh --check` passes rc 0 right now, in place. **Install (when Wednesday is
ready):** copy the brief + prompt into `briefs/`, the launcher into `launchers/`, re-point the three path
constants at the top of the launcher to the central `briefs/` location, re-run `--check` once more to confirm,
then:
`cockpit.sh add "QA/Secuura-939" "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_939_ks1068.sh"`

## NOT DONE / could not do

- No actual `tsc`, jest, or `packages/shared` build of any kind — this is a drafting/build pass over the gate
  SET, not the gate itself. The gate's own re-derivation of the reach question is the QA agent's job when
  launched.
- Did not install to the central `briefs/`/`launchers/` directories (not commissioned).
- Did not re-read Linear or GitHub PR comments beyond the READY mail and the s226 lane brief already quoted —
  the git-level facts (diff, blobs, numstat, compare, the exact widened-type and R2-clause text) were
  independently re-derived from the checkout itself.

## UNMEASURED (with the instrument that closes each)

- Whether `tsc --noEmit -p services/originate` on the merged tree, freshly re-derived, actually reads rc 0 for
  real, and whether any reader OUTSIDE this PR's two touched files reds — closed by the gate's own run, per the
  brief's explicit instruction to treat any such red as a FINDING rather than a silent workaround.
- Whether develop moves again before real launch, and whether it moves under a GUARDED path — the launcher's
  `--check` re-reads it at install time and at the start of the real run; a disjoint further move passes and is
  re-stated, a GUARDED-path move refuses (exit 18) unless content-cleared, and a move that lands one of #939's
  own three files at its own head blob refuses as moot (exit 19).
- Whether PR #919 has merged by the time this gate runs — irrelevant to this gate's own guards by design
  (Wednesday's explicit instruction), but worth a human glance in the report since both PRs touch `documents.ts`.

## Anything I must own

- The `GUARDED`/`LANDED_OK` mechanism, the M37-repin redproof technique, and the compare-API-unreadable exit-13
  correction were all worked out first on gate919 (built in parallel this session) and reused here directly,
  already corrected — no separate debugging cycle was needed for this set.
