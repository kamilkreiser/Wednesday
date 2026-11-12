# Commission: QA GATE 347, TIER 2, on PRs 2222 (KS-1912) and 2223 (KS-1776), Secuura/Blockchain, 2026-11-13 07:5x AEDT

Commissioned by Wednesday. Findings only: nothing fixed, posted, mailed, pushed, merged or written to Linear. Work only in `scratch/` of THIS folder; write `verdict.md` here.

## Copy-and-change
Template: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate346-tier2-pr2220-2221/commission.md` (read WHOLE) and its `verdict.md` (the admin external-config method that worked: reuse it for PR 2222). Clone notes: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate345-pr2079/tier.md` last paragraph (core.sshCommand from the project's repo config).

## Subjects (pins by Wednesday's ls-remote 07:54:07 AEDT; re-pin before the first measurement and before the verdict)
- develop e3cd5d6c204beafafffa3c677f9e8628f34b2a54 (moves: B 168th is merging PR 2177 in services/originate now; re-pin).
- PR 2222 (KS-1912, REFUSAL HALF ONLY) head 39035798163ab367857602c14d830c2225d9680b: frontend/admin src/services/api.ts (+5 -4: updateTenantStatus and deleteTenant return { ok, error? } and use the existing describeFailure import), src/pages/platform/ClientList.tsx (+11 -2: a destructive Alert on a refused status move or Delete), new ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx (+79, 4 cells). Base 410feda1a85e.
- PR 2223 (KS-1776) head 8752357228cdc9650b5b7cc5f2383b61a8fdb7d8: services/auth src/routes/auth.ts (+10 -3: the demo-user seed timer wraps seedDemoUsers in try/catch with a shared logSeedFailure) + new ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts (+102, fake timers). Base 1dd6299bccd6.
- The author's READY FOR GATE (Seat R 116th, 20:53:12Z) is in `/private/tmp/wed_newmail/batch_20261112T205352Z.txt` (read its R 116th section; quote nothing you did not re-measure).

## Tier
Tier 2 (Wednesday's STAMP item 5). KS-1776 lives in the auth service's routes module but changes only error handling around a seeding timer; if you find it changes any login, token or session behaviour, STOP and write `tier.md`.

## Questions
1. Scope vs ticket (Linear read-only): KS-1912 is claimed as the REFUSAL HALF only: confirm the body says so and nothing claims the Delete confirm-text half. KS-1776: the ticket proposed no fix; is try/catch + one log line the minimal correct shape, and does the async rejection path still log exactly once?
2. KS-1912: every caller of updateTenantStatus and deleteTenant at the head (git grep the whole frontend, not only ClientList.tsx; positive control). A caller expecting a boolean is a finding. PR 2159 (open) edits lib/settingsSavePayload.ts where describeFailure lives: does its diff change that function? Red-first under the external admin config as gate 346 ran it.
3. KS-1776: red-first (the new file against develop's auth.ts RED by assertion, green with the change); the whole services/auth suite on the MERGED tree (count, not rc: the seedDemoUsers whole-suite rc 1 flake, G321-PRE-1, is exactly what this touches; run it several times and report rc per run); tsc both auth configs (tsconfig.test.json has 41 develop-side diagnostics: report yours against develop's).
4. merge-tree of each PR against current develop, both orders, planted conflict refusing; the pair has 0 shared paths: confirm.
5. docs-fragments: reproduce the author's NO-PAIR.

Verdict format: line 1 `PR 2222: <GO | GO WITH NOTES | NO GO> (at head <full sha>; tier 2)`, line 2 the same for PR 2223; FOUND / TESTED / HOW / NOT TESTED; findings G347-<pr>-N. Do not write to /tmp. Model: Sonnet. Return a 10-line summary.
