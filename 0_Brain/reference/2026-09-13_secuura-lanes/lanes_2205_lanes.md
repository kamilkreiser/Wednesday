# Secuura/Blockchain — LANE SWEEP for the overnight builder fleet (measured 22:08–22:35 AEST, 2026-09-13)

**develop = `8861e6216`** (M18 = #980; local `origin/develop`, `ls-remote origin` and `git log` agree). **Board: 108 KS tickets active** — predicate `team KS, state.type in [unstarted, started]` (= Todo 35 · In Progress 42 · In Review 26 · Blocked 5), Linear GraphQL `first:50` paged to `hasNextPage:false` (3 pages: 50+50+14 = 114 with `includeArchived:true`, of which 6 carry `archivedAt` — KS-660/483/303/250/244/63 — leaving **108**). `board_count.sh` on the same predicate: `TOTAL=108 (limit was 250)`. **Open PRs: 42** (GitHub REST, one page of 100, 42 < 100). Target: KS active ≤ 60 by Tuesday 2026-09-15. Everything here is read-only; nothing was fetched, checked out, posted or written outside this directory. Instruments and controls: `method.md`; per-ticket data: `lanes.json` (`tickets[]`, `lanes[]`).

## Classes (one per ticket; precedence e > h > f > g > d > c > b > a — the rule text is in method.md)

| Class | Meaning | Count | Tickets |
|---|---|---|---|
| **a** | ours-to-build, NO PR — a lane starts from the ticket | **21** | KS-1076, KS-598, KS-716, KS-723, KS-724, KS-725, KS-823, KS-835, KS-579, KS-580, KS-581, KS-704, KS-711, KS-738, KS-741, KS-777, KS-780, KS-973, KS-669, KS-920, KS-790 |
| **b** | our PR open, no verdict at CURRENT head, no reviewer ask outstanding → GATE | **17** | KS-1026, KS-1075, KS-1077, KS-601, KS-993, KS-911, KS-912, KS-1059, KS-1078, KS-1046, KS-693, KS-734, KS-1027, KS-1061, KS-1068, KS-736, KS-773 |
| **c** | our PR open, Peter's asks / a withdrawn approval / a NO GO outstanding → FIX round then gate | **19** | KS-1004, KS-487, KS-764, KS-798, KS-841, KS-926, KS-968, KS-991, KS-577, KS-739, KS-945, KS-1043, KS-657, KS-679, KS-726, KS-791, KS-799, KS-931, KS-961 |
| **d** | GO'd at current head, unmerged → merge seat | **0** | — |
| **e** | Peter/Stuart-authored PR, or ticket assigned to Peter/Stuart with no kksecura PR → theirs | **11** | KS-188, KS-412, KS-61, KS-135, KS-492, KS-502, KS-533, KS-575, KS-1096, KS-573, KS-418 |
| **f** | needs a human by the ticket's own words (quoted in the row) | **21** | KS-485, KS-491, KS-683, KS-696, KS-735, KS-770, KS-772, KS-582, KS-256, KS-665, KS-729, KS-771, KS-775, KS-966, KS-174, KS-441, KS-762, KS-869, KS-229, KS-663, KS-946 |
| **g** | blocked on something measured (named in the row) | **5** | KS-576, KS-583, KS-843, KS-365, KS-763 |
| **h** | own PR(s) merged, no open PR, no remaining-work words → RECORD DEFECT: verify + move the ticket (not a lane; a Linear-write seat) | **14** | KS-664, KS-695, KS-698, KS-731, KS-796, KS-801, KS-802, KS-806, KS-937, KS-949, KS-962, KS-1098, KS-930, KS-969 |
| | **Sum** | **108** | = 108 |

**Class d is EMPTY**: no open PR has a GO/GO WITH FINDINGS at its current head (every verdict dir in both report trees was matched by PR number AND head prefix; the s161 batch pins were read from its §0 table). The four older-head verdicts (#924 @1497b39de, #925 @0956c3dbe, #927 @63e955e0f, and #913's — superseded by #970) are class b re-gates. Every GO'd PR from today's queue (#932, #969–#978, #980, #981) reads `merged=true` at the API (merge commits listed in method.md).

## What changed since the 19:2x In Review census

- **9 census rows left the board**: KS-643, 661, 754, 800, 804, 992, 1024, 1057 (its 8 class-D record defects) and KS-950 (#973 merged 11:29Z) are all `Done` + `archivedAt` 21:21–21:31 AEST (queried by number with `includeArchived:true`). In Review: 35 → **26**.
- **#973 (KS-950/962)** got GO WITH FINDINGS tier-1 r2 @ca2a9109c and merged as M16 `818002259`; **#928** was CLOSED unmerged 11:32Z (superseded). KS-962 is still In Progress → class h.
- **#980** r2 @103c235b4 GO WITH FINDINGS → merged M18 = develop. Open PRs 51 → 42 (closed: #928, #973–#978, #980, #981).
- Re-classified on re-reading the words: **KS-726** G→**c** (Peter's guard-5 item is 'a question rather than a verdict… if you tell me the trade is deliberate I will take your read and approve' — the builder answers it); **KS-790** F→**a** (defect confirmed at develop, fix-shape stated, `getUserByIdPreAuth` exists since #970); **KS-763** F→**g** (its remaining done-means is the express-5 shape held by KS-775 [Decision], 'back with him'). **KS-739** stays c (Peter 09-09: 'I have not approved yet — two small, non-code items'). **KS-1078**'s #942 is STILL unattached in Linear.
- Unchanged in kind: the 11 census-B gates minus KS-950 = 10 still need a gate; the 10 census-C fix rounds are all still open at the same heads (no push since 09-10 on any of them).

## The lanes, in rank order (priority × count; each lane = one seat; a lane's PRs merge in the order written)

| Rank | Lane | Tickets (class) | Directory family | Pane | Worktree holding a branch |
|---|---|---|---|---|---|
| 1 | **L1 auth-oauth** | KS-798(c), KS-841(c), KS-799(c), KS-790(a), KS-823(a), KS-835(a) | `services/auth/src/routes/oauth.ts; services/auth/src/services/jwt.ts; services/auth/src/__tests__/ks798-*,ks799-*,ks841-*,ks781-n1-* …` | `Secuura/Blockchain` | #881→none |
| 2 | **L7 preflight-scripts** | KS-1046(b), KS-773(b), KS-926(c), KS-991(c) | `scripts/preflight/preflight.sh; scripts/preflight/lockfile-cleanroom.sh; scripts/run-code-guards.sh …` | `-B` | #925→ks1046; #924→ks773; #918→s157-guards; #903→ks991-hook |
| 3 | **L9 ci-workflows** | KS-1075(b), KS-1077(b), KS-1078(b), KS-961(c), KS-1076(a) | `.github/workflows/security-scan.yml; .github/workflows/pr-security-gates.yml; .github/workflows/pr-platform-suites.yml …` | `-D` | #940→none; #941→none; #942→none; #887→rb-887 |
| 4 | **L5 shared-security-revoke** | KS-764(c), KS-577(c), KS-780(a) | `packages/shared/src/index.ts; packages/shared/src/middleware/index.ts; packages/shared/src/security/keyRevokePolicy.ts …` | `-E` | #799→none; #880→rb-880 |
| 5 | **L3a originate-anchorStateSync** | KS-1004(c), KS-1059(b) | `services/originate/src/services/anchorStateSync.ts; services/originate/src/__tests__/ks1004-*; services/originate/src/__tests__/ks535-anchor-async-fail-propagates.test.ts …` | `-F` | #912→none; #937→ks1059 |
| 6 | **L3b originate-test-mocks** | KS-1061(b), KS-487(c), KS-657(c), KS-777(a) | `services/originate/src/__tests__/helpers/sharedModuleMock.ts; services/originate/src/__tests__/{gdprService.erasure,ks444-webhooks-create-description-guard,ks445-*,ks563-*,ks584-*,ks695-*,ks914-deliver-webhook-*,qa-f4-*,ks1061-*,ks1103-verify-hash-field}.test.ts; BACKLOG.md (the #720 hunk)` | `-G` | #931→none; #720→rebase-720 |
| 7 | **L2 originate-documents-openapi** | KS-739(c), KS-1068(b), KS-791(c) | `services/originate/src/routes/documents.ts; services/originate/src/repositories/documentRepo.ts; services/originate/src/originate.openapi.ts …` | `-H` | #919→ks739; #939→none; #813→none |
| 8 | **L10 systemTest-performance-fixtures** | KS-993(b), KS-1026(b), KS-973(a), KS-704(a), KS-711(a) | `systemTest/package.json; systemTest/performance/runner/actor_manifest.ts + tests/unit/runner/actor_manifest.test.ts; systemTest/performance/gate/report.ts …` | `-I` | #916→s158-systemtest |
| 9 | **L8 relink-guard-and-launcher** | KS-945(c), KS-926(c), KS-930(h), KS-937(h), KS-911(b), KS-912(b) | `scripts/check-shared-relink.sh; scripts/__tests__/check_shared_relink.test.sh; docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md …` | `-J` | #879→none; #874→none |
| 10 | **L4 anchoring-and-spec-examples** | KS-726(c), KS-679(c), KS-741(a) | `services/anchoring/src/** (anchorSubmission.ts, cardano/index.ts, index.ts, reconciler.ts, verifyAnchorStatus.ts, anchoring.openapi.ts, __tests__/ks726-*); packages/shared/src/openapi/examples/fixtures.ts; packages/shared/src/__tests__/ks256-spec-example-contract.test.ts …` | `-K` | #805→none; #922→ks679 |
| 11 | **L12 akto-harness** | KS-716(a), KS-724(a), KS-725(a) | `systemTest/akto/config/secrets.yml, secrets.example.yml; systemTest/akto/src/** (setup, core, client); systemTest/akto/tests/**` | `-L` | none (no PR) |
| 12 | **L11 schemathesis** | KS-693(b), KS-738(a) | `systemTest/schemathesis/config/check_predicates.py; systemTest/schemathesis/schemathesis.toml; systemTest/schemathesis/scripts/run.py …` | `-M` | #809→none |
| 13 | **L13 systemTest-quarantine-tests** | KS-1027(b) | `systemTest/__tests__/pre_suite.test.sh; systemTest/__tests__/quarantine_call_sites.test.sh` | `-M (after L11)` | #927→ks1027 |
| 14 | **L14 e2e-suite** | KS-734(b) | `tests/e2e/** (BASELINE.md, check-e2e-ready.mjs, global-setup.ts, package.json); package.json (the #920 hunk); .gitignore (the #920 hunk) …` | `-N` | #920→ks734 |
| 15 | **L15 api-gateway-mount-auth-test** | KS-736(b) | `services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts` | `-N (after L14)` | #923→ks736 |
| 16 | **L16 docs-only** | KS-1043(c), KS-601(b) | `docs/PR-STATUS-FOR-PETER-2026-09-04.md → docs/archive/; deployment/KINTSUGI-REBUILD-RUNBOOK.md; deployment/DRAFT-kintsugi-notice-HELD.md` | `-O` | #811→none; #943→none |
| 17 | **L17 docker-schema-warning** | KS-968(c) | `docker/init/01-schema.sql` | `-O (after L16)` | #905→trap-schema |
| 18 | **L6 shared-ssrf-guard** | KS-931(c) | `packages/shared/src/security/ssrf-guard.ts; packages/shared/src/__tests__/ks914-shipped-path.test.ts` | `-O (first, 20 min)` | #873→none |
| 19 | **L18 docker-shared-prune** | KS-920(a) | `services/*/Dockerfile (24), shared-builder stage` | `-P` | none (no PR) |
| 20 | **L19 originate-registry-upsert** | KS-598(a) | `services/originate/src/routes/verification.ts (:396 registerInPlatformRegistry); services/originate/src/__tests__/ks598-*` | `-Q` | none (no PR) |

Pane note: the brief listed `Secuura/Blockchain, -B, -D, -E, -F, …` — I assigned in that order and did NOT use `-C` (absent from the brief's list; the coordinator may re-map). Lanes 13/15/17/18 share a pane with the lane above them sequentially (tiny lanes). Worktrees: `ls worktrees/` + `.git/worktrees/*/HEAD` at 22:12; mtimes ≤ 21:57 (s211-merge, 6 staged files at 1c38077ba — a merge seat's leftover, not a lane). No worktree is dirty except `ks1059` (untracked node_modules) and `s211-merge`. **Two detached worktrees carry unpushed lane commits**: `s172-pr813` (fdf0f1d26 minLength + merge 7be1eccbe) and `s172-pr879` (238f8ada0 + merge f1803166f) — on no branch ref, so a fresh clone will not see them.

### Shared-file rule (the three cross-lane collisions, all on ledger/generated files)
- `BACKLOG.md`: #799 (L5), #720 (L3b), #942 (L9) each append a hunk. `Blockchain/Dev/docs/DEV-PROCESS.md`: #887 (L9), #920 (L14). `Blockchain/Dev/docs/openapi/secuura-api.yaml`: #813/#919 (L2), #805/#922 (L4) — generated from `*.openapi.ts`, never hand-edited (`npm run check:openapi` byte-compares). **No lane adds a NEW edit to any of the three**; the merge seat rebases the later PR after the earlier merge. #880 (L5) will ADD a yaml touch (Peter's two description lines live in the generated file's source) — sequence it behind L2/L4 at the merge seat.


## L1 — auth-oauth · pane `Secuura/Blockchain` · rank 1

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-798 | In Progress | High | kamil.kreise | c | #881 `787771b` ms=blocked TE=Y files=5 · PeterObeden CHANGES_REQUESTED@787771b · verdict: none | #881 Peter CHANGES_REQUESTED @787771b on KS-799 only: 'KS-798 and KS-841 are done well… splitting them out for merge now is fine by me' |
| KS-841 | In Progress | High | kamil.kreise | c | #881 `787771b` ms=blocked TE=Y files=5 · PeterObeden CHANGES_REQUESTED@787771b · verdict: none | #881 (see KS-798) |
| KS-799 | In Review | Medium | kamil.kreise | c | #881 `787771b` ms=blocked TE=Y files=5 · PeterObeden CHANGES_REQUESTED@787771b · verdict: none | #881 Peter CHANGES_REQUESTED: 'the consent page's new inline <script> cannot execute in a browser' (CSP) — fix the KS-799 mechanism or split it out |
| KS-790 | In Review | High | kamil.kreise | a | merged:#812 | no PR of its own (#812 is KS-781's); 09-13 07:35: blind getUserById 'is still there — now at routes/oauth.ts:799 AND :849'; fix-shape: swap to getUserByIdPreAuth (exists since #970); after #881 |
| KS-823 | Todo | High | kamil.kreise | a | merged:#831 | auth routes/oauth.ts: /api/oauth/token refresh_token grant authenticates NO client; attached #831 is a docs PR (F-1 round 2), not this fix; after #881 merges |
| KS-835 | Todo | High | kamil.kreise | a | NO PR | auth routes/oauth.ts + services/jwt.ts + api-gateway middleware/auth.ts,scopes.ts: consent scope never reaches the token; fix shapes 1–3 given as 'HYPOTHESES, to be run against the unfixed product first'; after #881 |

**Owns (files):** `Blockchain/Dev/services/auth/src/routes/oauth.ts` · `Blockchain/Dev/services/auth/src/services/jwt.ts` · `Blockchain/Dev/services/auth/src/__tests__/ks798-*,ks799-*,ks841-*,ks781-n1-*` · `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` · `Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/services/auth/src/__tests__/ks781-n1-empty-mfacode-treated-as-absent.test.ts`, `Blockchain/Dev/services/auth/src/__tests__/ks798-consent-form-client-id.test.ts`, `Blockchain/Dev/services/auth/src/__tests__/ks799-consent-form-csrf-submit.test.ts`, `Blockchain/Dev/services/auth/src/__tests__/ks841-consent-form-pkce-and-client-id.test.ts`, `Blockchain/Dev/services/auth/src/routes/oauth.ts`

**Sequence:**
1. #881: fix KS-799 (inline <script> cannot execute under CSP — Peter CHANGES_REQUESTED @787771b) OR split KS-798+KS-841 into their own PR for gate+merge now (Peter: 'splitting them out for merge now is fine by me') → tier-1 gate → merge
2. KS-790 (a): swap blind getUserById → getUserByIdPreAuth at routes/oauth.ts:799 (authorization_code) and :849 (refresh); red-first cell; gate; merge
3. KS-823 (a): refresh_token grant must authenticate the client (routes/oauth.ts); gate; merge
4. KS-835 (a): carry granted scope onto the token (jwt.ts generateTokenPair/generateAccessToken; authMethod:'oauth' label; api-gateway scopes.ts) — ticket says the three fix shapes are 'HYPOTHESES, to be run against the unfixed product first'; gate; merge

**Must NOT touch:** Blockchain/Dev/services/auth/src/repositories/userRepo.ts (no open PR now — but #970/#972 just changed it; read before touching) · Blockchain/Dev/services/api-gateway/src/routes/* (L5 platform.ts; verification.ts family) · Blockchain/Dev/docs/openapi/secuura-api.yaml (L2/L4 own the open edits) · everything under L2–L19

**Worktrees:** #881 → NONE — clone by SHA

**Closes with:** 6 tickets (High, High, Medium, High, High, High).

## L7 — preflight-scripts · pane `-B` · rank 2

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-1046 | In Review | High | kamil.kreise | b | #925 `8a5aff8` ms=unknown TE=Y files=1 · no review · verdict: GO WITH FINDINGS @0956c3dbe — head moved | #925 verdict GO WITH FINDINGS @0956c3dbe (s161) — head moved to 8a5aff8 (F-925-1/2 fixed 09-09) → re-gate; 0 reviews |
| KS-773 | In Review | Medium | kamil.kreise | b | #924 `b85f1db` ms=unknown TE=Y files=1 · no review · verdict: GO WITH FINDINGS @1497b39de — head moved | #924 verdict GO WITH FINDINGS @1497b39de (s161) — head moved to b85f1db (F-924-1 + develop merge) → re-gate |
| KS-926 | In Progress | High | kamil.kreise | c | #874 `6f78856` ms=clean TE=Y files=1 · no review · verdict: none<br>#879 `79f1fcb` ms=clean TE=Y files=2 · PeterObeden APPROVED@79f1fcb · verdict: none<br>#918 `ed954f0` ms=unknown TE=Y files=3 · PeterObeden COMMENTED@ed954f0 · verdict: none | #918 Peter 09-09 COMMENTED @ed954f0 'not approving yet, for one line' (the SKIP-advisory line in the WIRED list); #874 docs (L8); #879 (L8) |
| KS-991 | In Progress | High | kamil.kreise | c | #903 `a70f92d` ms=unknown TE=Y files=2 · no review · verdict: none | #903 Peter 09-08 'The one ask': CASE 7 + CASE 8 cells (stale ancestor develop skips / still runs); .githooks/pre-push + scripts/preflight/preflight.sh |

**Owns (files):** `Blockchain/Dev/scripts/preflight/preflight.sh` · `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh` · `Blockchain/Dev/scripts/run-code-guards.sh` · `Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh` · `.githooks/pre-push`

**Open-PR file list (exact, from `/pulls/N/files`):** `.githooks/pre-push`, `Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh`, `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh`, `Blockchain/Dev/scripts/preflight/preflight.sh`, `Blockchain/Dev/scripts/run-code-guards.sh`

**Sequence:**
1. #925 (b): re-gate at 8a5aff8 (s161 verdict was at 0956c3dbe); merge
2. #924 (b): re-gate at b85f1db (s161 verdict at 1497b39de); merge (lockfile-cleanroom.sh — disjoint from preflight.sh, can go first)
3. #918 (c): Peter's one line (the SKIP-advisory entry in the WIRED list, review @ed954f0) → rebase onto the merged #925 (both edit preflight.sh) → gate → merge
4. #903 (c): add CASE 7 + CASE 8 cells Peter asked for (stale-ancestor develop skips / still runs) → rebase (preflight.sh +24) → gate → merge

**Must NOT touch:** Blockchain/Dev/scripts/check-shared-relink.sh + __tests__/check_shared_relink.test.sh (L8) · Blockchain/Dev/scripts/spec-examples/ (L4) · Blockchain/Dev/scripts/docker-build.sh, scripts/__tests__/ks949_*, docker_build_* (merged tonight — leave) · Blockchain/Dev/scripts/check-stack-safety.sh, __tests__/start_secuura_slot_names.test.sh, Start_Up/ (#959 Peter) · .github/workflows/ (L9)

**Worktrees:** #925 → ks1046; #924 → ks773; #918 → s157-guards; #903 → ks991-hook

**Closes with:** 4 tickets (High, Medium, High, High).

## L9 — ci-workflows · pane `-D` · rank 3

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-1075 | In Progress | High | — | b | #940 `1aa708b` ms=unknown TE=Y files=1 · no review · verdict: none | #940 .github/workflows/security-scan.yml; no review, no verdict; same file as #941 → sequential |
| KS-1077 | In Progress | High | — | b | #941 `d105e07` ms=unknown TE=Y files=2 · no review · verdict: GO WITH FINDINGS @c229aa256 — head moved | #941 security-scan.yml + .security/exceptions.yml; no review, no verdict |
| KS-1078 | In Review | Urgent | — | b | NO PR | #942 NOT attached in Linear (record defect: attach); no review, no verdict; .github/workflows/pr-security-gates.yml + systemTest/__tests__/manifest_quarantine.test.sh + BACKLOG.md |
| KS-961 | In Review | Medium | kamil.kreise | c | #887 `cb7a3e3` ms=unknown TE=Y files=2 · PeterObeden COMMENTED@cb7a3e3 · verdict: none | #887 Peter 09-09 COMMENTED @cb7a3e3 'the change I asked for is in, and it's right. One re-run before I approve' (earlier CHANGES_REQUESTED @bb0502c superseded); .github/workflows/pr-platform-suites.yml + docs/DEV-PROCESS.md |
| KS-1076 | Todo | Urgent | — | a | NO PR | verify-only: item 1 (4 jsdoc errors, systemTest/playwright/global-setup.ts) already on develop via #896 (14:20 sweep, [S] at 721b333a6); item 2 = run the Playwright job on a PR after L9's CI fixes and report; item 3 (.github/workf |

**Owns (files):** `.github/workflows/security-scan.yml` · `.github/workflows/pr-security-gates.yml` · `.github/workflows/pr-platform-suites.yml` · `Blockchain/Dev/.security/exceptions.yml` · `systemTest/__tests__/manifest_quarantine.test.sh` · `Blockchain/Dev/docs/DEV-PROCESS.md (the #887 hunk only)` · `BACKLOG.md (the #942 hunk only)`

**Open-PR file list (exact, from `/pulls/N/files`):** `.github/workflows/pr-platform-suites.yml`, `.github/workflows/pr-security-gates.yml`, `.github/workflows/security-scan.yml`, `BACKLOG.md`, `Blockchain/Dev/.security/exceptions.yml`, `Blockchain/Dev/docs/DEV-PROCESS.md`, `systemTest/__tests__/manifest_quarantine.test.sh`

**Sequence:**
1. attach #942 to KS-1078 in Linear (record defect)
2. #940 (b) gate → merge; then #941 (b) rebase (same security-scan.yml) → gate → merge
3. #942 (b) gate → merge
4. #887 (c): the ONE re-run Peter asked for @cb7a3e3, post it on the PR → gate → merge
5. KS-1076 (a, verify-only): with the gates green, run the Playwright job on a PR and record on the ticket whether a browser test executed; item 1 is already on develop (#896); item 3 is Kam-class

**Must NOT touch:** any NEW workflow edit beyond the four PRs' diffs — .github/workflows/ is Kam-class per the 14:20 standing list; a new edit pauses for Kam · systemTest/__tests__/pre_suite.test.sh, quarantine_call_sites.test.sh (L13) · systemTest/playwright/global-setup.ts (already fixed on develop)

**Worktrees:** #940 → NONE — clone by SHA; #941 → NONE — clone by SHA; #942 → NONE — clone by SHA; #887 → rb-887

**Closes with:** 5 tickets (High, High, Urgent, Medium, Urgent).

## L5 — shared-security-revoke · pane `-E` · rank 4

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-764 | In Progress | High | kamil.kreise | c | #799 `38f6377` ms=unstable TE=Y files=12 · PeterObeden COMMENTED@7dfc7eb · verdict: None @2026-09-04-799-majors-landing-through-code — head moved | #799 Peter 09-09 10:43 'Outstanding at head 7dfc7ebca — three lines and a fixture': KS-860 app.listen loopback ×2 (red on branch), F-2 assertion line, F-3 no-tenantId fixture; head now 38f6377 (develop merge?) — re-read; mergeable |
| KS-577 | In Review | High | kamil.kreise | c | #880 `85f8263` ms=clean TE=Y files=3 · PeterObeden COMMENTED@85f8263 · verdict: none | #880 Peter 09-09 'Conditional approval — two lines of YAML, and this is a yes: approving once the two secuura-api.yaml descriptions are corrected' (files: api-gateway routes/platform.ts, security/src/index.ts + test; yaml not in t |
| KS-780 | Todo | Medium | kamil.kreise | a | NO PR | move normaliseOrgId into @secuura/shared: packages/shared/src/security/keyRevokePolicy.ts is #799's new file → after #799 |

**Owns (files):** `Blockchain/Dev/packages/shared/src/index.ts` · `Blockchain/Dev/packages/shared/src/middleware/index.ts` · `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts` · `Blockchain/Dev/packages/shared/src/__tests__/ks764-*` · `Blockchain/Dev/services/security/src/index.ts` · `Blockchain/Dev/services/security/src/keyRevokePolicy.ts` · `Blockchain/Dev/services/security/src/__tests__/ks764-*,ks577-*` · `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` · `Blockchain/Dev/services/originate/src/middleware/auth.ts` · `Blockchain/Dev/services/originate/src/__tests__/ks764-*` · `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` · `Blockchain/Dev/services/originate/src/services/orgId.ts (KS-780 only, after #799)`

**Open-PR file list (exact, from `/pulls/N/files`):** `BACKLOG.md`, `Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts`, `Blockchain/Dev/packages/shared/src/index.ts`, `Blockchain/Dev/packages/shared/src/middleware/index.ts`, `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts`, `Blockchain/Dev/services/api-gateway/src/routes/platform.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts`, `Blockchain/Dev/services/originate/src/middleware/auth.ts`, `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`, `Blockchain/Dev/services/security/src/__tests__/ks577-revoke-on-rotate.test.ts`, `Blockchain/Dev/services/security/src/__tests__/ks764-key-revoke-organisation-arm.test.ts`, `Blockchain/Dev/services/security/src/__tests__/ks764-revoke-organisation-route-contract.test.ts`, `Blockchain/Dev/services/security/src/index.ts`, `Blockchain/Dev/services/security/src/keyRevokePolicy.ts`

**Sequence:**
1. #799 (c): Peter's 3 lines + 1 fixture @7dfc7ebca (KS-860 loopback ×2 — RED on the branch; F-2 typeof assertion; F-3 no-tenantId fixture); head is 38f6377 (develop merge 09-10) — mergeable_state=unstable; fix → gate → merge
2. #880 (c): correct the two secuura-api.yaml descriptions Peter named @85f8263 (source is the *.openapi.ts that generates them — this ADDS a yaml touch: sequence at the merge seat behind L2/L4) → rebase onto merged #799 (both edit services/security/src/index.ts) → gate → merge
3. KS-780 (a): move normaliseOrgId into @secuura/shared (keyRevokePolicy.ts + orgId.ts) after #799; red-first tamper cell in both places

**Must NOT touch:** Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts + __tests__/ks914-* (L6) · Blockchain/Dev/packages/shared/src/openapi/*, __tests__/ks256-* (L4) · Blockchain/Dev/packages/shared/src/__tests__/ks860,ks879,ks781-p3-3,entrypoint-corpus* (merged tonight) · KS-579/580/581 platform.ts features — POST-lane spares only

**Worktrees:** #799 → NONE — clone by SHA; #880 → rb-880

**Closes with:** 3 tickets (High, High, Medium).

## L3a — originate-anchorStateSync · pane `-F` · rank 5

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-1004 | In Progress | High | — | c | #912 `ae8751f` ms=unknown TE=Y files=3 · no review · verdict: none | #912: builder-posted tier-1 NO GO r1 (09-09 06:55, transcription) + Peter 09-09 13:44: 3 one-liners (threadToken/confidence dropped → #939 owns the type; anchoredAt comment; inFlight&& → #937 owns) + 'systemTest evidence — what's  |
| KS-1059 | In Review | Urgent | kamil.kreise | b | #937 `cf8b233` ms=unknown TE=Y files=4 · no review · verdict: none | #937 Urgent; 0 ticket comments, no review, no verdict; adds ks1059 test on anchorStateSync:360 (#912's line) — NOTE ride-along +3/-3 in three systemTest package-lock.json files, read before gating |

**Owns (files):** `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` · `Blockchain/Dev/services/originate/src/__tests__/ks1004-*` · `Blockchain/Dev/services/originate/src/__tests__/ks535-anchor-async-fail-propagates.test.ts` · `Blockchain/Dev/services/originate/src/__tests__/ks1059-*`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/services/originate/src/__tests__/ks1004-anchor-failed-lockout.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks535-anchor-async-fail-propagates.test.ts`, `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts`, `systemTest/api-explorer/package-lock.json`, `systemTest/performance/package-lock.json`, `systemTest/playwright/package-lock.json`

**Sequence:**
1. #912 (c): Peter's three one-liners (threadToken/confidence drop → note it is #939/L2's type fix, do NOT widen here; anchoredAt comment; inFlight&& is #937's cell) + the systemTest evidence he lists + the builder-transcribed tier-1 NO GO r1 → fix → tier-1 gate at the new head → merge
2. #937 (b): rebase onto merged #912 (its cell pins #912's line); READ the ride-along +3/-3 in systemTest/{api-explorer,performance,playwright}/package-lock.json and drop it if unowned → gate → merge

**Must NOT touch:** Blockchain/Dev/services/originate/src/routes/documents.ts, repositories/documentRepo.ts, originate.openapi.ts (L2) · Blockchain/Dev/services/originate/src/__tests__/ every other file (L3b owns the mock-factory set) · Blockchain/Dev/services/originate/src/routes/verification.ts (L19), routes/anchors.ts + middleware (L4's KS-741)

**Worktrees:** #912 → NONE — clone by SHA; #937 → ks1059

**Closes with:** 2 tickets (High, Urgent).

## L3b — originate-test-mocks · pane `-G` · rank 6

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-1061 | In Review | Medium | — | b | #931 `f2e0cb3` ms=unknown TE=Y files=12 · no review · verdict: none | #931 no review, no verdict; builder 09-13 05:02: #965 merged first with a hand-written root jest.mock in ks1103-verify-hash-field.test.ts:45-48 — rebase + fold that file in before the gate |
| KS-487 | In Progress | High | kamil.kreise | c | #720 `fcc611d` ms=dirty TE=Y files=2 · no review · verdict: none | #720 mergeable_state=dirty (conflict) — rebase; Peter 09-09 pass 2: 'the five changes I asked for on 2026-08-31 haven't landed' (4 one-line edits + 1 assertion); files BACKLOG.md + ks444 test (#931 edits ks444 too) |
| KS-657 | In Review | Medium | kamil.kreise | c | #720 `fcc611d` ms=dirty TE=Y files=2 · no review · verdict: none | #720 (with KS-487) |
| KS-777 | Todo | Medium | kamil.kreise | a | NO PR | residue only: rename qa-f4-resolveonbehalfof-org-normalisation.test.ts to the ksNNN-* convention ('All four are FIXED on #795') — #931 edits that file → after #931 |

**Owns (files):** `Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts` · `Blockchain/Dev/services/originate/src/__tests__/{gdprService.erasure,ks444-webhooks-create-description-guard,ks445-*,ks563-*,ks584-*,ks695-*,ks914-deliver-webhook-*,qa-f4-*,ks1061-*,ks1103-verify-hash-field}.test.ts` · `BACKLOG.md (the #720 hunk)`

**Open-PR file list (exact, from `/pulls/N/files`):** `BACKLOG.md`, `Blockchain/Dev/services/originate/src/__tests__/gdprService.erasure.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks444-webhooks-create-description-guard.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks445-pg-error-classification.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks563-certified-vs-anchored.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks584-p3-verify-list.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks584-verify-row-selection.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks695-erasure-by-external-ref.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts`

**Sequence:**
1. #931 (b): rebase onto develop 8861e6216 — #965's ks1103-verify-hash-field.test.ts:45-48 carries a hand-written root jest.mock; fold it into makeSharedMock → gate → merge
2. #720 (c): mergeable_state=DIRTY — rebase (ks444 test is also in #931: take #931 first); land Peter's five 2026-08-31 asks (1 toHaveBeenCalled on the guard in a 201 case; ':40 3 of 5 → 2 of 4'; merge the two threadTokenMint rows; tick BACKLOG.md:315; +1) → gate → merge → KS-487 + KS-657
3. KS-777 (a): rename qa-f4-resolveonbehalfof-org-normalisation.test.ts to the ks-NNN convention after #931 lands (that file is in #931's diff)

**Must NOT touch:** Blockchain/Dev/services/originate/src/__tests__/ks1004-*, ks535-*, ks1059-* (L3a) · Blockchain/Dev/services/originate/src/ (product files) — this lane is tests only; a product change = a finding to file · Blockchain/Dev/services/originate/src/__tests__/ks739-*, ks1068-* (L2)

**Worktrees:** #931 → NONE — clone by SHA; #720 → rebase-720

**Closes with:** 4 tickets (Medium, High, Medium, Medium).

## L2 — originate-documents-openapi · pane `-H` · rank 7

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-739 | In Review | High | kamil.kreise | c | #919 `d0aff46` ms=unknown TE=Y files=4 · no review · verdict: none | #919 Peter 09-09 12:27 'I have not approved yet — two small, non-code items… Nothing in the implementation is in my way' (PR-body items) → fix body, gate |
| KS-1068 | In Review | Medium | kamil.kreise | b | #939 `481e026` ms=unknown TE=Y files=3 · no review · verdict: none | #939 no review, no verdict; documentRepo.ts + routes/documents.ts (#919 edits routes/documents.ts too) |
| KS-791 | In Review | Medium | kamil.kreise | c | #813 `54225cb` ms=clean TE=Y files=4 · PeterObeden COMMENTED@54225cb (APPROVED then withdrawn by comment) · verdict: none | #813 Peter APPROVED then COMMENTED @54225cb 'My earlier approval on this PR was premature and I'm withdrawing it' — wants minLength:1 + systemTest evidence (Akto/Playwright/k6 'not run at all'); the minLength commit is LOCAL fdf0f |

**Owns (files):** `Blockchain/Dev/services/originate/src/routes/documents.ts` · `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts` · `Blockchain/Dev/services/originate/src/originate.openapi.ts` · `Blockchain/Dev/services/originate/src/__tests__/ks739-*,ks1068-*` · `Blockchain/Dev/services/api-gateway/src/middleware/contentType.ts` · `Blockchain/Dev/services/api-gateway/src/__tests__/contentType.test.ts` · `Blockchain/Dev/docs/openapi/secuura-api.yaml (the #919/#813 hunks — generated; regenerate, never hand-edit)`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/docs/openapi/secuura-api.yaml`, `Blockchain/Dev/services/api-gateway/src/__tests__/contentType.test.ts`, `Blockchain/Dev/services/api-gateway/src/middleware/contentType.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1068-blockchain-blob-type.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts`, `Blockchain/Dev/services/originate/src/originate.openapi.ts`, `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts`, `Blockchain/Dev/services/originate/src/routes/documents.ts`

**Sequence:**
1. #919 (c): Peter's 'two small, non-code items' at the bottom of his 09-09 12:27 comment (PR-body) → gate → merge
2. #939 (b): rebase onto merged #919 (both edit routes/documents.ts) → gate → merge
3. #813 (c): push the LOCAL minLength:1 commit fdf0f1d26 (worktree s172-pr813, detached; + develop merge 7be1eccbe) under the LEG-14 push rule; Peter withdrew his approval @54225cb for 'complete systemTest evidence' (Akto/Playwright/k6) — the tier-2 gate supplies it → rebase (originate.openapi.ts is in #919 too) → merge

**Must NOT touch:** Blockchain/Dev/services/originate/src/services/anchorStateSync.ts (L3a) · Blockchain/Dev/services/originate/src/__tests__/ mock-factory set (L3b) · Blockchain/Dev/services/anchoring/**, anchoring.openapi.ts (L4) · any yaml hunk not produced by regenerating from this lane's *.openapi.ts

**Worktrees:** #919 → ks739; #939 → NONE — clone by SHA; #813 → NONE — clone by SHA

**Closes with:** 3 tickets (High, Medium, Medium).

## L10 — systemTest-performance-fixtures · pane `-I` · rank 8

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-993 | In Progress | High | kamil.kreise | b | #916 `584b12b` ms=unknown TE=Y files=3 · no review · verdict: none | #916 (with KS-1026) |
| KS-1026 | In Progress | High | kamil.kreise | b | #916 `584b12b` ms=unknown TE=Y files=3 · no review · verdict: none | #916 READY FOR QA 09-09 ('584b12ba1 on origin'); no review, no verdict |
| KS-973 | Todo | Medium | kamil.kreise | a | NO PR | six items on systemTest/fixtures + performance/runner/actor_manifest.ts (#916 edits it) + playwright/config/actorManifest.ts + schemathesis/tests/actor_manifest.py → after #916 |
| KS-704 | Todo | Medium | kamil.kreise | a | NO PR | systemTest/performance gate/report.ts: add status-code breakdown to the k6 gate failure line; no open PR touches gate/ |
| KS-711 | Todo | Medium | kamil.kreise | a | NO PR | systemTest/akto + performance docs/quick_start.md + runner/cli.ts; #758 CLOSED unmerged 09-08 ('nothing landed') — restart from ticket |

**Owns (files):** `systemTest/package.json` · `systemTest/performance/runner/actor_manifest.ts + tests/unit/runner/actor_manifest.test.ts` · `systemTest/performance/gate/report.ts` · `systemTest/fixtures/**` · `systemTest/playwright/config/actorManifest.ts` · `systemTest/schemathesis/tests/actor_manifest.py` · `systemTest/akto/docs/quick_start.md, systemTest/performance/docs/quick_start.md, runner/cli.ts`

**Open-PR file list (exact, from `/pulls/N/files`):** `systemTest/package.json`, `systemTest/performance/runner/actor_manifest.ts`, `systemTest/performance/tests/unit/runner/actor_manifest.test.ts`

**Sequence:**
1. #916 (b): READY FOR QA @584b12b (KS-993 + KS-1026) → gate → merge
2. KS-973 (a): six items on the pre-suite step (actor_manifest.ts is #916's file — after it merges); red-first per item
3. KS-704 (a): status-code breakdown on the k6 gate failure line (gate/report.ts)
4. KS-711 (a): akto + performance quick_start.md gates red; #758 closed unmerged — restart

**Must NOT touch:** systemTest/performance/utils/yaml.ts + tests/unit/utils/yamlRedaction* (merged #963 — leave) · systemTest/akto/config/*, src/setup/* (L12) · systemTest/schemathesis/config/*, scripts/run.py (L11) · systemTest/__tests__/ (L9/L13) · systemTest/*/package-lock.json (#937's ride-along, L3a decides)

**Worktrees:** #916 → s158-systemtest

**Closes with:** 5 tickets (High, High, Medium, Medium, Medium).

## L8 — relink-guard-and-launcher · pane `-J` · rank 9

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-945 | In Review | High | kamil.kreise | c | #879 `79f1fcb` ms=clean TE=Y files=2 · PeterObeden APPROVED@79f1fcb · verdict: none | #879 Peter APPROVED @79f1fcb + 'THE UNIT TEST GAP IS EXACTLY TWO THINGS'; the fix is LOCAL commit 238f8ada0 in worktree s172-pr879 (detached, + develop merge f1803166f), on NO branch ref — push under the LEG-14 hold rule, then gat |
| KS-926 | In Progress | High | kamil.kreise | c | #874 `6f78856` ms=clean TE=Y files=1 · no review · verdict: none<br>#879 `79f1fcb` ms=clean TE=Y files=2 · PeterObeden APPROVED@79f1fcb · verdict: none<br>#918 `ed954f0` ms=unknown TE=Y files=3 · PeterObeden COMMENTED@ed954f0 · verdict: none | #918 Peter 09-09 COMMENTED @ed954f0 'not approving yet, for one line' (the SKIP-advisory line in the WIRED list); #874 docs (L8); #879 (L8) |
| KS-930 | In Progress | Medium | kamil.kreise | h | #874 `6f78856` ms=clean TE=Y files=1 · no review · verdict: none<br>#879 `79f1fcb` ms=clean TE=Y files=2 · PeterObeden APPROVED@79f1fcb · verdict: none | #876 (round 3) + #886 merged; #879 attached — verify residues closed, move |
| KS-937 | In Progress | High | kamil.kreise | h | #874 `6f78856` ms=clean TE=Y files=1 · no review · verdict: none | 0 comments; #876 merged — verify whether the awk case-sensitivity residue landed in #876/#879 (check-shared-relink.sh), then move or re-open as (a) |
| KS-911 | In Progress | Medium | kamil.kreise | b | #874 `6f78856` ms=clean TE=Y files=1 · no review · verdict: none | 09-06: 'BUILT and READY FOR QA — held for the gate. Ships BY HASH with KS-912; the launcher is at the project root, outside git' — gate the by-hash launcher change |
| KS-912 | In Progress | Low | kamil.kreise | b | #874 `6f78856` ms=clean TE=Y files=1 · no review · verdict: none | (with KS-911) |

**Owns (files):** `Blockchain/Dev/scripts/check-shared-relink.sh` · `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh` · `Blockchain/Dev/docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md` · `Launch_Claude.seats.test.sh (project root, OUTSIDE git — by-hash)`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md`, `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh`, `Blockchain/Dev/scripts/check-shared-relink.sh`

**Sequence:**
1. #879 (c): push LOCAL commit 238f8ada0 (worktree s172-pr879, detached; + develop merge f1803166f) under the LEG-14 rule — it carries Peter's two test asks (npm run pinned as a write; version/help probes ahead of the fail-closed default); Peter APPROVED @79f1fcb → gate → merge → KS-945; then verify KS-937 (awk case-sensitivity) + KS-930 residues against the merged guard and move them
2. #874 (b): docs-only census — tier-2 read gate → merge (KS-926 closes only when #918 in L7 also merges)
3. KS-911/KS-912 (b): gate the by-hash launcher change (sha256 recorded on the tickets 09-06) — no repo files

**Must NOT touch:** Blockchain/Dev/scripts/preflight/*, run-code-guards.sh (L7) · Blockchain/Dev/scripts/docker-build.sh (merged #977) · Launch_Claude.command itself (Kam's launcher)

**Worktrees:** #879 → NONE — clone by SHA; #874 → NONE — clone by SHA

**Closes with:** 6 tickets (High, High, Medium, High, Medium, Low).

## L4 — anchoring-and-spec-examples · pane `-K` · rank 10

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-726 | In Review | Medium | kamil.kreise | c | #805 `97e2161` ms=clean TE=Y files=9 · no review · verdict: none | #805 Peter 09-08 'F1–F4 all land. Holding on one new finding, and it is a question rather than a verdict… if you tell me the trade is deliberate I will take your read and approve' — the builder answers on the PR (answer-class; esc |
| KS-679 | In Review | Medium | kamil.kreise | c | #922 `2b5075e` ms=unknown TE=Y files=5 · no review · verdict: none | #922 Peter 09-09 'three things holding up approval': 1 commit the BENIGN_SHAPES seven-case control as a cell; 2 PR body Linear URL + two ack checkboxes; 3 (read on the PR) — 'none of the three reasons is about the substance' |
| KS-741 | Todo | Medium | kamil.kreise | a | NO PR | 09-11: 'hold condition is met… Not started.' Files: originate middleware + routes/anchors.ts, api-gateway/src/index.ts, anchoring/src/index.ts (#805 edits anchoring/src/index.ts +121) → after #805 |

**Owns (files):** `Blockchain/Dev/services/anchoring/src/** (anchorSubmission.ts, cardano/index.ts, index.ts, reconciler.ts, verifyAnchorStatus.ts, anchoring.openapi.ts, __tests__/ks726-*)` · `Blockchain/Dev/packages/shared/src/openapi/examples/fixtures.ts` · `Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` · `Blockchain/Dev/scripts/spec-examples/check/contract.mjs` · `Blockchain/Dev/docs/openapi/secuura-api.yaml (the #805/#922 hunks — generated)` · `Blockchain/Dev/services/originate/src/routes/anchors.ts + middleware (KS-741 only, after #805)` · `Blockchain/Dev/services/api-gateway/src/index.ts (KS-741 only)`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/docs/openapi/secuura-api.yaml`, `Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts`, `Blockchain/Dev/packages/shared/src/openapi/examples/fixtures.ts`, `Blockchain/Dev/scripts/spec-examples/check/contract.mjs`, `Blockchain/Dev/services/anchoring/src/__tests__/ks726-review-f1-f3.test.ts`, `Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts`, `Blockchain/Dev/services/anchoring/src/anchorSubmission.ts`, `Blockchain/Dev/services/anchoring/src/anchoring.openapi.ts`, `Blockchain/Dev/services/anchoring/src/cardano/index.ts`, `Blockchain/Dev/services/anchoring/src/index.ts`, `Blockchain/Dev/services/anchoring/src/reconciler.ts`, `Blockchain/Dev/services/anchoring/src/verifyAnchorStatus.ts`

**Sequence:**
1. #805 (c): answer Peter's guard-5 question on the PR ('if you tell me the trade is deliberate I will take your read and approve') — answer-class; if the builder cannot assert the trade, escalate to Kam instead of guessing → tier-1 gate (real anchoring path) → merge
2. #922 (c): commit the BENIGN_SHAPES seven-case control as a cell; add the Linear URL + two ack checkboxes to the body; read item 3 on the PR → rebase (anchoring.openapi.ts is in #805) → gate → merge
3. KS-741 (a): strip x-emitter-internal in originate's own middleware + a test that a client header never reaches anchoring + fix the comment (anchoring/src/index.ts is #805's file — after it)

**Must NOT touch:** Blockchain/Dev/packages/shared/src/security/*, index.ts, middleware/index.ts (L5/L6) · Blockchain/Dev/services/originate/src/routes/documents.ts, verification.ts (L2/L19)

**Worktrees:** #805 → NONE — clone by SHA; #922 → ks679

**Closes with:** 3 tickets (Medium, Medium, Medium).

## L12 — akto-harness · pane `-L` · rank 11

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-716 | Todo | High | kamil.kreise | a | NO PR | systemTest/akto config/secrets.yml + secrets.example.yml: add the system_admin block so resolveReplayTokens() gets adminToken; 16 super-admin endpoints unscanned |
| KS-724 | Todo | High | kamil.kreise | a | NO PR | akto harness: >10 logins as one user evict the scan bearer (GET /api/sessions window) — reuse one session per persona in the harness |
| KS-725 | Todo | High | kamil.kreise | a | NO PR | akto test:pr never re-imports the OpenAPI spec (08-31: 'after a spec re-import, Akto CAN see identityCommitment') — add the re-import step to test:pr |

**Owns (files):** `systemTest/akto/config/secrets.yml, secrets.example.yml` · `systemTest/akto/src/** (setup, core, client)` · `systemTest/akto/tests/**`

**Sequence:**
1. KS-716 (a): add the system_admin block (secrets.example.yml documents it) so the issuer→admin replay fallback fires; prove the 9 non-excluded super-admin endpoints get scanned
2. KS-725 (a): make test:pr re-import the spec (08-31 measurement shows re-import is what makes a new field visible)
3. KS-724 (a): stop the harness logging in >10× as one user (session window evicts the bearer) — one session per persona

**Must NOT touch:** systemTest/akto/docs/quick_start.md (L10's KS-711) · systemTest/akto/src/config/secrets.ts:40 + src/core/runDir.ts (14:20 sweep R3: KS-1108/KS-755 — Backlog, not on this board; leave)

**Worktrees:** none (build lane — branch from develop 8861e6216)

**Closes with:** 3 tickets (High, High, High).

## L11 — schemathesis · pane `-M` · rank 12

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-693 | In Review | High | kamil.kreise | b | #809 `aa2270f` ms=clean TE=Y files=2 · no review · verdict: none | #809 systemTest/schemathesis config/check_predicates.py + schemathesis.toml; no review, no verdict |
| KS-738 | Todo | Medium | kamil.kreise | a | NO PR | systemTest/schemathesis scripts/run.py:124-131 os.execv loop guard (fix option 1 given) + tests/unit/runner/test_prevenv_bootstrap.py |

**Owns (files):** `systemTest/schemathesis/config/check_predicates.py` · `systemTest/schemathesis/schemathesis.toml` · `systemTest/schemathesis/scripts/run.py` · `systemTest/schemathesis/tests/unit/runner/test_prevenv_bootstrap.py`

**Open-PR file list (exact, from `/pulls/N/files`):** `systemTest/schemathesis/config/check_predicates.py`, `systemTest/schemathesis/schemathesis.toml`

**Sequence:**
1. #809 (b): gate at aa2270f (interim guard for the 8 M365 unconfigured-503 ops) → merge
2. KS-738 (a): loop guard in run.py:124-131 (fix option 1 in the ticket) + red-first unit test

**Must NOT touch:** systemTest/schemathesis/tests/actor_manifest.py (L10's KS-973)

**Worktrees:** #809 → NONE — clone by SHA

**Closes with:** 2 tickets (High, Medium).

## L13 — systemTest-quarantine-tests · pane `-M (after L11)` · rank 13

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-1027 | In Review | Medium | kamil.kreise | b | #927 `1041d2d` ms=unknown TE=Y files=2 · PeterObeden APPROVED@63e955e · verdict: GO WITH FINDINGS @63e955e0f — head moved | #927 verdict GO WITH FINDINGS @63e955e0f (s161) + Peter APPROVED @63e955e — head moved to 1041d2d (F-927-1) → re-gate |

**Owns (files):** `systemTest/__tests__/pre_suite.test.sh` · `systemTest/__tests__/quarantine_call_sites.test.sh`

**Open-PR file list (exact, from `/pulls/N/files`):** `systemTest/__tests__/pre_suite.test.sh`, `systemTest/__tests__/quarantine_call_sites.test.sh`

**Sequence:**
1. #927 (b): re-gate at 1041d2d (s161 verdict + Peter APPROVED were at 63e955e0f; F-927-1 ride-along since) → merge

**Must NOT touch:** systemTest/__tests__/manifest_quarantine.test.sh (L9's #942)

**Worktrees:** #927 → ks1027

**Closes with:** 1 tickets (Medium).

## L14 — e2e-suite · pane `-N` · rank 14

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-734 | In Review | High | kamil.kreise | b | #920 `2112a99` ms=unknown TE=Y files=7 · no review · verdict: none | #920 'READY FOR QA. Not merged.'; no review, no verdict; touches Blockchain/Dev/package.json, .gitignore, docs/DEV-PROCESS.md (#887 also edits DEV-PROCESS.md) |

**Owns (files):** `Blockchain/Dev/tests/e2e/** (BASELINE.md, check-e2e-ready.mjs, global-setup.ts, package.json)` · `Blockchain/Dev/package.json (the #920 hunk)` · `.gitignore (the #920 hunk)` · `Blockchain/Dev/docs/DEV-PROCESS.md (the #920 hunk)`

**Open-PR file list (exact, from `/pulls/N/files`):** `.gitignore`, `Blockchain/Dev/docs/DEV-PROCESS.md`, `Blockchain/Dev/package.json`, `Blockchain/Dev/tests/e2e/BASELINE.md`, `Blockchain/Dev/tests/e2e/check-e2e-ready.mjs`, `Blockchain/Dev/tests/e2e/global-setup.ts`, `Blockchain/Dev/tests/e2e/package.json`

**Sequence:**
1. #920 (b): gate at 2112a99 (clean-checkout install + baseline) → merge; DEV-PROCESS.md is also in #887 (L9) — additive, merge seat sequences

**Must NOT touch:** systemTest/playwright/** (not tests/e2e) · dependabot's package.json/lockfile PRs (theirs)

**Worktrees:** #920 → ks734

**Closes with:** 1 tickets (High).

## L15 — api-gateway-mount-auth-test · pane `-N (after L14)` · rank 15

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-736 | In Review | Medium | kamil.kreise | b | #923 `d127dc7` ms=unknown TE=Y files=1 · no review · verdict: none | #923 'READY FOR QA. Not merged.'; one test file; no review, no verdict |

**Owns (files):** `Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts`

**Sequence:**
1. #923 (b): gate at d127dc7 (one test file) → merge

**Must NOT touch:** Blockchain/Dev/services/api-gateway/src/routes/**, middleware/** (L1/L2/L5)

**Worktrees:** #923 → ks736

**Closes with:** 1 tickets (Medium).

## L16 — docs-only · pane `-O` · rank 16

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-1043 | In Review | Medium | kamil.kreise | c | #811 `6200833` ms=clean TE=Y files=1 · PeterObeden COMMENTED@6200833 · verdict: none | #811 Peter 09-09 COMMENTED: '1. Re-measure, or move the file to Blockchain/Dev/docs/archive/ 2. Correct or drop the #800 paragraph 3. Attach a Linear ticket to the PR body' |
| KS-601 | In Progress | High | kamil.kreise | b | #943 `4e1bd16` ms=unknown TE=Y files=2 · no review · verdict: none | #943 docs-only (deployment/KINTSUGI-REBUILD-RUNBOOK.md + DRAFT notice HELD); no review, no verdict; Kintsugi is Kam's box — read gate, no deploy |

**Owns (files):** `Blockchain/Dev/docs/PR-STATUS-FOR-PETER-2026-09-04.md → docs/archive/` · `Blockchain/Dev/deployment/KINTSUGI-REBUILD-RUNBOOK.md` · `Blockchain/Dev/deployment/DRAFT-kintsugi-notice-HELD.md`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/deployment/DRAFT-kintsugi-notice-HELD.md`, `Blockchain/Dev/deployment/KINTSUGI-REBUILD-RUNBOOK.md`, `Blockchain/Dev/docs/PR-STATUS-FOR-PETER-2026-09-04.md`

**Sequence:**
1. #811 (c): Peter's three asks — move the snapshot to docs/archive/ (or re-measure), drop the #800 paragraph, put KS-1043 in the body → read gate → merge
2. #943 (b): tier-2 read gate on the runbook (no deploy, Kintsugi is Kam's box) → merge

**Must NOT touch:** Blockchain/Dev/docs/DEV-PROCESS.md (L9/L14) · Blockchain/Dev/docs/openapi/** (L2/L4)

**Worktrees:** #811 → NONE — clone by SHA; #943 → NONE — clone by SHA

**Closes with:** 2 tickets (Medium, High).

## L17 — docker-schema-warning · pane `-O (after L16)` · rank 17

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-968 | In Progress | High | kamil.kreise | c | #905 `c38040b` ms=unknown TE=Y files=1 · no review · verdict: none | #905 Peter 09-08 'holding off on approval for two lines, not for the idea' — docker/init/01-schema.sql |

**Owns (files):** `Blockchain/Dev/docker/init/01-schema.sql`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/docker/init/01-schema.sql`

**Sequence:**
1. #905 (c): Peter's two lines (@c38040b, 09-08) → gate → merge

**Must NOT touch:** Blockchain/Dev/migrations/** (KS-1054/1055 need Kam)

**Worktrees:** #905 → trap-schema

**Closes with:** 1 tickets (High).

## L6 — shared-ssrf-guard · pane `-O (first, 20 min)` · rank 18

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-931 | In Review | Medium | kamil.kreise | c | #873 `7d8a3f0` ms=clean TE=Y files=2 · no review · verdict: none | #873 Peter 09-09 'holding approval on one clerical thing and one number that doesn't match — neither is about the code' (PR body) → fix body, gate |

**Owns (files):** `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts` · `Blockchain/Dev/packages/shared/src/__tests__/ks914-shipped-path.test.ts`

**Open-PR file list (exact, from `/pulls/N/files`):** `Blockchain/Dev/packages/shared/src/__tests__/ks914-shipped-path.test.ts`, `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts`

**Sequence:**
1. #873 (c): PR-body only — the clerical item + the 784+7 vs 787+4 count Peter laid out 09-09 12:50 → gate → merge

**Must NOT touch:** Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts, index.ts, middleware/ (L5)

**Worktrees:** #873 → NONE — clone by SHA

**Closes with:** 1 tickets (Medium).

## L18 — docker-shared-prune · pane `-P` · rank 19

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-920 | In Progress | Medium | kamil.kreise | a | NO PR | /shared prune in the shared-builder stage across 24 Dockerfiles; ticket: 'needs a real start probe per service, not reasoning'; no open PR touches a Dockerfile |

**Owns (files):** `Blockchain/Dev/services/*/Dockerfile (24), shared-builder stage`

**Sequence:**
1. KS-920 (a): prune /shared after the shared-builder build; the ticket requires 'a real start probe per service, not reasoning' (the #851 hazard) — every image must boot; local only

**Must NOT touch:** Start_Up/, check-stack-safety.sh (#959 Peter) · docker-compose*.yml (KS-762 Blocked on Kam)

**Worktrees:** none (build lane — branch from develop 8861e6216)

**Closes with:** 1 tickets (Medium).

## L19 — originate-registry-upsert · pane `-Q` · rank 20

| Ticket | State | Prio | Assignee | Class | PR · head · ms · TE · review · verdict | Measured note |
|---|---|---|---|---|---|---|
| KS-598 | Todo | High | kamil.kreise | a | NO PR | originate/src/routes/verification.ts:396 upsert; ticket offers two fix shapes ('re-key the registry on the document UUID, or explicitly remove/disable the upsert') — builder picks the smaller (disable) and says so; no open PR touc |

**Owns (files):** `Blockchain/Dev/services/originate/src/routes/verification.ts (:396 registerInPlatformRegistry)` · `Blockchain/Dev/services/originate/src/__tests__/ks598-*`

**Sequence:**
1. KS-598 (a): defuse the MULTI_TENANCY upsert — the ticket accepts either 're-key the registry on the document UUID, or explicitly remove/disable the upsert'; take the smaller, say which, red-first cell with MULTI_TENANCY_ENABLED=true

**Must NOT touch:** Blockchain/Dev/services/originate/src/routes/verification.ts hunks from #965 (merged) — rebase-read first · everything else in originate (L2/L3a/L3b)

**Worktrees:** none (build lane — branch from develop 8861e6216)

**Closes with:** 1 tickets (High).

## Post-merge spares (class a, deferred — file held by a lane PR)

- **KS-723** High Todo: declare ~157 routed-but-undocumented /api ops in the spec — spans every *.openapi.ts → regenerates docs/openapi/secuura-api.yaml, which #813/#919/#922/#805 all edit → after L2 + L4 merge
- **KS-579** Medium Todo: api-gateway routes/platform.ts — same file as #880 (L5); feature-shaped; after #880
- **KS-580** Medium Todo: api-gateway routes/platform.ts + services/security/src/index.ts — both in #880/#799 (L5); after L5
- **KS-581** Medium Todo: api-gateway routes/platform.ts — same file as #880; after L5
- **KS-669** High In Progress: #725 merged; 's54 measured 17 of its 18 URLs still open work' — spec URL edits regenerate secuura-api.yaml → with KS-723 after L2/L4

## Not lanes — class h: 14 record defects (own PR merged, nothing left by the ticket's words) → a Linear-write seat verifies + moves; the cheapest −14 toward ≤ 60

| Ticket | State | Merged PRs | Words / what to verify |
|---|---|---|---|
| KS-664 | In Progress | #725 | #725 merged; 08-26: 'No change to the row' — verify nothing remains, move |
| KS-695 | In Progress | #788, #790 | #788/#790 merged; 09-09: 'KS-695 is not blocked on the re-key work, and you can proceed' (to Stuart) — verify K-side done, move |
| KS-698 | In Progress | #882 | #882 merged; ticket still In Progress — move |
| KS-731 | In Progress | #792, #800, #806 | 09-10: '#806 squash ec2d8c4ca merged' — move |
| KS-796 | In Progress | #815, #816, #819, #820, #822 | #815/#816/#819/#820/#822 all merged; newest is a migration-046 observation — verify no remaining door-3 item, move |
| KS-801 | In Progress | #817 | #817 merged 09-05 — move (its 09-05 note is about #812's revert depending on it, which is now merged) |
| KS-802 | In Progress | #818 | #818 merged; unarchived 09-08 by Kam's ruling — verify remaining test-quality items, move |
| KS-806 | In Progress | #819 | #819 merged; 0 comments — move |
| KS-937 | In Progress | #876 | 0 comments; #876 merged — verify whether the awk case-sensitivity residue landed in #876/#879 (check-shared-relink.sh), then move or re-open as (a) |
| KS-949 | In Progress | #885 | #885 merged; newest is an observation of the 42P10 class (fixed by #973/KS-962 tonight) — verify, move |
| KS-962 | In Progress | #973 | 09-13 11:31: '#973 squash-merged onto develop as 818002259 (M16) VERIFIED' — move to Done |
| KS-1098 | In Progress | #961 | 09-12: '#961 squash-merged as 21c74dd2a' — move |
| KS-930 | In Progress | #876, #886 | #876 (round 3) + #886 merged; #879 attached — verify residues closed, move |
| KS-969 | In Progress | #892 | #892 merged; residues live in KS-973 (L10) — move |

Which completed state applies (Tested Not Deployed / Deployed to UAT / Done) is Kam's call, as in the census; tonight's 9 moves went to Done.

## Not lanes — class f (21): a human by the ticket's own words

| Ticket | State | Prio | Whose | Quote |
|---|---|---|---|---|
| KS-485 | Todo | High | Kam | tracker (Peter's review-stream parent, CLAUDE.md). Newest 09-12: 'No action needed.' |
| KS-491 | Todo | High | Kam | Review F tracker. Newest 09-02: 'the Caddyfile row is FALSE, and this ticket contradicts itself about it' — needs Kam to re-scope the review |
| KS-683 | Todo | High | Kam/Stuart | 08-21: 'Layer 1 is closed on the evidence below. What remains is ours (KS-670's quota recovery), yours-but-separate (Layer 3), and still-open (Layer 4)' — disposition needs Kam/Stuart; no fix shape on K |
| KS-696 | Todo | High | Kam/Peter | 08-27: 'The variance is real — but this ticket's headline figure was partly an artifact of KS-700' — Akto verdict-engine variance; needs a ruling (accept/ratchet), no code shape |
| KS-735 | Todo | High | Peter | 09-02: 'BOUNCE, no state change. The remaining actor is @PeterObeden, named by this ticket's own text: the flat-vs-nested contract question' |
| KS-770 | Todo | High | Peter (stream) | review-stream tracker (API contract + four suites). Newest 09-05: 'RECORD ONLY — Kam's ruling on the #800 status question. No new ask' |
| KS-772 | Todo | High | Stuart (stream) | review-stream tracker (S↔K). Newest 09-12: 'No action needed' |
| KS-582 | Todo | Medium | Kam | label Decision: '[Decision] Approval shape for bulk re-key — two approvers for a batch, one for a single-org rotation' — Kam |
| KS-256 | In Progress | High | Kam | 09-02: 'RULED — Kam's action, not ours' (card secuura-ks304-ks256-bounces) |
| KS-665 | In Progress | High | Peter | 08-21: '@PeterD — this is a proposal, not a change. Implementation stays deferred' — fixture design awaiting Peter's agreement |
| KS-729 | In Progress | High | Peter | 09-08: 'Explicitly NOT Done — @peter asked for that in writing: KS-729 stays open on leg 2' |
| KS-771 | In Progress | High | Peter | 09-06: 'Test block for Peter — six changes, one review, one pass' — awaiting Peter's pass |
| KS-775 | In Progress | High | Peter | [Decision] express 4→5; 09-04: 'back with him' (Peter) |
| KS-966 | In Progress | High | Kam | unassigned; Peter 09-11 measured a consequence and recorded a rule in systemTest/CLAUDE.md — needs Kam's 'rotate-properly' close call |
| KS-174 | In Progress | Medium | Kam | 09-08: 'Unarchived on Kam's ruling' — 2026-06 ticket, #191 closed unmerged; no current branch or fix shape; needs Kam's re-scope |
| KS-441 | Blocked | Urgent | Kam/Stuart | 09-10: 'Reassigned to @stuart.jamieson as a budget item — Kam's call… it is a spend decision' |
| KS-762 | Blocked | High | Kam | 09-06: 'I did not make this change, and I think that is correct — all three conditions are @kam's' |
| KS-869 | Blocked | High | Kam | 09-08: 'It is waiting on Kam, and that should be visible on the board'; rides on #880 (L5) |
| KS-229 | In Review | High | Kam | tracker; 'State unchanged (In Review): KS-229 is the 2026-06-10 platform assurance tracker' — Kam rules its column |
| KS-663 | In Review | High | Peter | #808 merged; 'Peter (2026-09-08) asked to keep KS-663 open because its third criterion' (CI enforcement of the spec contract — .github/workflows, Kam-class) |
| KS-946 | In Review | Medium | Kam | #884 is KS-858's PR; 'Left open for a second read of the re-price, since it is a security call' — Kam |

## Not lanes — class g (5): blocked on something measured

- **KS-576** Todo High: ticket: 'It must not ship before KS-577 (revoke-on-rotate)' — KS-577 = #880 open (L5). Stuart re-filed the S half as PS-740
- **KS-583** Todo Medium: 'would pass today while leaving the compromised credential live' — needs KS-577/#880 (L5) merged first; DR rehearsal = run + report after
- **KS-843** In Progress Medium: 09-08: 'rotating Platform S's connector keys stops being safe by default the moment KS-577/#880 merges, and needs an explicit setting' — waits on L5's #880 shape
- **KS-365** Blocked High: 09-08: 'waiting on Docker Hub… a Docker Hub rebuild of the postgres image carrying the CVE-2025-68121 fix' (upstream; not re-probed tonight)
- **KS-763** In Review High: no open PR; 09-03: 'Item 1 of the corrected done-means is on #797; the ticket stays In Review'; remaining done-means = express 5 fix shape → KS-775 [Decision] 'back with him' (Peter)

## Not lanes — class e (11): theirs

- **KS-188** Todo High · stuart.jamieson: assignee stuart.jamieson; Peter's 08-05 measurement 'transitions: 0 of 318' — spec-source operationId/links work on the S↔K stream
- **KS-412** Todo High · peter: assignee peter; branch-protection 'Required' settings = org-admin, not a builder
- **KS-61** Todo High · stuart.jamieson: assignee stuart.jamieson; 'reminder ticket, best addressed per-API as each is touched'
- **KS-135** Todo Medium · stuart.jamieson: assignee stuart.jamieson; Platform S refactor
- **KS-492** Todo Medium · peter: assignee peter; Review G tracker
- **KS-502** Todo Medium · peter: assignee peter; 'skipped security regressions needing a proper harness'
- **KS-533** Todo Medium · peter: assignee peter; S↔K security register
- **KS-575** In Progress High · peter: assignee peter; #654 merged
- **KS-1096** In Progress Medium · peter: PeterObeden's draft #959 (Start_Up/start-secuura.sh, check-stack-safety.sh, CONTRIBUTING.md)
- **KS-573** In Progress Medium · peter: assignee peter; #817/#599 merged
- **KS-418** Blocked Medium · peter: assignee peter; #891 merged; Peter 09-09 reviewed the nightly wording

## Arithmetic toward ≤ 60
108 now − 14 (h, ticket moves) = 94 · − 52 (a/b/c in lanes L1–L19, if every lane closes) = 42 · the 5 deferred a's, 11 e, 21 f, 5 g = 42 remain. So ≤ 60 needs the 14 h moves plus **≥ 34 lane closures**; ranks 1–9 alone carry 36 tickets (b/c items are the fast ones: 17 gates + 19 fix rounds sit on branches that already exist).

## Not measured (see method.md)
- `mergeable_state` reads `unknown` on 26 of the 31 kksecura PRs (GitHub had not computed it); only #720 (`dirty`), #881 (`blocked`), #799 (`unstable`) discriminate. Rebase need vs 8861e6216 was NOT computed per PR — every lane re-reads its head and rebases first.
- Whether the older-head verdicts (#924/#925/#927) survive a re-gate; whether #931 conflicts with #965 beyond the builder's own note.
- Seat liveness on any worktree (mtimes only; `git worktree list` is a write-adjacent verb I did not run).
- KS-365's Docker Hub condition, KS-441's budget, KS-661's platform-s half — not re-probed.
- Peter's third item on #922 and the full text of his #912 systemTest list — read on the PR before briefing (first 900 chars quoted in lanes.json).
