<!-- COPIED from the QA project's own report directory, which is where THIS gate wrote it
     (unlike the #912 gate, whose verdict had to be dug out of a session transcript because
     Wednesday's prompt never told it where to send). Source, read-only:
     /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-qa-gate-ks754-pr914/mail-body.txt
     Copied 2026-09-09 by Wednesday s156. Verified on copy: byte count matches source. -->

QA GATE — Secuura KS-754 / PR #914 @ 311dc1ae4 — TIER 1, round 1 of 2

VERDICT: GO WITH FINDINGS

Findings-only. Nothing fixed, merged, pushed or deployed. The Secuura working
tree is CLEAN at close (`git status --porcelain` empty) and still on
feature/ks-963-f3-structural-cells @ b083c0e1e — nothing was checked out; every
by-SHA read used git show / git archive into my own scratchpad. The shared stack
was not rebuilt or restarted and :6882 was never used as evidence — checked at
close, secuura-postgres is Up 13 hours and secuura-auth Up 5 hours, both
predating this pass. My own Postgres 15.19 container (qa914-pg, port 55488)
was stood up and has been REMOVED (`docker rm -f`, verified: no such container).

Full report with every table and control:
/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-qa-gate-ks754-pr914/report.md

=============================================================================
FRAME — one thing that nearly produced a false verdict
=============================================================================
The Secuura working tree sits on a different branch, so reading product files in
place measures the WRONG CODE. My first instrument did exactly that and returned
two identical results for cells that had to differ — which is how it was caught.
Both trees were then reconstructed by SHA into scratchpad and hash-matched
against the repo objects (head 8ed16047a031, base 4d6c0f2ea179). If a future
gate drives this repo's source, reconstruct by SHA first; do not read in place.

=============================================================================
Q1 — WHAT A THROW AT gdprService.ts:859 DOES TO A PART-COMPLETED ERASURE
=============================================================================
FOUND. There is NO catch between :859 and the caller except executeErasureImpl's
own outer try/catch, which returns {success:false}. A throw at step 12 therefore
lands there and SKIPS STEP 13 — the USER_ERASED fan-out — AFTER step 11 has
already crypto-shredded
the subject's DEK, which is irreversible.

TESTED. Seeded subject, executeErasure driven end to end on a fully-migrated,
healthy DB, one transient 57P01 injected on exactly ONE statement (step 12's
UPDATE; injectedStatements=1 asserted in every row):

  S3       head + injection : success=false  DEK=1  USER_ERASED=0  DSR=processing
  S3-CTL-A head, injection OFF: success=true DEK=1  USER_ERASED=1  DSR=completed
  S3-CTL-B base + SAME inject : success=true DEK=1  USER_ERASED=1  DSR=processing

CTL-A isolates the injection as cause of the abort. CTL-B holds DB and injection
fixed and varies ONLY THE CODE, isolating the rethrow as cause of the lost
fan-out. Both controls can fail independently of the thing tested. CTL0 (base
code x pre-048) reproduced the ticket exactly: success=true, event published,
DSR left processing with no actor and no trail.

RECOVERABLE — DRIVEN, NOT ASSUMED. Second attempt on the same already-erased
subject with the injection lifted:
  attempt1 (injected): success=false USER_ERASED=0 DSR=processing/null/trail=0
  attempt2 (retry)   : success=true  USER_ERASED=1 DSR=completed/connector:abc/trail=1
The retry FULLY repairs it. The base-code control never repairs: both attempts
"succeed" and the DSR stays processing with no actor forever.

Connector path self-heals (ConnectorErasureIncompleteError -> DSR left
non-terminal -> S retries unbounded). ADMIN path has NO automatic retry — it
answers {success:false,'Erasure partially failed'} and a human must re-drive.

ASSESSMENT: your worry is real but BOUNDED and SELF-CORRECTING, and it replaces
a defect that was permanent and silent. Net improvement. What is nowhere in the
PR and should be: between the failed attempt and the retry, originate's copy of
the subject is destroyed while every downstream service still holds their data.

=============================================================================
FINDINGS
=============================================================================
F-1 MAJOR — a step-12 throw skips the downstream USER_ERASED fan-out after the
  crypto-shred.
  SCOPE, MEASURED: the fan-out has EXACTLY FOUR subscribers — auth, kyc,
  m365-integration and wallet-connector, each a .subscribe([EventTypes.USER_ERASED],
  CONSUMER_GROUP, ...) call (auth/src/services/userErasedSubscriber.ts:41,
  kyc/src/userErasedSubscriber.ts:28, m365-integration/src/userErasedSubscriber.ts:35,
  wallet-connector/src/userErasedSubscriber.ts:29). Those four are what stops
  cascading. Per occurrence that is ONE Art.17 erasure: originate's copy of the
  subject is destroyed and unrecoverable (DEK crypto-shredded), and those four
  services keep their copy until a retry lands. Connector path self-heals WHEN
  THE CAUSE IS TRANSIENT; admin path depends on a human noticing. F-4 is the
  case where the cause is NOT transient and the retry therefore never lands —
  the two are the same defect under different causes, not two claims in
  conflict. NOT wider than that: no other
  subscriber exists (see N-5).
  NOT a blocker: measured recoverable, and better than what it replaces.
  ASK: name it in the PR body and ticket it (move step 12 before the shred, or
  wrap it so the fan-out still fires). Does not belong in this PR.

F-2 MAJOR — PATCH /api/gdpr/dsr/:dsrId regresses a MALFORMED dsrId from
  HTTP 200 {success:false,'DSR not found'} to HTTP 500. Driven over real HTTP
  against the mounted router, three ids in one run, both SHAs:
    malformed        base 200 {success:false}  -> head 500 INTERNAL_ERROR
    well-formed absent  200 {success:false}    -> 200 {success:false}  (control, unchanged)
    well-formed REAL    200 {success:false}    -> 200 {success:true}   (the fix working)
  That third row is worth reading twice: on develop, a legitimate admin PATCH
  with a connector actor is told "DSR not found" about a DSR THAT EXISTS. #914
  fixes that. But it converts a client input error into a server error, which is
  the exact class KS-431 fixed on a SIBLING ROUTE IN THE SAME FILE — and
  routes/gdpr.ts:39 already defines UUID_PATTERN and uses it at :201 and :296,
  just not here. One line closes it without weakening the fix.
  SCOPE, MEASURED: admin-only — the route is gated
  requireRole('SYSTEM_ADMIN','ORG_ADMIN') at routes/gdpr.ts:348. No data
  impact: the throw IS the UPDATE failing, so nothing is written on that path
  — read back independently from pg after each driven case, the row was
  unchanged every time. NO information disclosure in production: verified with
  NODE_ENV=production, the pg message is masked to 'Internal server error'.
  Expect the sweep to flag the status code.

F-3 MINOR (process) — migration 048 ships with ZERO automated coverage. The new
  suite mocks $executeRaw outright and never touches a database, despite its
  name claiming the widening. The repo's only migration-behaviour gate,
  `npm run test:migrations`, is HARD-WIRED to a single file
  (MIGRATION=".../044_vault_entries_repair.sql"); the CI job gated on "did this
  touch migrations/?" runs those 044 scenarios — and Actions is retired anyway,
  as the workflow itself states. So a migrations/ change fires a gate about a
  DIFFERENT migration. I drove 048 by hand and it holds; nothing will again.
  KS-667's own argument applies verbatim.

F-4 MINOR — deploy ordering makes F-1 deterministic rather than transient. Head
  code against an un-migrated DB (driven): every connector erasure anonymises,
  shreds the DEK, then aborts with USER_ERASED=0. The cause (22P02) is not
  transient, so the connector's unbounded retry NEVER succeeds and each
  iteration re-runs steps 1-11. In fairness docker-compose DOES gate originate
  on `migrations: service_completed_successfully` — but run-migrations.sh EXITS
  0 WHEN MIGRATIONS FAIL, by design (its own closing block; BACKLOG #6), so that
  condition is satisfied by a run in which 048 failed. On Azure, migrations run
  at api-gateway boot while originate is a separate app with no such ordering.
  ASK: apply 048 before rolling the originate image, and confirm processed_by is
  `text` in the target DB before rollout.

=============================================================================
WHAT CAME BACK CLEAN (each with a control that could have failed)
=============================================================================
Q2 (the #912 shape) — NOT PRESENT. pg_depend on data_subject_requests.processed_by
  returns EXACTLY ONE object pre-048 (the FK itself) and EMPTY post-048; control:
  the same query for user_id returns its FK, so it finds a dependent when there
  is one. No index, view, trigger or RLS policy on the column. ZERO JOINs on the
  table tree-wide (control: same instrument finds 8 `JOIN users` lines). NOT
  modelled in schema.prisma (which models 15 things) so no client coupling. One
  reader only: mapDsrRow:391, a plain string passthrough, and the published
  response already types it z.string().nullable().optional(). The direction
  people forget — the FK also RESTRICTed DELETE FROM users — is inert: there is
  no DELETE FROM users anywhere in the tree (control: DELETE FROM matches widely)
  and erasure anonymises rather than deletes. Residual, stated not buried: a
  manual DBA delete can now orphan a value.

Q4/Q5 — re-derived, not accepted. FK drop is FORCED (red-proof: ALTER TYPE
  without the drop errors verbatim as the header claims; control: the identical
  statement on an FK-free column of the same table succeeds). Constraint name
  measured as data_subject_requests_processed_by_fkey, so DROP IF EXISTS is not
  silently no-op'ing on a mismatch. 048 run TWICE on a chain DB: both rc=0,
  second emits only the skip NOTICE. All three provisioning paths (chain,
  edited azure init, edited docker init) end text / 0 FKs / nullable, and the
  FULL column definition of the table is byte-identical across all three;
  negative control against a pre-048 azure build differs on exactly one line
  (uuid vs text), so the comparison can see a divergence. connector:abc INSERTs
  on all three; control: pre-048 rejects it 22P02; control-of-control: a real
  uuid inserts there, so the rejection is about the value not a broken fixture.
  The azure-init error at line 1869 is identical at base and head — pre-existing.

  Also worth having: base code x POST-048 DB still returns false. THE MIGRATION
  ALONE DOES NOT FIX IT — base casts the actor to uuid before the column type
  ever matters. The author's "two fixes, independent" is right.

Q3 — the catch exists at routes/gdpr.ts:363 and produces a 500. Author's claim
  is literally true. See F-2 for the part the commit message does not say.

Q6 — +57/-0 lines, 0 removed. Parsed JSON both SHAs: 8 rows ADDED (2+1+5,
  matching the three commits), 0 removed, 0 existing rows modified, $comment
  unchanged. All carry ticket KS-1024, decidedAt 2026-09-09, expires 2026-09-24
  (time-boxed, not permanent). colord carries scope:"standalone-locks" exactly as
  claimed — audit-gate.mjs:204 is the consumer that field exists for. GHSA-8m3c
  present as expected given #915 removes it. The acceptance decisions are Kam's
  and were not re-litigated.

Caller census — agrees with your table EXACTLY. Two non-test call sites,
  routes/gdpr.ts:360 and gdprService.ts:859. Positive control matched, negative
  control rc=1/0 lines. Neither of us was wrong.

Suites — base 48 suites/509 tests, head 49/515, delta exactly +1 suite +6 tests.
  RED-PROOF of the new suite, each mechanism reverted SEPARATELY on a copy:
  untampered 6 passed; restore ::uuid -> 1 failed; restore `return false` -> 2
  failed. It genuinely guards both code changes. It does not guard the migration.

=============================================================================
NOTES — pre-existing, reported rather than skipped
=============================================================================
N-1 develop IS RED. ks444-webhooks-create-description-guard.test.ts, 2 tests,
    expect 201 received 500. IDENTICAL at base and head. Not #914's.
N-2 A SECOND, UNMENTIONED SCHEMA ASYMMETRY. docker/init/01-schema.sql omits
    data_subject_requests_user_id_fkey, which migrations/001 and the azure init
    both declare. Identical at base and head. 048's header flags a three-file
    asymmetry on processed_by; this is a different one on user_id it does not
    mention — the same "looks like convergence and is not" trap it warns about.
N-3 THE Q5 RATIONALE IS RIGHT ABOUT THE WRONG RUNNER. "Keys on filename with no
    checksum" is true of scripts/run-migrations.sh and startup-migrations.ts,
    and FALSE of packages/shared/src/db/auto-migrate.ts, which computes SHA-256
    and raises "Checksum mismatch ... file was modified after it was applied".
    That runner has ZERO callers (control: the grep does find its export line),
    so the conclusion — leave 001 alone — STANDS and is in fact REINFORCED: were
    it ever wired up, editing 001 would error on every migrated database.
N-4 tsconfig.json excludes src/__tests__, so tsc never type-checks the new test.
N-5 THE FAN-OUT COMMENT OVER-STATES BY ONE. gdprService.ts:861-866 names
    "auth, kyc, m365, wallet-connector, security audit" as the downstream
    services. services/security SUBSCRIBES TO NOTHING: git grep for USER_ERASED
    under services/security/ returns rc=1, 0 lines, against a control that finds
    EventTypes under services/kyc/. Four subscribers, not five. Pre-existing
    comment, untouched by #914 — but it is the sentence a reader would use to
    size exactly the blast radius F-1 is about.

=============================================================================
WHAT I DID NOT TEST — in the same breath
=============================================================================
- executeErasureByExternalRef END TO END. Not driven (needs action_provenance /
  resolveExternalRef seeding). The connector-retry claim is read from
  gdprService.ts:1398-1410 plus the driven repair through executeErasure.
- RLS INTERACTIONS. My psql role owns the schema, so RLS never engaged. Any RLS
  effect on the erasure path is unmeasured.
- 048's LOCK / REWRITE COST on a production-sized table. My tables were empty.
  ALTER COLUMN TYPE takes ACCESS EXCLUSIVE and rewrites the column; duration on a
  real data_subject_requests is unknown and is a rollout question.
- Platform-DB routing: PLATFORM_DATABASE_URL was unset in every run.
- Other services' suites, schemathesis, the property sweep, the pre-push
  preflight: not run.
- No built image inspected. Shared stack untouched. :6882 never used.
- The 8 advisories' factual claims: not re-litigated (Kam's rulings).

=============================================================================
CLOSING — I have no inbox, so everything I want acted on is here
=============================================================================
1. F-2 is the one I would fix before merge if anything is fixed: one line, using
   the UUID_PATTERN already in that file, and it removes a regression the sweep
   is likely to raise against you anyway.
2. F-1 and F-3 want tickets, not code in this PR.
3. F-4 is a ROLLOUT instruction, not a code change: apply 048 before rolling the
   originate image, and confirm processed_by is `text` in the target DB first.
   run-migrations.sh exiting 0 on failure means "migrations completed" is not
   evidence that it landed — check the column, not the exit code.
4. N-1 means develop is red independently of #914. If the unblock ordering is
   #914 -> #915 -> develop, that red travels with it and someone should own it.
5. UNASKED QUESTION I could not answer from here: is `processed_by` read by
   anything OUTSIDE this repo — a BI query, a report, a compliance extract? Every
   in-repo consumer is accounted for, but an external reader that assumed a uuid
   would not appear in any census I can run.

PROVENANCE:
- merge-base equals develop head (f9296f9ea) and PR head is 311dc1ae4 | `git merge-base 311dc1ae4 f9296f9ea` and `git ls-remote origin refs/heads/develop refs/pull/914/*` in Secuura/Blockchain/2_Project_Files (not your project) | read 2026-09-09
- updateDSRStatus has exactly two non-test call sites, routes/gdpr.ts:360 and gdprService.ts:859 | `git grep -an updateDSRStatus 311dc1ae4` whole tree, no pathspec, with positive and negative controls | read 2026-09-09
- executeErasureImpl wraps steps 1-13 in one try/catch returning {success:false}, so a step-12 throw skips step 13 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/services/originate/src/services/gdprService.ts:545-902 at 311dc1ae4 | read 2026-09-09
- a step-12 throw yields USER_ERASED=0 while the DEK is destroyed, and a retry repairs it | driven against my own postgres:15-alpine (qa914-pg:55488) with the real gdprService at both SHAs, injection plus two controls | read 2026-09-09
- PATCH /dsr/:dsrId answers 500 on a malformed id at head and 200 at base | driven over HTTP against the mounted real gdprRouter, three ids x two SHAs x NODE_ENV | read 2026-09-09
- the FK drop is forced and 048 is idempotent, and all three provisioning paths converge | `psql` against qa914-pg: ALTER without the drop, 048 twice, three builds diffed, with negative control | read 2026-09-09
- the only DB object depending on processed_by was the FK itself | `pg_depend` query on a pre-048 and a post-048 build, with a user_id control | read 2026-09-09
- npm run test:migrations is hard-wired to 044 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/migrations/__tests__/ks667-044-scenarios.sh:50 at 311dc1ae4 | read 2026-09-09
- run-migrations.sh exits 0 when migrations fail | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/scripts/run-migrations.sh closing block at 311dc1ae4 | read 2026-09-09
- auto-migrate.ts DOES checksum and has zero callers | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/packages/shared/src/db/auto-migrate.ts and `git grep -an runMigrations 311dc1ae4` | read 2026-09-09
- 8 baseline rows added, 0 removed, 0 modified, $comment unchanged | parsed JSON of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/scripts/audit/audit-baseline.json at both SHAs | read 2026-09-09
- F-1 SCOPE: the USER_ERASED fan-out has exactly four subscribers (auth, kyc, m365-integration, wallet-connector) and services/security is not one | `git grep -an 'subscribe(\[EventTypes.USER_ERASED\]' 311dc1ae4` whole tree, plus a services/security pathspec search returning rc=1/0 lines against a working control | read 2026-09-09
- F-2 SCOPE: the affected route is admin-only and writes nothing on the failing path | requireRole('SYSTEM_ADMIN','ORG_ADMIN') at /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/services/originate/src/routes/gdpr.ts:348, plus an independent pg read-back after each driven case showing the row unchanged | read 2026-09-09
- F-1 is recoverable rather than permanent, which is what keeps it out of blocker scope | the driven attempt1/attempt2 pair through executeErasure against qa914-pg, plus /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/services/originate/src/services/gdprService.ts:1398-1410 for the connector retry | read 2026-09-09
- base 48 suites/509 tests, head 49/515, same 2 pre-existing failures | jest run from by-SHA scratchpad trees using the service's own jest.config.js | read 2026-09-09

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-09 11:31
