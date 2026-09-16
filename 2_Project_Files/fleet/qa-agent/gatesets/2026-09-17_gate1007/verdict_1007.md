# [Wednesday -> Wednesday] [QA -> Wednesday] TIER 2 GATE #1007 (KS-864) b28ed490a — GO WITH FINDINGS
# 2026-09-16T15:08:29.617Z from=Wednesday <wednesday-agent@agentmail.to> labels=['sent'] auth=None

BLUF
- PR #1007 (KS-864 parts A+B) at b28ed490ada70df2056763f4512c98443285a694: GO WITH FINDINGS. 0 Blocker, 0 Major, 1 Minor (F-1007-1), 1 Polish (P-1007-1), and 1 correction to a seat claim (C-1).
- TIER 2 is confirmed. I found no evidence that a live or shared gateway runs NODE_ENV=staging. That evidence is READ ONLY: no az, no remote host.
- The load-bearing claim holds, MEASURED: outside staging, 156 of 156 cells are identical across base 40fe4db69, head b28ed490a and head merged with current develop 93629700c. The grid includes the live NODE_ENV values dev and demo, and every one of the 21 env vars set alone.

REPORT (absolute path): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/report.md
Every instrument and its output is in the evidence folder beside the report.

HEADS AND BOUNDS
- Head b28ed490a at every reading: git ls-remote at 00:51:16, 01:03:26 and 01:06:23 (feature branch and refs/pull/1007/head), and the PR API head.sha at 01:02:35.
- Develop was 93629700c at all readings. It is diverged from the head, ahead 1 and behind 1, with merge base 40fe4db69.
- Secuura checkout, start 00:51:15 and end 01:06:23:
  - porcelain 0 and 0;
  - .git/config sha256 e0fa706f4bdae2778a5fe5975676f24459c5a3c6455de4ae85aa286f67632d1a both times;
  - worktree entries 111 and 111;
  - for-each-ref 888 and then 889. The +1 had already happened by 01:03:26. My clone is --shared and writes nothing to the source, so another session fetched.
- Substrate:
  - My own mktemp -d clone (--shared --no-checkout) with three worktrees: base, head, and merged. Merged is head plus a local --no-ff merge of 93629700c, never pushed, and differs from head only by the two #1005 files.
  - node_modules farmed from the checkout, @secuura rebound into each tree, shared dist built per tree.
  - Node v24.7.0, vitest 4.1.10, typescript 5.9.3.

TIER CHECK (READ ONLY, done first)
- The gateway container gets NODE_ENV from the bicep environment param (services.bicep:613). It does not take commonEnvVars; the hard-coded staging values at :373, :1514, :1567, :1709 and :1761 belong to commonEnvVars and to the issuer, verifier, outlook and admin frontend containers.
- deploy.sh accepts only dev or demo and passes environment= on both deployment creates (:349, :722). deploy-demo.yml sets demo. Both parameter files say demo.
- The only command in the repo that omits environment= is the RUNBOOK 1.2 what-if. A what-if deploys nothing (recorded as R-3).
- The staging compose overlay has no script or workflow user.
- The 2026-05-02 NODE_ENV=staging create is for the outlook frontend, not the gateway.

FINDINGS
- F-1007-1 (Minor, MEASURED): nothing pins the env-var arm of the three rewritten portal expressions, in any NODE_ENV.
  - That includes the new staging behaviour: head honours ISSUER, VERIFIER and ADMIN _PORTAL_URL under staging, where base ignored them.
  - Tamper G-2 (issuer url hard-coded to its default) compiles (tsc rc 0) and gives 0 reds on the whole suite (44 files, 388 tests).
  - The behaviour itself is correct: in my probe each only-PORTAL_URL staging cell moves exactly its own portal at head, and moves nothing at base.
  - Owner's regression test (prose): a staging cell and a non-staging cell that set each portal var and assert it wins.
- P-1007-1 (Polish, MEASURED): an INCLUDING tsc program finds 4 new errors, all in the two new test files.
  - TS1378 top-level await at :13 in each file. No base api-gateway test file uses a column-0 top-level await.
  - TS2554 at :18 in each file: the 10_000 passed as a second argument to new Promise is dead. The real hook timeout is on :19.
  - Controls: the program listed 42, 44 and 45 test files on the three trees; a planted type error in ks864a was caught, and the file was restored sha-identical.
  - 0 errors in system-status.ts. The new-error set matches D9. My distinct-error totals (29, 33, 34) differ from D9's 12 and 16 only because I keyed on the full diagnostic line.
- C-1 (correction to a seat claim and to the brief's S-C row): the seat's tamper "getServiceUrl ignores its env var" (if envUrl and false) does NOT compile.
  - The project tsc -p . gives rc 2: system-status.ts(44,24) TS2322.
  - Its two reds come from a program that does not type-check, so that row is VOID as a red-proof. The drafter did not run tsc per tamper.
  - The controls are still pinned, by compiling tampers that each hit exactly one control: G-1 (gateway var renamed) gives 1 red on the ks864b control; my Q-1 (helper ignores only ANCHORING_SERVICE_URL) gives 1 red on the ks864a control.

TAMPERS
- Setup: head, whole suite at 44 files and 388 tests, TEXT anchors count 1, project tsc per tamper, restore sha256-identical to 12a3287b (blob 956083916). All reds were AssertionErrors.
- Baselines: T0 base 42 files, 382 tests, 0 reds. T0 head 44/388, 0 reds. T0 merged 45/391, 0 reds.
- S-A, staging branch restored: 2 reds (ks864a gateway-localhost and no-internal-ashypond), as predicted.
- S-B, issuer ternary restored: 2 reds (ks864b issuer-default and no-portal-dead-estate), as predicted.
- S-C: VOID, tsc rc 2 (C-1).
- G-1: 1 red. Q-1 (mine): 1 red. G-2: 0 reds (F-1007-1). Q-2 (mine, issuer default changed to 8080): 1 red.
- T0-after: 0 reds. G-3, G-4 and T6 were not run.

PARITY AND STAGING (MEASURED)
- Probe setup:
  - REAL routes/system-status imported fresh after vi.resetModules() in every cell;
  - mounted at /system and /api/system on 127.0.0.1:0;
  - fetch replaced by a recorder, which saw at least 21 hits per status call.
- Compared per cell: codes, normalised body hashes on both mounts and on simple, the sorted fetched URLs, each resolved url, environment.env and the top keys.
- Grid: 7 NODE_ENVs (development, test, production, unset, dev, demo, staging) times 26 configs = 182 cells per tree.
- Outside staging: 156 of 156 identical for base vs head, head vs merged, and base vs merged.
- Controls:
  - staging differs base vs head in 26 of 26 cells (the instrument sees change);
  - every var set alone moves exactly one entry to the planted value, in every tree and NODE_ENV, which also proves resetModules works.
- Staging at head:
  - the 17 helper entries become localhost defaults; the api-gateway entry becomes http://localhost:8080, a self-probe;
  - the portals become the frontend defaults on port 80;
  - 0 dead-estate url values in every cell.
- Dead estate in the body: base staging has 76 occurrences. Head and merged have 16, in every NODE_ENV, all in troubleshooting commands.
- The :527 az hint is a RECORD, not a finding against #1007:
  - 8 commands (16 occurrences) whenever services are unhealthy, in every NODE_ENV, identical on base, head and merged;
  - absent when services are healthy;
  - served to anonymous callers.
- Grep 22 to 18, re-derived: base 22 lines and 30 occurrences; head 18 lines and 19 occurrences (17 call-site third args plus the :527 hint, which counts twice). Every hit was read and classified; a control count agreed with both instruments.
- Part B port 80: the head expression equals base's non-staging arm, and outside staging the only-PORTAL_URL cells moved the portal at base too (under staging base ignored them, see F-1007-1). So base resolved the env var first outside staging, with the same default.

PARSER, STATIC, LINKAGE (MEASURED)
- Parser (typescript AST) on base and head:
  - one non-exported const; module exports default=router only;
  - 18 calls, 17 with 3 args; 0 spread args, 0 object-literal args, 0 non-call references; call lists identical;
  - third parameter used 2 times at base and 0 at head;
  - only system-status.ts of 77 src files names the helper;
  - 5 of 5 synthetic controls detected.
- noUnusedParameters: renaming the parameter back gives TS6133 rc 2; after restore, rc 0.
- eslint: 0 errors and 0 warnings on the three head files and on base system-status.ts. A planted unused const was reported (as a warning), then restored.
- Closing phrases: 0 across the PR body, title, commit message, 1 linear-bot comment, 0 reviews and 0 review comments. A planted "Fixes KS-864" control was caught.
- Linear, re-read at 01:08:17 AEST, immediately before sending (queries only): attachmentsForURL(pull 1007) gives exactly 1, on KS-864 (In Progress), linkKind "contributes", status open. KS-864 has only that attachment. PREDICTED, needs a merge: merging leaves KS-864 open.

KS-1102 RECORD (MEASURED)
- The REAL gateway app, with no credential: /system/status and /api/system/status answer 200 in test, development, dev and staging. Controls /api/documents and /api/admin/audit answer 401.
- So these routes are public under Kam's ruling.
- #1007 adds, removes or renames no key; it changes url values only under staging. It is independent of the ruling.
- PREDICTED (READ ONLY): no textual conflict with the ruling's fix.

NOT TESTED
- Not applicable per the brief: Schemathesis, Akto, Playwright, k6, docker or any stack, live or remote status, az, preflight legs 3, 4 and 8, the shared suite.
- Real network fetch: skipped. Outside staging the fetched lists are identical, so no difference is possible. The healthy or unhealthy outcome of a real staging self-probe was not measured.
- Real-app probe under production and demo: NOT RUN (time box). Those values were covered by the router probe.
- G-3, G-4, T6: optional, not run.
- The seat's red-before-green sequence: not re-run; the tampers stand in for it.
- The history grep for recorded staging readings was capped at 20 lines, so it is not exhaustive.
- CI check-runs: not read.

CLOSING — for your action
1. F-1007-1: ask Seat A to add a cell that sets each portal env var, under staging and outside it, before or after merge at your discretion. G-2 must go red afterwards. The product behaviour is already correct.
2. C-1: tell Seat A that the "if envUrl and false" tamper does not compile. Future red-proof rows should carry a tsc rc. Controls are proven by G-1 and Q-1, so nothing needs redoing on #1007.
3. P-1007-1: the dead 10_000 argument and the top-level await are at the builder's discretion.
4. Records, not #1007's:
   - R-1: the :527 hint reaches anonymous callers in every NODE_ENV; it belongs to KS-864's open item and the KS-1102 ruling.
   - R-3: the RUNBOOK 1.2 what-if omits environment, so if it runs it falls back to the bicep default staging (READ ONLY; not executed). Harmless as a what-if; wrong if copied into a create.
   - R-4: dead-estate siblings in deployment azure configure-domain.sh and env.staging.example.
   - R-5: the merged tree has a TS18046 from #1005's ks1073 test file in an including program.
5. Nothing in this gate needs Kam's eyes.

PROVENANCE:
- head at origin, develop tip, checkout porcelain, config sha256, ref and worktree counts at start, mid and end | git ls-remote, git status, shasum, git for-each-ref and git worktree list as read verbs in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, output /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_bounds.out | read 2026-09-17
- tier check deploy paths and gateway NODE_ENV source | head tree of my clone, /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_tier_read.out | read 2026-09-17
- clone, trees, blobs, farm, merge with develop | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_setup.out | read 2026-09-17
- parity and staging cells and controls | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_parity_run.out and /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_parity_analyse.out | read 2026-09-17
- suites and tamper rows | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_tampers.out | read 2026-09-17
- including tsc, rename control, eslint | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_static.out | read 2026-09-17
- parser proof | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_parser.out | read 2026-09-17
- real app auth and grep census | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_realapp_census.out and /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_sibling_census.out | read 2026-09-17
- PR state, head sha, body, commit, comments, closing phrases | GitHub REST GET only, /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_gh_read.out | read 2026-09-17
- Linear linkKind and KS-864 attachments | Linear GraphQL queries only, /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_linear_read.send.out | read 2026-09-17
- READY bytes versus head | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/evidence/qa_ready_vs_head.out | read 2026-09-17
- the brief and the charter | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1007-ks864-tier2.md and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md | read 2026-09-17

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-17 01:08
