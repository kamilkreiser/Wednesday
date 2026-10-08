Refs KS-1171 — https://linear.app/secuura/issue/KS-1171

Raised from a Wednesday-held Spark pass (`spark_secuura_2026-10-05_KS-1171-b1-boundary-pin`, which
is at REVIEW HOLD and has **no READY artefact** — the run dir holds none, and the ten
`READY_KS-1171*` files in `local-model/night/` all belong to other KS-1171 passes), re-proved on
develop by Seat G 5th. Base `0a6177ea5482`.

## What this is

One new test file pins the **INCLUSIVE** side of rule (c) of the absent-anchor decision at
`services/anchoring/src/anchorSubmission.ts:345`:

```
typeof lastAnsweredElapsedMs === 'number' && lastAnsweredElapsedMs >= ABSENT_MIN_LAST_ANSWER_MS;
```

`ABSENT_MIN_LAST_ANSWER_MS` is `60_000` and `ABSENT_MIN_ANSWERED_POLLS` is `2` (`:170-171`). That
`>=` is the moment at which **a second fee-paying Cardano transaction may be minted**, and nothing
asserted which side of the boundary the constant itself falls on — the comparison could be relaxed
to `>` and every suite would stay green.

Three cells: the last answer **exactly at** the constant (with enough answered polls) reads absent
and schedules the retry; one millisecond earlier does not; and the two constants read their ruled
values.

**No product code changes.** `anchorSubmission.ts` is byte-identical before and after, by whole-file
sha256. This guards a money path and adds coverage only.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/anchoring/src/__tests__/ks1171-b1-absent-boundary-is-inclusive.test.ts` —
  NEW, 96 lines, 4,296 B, mode 100644, sha256/16 `f2e97786cd943561`
- `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` — flow block
  `40.` appended (SKILL §4)
- `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` — one cheat section appended
- 3 files, +234, 0 trailers, parent = base `0a6177ea5482`

**Ran**
- **Why there is no red at the base:** a pin passes the moment it is written, so quoting a green as
  a red-to-green would be a false claim. The honest red is a **reverted tamper**. The anchor string
  was proved **unique (`grep -c` = 1, control `ABSENT_MIN_LAST_ANSWER_MS` = 2)**, `>=` was changed to
  `>` at `:345`, and the file was restored by content with **whole-file sha256/16 `310b2befe5cf4ce6`
  asserted identical to the pre-tamper hash**, `cmp` rc 0 against a kept copy, and `git diff` rc 0 on
  that path. The tamper was never staged and never committed.
  - under the tamper: **1 failed / 2 passed (3)**, rc 1, failing on exactly the boundary assertion,
    with **both control cells green** — which is what makes it an assertion rather than a load
    failure. A `0 total / 0 failed` reading would have proved nothing.
  - restored: **3 passed (3)**, rc 0.
- Whole `services/anchoring` suite through its own `npm test` (`vitest run`):
  **28 files, 1 failed / 361 passed (362)** at the base → **29 files, 1 failed / 364 passed (365)**
  at this head. +3 tests, and the **same single failure on both sides**.
  - That failure is **not ours**: `threadTokenMint emulator round-trip`
    (`Could not serialize the data: Unsupported type`, inside `@lucid-evolution/plutus`). It is
    develop's own pre-existing red, recorded at `BACKLOG.md:182` under KS 562. **Attributed, not
    claimed, not fixed here.** The new-red set for this PR is **empty**.
- `npx tsc --noEmit -p services/anchoring`: rc 0, 0 lines.
- Pre-push hook, from this push's own log:
  - `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`
  - `OK — 13 code guards passed.`
  - `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`
  - `legs 3 4 8 — local stack not up; you can clear this by starting it.`
  - A `VERDICT: MISMATCH — STOP` string appears in the run. It is **not a failure**: it is a fixture
    control arm inside `Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh:459-460`, which runs
    a fixture with a deliberate header mismatch and asserts the verdict is `HEADER-MISMATCH/1`. The
    enclosing suite reports `5 passed, 0 failed`.
- Doc blocks verified by `docblockra3.py`, **0 failed**: flow tail `26.` → `40.` (30 → 31 blocks,
  order otherwise unchanged and ascending), cheat tail `KS 1164` → `KS-1171` (19 → 20 sections), and
  on both docs *"THE ONLY difference from the blob at --base IS this fragment, byte for byte"* — with
  a 1-byte-altered fragment failing the same comparison and a one-character edit to block 1 detected
  by the second reading. (`html_docs_matrix.test.sh` tallies are **not** quoted as evidence of a
  well-formed block; they cannot fail on an unbalanced tag.)
- Environment, read from `node_modules` rather than assumed: **vitest 4.1.11** agreeing two ways
  (`node_modules/vitest/package.json` and `vitest --version` →
  `vitest/4.1.11 darwin-arm64 node-v24.7.0`), **node v24.7.0**, **npm 11.5.1**, Darwin 27.0.0 arm64.
- Install: `npm ci --ignore-scripts` in `Blockchain/Dev` (1,937 packages) then
  `npm run build --workspace=packages/shared` with `packages/shared/dist/index.js` **asserted
  present at 17,746 B** (absent beforehand — `npm ci --ignore-scripts` builds nothing), plus
  `npm ci` in all four of `systemTest/{akto,api-explorer,performance,playwright}`.
  `systemTest/package.json` itself declares no dependencies and has no lockfile, so `npm ci` there
  would refuse and was not run.

**NOT run**
- **The four platform suites (Schemathesis, Akto, Playwright, performance/k6) are UNMEASURED, not
  passing.** There is no local stack on `http://localhost:6882`; the only evidence quoted is the
  push's own SKIP line naming legs 3, 4 and 8.
- **A live sweep is still owed on KS-1171 itself.** This PR settles gate finding B1 of #1228 only;
  the 8k item and the live sweep remain owed, and **the ticket does not move to Done.**
- `systemTest/{akto,performance,playwright}` declare `engines.node >= 24.11.0` while this host runs
  **v24.7.0**. Recorded, not worked around.
- One transient worth naming rather than smoothing over: the **first** full-suite run after the new
  file was added also reported `db.retry.test.ts > reports available immediately when the probe
  succeeds at boot` as `Error: Test timed out in 5000ms`. It was not called flaky on a hunch — that
  file passes **5/5 alone** on the same tree, the **second** full-suite run is clean, and
  `BACKLOG.md:1182` already documents the identical cold-transform symptom for `services/kyc`. This
  is its first recorded sighting in `services/anchoring`.
- One gate control in this round's tooling is **vacuous for this PR** and is reported as such rather
  than banked: the path gate's "an allowed path inside the PR 0 control range is still counted" arm
  runs over an empty generator here, because this PR's declared set has no intersection with PR 0's
  files. Its ability to fire was proved separately on a constructed run.

**Migrations + config**
- None. No migration, no dependency, lockfile, manifest, baseline or spec-version change. `git status`
  after install showed 0 tracked files modified.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
