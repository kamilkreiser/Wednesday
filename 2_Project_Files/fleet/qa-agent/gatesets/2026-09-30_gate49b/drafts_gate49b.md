# gate49b DRAFTS — every client-facing drafted comment, sentence by sentence (claims_gate49b.py, 2026-09-30T07:49:13Z)

Source: the READYs VERBATIM in mail_gate49b_ready.md. Tag = the drafter's LEXICAL read (a word match), never a ruling: the gate rules each sentence TRUE (with its instrument) / FALSE / UNMEASURED, and each draft POST AS-IS / AMENDED / DO NOT POST.

## C1 — Kam's ruling (a) in #1357's body

- label: `Keep serving, flag it on /health` — present verbatim: True
- detail: `The migration run returns its failed count. /health reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the deploy reads as failed. The running service is not stopped.` — present verbatim: True

## D-KS-1054-1357 — Seat B 49th's drafted KS-1054 comment (8 sentences; from the READY for #1357)

| id | sentence (verbatim) | drafter's lexical tag | gate: TRUE / FALSE / UNMEASURED + instrument |
|---|---|---|---|
| D-KS-1054-1357-1 | Follow-up to the exit-status note above. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1357-2 | That note covers python3 being ABSENT. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1357-3 | This change closes the remaining case: a python3 that is PRESENT BUT BROKEN — on PATH, but exiting non-zero — was read as "the /health body is not JSON" and the check exited 2 (PASS-WITH-SKIP), so a deploy whose migration status could not be read did not fail. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1357-4 | It now exits 1 and names the parser, matching the absent case. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1357-5 | A genuinely non-JSON body still exits 2, pinned by a control cell. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1357-6 | Proved red-first on macOS and in python:3.12-slim (bash 5.2.37, coreutils 9.7, Python 3.12.14): with the predicate at its previous state the two new cells fail and nothing else does; with the change the suite reads 40 passed, 0 failed on both runners. | INSTRUMENT-NAMED | |
| D-KS-1054-1357-7 | Each cell's fixture guard is asserted green, so neither red is vacuous. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1357-8 | Not covered: the macOS python3 shim case is not reproducible on this Mac and is unmeasured on a Mac without developer tools; deploy.sh and deploy-all.sh were not driven end to end with a broken-python3 stub; the scripts were not run against any real environment, so a live sweep is owed and remains blocked on KS 1380. | INSTRUMENT-NAMED | |

**Verdict for this draft (the gate):** POST AS-IS / AMENDED (give the amended text) / DO NOT POST — and whether it repeats or contradicts KS-1054 comment 49aff833 (2026-09-29T16:23:17Z; it already says python3 ABSENT now fails the deploy in both scripts).

## D-KS-1054-1359 — Seat B 49th's drafted KS-1054 comment (5 sentences; from the READY for #1359)

| id | sentence (verbatim) | drafter's lexical tag | gate: TRUE / FALSE / UNMEASURED + instrument |
|---|---|---|---|
| D-KS-1054-1359-1 | A second exit-status follow-up, on the callers rather than the predicate. rc 1 from the startup check means either that migrations failed or that the check could not be verified, but both callers printed a line claiming they FAILED. deploy.sh:857 now reads "FAILED or could not be verified" and deploy-all.sh:312's smoke value reads "failed or could not be verified"; deploy-all.sh still fails against "0 failed", so nothing about the pass/fail outcome moves. | INSTRUMENT-NAMED | |
| D-KS-1054-1359-2 | Message text only — no exit code, counter or branch changed, and a control cell in each new suite pins that rc 1 still counts an ERROR and rc 2 still counts a SKIP. | INSTRUMENT-NAMED | |
| D-KS-1054-1359-3 | Proved red-first on macOS and in python:3.12-slim: with the previous wording exactly one cell in each suite fails and the controls stay green; with the change each suite reads 4 passed, 0 failed. | INSTRUMENT-NAMED | |
| D-KS-1054-1359-4 | The deploy-all.sh twin was not named in the original finding; it was found by a screen of the same class. | NO-INSTRUMENT-WORD | |
| D-KS-1054-1359-5 | Not covered: neither script was driven end to end, and neither was run against any real environment, so a live sweep is owed. | INSTRUMENT-NAMED | |

**Verdict for this draft (the gate):** POST AS-IS / AMENDED (give the amended text) / DO NOT POST — and whether it repeats or contradicts KS-1054 comment 49aff833 AND #1357's drafted KS-1054 comment (two follow-ups on one ticket).

## D-KS-1395-1358 — Seat D 1st's drafted KS-1395 comment (14 sentences; from the READY for #1358)

| id | sentence (verbatim) | drafter's lexical tag | gate: TRUE / FALSE / UNMEASURED + instrument |
|---|---|---|---|
| D-KS-1395-1358-1 | BLUF: both advisories this ticket names are CLEARED at develop as of #1356's merge, but they were cleared by #1354 and #1355, and a DIFFERENT set of six advisories is what actually kept pushes frozen after this ticket was raised. | INSTRUMENT-NAMED | |
| D-KS-1395-1358-2 | Measured at develop 3e3a68260d0e and at #1356's head 52dadb07f70d (`npm run audit:gate`, `npm run audit:locks` from Blockchain/Dev, each rc on its own line): GHSA-r53p-7pc4-xj5r — NOT reported as new at either SHA. | INSTRUMENT-NAMED | |
| D-KS-1395-1358-3 | It appears only in leg 6's CLEANUP block: "- GHSA-r53p-7pc4-xj5r (undici, KS-470)", under "15 baseline entries are no longer reported — remove". | NO-INSTRUMENT-WORD | |
| D-KS-1395-1358-4 | Mechanism: frontend/issuer and the root lock both pin undici 7.30.0, so the vulnerable 5.29.0 is gone. | NO-INSTRUMENT-WORD | |
| D-KS-1395-1358-5 | GHSA-r3ph-w7gj-g6xm — does not appear anywhere in either leg at either SHA, and is in NO baseline row (26 rows parsed). | NO-INSTRUMENT-WORD | |
| D-KS-1395-1358-6 | Mechanism: systemTest/performance pins js-yaml 5.4.2. | NO-INSTRUMENT-WORD | |
| D-KS-1395-1358-7 | So this ticket's "done means" items 1 and 2 are already satisfied without a new baseline row. | NO-INSTRUMENT-WORD | |
| D-KS-1395-1358-8 | SEPARATELY, and this is the part the ticket could not have known: at develop 3e3a68260d0e leg 6 was rc 1 with 4 NEW and leg 7 rc 1 with 6 NEW — three brace-expansion (two high), one fast-uri, and two ip-address in services/mcp-server alone. | INSTRUMENT-NAMED | |
| D-KS-1395-1358-9 | Those six were published after this ticket was raised at 02:52Z and are what re-froze pushes. #1356 (merged as 377989cf3829) closes all six: at its head both legs are rc 0. | INSTRUMENT-NAMED | |
| D-KS-1395-1358-10 | One correction to the ticket's routing note: the r53p baseline row's `ticket` field reads KS-470, which is why leg 6 prints "(undici, KS-470)". | INSTRUMENT-NAMED | |
| D-KS-1395-1358-11 | Its `reason` does cite Kam's 2026-09-30 ruling and predicts its own obsolescence in as many words. | INSTRUMENT-NAMED | |
| D-KS-1395-1358-12 | No row was edited. | NO-INSTRUMENT-WORD | |
| D-KS-1395-1358-13 | Not measured: whether the row should now be removed as stale. | INSTRUMENT-NAMED | |
| D-KS-1395-1358-14 | That is the CLEANUP question, which is a separate piece of work. | NO-INSTRUMENT-WORD | |

**Verdict for this draft (the gate):** POST AS-IS / AMENDED (give the amended text) / DO NOT POST — and whether it repeats or contradicts any other comment on the ticket.

## D-KS-1387-1358 — Seat D 1st's drafted KS-1387 comment (18 sentences; from the READY for #1358)

| id | sentence (verbatim) | drafter's lexical tag | gate: TRUE / FALSE / UNMEASURED + instrument |
|---|---|---|---|
| D-KS-1387-1358-1 | BLUF: the three failures are real and are fixed by #1358. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-2 | Two claims in this ticket did not survive measurement, and one of them matters because it would put a gate in place that cannot catch this bug. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-3 | 1. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-4 | `Blockchain/Dev/.dockerignore` DOES exclude `packages/shared/node_modules`. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-5 | Line 19 is `packages/*/node_modules`, which matches it. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-6 | Present at 0aa9b52c6 and 8c810023f (both SHAs this ticket and KS-1380 were measured at), at 8af6ab821600, d9ce1403d158, 3e3a68260d0e, 52dadb07f70d and 377989cf3829 — seven of seven — and present since the file was created (3115fa752). | INSTRUMENT-NAMED | |
| D-KS-1387-1358-7 | No later negation re-includes `packages/*`; the only negations in the file are `!docs/openapi` and `!connectors/whatsapp-bot`, and the latter is re-narrowed on the next two lines. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-8 | So the second route to TS2742 described here does not exist, and the remaining route is the @types disagreement. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-9 | 2. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-10 | The suggested `tsc --noEmit` over every service in the PR gate would be GREEN on this bug. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-11 | At develop 52dadb07f70d, where all three images FAIL, `npx tsc --noEmit` in services/analytics, services/billing and services/governance is rc 0 with ZERO `error TS` lines — all three. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-12 | The reason is structural: on the host, npm workspace hoisting resolves ONE copy of `@types/*` from the root, while each image has two — `/app/node_modules` from the service's lock and `/shared/node_modules` from packages/shared's. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-13 | The annotation fix suggested here (`const router: Router`) is still worth doing on its own merits, but it addresses one symptom site, not the cause. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-14 | What does work is KS-1380's own suggestion: assert every service lock agrees with packages/shared on the @types it re-exports. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-15 | Measured, that check is rc 1 at the base naming all 15 disagreeing locks, and rc 0 at #1358's head. | INSTRUMENT-NAMED | |
| D-KS-1387-1358-16 | It is written and run but deliberately not committed in #1358 — wiring the pre-push hook is gate code and wants its own review. | NO-INSTRUMENT-WORD | |
| D-KS-1387-1358-17 | Also found while building every service one at a time: `services/queue` and `services/guardian` sit behind `profiles: [phase2]`, so `docker compose config --services` omits them and a default `docker compose build` never touches them (34 services resolved, 31 with a `build:` section). | INSTRUMENT-NAMED | |
| D-KS-1387-1358-18 | Relevant to any per-service gate proposed here or on KS-1379: it would silently skip those two unless it enumerates profiled services. | NO-INSTRUMENT-WORD | |

**Verdict for this draft (the gate):** POST AS-IS / AMENDED (give the amended text) / DO NOT POST — and whether it repeats or contradicts any other comment on the ticket.

## D-KS-1380-1358 — Seat D 1st's drafted KS-1380 comment (11 sentences; from the READY for #1358)

| id | sentence (verbatim) | drafter's lexical tag | gate: TRUE / FALSE / UNMEASURED + instrument |
|---|---|---|---|
| D-KS-1380-1358-1 | BLUF: fixed by #1358, 15 package-lock.json only, 27 entries moved, 0 added, 0 removed, no manifest change. | INSTRUMENT-NAMED | |
| D-KS-1380-1358-2 | The three failing images build; the ten latent ones stay green. | NO-INSTRUMENT-WORD | |
| D-KS-1380-1358-3 | The mismatch was wider than the three that fail, as this ticket says: 15 locks disagreed with packages/shared, not 11 — the workspace root and connectors/whatsapp-bot are in it too, and services/shared and services/vc-issuer disagree on only one of the two packages (vc-issuer disagrees UPWARD on pg, 8.21.0 against shared's 8.23.1, while already matching on esc). | INSTRUMENT-NAMED | |
| D-KS-1380-1358-4 | Measured from every lock at four SHAs. | INSTRUMENT-NAMED | |
| D-KS-1380-1358-5 | One correction to the description: at d9ce1403d it is not true that "every lock agreed". services/mcp-server (esc 4.19.9) and services/vc-issuer (esc 4.19.9, pg 8.21.0) disagreed there too, and that build passed. | INSTRUMENT-NAMED | |
| D-KS-1380-1358-6 | A disagreement is therefore not sufficient for the failure — what fails is a type inferred or passed across the /shared boundary. | NO-INSTRUMENT-WORD | |
| D-KS-1380-1358-7 | That is why exactly 3 of the 15 fail today and 12 are latent, and it is measured, not inferred: 13 services built one at a time at two SHAs, 3 fail at both, 10 rc 0 at both. | INSTRUMENT-NAMED | |
| D-KS-1380-1358-8 | What #1358 does NOT do: it moves none of KS-1379's ~1,000-entry drift, so the runtime majors #1339 pulled in stay (services/queue bullmq 5.76.2->5.81.5 with msgpackr 1->2; services/m365-integration and packages/shared @azure/identity 4.13.1->4.13.3 with @azure/msal-node 5->6). | NO-INSTRUMENT-WORD | |
| D-KS-1380-1358-9 | KS-1379's deploy hold is unaffected. | NO-INSTRUMENT-WORD | |
| D-KS-1380-1358-10 | The alternative direction — regenerate each lock from its committed pre-#1339 version — was measured and is not admissible as written: it regresses brace-expansion in four locks and fast-uri in two (no named target moves them back), leaves 1,097 entries still differing from the base, and overshoots its own targets (nodemailer@^10.0.12 resolves to 10.0.13). | INSTRUMENT-NAMED | |
| D-KS-1380-1358-11 | It does fix this ticket as a side effect, as predicted, by putting packages/shared back to esc 4.19.8 / pg 8.20.0 — the cost is what rules it out. | NO-INSTRUMENT-WORD | |

**Verdict for this draft (the gate):** POST AS-IS / AMENDED (give the amended text) / DO NOT POST — and whether it repeats or contradicts any other comment on the ticket.

## C3 — every `<script>.sh:<line>` cited, resolved at develop / the owning PR head / END

| cite | cited in | develop | PR head | END |
|---|---|---|---|---|
| deploy-all.sh:281 | PR body #1357, ruling card | `local actual="$3"` | `local actual="$3"` | `local actual="$3"` |
| deploy-all.sh:312 | PR body #1359, READY #1359 | `smoke_test "Startup migrations" "0 failed" "one or more failed"` | `# rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer` | `# rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer` |
| deploy.sh:823 | PR body #1357, ruling card | `log_info "Checking API gateway health..."` | `log_info "Checking API gateway health..."` | `log_info "Checking API gateway health..."` |
| deploy.sh:857 | PR body #1359, READY #1359 | `log_error "  API Gateway: startup migrations FAILED — see above"` | `# rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer` | `# rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer` |
| push45.sh:110 | READY #1358 | (unmapped) | | |
| run-migrations.sh:190 | ruling card | (unmapped) | | |

## C4 — per-file +a/−d claims in the PR bodies vs the pinned numstat

- #1359 `Blockchain/Dev/deployment/azure/deploy.sh`: body +2/−2 | numstat +3/-1 | **DIFFERS**
- #1359 `Blockchain/Dev/deployment/azure/deploy-all.sh`: body +2/−2 | numstat +3/-1 | **DIFFERS**
