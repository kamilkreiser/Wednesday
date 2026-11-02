# QA Gate 100 verdict: Secuura/Distributed_Secuura PR 1918 (KS-1933, billing: one Stripe purchase credited once; new `services/billing/src/creditGrants.ts`, `routes/webhooks.ts`, migration 056), TIER 1 (MONEY, design fix), stacked on PR 1913

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** I ran the REAL webhooks router, mounted as `src/index.ts` mounts it (`express.raw` on `/webhooks`), with the real logger (wrapped, pass-through), the real `@secuura/shared` errorHandler and the real `/replay` route with a signed admin JWT. I replaced only `../db` and `../services/stripeService`. My `../db` stand-in is my own. It matches each statement by its FULL SQL text, so an edited statement falls through to "unknown", and every cell recorded 0 unknown statements. I ran it at base (PR 1913's head `5d6bd74d`, webhooks.ts sha `f97aa90c…`) and at head (`d411445f`, webhooks.ts sha `903e84d7…`), 33 cells each (scripts/probe.test.ts, logs/probe_{base,head}.jsonl).
**Exactly once holds in every reachable case.** Two events for one purchase, in either order, concurrent, or concurrent with the first credit failing: base 2, head **1**. A throw after the grant, ordinary or unreadable, at either handler, then redelivered: base 2, head **1**. A finalise rejection, ordinary or unreadable: base 2/3, head **1**. Two purchases by one customer (4 events): base 4, head **2**. Replay of a credited event: base 3, head **1** (`creditsAdded:0`). Replay of a never-credited event: **1**.
**Fail-closed holds.** When the claim INSERT rejects (ordinary or unreadable), the result is 500 with 0 grants, the event row is released, and the redelivery gives 1 grant. A mark-granted failure answers 200 with 1 grant, and the row stays `granting` and blocks the other event and a replay.
**Real PostgreSQL** (my own throwaway postgres:15-alpine, removed by its recorded id): the migration applied twice gives rc 0 both times, and the second prints NOTICE "already exists, skipping". **21/21** checks pass on the statements read FROM the head's creditGrants.ts, including two-connection races (commit gives 0, rollback gives 1), a `failed` row contended by two transactions (exactly 1 wins), and 20 concurrent claims (fresh and `failed`), each with exactly **1** winner. Both planted controls are caught: with the WHERE removed, 7 checks fail (20 winners). With DO NOTHING, 3 fail.
**Re-measured:** red-first 16 failed / 6 passed (16 AssertionError). Green 22/22. Suite 343 -> 365 (17 -> 18 files). tsc 18 -> 18 and 2 -> 2 with identical multisets. eslint 0. docs-fragments rc 0 with both planted defects caught. Mutants: **15 of 18 killed**, all by AssertionError. The 3 survivors are unreachable or benign (G100-F4). merge-tree onto develop `92a26320` is clean, has the same patch-id as the stack, and uses 056 only: across all **1838** PR heads, open and closed, no other PR adds a migration numbered 056 or above.
The notes are two RECOMMENDED operational items. A row stranded at `granting` gets no recovery from the code (G100-F1). The deploy order matters, because the code fails closed without the table (G100-F2).

## Heads
- START (logs/head_start.log, 2026-11-02T01:29:10Z): PR 1918 head `d411445fff316b442fc64eb65169c19d0e0249e2` (= claim), PR 1913 head `5d6bd74daa3e0d29092524a59be182e3d31abb15` (= claim), develop `92a26320e30a…`. PR 1918 is 1 commit and its parent is PR 1913's head.
- END (logs/head_end.log, 2026-11-02T01:43:17Z): all three are **unchanged**. Local HEAD is `d411445f`, the working tree is clean, and the product sha256 values are webhooks.ts `903e84d7…` and creditGrants.ts `b94ecf93…`.
- PR body not read (no isolated Secuura gh login; global one not used, rule 5). I used the author's design, BUILT AND PROVEN and READY mails in evidence/ and the commit.

## 1. Diffstat (three-dot vs PR 1913's head; logs/diffstat.log, numstat.log)
9 files, **+805/-13**, exactly as claimed. ARCHITECTURE.md +1/-1, migration 056 +30, creditGrants.ts +142, webhooks.ts +36/-12, the new test +530, the ks1868 handler test +21, the ks488-c4 test +2, and the flow/cheat fragments +22/+21. Nothing outside the declared paths. develop since the stack base `03977e89` touches no billing, migrations or ARCHITECTURE.md path.

## 2. Hunks (logs/product_diff.log)
- webhooks.ts: imports `grantCreditsOnce, checkoutPaymentKey, describeThrown`. `finaliseEvent`'s catch: `err?.message` becomes `...describeThrown(err)`. `releaseClaim`'s catch: the same. Both handlers take the `event` (id and type) and call `grantCreditsOnce` instead of `addCertificationCredits`. A `null` (claim lost) returns 0, and the checkout handler now returns `creditsAdded` (0 when skipped) instead of `certifications`. **Not changed:** PR 1913's three hunks, every status and body, claimEvent, the KS-488 claim rule, the replay route, `creditsAdded` metadata check, the admin credit route, stripeService.
- creditGrants.ts (new): it holds the four statements, `describeThrown`, `checkoutPaymentKey` and `grantCreditsOnce`. The order in `grantCreditsOnce` is: claim (INSERT … ON CONFLICT DO UPDATE … WHERE status='failed' RETURNING). If the claim is lost, READ and warn, then return null. If the claim returns no row and no row exists, throw. Then the credit. If the credit throws, mark 'failed' (its own failure is logged) and rethrow. Then mark 'granted', whose failure is logged and not thrown.
- migration 056: CREATE TABLE IF NOT EXISTS only (§E).

## 3. Key questions

### A. Exactly once (real router; logs/probe_{base,head}.jsonl; GRANTS = credit calls that succeeded)
| cell | base (PR 1913 head) | head | head answers / rows |
|---|---|---|---|
| A1 cs then pi, clean | 2 | **1** | 200, 200; pi key granted; 2nd logs warn "already granted…" status granted |
| A2 pi then cs | 2 | **1** | 200, 200 |
| A3 both in flight (credit held) | 2 | **1** | 200, 200 |
| A3b in flight, first credit FAILS, then its redelivery | (base cell invalid: no ledger, so the held credit blocked both requests) | **1** | 500 / 200 (0) / redelivery 200 re-claims `failed` and grants |
| A3c same event sent twice concurrently | 1 | 1 | 200 / 200 duplicate |
| A4 post-grant ordinary / unreadable (checkout), redelivered | 2 / 2 | **1 / 1** | 500 (row failed) then 200 |
| A4b post-grant ordinary / unreadable (payment_intent), redelivered | 2 / 2 | **1 / 1** | 500 then 200 |
| A5 finalise rejects ordinary / unreadable, redelivered, then the other event | 2 / **3** | **1 / 1** | 200, duplicate, 200; event row stays processing (designed) |
| A6 credit fails AND release rejects ordinary / unreadable; redelivery; admin replay | 1 / 1 (unreadable: NO ANSWER, 1 unhandled) | 1 / 1 (both 500, 0 unhandled) | redelivery duplicate (stranded, logged "needs manual replay"); grant row `failed`; replay credits once |
| A6b post-grant throw AND release rejects; redelivery; other event | 2 / 2 (unreadable NO ANSWER) | **1 / 1** | 500 / duplicate / 200 (0) |
| A7 single clean + redelivery | 1 | 1 | 200 / duplicate |
| A8 two purchases one customer, both events each | 4 | **2** | two `pi:` rows granted |
| A9 replay of a credited event (twice) | 3 | **1** | replay 200 `creditsAdded:0` |
| A9b replay of the purchase's other event | 3 | **1** | `creditsAdded:0` |
| A10 replay of a never-credited event, then redelivery | 1 | 1 | replay credits 5; redelivery duplicate |
| A11 session with no PaymentIntent (`cs:`), replay, redelivery | 2 | **1** | `cs:` row granted |
| A12 session with an EXPANDED payment_intent object, then pi | 2 | **1** | keyed `pi:` |
| B7 residual: Stripe applied, then the call throws; redelivered | 2 | 2 | the stated residual, unchanged (as designed) |
| B8 the two events carry different credits (pi 3, cs 5) | 2 | 1 | first event's amount wins (G100-F6) |
No reachable cell grants 2. No cell skips a paid purchase silently: every 0-grant outcome (A6 before replay, B5, B6) leaves a `failed` or `granting` row and an error or warn log (§B).

### B. Fail-closed (same probe)
- **Claim INSERT rejects** (B1, ordinary Error with code/amount fields, and a revoked Proxy): head 500 INTERNAL_ERROR, 0 grants, 0 unhandled, event row released to `failed`. Redelivery 200, **1** grant. Base, for comparison: 200 and 1 grant on the first delivery (no ledger). It is not a silent "already granted": mutant M2 (swallow as already granted) and M3 (swallow as won) are both killed by T8a/T8b.
- **Claim returns no row AND no row exists** (B2, impossible on PostgreSQL): 500, then the redelivery grants once.
- **READ after a lost claim rejects** (B3): 500, 1 grant in total, the claim-lost path never credits.
- **Mark-granted UPDATE rejects** (B4, ordinary and unreadable): 200, **1** grant, row stays `granting`. The same event's redelivery is a duplicate, the other event gets 0, and an admin replay gets 0 (`creditsAdded:0`). Logged `Credit granted but its grant row could not be marked granted {paymentKey, eventId, errorType, errorFields}`.
- **Process died between claim and credit** (B5; state seeded: grant `granting`, event `processing`): redelivery duplicate; the other event 200 with 0 and warn `Credit for this payment already granted or in progress — not granting again {…, status:"granting", ageSeconds}`; admin replay 200 `creditsAdded:0` with the same warn. **0 grants. Confirmed: it skips with a log.** **Recovery offered by the code: none.** Replay cannot recover it, and the replay answer does not say why it added 0. Manual only: check the customer's Stripe balance, then use `POST /admin/credits` (billing.ts, KS-1850) or `UPDATE billing_credit_grants SET status='failed'` followed by a replay. Base, for comparison: the other event grants and the replay grants again (2). See G100-F1.
- **Credit throws AND mark-failed rejects** (B6): 500. The row stays `granting` with error log `Credit not granted and its grant row left granting — needs manual reconciliation`, then the redelivery and the other event 200 with 0 and warn. **0 grants, logged, not silent.** Base gives 2 here. This is a new zero-grant path that needs two failures in one request (G100-F1).

### C. SQL semantics on a real PostgreSQL (scripts/pgproof.mjs; logs/pg_migration_twice.log, pgproof_real.log, pgproof_planted_*.log)
Container `gate100-pg-ks1933`, id `fb0a356765e0…` (logs/pg_container_id.txt), from local postgres:15-alpine, bound to 127.0.0.1 on a random port, and removed with `docker rm -f <id>` (rc 0, 0 left). The `docker ps` before and after lists are identical (gate65-pg and s-w13-pg untouched).
- Migration applied twice: `CREATE TABLE` rc 0, then `NOTICE … already exists, skipping` rc 0. `\d` shows the PK `payment_key`, CHECK credits > 0, and CHECK status IN (granting, granted, failed).
- The statements are extracted by regex FROM head creditGrants.ts, not retyped. 21/21 PASS. A fresh claim gives 1. Claims on granting and on granted give 0. READ returns status and age. Mark-failed leaves a granted row alone. A failed row is re-claimable and names the new event. Four constraint refusals fire (credits 0, credits -1, null customer, bad status). Race: B waits on A's uncommitted claim, then gets **0 after COMMIT and 1 after ROLLBACK**. A failed row with two contenders gives exactly 1. **20 concurrent claims give 1 winner** (fresh key) and **1 winner** (failed key). `cs:` and `pi:` keys are independent.
- Planted controls: with the WHERE removed, 7 FAIL (claims on granting and granted win, the race B wins, 20/20 winners). With `DO NOTHING`, 3 FAIL (a failed row is never re-claimable). Each control exits rc 1.
- Read, not run: through pgbouncer, `query()` is autocommit per statement (`queryWithTenantGuc` without a scope = plain `pool.query`; with a scope, BEGIN … COMMIT around the one statement). Neither changes ON CONFLICT semantics.

### D. The key
- stripe 14.25.0 is installed (node_modules/stripe/package.json). `types/Checkout/Sessions.d.ts:177-180`: `payment_intent: string | Stripe.PaymentIntent | null`, "The ID of the PaymentIntent for Checkout Sessions in `payment` mode." The service uses `apiVersion '2023-10-16'` (stripeService.ts:95). Both session creators use `mode: 'payment'` (:307, :362) and copy `certifications` onto the PaymentIntent via `payment_intent_data.metadata` (:332-337, :385-390). No caller passes `params.metadata` (billing.ts:477, :521), so the two copies are identical. `payment_intent.succeeded`'s object IS that PaymentIntent, so `pi:<session.payment_intent>` equals `pi:<paymentIntent.id>`. Measured by A1/A2/A3/A12.
- `checkoutPaymentKey` falls back to `cs:` ONLY when `payment_intent` is neither a string nor an object with a string `id`. A webhook payload carries it unexpanded (a string). The replay route re-runs the stored payload, so the key is the same on every delivery of one event. **A cs: key and a pi: key for one purchase would double-grant** (A13, hypothetical: 2). That needs a completed payment-mode session with a null `payment_intent` while a PaymentIntent exists. By Stripe's documented behaviour, `payment_intent` is null at completion only when no payment was required, and then there is no `payment_intent.succeeded` to collide with. That last step is read from Stripe's semantics, not run against Stripe (G100-F8). An `unpaid` (delayed-method) completion also carries its PaymentIntent, so it is keyed `pi:` (KS-1934 is a separate issue).

### E. The migration
`Blockchain/Dev/migrations/056_ks1933_billing_credit_grants.sql`: one `CREATE TABLE IF NOT EXISTS`, no ALTER, DROP, INSERT or UPDATE (read whole). It is **additive only**. **056 is unique**: develop ends at 055, and across all 1838 `refs/pull/*/head` (open and closed) the only file numbered 056 or above is this one (logs/scan_056.log; the control counts 055 present in 253 heads). Conventions: `NNN_description.sql`, applied in lex order by `scripts/run-migrations.sh` (psql -f; the header says node-pg-migrate was replaced; `config.js` remains) and by the gateway's startup-migrations stage 1. A filename without "platform" routes to the main DB, where `webhook_events` (004) also lives. The grants come from `docker/init/01-create-app-role.sh:67-71` default privileges, as the file says for 049 and 053. No RLS and no tenant_id, like 004. Unlike 053, it is not mirrored into docker/init or deployment/azure/migrate/init.sql, but neither is 004's `webhook_events`, so it follows 004's precedent (G100-F2).

### F. Kam's ks1346 logging rule
New log lines (head creditGrants.ts:106, :122, :135; webhooks.ts finalise and release catches): `paymentKey`, `eventId`, `status`, `ageSeconds`, and `describeThrown` = `{errorType, errorFields}`. Measured: an ordinary Error carrying `message 'SECRET-msg cus_leak a@b.c'`, `code`, and `amount: 9900` is logged as `{"errorType":"Error","errorFields":["code","amount"]}`. **No message, amount, customer id or email.** A revoked Proxy is logged as `unreadable thrown value`, and nothing throws (M12 and M13 are killed by T5c/T6c and T5b/T6b). No new line logs a thrown object's value. **Complies.** Unchanged: PR 1913's P3 line and `releaseClaim`'s `reason` still log `error.message` (the probe shows the planted message there). The new claim path now feeds pg errors into that line too. pg messages name relations and constraints, and the values sit in `detail`, which is not logged (G100-F9).

### G. The two existing stand-in test files
`git diff pr1913 pr1918` on them shows **0 removed lines**. ks1868 handler test: +21 (a `grants` map, three ledger branches placed BEFORE the release branch, `grants.clear()`). ks488-c4: +2 (claimWins also wins the grant claim). `expect(` counts are 31 = 31 and 30 = 30, and `it(` counts are 5 = 5 and 10 = 10. Both files pass at base and at head (343 at base, 343 + 22 = 365 at head). **No assertion is weakened**, and every added line is a stand-in branch.

### H. New ways to lose money or credits
1. **A paid purchase can now end at 0 grants with no code path that recovers it** (B5: process death between claim and credit. B6: credit failure plus mark-failed failure). Both are logged and leave a `granting` row. The replay route returns `creditsAdded:0` for them exactly as it does for an already-credited purchase. Base would recover these (and could double-grant). This is the designed fail-closed trade. RECOMMENDED, G100-F1.
2. **Deploying billing before the table exists makes every paid event answer 500** (the claim INSERT fails with relation-does-not-exist, the same path as B1). Stripe retries for up to about 3 days, and after that the events stop. Nothing is double-granted, and stored events stay replayable once the table exists. A missed migrations-image rebuild (the KS-564 trap) is therefore an outage of crediting, not a money error. RECOMMENDED, G100-F2. Read, not run on a box.
3. Nothing else found. The residual (B7, throw after Stripe applied) is 2 at base and 2 at head, unchanged and stated.

## 4. Re-measure (Node v26.8.1 only, NOT measured on Node 24)
- Head new file: **22/22** (logs/head_new_tests.log).
- Red-first (base webhooks.ts plus the new file): **16 failed | 6 passed**, 16 AssertionError. The controls that pass are T3c, T5a, T6a, T7, T9a and T10a (logs/red_base_new_tests.log). This equals the author's figure.
- Whole billing suite: base (PR 1913 webhooks.ts and both base test files, new file excluded) **17 files 343/343**. Head **18 files 365/365** (logs/base_whole.log, head_whole.log).
- tsc with the tests in the program (scratch configs in scripts/; logs/tsc_lint.log): service config 18 -> 18, ESM config 2 -> 2. The multisets with line numbers removed are **identical**. Examined test files 17 -> 18. The planted error is reported once. 4 of the 18 are pre-existing TS1378 in the two modified test files (G100-F7).
- eslint on the 5 changed TS files: rc 0, 0 problems. Planted control: no-debugger and no-unused-vars, rc 1.
- docs-fragments: clean rc 0, flow and cheat each 65 new. Planted unclosed `<div>` in flow and in cheat: each rc 1 naming the KS-1933 fragment. Restored by sha, rc 0 after. One cheat ADVISORY at 6235 (pre-existing on develop, see gate 95 G95-F7).

## 5. Mutants (scripts/mutants.py; product only, tests untouched, sha256-restored after every run, final both equal; run against the ks1933, ks1868-billing-webhook-stripe-* and ks488-c4 files; logs/mutants_table.jsonl)
| mutant | result |
|---|---|
| M1 lost claim ignored | KILLED T1 T2a T2b T3 T4 T8c T9b T10b T11 |
| M2 claim error swallowed as already-granted | KILLED T8a T8b |
| M3 claim error swallowed as won | KILLED T8a T8b |
| M4 impossible empty claim -> silent skip | **SURVIVED** (no cell; unreachable on PG, probe B2 shows the head behaviour) |
| M5 READ failure after a lost claim swallowed -> skip | **SURVIVED** (no cell; money-neutral: the claim was lost, so skipping is what the head already does, minus the 500) |
| M6 mark-failed removed | KILLED T3c T6c T10a + ks1868 cells |
| M7 credit failure swallowed (no rethrow) | KILLED T3c T6a T6b T6c + ks1868 cells |
| M8 mark-granted removed | KILLED T7b |
| M9 mark-granted failure rethrown | KILLED T8c |
| M10 checkout key always `cs:` | KILLED T1 T2a T2b T6c T7b T8c T9b |
| M11 checkout key ignores an expanded object | **SURVIVED** (no cell; webhook payloads never expand; probe A12 shows the head behaviour) |
| M12 describeThrown logs the message | KILLED T5c T6c |
| M13 describeThrown rethrows an unreadable value | KILLED T5b T6b |
| M14 PI handler bypasses the ledger | KILLED T1 T2a T2b T8c T9b |
| M15 PI handler keyed on the event id | KILLED T1 T2a T2b T8c T9b |
| M16 checkout reports credits when skipped | KILLED T10b |
| M17 finalise catch rethrows | KILLED T5a T5b |
| M18 release catch reads message | KILLED T6b T6c |
15/18 killed, all by AssertionError (0 syntax/transform signals). The 3 survivors are G100-F4.

## 6. merge-tree (logs/merge_tree.log)
Onto develop `92a26320` (= ls-remote at START and END): rc 0, tree `a3fc3c00…`, clean. It changes **13 paths**, exactly the union of PR 1913 and PR 1918 against their base `03977e89`. Its patch-id `2ce8c9c2…` equals the stack's own diff. develop since the base touches no billing, migrations or ARCHITECTURE.md path. (PR 1913 is held unmerged; if it merges first, PR 1918's own diff is the 9 paths above.)

## 7. Kam's ks1346 logging rule: see §3F. Complies.

## FINDINGS
- **G100-F1 (RECOMMENDED, money operations; measured B5/B6)** A `granting` row that is never resolved means 0 grants for a paid purchase. This happens when the process dies between claim and credit, or when the credit throws and the mark-failed UPDATE also fails. It is logged, not silent, but **the code offers no recovery**. The admin replay answers `200 creditsAdded:0`, the same answer as for an already-credited purchase, and every later event only warns. Recovery is manual: check the customer's Stripe balance, then `POST /admin/credits` (KS-1850 route), or set the row `failed` and replay. The PR body should state this runbook and say that a replay's `creditsAdded:0` does not prove the purchase was credited. Follow-up idea (not for this PR): have the replay or a status read surface the grant row's status and age.
- **G100-F2 (RECOMMENDED, deploy order)** Without the table, the claim INSERT fails on every paid event, so billing answers 500 until migration 056 is applied. That fails closed with nothing double-granted, but Stripe stops retrying after about 3 days. Before the billing image rolls, rebuild the image that bakes migrations/ (the compose `migrations` service builds from services/originate/Dockerfile; the gateway image also copies migrations/), and **verify `\d billing_credit_grants` on the box directly** (the KS-564 trap: the runner can report `failed=0` without applying a new file). Note: deployment/azure/migrate/init.sql carries neither this table nor 004's `webhook_events`, so the Container Apps template already lacks billing's tables. That is pre-existing and info for this PR.
- **G100-F3 (INFO)** Measured independently: every reachable double-grant case goes from 2 (or 3, or 4) to 1 per purchase. A finalise failure on an unreadable value goes from 3 to 1 across both events (closes G95-F2). A release failure on an unreadable value goes from no answer plus an unhandled rejection to 500 with 0 unhandled (closes G95-F3). The residual (throw after Stripe applied) is 2 at base and 2 at head, as stated.
- **G100-F4 (INFO, test gap)** 3 mutants survive: M4 (an impossible empty claim becomes a silent skip), M5 (a READ failure after a lost claim is swallowed), M11 (an expanded `payment_intent` object is ignored). All are unreachable or money-neutral today. Optional cells: a stand-in that answers the claim with no row and the READ with none (expect 500), and a session whose `payment_intent` is `{id}` (expect the `pi:` key).
- **G100-F5 (INFO)** On re-claiming a `failed` row, `DO UPDATE` sets status, event_id and event_type but not `credits` or `customer_id`. The ledger row can therefore show the first event's figures while the credit applied uses the second event's. This is bookkeeping only, because the two events carry identical metadata by construction.
- **G100-F6 (INFO)** If the two events of one purchase ever carried different `certifications`, the first event to arrive would win (B8: 3 rather than 5). That is not reachable from the current session creators (identical copies, no caller metadata).
- **G100-F7 (INFO, the author's wording)** The BUILT mail and the fragment say tsc errors are "none in a changed file". In fact 4 of the 18 (service config) are pre-existing TS1378 top-level-await errors in the two modified test files (ks1868 handler test 2, ks488-c4 2). They are identical before and after apart from line shifts. All other figures re-measure exactly: 9 files +805/-13, red 16/6, 22/22, 343 -> 365, 18 -> 18 and 2 -> 2, eslint 0, mutants (theirs 10/10, my 15/18 on a different set), and the SQL (theirs 22/22, mine 21/21 on my own checks).
- **G100-F8 (INFO, read not run)** A completed payment-mode session keyed `cs:` while a PaymentIntent exists would double-grant (probe A13 = 2). By the 14.25 types plus Stripe's documented semantics, `payment_intent` is null at completion only when no payment was required, which emits no `payment_intent.succeeded`. This was not verified against live Stripe.
- **G100-F9 (INFO, logging)** `describeThrown` logs `constructor.name` and own enumerable keys. A thrown plain object with data as keys, or with an own `constructor`, could put a value in those fields. No billing throw source does this (Error, pg DatabaseError, Stripe errors). Pre-existing and unchanged: PR 1913's P3 line and `releaseClaim`'s `reason` log `error.message`, and the new claim path now routes pg errors there too (pg messages carry no row values; `detail` is not logged).

## 8. Notes for the PR body
1. G100-F1: the stranded-`granting` runbook, and the fact that a replay's `creditsAdded:0` is ambiguous. RECOMMENDED.
2. G100-F2: the deploy order (migrations image rebuilt and the table verified on the box before billing rolls; 500 until then). RECOMMENDED.
3. G100-F7: correct "none in a changed file" to "4 pre-existing TS1378 in the two modified test files, unchanged". INFO.
4. G100-F3/F4/F5/F6/F8/F9: independently re-measured; optional cells for M4 and M11; the ledger bookkeeping; the cs:/pi: dependency on Stripe semantics; describeThrown edge cases. INFO.
No FIX-BEFORE-MERGE item.

## 9. NOT TESTED
- The real PR body (no isolated Secuura gh login); CI; the pre-push hook legs (quoted from the READY mail only).
- Live Stripe: the real SDK, real event payloads (in particular `payment_intent` on a completed session, §D), Stripe's retry window, and which events the live endpoint receives.
- The migration on any box or through `run-migrations.sh` / gateway startup-migrations (applied with psql directly into my container). Privileges for the app role (`secuura_app`) on the new table (read from docker/init/01, not run). pgbouncer.
- A booted billing service, process death (B5 was seeded state, not a killed process), Node 24, the four platform suites, docs-fragments on the merged tree.
- The thrown values are synthetic (revoked Proxy, Error with fields).
- Spark shadow calibration: not run.
- Left in the workdir: `repo/` (my clone, push disabled, plus `refs/gate/pr/*` fetched for the 056 scan) and `logs/_quarantine/` (moved probe and planted files). The throwaway container is removed. Nothing was written outside the workdir. Nothing was pushed, mailed or posted.
