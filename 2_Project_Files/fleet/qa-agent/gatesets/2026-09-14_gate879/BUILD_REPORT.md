# BUILD REPORT — QA gate set for Secuura/Blockchain PR #879 (KS-945), TIER 2, ROUND 2

Drafter: Wednesday-assistant DRAFTING subagent (Sonnet), 2026-09-14 ~18:10–18:35 AEST. One of three gate
sets built in this commission (siblings: `2026-09-14_gate988/` for PR #988, `2026-09-14_gate874/` for
PR #874). Nothing launched, nothing committed, nothing mailed. The Secuura checkout was touched with READ
verbs only (`ls-remote`, `log`, `show`, `diff`, `diff --numstat`, `ls-tree`, `merge-base`, `cat-file`)
against the existing read-only checkout at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`;
no `fetch`/`checkout`/`worktree`/`merge-tree` anywhere.

## FOUND

- PR #879 (KS-945), branch `kamilkreiser/ks-945-install-detector-fail-closed`, base `develop` M38
  `0e78c7270188ac45c1c29f927bdf90728f10215d`. Head `0374bec007d09d62afd8596d3d15abeead0526b9`, a 4-commit
  chain confirmed directly (`git log --format='%H %P %cI %s'`): `79f1fcb48` (original, Peter's approved
  head) → `238f8ada0` (Peter's two asks built) → `f1803166f` (`--no-ff` merge of develop `2d864ae92`,
  carries the leg-14 `GIT_*` strip #953) → `0374bec00` (`--no-ff` merge of develop M38). Confirmed
  `git merge-base --is-ancestor 79f1fcb48… 0374bec00…` rc 0 — the origin push is a genuine FAST-FORWARD;
  Peter's line-cited approved head stays in the branch's own history.
- Diff vs develop M38 = exactly 2 files (`git diff --name-only`, `--numstat`, `ls-tree`, independently
  re-derived, matching the builder's own claim): `Blockchain/Dev/scripts/check-shared-relink.sh` (+77 −7)
  and `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh` (+191 −0). Control row
  `audit-baseline.json` confirmed identical (`03d1680e3…`) at both the head and develop M38. The head's
  two blobs (`d41c79538`, `867ce728a`) are confirmed BYTE-IDENTICAL to `f1803166f`'s own two blobs
  (`git ls-tree`) — the M38 merge-in changed nothing in either lane file, as predicted.
- Read the full `check-shared-relink.sh` diff directly: the new `pm_writes(L)` function (`:169`), the
  probe-regex allowance (`:195`) sitting ahead of the default-verb rule, the read-only allowlist (`:203`),
  and confirmed the OLD enumerating rule (`npm[ \t]+(ci|install|i)…`) is gone at head, present at develop.
  Read the suite's five new `expect` cells at their exact line numbers (`:1154`, `:1169`, `:1178`,
  `:1187`, `:1199`) — all match Peter's two asks and the builder's claims exactly.
- Built a LEGITIMATE SHAPES table (brief §2a, required — this target is a checker) covering 13 rows: every
  ordinary RUN-line shape a real Dockerfile produces, both defect classes the guard exists to catch, both
  of Peter's round-2 asks, and the four residual false-clean shapes (Peter's finding 4, explicitly NOT
  fixed by this PR and routed to KS-930) — each traced to its exact clause in `pm_writes` at the head.
- The builder's (s229) full Test Evidence and NOT-covered block — read from `ready_879.txt` — quoted
  verbatim in the brief.

## TESTED / HOW

- **`--check` against the LIVE current develop tip and the live PR head**, run at close-out (~18:33 AEST):
  **rc 0**. **Develop MOVED live during this drafting session** (M38 `0e78c7270…` →
  `e86bffee0f10809db30b8e0c08994f66ace96232`, 1 commit, 4 files) — a real, unplanned exercise of the
  content-judgement mechanism, not a synthetic test: the launcher correctly judged the move DISJOINT from
  the two guarded paths and proceeded (rc 0), printing the move and its judgement rather than either
  silently ignoring it or spuriously refusing. See the final `check.out`.
- **`controls_check.sh`** (`controls_check.out`): fetches both files at both the head and develop via the
  GitHub contents API, asserts every blob against the table, the audit-baseline identity, the `pm_writes`
  function and its three key clauses at the head (absent at develop), the OLD enumerating rule's presence
  at develop / absence at head, and all five of the suite's new `expect` cells by their exact literal text
  (including the escaped-backtick case-name convention the suite itself documents — `\`npm run build\``,
  not `` `npm run build` ``, since the source is a double-quoted bash string). **First run clean, FAILS=0
  — no anchor-wording corrections were needed** (unlike gate988's authoring pass), because every anchor
  was copied directly from `git show` output rather than re-typed from memory.
- **`redproof.sh`** (`redproof.out`, work dir kept at `redproof.EflhKp/`): **22 cells (0–20, 8b, 21),
  FAILS=0.** Every guard the launcher declares fires at its own distinct exit code
  (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22) plus `0` (green first and green again, pristine
  sha-identical). **Two cells needed real debugging during authoring, both found and fixed live:**
  - **Cell 8b** (proving the develop content-judgement branch runs on live data, not just "still pinned"):
    the first attempt re-pinned `DEVELOP_SHA` to the PR's own merge-base (`2d864ae92`, 119 commits / 382
    files back) — measured live, this tripped the launcher's OWN `len(files) > 250` UNJUDGEABLE cap
    (GitHub's compare API response paginates past 300 files), producing exit 18 instead of the intended
    0. Corrected to develop's immediate parent (M37 `54e9b835d`, ONE commit / 2 files to M38, neither a
    guarded path) — confirmed disjoint live before folding into the kept script. This is a genuine
    property of the launcher (a very large disjoint move is UNJUDGEABLE and refuses safely rather than
    guessing), not a bug — the fix was to the redproof CELL's choice of test data, not the launcher.
  - **Cell 17** (`NEVER print a credential value` missing from prompt → expect exit 17): the first live
    run got exit 13 (`UNREADABLE TimeoutError` from the GitHub compare API) instead of 17 — a transient
    network timeout under ~20 rapid successive live API calls in one redproof pass, not a defect in the
    guard order. Re-ran the full suite after the cell-8b fix; the retry passed cleanly at exit 17 as
    designed. No code change was needed for this cell; noted here so a future re-run that hits a flake
    is read as network noise, not a regression, unless it recurs.
- **Raw-control-byte census**: 0 across all five text/script files; the synthetic NUL positive control
  fires at its expected offset (`[16]`).
- **`bash -n`**: clean on the launcher.

## CAVEATS

- The head may move a third time before real launch (a further round from Peter, or a squash) — the
  `HEAD_SHA` one-line mechanism is the designed remedy; `AHEAD_WANT`/`FILES_WANT` must be checked
  alongside it if the commit/file count changes.
- Live GitHub API calls under rapid repetition can time out transiently (observed once during this
  authoring pass, at cell 17 of the first redproof run) — a lone timeout on re-run is noise; a
  reproducible one is a finding.
- The suite (106/0/0), the real-tree census (25/25 both modes), `npm run test:shell` (30/30), and the
  LEGITIMATE SHAPES table's live-fixture exercise were NOT run by this drafter (drafting a gate set is not
  running the gate itself) — they are commissioned for the QA seat to run at launch time, in its own
  worktree, after confirming the KS-1086 strip is an ancestor (brief item 6).

## PINS (re-read live at close-out, ~18:33 AEST)

- Head: `0374bec007d09d62afd8596d3d15abeead0526b9` (`git ls-remote origin refs/pull/879/head` and the
  branch ref — identical).
- Base (as pinned in the brief/launcher): develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`.
- Compare: `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=4 files=2` (GitHub compare API, live).
- **DEVELOP MOVED DURING THIS DRAFTING SESSION** to `e86bffee0f10809db30b8e0c08994f66ace96232` (1 commit,
  4 files) — judged DISJOINT from the two guarded paths by the launcher's own live `--check`, rc 0.

## `--check` RETURN CODE: **0** (live develop tip — now one commit past M38 — live PR head, no env overrides; the move was judged DISJOINT and re-stated, not silently ignored).

## Deliverables (this dir → install targets)

| file | install target |
|---|---|
| `2026-09-14_secuura-879-ks945-tier2-r2.md` | `fleet/qa-agent/briefs/2026-09-14_secuura-879-ks945-tier2-r2.md` |
| `2026-09-14_secuura-879-ks945-tier2-r2.prompt.txt` | `fleet/qa-agent/briefs/2026-09-14_secuura-879-ks945-tier2-r2.prompt.txt` |
| `launch_qa_secuura_879_ks945.sh` | `fleet/qa-agent/launchers/launch_qa_secuura_879_ks945.sh` |
| `controls_check.sh` (+ `controls_check.out`: FAILS=0) | this set |
| `redproof.sh` (+ `redproof.out`: 22 cells [0–20, 8b, 21], FAILS=0; work dir `redproof.EflhKp/`, kept) | this set |
| `model/` — fetched-bytes copies from `controls_check.sh`'s own run | this set |
| `check.out` (final `--check`, rc 0, live develop move observed and judged DISJOINT) | this set |
| `SHA256SUMS.txt` — sha256 of every other top-level file in this set | this set |

**Not installed** — every path above is the eventual install target. The launcher's `BRIEF`/
`PROMPT_FILE`/`REAL_BRIEF` defaults currently point at THIS gateset directory (not the central one), so
`bash launch_qa_secuura_879_ks945.sh --check` passes rc 0 right now, in place, without an install step
first. **Install (when Wednesday is ready):** copy the brief + prompt into `briefs/`, the launcher into
`launchers/`, re-point the three path constants at the top of the launcher to the central `briefs/`
location, re-run `--check` once more to confirm, then:

```
cockpit.sh add "QA/Secuura-879" "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_879_ks945.sh"
```
