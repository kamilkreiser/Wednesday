# QA BRIEF — Secuura/Blockchain, s161's six PRs, batched. Round 1 for every class.

## BLUF
**Six PRs from one seat, none merged, none deployed. Two carry a DEPLOYABLE surface and go FIRST.** You are findings-only: **you never fix.** Every PR below is pinned to a head SHA read from origin — **gate that SHA, not the branch tip**, and if the tip has moved say so and stop rather than gating something else.

## ORDER — deployable first, because a finding there is worth most
| # | PR | ticket | head SHA | tier | why that tier |
|---|----|--------|----------|------|----------------|
| 1 | **#929** | KS-943 | `8e082d96e` | **1** | `services/auth` — a repo function that answered success over a 0-row UPDATE. Auth surface + a deployable service. |
| 2 | **#928** | KS-950 | `e28d64b8d` | **1** | `services/api-gateway` — migration loaders and a seed arbiter. **Data/migration surface + deployable.** |
| 3 | #925 | KS-1046 | `0956c3dbe` | 2 | the preflight VERDICT line. No runtime surface — but it is the line quoted into Test Evidence blocks a client human reads. |
| 4 | #924 | KS-773 | `1497b39de` | 2 | `lockfile-cleanroom.sh` preflight guard. |
| 5 | #927 | KS-1027 | `63e955e0f` | 2 | systemTest restore/quarantine guards. |
| 6 | #926 | KS-927 | `542492c41` | 2 | a jest mock omission in `webhooks`. |

**If your window runs out, wrap having done 1 and 2 properly rather than all six thinly.** Say which you did not reach. That is a correct outcome.

## WHAT EACH ONE CLAIMS — check the claim, not the intention
- **#929 (KS-943):** `updateUser` returned a user object on a 0-row UPDATE, so two call sites answered success over a no-op. **Fixed at BOTH sites** — the ticket originally named one; `wallet.ts:468` is the second, identical, one function away. Returns `null`, which is already inside the declared `Promise<User | null>`. **`throw` was rejected on a measured 24-caller blast radius.** Three cells, the third a **control** (*both still answer 200 at rowCount 1*). Claims: `tsc` clean, auth **638/638** vs develop **635/635**, same 45 files, delta +3.
- **#928 (KS-950):** a seed `ON CONFLICT (email)` arbiter mismatch, plus **both** migration loaders (`applyFileMigrations` AND `migrateDatabase`) failing silently — `migrateDatabase` logged at debug and only when the message lacked *"already exists"*, and neither returned a count, so six call sites said `complete { applied: N }` whether 0 or 5 failed. Now both return `{applied, failed}`. Claims: `tsc` clean, api-gateway vitest **294/294 both sides**.
- **#925 (KS-1046):** `PREFLIGHT PASSED.` printed identically whether 13 legs ran or 10. Now a ratio, with `INCOMPLETE` and an explicit *"This is NOT a pass. Do not quote it as one."* **Non-blocking by default; strict behind `PREFLIGHT_STRICT_LEGS=1`** — a deliberate departure, because `.githooks/pre-push` states *"a normal push is never blocked by infrastructure being off — CI is the hard gate."*
- **#924 (KS-773):** the old guard ran all 35 lock members, **skipped a broken one and printed "All standalone locks pass clean-room npm ci." exit 0.**
- **#927 (KS-1027):** four follow-ups on the KS-992 restore guard.
- **#926 (KS-927):** a `jest.mock` factory omitted `assertSafeOutboundUrl`, which `webhooks.ts:170` calls — so it was `undefined` and both positive cells 500'd **while the suite printed two ticks.**

## 🔴 WHAT THE BUILDER SAYS IS **NOT** COVERED — do not re-derive these, TEST them
1. **#924** — the dockerised `node:24-alpine` clean-room path **did not execute** (host node 24 takes the fast path).
2. **#925** — only the **3 stack-class** skips were exercised. The **8 advisory** skips use the identical mechanism and are **unproven**. *"I proved 3 of 11 and I am claiming 3 of 11."*
3. **#929** — **~21 other discarding callers of `updateUser` are NOT swept** (KS-1050 filed for the one known consequence at `users.ts:933`).
4. **#928** — **no boot-2 integration proof.** Mechanism proven from live schema + source; a clean Postgres was not stood up and booted twice.
5. **#928 / #926** — ⚠ **the leg-by-leg preflight transcript is NOT RECOVERABLE.** Their preflight passes rest on **exit code plus a positive control** (an earlier push printed `PREFLIGHT FAILED` and exited 1), not on a transcript. **Do not treat "preflight passed" on those two as transcript-backed, and do not repeat the claim without that provenance.**

## HOW TO WORK — traps that cost the builder real time
- **`services/api-gateway` is VITEST. `services/originate` is JEST.** The wrong runner gives **27 suites failed / 0 tests**, which is the all-fail signature meaning *test the tool, not the subject*.
- **A fresh worktree needs `npm ci` AND `npm run build -w packages/shared`** before anything runs.
- **A tamper that breaks compilation is not a red-proof** — the suite reddens having executed **zero** tests. Any tamper you write must still compile.
- **Do NOT pipe command output through `tail`/`head` and then read the absence as a result.** The builder made exactly that error tonight and corrected it; it is why item 5 above exists.
- **Backticks inside a JS template literal close the string.**
- **A known unexplained flake:** two events on develop baselines (api-gateway 1/293, auth 2/633), both clean on re-run, **no names captured**, and the concurrency hypothesis was **tested and refuted**. If you see a third, **capture the name BEFORE re-running**: `npx vitest run --reporter=json --outputFile=…`, then read `fullName` + `status`. A re-run destroys the evidence.

## YOUR RULES
- **Findings only. You never fix, never merge, never push, never deploy.**
- **Every finding gets: what you did, what it produced, and the control that makes the result mean something.** A zero without a control is not a finding.
- **State what you did NOT test, in the same breath.** *"Unit-proven; the click path could not be exercised"* is a complete record; a bare green tick is not.
- **Tier 1 (#929, #928) gets the through-code half AND the run-it half.** Tiers 2 get through-code: read the diff against the ticket's claim, read the tests rather than only running them, and **red-proof at least one assertion per PR** — build the product with the property REMOVED and prove the check fails.
- **This is round 1 for every class.** Nothing here is at the two-NO-GO cap.
- **Report per PR: GO / GO WITH FINDINGS / NO GO**, with severities. **Mail the verdict to `wednesday-agent@agentmail.to` — a verdict that lives only in your scrollback is one pane-close from being lost, and that has happened in this fleet.**

## HOLDS
**No merge. No deploy. Demo and UAT are HELD by Kam and you do not touch them.** No contact with Peter or Stuart. **Migration 048 must be applied before any deploy of #928 or #929 — that is not yours to do, but if you find anything that bears on it, say so loudly.**
