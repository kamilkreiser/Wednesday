# QA Gate 95 verdict: Secuura/Distributed_Secuura PR 1913 (KS-1868, services/billing/src/routes/webhooks.ts, three catches of `router.post('/stripe')`: O55-P1 :166 signature / O55-P2 :184 claim / O55-P3 :215 handler), TIER 1 (money-adjacent)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** On Q1 (P3, the paid-event site) I ran the REAL webhooks router, mounted the way `src/index.ts:50` mounts it (`express.raw`), with the real logger (spied, pass-through) and the real `@secuura/shared` errorHandler. I replaced only `../db` (an in-memory `webhook_events` claim table that follows the claim / release / finalise SQL semantics) and `../services/stripeService` (the credit call `addCertificationCredits` plus a `constructWebhookEvent` stub). I ran it at base `03977e89a343` and at head `5d6bd74daa3e` (scripts/probe.test.ts, logs/probe_{base,head}.jsonl). **The author's STOP-RULE table re-measures exactly.** Head-A (unreadable value from the credit call, then a clean redelivery) gives 500, row `failed`, 0 unhandled, redelivery `200 {"received":true}`, row `processed`, **1 grant**. That is identical, cell for cell, to base-C and head-C (an ordinary Error). Base-A gives no answer, the row stays `processing`, 1 unhandled rejection, and the redelivery is answered `200 {"received":true,"duplicate":true}` with **0 grants**: the paid event is skipped. P1 and P2 (Q2) persist nothing at either version. Head answers 400 'Invalid signature' and 503 exactly as an ordinary Error does. At base the same two sites give no answer and an unhandled rejection.
**Q3, measured, in one line:** reading (ii) is unchanged, and reading (i) is unchanged for an ordinary Error. Reading (i) gains one more input, an unreadable value thrown after the grant, which goes from 1 grant to 2 (the ordinary-Error figure). See Q3 and G95-F1.
Other figures re-measure exactly: 6 files +606/-3; red-first 7/12 failed by assertion, 5 controls green; green 12/12; suite 331 -> 343 (14 -> 17 files); tsc with the tests in the program 12 -> 18 (service config, the 6 new are TS1378 on the new files' top-level awaits) and 2 -> 2 (ESM config, byte-equal); eslint 0. Mutants: 18 of 20 killed. The 2 survivors are the known readable-non-Error branch (G95-F4). merge-tree onto develop is clean with 0 shared paths, on the brief's develop `cde2dee4` and again on `b8874803`, which develop reached while I worked (G95-F6).

## Heads
- START (logs/head_start.log, 2026-11-01T22:38:03Z): PR head `5d6bd74daa3e0d29092524a59be182e3d31abb15` (as expected), develop `cde2dee4dffba6a61228c40d641ff567660c32b2` (as expected). One commit. Its parent is the merge-base `03977e89a343` (logs: `git log`, merge-base).
- END (logs/head_end.log, 2026-11-01T23:03:02Z): PR head `5d6bd74d...` **unchanged**. Local HEAD is the same, the product sha256 `f97aa90c351f9158...` equals the author's figure, and the working tree is clean. **Develop MOVED** during the gate: `cde2dee4` -> `c8d77dce` (KS-1868 auth) -> `b8874803` (KS-1868 nft). Neither touches billing or any PR path. I re-ran merge-tree onto `b8874803` (Q6).
- Billing is byte-identical between the base and both develops (`git diff --quiet ... -- services/billing` rc 0), so "base" means one product file throughout (sha256 `18f4fc26f74c...`).
- **PR body not read directly.** No Secuura `gh` login is isolated for this session, and I did not use the global one (rule 5). I used the author's READY and BUILT AND PROVEN mails (evidence/) and the commit message.

## FINDINGS
- **G95-F1 (RECOMMENDED, wording; measured; reading (i))** The fragment says "by reading and not run, a hostile value thrown after the grant now takes that same path". This gate measured it, with `logger.info('Payment status')` made to throw after `addCertificationCredits` succeeded. Base: no answer, row `processing`, 1 unhandled, redelivery acknowledged as a duplicate, **1 grant** in total. Head: 500, row `failed`, redelivery processed, **2 grants**. That equals the ordinary-Error post-grant case at base and at head (2 grants). So for this one synthetic input, head grants more credits than base. Base's single grant was an accident of the crash, not a design, and it came with an unanswered request and a process-fatal unhandled rejection on Node >= 15 (billing registers no `unhandledRejection` handler, grep in src). The STOP rule (the after-state equals what an ordinary Error gets) holds, so this is not a block. The PR body should state the measured 1 -> 2 plainly, so that Kam's card (secuura-billing-possible-double-credit-two-stripe-events-1102) has it.
- **G95-F2 (INFO for this PR, pre-existing, money, measured base = head; follow-up KS-1868 site)** `finaliseEvent`'s catch (webhooks.ts:110-111) reads `err?.message` unguarded. It runs AFTER the grant. With an ordinary Error from the finalise UPDATE: 200, row stays `processing`, redelivery a duplicate, **1 grant** (the designed outcome, per the docblock at :86-88). With an unreadable rejection the read throws a TypeError out of `finaliseEvent`, which goes into the P3 catch: 500, claim released, redelivery processed, **2 grants**. Base and head are identical (probe cells N-finalise-*). So at this site an unreadable value already gets an outcome an ordinary Error does not, and it is a double grant. It is not in this PR's hunks and this PR does not change it, but it belongs on Kam's card next to reading (i) and in the KS-1868 site list.
- **G95-F3 (INFO, pre-existing, measured base = head; follow-up KS-1868 site)** `releaseClaim`'s catch (:129-135) also reads `err?.message` unguarded. An unreadable rejection from the release UPDATE throws out of the P3 catch, AFTER this PR's guard. The result is no answer, 1 unhandled rejection, the row left `processing`, the redelivery acknowledged as a duplicate and 0 grants (probe N-release-revokedProxy, base = head). An ordinary Error there gets 500 and the same stranded row (the designed "needs manual replay" path). `claimEvent`'s catch (:77-79) has the same unguarded read, but its TypeError lands in the P2 catch and gets 503, so it is harmless.
- **G95-F4 (LOW, test gap)** M6 (the readable non-Error branch `String(error)` -> `'x'`) SURVIVES at P2 and P3. No cell throws a readable non-Error. That branch is not changed by this PR. The same gap as G90-F3 and earlier.
- **G95-F5 (INFO, the author's own figure)** The BUILT mail says "flow 20 lines, cheat 22 lines". numstat gives flow **22**, cheat **20**. The total +606 is right.
- **G95-F6 (INFO)** Develop moved twice during the gate (cde2dee4 -> c8d77dce -> b8874803, both other KS-1868 services). merge-tree onto `b8874803` is clean, 0 shared paths, and has the same patch-id. docs-fragments passes on that merged tree too.
- **G95-F7 (INFO)** docs-fragments prints a cheat ADVISORY at line 6235. It is on develop alone (logs/frag_develop_now.log), so it does not come from this PR. I saw one advisory, where the author's run had two (6249 and 6235). The flow one does not appear on the current develop.

## Q1. P3, the paid-event site (real router; logs/probe_{base,head}.jsonl, logs/probe_runs.log)
Each cell is one delivery, followed by one clean redelivery of the same event id. "Stripe receives" is the HTTP answer on the loopback. "No answer" means none arrived inside a 2.5 s client deadline.

| case | version | Stripe receives (1st) | row after 1st | unhandled | redelivery answer | row at end | GRANTS |
|---|---|---|---|---|---|---|---|
| A revoked Proxy from credit call | base | NO ANSWER | processing | 1 | 200 {received:true,duplicate:true} | processing | **0** (skipped) |
| A revoked Proxy | head | 500 INTERNAL_ERROR 'Webhook handler failed' | failed | 0 | 200 {received:true} | processed | **1** |
| A' throwing message getter | base | NO ANSWER | processing | 1 | 200 duplicate | processing | 0 |
| A' throwing message getter | head | 500 | failed | 0 | 200 {received:true} | processed | 1 |
| C ordinary Error from credit call | base | 500 | failed | 0 | 200 {received:true} | processed | **1** |
| C ordinary Error | head | 500 | failed | 0 | 200 {received:true} | processed | **1** |
| control: clean, then redelivery | base = head | 200 {received:true} | processed | 0 | 200 duplicate | processed | 1 |

DB call sequences: head-A = head-C = base-C = `claim,release,claim,finalise`. Base-A = `claim,claim`. Logs at head-A: `[Webhook] Error handling checkout.session.completed: {"error":"unreadable thrown value"}` and `Webhook claim released for retry {"eventId":..., "reason":"unreadable thrown value"}`. **Head-A equals base-C and head-C in every column.** The raise is acceptable under the brief's rule.
Read, not run: Stripe's retry of a non-2xx answer (its documented rule), and the process exit on an unhandled rejection under plain Node (no handler in billing src; Express 4.22.3 does not catch an async handler's rejection).

## Q2. P1 and P2 (same probe)
| site / thrown value | base | head | persisted (both) |
|---|---|---|---|
| P1 ordinary Error from constructWebhookEvent | 400 'Invalid signature' | 400 'Invalid signature' | no db call, no credit call |
| P1 revoked Proxy / throwing getter | NO ANSWER, 1 unhandled | 400 'Invalid signature', 0 unhandled | no db call, no credit call |
| P2 ordinary (DB unavailable -> ClaimUnavailableError) | 503 SERVICE_UNAVAILABLE | 503 | no db call, no row |
| P2 logger.warn throws an ordinary Error | 503 | 503 | no row |
| P2 logger.warn throws revoked Proxy / throwing getter | NO ANSWER, 1 unhandled | 503, 0 unhandled | no row |
P2 is reachable with an unreadable value only through `logger.warn` in the `!isDbAvailable` branch (claimEvent wraps DB failures in its own ClaimUnavailableError). That confirms operator 55's reachability note: these are defence-in-depth sites.

## Q3. The two pre-existing money readings (Kam's card; no fix designed)
This PR leaves reading (ii) unchanged. I measured it: a `checkout.session.completed` and a `payment_intent.succeeded` for one purchase, both carrying `certifications: '5'` and no `creditsAdded` flag, delivered clean, give **2 grants at base and 2 at head** (probe cell reading-ii). The PR touches neither handler and no claim key. Reading (i), an ordinary Error thrown after the grant, is also unchanged: **2 grants at base and 2 at head** (the author's figure, re-measured). It is not made better. It does reach one more input: an unreadable value thrown after the grant goes from 1 grant at base (by the crash accident, with an unanswered request and a stranded row) to 2 grants at head, the ordinary-Error figure (G95-F1). Beside it, and outside this PR, `finaliseEvent`'s unguarded catch already double-grants on an unreadable value at base and at head (G95-F2). Kam's card should carry both.

## Q4. Kam's ks1346 logging rule
The only log lines the hunks touch are `logger.error('Webhook signature verification failed', { error: reason })` and the `error: reason` field of the claim-refusal log (P2). P3's log and `releaseClaim(event.id, message)` are unchanged lines that now receive the guarded `message`. Each logs a string: the existing expression (`String(error)` or `error instanceof Error ? error.message : String(error)`), and otherwise the constant `'unreadable thrown value'`. No object, no Stripe payload and no event body is logged. At P1 the Stripe SDK's `StripeSignatureVerificationError` carries `header` and `payload` properties, but `String(err)` gives only `name: message`, and its messages are constants (stripe 14.25.0 `cjs/Webhooks.js`). The constant fallback is the hunks' only new value. **Complies.** Pre-existing and unchanged: the existing expression logs an ordinary Error's `message` text, as the rest of the file does.

## Hunks (logs/product_diff.log)
Three hunks, webhooks.ts +20/-3, all inside `router.post('/stripe')`. P1: `String(error)` moves into `try { reason = String(error) } catch { reason = 'unreadable thrown value' }` and the log uses `reason`. P2: the same guard around `error instanceof Error ? error.message : String(error)`, and the log uses `error: reason`. P3: `const message = ...` becomes `let message` plus the same guard. Unchanged: every status and body (400, 503, 500), `releaseClaim(event.id, message)`, `return`, the claim and finalise code, every handler, the replay route and the export surface. No rethrow.

## Re-measure (Node v26.8.1 only, NOT Node 24)
- Head, 3 new files: **12/12** (logs/head_new_tests.log).
- Base product + the new files: **7 failed | 5 passed** (logs/red_base_new_tests.log). All 7 fail as `AssertionError: expected undefined to be 400/503/500`; the controls pass. Base R3 stops at its first assertion, so the committed cells cannot show the skip at base. The probe shows it (0 grants).
- Whole suite: base without the new files **14 files 331/331** (logs/base_whole_excl_new.log); head **17 files 343/343** (logs/head_whole.log).
- tsc with the tests in the program (scratch configs in scripts/, outside the repo; logs/tsc_lint.log): service commonjs config 12 -> 18. The 6 new errors are all TS1378 on lines 53/54, 57/58 and 91/92 of the three new files, and there are 0 in webhooks.ts. ESM config: 2 -> 2, byte-equal (the pre-existing chargeable-events TS6196 and webhooks-replay-auth TS18046). Examined test files 14 -> 17. Planted type error: reported once. (My first run had a config defect, TS2688 alone, and the planted control caught it reporting nothing. I fixed it with typeRoots and re-ran.)
- eslint (cwd billing): webhooks.ts + 3 tests rc 0, 0 problems. The planted file gives `no-debugger` + `no-unused-vars`, rc 1.
- docs-fragments: clean rc 0 (64 new). Four planted defects (flow unclosed div, flow `<!--n-->.` removed, cheat unclosed div, cheat `</table>` corrupted) each rc 1 naming the fragment. All restored by sha, and rc 0 after (logs/frag_check_*.log).

## Mutants (scripts/mutants.py; one site of the head product at a time, tests untouched, parsed by esbuild before running, sha256 restored after every run, all `restore: true`; logs/mutants_table.jsonl, logs/mut_*.log)
20 runs: **18 killed, 2 survived.** Every kill was by AssertionError and only in that site's own test file.

| Mutant | P1 signature | P2 claim | P3 handler |
|---|---|---|---|
| M0 drop the guard (base shape) | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 R3 |
| M2 fallback re-reads `String(error)` | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 R3 |
| M3 rethrow when unreadable | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 R3 |
| M4 constant for every value | KILLED C1 | KILLED C1 C2 | KILLED C1 |
| M5 log call removed | KILLED C1 R1 R2 | KILLED all 4 | KILLED C1 R1 R2 |
| M6 readable non-Error branch -> 'x' | n/a (no branch) | **SURVIVED** | **SURVIVED** |
| M7 unreadable path returns silently (no answer, no release) | KILLED R1 R2 | KILLED R1 R2 | KILLED R1 R2 R3 |

## merge-tree (logs/merge_tree.log, logs/merge_tree_c8d77dce.log)
- Onto `cde2dee4` (the brief's develop): rc 0, tree `73749e38...`, clean. It changes exactly the PR's 6 paths. develop-since-base touched 6 mcp-server paths, 0 shared with the PR.
- Onto `b8874803` (develop at END): rc 0, tree `e1495ed4...`, clean. It changes exactly the PR's 6 paths, patch-id `b23468c9...`, the same as the PR's own diff. 17 develop paths since the base, 0 shared. docs-fragments on that merged tree: rc 0, 67 new (logs/frag_merged_b887.log).

## Notes for the PR body
1. G95-F1: replace "by reading and not run, a hostile value thrown after the grant now takes that same path" with the measured figures: base 1 grant (no answer, row stranded, redelivery a duplicate), head 2 grants, the same as an ordinary Error thrown after the grant (2 at both). RECOMMENDED.
2. G95-F2 / G95-F3: name `finaliseEvent`'s catch (:110-111, post-grant, unreadable value -> 2 grants against 1 for an ordinary Error, base = head) and `releaseClaim`'s catch (:129-135, no answer and a stranded row) as follow-up KS-1868 sites, and point to Kam's card for the money part. RECOMMENDED.
3. Q1 table: now independently re-measured on the real router by gate 95 (head-A = base-C = head-C, 1 grant). INFO.
4. G95-F4 optional cell (a readable non-Error throw); G95-F5 the flow/cheat line counts. INFO.

## NOT TESTED
- The real PR body (no isolated Secuura gh login); CI; the pre-push hook legs (quoted from the READY mail only).
- A real PostgreSQL (the claim table is a model of the three statements), the real Stripe SDK's `constructWebhookEvent` on a real signature, Stripe's retry behaviour, a booted service, the gateway hop, Node 24, the four platform suites.
- Process death on the base unhandled rejection under plain Node: read, not run (vitest's listener counted it).
- The live Stripe endpoint's event subscriptions (whether both events of reading (ii) are actually delivered).
- Spark shadow calibration: not run for this gate.
- The thrown values (revoked Proxy, throwing getter) are synthetic. Nobody acting on the system can choose what the credit call, the logger or pg throws.
- Left in the workdir: `wt_develop/` (a git worktree of my clone, at the merged tree) and `logs/_quarantine/` (moved probe/planted files). Nothing was written outside the workdir. Nothing was pushed, mailed or posted.
