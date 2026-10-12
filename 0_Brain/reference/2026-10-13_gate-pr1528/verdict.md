# Gate verdict: Secuura Platform K PR #1528 (KS-865, KS-1347, KS-1137 F-4)

Gate: independent QA, findings only. Tier: narrow (tooling + tests). Run 2026-10-13 by a Sonnet gate session.

**Head under test:** `6bfd74ad7c39b43c614c5d837744780f20788fa2` (asserted via `git rev-parse pr1528` after `fetch refs/pull/1528/head` with the project's core.sshCommand).
**Base:** develop `81ac1ea60ec684f1636a25832d9a7f3bf28470f5` (asserted, unmoved). Diff: 7 files, as briefed.
**Method:** `git clone --shared` of the project into my scratchpad (two clones: head, and develop for A/B). Project checkout never written. No pushes, no GitHub/Linear writes, no box contact. Hosts: macOS, bash 3.2.57, node v24.7.0, /usr/bin/jq 1.7.1-apple. Clone has NO npm installs.

## VERDICT: GO WITH NOTE

Majors: 0. Minors: 3 (M1 incomplete class, M2 brittle probe, M3 leftover raw .pathname site, already known to the author). The PR's claims held up under independent re-derivation.

## 1. KS-1347 and mutant u4 (re-derived, not taken from the author)

FAIL condition stated before running: deleting the node:url import from server.ts must turn the KS-1347 suite red; restoring must turn it green; the real file must also fail at runtime without the import.
- Head suite as shipped: 8 passed / 0 failed (evidence/01). 
- u4 (delete `import { fileURLToPath } from 'node:url'`): tamper LANDED (grep count of `node:url` 1 -> 0, `git diff --stat` shows 1 deletion; evidence/03). Suite: 4 passed / 4 failed, rc 1. Reds: the import CONTROL plus the three cells that need a working probe. u4 BITES.
- I read WHY it is red, not just that it is: the probe dies, its stderr is discarded (`2>/dev/null`), so the cells show `got ""`. Independent proof of the cause: running the real mutated server.ts under node v24.7.0 gives `ReferenceError: fileURLToPath is not defined` at server.ts:35 (evidence/04). So the real file would fail without the import, and the suite's red tracks that.
- Restore: tree clean (`git status --short` empty), suite 8/0 again. Restored server.ts, run offline on an ephemeral port, loads past line 35 and stops at the R12 `HARVEST_EXAMPLES is not set` refusal (a guard that comes after the OUT_DIR line), so the import resolves. 
- Extra mutants (evidence/05): u5 revert to `new URL(import.meta.url).pathname`: 4 red incl. the spaced-checkout cells, while the no-space control stays green (reproduces the original bug as the ticket describes). u6 right function, wrong dir (`'..','..','out'`): 3 red. Both bite.

## 2. KS-1137 F-4, all three suites (evidence/06, 07)

Instrument: the suites' own output plus rc, with `sandbox-exec` denying exec and read of /usr/bin/jq to simulate a homebrew-only host (this machine has no brew jq, so the simulation is the only way to see the defect). The sandbox control FAILED as it should have: `/usr/bin/jq` rc 71 "Operation not permitted", and `jq` on a private `/usr/bin:/bin` PATH gives "command not found" rc 127. A signed copy of jq in a scratch dir stood in for the homebrew jq (it runs, rc 0).

| scenario | develop (3 suites) | head (3 suites) |
|---|---|---|
| normal host (jq in /usr/bin) | 6/5/5 pass, rc 0 | 7/6/6 pass, rc 0 |
| jq only on the OUTER PATH (homebrew-like) | **FALSE RED**: 1p/5f, 1p/4f, 3p/2f, rc 1; raw output shows `jq: command not found` from jobs/04-container-trivy.sh | 7/6/6 pass, rc 0, zero "command not found" |
| jq NOT on outer PATH, present in /usr/bin | FATAL rc 2 (all 3) | FATAL rc 2 (all 3), new wording "could not be resolved" |
| jq nowhere | FATAL rc 2 | FATAL rc 2 |

- No false pass: the new F-4 cell reds when the fix is removed. u7 (delete the `ln -sf "$JQ_BIN" "$root/bin/jq"` line, tamper landed, 0 of 1 remaining) on a NORMAL host: each suite goes 1 failed on exactly the F-4 cell (6p/1f, 5p/1f, 5p/1f; evidence/07). So the cell can fail even on a host where the bug is invisible.
- No false refusal introduced: the third row (jq reachable only via the subject's private PATH, absent from the outer PATH) refuses with FATAL rc 2 on head as on develop. I judge that correct, since the suites call `jq -r` themselves at outer level (e.g. `art()` helpers). Behaviour is unchanged from develop other than message text.
- Census (evidence/08, 09, 12). Instrument: `git grep` over the whole tracked tree for the CAUSE (a private PATH of `...:/usr/bin:/bin` combined with an outer `command -v jq`), not the damage. Control: the same pattern run on the develop tree finds all three known sites plus the others listed. **The three sites are NOT the full set. See M1.**

## 3. KS-865 (evidence/02, 17)
Header "What's checked" now lists 5 files (docker-compose.production.yml, services.bicep, services.parameters.json, main.bicep, main.parameters.json), identical by basename to CHECK_FILES (5). Suite: 9 passed / 0 failed. Mutants: u8 (re-add the stale header bullet, anchor asserted) -> KS-865 cell 8 reds, 8p/1f. u9 (drop main.bicep from the list) -> 4 red incl. cell 8. Cell 9's control plants an entry in a COPY, so cell 8 is not a tautology; u8 confirms it on the real file.

## 4. "Already done at develop" claims (read at develop)
- KS-865: PARTLY stale. At develop CHECK_FILES already had 5 entries (the dead one gone) but the header still advertised deploy-staging.yml (evidence/11). The ticket is NOT stale; this PR closes the residue.
- KS-1347: the auth half: not in my scope to re-prove from the ticket text, but the tree-wide census (any `new URL(...import.meta.url...).pathname`, plus a looser pass over files holding both tokens) at head finds one remaining site only: `systemTest/playwright/global-setup.ts:42`. Develop census (control) finds that plus server.ts:31. Sibling fixes visible: `systemTest/performance/runner/cli.ts:169` and the auth test at `ks847-no-raw-control-bytes.test.ts` already use fileURLToPath. Claim holds.
- KS-1137 F-2: DONE at develop. 04-container-trivy.sh:62 has the digit-bearing regex and a F-2 cell (container_trivy_image_filter.test.sh:141-157) already exists on develop; the PR changes nothing under Blockchain/Testing (`git diff dev head -- Blockchain/Testing` empty). A ticket closure candidate for F-2.

## 5. Full tracked shell-suite runner at head (evidence/14, 15b, 16)
- `run-shell-suites.sh --check-unreached`: OK, all 84 tracked suites reached (so the new ks1347 suite is wired).
- Full run, offline (`npm_config_offline=true`, stdin closed): **82 passed, 2 failed, 0 skipped of 84**.
  - `ks949_main_seed_idempotence.test.sh`: "packages/shared is not built (dist/index.js missing)", aborts at cell 1 of 27.
  - `preflight_test_types_ratchet_leg.test.sh`: 3 cells red ("planted type error FAILS the leg", etc.); the checker's own summary line absent.
  - Both fail IDENTICALLY on develop (evidence/16), so they are the missing-npm-install environment, not this PR. Neither suite was measurable here.
- Disclosure: my FIRST runner attempt was online-capable; I aborted it when I saw `npm exec tsx` starting in `systemTest/__tests__/provision_base_url.test.sh` (it could reach the npm registry, outside the brief). Its partial log is evidence/15a. I cannot rule out that suites before that point made an npm lookup; the rerun was offline. I flag it for the owner rather than smoothing it over.

## Findings

**M1 (Minor, regression-class): the F-4 fix leaves a fourth sibling.** `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` has the identical pattern: outer-PATH check at line 28 and private `PATH="$root/bin:/usr/bin:/bin"` at line 64, while its subject `Blockchain/Testing/jobs/06-tenant-isolation.sh:77-78` calls jq. Reproduced on the simulated jq-outer-only host at head: 4 passed / 1 failed, `FAIL RED the fallback run prints tested=3 cross-tenant_findings=0 want 1, got 0 (output: "tested=? cross-tenant_findings=?")` (evidence/09, 10). Oracle: History / Product (same class fixed in three, the fourth missed; the PR comment claims to fix "the class"). Quieter than the three fixed ones: the failure never says "jq". Severity: low (test tooling, host-shaped, invisible on /usr/bin/jq hosts), but it is exactly the recurrence the PR set out to stop. Fix-shape: same two-line change (resolve `JQ_BIN`, `ln -sf` it into `$root/bin`) plus the same F-4 cell. Regression test: the owner's F-4 cell copy for that suite, or better one structural guard that fails any `*.test.sh` that builds a `...:/usr/bin:/bin` PATH while checking jq on the outer PATH only. (`aggregate_report_trivy_artefact` and `ks1136_aggregate_report_unreadable_artefacts` have an outer jq check but no private PATH; they passed 5/5 and 6/6 on the simulated host, so they are not affected.)

**M2 (Minor): the KS-1347 probe is brittle against equivalent import spellings.** `ks1347_proxy_out_dir_spaced_checkout.test.sh` takes `NODE_IMPORTS` from `grep -E "^import .* from 'node:[a-z]+';$"` (script line ~51) and a control that requires `node:url`. Mutant u10 (`from 'url'`, valid Node, the mutated server.ts loads fine) and u11 (`from "node:url"`) each make 4 cells red while server.ts works (evidence/18). A false red on a harmless refactor, and the probe's stderr is `2>/dev/null` so the reason is invisible to whoever hits it. Fix-shape: accept both quote styles and bare builtin specifiers, and print the probe's stderr when it exits non-zero. Oracle: Purpose (a test of the OUT_DIR path, not of an import style).

**M3 (Minor, known): `systemTest/playwright/global-setup.ts:42` still uses raw `new URL(..., import.meta.url).pathname`.** Same class, same space-in-checkout defect, and the author attributes it to KS-1337 by design. I confirm it is the only remaining site tree-wide (evidence/11, 12) but note it is live, not fixed; the ticket must stay open.

## Not tested (Rule 2)
- A real homebrew host. I simulated one with `sandbox-exec` plus a signed jq copy; I did not test on a machine with only /opt/homebrew/bin/jq, nor Linux/CI, nor a different bash than 3.2.57.
- Suites needing npm installs, or the built packages/shared (ks949 and the test-types ratchet, plus anything `tsx`-based run offline): not measurable here; they behave identically on develop.
- The `scripts/openapi-examples/*.test.ts` files (the PR says no runner reaches them): not run, not audited.
- server.ts was loaded only up to the R12 guard; I never ran a real capture, and never contacted an upstream or any server (a loopback listen on port 0 was never reached because R12 refuses first).
- The spaced-checkout behaviour of the whole proxy end to end (only the OUT_DIR expression via the probe, in a temp dir with and without spaces).
- GitHub CI status for the PR, ticket text for KS-865/1347/1137 (I judged "already done" by code only), and the correctness of the KS-1337 auth half beyond the grep census.
- No retractions: none of my findings changed during the session.

## Evidence index (this folder, `evidence/`)
01 ks1347 head run; 02 ks865 head run; 03/04 u4 and real-module proof; 05 u5/u6; 06 F-4 matrix; 07 why-red + u7; 08 census; 09/10 fourth sibling; 11/12 census KS-1347/865/F-2; 13/14 runner list and unreached check; 15a aborted online run (kept, disclosed), 15b full offline runner; 16 two failures dev vs head; 17 KS-865 mutants; 18 import-spelling mutants.
