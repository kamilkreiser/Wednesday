#1260 KS-1139 ARITHSTATUS: the 8 sync-secrets counters stop returning 1 at zero
head 62e69d23b2507780316f1930123c7d57ebba3ae2

## BLUF

The last **8 errexit-live sites** of KS-1139's census, all in `Blockchain/Dev/deployment/azure/sync-secrets.sh` at `:186 :192 :198 :204 :216 :221 :227 :232` (`SKIPPED`, `GENERATED`, `UPDATED`), under `set -euo pipefail` at `:20`.

An arithmetic command exits 1 when its expression evaluates to 0, and a post-increment yields the OLD value — so `((COUNT++))` at `COUNT=0` returns status 1, and on bash ≥ 4.1 errexit exits the script at the first count (bash COMPAT item 45).

`COUNT=$((COUNT + 1))` — an assignment's status is 0 at every value. **Not** `((++X))` (a pre-decrement evaluates to 0 at the last step and fails there) and **not** `((X++)) || true`, which masks the status instead of removing the failing construct.

## ⚠ This script was never executed and `az` was never run

It writes Azure Key Vault secrets. The proof lifts the file's **own bytes** and runs them with `az` behind a PATH shim that logs every call; **the log is asserted EMPTY**, and a deliberate call afterwards makes it read 1 — so the zero is a measurement, not a promise. The extracted region deliberately **excludes `:177`**, the `az keyvault secret show` line, so `az` cannot be reached even by accident.

## Test Evidence

**Touched:** `Blockchain/Dev/deployment/azure/sync-secrets.sh` — **8 lines changed of 8**, and every changed line is asserted to be an arithmetic counter, so a stray edit would show. Mode `100755` preserved.

**Ran — per site, from each file's own bytes.** Each of the 8 lines lifted verbatim and run with its counter at 0:
- **BASE returns non-zero at 8 of 8. HEAD at 0 of 8.**
- Counter **values** are identical at every site (0 → 1), so the fix changes status and not effect.

**Ran — the whole region.** `179-233` (the complete `if/elif/else/fi`) lifted and driven once per branch with `log_*`/`set_secret`/`generate_value` stubbed: **UPDATED**, **SKIPPED**, **GENERATED** and **SKIPPED-when-already-generated** all reach the same counts on BASE and on HEAD, rc 0 both.

**Ran — the static census, with controls in both directions.** The CELL 4 regex from `docker_build_empty_table.test.sh`: **8 on the base → 0 on the head**; the safe `$((X + 1))` form **0 → 8**. Negative control: `docker-build.sh` reads **0** (fixed by #977). Positive control: the pre-patch copy reads **8**.

**Ran — the in-hook gate on this push:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` · `legs 3 4 8 — local stack not up`. `pre_push_hook_base` **28/0** · fixture guard **6/0** · `run_shell_suites` **49/0** · **shell suites 60 passed, 0 failed, 0 skipped (of 60)**. `bash -n` rc 0. **No suite count changes in this PR.**

## NOT COVERED — and this is the honest limit of the whole PR

**The errexit DEATH is not reproduced. It is cited, from bash COMPAT 45.** `/bin/bash` 3.2.57 is the only bash on this machine and every local container image is busybox with no `bash` at all, and 3.2 does not apply errexit to an arithmetic command.

Five shapes measured here under `set -e`:

| shape | outcome |
|---|---|
| `((X++))` at top level | **survives** |
| inside an `if` body at top level | **survives** |
| inside an `if` within a `while` body | **survives** |
| as the **last command of a called function** | **DIES, rc 1** |
| `X=$((X + 1))` anywhere | survives, status 0 |

**These 8 sites are the `if`-inside-`while` shape**, so on this host they do not die. That also **reconciles this ticket's header with its own 2026-09-22 gate comment**: the gate measured the *function* shape in `validate-lint.sh`, the header describes the *command* shape, and both are right about different things.

Also not covered: **no run against a real Key Vault, no `az` call, no deploy** — by design and by hold. **No measurement on Linux or on bash ≥ 4.** And the fix's correctness does not rest on the unreproduced death: removing a construct that returns 1 is right at every bash version.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no workflow. This file is a deployment script and **is not executed by this PR or its tests.**

`Refs KS-1139`; does not close it — the ticket's census also covered `validate-lint.sh`, whose 2 sites were already the safe form at the round-20 base.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

