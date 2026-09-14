# BUILD REPORT — QA gate set for Secuura/Blockchain PR #919 (KS-739) — ci: originate route + spec, TIER 2, ROUND 1, ONE VERDICT

Drafter for Wednesday, 2026-09-14 ~07:05–17:34 AEST (an interrupted first pass wrote the brief and prompt; this
drafter completed the launcher, controls_check.sh, redproof.sh, and this report, then re-verified everything
against live state before closing).

Nothing launched, nothing mailed, nothing installed, nothing committed. The Secuura checkout was touched with
READ verbs only (`ls-remote`, `log`, `show`, `diff`, `ls-tree`, `merge-base` — all via the existing read-only
checkout at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`); no `fetch`/`checkout`/`worktree`/
`merge-tree --write-tree` was used anywhere. Every write this session made lives under
`gatesets/2026-09-14_gate919/`. Nothing deleted.

## FOUND

- PR #919 (KS-739), branch `feature/ks-739-transfer-custody-maps-a-401403-from-userslookup-to-502`, head
  `4736e22771c12e56d004f58a67f960ddbc0b0508` — a `--no-ff` merge of the PR's own 09-09 commit and develop M38,
  `check:openapi` passing rc 0 directly on the merged tree (no regeneration commit needed).
- Base: origin develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`. Live compare (`develop...head`):
  `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=2 files=4` (measured, not assumed — the brief's earlier
  guess of `ahead=4` was WRONG and was corrected against the live GitHub compare API before the launcher's
  `--check` was ever run green).
- The four files, their blobs and numstat, and the audit-baseline control row, all independently re-derived via
  `git diff --name-only`/`--numstat` and `git ls-tree` in the checkout — matches the s226 READY mail
  (`ready_919.txt`) exactly.
- Peter's ask for the gate: a targeted Schemathesis pass on `postDocumentsByIdTransferCustody`
  (`POST /api/documents/{id}/transfer-custody`, the yaml's only operation on that path, confirmed at
  `Blockchain/Dev/docs/openapi/secuura-api.yaml:28481-28570` at the head).

## TESTED / HOW

- **The Schemathesis targeting mechanism** — read `systemTest/schemathesis/scripts/runner/args_builder.py`,
  `cli.py`, and `config/schemathesis_tests.yaml` at the head (READ ONLY). `args_builder.py`'s `_filter_args`
  supports `--include-path-regex` / `--exclude-path` / `--exclude-path-regex` / `--include-by` / `--exclude-by`
  (KS-270/KS-544); `schemathesis_tests.yaml:256-259` states explicitly: *"This block is RUN-LEVEL … If a
  setting should affect ONE endpoint, it does NOT belong here — put it in `schemathesis.toml` under
  `[[operations]] include-name = "<METHOD /path>"`, which is the only place Schemathesis supports per-operation
  scoping."* The brief instructs the gate to use the precedented `--include-path-regex` mechanism
  (`^/api/documents/[^/]+/transfer-custody$`, the KS-270 pattern narrowed to one path — this path carries
  exactly one operation, so a path-regex and a per-operation `include-name` scope achieve the same practical
  effect) via the `pr` profile, but to verify the exact flag itself against the LIVE `args_builder.py` at gate
  time (versions/behaviour can drift) rather than trust this drafter's read. The brief requires probing
  reachability (`curl --max-time 5` against the resolved base URL) BEFORE ever writing NOT RUN — the gate must
  not simply repeat the builder's HOLD claim.
- **`launch_qa_secuura_919_ks739.sh`** — guard family adapted from `gate912r2`/`gateL9`: dir/file existence
  (exit 2-5), head-at-branch via `ls-remote` (exit 6), GitHub compare API match (exit 10/13), develop judged BY
  CONTENT using the `DEV_CONTENT_ALLOWED`/`LANDED_OK` pattern from gate912r2 (exit 18 GUARDED / exit 19
  LANDED-moot / rc 0 disjoint), brief/prompt tier+round agreement (exit 7/15), `ultrathink`-first-line (exit 8),
  brief-path-named (exit 9), head-SHA-in-both (exit 20), MAIL-YOUR-VERDICT / never-push / no-memory /
  never-print-credential lines present (exit 12/11/14/17), env-override refusal (exit 16), no-TTY refusal on a
  real launch (exit 21). `bash -n` clean. GH_TOKEN sourced by NAME from
  `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, never printed.
- **`controls_check.sh`** (`controls_check.out`): fetches all 4 files + the audit-baseline control row at both
  the head and develop via the GitHub contents API (falling back to the git blobs API for the 1.3MB yaml, which
  the contents API's inline-content field cannot carry — this was caught and fixed during authoring: the first
  run produced 0-byte yaml files). Asserts every blob against the table, the fetched bytes against `model/`
  copies, the route-change anchors (`RECIPIENT_LOOKUP_FAILED` count 1, the class-branch condition count 1, both
  absent on develop), the yaml's `KS-739` count (3) and `verify-file` count (0, until #813 lands), the
  operation-id present both sides, the PII at-sign control (95 hits elsewhere in the yaml, proving the grep is
  live), and a raw-control-byte census with a synthetic NUL positive control. **Result: FAILS=0, rc 0.**
- **`redproof.sh`** (`redproof.out`, work dir kept at `redproof.ffFEog/`): **22 cells (0–21), FAILS=0.** Every
  guard the launcher declares fires at its own distinct exit code (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,
  19,20,21) plus 0 (green first and green again, pristine sha-identical). Three cells needed real debugging
  during authoring:
  - Cell 7 (a nonsense `DEVELOP_SHA`) was first predicted to trip the develop-content guard (exit 18); measured,
    it instead broke the compare-API call itself (the bogus SHA is unresolvable) — exit 13. Corrected to the
    measured behaviour rather than the prediction.
  - Cell 8 (re-pinning `DEVELOP_SHA` one commit back to M37, to reach the develop-content-judgement branch at
    all under a currently-unmoved live develop) required `CMP_WANT` re-aimed to the LIVE, measured
    `develop(M37)...head` compare (`mb=M37 ahead=2 files=4` was wrong; the real value is `ahead=2 files=4`... —
    corrected via a live probe to the actual `mb=54e9b835d… ahead=2 files=4`) before the develop-guard could be
    exercised at all.
  - Cells 8b/8c: widening `GUARDED` to include `BACKLOG.md` (one of the two real M37→M38 delta files) exercises
    the GUARDED arm (exit 18) un-cleared, and additionally registering it in `LANDED_OK` at its REAL, measured
    M38 blob (`dca47caa155e3f743ad401fc62a56618ec6f47fa`, read via `git ls-tree`) exercises the LANDED arm (exit
    19) — on real, live data rather than a fabricated scenario, since #919's own four files have not (yet)
    landed into develop for a live exit-19 to occur naturally.
- **`--check` against the LIVE current develop tip and the live PR head**, run fresh as the final close-out
  step (17:34 AEST): **rc 0**, "all guards pass," 11 guard lines, reading `compare: mb=0e78c7270… ahead=2
  files=4` and `origin develop still 0e78c7270… (M38, git ls-remote)`.

## PINS (re-read live at 17:34 AEST close-out; all agree with the READY mail and the s226 brief)

- Head: `4736e22771c12e56d004f58a67f960ddbc0b0508` (`git ls-remote origin refs/pull/919/head`).
- Base: develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d` (`git ls-remote origin refs/heads/develop`) —
  unmoved throughout this drafting session.
- Compare: `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=2 files=4` (GitHub compare API, live).

## `--check` RETURN CODE: **0** (live develop tip, live PR head, no env overrides).

## Deliverables (this dir → install targets)

| file | install target |
|---|---|
| `2026-09-14_secuura-919-ks739-tier2.md` | `fleet/qa-agent/briefs/2026-09-14_secuura-919-ks739-tier2.md` |
| `2026-09-14_secuura-919-ks739-tier2.prompt.txt` | `fleet/qa-agent/briefs/2026-09-14_secuura-919-ks739-tier2.prompt.txt` |
| `launch_qa_secuura_919_ks739.sh` | `fleet/qa-agent/launchers/launch_qa_secuura_919_ks739.sh` |
| `controls_check.sh` (+ `controls_check.out`: FAILS=0, rc 0) | this set |
| `redproof.sh` (+ `redproof.out`: 22 cells, FAILS=0; work dir `redproof.ffFEog/`, kept) | this set |
| `model/` (fetched-bytes copies the controls check compares against) | this set |
| `check.out` (final `--check`, rc 0) | this set |
| `SHA256SUMS.txt` (sha256 of every top-level file in this set) | this set |

**Not installed** — every path above is the eventual install target, per the exemplar sets' own convention
(gateL9's `BUILD_REPORT.md` names the same central `briefs/`/`launchers/` targets without copying). The
launcher's own `BRIEF`/`PROMPT_FILE`/`REAL_BRIEF` defaults currently point at THIS gateset directory (not the
central one), so `bash launch_qa_secuura_919_ks739.sh --check` passes rc 0 right now, in place, without
requiring an install step first. **Install (when Wednesday is ready):** copy the brief + prompt into `briefs/`,
the launcher into `launchers/`, re-point the three path constants at the top of the launcher to the central
`briefs/` location, re-run `--check` once more to confirm, then:
`cockpit.sh add "QA/Secuura-919" "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_919_ks739.sh"`

## NOT DONE / could not do

- No actual Schemathesis run, jest run, tsc run, or eslint run of any kind — this is a drafting/build pass over
  the gate SET (the brief, launcher, and its own verification scripts), not the gate itself. The gate's
  in-session test execution is the QA agent's job when launched.
- Did not install to the central `briefs/`/`launchers/` directories (not commissioned; explicitly out of scope
  for this drafting task).
- Did not re-read Linear or GitHub PR comments beyond what the READY mail and the s226 lane brief already
  quote — the git-level facts (diff, blobs, numstat, compare) were independently re-derived; the narrative facts
  (Peter's comments, the ticket state) were taken from the already-quoted sources and not re-fetched from
  Linear/GitHub APIs beyond the PR-files/compare calls needed for the launcher and controls_check.sh themselves.

## UNMEASURED (with the instrument that closes each)

- Whether the exact Schemathesis flag (`--include-path-regex` vs a native `--include-operation-id`) resolves
  cleanly against the pinned schemathesis version at gate time — closed by the gate's own read of
  `args_builder.py`/`cli.py` immediately before running, per the brief's explicit instruction.
- Whether develop moves again before real launch, and whether it moves under a GUARDED path — the launcher's
  `--check` re-reads it at install time and at the start of the real run; a disjoint further move passes and is
  re-stated, a GUARDED-path move refuses (exit 18) unless content-cleared, and a move that lands one of #919's
  own four files at its own head blob refuses as moot (exit 19).

## Anything I must own

- The compare API's real `ahead_by` for `develop...head` is **2**, not 4 as an early draft of the brief
  guessed before this drafter checked it live — corrected in the launcher's `CMP_WANT` and verified green; the
  brief itself states the number correctly (§TARGET, "The files, by blob") and was not affected.
- The interrupted first pass (whoever/whatever wrote the brief and prompt before this drafter continued) left
  genuinely solid, complete work — both files needed no correction, only completion of the remaining
  deliverables.
