Refs KS-1139
https://linear.app/secuura/issue/KS-1139

Raised from a Wednesday-held Spark pass, re-proved by Seat R 19th on develop `0a6177ea5482`.

## What this changes

`pass()`, `fail()` and `warn()` in `Blockchain/Dev/scripts/smoke-test.sh` counted with
`((PASS++))`. A post-increment from **0** evaluates to 0, so the arithmetic command returns
**status 1**. The script runs under `set -euo pipefail`, and bash **4.1 and later** apply errexit to
`(( ))` — so on a Linux runner or the Ubuntu demo VM the script **died at its first check** and
printed nothing after it. macOS `/bin/bash` **3.2.57**, which this host ships, ignores that status,
which is why it passed locally and was still unusable as a deploy check. All three helpers now use
`X=$((X + 1))`, which never returns non-zero.

**Ruled deviation from the payload, recorded here as required.** The payload applies byte-for-byte;
in the same commit it gains one WHY comment above `pass()` naming the prior behaviour, and a single
ticket-reference line in the new suite's header. Nothing else changed. Payload 6,754 B,
sha256/16 `48b01b8cb87e16d7`; its tree at the base reproduced `70a196f6e368` exactly before the two
additions.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/smoke-test.sh`, a new
`Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh`, and both platform-k
HTML docs (flow block `37.`, cheat section for this ticket) in the same commit, per SKILL §4.

**Ran, on this branch, by the author:**

- **Red-first, SKILL §5b.** With `smoke-test.sh` reverted to the base and the new suite kept:
  **3 passed, 3 failed, rc 1**. With the fix: **6 passed, 0 failed, rc 0**. The three cells passing
  in *both* arms are the controls — a degraded run still counts, a down service still fails — and the
  total staying at **6** across both arms is what shows the cells executed rather than the suite
  failing to load. The product file was then restored and re-verified `cmp`-identical (with a 1-byte
  tamper proving `cmp` can fail), and the green re-run reproduced 6/0.
- **Sibling suite, unchanged:** `smoke_test_degraded_warns.test.sh` — **5 passed, 0 failed, rc 0**.
- **`bash -n` clean on both files AFTER the two additions**, and the three anchors
  `^pass() { ` / `^fail() { ` / `^warn() { ` each still read exactly 1.
- **S-1:** `npm ci --ignore-scripts` in `Blockchain/Dev` rc 0; `npm run build --workspace=packages/shared`
  rc 0 with `dist/index.js` asserted present (17,746 B); `npm ci` in all four of
  `systemTest/{akto,api-explorer,performance,playwright}`, rc 0 each.
- **Doc blocks:** appended by tool with a byte-for-byte read-back — **0 failed**, including "THE ONLY
  difference from the blob at the base IS this fragment, byte for byte" for both documents, both
  1-byte-altered-fragment controls correctly failing, and all 30 / 19 pre-existing blocks re-read
  byte-identical.
- **Committed modes, read from the tree** (a mode-delta *diff* check is vacuous here because
  `core.filemode=false` — a deliberate `chmod` on a tracked 100644 file also shows zero mode lines,
  which I verified): `smoke-test.sh` **100755**, the new suite **100644**, matching its sibling
  `smoke_test_degraded_warns.test.sh`. Preflight leg 10 checks only scripts invoked by bare path from
  a `package.json` script, which this suite is not — read at source in
  `scripts/preflight/bare-path-scripts-executable.sh`, not assumed.

**Versions, read from `node_modules` rather than memory:** node `v24.7.0`, npm `11.5.1`,
`/bin/bash` **`3.2.57(1)-release`**.

**NOT run, and not claimed:**

- 🔴 **The defect itself was never reproduced on this host.** It only bites on bash **>= 4.1** and
  there is no such shell here. The failing-before behaviour is read from documented errexit semantics
  and corroborated by a reviewer's own rc-1 measurement on bash 5.2 — **his figure, not mine**. A run
  on bash >= 4.1 is **owed**; the ticket does **not** move to Done (SKILL §5f).
- The four platform suites (Schemathesis, Akto, Playwright, Performance/k6) did not run — no local
  stack. No pass is claimed for any of them.
- The `scripts/validate-env.sh` sites of the same shape, raised in review "for completeness only",
  are deliberately **out of scope** and remain **OPEN**: they need their own ticket and their own pass.

**Migrations + config:** none. No dependency, lockfile, manifest, baseline or spec-version edit. No
file under `systemTest/` is touched, so SKILL §5c does not apply.
