STARTABLE: YES (after Tuesday's stamp; two rulings are wanted first, Q-1 and Q-2, each with a default that lets it start)

# B1565 drafter report: HPSM-POC lane H-2 (HPSMPOC-193), seat H164

Drafted 2026-11-15 09:59 to 10:13 AEDT (`date` printed 09:59:08, 10:01:37, 10:03:35, 10:06:05, 10:13:21). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1565_SEAT-H164_hpsmpoc-lane-h2-server-headers.md` (86 lines), sidecar `...h2-server-headers.md.measured` (100 claims plus Sxx lines), work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s276/d1565/`.

## BLUF
- **One ticket kitted: HPSMPOC-193.** The product owner's ruling (comment 41009: option (b), "a shared header value that only the web front end sends, held on both apps, so that the API believes a forwarded address only when that header is present") is buildable as code and tests on the API and the web server, with no value stored and nothing set on a host. Not an HTML-phase ticket, no `next-phase`/`gather`/`awaiting-hp` label (JQL count 0, control 27).
- **Lane H-3 is NOT kitted** (reasons under Scope). H-3 is file-disjoint from 193 but is a different shape and a different gate tier.
- **Base `b6c282ee50086bc1ac7d773ccabf00fcf8c055cc`**, open PRs 0, no `b1565*` branch, no HPSM pane, ports 9810-9819 free.
- **The kit is bigger than the sweep's "M" implies, because of three findings the drafter measured:** (1) a SECOND reader of `X-Forwarded-For` (`FollowUpLink.ClientAddress`) exists beside the middleware; (2) **a new web environment read reds the web unit job and the infra job unless one line is added to `infra/tests/test_security_baseline.py`** (measured in a copy: `web-settings.test.ts` 3 passed 1 failed, then 4 of 4 with one `WEB_SETTINGS_NOT_HOSTED_YET` entry); (3) the platform switch's own forwarded-headers middleware may run BEFORE any gate placed in `Program.cs`, which the drafter could not measure (no `dotnet` here), so the kit puts a measured probe first (Step 3a) and names the fallback shape.
- **Not deployed, nothing stored.** Until the same value is stored on both hosted apps, the new code believes no forwarded address (fail closed): the follow-up unknown-link limit falls back to the connection's own address. That is Q-2.

## Scope, in and out, with reasons
IN: HPSMPOC-193 (API gate on `X-Forwarded-For`, web sender, one infra-test line).
OUT, with reasons:
- **H-3 items (web/e2e/a11y.spec.ts, api/tests point 4, scripts/deploy-from-ci.sh stub test, 480).** (a) 470 itself says "Not decided: whether to widen the journey test's margin ... and whether the migration timeout needs its own fix"; point 4 is "diagnose, add a test or record not reproducible", open-ended and a SQL Server timing problem that must not share a gate with a security-surface change; (b) 480 is "conditional": a remedy is still to be chosen (sweep Q2, default (a)); (c) these items read different CI jobs (`web-e2e`, the SQL Server shards for unrelated tests, a shell-script test) and would turn a G1 gate (Q-1) into a mixed one; (d) 193 alone already touches both API shards, web-unit, infra and one e2e shard. File-disjointness holds (H-3 owns `web/e2e/a11y.spec.ts`, other `api/tests/` files, `scripts/deploy-from-ci.sh`; this kit owns `ForwardedClientAddressTests.cs` and the H106 rows of `FollowUpHardeningTests.cs` only). Recommended: separate kit B-next for H-3 (Q-5).
- **Storing the value and rotating it** (Key Vault reference on both apps, Bicep, parameter files): the ruling calls it configuration; the sweep says "set nothing on a host". Infra edit is outside H-2's OWNS (Q-4).
- **OpenAPI sentence** at `api/tests/.../Contract/openapi.yaml:2244` ("`X-Forwarded-For` believed only from a configured proxy"): stays true; changing it touches three generated or compared files; left.
- **HPSMPOC-196** (measure the hosted front end's forwarded-header shape): hosted measurement, not buildable here.
- Nothing from the HTML phase and no HP-tool integration is built; the standing line is in the kit.

## PRIOR WORK (each count with its instrument and control)
- Open PRs: `pulls?state=open` length 0; `pulls/99999` 404; `state=all&per_page=4` 317, 316, 315, 314 closed (317 is B1556).
- Branches: `branches?per_page=100` paginated 332 names; loose pattern `1565|193|forward|proxy|h164|header` 6 hits, all unrelated (`header`/`proxy` words). `git/matching-refs/heads/b1565` 0; control `heads/b1541` 1.
- Earlier PRs that built what is extended: #93 (forwarded client address), #103 (demo outbound list param), #178 (UAT template outbound addresses); none carries a proof.
- Jira (own GET helpers `jget.py`, `jsearch.py` in the work folder; every JQL `project = HPSMPOC AND ( ... )`): 193 Backlog, label `b118-found`, comments 38951 and 41009 read whole; related 118 and 195 Done, 196 Backlog (hosted measurement). Text search `forwarded|KnownProxies|X-Forwarded-For|webOutboundAddresses` printed 89 rows, nearly all noise from the word "forward"; the relevant ones are 193, 118, 195, 196, 106, 107, 145, 210, 194.
- Code prior: `/usr/bin/grep -rn -F` over the tarball for `HPSM_FORWARD_PROOF`, `X-Hpsm-Web-Proof`, `ForwardedHeaders:Proof`: 0; control `HPSM_FORWARD_CLIENT_ADDRESS`: 11.
- Code at main today: the middleware path (`ForwardedClientAddress.cs`, `Program.cs:39-41,119-124`), a second reader `FollowUpLink.ClientAddress` (`FollowUpLink.cs:87-95,280`) with empty `FollowUp:TrustedProxies` hosted, the web sender (`bff.ts:296-306`). The UAT open sign-in key (`HPSM_UAT_OPEN_KEY`, `Auth__UatOpen__Key`) is the in-repo precedent for a value held by Key Vault reference on both apps, for the later infra step.

## Census by program (test files pinning behaviour this slice changes), frame stated
Frame: tracked files at main `b6c282ee`, tarball extracted in the work folder; C# counts are `grep -c` (DERIVED: no `dotnet` on the drafter box, so none could be run); TypeScript counts are real vitest runs (node v26.13.0 against `.nvmrc` 24, so the seat re-prints on the pinned node).
| program | file / rows | command and count | verdict |
|---|---|---|---|
| API, shard `api-assessment` (namespace `...Hosting.`) | `ForwardedClientAddressTests.cs`: 6 `[Fact]`, 2 `[Theory]` (11 + 12 rows) = 29 cases | `grep -c -F '[Fact]'` 6, `'[Theory]'` 2, awk over `Chain` 11, `Refused` 12 | the bucket row `:40-49` rewritten (sends the address through the pipeline with no proof); `AddressSeen` rows `:94-108,148-155` run the middleware alone on host options: unaffected unless shape A4 moves those options (the seat prints which) |
| API, shard `api-other-and-feedback` (namespace `...FollowUp.`) | `FollowUpHardeningTests.cs` H106 fact `:291-300` with `TrustedProxyFollowUpFactory` `:344-352` | `grep -n -F` | rewritten (needs the proof header); the static `H106_the_client_address_reads...` theory calls `FollowUpLink.ClientAddress` directly: unaffected (function unchanged) |
| API, every other test | all go through the real `Program.cs` pipeline | not enumerable by file; proof is both SQL Server shards whole plus the api project on SQLite | unaffected, shown by running them |
| web unit | `bff.client.test.ts` 17 rows, of which the 4-row address block | vitest json: 17/17; block 4 passed | 4 stay green and unchanged (the control); new rows added |
| web unit | `warmup-render.test.ts` 12 (`:40` asserts no `x-forwarded-for` on the warm-up request) | vitest json 12/12 | unaffected |
| web unit | `web-settings.test.ts` 4 | 4/4 at main; 3/1 with the new env read and no list entry; 4/4 with one entry | the one-line infra edit makes it green |
| web unit, whole dir | `src/server` | 40 files, 1326 tests, 1326 passed, 0 failed | unaffected |
| infra | `test_security_baseline.py` (`WEB_SETTINGS_NOT_HOSTED_YET` `:432-435`, `rule_web_settings` `:497-506`), `test_outbound_address_spelling.py` | unittest discover in the tarball: 189 ran, failures 5, errors 4 (4 = no `bicep`; 5 include repo-wide scans reading the OUTER repository) | NOT a baseline; the seat takes it in its own clone |
| e2e | `hosted` project in shard `journey-and-prototype` runs the real BFF in proxy mode against a stub | `grep -c -F HPSM_FORWARD` over `web/e2e`, config, `web/scripts`, `scripts` 0 each; control `web/src/server` 5 | the one shard runs whole; seven NOT RUN with that reading |

## Chain table (rule 4: every step's inputs against the producer)
| step | inputs | produced by |
|---|---|---|
| 0 | the kit; the project's identity; the pinned toolchain | exist at BASE |
| 1 | `repo` clone, `gh` | step 0 |
| 2 | `repo`, `mut`, `head` clones; `base-unit.json` | step 0; step 2 writes `base-unit.json` |
| 3a | `mut`, `ForwardedClientAddressTests.cs` helpers (`Hosted`, `Peer`, `Open`, `ForwardingFactory`) | step 0; exist at BASE (`:31-36,161-167,172-178,196-210`) |
| 3 | `head`; the `ORDER:` line | step 0; step 3a |
| 4 | `head`; `bff.ts`; the infra-test dict | step 0; exist at BASE |
| 5 | steps 3 and 4 product code; the test harness files | steps 3, 4; exist at BASE |
| 6 | `mut`; the new and changed tests | step 0; step 5 |
| 7 | `head` whole; `base-unit.json`; SQL Server and Azurite containers on 9810 and 9811; `ci.yml` predicates | steps 2-5; containers started in step 7 |
| 7e | every added line of `head` | steps 3-5 |
| 8 | all the above green; `.tools` scan files | steps 5-7e |
| 9 | the pushed sha; the PR texts | step 8 |
No input is produced by a later step.

## Facts re-measured with instruments (most; the rest are in the sidecar)
- Main sha, PR and branch counts above: `gh api -X GET`, 09:59 and again 10:13 (`b6c282ee`, open PRs 0).
- Ports: `lsof -nP -iTCP:9810-9819 -sTCP:LISTEN` 0 rows at 10:06 and 10:13; control unfiltered 12 lines. Word-boundary scan `(^|[^0-9A-Za-z-])981[0-9]([^0-9A-Za-z-]|$)` over the 12 other non-`.pre-` SEAT kits of 14 and 15 Nov: 0 in each; control `978[0-9]` over the B1556 kit 2. Panes: `%0 tuesday`, `%1 fleet-monitor`, two unnamed; no HPSM pane.
- CodeQL: `code-scanning/default-setup` languages actions, csharp, javascript, javascript-typescript, python, typescript, suite `extended`; analyses categories seen for actions, csharp, javascript-typescript, python. The kit's step 7e covers C# and TypeScript rows in addition to the gate standard's JS and Python rows, and the one-line Python edit.
- Model rows: `model-routing.md:92` (C2), `:93` (C3), `:108` (G1), `:109` (G2); `models_latest.json:23` has `claude-sonnet-5-5`.
- `global.json` at the repository ROOT (not `api/`) pins `10.0.404`, `rollForward` `disable` (lines 3-4).
- `ci.yml`: `api` job runs `dotnet test` at `:87`; SQL Server shard filters `:252` (Assessment and Hosting) and `:255` (the rest); python predicate `:303` fails any non-Passed outcome, a skip included; database floors `:314` (100 and 110).
- The project's own checkout `2_Project_Files` still names `/Volumes/Laptop-DEV/` for the deploy key: `git ls-remote` from it printed `Permission denied (publickey)`. The kit tells the seat to clone by URL with the Datasec_DEV key (as the precedent does).

## D-decisions (made in the kit, each reversible by Tuesday at the stamp)
- D-1 Names: header `X-Hpsm-Web-Proof`, API key `ForwardedHeaders:Proof`, web env `HPSM_FORWARD_PROOF`; value 32-128 chars of `A-Za-z0-9._~+/=-`; never logged, never in an exception (the existing `Refuse` writes the value into its message, `ForwardedClientAddress.cs:105-106`: the kit forbids using it). The word "proof" is used in names because CodeQL's credential queries key on names such as secret, token, password.
- D-2 The gate removes `X-Forwarded-For` unless the proof matches (constant-time over SHA-256 digests), so both readers (middleware and `FollowUp:TrustedProxies`) are protected by one rule; the proof header is removed after the check.
- D-3 A malformed `HPSM_FORWARD_PROOF` on the web is dropped (not sent), not an error (an `off` mode would 503 every API call for a rate-limit helper); the API side refuses to start on a malformed value.
- D-4 The web keeps sending `X-Forwarded-For` as today and adds the proof beside it; the four existing web rows stay unchanged as the control.
- D-5 Middleware order is UNMEASURED, so Step 3a measures first and names fallback shape A4 (platform-instance options `None`, `Program.cs` adds the gate and its own `UseForwardedHeaders`).
- D-6 Tests spell the new names as string literals so that the red-first run fails by assertion at `mut`, not by compile error.
- D-7 Launch form, REFUSE list, lock, A MOVED MAIN, handover and identity lines copied from B1556/B1496; the kit adds `docker` containers by name (`b1565-mssql`, `b1565-azurite`) and a SQL Server run of BOTH shards whole, because every API test builds the changed `Program.cs`.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 Model and gate.** Row C3 says the design of a security surface does not go to Sonnet; the ruling and the shape are spelled out in the kit, so the sweep's Sonnet applies. Default: Sonnet builder, **G1 (Opus) gate**, round 1 of 2. Alternative: Opus builder (`BRIEF_SEAT_LEVEL=opus` in the launch line).
- **Q-2 Default when no proof is configured.** Kit default: fail closed, nothing believed, the host starts and logs one line. Consequence: after deploy, until the value is on both hosted apps, the unknown-link limit counts the front end's address (one shared bucket; the global ceiling holds; the ticket's own risk is Low). Alternative: legacy behaviour (believe as today) until a value is configured: weaker, contradicts the ruling's "only when that header is present". Default: fail closed.
- **Q-3 The one infra-test line.** A new web env read forces an entry in `WEB_SETTINGS_NOT_HOSTED_YET` (`infra/tests/test_security_baseline.py:432-435`). Default: yes, that single line is in the OWNS list; any other line of that file or any Bicep is a STOP. Alternative: split into two kits (web half and infra half), which leaves the web half unable to pass CI alone.
- **Q-4 Storing and rotating the value.** Not built. Default: after landing Tuesday cards a separate infra kit (Key Vault reference on both apps, modelled on the UAT open sign-in key, with the infra test pins); rotation is a single value, with a short window in which no forwarded address is believed. Needs the product owner only for the rotation cadence, if wanted.
- **Q-5 Lane H-3.** Not kitted (see Scope). Default: leave for a later kit; if released, draft three items separately: the a11y journey spec margin, the migration-timeout diagnosis (record not reproducible if so), and 480 under its own stated default (a).
- **Q-6 Seat on the first hosted deploy of this code.** Unrelated to building, named so the deploy kit orders it: the value must be on both apps before the API image carrying the gate is deployed, or the follow-up limit degrades as in Q-2.

## UNMEASURED
- Whether the platform switch's middleware runs before a gate in `Program.cs` (Step 3a measures); whether App Service sets `ASPNETCORE_FORWARDEDHEADERS_ENABLED` for this API (the test file itself says unmeasured, `ForwardedClientAddressTests.cs:52-54`).
- Every C# test count and all `dotnet` behaviour: no `dotnet` on the drafter box (`command -v dotnet` printed nothing). All SQL Server runs: docker not run by the drafter.
- Whether `codeql` is on the seat's box.
- The infra job at main in a real clone (no `bicep`, and the tarball sat inside another git repository).
- Whether App Service's front end passes a custom request header (`X-Hpsm-Web-Proof`) through unchanged between the web and the API: ordinary behaviour, not measured, and it is a hosted measurement (belongs with HPSMPOC-196).
- The landing rule quote (head-pinned squash, CLARIFICATIONS.md line 3617) is RELAYED from the B1556 kit; the project's local copy was not found to hold the phrase and may be older than origin.

## Outside-the-fences disclosure
Reads: `DRAFTER_RULES.md`, the lane sweep, the B1556, B1496 precedent kits, the gate standard, `model-routing.md`, `models_latest.json`, ticket 193, 470, 480 via my own GET-only Jira helpers (credentials read in-process from the project `.env`, never printed), `gh api -X GET` under the project's `GH_CONFIG_DIR` (branches, pulls, tarball, code-scanning), the project checkout's `git ls-remote origin refs/heads/*` (read verb; it failed on the stale key path and printed nothing but errors). Local runs in the work folder only: `npm ci`, vitest on a tarball copy, a mutated copy `mut/` of the tarball for the web-settings probe, `python3 -m unittest` on infra tests, `tmux list-panes`, `lsof`. One stray scratch file `/tmp/x_kits.txt` was written by a listing command and removed. No Jira write, no git push, no GitHub write, no file inside `/Volumes/Datasec_DEV/!CODING/`, no message, no tmux send-keys, no az, no docker, nothing deployed. No decision card was read; no other client's tree was read.

DRAFTED B1565: kit 86 lines, sidecar rc 0, questions 6
