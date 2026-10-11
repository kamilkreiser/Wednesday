From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).

# BRIEF B219 (SEAT B): give `POST /api/v1/admin/demo/reset` its own 90 s BFF limit so the hosted "Reset demo" can finish
**Written:** @NOW@ AEDT 2026-10-11 by Friday. **Pane:** `Datasec/HPSM-POC-B` (the launcher picks the newest `Briefs/` file containing `_SEAT-B_`, `Launch_Claude.command:110`; the last one, B216, ended `READY FOR REVIEW`). **Tier 2** (one constant + one route in the BFF, plus tests; a QA gate follows; nothing on screen changes).
**Report:** `1_Project_Definition/Briefs/2026-10-11_B219_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · NEW WORDS candidates). Last line exactly `READY FOR GATE: b219/demo-reset-upstream-timeout <sha>` (sha read by `git ls-remote origin refs/heads/b219/demo-reset-upstream-timeout` after your last push), or `STOPPED: NEEDS FRIDAY` + ONE question.

## Why
B217 (`Briefs/2026-10-11_B217_STATUS.md`, evidence `Briefs/2026-10-11_B217_evidence/`) pressed "Reset demo" once on hosted. The API needs about **34 s** for the reset (12.6 s of that is the sample PDF). The web BFF cut the call at 30 s (`[bff] upstream POST /api/v1/admin/demo/reset timed out after 30000 ms limit in 30229 ms`), so the browser got **504 `upstream-timeout`**. The API then saw that the caller had gone, answered **499 after 34,090 ms**, and **rolled the reset back** (`ShowcaseEndpoints.cs:243`; the transaction is in `ShowcaseSeeder.cs:274-387`).
**Friday's ruling (ADDENDUM-1 to B217):** raise the limit for that ONE route only, 30 s → **90 s**. No global change. It ships in the next hosted deploy; a fresh seat presses the reset once after that deploy.

## Every limit on the path (drafter's read at main `4229be3`; re-cite each at your base)
| Hop | Where | Limit | Fits 90 s? |
|---|---|---|---|
| Browser fetch | `web/src/api/client.ts:221-223` (`resetDemo`, openapi-fetch) and `:229-241` (`resetShowcase`, plain fetch); `readRetry.ts` never retries a write (`:10`) | none: no signal, no timer | yes |
| Next route handler | `web/src/app/api/v1/[...path]/route.ts` (`force-dynamic`, no `maxDuration`); `next.config.ts` sets none | none in repo (standalone `node server.js`, `appservice.bicep:177`; Node's own server `requestTimeout` default is 300 s) | yes |
| **BFF upstream** | `web/src/server/bff.ts:151` `NAMED_WRITE_TIMEOUT_MS = 30_000`, applied through `NAMED_WRITES` `:152-159` (the reset is `:155`) by `upstreamTimeoutMs` `:171-176`; the timer `:267-271` | **30 s: the cut** | **this brief** |
| Web → API transport | Node `fetch` (undici) header/body timeouts default to 300 s; `HPSM_API_BASE_URL` = the API's own `*.azurewebsites.net` (`appservice.bicep:189`) | 300 s | yes |
| Azure edge | no Front Door, CDN or Application Gateway in `infra/` (`git grep -i "frontdoor\|Microsoft.Cdn\|applicationGateway\|Microsoft.Network"` → 0); App Service's front end cuts a request at 230 s (Azure's documentation, outside the repo), on both hops | 230 s | yes |
| API | no request-timeout middleware (no `RequestTimeout` / `UseRequestTimeouts` in `api/src`); the seed lock waits up to 15 s for a reset (`ShowcaseSeedLock.cs:62`), so worst case is about 15 + 34 = 49 s | none overall | yes |

Re-check each row. **If you find any limit below about 50 s on this path other than `bff.ts:151`, STOP and name it (file:line, value).**

## Do
1. **Base:** your own worktree from main. `git ls-remote origin refs/heads/main` must be `4229be358760b9e2af9ed6ccc68a60332d9b97ec` (Friday read it at drafting). If main moved, read `git diff --name-only 4229be3 <new>`. If nothing is under `web/src/server/**` or `web/src/api/**`, base on the new main and say so. Otherwise STOP. Branch: `b219/demo-reset-upstream-timeout`. Every code-repo ref write (fetch, worktree add, commit, push) goes under the shared lock `.tools/.git-lock` (copy B215's `lock.sh`). Scratch: `.tools/b219/`.
2. **Red first**, in `web/src/server/bff.timing.test.ts`, using the fake-clock pattern already there (`:73-84`, `:85-104`). No real 35 s sleeps.
   - `upstreamTimeoutMs("POST", "/api/v1/admin/demo/reset")` → `90_000`.
   - `handleApi` on that route, with a fake upstream that answers 200 at 35 s: it is **not** cut at 30 s and answers 200.
   - The same route with a stalled upstream answers 504 at 90 s, and not before.
   - **Controls (unchanged):** `POST /api/v1/showcase/reset` and every other named write → 30 s; the downloads → 30 s; everything else → 10 s; the narrative draft → 75 s. One control does the 30 s cut through `handleApi` on `POST /api/v1/showcase/reset`.
   - Move the reset's row out of the 30 s table (`:24`) into its own case. Say in HOW that this is the only changed expectation and why.
   - Show the new cases failing at base before the code change (quote the reporter).
3. **Code, `web/src/server/bff.ts` only:** reuse the existing per-route mechanism. Add one named constant (e.g. `DEMO_RESET_TIMEOUT_MS = 90_000`) with a comment citing B217's 34 s measurement and Friday's ruling. Take `/api/v1/admin/demo/reset` out of `NAMED_WRITES` and match it in `upstreamTimeoutMs` before the named-write check. Do not touch the other limits, the timer code, the 504 mapping or any words.
4. **Prove it:** run the full vitest suite (`--maxWorkers=4`), then `typecheck`, `lint` and `build` in `web/`. Report the pass counts at base and at head. Run gitleaks over `<base>..<head>`.
5. **One commit**, then a plain push of the branch only. Read the head back with `ls-remote`.

## FOUND (report these; change none of them)
- **NEW WORDS candidate for Kam (do NOT change in this round):** after a BFF timeout the screen shows *"This screen's demo state was cleared, but the sample data could not be reset: This is taking longer than usual. It may still finish, so reload the page in a minute before you try again."* For the reset this is misleading on hosted: when the web gives up, the API rolls the reset back, so it never finishes.
  - The prefix comes from `web/src/components/shell/AppShell.tsx:63`.
  - The 504 sentence comes from `describeFailure`, `web/src/api/client.ts:288`.
  - Re-cite both at your base. Under NEW WORDS, quote them and say where they come from. Propose nothing on screen. Words change only on Kam's card.
- The code comments at `bff.ts:264-266` and `client.ts:285-287` assume the API carries on when the proxy gives up. Note that the reset is the counter-case (the API's token is cancelled). Leave the comments as they are.

## Partition, ports, holds
- **Yours:** `web/src/server/bff.ts`, `web/src/server/bff.timing.test.ts` (and a new `web/src/server/*.test.ts` only if needed). Prove the partition in HOW with `git diff --name-only <base>..<head>`.
- **Not yours:**
  - Live seat **Datasec/HPSM-POC-A = B215**. Its write set is the customer pages, `CustomerShell.tsx`, `components/{screens,customer}/**`, `attribution-preview.ts`, `ReportingEndpoints.cs` and `Reporting/Report/**`. Its brief lists `bff.ts` as NOT B215's (`B215 brief :92`), and B215 STOPs if main changes under `web/src/components/{shell,customer,screens}/**`. So **touch nothing under `web/src/components/**`** (AppShell included) and nothing in `web/src/api/**`.
  - **Datasec/HPSM-POC-E = gate B218**, read-only. Never touch its worktree.
  - Also never: `web/contract/**`, `schema.gen.ts`, `api/**`, `infra/**`.
- **Ports: 6930–6939 only**, if anything binds one (vitest should not). At drafting: `lsof -nP -iTCP:6930-6939` → 0 lines, and no brief or draft allocates them. **Never yours:** 6860–6929 (6890–6899 B215; 6920–6929 B218), 6540–6549, 6730–6739, 6941. Re-check with `lsof` before any bind.
- **Holds:**
  - Push your branch only. Friday opens the PR and merges once CodeQL and the checks are green.
  - No merge, PR, deploy, hosted access, Jira or mail. Nothing goes to any human.
  - Never delete files. Never edit a running script. Use your own worktree, and never gc/prune/reset anything that is not yours.
  - **Nothing is deployed:** this rides the next hosted deploy.
