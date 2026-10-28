# QA gate 12 (batch, findings only): Secuura #1801 round 1 (TIER 1, KS-1240 option b keyPending) and #1795 round 1 (TIER 2 Claude half, KS-1780 parts 1+3)

**ROUTING RECEIPT:** model: opus -- tier-1 gate row (fleet/specs/model-routing.md) -- weekly gauge 90% (a guide per Kam 2026-10-22; tier 1 has no promoted local gate; #1795's tier-2 Claude half is batched into this session to avoid a second gate session, Kam's 2026-09-18 batch rule).

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), subagent of Wednesday. Spark review model: deepseek-v4-flash via the tunnel (`spark_status.py` at start: tunnel UP, queue 0, idle 89 min).
- **Pushed / merged / commented / Linear / mail:** nothing. `gh` not used (PR bodies NOT read; commit messages stood in, flagged to Spark).
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate12/repo` (path did not exist; `git clone --shared .../spark/cache/src`; `rev-parse --show-toplevel` asserted equal to the path before the first fetch; origin re-pointed to GitHub, Secuura deploy key via GIT_SSH_COMMAND). All git writes (fetch, worktrees, merge-tree objects) there only. Worktrees: `/private/tmp/claude-501/gatework12/{w1801, w1801base, w1795}` + spark_gate's own `sg1801`. Mutated product files were restored from `git show HEAD:` and `git status --porcelain --untracked-files=no` read back empty after every mutant (asserted in the drivers). Scratch left in my worktrees only: `gate12-probe.test.ts` (w1801, w1801base), the PR test copied into w1801base, node_modules symlinks. Nothing deleted.
- **node_modules:** read-only symlinks to the Secuura checkout's `Blockchain/Dev/node_modules` (as gate 11). `npm run check:openapi` builds `packages/shared` - it wrote to MY worktree's `packages/shared/dist` (05:39), the checkout's dist is untouched (mtime Oct 12, checked). **Host Node v26.8.1 (not LTS 24)** on every run.
- **Containers:** none started (no DB needed: both PRs' cells and my probes use a pg recorder / jest mocks). `docker ps -a` shows 0 `gate12` names. No port 5432/6432/6433 touched.
- **Processes:** only vitest/jest/npm runs I launched (foreground or my own background scripts); all exited. One background `grep` of my own (card search) stopped by its task id. No kill by name.
- **Load:** load1 2.6-3.5 throughout; timings below are not load-distorted.

## Pins (git ls-remote)

| ref | start (18:29Z) | end (18:43Z) |
|---|---|---|
| refs/pull/1801/head | **5c158f42adba5a3ee3b13521ca6f24de91661ca3** (= brief) | same |
| refs/pull/1795/head | **3b1741524383971b85037a6f048d9bc49e58c06c** (= brief) | same |
| develop | 56062b373d6c (= brief) | **b5583cb6974a** (#1787 merged mid-gate: originate `routes/adminConfig.ts` + a ks1779 test + the two docs) |

Merge-bases: #1801 = 514a6a4915df (= brief); #1795 = bd6697e079fc (= Spark half). `git merge-tree --write-tree --name-only` of each PR with develop 56062b37 **and** with b5583cb6: conflicts are **the two Projects Documents html files only**, no code file, for both PRs. Develop since #1795's merge-base (14 commits) touches no file the PR touches except those two docs; the only originate product file develop changed is `adminConfig.ts` (#1787, KS-1779; KS-1780 part 2 territory, not in #1795). #1801 x #1795 are disjoint.

## BLUF

| PR | Verdict | One line |
|---|---|---|
| **#1801** (tier 1, round 1) | **GO WITH NOTES** | **Implements exactly Kam's option b and nothing more**, measured through the real gateway router in front of the real handler at the **real 3 s bounds**: 201 kept on every path, `keyPending: true` + `keyPendingMessage` on all 11 non-delivery shapes I drove (down, hung 3015 ms, slow 3500 ms, body trickled past the bound, 401/403/500/400 refusals, null body, HTML 200, non-JSON 502 in the PR's cells, both hung 6008 ms), `keyPending: false` and no message on all 3 delivery shapes; writes unchanged (5 calls, 0 DELETE, NULL hash on failure), no status change, no 503, no rollback. Red-proof 9/3 and 12/12 x5 and 47/47 and check:openapi rc 0 all reproduced. **Flag is vault-key only by design**: a failed metering mint leaves `keyPending: false` (answer to (b): metering is NOT covered; that is the PR's stated reading of "a key nothing currently uses", not an omission). Notes: an answer with **no `success` field** and an answer with `success: true` but **no `keyHash`** are unpinned (mutants survive); the docs/commit red-proof figure says **10/2, measured is 9/3**; the gateway adds an undeclared `data` field so KP10's "declares no field it does not publish" holds for the upstream body only. No fix-before-merge. |
| **#1795** (tier 2, Claude half) | **GO WITH NOTES** | Does what KS-1780 parts 1 and 3 ask, narrowly: 12/12 head; the two catches are correct (`isZodError` only swallows a throw from `instanceof`; `extractPgCode` wraps the unchanged reader). My 7 valid mutants: **all killed** (catch-returns-true, call site reverted, always-false, wrapper without try, wrong code in the catch, meta candidate dropped, try covering `code` only). The wrapper fixes all 6 `extractPgCode` callers at once (fail-safe direction). Spark half's 0-defect judgement stands. Notes: a `message`-getter-only hostile value is unpinned (single try covers it; pin gap only), and `gdpr.ts:139` reads `err?.pgCode` **before** the now-safe `extractPgCode` (outside the ticket's 17 sites; unmeasured). Merge-in: docs-only conflicts. |

**Merge order:** independent (disjoint code; docs-only conflicts with develop and each other). Either first; docs renumbering at prep as usual (#1801 carries section 96 PROVISIONAL).

---

## #1801 (KS-1240 option b): GO WITH NOTES

Diff vs merge-base 514a6a4: 8 files, +376/-2 (= brief). Product: `index.ts` +22/-1 (const `KEY_PENDING_MESSAGE`; `error?` on the result type; `describeKeyRefusal()`; `let keyPending`; `else` branch sets the flag + new warn line; catch sets the flag and its existing warn line gains `{ tenantId, slug }`; two fields appended to the 201), `tenant-provisioning.openapi.ts` +10 (`keyPending: z.boolean()`, `keyPendingMessage: z.string().optional()`), yaml +11 (two properties + `keyPending` in `required`), 2 md docs, the 12-cell test, 2 html docs.

### (a) Exactly option b, nothing more? YES

Kam's card (verbatim from the brief): option [b] "Explicit 'key pending' flag" - "Keep 201 and add a pending flag and message to the published response plus the log line; changes the public API for a key nothing currently uses."

| element | present | evidence |
|---|---|---|
| 201 kept | yes, every path | probe: all 21 rows 201 (head), status passes through the real gateway router (`res.status(r.status)`) |
| pending flag in the PUBLISHED response | yes | yaml + openapi source; gateway spreads `...upstream` so the flag reaches the caller (probe, via gateway) |
| message | yes, only when true | probe `hasMessage` = keyPending on every row |
| log line | yes | not-ok answers now log (`FORBIDDEN Role X ...`, `INTERNAL_ERROR m...` capped at exactly 200 chars, `no error code` for a body with no envelope); base logged nothing on a 403 (measured, base probe A6/A7: `logs: []`) |
| no status change / no 503 | none | `git diff` has no `res.status(` change; probe |
| no rollback of the orphan key row (KS-1789's) | none | probe: `deletes: 0` on every row; KP8 pins the 4 writes |
| anything else | only: existing catch warn line gains `{tenantId, slug}`; `describeKeyRefusal` helper | disclosed in the commit message; harmless |

"a key nothing currently uses" = the vault key file: the real tokenisation `generate-key` has answered `{success, keyId, keyHash, ...}` with no key since AUDIT B-5 (read: `tokenisation/src/index.ts:254-262` at head), so the success body has no `keyFile` at all (probe A0 keys = success, tenant, meteringApiKey, keyPending, data). That supports the PR's vault-key-only reading.

### (b) Is the flag set on every non-delivery path, and only there? MEASURED

Probe `gate12-probe.test.ts` (scratch, my worktree): the **real `createPlatformRoutes` router** (api-gateway `routes/platform.ts`, auth stubbed to SUPER_ADMIN) forwarding to the **real tenant-provisioning `index.ts`** (pg recorder, JWT pass-through - the PR's harness), fake tokenisation/security servers. **No bound shortened; gateway default deadline.** Each row waits to 7 s to catch late writes. Evidence: `out/probe1801_head.jsonl`, base subset `out/probe1801_base.jsonl`.

| row | tokenisation / security | head: status, ms | keyPending / msg | vault hash param | note |
|---|---|---|---|---|---|
| A0 control | real-shaped success / ok | 201, 15 | **false / absent** | set | base: same body minus the flag |
| A0d control, direct (no gateway) | same | 201, 14 | false / absent | set | 0 schema breaches |
| A1 | **down** (port closed) | 201, 14 | **true / yes** | NULL | log "fetch failed" + tenant |
| A2 | **hung** | 201, **3015** | **true / yes** | NULL | real 3 s bound |
| A3 | **slow 3500 ms (not hung)** | 201, 3017 | **true / yes** | NULL | tok received the request, never delivered: the real service would still have written its `tenant_keys` row (KS-1789 orphan, out of scope) |
| A4 | slow 2900 ms (inside bound) | 201, 2914 | **false / absent** | set | |
| A5 | headers fast, body completes at 3500 | 201, 3009 | **true / yes** | NULL | the bound covers the body read |
| A6 | 401 `{error:"Unauthorized"}` (no `success`) | 201, 5 | **true / yes** | NULL | log says only "no error code" |
| A7 | 403 `{success:false, error:{code,message}}` | 201, 4 | **true / yes** | NULL | log names FORBIDDEN + tenant; **base: no log** |
| A8 | 200 `{success:true}` **no keyHash** | 201, 4 | **false / absent** | **NULL** | see 1801-2 |
| A9 | 200 body `null` | 201, 12 | true / yes | NULL | TypeError caught |
| A10 | 200 `{success:"false"}` (string) | 201, 9 | **false** | NULL | truthy string; Info |
| A11 | 200 HTML | 201, 14 | true / yes | NULL | |
| A12 / A12b | 500 long message / 400 `error` as a string | 201, 4-5 | true / yes | NULL | log capped at 200; string error logs "no error code" |
| A13 / A14 / A17 | tok ok; security **down / hung / 3500 ms** | 201, 7 / 3015 / 3006 | **false / absent** | set | `meteringApiKey: null` + its own log; flag not set (by design, KP7) |
| A15 | **both hung** | 201, **6008** | **true / yes** | NULL | 1992 ms margin to the 8000 ms gateway deadline |
| A16 | legacy success with keyFile | 201, 6 | false / absent | set | keyFile delivered |

**Answer:** set on every path where the vault key is not delivered (down, hung, slow-past-bound, trickled body, every not-ok shape, non-JSON, null), cleared on every delivery. **Metering is not covered**: by design and documented ("independent of the metering key", METERING-USAGE-API.md:122; KP7 pins it). Two shapes give `keyPending: false` while no hash is recorded or the failure is masked: A8 (`success: true`, no `keyHash`) and A10 (`success` a truthy non-boolean). The real tokenisation always sends a boolean `success` and a `keyHash` on success (read), so neither is reachable from today's service; both are unpinned (1801-2).

### (c) Contract consistency, and does the guard check it?

- yaml and source agree: `check:openapi` rc 0 at head ("CHECK PASS: on-disk YAML matches generated", 414 example blocks OK) and at base. Field names, types (boolean / string), required (`keyPending`) / optional (`keyPendingMessage`) match the runtime (probe: `keyPending` always present and boolean; message present iff true). No `example` was added for either field (none needed by check:spec-examples).
- **The conformance guard checks the YAML, not the source**: mutant N9 (`keyPending` made `.optional()` in `tenant-provisioning.openapi.ts` without regenerating) -> **12/12 cells green**, `generate-openapi --check` **FAIL**. So source drift is caught only by `check:openapi`, and **no workflow under `.github/workflows/` names openapi** (`git grep -i openapi` 0 hits; positive control `runs-on` 6 hits in ci.yml). Pre-existing, repo-wide (1801-5).
- KP10 ("declares no field it does not publish") is run against the **upstream** body (`/api/tenants` direct). The **published** route is the gateway's, which adds `data: tenantObj` (KS-39 #6) - not declared in the published 201 schema: every gateway body in my probe breaches the PR's own top-level rule with `$.data: not declared`, at base and head alike (1801-4). The yaml has no `additionalProperties: false`, so this is a description gap, not a validator failure.
- Descriptions: accurate. One wording nit: the message says "the key service did not return a key" - the real service never returns a key on success either (it returns a hash); "did not confirm the key" would match the field name (Info, in 1801-3).

### (d) Red-proof, repeats, suite, mutants

| run | result |
|---|---|
| PR test at head | **12/12**; **5 of 5** consecutive runs 12/12 (`out/x5_*.txt`) |
| PR test on base product (my worktree) and spark_gate | **9 failed / 3 passed** in both: KP8 (writes pin), KP10 (conformance guard), KPC2 (warn-capture control) pass. = the seat's claim to Wednesday. **The commit message and both html docs say "10 failed / 2 passed (the writes pin and the conformance guard)"**: stale (1801-3) |
| tenant-provisioning suite at head | **7 files / 47 tests, 0 failed** |
| `tsc --noEmit -p services/tenant-provisioning` | 0 errors head, 0 base (the project tsconfig does not include tests; the seat's "2 pre-existing TS2835 including test files" was not reproduced with a test-including config - not run) |
| check:openapi | rc 0 head and base |

My mutants (`out/mut1801/summary.json`, each restored and clean-asserted):

| mutant | killed by |
|---|---|
| N1 catch path does not set the flag | KP1, KP2, KP4 |
| N2 not-ok path does not set the flag | KP3, KP5 |
| N5 message always present | KP6, KP7 |
| N7 log line copies the whole answer | KP5 |
| N8 yaml: `keyPending` not required | KP9, KPC1 |
| N10 flag placed before the existing fields | KP1-KP7 (7) |
| N11 not-ok log drops the tenant id | KP3 |
| N12 metering failure sets the flag | KP7 |
| N13 not-ok log line removed | KP3, KP5 |
| N9 source schema optional, yaml not regenerated | **none** (cells read the yaml); `generate-openapi --check` FAIL |
| **N3 `if (keyResult.success !== false)`** (an answer with no `success` field counts as confirmed) | **none - survives** |
| **N4 flag derived from `!keyHash`** | **none - survives** (differs only on A8) |
| **N6 200-char cap removed** | **none - survives** |

**9 of 12 behavioural mutants killed** (+ N9 caught by check:openapi only). The seat's "10/10 killed" is true of its own set (its list matches N1/N2/N13/N5/N7/N12/N10/N8 shapes); a different reasonable set leaves three unpinned behaviours, one of which (N3) is a plausible refactor that would silently clear the flag for a 401/404 from middleware that answers `{error: "..."}`.

### (e) Consumers of the 201 body (enumerated; none breaks)

| consumer | reads | effect of the new field |
|---|---|---|
| api-gateway `routes/platform.ts:314-348` | `r.json()`, spreads `...upstream`, adds `data`, passes status | passes through (probe) |
| admin UI `frontend/admin/src/services/api.ts:1045` + `pages/platform/ClientList.tsx:68-70` | `success`, `keyFile`, `error` | ignored; **the UI does not show the flag** (disclosed in the docs) |
| `insurance-test-runner.js:155` | status, `data.id` / `id` | none |
| e2e-v2 `tier1-api/multi-tenancy.api.spec.ts:31,77` | status < 500, `data.id` | none |
| schemathesis `tests/isolation_tenant_fixtures.py:32` (`created_tenant_id(created.json())`) + response-conformance against the published spec | id; spec conformance | none on a stack built from the same commit; **rollout-order note**: if the published spec reaches an environment before the service does, the old service's 201 lacks a now-REQUIRED field (unmeasured, Info) |
| `scripts/smoke-test.sh:344`, `deployment/azure/deploy-all.sh:331,356`, `systemTest/inline-runner/runner.js` | GET / status codes only | none |
| api-gateway `ks1215-...test.ts:413-419` | status + forwarded headers, mocked upstream | none |
| tenant-provisioning `ks1240b` test | its own bodies | 47/47 green |
| SDK | none found (`git grep` keyFile/meteringApiKey in packages/: only a masking key list) | - |

### Findings (#1801)

| # | Sev | Class | Finding | FOUND / TESTED / HOW |
|---|---|---|---|---|
| 1801-1 | Low | ticket (or 1-cell add at merge) | **An answer with no `success` field is unpinned.** Today it sets the flag (A6: 401 `{error:"Unauthorized"}` -> keyPending true), but mutant N3 (`success !== false`) turns that into `keyPending: false` with all 12 cells green. Add a cell: a 401 whose body has no `success`. | TESTED: probe A6 (head) + mutant N3 12/12 green. Control: N2 (the `success:false` path) is killed by KP3/KP5. |
| 1801-2 | Low | ticket | **`keyPending: false` does not guarantee a recorded hash**: `{success: true}` with no `keyHash` (A8) gives `keyPending: false`, no message, `vault_key_hash` NULL; a truthy non-boolean `success` (A10) likewise. The published description says "False when the key service confirmed the key". Unreachable from today's tokenisation (always boolean `success` + `keyHash`, read), so not exploitable; deriving the flag from `!keyHash` (N4) would close it and also survives every cell. | TESTED: probe A8/A10 head and base (A8 base: same NULL hash, no signal). Real service shape READ, not run. |
| 1801-3 | Low | merge-time wording | **Red-proof figure is stale in the commit message and both html docs: "10 failed / 2 passed (the writes pin and the conformance guard)"; measured 9 / 3** (KPC2, the warn-capture control, also passes on base). The seat's mail to Wednesday had it right. Also (Info) the message "the key service did not return a key" - the real service never returns a key, only a hash. | TESTED: base run in my worktree and spark_gate facts.json (`passed: 3, failed: 9`), identical cell lists. |
| 1801-4 | Info | ticket (pre-existing) | **Published 201 is the gateway's, which adds `data` (KS-39 #6); the schema does not declare it**, so KP10's "declares no field it does not publish" holds for the upstream body only. Every gateway body breaches that rule at base and head alike. | TESTED: probe `breachesVsPublished` = `["$.data: not declared"]` on every gateway row, `[]` on A0d direct. |
| 1801-5 | Info | ticket (pre-existing, repo-wide) | The cells read the yaml, so source-schema drift is caught only by `check:openapi`, and no CI workflow names openapi. | TESTED: mutant N9 (cells 12/12 green, `generate-openapi --check` FAIL). READ: `git grep -i openapi .github/workflows/` 0 hits (control: `runs-on` 6 in ci.yml). |
| 1801-6 | Info | none | Log-line details: the 200-char cap is unpinned (N6 survives); a refusal whose `error` is a string or absent logs only "no error code" and never the HTTP status. | TESTED: probe A6/A12/A12b; mutant N6. |
| 1801-7 | Info | none (rollout note) | `keyPending` is REQUIRED in the published spec; a contract test run against an environment still on the old service would flag its 201. | READ only; unmeasured. |
| 1801-8 | Info | none (out of scope, KS-1789) | Slow-but-not-hung tokenisation (A3) still writes a key row the caller never learns about; the flag now SAYS the key was not confirmed, which is option b's whole point. | TESTED: A3 (tok received 1, delivered 0, keyPending true). |

**Nothing is fix-before-merge.**

---

## #1795 (KS-1780 parts 1+3, tier 2 Claude half): GO WITH NOTES

Diff vs bd6697e: `routes/systemErrors.ts` +13/-1 (local `isZodError` helper; the list route's catch calls it), `utils/pgErrors.ts` +10 (`extractPgCode` becomes a try-wrapper around the unchanged body renamed `readPgCode`), two new jest files (8 + 4 cells), two html docs. One commit.

### Does it do what KS-1780 parts 1+3 ask? YES, narrowly
- Part 1 (brief `ks_1780_p1`): the `systemErrors.ts:196` site. `isZodError` catches only a throw from `err instanceof z.ZodError` and answers false; the 400 arm still reads `err.errors` only when the check is true; a hostile value falls through to `fail500` (hardened by KS-1772). The file has no other `instanceof z.ZodError` (grep: only the helper).
- Part 3 (brief `ks_1780_p3_webhooks`): fixed at the helper, so `webhooks.ts:320` and **all 6 production callers** (certifications.ts:920, documents.ts:2632/2865, gdpr.ts:139, gdprService.ts:73, webhooks.ts:320) now get `undefined` for an unreadable value. Each caller compares against fixed codes and otherwise goes to its 500 path, so the widening is in the fail-safe direction; readable values give the same answer (C1-C4).
- The try in the wrapper covers all three reads (`code`, `meta.code`, `message`); it is not wider than the reader.

### Runs and mutants
| run | result |
|---|---|
| both files at head (my worktree, jest) | **12/12** |
| base product (Spark half, spark_gate) | 6 fail / 6 pass (B1-B4, R1, R2 red; controls green) - accepted, not re-run |

My mutants (`out/mut1795/summary*.json`, restored + clean-asserted):

| mutant | killed by |
|---|---|
| M1 `isZodError` catch returns true (then `err.errors` is read) | R1, R2 |
| M2b call site reverted to `instanceof` | R1, R2 |
| M3b `isZodError` always false | C2 (the ZodError 400 arm) |
| M4 wrapper without try | B1, B2, B3, B4 |
| M5 wrapper catch returns `'22P02'` | B1, B2, B3, B4 |
| M7 drop the `meta.code` candidate | C1 |
| M8 try covers only the `code` read | B4 |
| M2, M3, M6, M6b first spellings | invalid: ts-jest TS6133 (unused symbol) - the suite failed to compile, not a behavioural kill; M2/M3 respelled as M2b/M3b above; the message-fallback mutant not respelled (C4 pins it by reading) |

**7/7 valid mutants killed.** Red-proof real: base answers `NO ANSWER` (Spark half measured; the test's 1500 ms abort makes a hang a red assertion).

### Docs entry
Read (Spark half section 3 and the diff): it states parts 1+3 only, names part 2 (adminConfig.ts) as separate, discloses synthetic hostile values. No figure in it contradicts my 12/12.

### Merge-in
Develop has moved 14+ commits since bd6697e (now b5583cb6). `merge-tree --write-tree --name-only` in my clone against develop 56062b37 and b5583cb6: **conflicts only in the two Projects Documents html files**. No develop change touches `systemErrors.ts`, `pgErrors.ts` or the new tests; #1787 (mid-gate) changed `adminConfig.ts` only.

### Findings (#1795)
| # | Sev | Class | Finding | FOUND / TESTED / HOW |
|---|---|---|---|---|
| 1795-1 | Info | ticket / optional cell | A hostile value whose **`message` getter alone** throws is not a cell (B2 = `code`, B4 = `meta`, B3 = revoked Proxy). The single try covers it, so this is a pin gap only (= Spark half's Minor 4). | READ + mutant M8 shows per-read narrowing is caught for `meta`; a narrowing that leaves only `message` outside the try would survive (not run). |
| 1795-2 | Low | ticket (outside KS-1780's 17 sites) | `routes/gdpr.ts:139` `mapGdprWriteDbError` reads `(err as {pgCode?})?.pgCode` **before** calling the now-safe `extractPgCode`; a revoked Proxy throws on that read. Whether the route then hangs depends on its caller's catch. | READ only; **unmeasured**. |
| 1795-3 | Info | none | `extractPgCode` hardening applies to 6 callers, not just webhooks; all compare to fixed codes, so behaviour for readable values is unchanged and unreadable ones go to 500. | READ (`git grep extractPgCode(`, 8 hits incl. 2 in pgErrors.ts). |

**Nothing is fix-before-merge.**

---

## Spark findings judged

| PR | spark_gate (deterministic) | Spark review |
|---|---|---|
| #1801 | head 12/0, base product 3 pass / **9 fail**, 63 s, rc 0 (`out/p1801/facts.json`) - matches my runs | attempt 1: **HTTP 400** (prompt 1.81 MB: the 36k-line yaml was in the full-text section; `out/p1801/spark_attempt1_http400/`). Retry with the yaml's full text dropped (its +11 hunk stays in the diff; flagged HARNESS LIMIT in facts): **VALID, NO GO**, 5 Major / 4 Minor / 1 Note, 45,306 prompt tokens, 103 s, no repetition abort (`out/p1801/spark/review.json`). |
| #1795 | Spark half (separate operator): 12/0 head, 6/6 base | NO GO, 0 defects confirmed by the operator |

**#1801 Spark findings, each judged:**
- Major 1 "does not implement the ticket (gateway connector-token timeout)": **FALSE as a defect.** KS-1240 is multi-part; this is Kam's ruled follow-on, stated in the test header ("scope extended by the coordinator's brief, not by the ticket") and passed to Spark in facts.not_run. Spark scored against the original ticket text.
- Major 2 "the timeout already existed": **TRUE fact, FALSE claim** - the PR never says it adds a timeout (the 3 s bound is #1782's); the quoted "The fetch carried no timeout" is ticket text, not PR text.
- Major 3 and 5 "the real route is not exercised, only the fake": **FALSE.** The test imports the real `index.ts`; only pg and JWT are replaced. My probe additionally put the real gateway router in front at real bounds and reproduced every flag value.
- Major 4 "'used to write no log line' unproven, absence-red": **FALSE.** KP3 is red on base (measured), though it fails at the raw-body assertion first; my base probe A6/A7 measures it directly: `logs: []` on a 403 at base.
- Minor "fake pg is not faithful": TRUE, disclosed, Note.
- Minor "KP2 does not measure the bound": TRUE; the bound is #1782's and pinned by ks1240b; my probe measured 3015 ms. Note.
- Minor "docs out of ticket scope": FALSE (same as Major 1).
- Minor "KP4 does not pin log content": **TRUE, Info** - pin gap; probe A11/A9 show the line carries tenant id + slug.
- Note "no real DB/service": TRUE, disclosed.

**Calibration #1801:** Spark NO GO vs gate GO WITH NOTES. Defects Spark found that stand: 0 (2 true Notes/pin gaps). Real findings Spark missed: 1801-1 (no-`success` body unpinned), 1801-2 (`success:true` without hash), 1801-3 (stale 10/2 figure, despite the facts.json it had saying 9/3), 1801-4 (gateway `data`). Its NO GO is driven by scoring a ruled follow-on against the parent ticket's text - the same "stated scope boundary read as a defect" pattern as #1795's Spark half and gates 6/8.

**#1795 Spark half judged:** agree with the operator. Major 1 (only 2 of 17 sites) is the PR's stated scope; Major 2 (tests do not measure a hang) is false (base `NO ANSWER`); Minor 4 (meta getter only) is true and is my 1795-1. Spark missed 1795-2 (gdpr.ts:139), as did the operator.

| PR | Spark verdict | This gate | Spark defects that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1801 | NO GO (valid on retry) | GO WITH NOTES | 0 (2 true pin-gap notes) | 1801-1, -2, -3, -4 | **Wrong**: scope misread drives it |
| #1795 | NO GO | GO WITH NOTES | 0 (1 true pin gap) | 1795-2 | **Wrong**: scope boundary + misread test |

## What I did NOT test
- A real api-gateway process (index.ts, front-door auth), real tokenisation/security services, real platform-DB writes, `PROVISION_PER_TENANT_DB=true`, a deployed stack, the admin UI, the four platform suites (Schemathesis, Akto, Playwright, k6), Node 24.
- #1801: the seat's "tsc including test files: 2 pre-existing TS2835" (I ran the project tsconfig only: 0/0); the rollout-order schemathesis effect (1801-7); any `PLATFORM_UPSTREAM_TIMEOUT_MS` override.
- #1795: base runs (accepted from the Spark half), the whole originate suite, tsc/lint, a `message`-only hostile value, gdpr.ts:139 behaviour (1795-2), the 15 adminConfig sites (part 2).
- PR bodies (gh not used); Kam's decision card itself (not found in the brain by a bounded search; the brief's verbatim option text was used).

## Evidence locations
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate12/out/`: `p1801/` (facts.json, facts_spark.json, diff.patch, pr_body_from_commits.txt, `spark_attempt1_http400/`, `spark/review.json`), `sg1801.log`, `t1801_head.txt`, `t1801_base.txt`, `x5_{1..5}.txt`, `suite_head.txt`, `checkopenapi_{w1801,w1801base}.txt`, `tsc_{w1801,w1801base}.txt`, `probe1801_head.{jsonl,txt}`, `probe1801_base.{jsonl,txt}`, `mut1801/` (summary.json, N9_*), `t1795_head.txt`, `mut1795/` (summary.json, summary_b.json). Drivers: `/private/tmp/claude-501/gatework12/` (`run_sg.sh`, `run_rev.sh`, `run_probe.sh`, `run_checks1801.sh`, `mut1801.py`, `mut1801_n9.sh`, `run_jest1795.sh`, `mut1795.py`, `mut1795b.py`); probe source `w1801/Blockchain/Dev/services/tenant-provisioning/src/__tests__/gate12-probe.test.ts`.
