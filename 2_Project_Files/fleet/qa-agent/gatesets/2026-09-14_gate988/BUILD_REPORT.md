# BUILD REPORT — QA gate set for Secuura/Blockchain PR #988 (KS-704), TIER 2, ROUND 1

Drafter: Wednesday-assistant DRAFTING subagent (Sonnet), 2026-09-14 ~18:05–18:25 AEST. One of three gate
sets built in this commission (siblings: `2026-09-14_gate879/` for PR #879, `2026-09-14_gate874/` for
PR #874). Nothing launched, nothing committed, nothing mailed. The Secuura checkout was touched with READ
verbs only (`ls-remote`, `log`, `show`, `diff`, `diff --numstat`, `ls-tree`, `merge-base`, `cat-file`)
against the existing read-only checkout at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`;
no `fetch`/`checkout`/`worktree`/`merge-tree` anywhere.

## FOUND

- PR #988 (KS-704), branch `feature/ks-704-k6-gate-reports-a-failure-rate-with-no-status-code-breakdown`,
  base `develop` M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`. ONE commit, head
  `8cb99a002c5177bb1418ee1fab7cd2974076989a` — confirmed live at origin by `ls-remote`; develop unmoved
  since M38 (also confirmed live).
- Diff vs develop M38 = exactly 4 files (`git diff --name-only`, `--numstat`, `ls-tree`, independently
  re-derived, matching the builder's own +287 −10 total exactly): `systemTest/performance/gate/report.ts`
  (+108 −8), `systemTest/performance/gate/cli.ts` (+1 −1, the one call-site line at `:92`),
  `systemTest/performance/tests/unit/gate/reportFailedGateBreakdown.test.ts` (new, +166),
  `systemTest/performance/docs/quick-start.md` (+12 −1).
- Read the full `report.ts` and `cli.ts` diffs and the new test file's content directly (`git diff`,
  `git show` at both SHAs) — confirmed `STATUS_CODE_COUNTERS` (`report.ts:40`), `isHttpRateGate`
  (`:78`), `formatStatusCodeBreakdown` (`:98`), `printGateLines` (`:216`), the `cli.ts:92` one-line
  change, and the new test file's exactly 4 `it(` cells (confirmed by `git show` + `grep`, not by
  trusting the READY mail's count) — all match the builder's claims.
- Read the fixture `tests/unit/fixtures/smoke-summary.json` at the head directly: `http_rate_limited`
  passes=0/fails=28, `http_req_failed` passes=0/fails=37, `http_server_error` passes=0/fails=28,
  `http_503` passes=0/fails=28 — these are the exact numbers the new test file's assertions and this
  brief's controls_check.sh tokens depend on; independently confirmed, not copied from the READY mail.
- The builder's (s227) full Test Evidence, tamper table, and NOT-covered block — read from `ready_988.txt`
  AND its correction `corr_988.txt` (07:13:27Z — the original READY's merge-order file-name list was lost
  to an unquoted heredoc; the correction is what the brief quotes) — quoted verbatim in the brief.

## TESTED / HOW

- **`--check` against the LIVE current develop tip and the live PR head** — run fresh at close-out
  (18:1x AEST): **rc 0**, "all guards pass," 11 guard lines, reading `compare: mb=0e78c7270… ahead=1
  files=4` and `origin develop still 0e78c7270… (M38; git ls-remote)`. See `check.out`.
- **`controls_check.sh`** (`controls_check.out`): fetches all 4 files at both the head and develop via the
  GitHub contents API (`GH_TOKEN` sourced by name from the Secuura `.env`, never printed), asserts every
  blob against the table, re-derives the `report.ts`/`cli.ts` anchors (the four new symbols, the `if (name
  === 'http_req_failed')` relabel branch, the three `STATUS_CODE_COUNTERS` table rows, the one-line
  `cli.ts` call-site both ways), the new test file's 4 cells and its key assertion strings, and the doc
  sample block's exact text. **Two anchor mismatches were found and fixed during authoring** (both false
  positives from an over-broad literal-string match, not defects in the PR):
  - `'metrics: K6Summary'` matched **4** times, not 1 (the type appears in four function signatures) —
    narrowed the anchor to the specific default-parameter form `"metrics: K6Summary['metrics'] = {}"`,
    which is unique to `printReport`'s signature.
  - `"it('"` matched **5** times, not 4 — the substring `it('` also occurs inside `.split('\n')` (the
    tail of "spl**it('**\n')"). Narrowed the anchor to `"    it('"` (the 4-space test-body indent), which
    only matches actual `it(` test declarations.
  Both fixes verified live; final run **FAILS=0, rc 0**.
- **`redproof.sh`** (`redproof.out`, work dir kept at `redproof.0Vg3AC/`): **26 cells (0–23, 25, 26; cell
  24's number retired, matching the gate916/gate919 convention), FAILS=0.** Every guard the launcher
  declares fires at its own distinct exit code (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,22) plus
  the natural `127` at the exec line with `claude` absent from PATH, plus `0` (green first and green
  again, pristine sha-identical). Built directly from the gate916 exemplar's `redproof.sh` template with
  variable substitution only (env-var prefix `QA988_*`, `AHEAD_WANT=1`/`FILES_WANT=4`, the
  `systemTest/performance/` guarded-prefix wording) — no template-mechanism bugs were found this time
  (gate916's authoring pass had already found and fixed the exit-13/exit-18 issues this template now
  encodes correctly).
- **Raw-control-byte census**: 0 across all five text/script files; the synthetic NUL positive control
  fires at its expected offset (`[16]`).
- **`bash -n`**: clean on the launcher.

## CAVEATS

- The head may move before real launch — the `HEAD_SHA` one-line mechanism (launcher, near the top) is
  the designed remedy; `FILES_WANT`/`AHEAD_WANT` must be checked alongside it if the commit/file count
  changes. Redproof cell 25 exercises this substitution point directly and confirms it works.
- `controls_check.sh`'s `model/` copies are the fetched-bytes record from THIS authoring pass — if the
  head re-pins, they should be refreshed by re-running `controls_check.sh` (it writes into `model/` on
  every run).
- The unit suite, the k6-run reachability probe, lint/knip/format:check, and the golden-file identity
  named in the brief were NOT run by this drafter (drafting a gate set is not running the gate itself,
  per every prior exemplar's own convention) — they are commissioned for the QA seat to run at launch
  time.

## PINS (re-read live at close-out, ~18:33 AEST)

- Head: `8cb99a002c5177bb1418ee1fab7cd2974076989a` (`git ls-remote origin refs/pull/988/head` and the
  branch ref — identical).
- Base (as pinned in the brief/launcher): develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`.
- Compare: `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=1 files=4` (GitHub compare API, live).
- **DEVELOP MOVED DURING THIS DRAFTING SESSION** (M38 → `e86bffee0f10809db30b8e0c08994f66ace96232`,
  1 commit, 4 files — read live at close-out, ~18:33 AEST) — a real, unplanned exercise of the launcher's
  content-judgement mechanism, not a synthetic test. The launcher's `--check` correctly judged the move
  DISJOINT from `systemTest/performance/` (this PR's only guarded prefix) and returned **rc 0**, printing
  `origin develop MOVED … disjoint from systemTest/performance/ …` rather than refusing — see the final
  `check.out`. This is the mechanism working exactly as designed and documented in the brief's
  KNOWN-FRAGILE section, observed live rather than only red-proofed.

## `--check` RETURN CODE: **0** (live develop tip — now one commit past M38 — live PR head, no env overrides; the move was judged DISJOINT and re-stated, not silently ignored).

## Deliverables (this dir → install targets)

| file | install target |
|---|---|
| `2026-09-14_secuura-988-ks704-tier2.md` | `fleet/qa-agent/briefs/2026-09-14_secuura-988-ks704-tier2.md` |
| `2026-09-14_secuura-988-ks704-tier2.prompt.txt` | `fleet/qa-agent/briefs/2026-09-14_secuura-988-ks704-tier2.prompt.txt` |
| `launch_qa_secuura_988_ks704.sh` | `fleet/qa-agent/launchers/launch_qa_secuura_988_ks704.sh` |
| `controls_check.sh` (+ `controls_check.out`: FAILS=0) | this set |
| `redproof.sh` (+ `redproof.out`: 26 cells [0–23, 25, 26; cell 24 retired], FAILS=0; work dir `redproof.0Vg3AC/`, kept) | this set |
| `model/` — fetched-bytes copies from `controls_check.sh`'s own run | this set |
| `check.out` (final `--check`, rc 0) | this set |
| `SHA256SUMS.txt` — sha256 of every other top-level file in this set | this set |

**Not installed** — every path above is the eventual install target. The launcher's `BRIEF`/
`PROMPT_FILE`/`REAL_BRIEF` defaults currently point at THIS gateset directory (not the central one), so
`bash launch_qa_secuura_988_ks704.sh --check` passes rc 0 right now, in place, without an install step
first. **Install (when Wednesday is ready):** copy the brief + prompt into `briefs/`, the launcher into
`launchers/`, re-point the three path constants at the top of the launcher to the central `briefs/`
location, re-run `--check` once more to confirm, then:

```
cockpit.sh add "QA/Secuura-988" "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_988_ks704.sh"
```
