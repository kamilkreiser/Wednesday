# QA GATE tier 2, round 1 of 2 - T/U batch (#1713, #1715, #1716) - findings only

Gate model: claude-sonnet-5-5 (row G2). Window 12:42Z to 13:04Z, 2026-10-26. Pushed/merged/commented: nothing.

## Pins
ls-remote at START (12:42:52Z) and END (13:04:26Z) identical, matching Wednesday's pins. No head moved.
develop `5f689991861b3b9be295797a437ef18b6f55a492`; #1713 `7507b9e61ca1b26d64190d6164de6c9fe87b685d`; #1715 `1cdde251848f20e641ab6f9075c2930f5de27dff`; #1716 `71eb278f641ca0000d395ecfb6ed6837ebfa6bff`.
A GO below is about these SHAs only. All three PRs are branched off older bases (behind develop by 4/3/3 commits); I diffed with three-dot and also tested a merged tree (below).

## BLUF

| PR | Verdict | Worst finding |
|---|---|---|
| #1713 KS-1726 | GO | LOW: T's "bicep byte-identity UNMEASURED" is now MEASURED and clean; only residual is a doc line (ENVIRONMENT-VARIABLES.md:124) that is prose, not comment, which the "comment-only" wording slightly undersells |
| #1715 KS-1443 | GO | none above INFO; Linux red/green reproduced end to end |
| #1716 KS-1736 | GO WITH NOTES | LOW: quickstart's "3,000 req/hour" figure is not pinned by any cell (mutant 3,000 -> 30,000 survives 16/16); LOW: PR-body-level cite ranges off by a line or two |

Order: all pairwise and all three sequential orders merge clean (disjoint files: 7 files, +106/-27 = exact sum of the three). No ordering constraint. Suggested: #1715, #1713, #1716 (test-only first, then docs/comments, then the user-visible portal text, so the one with a note lands last and can wait on the LOW). Any order is safe.

## #1713 KS-1726 (comment-truth, six sites)

FOUND
- Scope: 3 files, +16/-16 (three-dot vs develop). Two commits `1d89806dd` (comments) and `7507b9e61` (@description). I checked every changed line in services.bicep and docker-compose.yml programmatically: all are `//` or `#` comment lines except exactly one, the `@description` on services.bicep:129. ENVIRONMENT-VARIABLES.md:123-125 is a doc paragraph (not a code comment), 3 lines.
- Truth of the new text against code: `originate/src/utils/gatewayProvenance.ts` `createGatewayProvenanceMiddleware` with empty secret does `record('unconfigured'); strip(); next()` (fails closed, KS-1032, Kam 2026-10-13), and `describeState('')` emits `[gateway-provenance] FAIL-CLOSED - GATEWAY_VOUCH_SECRET is unset, ... DROPPED from every request`. So the new docs line quoting `FAIL-CLOSED - ...headers are DROPPED from every request...` matches the real boot line, and the old `DISABLED - ...honoured from ANY caller` is gone and is pinned absent by existing originate cells.
- Census at the PR head: no remaining "fail-open / inert / honoured from ANY" statement about GATEWAY_VOUCH_SECRET anywhere under Blockchain outside the deliberately historical paragraph at gatewayProvenance.ts:54. (My census is my own regex, not a re-run of T's 13->7->6; the unrelated fail-open hits in RLS/session/redis files are different controls.)

TESTED-HOW
- bicep CLI: none installed anywhere (no `bicep`, no dotnet, `~/.azure/bin` absent; the az bicep cache is empty). I downloaded the official release binary (`bicep-osx-arm64`, v0.48.1, sha256 `62cd5958c62fa1b738e9b69f24799fabddb90ed83fdb7d6d2563dde376ce479d`) into the gate workspace only. Provenance caveat: fetched over HTTPS from the GitHub release URL, no signature check done.
- `bicep build --stdout services.bicep`, develop vs #1713 head: both rc 0, no errors. `diff` shows EXACTLY two differing lines: `templateHash` (expected: the hash covers the template body) and the parameter `description` metadata string (170952 -> 170995 bytes). Nothing else. This is the measurement T declared missing; it confirms commit 2 changes the compiled ARM only in the description metadata.
- Control A: commit 1 alone (`1d89806dd`) compiled vs develop compiled: BYTE-IDENTICAL (cmp), including templateHash. So the comment commit is compile-neutral.
- Control B / mutant: in the PR-head services.bicep I removed the `//` from one of the changed comment lines (the :705 line); bicep rc=1 with BCP057/BCP236. The compile instrument is sensitive to comment-line damage.
- `docker compose -p gatetu config` develop vs head: identical after normalising the build-context path (my first compare differed only because I had named the two temp dirs differently, an instrument error of mine, recorded below). Control: changing `GATEWAY_VOUCH_SECRET=${GATEWAY_VOUCH_SECRET:-}` to `:-x` shows `GATEWAY_VOUCH_SECRET: x` vs `""` in the diff, so the comparison can see a value change. No container started (config only).
- Shell suites that read compose/bicep at head: check_no_latest_tags 9/0, prometheus_targets 6/0, start_secuura_expected_services 5/0, slot_is_local_host_only 4/0. Originate jest `ks1032-unconfigured-vouch-fails-closed` + `ks1041-gateway-provenance`: 2 suites, 33 passed.

NOT TESTED
- A real Azure deploy or `az deployment what-if` (no subscription work; out of scope and would touch a tenant).
- Whether T's seat-level 18/18 and 6/6 changed-line claims reproduce line for line; I re-derived the property (all changed lines are comments) rather than their counts.

SEVERITIES: LOW only (the doc paragraph is prose, so "comment-only" is true of code files, not of the md).

## #1715 KS-1443 (lsof selector, Linux-only)

FOUND
- Scope: 2 files, +43/-9, both shell tests (`Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`, `systemTest/__tests__/bootstrap_login_diagnosis.test.sh`). No product code touched, so "not a product bug" holds.
- Root cause reproduced on Linux (below): lsof's COMMAND column for a listening node reads `MainThrea`, so `awk '/node/{...}'` matched nothing. The new selector reads only lsof's PID column and decides membership from `$!`-captured PIDs, then confirms by the stub's absolute path.
- Cell 5: the PR's claim that `/bin/sh` must be absolute and that the tool list is complete is consistent with `run-migrations.sh`: cell 5 exits rc 4 at the `command -v pg_isready` guard before sed/sleep/basename/tail are reached, so the tool list is over-provisioned, not under.

TESTED-HOW (one throwaway `docker run --rm node:24-bookworm` per run, arm64 Debian 12, lsof + postgresql-client installed from apt inside, tsx installed under the mounted dir)
- Linux, develop's tests: bootstrap 17 passed / 1 failed (`KS-1201 CONTROL: the listener count must fire with a stub running`); migrations 6 / 1 failed (`CELL 5 precondition - pg_isready IS findable at /usr/bin/pg_isready`). RED for the stated reasons.
- Linux, #1715 head: bootstrap 18/0 (CONTROL fires, reads 1); migrations 7/0. GREEN. This is the WHOLE bootstrap file on Linux (U's declared "full part-1 suite not run on Linux" - I ran the full file; 18 cells).
- macOS, develop's tests and head: both 18/0 and 7/0 (the defect is Linux-only; the change does not regress macOS).
- Mutants on the Linux head copy, all KILLED: (A) `stop_stub` made a no-op -> "no login_stub.mjs listener may survive" FAIL 17/1; (B) `start_stub` called in a subshell `( )` -> KS-1201 CONTROL FAIL 17/1 (matches U's 17/1); (C) path confirmation changed to `$STUB.x` -> CONTROL FAIL 17/1; (D) cell-5 PATH given `:/usr/bin:/bin` back -> precondition FAIL 6/1.
- Containers: 228 total / 0 running before (`docker ps -a`), 228 / 0 after. Two run-then-removed containers for the main run plus one for mutants, all `--rm`.

NOT TESTED
- Alpine/busybox lsof (different column layout); a Linux runner that is not aarch64; the real CI runner image. The fix reads only the PID column, so the risk is low but unmeasured.

SEVERITIES: none above INFO. INFO: the `lsof -sTCP:LISTEN` presence check is partly redundant with the `ps -o command=` check for a dead PID (a killed PID has no command line), so the listen filter is not what makes mutant A die; that is harmless.

## #1716 KS-1736 (developer-portal.html text)

FOUND
- Scope: 2 files (+47/-2): `developer-portal.html` (2 lines) and the existing KS-1649 test file (6 new cells). No code.
- Citations checked against code (at head):
  - `routes/platform.ts:142-150`: lines 142-150 are the tail of the KS-1195 comment block ("hour, tunable by env... new keys only... existing keys keep 1,000 until rotated ... This value travels on the key MINT ... inserts a row and never updates one ... A rotate mints a new key, so a rotated key takes the new ceiling"). The substance the portal now states is at 146-150; the block starts at 141 ("Kam ruled on 2026-10-09"). Cite is accurate for the content, one line short at the start.
  - `middleware/rateLimitEnforce.ts:63-67`: the comment "Conservative fallback applied only when a machine caller reaches the limiter without a configured rateLimit (misconfiguration / future path)" and `DEFAULT_MACHINE_RATE_LIMIT = 100`, `..._WINDOW = 60`. Exact. (Commit message cites 66-67, PR text per the brief 63-67; both defensible.)
  - `middleware/auth.ts:248-249`: `rateLimit: data.rateLimit || 100, rateLimitWindow: data.rateLimitWindow || 60`. Exact.
  - "A key keeps the ceiling it was minted with": no `UPDATE svc_api_keys SET rate_limit` exists in any service; `scopes.ts:105` records "no PATCH and no UPDATE svc_api_keys". Only UPDATEs are is_active/last_used/usage. Claim holds.
  - 3,000 default and 1-10,000 bounds: `CONNECTOR_RATE_LIMIT_DEFAULT = 3000`, MIN 1, MAX 10000 in platform.ts. Per-key 1,000/hour default: security schema `.default(1000)`/`.default(3600)`, column default 1000/3600, admin-created keys `d.rateLimit || 1000`.
- Builders' declared unknown ("which keys actually carry no recorded allowance"): still unknown to me, and I could not measure it without a running gateway/DB. Code shows the fallback fires only if the validated key response has a falsy rateLimit, and every insert path writes 1000 or more, so in practice the 100/min sentence describes a path that stored keys are unlikely to hit. The wording is "A key with no recorded allowance falls back to 100 requests per minute" - true as code behaviour, mildly unreachable in practice. Not wrong.

TESTED-HOW
- Instrument errors first (recorded below): I wrongly ran jest, then used a TMPDIR too long for tsx's socket (unrelated to this PR).
- vitest, ks1649 file, develop's HTML + head's tests: 5 failed / 11 passed (16): A1, A2, B1, B2, C3 red; C4 (non-vacuity control) green; all ten pre-existing KS-1649 cells green. Matches the PR's 5/11.
- Head: 16/16 passed.
- Full api-gateway suite at head: 122 files, 1196 passed (1190 + 6 new, consistent with the claim). Same 1196/122 on the merged tree of all three PRs.
- Mutants on head's HTML: (M1) quickstart fallback 100 -> 1,000/min: killed by C3 (1 failed/15). (M3) row "keeps the ceiling it was minted with" -> "keeps its ceiling": killed by A2 (1/15). (M2) quickstart "3,000 req/hour" -> "30,000 req/hour": SURVIVES, 16/16 green. File restored afterwards (status clean, 16/16).
- Residual census: only DEPLOYMENT.md:1015 (`RATE_LIMIT | 1000/min | 100/min | 60/min`, an env-tier table, unrelated) mentions per-minute figures elsewhere in docs.

NOT TESTED
- Rendered HTML in a browser; a running gateway; real keys.

SEVERITIES
- LOW: the quickstart's second number (3,000 req/hour) and the "Platform S" attribution are unpinned; D1 pins the row, B2 pins only the 1,000 phrase. A later edit of the default would leave the quickstart stale and the suite green. Suggest a one-line cell (quickstart contains the same `fmt(3000)` the resolver returns) - not a blocker.
- LOW: cell C3 is labelled CONTROL but is red on develop (it asserts new text), so "control" is a misnomer; harmless.
- INFO: "keys minted before the default moved to 3,000" correctly drops the date/release name; true per platform.ts:141-150.

## Merge-tree (my own clone, objects only)
- dev+#1713, dev+#1715, dev+#1716: each rc 0 (clean). Pairwise #1713+#1715, #1713+#1716, #1715+#1716: clean. Sequential orders 1713,1715,1716 / 1716,1715,1713 / 1715,1716,1713: all clean. File sets are disjoint. Combined stat +106/-27 across 7 files = exact sum of the three.
- On the merged tree (develop + all three): bicep compile differs from develop by the same two lines only (hash + description); api-gateway 1196/1196; bootstrap 18/0; migrations 7/0; deps-present rc 0.
- Recommendation: any order; I'd land #1715, #1713, #1716.

## Instruments and errors of mine (recorded)
1. Ran `npx jest` on the api-gateway file; that package uses vitest. Re-ran with vitest. Conversely tried vitest on originate, which is jest; re-ran with jest.
2. First bootstrap run on macOS used a long workspace TMPDIR; tsx's IPC pipe path exceeded the Unix socket limit (EINVAL) -> 11 spurious failures. Re-ran with a short private `mktemp -d /tmp/gtu.XXXX` (this is why the TMPDIR is under /tmp, not the workspace, for the shell suites). The earlier `tmp.HBVt` dir in the workspace was used for the other runs.
3. First compose-config compare was byte-different only because my two temp dirs had different names (build context path). Normalised and re-compared, with a control.
4. My first Linux container ran a foreground `node` server then `wait`ed on it forever (10+ minutes); I killed that one child process inside my own container and the script proceeded. No effect on results.
5. Hooks blocked `$R`-variable write verbs outside literal paths; I used literal paths inside my own clone. `gh` is unauthenticated in this shell, so I could not read the PR BODIES; I used the three PR head commit messages plus the brief's verbatim claims. If a PR body says something the commit message does not, I did not check it.
6. One `bicep` binary was downloaded to `.../gate_tu_batch_20261026/bicepbin/` (no signature verification) - delete if the workspace is audited.

## Artifacts
Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_tu_batch_20261026/` (repo, linux/, bicep outputs bic_*.json, u_linux.txt, u_linux_mut.txt, v1716_*.txt, mt.txt, lsremote_start.txt / lsremote_end.txt).
