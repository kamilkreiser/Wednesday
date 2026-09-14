# BUILD REPORT — QA gate set, lane L3b: PR #931 (KS-1061) @ 795307023 [RE-PINNED, PART 1] + PR #720 (KS-487/KS-657) @ cd62c9f89 [PART 2, added mid-draft]

Drafter for Wednesday, 2026-09-14, 13:24–14:0x AEST. Nothing launched, nothing mailed, nothing merged,
nothing deleted. Nothing written outside `fleet/qa-agent/gatesets/2026-09-14_gate931/`. The read-only
Secuura checkout at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` was touched with READ
verbs only (`show`, `diff --name-only`/`--stat`, `log`, `ls-tree`, `cat-file`, `merge-base`, `ls-remote`);
the session's own `pretooluse_no_cd.sh` hook refused an in-place `fetch`/`merge-tree` there and forced the
isolated-clone approach documented below — a real, live enforcement of hard rule 1, not a hypothetical.

## THE RE-PIN — landed, this gate set SHIPS on the new head

**PR #931's branch moved TWICE during this drafting session.** Round-1 was drafted against
`53b8a1f7a6056c1560af71252c753c005bee8f06`; mid-draft this drafter discovered (by direct `git ls-remote`,
before any READY mail existed for it) that the branch had already moved to
`7953070230d285fdebc0c65b834ac8340c02c0b6` — a second `--no-ff` merge of a later develop tip
(`b9f541e6b158f831576ecc870244f361f219a114`, M31, containing #985's squash) resolving the ks695 conflict
PART 1 had found as the UNION: the helper form with #985's `normaliseOrgId` pass-through kept as an
override (never a stub). Wednesday's own re-read confirmed the same SHA and supplied the READY mail's
facts (`ready_931_r1b.txt`, ticket comment `7fa0ca09-c69f-461f-8dd9-b875344b7faf`, PR comment `5658732108`).
**This gate set now SHIPS re-pinned to `7953070230d285fdebc0c65b834ac8340c02c0b6` — every deliverable
(launcher, `controls_check.sh`, `guards_sim.py`, `gh_read.py`) was re-run against this head and is
GREEN at it (see TESTED/HOW below).** `53b8a1f7a6056c1560af71252c753c005bee8f06` is SUPERSEDED — named
throughout the brief/prompt as history, never as the gate target.

**Merged view vs own-delta view (Wednesday's instruction), both independently derived:**
- **Merged view** — `git diff --name-only b9f541e6b158f831576ecc870244f361f219a114
  7953070230d285fdebc0c65b834ac8340c02c0b6` = **14 paths**, all under
  `services/originate/src/__tests__/`, matching GH `/pulls/931/files` (14) and `compare/develop...795307023`
  (`status=ahead ahead=4 behind=0 files=14 merge_base_commit=b9f541e6b158f831576ecc870244f361f219a114`).
- **Own-delta view — corrected after this drafter's first attempt used the wrong formula** (caught before
  shipping): `git diff --name-only $(git merge-base b9f541e6b 795307023) 795307023` does **NOT** isolate
  "what the re-merge changed" — that merge-base IS `b9f541e6b` itself, so the two-tree diff returns the
  SAME 14 files as the merged view (develop's tree never had the helper-converted forms, so the diff is
  dominated by the branch's entire cumulative history — exactly the two-dot/merge-base trap
  STANDING_LINES warns about). The command that actually answers "what did THIS merge commit change" is a
  **direct two-head diff**: `git diff --name-only 53b8a1f7a…06 795307023…0c6` = **28 files, +2366/−159**
  (develop's own M23→M31 history: workflows, `packages/shared/**`, `services/auth/**`, none of it this
  PR's). **Restricted to `services/originate/src/__tests__/`, that same two-head diff narrows to exactly
  TWO files**: `ks695-erasure-by-external-ref.test.ts` (+4, the union's pass-through, new blob
  `b0933eddf40360ca89415f7f608aa75b92ae4cd4` — matches the READY mail exactly) and the brand-new
  `ks780-org-id-is-the-shared-implementation.test.ts` (+49, 0 root shared mocks, develop's own, riding
  along). **Independently confirmed by blob comparison** that the two folds
  (`ks1103-verify-hash-field.test.ts`, `ks764-admin-api-keys-revoke-route-contract.test.ts`) are
  byte-identical between `53b8a1f7a` and `795307023` — untouched by the re-merge.

**What is CONFIRMED at the new head vs what is still CLAIMED (builder-only), stated plainly:** the file set,
the file-count cross-checks, the ks695/ks780 isolation, and the two folds' blob-identity are all
independently confirmed by this drafter (git + GH REST, not narrated). The builder's specific jest numbers
at this head (guard 3/3, ks695 40/40, ks780 3/3, whole originate 58/604, tamper T5's 10/40) are CLAIMED
only — this drafter ran no jest, per charter; they are the gate's to confirm.

## Deliverables (scratch paths → install targets)

| file | install target | sha256[:16] |
|---|---|---|
| `2026-09-14_secuura-931-ks1061-tier2.md` (brief, PART 1 + PART 2, RE-PIN notice at top) | `fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.md` | see SHA256SUMS.txt |
| `2026-09-14_secuura-931-ks1061-tier2.prompt.txt` (prompt, PART 1 + PART 2, RE-PIN notice at top) | `fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.prompt.txt` | see SHA256SUMS.txt |
| `launch_qa_secuura_ks1061_931.sh` (pins BOTH #931 `795307023` and #720 `cd62c9f89`, each independently substitutable via `QA931_HEAD`/`QA720_HEAD`) | `fleet/qa-agent/launchers/launch_qa_secuura_ks1061_931.sh` | see SHA256SUMS.txt |
| `gen_launcher_931.py` (generator, `--head`/`--devbase` CLI re-pin support — used LIVE to perform this very re-pin) | this set | see SHA256SUMS.txt |
| `controls_check.sh` (+ `.out`: FAILS=0 at the re-pinned head; PART 1 §1-6 + PART 2 §7) | this set | see SHA256SUMS.txt |
| `controls_check.neg-devashead.out`, `.neg-basashead.out`, `.neg-head720bad.out` (3 negative-control runs at the re-pinned head, all FAIL as designed) | this set | see SHA256SUMS.txt |
| `redproof.sh` (+ `.out`) | this set | see SHA256SUMS.txt |
| `guards_sim.py` (+ `.out`: census/red-first/tamper SIMULATION at both the superseded and re-pinned heads, no jest run) | this set | see SHA256SUMS.txt |
| `gh_read.py`/`gh_read.out` (re-fetched at the re-pinned head), `linear_read.py`/`linear_read.out` (PART 1, superseded-head Linear reads — KS-1061's ticket state is unaffected by the re-pin) | this set | see SHA256SUMS.txt |
| `model/` (saved read-only file copies at 6 refs incl. both heads + one isolated `git clone --shared --no-checkout` at `model/repo/`) | this set | not individually summed (bulk evidence) |
| `SHA256SUMS.txt` | this set | — |

## Pins (final, as shipped)

- **PART 1, PR #931: HEAD `7953070230d285fdebc0c65b834ac8340c02c0b6`** (RE-PINNED; superseded:
  `53b8a1f7a6056c1560af71252c753c005bee8f06`). Merge-base `b9f541e6b158f831576ecc870244f361f219a114` (M31)
  — confirmed via GH compare's `merge_base_commit`. Re-read via `git ls-remote` at close, unmoved since the
  re-pin.
- **PART 2, PR #720: HEAD `cd62c9f89491072ce4e6e7bde9946d22409b1110`** — independently confirmed via GH
  REST `/pulls/720` (not copied verbatim from the commission mail, which arrived with the SHA split across
  a line break). Re-checked via `git ls-remote` at close — **unmoved** throughout the whole session.
- **origin/develop's live tip**, read repeatedly across the session: `f09b629457…` (13:26) →
  `b9f541e6b…` (13:4x, unmoved through close) — the content-judged guard (`controls_check.sh` §6, launcher
  exit 18) re-derives this live every run; it needed no manual pin, unlike the #931 HEAD itself.

## FOUND (hypotheses with FAIL conditions and predictions)

- **F1:** #931's delta is tests-only, exactly 14 paths at BOTH heads — CONFIRMED three independent ways
  (local git diff, GH `/pulls/931/files`, GH `compare`) at the superseded head, RE-CONFIRMED at the
  re-pinned head. No FAIL.
- **F2:** the ks1061 guard's red-first state is exactly `{ks1103, ks764}` offenders, totalFactories=12 —
  SIMULATED (not jest-executed) via `guards_sim.py`, matches the builder's own claim exactly, UNCHANGED by
  the re-pin (the folds are untouched). `predicted-by: drafter` — the gate must confirm by running jest.
- **F3:** the live-develop content guard showed EXACTLY ONE merge-tree conflict (ks695) against the
  superseded head, confirmed independently twice. **On the re-pinned head, the SAME merge-tree check
  (isolated clone, live develop tip) now shows 0 conflicts** — because the branch has already absorbed the
  develop tip it needed. Both states independently verified; the guard logic handles both explicitly
  (`controls_check.sh` was updated to assert either outcome by name, not to silently accept "not 1").
- **F4:** GH `mergeable` read `None`/`unknown` against the superseded head; **`true`/`unstable` against the
  re-pinned head** — both are transient/real GitHub states, not contradictions.
- **F5:** the PR body's Test Evidence is internally consistent with each READY mail in turn (same author,
  same session) — READ evidence, not RUN evidence, at either head.
- **F6 (PART 2):** #720's 12 added lines do not touch the shared ks444 factory itself — CONFIRMED by direct
  diff read. Supports "#931 before #720"; not independently proven composable (the gate's to run).
- **F7 (PART 2):** the BACKLOG.md merge-conflict-recovery mechanism is a real, well-known git-merge class,
  plausible and consistent with this fleet's own precedent, but the specific row-count numbers are CLAIMED
  by the builder only — not independently re-derived.
- **F8 (new, from the re-pin process itself):** this drafter's OWN first attempt to state the "own-delta
  view" used the wrong git-diff formula and would have shipped a wrong claim (see THE RE-PIN section above)
  — caught and corrected before shipping by actually running the commands rather than reasoning from the
  merge-base concept alone. Recorded here because it is exactly the class of error this fleet's own
  STANDING_LINES exists to catch, and this drafter caught its own instance of it.

## TESTED / HOW (controls, this drafter's own runs, chronological)

- **`controls_check.sh` — final clean run AT THE RE-PINNED HEAD: FAILS=0, rc=0** (`controls_check.out`,
  ~14:00 AEST) — 14-path census (both merged-view and own-delta-view numbers independently re-derived), GH
  cross-checks (fresh `/pulls/931/files`, fresh `/pulls/720/files`), the two folds' byte-exact shapes (via
  `perl -0777` — macOS `/usr/bin/grep` has no `-P`/`-z`), the ks444 KS-927 comment-block byte-identity, the
  live-develop content guard (isolated `model/repo` clone, `merge-tree --write-tree`, now correctly
  asserting 0 conflicts since DEVTIP==DEVBASE post-re-pin), and PART 2's 2-file/0-product delta for #720.
  **Three independent negative-control runs at the re-pinned head, all FAIL as designed**
  (`controls_check.neg-devashead.out` FAILS=6 rc=1; `controls_check.neg-basashead.out` FAILS=3 rc=1;
  `controls_check.neg-head720bad.out` rc=2, "CANNOT READ HEAD720") — exceeds the "≥2 negative arms FAIL" bar.
- **`launch_qa_secuura_ks1061_931.sh --check` — final clean run AT THE RE-PINNED HEAD: rc=0, "all guards
  pass"** (`check.out`) — both heads confirmed present at their branches, merge-base `b9f541e6b…` confirmed
  live via GH compare, origin/develop confirmed still at that same SHA (stable through close), both
  brief+prompt agreement checks, the model-clone-present check, the TTY-refusal note.
  **Earlier in the session, the SAME launcher — still pinned to the by-then-superseded `53b8a1f7a` —
  correctly REFUSED with exit 6** the moment the real branch moved, unprompted, before any human or
  READY mail said so. That refusal is preserved as the strongest evidence this guard family works: it
  caught a real state change in real time.
- **`redproof.sh` — SIX runs total this session, all evidence kept** (`redproof.bNh6Sh/`, `redproof.FJF7BN/`,
  `redproof.9nfoEf/`, plus three more at/after the re-pin — none deleted, per the never-delete HOLD).
  1. **First run, against the then-current, unmoved `53b8a1f7a`:** 22 cells + the final byte-stability
     checks, **FAILS=1** — the single failure was a SCRIPT bug (a cell name containing a literal `/` broke
     its output path) — found and fixed, not a guard-logic defect. `grep -l "REFUSING: 53b8a1f7a"
     redproof.bNh6Sh/*.out` → **0 files**, confirming every cell in that run saw the correct, then-current
     head.
  2. **Second and third runs (after the fix):** cells 0-13 all `ok`, then cells 14-22 all read `got=6`
     instead of their designed codes — root cause confirmed NOT a script bug: the branch moved to
     `795307023` **during** these runs, and the exit-6 "head not at branch" guard fired correctly and
     consistently for the remainder, because the world had genuinely changed underneath a pin that was, by
     then, stale. This is the discovery that led to the re-pin documented above. (One further complication,
     also found and fixed: two of these background runs briefly overlapped after an editing pass, corrupting
     one `redproof.out` with interleaved output from two processes — caught by the garbled formatting,
     the stale process killed, and every subsequent run confirmed single-instance via `ps aux` before trusting
     its output.)
  3. **Fourth run, launched immediately after the re-pin:** FAILS=2 — both attributable to ONE cell (20),
     itself attributable to a real, understood consequence of the re-pin: at the new pin, `ks695` is no
     longer part of the delta between `DEVBASE` (M31, already containing the ks695 union) and the live
     develop tip, so the cell's original tamper (removing `ks695` from `KNOWN_PR_FILES`) had nothing left to
     bite on and the guard correctly read exit 0. Not a guard defect — a test that needed updating for the
     world it now tests.
  4. **Cell 20 rewritten** as a compound tamper (also rewinding `DEVELOP_SHA` to the original M23 pin, where
     `ks695` legitimately IS part of the live-moving delta) and verified standalone before the next full run.
  5. **Fifth run:** FAILS=0 through cell 19b, but the underlying live develop tip HAD ALREADY moved again by
     the time cell 0 ran (`b9f541e6b` → `2c3315f37…`, 1 commit / 6 files, 0 under the guarded directory —
     correctly read as disjoint throughout) — this run is superseded by the sixth, kept as further evidence.
  6. **Sixth run — FINAL, CLEAN: all 22 cells + the 3 byte-stability checks, `FAILS=0`.** Every guard fired
     its designed exit code at every cell, `LANDED` on every tamper, and the launcher/brief/prompt's SHA256
     were unchanged start-to-finish. This is the single, unbroken, end-to-end validation this report ships
     with (`redproof.out`, this run's timestamp is the file's own).
  - **Net assessment:** every guard's logic is now proven correct BOTH individually (across the six runs,
    each guard fired correctly at least once, several many times) AND as a complete, uninterrupted 22-cell
    system (run 6) — against the FINAL, currently-shipped pin.

## NOT DONE

- **No jest/vitest run of any kind, for either PR, at either head** — reserved for the gate, per charter;
  `guards_sim.py` is a prediction, not a substitute.
- **PART 2's launcher/controls_check/redproof coverage is MINIMAL, not full** — added under a ~20-minute
  budget mid-draft, then re-verified (not re-extended) after the #931 re-pin. Specifically NOT done for
  #720: a develop-merge-base guard, a content-judged develop-move guard, tamper-based redproof cells for
  the exit-22 guard, any BACKLOG.md row-set independent verification (F7). `gen_launcher_931.py` was NOT
  extended to generate the #720 pin — the launcher's #720 block was hand-patched directly (documented
  inline) — a good candidate for a follow-up `gen_launcher_L3b.py`.
- **Peter's asks 2-5 for #720** were not independently checked against his source PR comments
  (`5479494525`, `5600892508`).
- **A fresh Linear read for KS-487/KS-657/KS-658** was not run — their comment ids are taken from the
  builder's READY mail only. (KS-1061's own Linear state WAS read, at the superseded-head timestamp; its
  ticket identity/comments are unaffected by which PR head is current.)
- **`tsc --noEmit` rc 0** was not independently re-run for either PR at either head — CLAIMED by the
  builder in both READY mails.

## UNMEASURED, with the instrument that would measure it

- **The whole-originate-suite counts** (58/604 for #931 at the re-pinned head; 48/509 and 57/601 for #720's
  before/after) — instrument: `npx jest` inside a scratch worktree at the given ref, `packages/shared` dist
  rebuilt first. Reserved for the gate.
- **Tamper T5** (the union's discriminator, predicted 10 failed/30 passed/40 total on `ks695` if the
  pass-through override is deleted) — instrument: the same tamper-and-restore discipline this drafter used
  in `guards_sim.py` for T1-T4, extended to T5 with an actual jest run; not built, named for the gate.
- **#720/#931 sequential-merge composability** (F6) — instrument: build develop with #931 merged first (its
  helper-form ks444 factory), then apply #720's 12-line diff on top, run the two 201-cell assertions.

## Anything Wednesday must own

1. **The re-pin is DONE and fully verified green** — `--check` rc=0, `controls_check.sh` FAILS=0 (+3
   negative controls all FAILing as designed), `redproof.sh`'s final clean run FAILS=0 across all 22 cells
   and 3 byte-stability checks, all at `795307023`. No further action needed to launch the gate.
2. **PART 2's guard coverage is intentionally thin** (see NOT DONE) — a QA agent reading PART 2's
   "DELIVERED VS COMMISSIONED" table should expect mostly "CLAIMED only, not independently confirmed" rows;
   this round verified #720's DIFF SHAPES, not its CLAIMED TEST BEHAVIOUR.
3. **A follow-up `gen_launcher_L3b.py`** that generates both PRs' full guard families from one call would
   remove the hand-patch debt PART 2 incurred under time pressure, and would make any THIRD re-pin (should
   #931 or #720 move again) a single command instead of the multi-file manual pass this round required.
4. **F8** (this drafter's own caught-before-shipping error on the own-delta-view git-diff formula) is worth
   a beat of attention only insofar as it is a live instance of the exact class STANDING_LINES already
   documents — no new rule needed, the existing one worked.
