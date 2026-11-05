# DRAFTER REPORT: Seat G 27th (security service, lane E + KS-1585), 2026-11-05 17:3x AEDT

**BLUF.** Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatG_security_service.md`. Seat G, ordinal **27th** (measured max `Seat G <N>` in anchored headings of the Secuura history = 26, line 5125; 27 has 0 hits). Develop tip read `5fc5569ed96a`. SELF-CHECK stamp left as the literal `@STAMP@`. `self_check_view.sh` run: no contradiction found; no scope-gate words. **Three of the six tickets had a stale or unmeasured remaining scope in the lane plan, and one hidden sibling ticket (KS-1592) is the same defect as the KS-1585 ruling.** Nothing written outside the two files; no repo, Linear or mail write.

## Model recommendation (your call)
**Opus 5.5 for the whole seat** (`claude-opus-5-5`, read from models_latest.json). KS-1585 is row C3: it changes who may mint and revoke API keys, and the reader predicate ("still ADMIN") is a design with live case-fold questions (the writer's own predicate took PR 1539 and PR 1548 rounds 1 and 2; KS-1601 holds an open `upper(role)` fold decision). The other five are row C2 (Sonnet). Fallback written into the brief: if you launch Sonnet, ITEM 1 stops at the plan QUESTION until you send `/model claude-opus-5-5` (model-routing section 7) or route KS-1585 to an Opus seat, and the seat starts with KS-908.

## Tickets in order, scope as the ticket states it
1. **KS-1585** (tier 1). "The follow-up to pull request 1535 (KS-1570 PR A): three Minors and three Nits from its Opus gate, plus the inputs that PR B must honour." Included: the ruled reader change (card b, comment `bbac61ca`), **m1** (503 not 500 on a scope-read infrastructure fault; mint `:1313`, revoke `:1586`, classifier `:1183`), **m2** (`scripts/rls/verify-fail-closed.sh:53`, still absent), **n2** (comment at the integration test line 19, still overstated). n1 is done (PR 1828). **n3** (`statement_timeout`, "Optional", changes the pool for every route) is NOT built without Wednesday's word. Measured: the table has ONE SQL reader, `adminScope.ts:21`; `keyRevokePolicy.ts` only receives the array, so `packages/shared` is a named exception only if the seat measures a need (suite list and the originate importers it must RUN are in the brief; 32 files import the policy symbols).
2. **KS-908**: "connectorId persists but is invisible through the API". PR 1319 echo is on develop and deployed by ancestry. What remains (from its own merge comment): the empty-string polish and declaring `connectorId` in the response schema. The schema part regenerates `docs/openapi/secuura-api.yaml`, which **E 37th is live on**, so the brief tells the seat to stop that part and ask. Probably evidence-only.
3. **KS-1377**: buildable remainder is the revoke-path `usage_count`/`last_used_at` overwrite (`index.ts:457`). N-1338-5 is already done at the tip (`ks1370...test.ts:184`). **N-1338-4** (cache-miss read fault 200 vs 503) is "a product decision" by the ticket's own words with no ruling: the seat asks, does not build.
4. **KS-1525**: G1, G10 (PR 1601) and the `'f'` defect (KS-1639, PR 1631) are all on develop. Remaining is only the empty-string question (G7/G8), which needs a ruling; evidence-only otherwise.
5. **KS-1568**: o6 merged (PR 1628). Open: cells for M10, M3b, M7, M1, plus the large-value timer edge. The seat plants each mutant first and writes a cell only for a survivor.
6. **KS-1602**: stale in the plan. PR 1703 and KS-1734 (PR 1727, `vitest.config.ts` now 60 s hook and test budgets) landed; the third shape is optional. Evidence-only likely; a test-only Done proposal under the no-deploy-surface addendum. Lane plan routed it to the Spark; the brief gives it to the seat.

## Excluded
KS-1579, KS-1600, KS-745 (Lane X, as you said). KS-1553, KS-1594 (In Review, same service, not this seat). KS-1592 and KS-1601 (Backlog, board account): not commissioned, only read and cited. Peter/Stuart: none among the six.

## Things that looked wrong in the lane plan, and board hygiene for you
- **KS-1592 (Backlog) describes the same defect** the KS-1585 card rules on ("rows ... revive silently"; its option 2 is exactly "filter at read time"). Ruling b answers it. Who owns the build ticket (KS-1585 vs KS-1592) is your board call; the brief says the seat comments, does not move either.
- **KS-1601 (Backlog) is an open design decision** on the same predicate (`upper(role)` fold), so the reader's role comparison cannot be settled by the seat alone; the brief makes it a QUESTION before code.
- The ticket's cited line numbers for KS-1585 are stale (`:1181`/`:1419` are now `:1313`/`:1586`); the brief carries the measured ones.
- The lane plan's kam_decisions text for the KS-1585 card differs slightly from the card as queued (ruled option wording is the card's).

## UNMEASURED (each conditional in the brief)
Open PRs on `services/security/src` (gh not logged in here; ls-remote shows branches only); whether the machine can run PostgreSQL for the integration suites (the seat must not start Docker); the worktree convention; which of M10/M3b/M7/M1 are already killed (no mutant run); any live behaviour (no box contact); the seat's pane id; the live floor itself (taken from your commission). Open QUESTIONs the seat must route: empty-string normalisation (KS-908 + KS-1525), KS-1377 miss-branch status, KS-1585 liveness predicate, n3, the yaml sequencing with E 37th.

/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatG_security_service.md
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatG_security_service_DRAFTER-REPORT.md
