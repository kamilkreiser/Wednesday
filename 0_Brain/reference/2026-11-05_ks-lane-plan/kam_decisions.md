# KAM-DECISION tickets: card drafts (2026-11-05, read-only; nothing posted to the board)

17 tickets in class KAM-DECISION (non-human-owned, still In Progress at 15:4x). Each was re-read whole (description, newest comment, and for KS-843, 1084, 771, 1143, 1156, 1933 the last two comments) on 2026-11-05. Prior-ruling check: `0_Brain/dashboard/data/decisions.json` (1198 cards, read-only) searched for the ticket number and for the subject words. Where a card already rules the subject it is named under "Prior ruled card".

Card fields follow the board format: id, client_project (all `Secuura/Blockchain`), title, bluf, options, recommended, default_action. Default-if-silent rule used throughout: reversible housekeeping defaults to the recommended option; anything that changes behaviour, deletes data or touches Stripe/prod defaults to NO CHANGE.

**Summary: 17 tickets, 14 cards worth posting, 3 that need no card** (KS-1336 already ruled 2026-11-02; KS-771 and KS-1084 are not Kam-decisions, see their entries). Four more (KS-692, KS-843, KS-1143, KS-1494) are decisions already largely made; the card only asks the residual.

---

## KS-692 (High) status revoke/unrevoke: when to build "bind-creator"
Prior ruled card: `secuura-ks692-status-revoke-interim-posture` (ruled a, 2026-09-16: narrow now, bind-creator later) and `secuura-ks1116-presentation-credential-ownership-model` (ruled bind-creator, 2026-09-13). The ownership MODEL is ruled; only timing is open.
- id: `secuura-ks692-status-revoke-bind-creator-1105`
- client_project: Secuura/Blockchain
- title: KS-692: build the creator-bound check on the status revoke/unrevoke routes now, or leave the platform-only interim?
- bluf: Today only platform roles can revoke or un-revoke a credential through `/api/status/:id/revoke`; an ISSUER_ADMIN in another tenant cannot (safe, deployed at b1fb543640e7). Credential revoke (`/api/credentials/:id/revoke`, KS-1851) is already creator-bound, so the two revoke doors admit different callers. You ruled the model; this asks only whether to build it now.
- options:
  - a: Build bind-creator on the status routes now (an Opus seat, same pattern as KS-1851), gated.
  - b: Keep the platform-only interim until a tenant admin or Platform S needs to revoke on their own.
- recommended: a, because the model is ruled, the pattern exists next door, and today's two doors disagree.
- default_action: b (no behaviour change; ticket stays open, re-ask at next triage).

## KS-771 (High) review stream tracker: keep or close
Prior ruled card: none found (no card names KS-771). NOT a Kam decision in substance: a tracking ticket, block approved 2026-10-22, four streams recorded as the standing process; six of seven children are open on their own tickets.
- id: `secuura-ks771-review-stream-tracker-1105`
- client_project: Secuura/Blockchain
- title: KS-771: close the build/supply-chain review-stream tracker, now that its children carry their own state?
- bluf: The test block (changes 842 to 848) was approved and the streams are written into DEV-PROCESS. KS-1149, 664, 657, 418, 412, 365 stay tracked on their own tickets, so the tracker adds nothing a reader cannot get from them.
- options:
  - a: Close the tracker; children keep their own state.
  - b: Keep it open until all children are Done.
- recommended: a (a tracker that mirrors six open tickets goes stale; the 10-22 approval is on record).
- default_action: a (reversible board housekeeping). Peter is the reviewer of the stream, so note the close on his thread.

## KS-843 (Medium) erasure scope gate: when does the `subjects:erase` flip happen
Prior ruled cards: `secuura-erasure-scope-gate` (ruled A, 2026-09-02: dedicated subjects:erase scope) and `secuura-ks889-platform-s-key-remint-1102` (ruled b, 2026-11-02: no re-mint; decide the flip on other evidence or keep logged grace). The 11-02 comment on the ticket already records "no re-mint; flip waits; logged grace continues". Same subject, ruled.
- id: `secuura-ks843-erasure-flip-trigger-1105`
- client_project: Secuura/Blockchain
- title: KS-843: what evidence flips SUBJECTS_ERASE_SCOPE_ENFORCED, given you ruled no re-mint?
- bluf: The gate is built and deployed in logged-grace mode. Existing Platform S keys carry no connector link (a backfill recovers 5 of 32), so the log cannot prove Platform S moved to the new scope on its own. Without a trigger the ticket waits forever.
- options:
  - a: Keep logged grace; flip once the grace log shows zero un-scoped Platform S erasure calls over 30 days.
  - b: Pick a hard flip date and give Stuart written notice (he re-mints on his side).
  - c: Park to Backlog with a note; revisit when the KS-577 rotation window is discussed.
- recommended: a, because it needs no new ask of Stuart and the log is already collecting.
- default_action: a.

## KS-1084 (Urgent) gateway to originate calls send no x-tenant-id
Prior ruled card: `secuura-ks1084-part-b-api-batch-surface-unauthenticated-dead` (ruled a, 2026-09-22: part B tabled, KS-1243 carries it). No other card. NOT a Kam decision in substance: the open P0 item is an unmeasured cross-tenant effect needing a two-tenant LOCAL stack (a build/measure task for a seat, class NEEDS-DISPOSABLE-STACK).
- id: `secuura-ks1084-keep-p0-1105`
- client_project: Secuura/Blockchain
- title: KS-1084: keep Urgent until someone drives one read and one write as a non-default-tenant caller on a local stack?
- bluf: The forwarding was fixed for two sites (PR 1211) but nobody has measured whether the other gateway-to-originate calls land in DEFAULT_TENANT_ID. Part B waits on KS-1243 (dead /api/batch). The ticket has had no work since 2026-09-25.
- options:
  - a: Keep Urgent; a seat runs the two-tenant local measurement (read and write) this week.
  - b: Drop to High until the measurement is scheduled.
  - c: Leave as is.
- recommended: a (local, disposable, no prod contact).
- default_action: a (agent-workable without approval).

## KS-1098 (Medium) k6 runner echo mask: the credential-name set
Prior ruled card: none. The ticket itself says "the name set is Peter's to confirm": the real owner of this decision is Peter, so also listed in human_owned.md.
- id: `secuura-ks1098-k6-mask-name-set-1105`
- client_project: Secuura/Blockchain
- title: KS-1098: widen the k6 runner's masked-name set to any credential-shaped name, and redact BASE_URL userinfo?
- bluf: The runner masks a fixed word set when it echoes its docker command. QA-958-2: credential-shaped names outside that set, and a BASE_URL carrying user:pass@, still print in clear. QA-958-1 and 3 are fixed (PR 961). Nothing leaks on today's shipping CLI paths.
- options:
  - a: Redact BASE_URL userinfo and widen the name set (suffix match: _KEY, _TOKEN, _SECRET, _PASSWORD, _PASS, PWD).
  - b: Redact BASE_URL userinfo only; keep the name set.
  - c: Leave both.
- recommended: a (cheap, one file `systemTest/performance/runner/k6_docker.ts`, gate recommends the userinfo part either way).
- default_action: b (the gate-endorsed half; do not widen the set without Peter's confirmation).

## KS-1143 (Medium) ks781 LEG F guard walk: close with the disclosed limit?
Prior ruled card: none for KS-1143. The indirect-invocation false negative was ruled out of scope earlier (per the 09-25 merge comment). CONT-DEFERRED (a guard defined but never called inside a parser continuation) went to KS-1316, whose only PR (1268) was closed unmerged.
- id: `secuura-ks1143-close-with-disclosed-limit-1105`
- client_project: Secuura/Blockchain
- title: KS-1143: close it now that both gate findings are merged and the leftover shapes have their own ticket?
- bluf: PRs 1212 and 1248 merged and close GF-1 and GF-2 (tests only, no deploy). What remains is a disclosed limit plus KS-1316, which is the right home for CONT-DEFERRED.
- options:
  - a: Close KS-1143; KS-1316 carries the remaining shape.
  - b: Keep open until KS-1316 is built.
- recommended: a.
- default_action: a (reversible board housekeeping).

## KS-1156 (Medium) AUTH4 gate records: the forward-only refresh window
Prior ruled card: none. The ticket's own item C is addressed to you via Wednesday.
- id: `secuura-ks1156-oauth-refresh-window-1105`
- client_project: Secuura/Blockchain
- title: KS-1156: accept that OAuth refresh tokens minted before the label fix expire on their own (default 7 days), or revoke them?
- bluf: A refresh token minted at the OAuth grant before PRs 983/984 carries neither client_id nor authMethod, so it passes the new guard and still refreshes into a normal session until it expires (JWT_REFRESH_EXPIRES_IN, default 7d; the value on kintsugi/demo is UNMEASURED). The fix deployed 2026-11-01, so the window closes about 2026-11-08 on the default. The same ticket also carries a Polish item (R-C3: the 401 text for a label-only token says "Invalid email or password"); default is to keep it.
- options:
  - a: Accept; let the old tokens expire; no deploy-side action.
  - b: Denylist the pre-deploy OAuth refresh jtis on each box (needs a read of live token ids).
  - c: Force re-authorisation by rotating the signing secret (logs everyone out).
- recommended: a (short window, already mostly elapsed, b and c touch live sessions).
- default_action: a.

## KS-1336 (Medium) per-tenant DB readiness parent
Prior ruled card: `secuura-ks1336-per-tenant-db-priority-1102` (ruled a, 2026-11-02: downgrade High to Medium, keep parked until per-tenant DBs are planned). Same subject, ruled this week. **No card needed.** The ticket is parked by ruling; it should leave the In Progress count (board-only move to Backlog is the only residual, and the ruling said "state unchanged").

## KS-1491 (Low) mock-completeness guard: its blind spots
Prior ruled card: none.
- id: `secuura-ks1491-mock-guard-blind-spots-1105`
- client_project: Secuura/Blockchain
- title: KS-1491: teach the mock-completeness guard four mocking shapes it cannot see, or record them as accepted limits?
- bluf: Items 1 and 2 (negative-twin cells) are merged. The guard cannot see `setMock`, `unstable_mockModule`, an aliased `jest`, or a non-literal module name; none is present in the corpus today. Test-only, no runtime risk.
- options:
  - a: Accept; record the four shapes as documented limits in the guard header (item 3).
  - b: Extend the guard to all four shapes with cells.
- recommended: a (nothing in the corpus uses them; b is pure maintenance cost).
- default_action: a.

## KS-1493 (Low) the unversioned /api/verification* 307s are counted by no limiter
Prior ruled card: `secuura-ks1234-production-307-1104` (ruled a, 2026-11-04: build a production-mode regression test for the same 307 behaviour). Related subject, different question (that one pinned the redirect; this asks whether it should be rate-limited).
- id: `secuura-ks1493-unversioned-307-limiter-1105`
- client_project: Secuura/Blockchain
- title: KS-1493: is an unbounded flood of the unversioned /api/verification 307 redirects acceptable?
- bluf: In production the redirect is counted by no limiter (305 of 305 requests passed in the gate's test). A 307 reaches no handler, so a flood costs only the redirect itself. Counting it would also double-count a client that legitimately follows the redirect.
- options:
  - a: Accept; write the reasoning beside the limiter block and pin it with a cell.
  - b: Count the unversioned redirect in the global limiter (drop the prefix from READ_ONLY_PATHS for that spelling only).
- recommended: a (cost is one redirect; b penalises legitimate followers).
- default_action: a.

## KS-1494 (Medium) KS-968 follow-ups: legacy plaintext email row now leaves the id row active
Prior ruled card: none naming KS-1494 or KS-968's seed; item 5 is the open ruling, items 2 and 3 are fixes (lane A of lanes.md would take them; not decisions).
- id: `secuura-ks1494-seed-legacy-email-row-1105`
- client_project: Secuura/Blockchain
- title: KS-1494: when the platform-admin email row has no lookup hash, the new seed leaves the id row ACTIVE where the old code suspended both rows. Keep that?
- bluf: The PR 1485 rewrite (deployed 2026-11-01) is not "otherwise unchanged" for a legacy plaintext email row: old code suspended both rows, new code keeps the id-row active. Suspending both is what locked the admin out originally (KS-968). The change is deployed; nothing is broken today.
- options:
  - a: Accept the new behaviour; correct the PR text and the doc claim "otherwise unchanged".
  - b: Restore suspend-both for the legacy plaintext case.
  - c: Migrate legacy plaintext email rows to lookup hashes, then delete the special case.
- recommended: a (avoids the lockout; b reintroduces it).
- default_action: a (no behaviour change).

## KS-1499 (Medium) KS-1311 test gaps: no CI runs the originate integration suite
Prior ruled card: none. F1, F2 and F5 delivered (PR 1792); N1 is a recording decision.
- id: `secuura-ks1499-manual-integration-run-1105`
- client_project: Secuura/Blockchain
- title: KS-1499: write the manual run command for the originate integration suite into DEV-PROCESS, or just say it is manual?
- bluf: Nothing under `.github` runs the originate integration config (GitHub Actions is retired for this repo), so this suite and its predecessors are a manual instrument. N1 asks whether to write the run command into `docs/DEV-PROCESS.md` under "Manual CI-gate equivalents" or accept and say so.
- options:
  - a: Record the command in DEV-PROCESS (one docs paragraph).
  - b: Accept and say so on the ticket; no docs change.
- recommended: a (a suite nobody can find does not get run).
- default_action: a.

## KS-1524 (Medium) document-lookup log line: cap its length?
Prior ruled card: none. Items (a) to (c) delivered; (e) is a measurement on the deployed ingress (a seat task, not a decision).
- id: `secuura-ks1524-cap-document-lookup-log-line-1105`
- client_project: Secuura/Blockchain
- title: KS-1524: cap the document-lookup error log line (about 15 KB worst case), or accept it uncapped like the 500 handler?
- bluf: If a database error echoes a maximal caller value the logged line reaches about 15 KB, and an object with 100k fields makes one huge string. The 500 handler (`fail500`) has the same exposure, so a cap here alone would leave the two inconsistent.
- options:
  - a: Cap the line at a fixed length here and in `fail500` together (one small PR with a cell).
  - b: Accept uncapped; write it down on the ticket.
- recommended: a (log volume is billed; one change covers both sites).
- default_action: a.

## KS-1534 (Medium) connector allow-list: an array of non-strings
Prior ruled cards: `secuura-connector-allowlist-missing-setting-ks1256-1005` (ruled b: a missing setting keeps "no restriction") and `secuura-ks1348-r2-files-still-leak-allowlist` (unrelated). Different question: a MALFORMED stored value, not a missing one. KS-1230 (write-side element validation) went Done today.
- id: `secuura-ks1534-allow-list-array-of-non-strings-1105`
- client_project: Secuura/Blockchain
- title: KS-1534: should both allow-list read routes refuse a stored array that contains non-strings?
- bluf: The connector-info reader echoes `[1,2]` or `[null]` raw and the create path would refuse every create with the wrong message text, so the two answer differently for the same stored value. With the write side now validating elements (KS-1230), such a value should not be storable.
- options:
  - a: Refuse in both reads with one shared message (fail closed on a malformed value).
  - b: Leave the reads; rely on the write-side validation.
- recommended: a (small, consistent with the fail-closed fixes in KS-1231, and a belt over KS-1230).
- default_action: b (no contract change without your word).

## KS-1548 (Medium) platform audit-log: a final window that answers after the deadline
Prior ruled card: none; Wednesday's earlier ruling ("a spent budget discards the platform half") is quoted on the ticket and m3 asks whether it applies to a last window that is late but complete.
- id: `secuura-ks1548-late-final-window-1105`
- client_project: Secuura/Blockchain
- title: KS-1548: when the last audit-log window arrives after the time budget, serve its complete rows late, or drop the platform half?
- bluf: Measured: a last window that took 1.5 times the budget was served after 3021 ms against a 2000 ms budget. The rows are complete, never partial. Dropping them would make the response silently incomplete, which is what KS-1545 complained about; a deadline check would not bound the time anyway (a slow body is outside every timer, m1).
- options:
  - a: Keep serving the complete late rows; record the rule and pin it with a cell.
  - b: Add the post-body deadline check and discard the platform half.
- recommended: a.
- default_action: a (no change to a request path).

## KS-1585 (Medium) KS-1570 PR B inputs: what happens to scope rows when the admin is deleted or demoted
Prior ruled card: none naming KS-1585 (KS-1570 shape-b rulings are quoted in the code docstring). The Minors m1 and m2 are fixes, not decisions.
- id: `secuura-ks1585-scope-rows-on-admin-change-1105`
- client_project: Secuura/Blockchain
- title: KS-1585: when an admin who has organisation-scope rows is deleted or loses ADMIN, delete the rows or keep and ignore them?
- bluf: The new organisation-scope table has no foreign keys. PR B (the writer) must validate at write time and decide what becomes of rows when a user is deleted or changes role. Rows left behind are harmless today (they only narrow) but they outlive the user and are personal data keyed on `user_id`.
- options:
  - a: Delete in the same transaction as the user delete or demotion, with an audit row.
  - b: Keep the rows; the readers apply a row only while the user is still ADMIN in that tenant.
  - c: Refuse to delete or demote an admin who still has scope rows.
- recommended: a (rows never outlive their meaning; fits the erasure obligations).
- default_action: b (non-destructive; nothing is deleted without your word).

## KS-1933 (High) one Stripe purchase credited more than once: the residual
Prior ruled card: `secuura-billing-possible-double-credit-two-stripe-events-1102` (ruled a, 2026-11-02: file a ticket; a seat designs and tests the fix through the QA gate; nothing deployed without your tap; you check the Stripe endpoint's event list once). Same subject. PR 1918 is merged and migration 056 is applied on kintsugi. Open: (1) the one-time Stripe event-list read is YOURS and not recorded as done (an action, not a decision); (2) the residual below.
- id: `secuura-ks1933-stripe-payment-key-residual-1105`
- client_project: Secuura/Blockchain
- title: KS-1933: close the last double-credit gap by writing the payment key into the same Stripe customer update?
- bluf: The fix credits once per payment. One gap remains by design: if the credit call throws AFTER Stripe applied the update, the payment is marked failed and credited again on redelivery. Closing it needs the payment key written into the same Stripe customer update, a new Stripe-side field. Also: a row stuck in `granting` by a process that died needs a manual check, and purchases credited before the migration have no row (no backfill).
- options:
  - a: Build it (an Opus seat, through the QA gate, nothing deployed without your tap).
  - b: Accept the residual and document it; add a periodic check for rows stuck in `granting`.
  - c: Build only a reconciliation report that lists payments credited twice.
- recommended: a (money; the whole ticket exists to prevent this).
- default_action: b (no Stripe-side change without your tap).
- also owed (not a decision): your one-time read of the live Stripe endpoint's event list (do both `checkout.session.completed` and `payment_intent.succeeded` fire to the endpoint).
