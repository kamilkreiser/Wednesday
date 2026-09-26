# CAPTURE for gate27 (QA/Secuura-batch1278) — 2026-09-26T03:14:10Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.

## #1278 KS-1314 (Seat L7 (round 1) / B 30th (fix round, fast-forward), T2) — head 18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8

#1278 ticket line: #1278 is KS-1314.

### PR BODY (gh_body_1278.md) TEXT_SHA256 d582941d905a931c71af763496c70e0ff38f6b4c4d0cca47b6cd367a636b7cf5

#1278 KS-1314: a prettier-wrapped parser import evaded the routing check; pin the loaders; record the canary spawn
head 18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8

## BLUF

Test-only, two files. **A parser import that prettier has wrapped evaded the routing check entirely** — and the fixture proving it is *captured from this package's own prettier*, because my first attempt at writing one by hand didn't wrap at all. Plus a cell pinning the product loaders, and the canary's spawn recorded with its measured cost.

`Refs KS-1314`

> **Base:** branched from `4db87c3e4b98`. This is a `systemTest/` path, so **no preflight ran** and **no fleet STOP count was executed or is quoted**.

## Item 1 — a wrapped import hides the specifier from every line-anchored pattern

`parserImportSites()` matches line by line. When prettier wraps a statement the first line is `import {` and the module name only appears on the **last** line, `} from '<parser>';`. No pattern sees it.

**Measured before the fix:** `parserImportSites(PRETTIER_WRAPPED_IMPORT)` → `[]`, while the **identical single-line import was caught**.

**The fixture is captured, not typed**, and this mattered: my first candidate was a 99-character import, and **prettier left it on one line** — `printWidth` here is 120. A hand-written "wrapped import" can be wrapped at the wrong column and pin a shape prettier never emits. The real shape came from `npx prettier --stdin-filepath` on a 136-character import: 12 lines, `tabWidth: 4`.

Multi-line `import`/`export` statements are now collapsed onto one logical line before matching, **bounded at 40 lines** so an unterminated statement cannot swallow the file.

**Controls in the cell:** a wrapped import of *something else* is not a hit; an unterminated statement yields at most one.

## Item 2 — nothing pinned the thing the property is about

The routing cells read only **this suite's own source**. The suite could be perfectly routed while `runner/config_loader.ts` parsed the file itself. A new cell pins that every product loader calls `readYaml()` and imports no parser.

**Its control is the load-bearing part:** `utils/yaml.ts` is asserted to be the **one** module that *does* import the parser. If that ever reads `[]`, the instrument has stopped seeing real imports and every other assertion in the cell is vacuous.

## Item 3 — the spawn stays, recorded with its cost

**Measured: 193 ms of the file's 220 ms.** Each alternative is worse:

- **import the parser in-process** — it would (correctly) trip the routing cell, so the only way is a computed specifier: deliberately evading this suite's own guard in order to test it;
- **capture the raw error once as a fixture** — it stops being a live witness the moment js-yaml changes its message, which is exactly how the original canary was lost;
- **drop the raw half** — the claim is comparative ("the raw parser prints the file, `readYaml` does not"), and half a comparison proves nothing.

193 ms is the cheapest honest form, and the file now says so rather than leaving it to be re-litigated.

## Red-proof, re-run against the FINAL bytes

The first pass predated prettier reformatting both files, so it was re-run rather than quoted from a draft.

| arm | result |
|---|---|
| collapse removed | the **wrapped-import cell reds, alone** |
| a loader imports `js-yaml` | the **loaders cell reds** |
| a loader drops `readYaml()` | the **loaders cell reds** |
| restored | **0 red** |

`runner/config_loader.ts` restored **byte-identical** after each arm.

## Test Evidence

**Touched**
- `tests/unit/support/readYamlRouting.ts` — the collapse, and `PRETTIER_WRAPPED_IMPORT`.
- `tests/unit/config/sheddingCeiling.test.ts` — two new cells, and the canary's recorded rationale.

**No product file is in this PR.**

**Ran**
- `npm run test:unit` in `s-l7-ks1314/systemTest/performance`, at base `4db87c3e4b98`: **1104/1104 bare → 1106/1106 patched**, 63 files, **+2 = exactly these cells**. Load **9.01** bare / **7.65** patched.
- `npm run lint` → **rc 0** (both tsconfigs and eslint). It caught three things I had not: two prettier wraps and a missing `curly` brace.
- All four red-proof arms above.
- Push: **12 s**, `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`.

**NOT run**
- **No preflight, no fleet STOP count** — `systemTest/` path.
- **KS-1300 item 1 (READYAML-UNGATED) is deliberately out of scope**: wiring this suite into a gate touches the push gate, which is not in this lane. So these cells are still executed only by hand.
- **The collapse is text-level, not a parser.** A parser import assembled from a computed string still evades it, as does one reached through a helper in another module.
- The canary's 193 ms is measured on this box at this load; it is a cost, not a budget.

**Migrations + config**
- **None.**



### HEAD COMMIT MESSAGE TEXT_SHA256 5fef585744219dbfd1d785ff5aa2dda357a72f09d2ab3950e4e73be57e6f13ca

KS-1314: read the parser imports from the AST, and pin the CALL not the spelling

Fix round 1 for #1278, on the gate's blocking finding B-1278-1. The author of the
branch has wrapped, so this is a fast-forward commit by another seat; the history
before it stays its author's.

B-1278-1: round 1 read the TEXT. Four line-anchored patterns over a joiner that
collapsed a wrapped statement "until one line carries the ;". A SEMICOLON INSIDE A
COMMENT ended the join before the `} from ...` line, so the whole statement read
as no hit at all -- and a loader importing the parser directly kept the cell GREEN
at 11/11.

I measured the gate's two cheaper repairs before taking its third option, and the
measurements are why the AST won:

  * "end the join at a `} from '...'` line" does NOT fix it. The join still breaks
    at the ; in the comment BEFORE it reaches the } line. Both reported shapes stay
    unseen.
  * "strip comments before testing for ;" DOES fix those two, and a wrapped
    re-export. But a wrapped require( or a wrapped dynamic import( is still missed,
    because the joiner only ever OPENED on a line starting with import/export and
    the pattern needed the specifier on that same line.

parserImportSites now asks the compiler. ImportDeclaration, ExportDeclaration,
require() and dynamic import() are four node shapes rather than four regexes, and a
comment, a string, a wrap point and a spelling stop being things to reason about.
The reported unit is the STATEMENT, so the positive-control rows keep their
contract. typescript is already a dependency of this package. The text joiner is
REMOVED rather than left unused: a dead helper is both a compile error here and a
reader's trap describing a rule the module no longer applies.

M-1278-a: the loaders cell asserted src.includes('readYaml('), which a DOC COMMENT
satisfies -- the gate's A2c probe deleted the only real call and the suite stayed
green at 11/11 because two comments above it still spell it. It now asserts a real
CallExpression.

P-1278-b: the canary comment claimed "193 ms of the file's 220 ms" with no
conditions. The gate measured the same cell at 2089 of 2116 ms under load ~18.7.
Both figures are now stated with their load, because the ratio is the stable part
and a bare number from a quiet box is not a measurement anyone can use.

Three regression cells. The two semicolon-in-braces shapes are CAPTURED from this
package's own prettier and verified idempotent under it, so they pass the format
gate and can really appear. A third drives the gate's A4 plant against each
loader's REAL source in memory, with the unplanted read as its control. Nothing is
written to a product file.

Refs KS-1314

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1314-ff-18cca0a7e0fe-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1314-ff-18cca0a7e0fe-push.out",
 "lines": 7,
 "pre_push_hook_base": "NOT FOUND",
 "fixture_guard": "NOT FOUND",
 "run_shell_suites_region": "NOT FOUND",
 "run_shell_suites_prefixed": "NOT FOUND",
 "shell_suites": "NOT FOUND",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "NONE",
 "preflight_ran": false,
 "rc": "0",
 "start": "2026-09-26T02:47:20Z PUSH START",
 "end": "2026-09-26T02:47:28Z push rc=0"
}
```

## #1285 KS-766 (Seat B 30th (local-model patch, re-verified by the seat), T2) — head c7779a33031813cac9dab62abd0cb8fd9d73f2f9

#1285 ticket line: #1285 is KS-766.

### PR BODY (gh_body_1285.md) TEXT_SHA256 2590114b61fb18ae0553692f914b7f0f3c5e833be9946479fb515906015a7748

#1285 KS-766: red-prove the base-image-watch DB-age producer, not only its consumer
head c7779a33031813cac9dab62abd0cb8fd9d73f2f9

## BLUF
`base-image-watch.sh`'s self-test could red on the **consumer** of the DB-age value but not on the
**producer**, so the QA F-5 fix was half-guarded: reverting `decide()`'s future arm reds the suite,
reverting the producer clamp did **not**. The gate would have gone back to printing *"the vulnerability
DB is 0.0h old"* immediately before telling an operator to run the ACR leg against the live registry,
with the suite green throughout.

The age computation was inline `$( python3 -c '...' )` command substitution rather than a callable
unit, so no case could reach it. It is now an isolated function the self-test drives with a synthetic
trivy metadata timestamp, and two cases pair a **future** stamp against a past one.

## Provenance, stated plainly
**The patch was produced by the local model under a Wednesday brief** and checked by her harness. It
is **re-verified independently here**, and every figure below is this seat's own run, not a quoted
harness figure.

## Test Evidence
Base this worktree **CONTAINS**: `00de57baeb40` — **develop's current tip**, with this commit directly
on it (`merge-base --is-ancestor` YES; `git log` shows `c7779a330` on `00de57bae`).

| proof | result |
|---|---|
| `git apply --check` — **strict, no recount, no fuzz** | **rc 0** |
| self-test at the tip, patch NOT applied | **20 PASS / 0 FAIL, rc 0** |
| **the test hunk ALONE** | **rc 12** — 20 PASS / **2 FAIL** |
| all three hunks | **22 PASS / 0 FAIL, rc 0** |

**The red is the point of the ticket, and it names itself.** With only the self-test hunk applied, the
two failures are
`FAIL  a FUTURE UpdatedAt yielded '', not the future sentinel` and
`FAIL  a past UpdatedAt yielded '', not a numeric age` — i.e. the new checks *cannot* pass without the
extraction, which is exactly the coverage the ticket says is missing today. The two PASS lines added by
the full patch are those same two cases:
`PASS  a FUTURE UpdatedAt yields the future sentinel` and
`PASS  a past UpdatedAt yields a numeric age (59040.92h)`.

**Counting note.** The self-test **indents** its result lines, so a line-anchored `grep -c '^PASS'`
returns **0** and reads as "no checks ran". Every figure above is counted unanchored, with the anchored
count kept alongside as a control. An under-count here would look like a broken suite rather than a
broken parser.

**Modes after `git apply`** — restored and asserted, not assumed: the subject and `.githooks/pre-push`
are both executable, index mode `100755`. A rewritten hook silently losing its exec bit is how an
ungated push has happened before.

**Push gate:** `pre_push_hook_base` **28/0**, `fixture_guard` **6/0**, `run_shell_suites` **49/0**,
shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Preflight **12/15 legs ran, 3 SKIPPED
(3, 4, 8 — local stack not up), nothing failed** — not quoted as a pass.

## NOT covered
- **No docker or network run of the real trivy path.** The self-test drives the producer on JSON only.
- `shellcheck` is not installed here.
- Legs 3, 4 and 8 NOT run (no local stack). No database. No deploy.
- The consumer half (`decide()`'s future arm) was already guarded; this PR adds the producer half only.

Refs KS-766



### HEAD COMMIT MESSAGE TEXT_SHA256 c206cbdaeee72bd04103a456b2151b3476dec1c3446afa9becf30d1434f4c79e

KS-766: red-prove the base-image-watch DB-age producer, not only its consumer

The self-test could red on the CONSUMER of the DB-age value but not on the
PRODUCER, so the QA F-5 fix was half-guarded: reverting decide()'s future arm
reds the suite, reverting the producer clamp did not. The gate would have gone
back to printing "the vulnerability DB is 0.0h old" immediately before telling an
operator to run the ACR leg against the live registry, with the suite green.

The age computation was inline command substitution rather than a callable unit,
so no case could reach it. It is now an isolated function the self-test drives
with a synthetic trivy metadata timestamp, and two cases pair a FUTURE stamp
against a past one.

PROVENANCE, stated plainly: the patch was produced by the local model under a
Wednesday brief and checked by her harness. It is re-verified independently here,
and the figures below are this seat's own runs, not the harness's.

  * applies STRICTLY at this base with no recount: git apply --check rc 0.
  * at the tip, before the patch: 20 PASS, 0 FAIL, rc 0.
  * the test hunk ALONE: rc 12, 20 PASS, 2 FAIL -- and the two failures are the
    producer cases by name, "a FUTURE UpdatedAt yielded '', not the future
    sentinel" and "a past UpdatedAt yielded '', not a numeric age". That is the
    red the ticket asks for: the checks cannot pass without the extraction.
  * with all three hunks: 22 PASS, 0 FAIL, rc 0, and the two added PASS lines are
    the same two cases.

Disk modes were restored after the apply and asserted: the subject and
.githooks/pre-push are both executable, index mode 100755.

Refs KS-766

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks766-c7779a330318-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks766-c7779a330318-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T00:56:36Z PUSH START",
 "end": "2026-09-26T01:03:28Z push rc=0"
}
```

## #1286 KS-1336 (Seat B 30th, T3) — head 27480bb649477435b4a683059d3fcbded3611377

#1286 ticket line: #1286 is KS-1336.

### PR BODY (gh_body_1286.md) TEXT_SHA256 4b37d6bd4d6fab3c590bb1cbfc5fcf0ae92e6e47de5bda4ef50d635a5e28084f

#1286 docs: correct the tenancy docs to the shared database the code actually uses
head 27480bb649477435b4a683059d3fcbded3611377

## BLUF
Both tenancy documents describe a **per-tenant-database architecture that has never existed in any
deployed environment**. A reader of either overestimates the isolation in place. The worst of them is
the **Security Considerations** table, which told anyone checking the security posture that tenants
are physically separated with *"no shared tables"*.

Every claim below is measured at `00de57baeb405d0081fe8b6f192bd40d35acef61` and cited to the source
that implements it. **Nothing here is a plan or a recommendation** — whether the dormant path is
completed or removed is Kam's decision and is deliberately not recorded.

## What is true, and where it lives
- **Every tenant resolves to one shared application database.**
  `services/api-gateway/src/startup-migrations.ts:1116-1144` writes every `tenant_config` row with a
  single `db_name`, `db_host` and `db_port` taken from `DATABASE_URL`. Its own comment reads
  *"On Azure there is a single DB; per-tenant DBs are not provisioned."*
- **Isolation inside it is `tenant_id` + row-level security, fail-closed since
  `migrations/039_rls_fail_closed.sql`.** An unset `app.current_tenant_id` returns **zero** rows,
  where before 039 it returned **all** rows. The deliberate escape is
  `app.tenant_scope_bypass = 'platform_admin'` via `runWithPlatformScope`.
- **Two carve-outs keep 038's permissive policy, both named in 039's header:**
  `platform_document_registry` (public verify-by-hash is cross-tenant by design) and
  `svc_m365_connections` (its `tenant_id` holds the Microsoft/Entra directory id, so the comparison
  could never match).
- **The per-tenant path is dormant behind two flags set in no config file:**
  `MULTI_TENANCY_ENABLED` and `PROVISION_PER_TENANT_DB` (`tenant-pool-manager.ts:151-152`).
  *Control for that zero: 25 config files do mention `DATABASE_URL`, so the search is not blind.*

## FIVE assertions corrected in `MULTI-TENANCY.md`, not the two this change set out to fix
The extra three were found by **sweeping the file for the claim** rather than trusting the line
numbers I was handed. A docs PR that corrects one false line and leaves three standing is worse than
none, because the corrected line lends the rest credibility.

| where | was |
|---|---|
| `:13` summary | "Each client (tenant) receives an isolated PostgreSQL database" |
| `:16` key point | "Each tenant has its own PostgreSQL database (`secuura_tenant_{slug}`)" |
| the architecture **diagram** | drew `secuura_tenant_{slug}` beside `secuura_platform` as though it exists |
| **onboarding steps** | "Provisions a new PostgreSQL database" — a step that does not run |
| **Security Considerations** table | "Each tenant has its own PostgreSQL database — no shared tables" |

The benefits table is kept but re-cast as **intended vs. what holds today**, because three of its five
rows (independent backups, performance isolation, per-tenant residency/deletion) are **not available**
on a shared database and a reader is entitled to know which.

## `RLS-FAIL-CLOSED-PLAN.md` — `:35`, and its neighbour
`:35` claimed *"Real isolation is per-tenant databases."* **False, and false when written.**

Its neighbouring bullet claimed RLS was *"permanently on its fail-open branch — inert today"*. That was
true on 2026-05-29 and **039 has since made it false**. Correcting `:35` alone would have left the
document contradicting its own corrected line, so both are superseded in place. **This is one bullet
wider than the change was scoped to, and it is flagged rather than absorbed** — it can be reverted.

Both are struck through and superseded rather than deleted, because the document's later sections still
reason from them and a reader needs to know **which way** they changed. Everything from "The hard
problem" onwards is unreviewed against today's tree and is left marked a proposal; `status: proposed`
in the front matter is untouched.

## Verification
- **Re-swept after editing:** no live assertion of a per-tenant database remains in either file. The
  four remaining matches are my own correction notice, the struck-through quote, and a reference to
  KS-1055. *Control: the sweep still finds 4 occurrences of `secuura_tenant_`, so it is not silently
  matching nothing.*
- Docs-only: **no code, no migration, no config, no test** changes.
- Push gate `28/0 · 6/0 · 49/0 · 60 of 60`; preflight **12/15 legs ran, 3 SKIPPED (3, 4, 8 — no local
  stack), nothing failed** — not quoted as a pass.
- Base this worktree **CONTAINS**: `00de57baeb40`, develop's tip.

## NOT covered
- The readiness work itself is **not** done here; it is tracked on the parent ticket with its five
  children.
- `docs/TOKENISATION.md` and `docs/DEPLOYMENT.md` were **not** swept for the same drift — out of scope
  for this change, and worth a look by whoever picks up the parent.
- No opinion is offered on whether to build or delete the dormant path.

Refs KS-1336



### HEAD COMMIT MESSAGE TEXT_SHA256 598fb707d11b9e2dbe6149b6c8cc0d8737e3905a40ef7f806bacf40c6a924ba4

docs: correct the tenancy docs to the shared database the code actually uses

Both tenancy documents describe a per-tenant-database architecture that has
never existed in any deployed environment. Anyone reading either one
overestimates the isolation that is in place, and the Security Considerations
table is the worst of them: it told a reader checking the security posture that
tenants are physically separated with no shared tables.

Every claim below is measured at 00de57baeb405d0081fe8b6f192bd40d35acef61 and
cited to the source that implements it. Nothing here is a plan or a
recommendation: whether the dormant path is completed or removed is Kam's
decision and is deliberately not recorded.

WHAT IS TRUE, and where it is implemented:

  * every tenant resolves to one shared application database.
    startup-migrations.ts:1116-1144 writes every tenant_config row with a single
    db_name, db_host and db_port taken from DATABASE_URL. Its own comment says
    "On Azure there is a single DB; per-tenant DBs are not provisioned."
  * isolation inside that database is tenant_id plus row-level security, and the
    policy has been FAIL-CLOSED since 039_rls_fail_closed.sql: an unset
    app.current_tenant_id now returns ZERO rows where it previously returned ALL
    rows. The deliberate escape is app.tenant_scope_bypass = 'platform_admin' via
    runWithPlatformScope.
  * two tables keep the older permissive policy by design, both named in 039's
    header: platform_document_registry, because public verify-by-hash is
    cross-tenant on purpose, and svc_m365_connections, whose tenant_id holds the
    Microsoft/Entra directory id so the comparison could never match.
  * the per-tenant path exists in code and is dormant behind two flags that are
    set in NO configuration file: MULTI_TENANCY_ENABLED and
    PROVISION_PER_TENANT_DB (tenant-pool-manager.ts:151-152).

FIVE live assertions were corrected in MULTI-TENANCY.md, not the two this change
set out to fix. The extra three were found by sweeping the file for the claim
rather than trusting the line numbers I was given: the architecture diagram, the
onboarding steps that describe provisioning a database that is never
provisioned, and the Security Considerations row.

In RLS-FAIL-CLOSED-PLAN.md the neighbouring bullet is corrected as well as :35.
It asserted RLS was "inert today", which 039 has since made false; correcting :35
alone would have left the document contradicting its own corrected line. Both are
struck through and superseded in place rather than deleted, because the later
sections still reason from them and a reader needs to know which way they
changed. Everything from "The hard problem" onwards is unreviewed against today's
tree and is left marked as a proposal.

Refs KS1336

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-tenantdocs-27480bb64947-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-tenantdocs-27480bb64947-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T01:17:39Z PUSH START",
 "end": "2026-09-26T01:23:55Z push rc=0"
}
```

## #1287 KS-1318 + KS-1142 (Seat B 30th (re-raise of #1268's proven file), T2) — head 4dac00147f8861250bab6abbea2fec34b14b62f2

#1287 ticket line: #1287 is KS-1318 + KS-1142.

### PR BODY (gh_body_1287.md) TEXT_SHA256 8d356da01dc6f143914d73c2655f9e2caf35293c0284a6939074741f582fa8eb

#1287 KS-1318 + KS-1142: re-raise the proven entrypoint-corpus file on its own
head 4dac00147f8861250bab6abbea2fec34b14b62f2

## BLUF
#1268 carried three tickets and failed at the two-NO-GO cap on **ks1316's** guard-reachability rule,
so it ships nothing and stays open. **KS-1318's and KS-1142's work is in a different file**, was
proven in **both** rounds, and is not implicated in what failed. This raises that one file alone so it
is not lost with the vehicle.

**Nothing of ks781 is in this change, and no part of the rule that failed.**

## The file is not re-typed — it is the same blob, and you can check that
It is written from the object store at the exact blob both #1268 rounds carried:

```
$ git rev-parse HEAD:Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts
8a4ce36a3a96d2e511faf9b19eba14593d8e99fa
```

That is the blob the tier-2 report records at line 488. Content-addressed, so it is not a copy of
what some worktree happened to hold — it is the object itself. One file, one path.

## What the file does, unchanged from its proven form
- **KS-1318** — the combined default-shapes control asserts the three tags with `toEqual` **in source
  order**, rather than asserting their **count**. A swapped or renamed tag now reds instead of passing
  on arithmetic.
- **KS-1142** — K1's literal is hoisted and K1b reads `CORPUS` from the source text, with the subset
  reason stated in the cell. The corpus is pinned by **one** declaration instead of two
  hand-maintained literals in two files that could drift apart silently.

## Test Evidence
Verified on **develop as it stands** (`e6056de7ed640e3a441bc7e33853601bf9040084`), not on #1268's
older base — the point of this PR is that the file is independently good *here*.

| suite | result |
|---|---|
| `entrypoint-corpus.test.ts` alone | **30 / 30** |
| `packages/shared` **BARE** (develop as it stands) | **48 files / 944 tests / 0 failed** |
| `packages/shared` **PATCHED** | **48 files / 945 tests / 0 failed** |
| `tsc --noEmit` | **rc 0, zero `error TS`** |

Delta **+1 cell**. The whole package is green **with no ks781 change present**, which is the
load-bearing fact: this file does not depend on the rule that failed.

Control against the other failure mode: the change is **not** a no-op — it differs from develop by
**+73 / −29** on that path.

**Push gate:** `28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60)`. Preflight **12/15 legs
ran, 3 SKIPPED (3, 4, 8 — local stack not up), nothing failed** — not quoted as a pass. This worktree
contains develop's current tip, so the quadruple is a reading at `e6056de7ed64`.

## NOT covered
- **ks1316's guard-reachability rule is not here**, in any form. Its residue (parenthesised return
  forms reading `guarded: false`) is being tracked separately.
- #1268 is **not** closed by this PR, and should not be — that disposition is Kam's.
- No product code. No migration, no config, no lockfile.

Refs KS-1318
Refs KS-1142



### HEAD COMMIT MESSAGE TEXT_SHA256 9f9a620f144e651b5e6fdc615e24aff4358c8d546a16150efc1840d3bb74c713

KS-1318 + KS-1142: re-raise the proven entrypoint-corpus file on its own

#1268 carried three tickets and failed at the two-NO-GO cap on ks1316's
guard-reachability rule, so it ships nothing. KS-1318's and KS-1142's work is in a
DIFFERENT file, was proven in both rounds, and is not implicated in what failed.
This raises that one file alone so it is not lost with the vehicle.

The file is not re-typed or re-derived. It is written from the object store at the
exact blob both #1268 rounds carried, 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa,
and the PR states that blob so a reviewer can check it rather than take my word.
Nothing of ks781 is in this change, and no part of the rule that failed.

What the file does, unchanged from its proven form: KS-1318 makes the combined
default-shapes control assert the three tags with toEqual in source order rather
than asserting their COUNT, so a swapped or renamed tag reds instead of passing on
arithmetic. KS-1142 hoists K1's literal and has K1b read CORPUS from the source
text, with the subset reason stated in the cell, so the corpus is pinned by one
declaration rather than by two hand-maintained literals in two files that could
drift apart silently.

Verified on develop as it stands rather than on #1268's older base: the file is
green alone, the whole package is green with it, and tsc reports zero errors. It
depends on nothing from the failed rule.

Refs KS-1318
Refs KS-1142

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-corpus-4dac00147f88-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-corpus-4dac00147f88-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T02:51:35Z PUSH START",
 "end": "2026-09-26T02:58:28Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/measurements/fleet-measurement-RESULT-d7cdecf1.md TEXT_SHA256 a4c421c21ef366bfca8c8c580c187edd16433d0f2bf2d5e306d162fe6de7f576

# FLEET MEASUREMENT — preflight on the COMBINED tree d7cdecf1 (Seat L8, 2026-09-26)

Run at Wednesday's request (19:30Z ANSWER), because her 19:27Z declaration's line
"the first seat to push over it is the measurement" was wrong — a push measures its own
WORKTREE's base. This is the first tree that actually contains the merge.

**Base, stated per the new rule:** `merge-base --is-ancestor d7cdecf1d2ee HEAD` = **YES**.
HEAD = `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`, detached, throwaway worktree, **no push**.

## The four named counts — ALL MATCH the declaration

| count | measured | declared | |
|---|---|---|---|
| `pre_push_hook_base` | **28 / 0** | 28/0 | MATCH |
| `pre_push_hook_base_fixture_guard` | **6 / 0** | 6/0 | MATCH |
| `run_shell_suites` | **49 / 0** | 49/0 | MATCH |
| shell suites | **60 passed, 0 failed, 0 skipped (of 60)** | 60 of 60 | MATCH |

Zero lines starting `FIXTURE BUILD FAILED`. Preflight rc **0**;
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack
not up). That verdict is not a pass and is not quoted as one.

**The expectation is now a measurement.**

## The tree is proven to be the combined one, not a stale checkout

Three independent signs, each measured rather than assumed:

1. `merge-base --is-ancestor d7cdecf1d2ee HEAD` = YES.
2. The two suites the merge modified are the POST-merge copies:
   `run_migrations_failure_exit_code.test.sh` **180 lines** (105 pre-merge) and
   `no_tracked_credentials_root.test.sh` **352 lines** (324 pre-merge) — matching the compare's
   +77 and +31 exactly.
3. Their CELL counts moved with the content — **both of them**:
   `run_migrations_failure_exit_code` **5/0 -> 7/0** (+2 cells, from +77 lines) and
   `no_tracked_credentials_root` **15/0 -> 16/0** (+1 cell, from +31 lines).
   So the new content really RAN; the suites were not merely present in the tree.

That third point is what makes the four unchanged counts meaningful rather than vacuous: the
preflight demonstrably executed changed content and still produced the same quadruple.

## Method notes
- `d7cdecf1` was ABSENT locally, so one `git fetch origin develop` was taken **under
  `.push-lock-25`** — the lock honoured this seat's own 90 s cool-off first, and was held
  **3 seconds** (19:48:39Z -> 19:48:42Z).
- The fetch disturbed nothing another session owns: shared checkout HEAD and the **local `develop`
  branch both still `3bad652d17cf`** (only `origin/develop`, a remote-tracking ref, advanced);
  working tree still 17 untracked / 0 modified; shared `.git/config` sha unchanged.
- Counts read by **bounded region** between consecutive `=== <path> ===` headers, because the log
  carries two summary forms and either parser alone under-reports.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB30-2026-09-26.md TEXT_SHA256 6129824f0401239b34800d79e852212ce8540df0271f35cd2712965541f9e39f

# HANDOVER — Seat B 30th, Secuura/Blockchain, round 26 (2026-09-25 23:14Z → HOLDING)

> # ⚠ THIS SEAT IS STILL LIVE. IT HAS NOT WRAPPED.
>
> The queue is complete and this file was written at that point, but Wednesday ruled at 01:29Z that
> the seat **holds as the AUTHOR** for the gate26 verdicts rather than wrapping. **Do not boot a
> successor against this file while the pane is alive** — check the pane first.
>
> **Why the seat is held:** B 29th has wrapped, so **this seat is now the author of its PRs
> (#1280, #1281, #1282, #1283, #1284)** as well as its own. A round-1 NO GO on any of them, or on
> #1274 / #1261 / #1268, comes back as a fix round, and a live author saves a successor boot.
>
> **Gate kits in flight:**
> - **T1** — #1274 r2 (**at the cap**), #1280, #1281, #1282, #1283, #1284
> - **T2** — #1245 r3, #1261 r2 (**at the cap**), #1268 r2 (**at the cap**), #1275-#1279
> - **#1285 and #1286 go to the next kit.**
>
> **Three of mine are at the two-NO-GO cap: #1274, #1261, #1268. A second NO GO on any is STOP, not
> a third round.**
>
> **Wrap trigger:** ~80% context, or Wednesday's "wrap now" — whichever is first. At that point this
> banner is replaced and every PR still awaiting a GO is named below. **Merges stay with Seat M1.**

Written to be read COLD. Nothing here assumes you were in the room.

## STATE IN ONE LINE
**Queue COMPLETE: 8 items, 7 delivered, 1 skipped with its reason.** Three PRs raised (#1284, #1285,
#1286), three fix rounds pushed (#1274, #1268, #1261), four tickets filed (KS-1334, KS-1335, KS-1336,
KS-1337). **Nothing merged. Nothing deployed.** All six await gate dispositions.

## WHAT IS OPEN, WITH HEADS
| PR | ticket | head | state |
|---|---|---|---|
| **#1284** | KS-730 PR 3 of 3 | `dfc2468a547f0bb3d4995404942736312384539b` | READY, new PR |
| **#1274** | KS-934 | `8e94f5fb3e6d8ef21ba2007fde92d3ea0b5c942d` | READY, fix round **1 of 2** |
| **#1268** | KS-1318 + KS-1142 + KS-1316 | `5ac42fafeee11dec596e7e7d833ac82b8b478790` | READY, fix round **1 of 2** |
| **#1261** | KS-1293 | `0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a` | READY, fix round **1 of 2** |
| **#1285** | KS-766 | `c7779a33031813cac9dab62abd0cb8fd9d73f2f9` | READY, new PR |
| **#1286** | KS-1336 (docs) | `27480bb649477435b4a683059d3fcbded3611377` | READY, new PR |

**Three of these are round 1 of 2 — the two-NO-GO cap applies. A second NO GO on #1274, #1268 or
#1261 means STOP, not a third round.**

## UNSTARTED, IN ORDER
1. **KS-1333** — the only skipped item. anchorStateSync's four `blockHeight` writers. **Blocked on
   #1281 merging**: it is open at `c3374e3129cc` and owns the same file. Its first done-item is a
   MEASUREMENT (`GET /api/anchors/:id`'s `blockNumber` type at source), not a coercion.
2. Any fix round returned on the six PRs above.
3. **KS-1334** (High) — four production leak sites in `adminConfig.ts`. Filed this round, not built.
4. **KS-1335** — the notify rotation residual. Filed this round, not built.
5. **KS-1337** — the k6 pre-suite path encoding. Filed this round, not built.

## THE FOUR TICKETS I FILED, AND WHY EACH EXISTS
- **KS-1334** — `:113`, `:1859`, `:2031`, `:2158` in `adminConfig.ts` return `err.message` with **no
  `NODE_ENV` guard at all**, so they leak in production. Pre-existing (4 at the base, 4 at the head).
  A **worse class** than KS-730's off-production ternary, which is why KS-730 did not fix them.
  `KS-730 C4 SOURCE` pins them by route; **fixing one WILL red that cell — that is the intended
  signal**, and KS-1334's done-when says so.
- **KS-1335** — `last_sent_at` is written only on a SUCCESSFUL send, so a permanently failing webhook
  keeps NULL and sits at the head of every call. With `MAX_ROWS` such rows, #1274's starvation fix is
  defeated. **Cell R3 pins today's behaviour and WILL red when this is fixed.**
- **KS-1336** — the per-tenant DB readiness parent. KS-1304, KS-1235, KS-1055, KS-1054 are sub-issues;
  **KS-598 keeps KS-772 (Stuart's review stream) and is linked `related`** — do not re-parent it.
- **KS-1337** — `runner/cli.ts:162` takes a path from `URL.pathname`. **The QA gate's own checkout
  (`…/Testing Agent MAIN/`) contains spaces**, so this is live on this fleet, not hypothetical.

## THINGS THAT WILL BITE THE NEXT SEAT
1. **A fixture that routes the subject down a different branch gives green cells about code that
   never ran.** KS-730's cell failed 9 of 12 because its error string contained `does not exist`,
   which all four routes' pre-existing benign catch branch tests for — so every route answered 200 and
   never reached the code under test. **Three cells were PASSING while the fix was unexercised.**
   Assert the catch was REACHED before asserting what it wrote.
2. **The brief's diagnosis of that was wrong**, and Wednesday owned it. It named
   `queryWithTenantGuc` and four line numbers that are in a route the cell never calls. **Re-measure a
   diagnosis, not just a figure.**
3. **`pre_push_hook_base` is a PREFIX of `pre_push_hook_base_fixture_guard`.** A substring parser
   reports 6/0 where the truth is 28/0 — and an under-reported STOP count reads as a **missing gate**,
   not a parser bug. Match exact basenames.
4. **Counts are indented in several tools.** The base-image self-test's `PASS` lines and the push
   log's summaries are both indented; `grep -c '^PASS'` returns 0 on a healthy run. Count unanchored,
   keep the anchored count as a control.
5. **I wrote two compile-breaking tampers this round** (orphaned identifiers; a `never[]` inference).
   Both produced 0 passed AND 0 failed. **Grade that LOADFAIL, never a pass** — it is indistinguishable
   from an inert tamper otherwise. Knowing the rule did not stop me reproducing it; the separate
   verdict is what caught it. **A runner that refuses a 0/0 arm would be better than the discipline.**
6. **Linear relations are DIRECTIONAL.** A one-sided `relations` query reads `[]` and looks like the
   link failed. Check `inverseRelations` too.
7. **A count names the tree it was measured on.** `packages/shared` reads 930 on `fa25c9b10fb4` and
   941 on `4db87c3e4b98` — that is `walkTimeouts` landing between them, not a regression.

## THE FLEET MEASUREMENT — TAKEN
**`28/0 · 6/0 · 49/0 · 60 of 60`, measured at develop's tip `00de57baeb405d0081fe8b6f192bd40d35acef61`**,
on #1285's push and again on #1286's. **Caveat**: each tree is develop's tip **plus** that PR's change,
so it supports "the declaration holds" and "my change does not move it" together without separating
them. An isolated figure (throwaway worktree at the tip, preflight without pushing) was offered and not
requested.

## SHARED CHECKOUT — NEVER WRITTEN
Measured at boot **and** at wrap, identical both times: HEAD `3bad652d17cf111c1e2e1bed1ae7686894637487`,
branch `develop`, **17 `??` / 0 non-`??`**, local `develop` branch unmoved. `.git/config` byte-identical
across every `worktree add` and both fetches (every worktree created **detached from a raw SHA**, never
`-b`). Two fetches taken under `.push-lock-26`, each after reading `.push-lock-25` and finding it free.

## MY RESOURCES
- **Worktrees:** `s-b30-ks934`, `s-b30-ks1318`, `s-b30-ks1293`, `s-b30-ks766`, `s-b30-tenantdocs`.
  All pushed; all can be removed.
- **The ADOPTED `s-b29-ks730c`:** branch `feature/ks-730-adminconfig-prod-message-b29-9` at
  `dfc2468a5`, **porcelain 0 — its work is committed and pushed as #1284. It is idle and safe to
  remove.**
- **No Postgres was started**, so nothing to tear down: 0 containers named `s-b30-pg-`, 0 listeners in
  55440-55449 (control: 2 on `:5432`).
- **Tools** (re-key them, do not run mine): `5_Project_History/2026-09-26_seatB-30th/raise/` —
  `lock26.sh`, `push26.sh`, `push26_ff.sh`, `namecheck26.py`, `rekey_check26.py`, and the proofs
  `lockproof26.sh` 23/23, `pushproof26.sh` 22/22, `ffproof26.sh` 28/28.
  ⚠ **`namecheck26.py`'s adoption exception is keyed on the EXACT BRANCH NAME, not the token** —
  control C5 proves a one-character near-miss (`-b29-8` vs `-b29-9`) still reads BAD. Keep that shape.

## 🔴 STILL WITH KAM
- **The audit fuse lapses `2026-09-30T00:00Z`** — four days out. From then **every `Blockchain/Dev`
  push is refused**, including any round 2 on the three fix rounds above. **It needs Kam's own word; a
  relay does not substitute.** No re-date PR was built.
- **KS-1304** — ruled (c); nothing built. Referenced only by KS-1336.
- **KS-1267** and the two audit re-dates remain held.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL7-2026-09-26.md TEXT_SHA256 9e6169ace278af641bb1a92ce34161a371c573e4712b17dbddd3d2252d78119b

# HANDOVER — Seat L7 (2026-09-26, round 25). Written to be read COLD.

## 1. WHERE THINGS STAND

**Queue COMPLETE: 7 of 7 items, 7 PRs, all READY FOR QA. Nothing merged. Nothing deployed. No ticket state moved by me.**

| PR | key(s) | head | family | gate |
|---|---|---|---|---|
| #1263 | KS-1140 | `3c33f936fe39` | packages/shared | preflight 12/15 · STOP 28/0 6/0 49/0 60/60 |
| #1265 | KS-1315 | `87ef6a1b0887` | systemTest/performance | **no preflight** · format gate only |
| #1268 | KS-1318 + KS-1142 + KS-1316 | `a8e0fca70ed4` | packages/shared | preflight 12/15 · STOP all match |
| #1271 | KS-1164 | `c9ea1dc1705f` | systemTest/performance | **no preflight** |
| #1275 | KS-1179 | `d852e56b912f` | packages/shared | preflight 12/15 · STOP all match |
| #1277 | KS-1319 | `702171eaadbe` | packages/shared | preflight 12/15 · STOP all match |
| #1278 | KS-1314 | `c321bcce2a9a` | systemTest/performance | **no preflight** |

**Every one is branched from `4db87c3e4b98`.** develop is `d7cdecf1d2ee` and no worktree of mine contains it, so **every STOP count above describes `4db87c3e4b98` + that change** — not the combined tree. Mailed as COUNT ATTRIBUTION 19:4xZ.

**Ticket filed: KS-1329** — "packages/shared does not type-check `src/__tests__`, hiding 10 errors". Carries the full error table, the probe method, every control note, and the three ks781 errors marked "after #1268 merges".

**Shared checkout `2_Project_Files`: HEAD `3bad652d17cf`, 17 `??` / 0 non-`??` at boot AND at wrap, byte-identical.** No pull, no fetch, no commit there all session. Shared `.git/config` carries **0** lines with my token `l7r25`.

## 2. THE THING TO INHERIT — my harness failed the same way the code does, four times

Every one was caught by a control, never by reading the code. **The pattern: an arm that can only come out red proves nothing. You need the arm that comes out GREEN.**

1. **A control that reds for the wrong reason.** KS-1319's second arm was meant to show the OLD wiring check stayed green under a comment-out. I left my new assertions in the cell beside the old ones, so it reddened either way. Re-run isolated, the old check was **7/7 fully green** — which is the entire finding.
2. **An instrument that cannot see its subject.** A regex extracting "string literals" matched backticks **inside comments**, reporting 138 -> 155 literals for a comment-only edit. Replaced by an emit comparison (`removeComments`, compare bytes).
3. **A probe whose config invented the answer.** The typecheck probe reported 24 errors, then 2, then 10 across three configs. Only a **planted** error settled which was real — and my first read of that control grepped for the VARIABLE NAME when tsc prints the FILE and LINE.
4. **A control that never fired.** A `sed`-based syntax check used GNU syntax on BSD sed, so the tamper never applied and "rc 0" meant nothing.

## 3. A GUARD THAT COULD NOT FAIL, AND HOW IT LOOKED FINE

KS-1319's wiring cell read the config's **source text** for `setupFiles`. `//` does not remove a string. The budget could be unhooked entirely and the cell stayed green. It now **imports** the config and reads the resolved value.

**The general shape: any check that reads source TEXT for a setting is satisfied by that setting commented out.** Grep the repo for `toContain('` against a config file and you will find the next one.

## 4. MEASURE BEFORE BUILDING — three tickets were wrong about their own subject

- **KS-1179 / F-5:** the ticket and the ruling both asked me to correct a docblock. **It was already correct**, fixed in an earlier round with the record left in the file. I changed nothing.
- **KS-1179 / N1:** a comment claimed an `isIP` throw made a cleanup path "live". **`net.isIP` does not throw** — `'x'`, `''`, `null`, `undefined`, `123` all return 0. The path is reachable only under a mock.
- **KS-1314 / item 1:** my first "wrapped import" fixture was 99 characters and **prettier left it on one line**. `printWidth` here is 120. A hand-written wrapped import pins a shape prettier never emits — capture it.

## 5. WHAT I RECORDED INSTEAD OF FIXING, AND WHY

- **TS2349 in `ssrf-guard.ts`.** Four shapes measured, each **relocated** the error: no cast -> TS2349; cast the callee -> TS2769; cast at the call site -> clean but the **emit changes**; assertion on the declaration -> TS2352. Only `as unknown as https.Agent` remained. **Refused:** in an SSRF guard a type the compiler stops checking is the risk to avoid. On KS-1329.
- **TS1343** (`import.meta`): 9 across the package, 4 in one other file. Fixing it here alone would drop `import.meta` in one file while eight keep it. On KS-1329.
- **The canary's per-run spawn** (KS-1314): **193 ms of the file's 220 ms**, and each alternative is worse — in-process needs a computed specifier (evading the suite's own guard to test it), a captured fixture stops being a live witness, and dropping the raw half leaves half a comparative claim.

## 6. THE CROSS-LANE CATCH

KS-1179's F-5 wanted the deadline error text at `ssrf-guard.ts:605` changed. Repo-wide search found **three** hits; two are **exact-string assertions in Seat B 29th's lane** (`services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts:76` and `:86`). Changing it would have reddened another seat's suite mid-round. Ruled (c): docblock only, runtime string byte-identical.

**The proof that it stayed identical is the emit comparison, not a diff read:** pristine vs head **12,137 vs 12,137 bytes, 0 diagnostics**, with a control that reds on **one character** of that string. ks914's own cells: **16/16 green at my head**.

## 7. FOR WHOEVER SITS HERE NEXT

- **`ast_equiv.cjs` (copied from B 28th's folder) is the right instrument for "type-only" or "comment-only".** Type assertions and annotations erase at emit, so byte-identical output proves no runtime change AND no string change at once. Its control must red at an **identical emit size** — that is the case a token counter misses.
- **Re-run red-proofs after lint/prettier touches your files.** I had to on KS-1164 and KS-1314; the first pass was against bytes that no longer shipped.
- **`git merge-base --is-ancestor <sha> HEAD` fails identically for "not an ancestor" and "object not in the store".** If the sha is not local, the sound argument is the absence itself.
- **A `?? Blockchain/Dev/packages/shared/None/` directory** came from a python arm reading `os.environ.get('R')` with no default: `None` became a plausible PATH rather than an error. Check `git status` after any scripted run that writes a report.
- **Tools:** `2026-09-26_seatL7/raise/` — `lock25.sh` (10/10), `push25.sh` (8/8), `push25_ff.sh` (18/18), `seatreq25.sh` (8/8, my own LOCK_SEAT change), `containproof25.sh` (7/7, both sides + the read-back), `merge25.py` (never used — no GO arrived).
- **`merge25.py`'s `merge_note` is now REQUIRED** with no default. B 28th made `--seat` required and left the note optional, then omitted it and the inherited default asserted the opposite of their case. **A parameter whose default makes a factual claim is a hardcoded claim with extra steps.**

## 8. 🔴 THE FUSE — unchanged, and it is Kam's alone

**Both audit rows lapse `2026-09-30T00:00Z`, four days out.** From then `audit:gate` and `audit:locks` refuse **every** `Blockchain/Dev` push, from every author — that is #1263, #1268, #1275 and #1277 of mine. Legs 6 and 7 passed on all four. **It needs Kam's own word** — his typed line or mail with `dmarc=pass header.from=me.com`. A relay does not substitute. No open PR names KS-729. Nothing this round averted it.

## 9. RECORDS

`5_Project_History/2026-09-26_seatL7/raise/` — every tool, proof matrix, tamper arm, captured output, push log (named by head sha per KS-1323) and probe config.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1314-ff-824edb4882af-push.out TEXT_SHA256 bf106ec4440ec30be58759d1dca80ac4ee65f49bc2feddc1d53161973e71dc38

[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the
[pre-push]   stale ref for base selection. (git fetch origin develop:develop
[pre-push]   to refresh it.) origin/develop is still consulted below.
[format-gate] systemTest/performance — format:check FAILED
[format-gate]   systemTest/performance/tests/unit/support/readYamlRouting.ts   (in this push)
[format-gate]   fix: (cd systemTest/performance && npm run format)
[format-gate] 1 package(s) checked, 0 skipped, 1 failed
[pre-push] systemTest formatting gate FAILED — fix the files named above.
           (bypass, sparingly: git push --no-verify)
error: failed to push some refs to 'github.com:Secuura/Distributed_Secuura.git'


