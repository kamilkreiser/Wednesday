**Refs KS-1388** — https://linear.app/secuura/issue/KS-1388

Covers **section 1 only** of that ticket. Narrowing, not closing.

## What changed and why

Both commented `SECUURA_NGINX_STATUS_URI` examples — `observability/.env.example` and
`observability/config/alerting.env.example`, both at the **repository root**, not under
`Blockchain/Dev/` — suggested `http://secuura-nginx-gateway:6882/stub_status`. **6882 is the
gateway's published HOST port** and is not reachable from the exporter's network. The in-network
port is **80**, which `observability/docker-compose.yml:331` already defaults to. Both examples now
say `:80`.

Two new cells in the existing KS 971 shell suite
`Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` pin the port by source text, one per
env example. Each changed line carries a `# KS-1388:` why+ticket comment (skill section 5d).

## Test Evidence

Run by me, Seat B 61st, in the pushing worktree at base `f01c1da5717f`.

**touched** — `prometheus_targets.test.sh` (+16/-0), both env examples (+2/-1 each), both platform-k
documents (+92/-0 flow, +35/-2 cheat sheet).

**ran**
* the KS 971 suite directly: base **rc 0, 4 passed / 0 failed** → head **rc 0, 6 passed / 0 failed**
* `run-shell-suites.sh` whole: **67 passed, 0 failed, 0 skipped (of 67)** before AND after — the
  same suite count, because these are cells in an existing suite, not a new suite file
* `bash -n` on the modified suite: rc 0
* push preflight: **12/15 legs ran, 3 SKIPPED — legs 3, 4 and 8, because no local stack was up.**
  That is NOT a pass and is not quoted as one. 67 shell suites 0 failed, 13 code guards passed,
  0 orphaned `login_stub` pids.

**red rows, named descriptively**
* *both test sections applied, neither product hunk* → **rc 1, 4 passed / 2 failed**, one failure per
  env example, each printing its own want/got pair (`:80` wanted, `:6882` found). `bash -n` rc 0 in
  that state, so these are assertion reds and not a file that failed to load.
* *cross-control, `.env.example` product hunk alone* → 5 passed / 1 failed, and the surviving failure
  names **alerting.env.example**.
* *cross-control, `alerting.env.example` hunk alone* → 5 passed / 1 failed, naming **.env.example**.
  So each cell is keyed to its own file and neither can be satisfied by the other file's fix.
* *both hunks* → rc 0, 6 passed.

**NOT run** — no live sweep (skill section 5f), so KS 1388 does not move to Done on this PR's
account; the observability stack was never started; sections 2 and 3 of the ticket are untouched; no
image, container or deploy. Whether any deployment actually consumes either commented line is
**UNMEASURED** — both are comments.

**migrations + config** — no migration. The two config files changed are `.example` files; nothing
reads them at runtime.

## Applied == held

The two held carves were applied independently, in the same order, onto the same base blobs with a
separate index in a separate repository (tree `04d226e93b48`). The suite file is `cmp`-equal to this
branch's. Each env example differs from the independent apply by **exactly one added line**, which is
its `# KS-1388:` comment — so the proof is "held hunk plus exactly one named added line per file".
A firing control shows each file differs from its base blob.

**Exec bit:** `prometheus_targets.test.sh` is `100755` in the index and `git apply` left it
non-executable on disk under this repository's `filemode=false`. Restored with `chmod +x` on that one
file, never `checkout-index -a`, and re-asserted executable.

## Documentation (skill section 4)

A new KS 1388 block in **both** platform-k documents, in this same commit: flow block **14**, placed
in number order (the flow now reads 1–14 ascending, no duplicates), and a matching cheat-sheet
section placed last. Every figure states its value, the date and the host.

**Timing statement.** No stated timing covers this suite. Instrument, printed so it can be re-run:
`/usr/bin/grep -c -i -E` over both documents at base SHA `f01c1da5717f` — `run-shell-suites` **0**
flow / **0** cheat; `shell suite` **0** / **0**; `prometheus_targets` **0** flow / **1** cheat, and
that one hit is prose inside the KS 971 block (cheat `:2695`), not a timing row. Must-hit control
`auth`: **71** flow / **70** cheat, so the zeroes are measurements and not a blind grep.

**Also in this commit, outside this change's own block:** the measurement host appended to the two
cheat-sheet timing rows that carried a date and no host (gate findings N-1380-3 and N-1381-2). Each
is a one-row edit; a character diff shows the only difference is the appended host text.

## Path gate

`pathgate56` **PASS** — 6 assertions over the 5 measured paths, the set exactly equal to the declared
set, zero co-tenant paths, all three internal controls firing. Firing control: dropping one declared
path returns FAIL at rc 1 and names the extra path.

Raised from Wednesday-held Spark passes, re-proved by Seat B 61st.