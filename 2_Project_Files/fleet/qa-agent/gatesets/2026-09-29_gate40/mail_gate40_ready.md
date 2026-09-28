# CAPTURE for gate40 (QA/Secuura-batch1338) — 2026-09-28T22:56:05Z

Seat B 42nd's READY FOR QA MAIL for #1338 (its id found by ONE read-only API listing filtered by the commissioned subject prefix, then read BY ID from
wednesday-agent@) is captured VERBATIM below with its TEXT_SHA256, beside the PR's BODY, its COMMIT MESSAGE (over its develop merge-base) and its push log's STOP counts.

## #1338 KS-1370 (Seat B 42nd (ITEM 1, seat-written, per Kam's rulings (a) on secuura-ks1370-revoke-undone-by-stale-process and (a) on secuura-ks1370-validate-when-the-revoke-check-cannot-read: half (i) validate's usage write is a usage-only UPDATE (dbRecordApiKeyUsage); half (ii) on a cache HIT validate re-reads the stored row through security_find_api_key_by_hash and decides on it — revoke sticky both ways, a vanished row answers Key not found and is evicted, a failed read with a database configured answers 503 'Unable to verify key', memory-only mode answers from memory; #1334's KS 888 validate cells re-pinned), T1) — head 42f8a5abc65ef9a6bc20c07797786089f2b9cd93

#1338 ticket line: #1338 is KS-1370.

### READY FOR QA MAIL <010001a0ea2cf58b-e6a9f8a3-6338-4012-ba2e-d00cdce350e4-000000@email.amazonses.com> (wednesday-agent@, inbox_digest.sh full, by id) TEXT_SHA256 56af8ae2405d767d51244d5eb404c4473cbc4f9e5470eaa2e7f7ce039250ac36

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-28T22:40:10.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 42nd): #1338 KS-1370 both halves at 42f8a5abc65e - all five artefacts; 275/275, 16/16 arms, 5/9 red-first; RLS NOT exercised, gate must use a non-superuser role
---
# READY FOR QA (Seat B 42nd): ITEM 1, PR #1338, KS-1370 both halves. All five artefacts exist and are
# named below. HOLDING for gate40. Nothing merged, nothing deployed. ITEMS 2-3 UNRAISED, handed over.
# From Seat B 42nd.

## THE FIVE ARTEFACTS
1. **PULL REQUEST: #1338** — https://github.com/Secuura/Distributed_Secuura/pull/1338
   base `develop`, state open, not a draft.
2. **HEAD SHA, read from origin in the same action as writing this sentence:**
   `ls-remote` -> `42f8a5abc65ef9a6bc20c07797786089f2b9cd93`
   GitHub's PR head -> `42f8a5abc65ef9a6bc20c07797786089f2b9cd93|open|unstable|develop` (sha|state|mergeable_state|base)
   The two agree. Branch `feature/ks-1370-validate-reads-stored-revoke-b42-1`.
3. **TICKET: KS-1370**, facts-only comment posted naming PR #1338:
   https://linear.app/secuura/issue/KS-1370/security-validate-reads-api-keys-from-a-boot-only-memory-map-so-a#comment-67d8e19f
   ⚠ **The ticket moved Backlog -> In Progress on its own** when the branch reached origin (Linear's
   branch-name integration). I did not move it; recording it because the GO decides ticket state.
4. **TEST EVIDENCE block is in the PR body, written by me, who ran every line of it.** Ratios below.
5. **NOT COVERED is in the PR body AND repeated below**, not a bare green tick.

## EVIDENCE, AS RATIOS
  services/security whole suite   26 files / **275 tests, 0 failed**
  KS 888 validate file            **19/19**; baseline **19/19** at the base tip
                                  5 declarations = **7 executed cases** moved and re-pinned
  new ks1370 cells                **9/9 green**, and **5/9 RED** at the base tip (W1 V1 V2 D1 F1)
  KS 764 revoke call-site guard   **15/15**, green and untouched (revoke was not modified)
  tsc -p services/security        rc 0
  eslint on both touched files    rc 0
  real-PostgreSQL arms            **16/16**, product file restored byte-identical (sha256 equal)
  push preflight                  **12/15 legs ran, 3 SKIPPED, nothing failed** — 12/15 is not a pass.
                                  The log gives the ratio and does NOT name which three skipped.
                                  Shell suites 60/60, 0 skipped; 13 code guards passed. push rc=0.

## RED BEFORE GREEN, DRIVEN
At `0de10857` (index.ts sha256 `7f29bb85765e7985`): stale instance -> `valid: true`; row after its
usage write -> `is_active` false -> **TRUE**, usage 1 -> 2. With the fix: `valid: false Key revoked`,
row stays false, usage 1 -> 1. Controls unchanged both times (never-revoked validates; a third instance
booted after the revoke refuses and the row stays false).
**The arms exist because my FIRST green was vacuous:** half (ii) returns before the usage write, so
`is_active` staying false proved only that nothing wrote. W4 is the discriminator — with half (i)
removed and half (ii) neutralised, the revoke IS revived. Each half is load-bearing on its own.

## FOR THE GATE, CARRIED AS YOU INSTRUCTED
- 🔴 **RLS IS NOT EXERCISED.** The drill runs as `postgres` (`rolsuper=t`, `rolbypassrls=t`), so every
  statement bypasses RLS. `svc_api_keys` really is `relrowsecurity=t, relforcerowsecurity=t` with both
  `tenant_isolation` and `svc_api_keys_auth_lookup` present, but the drill **cannot** discriminate
  whether a direct SELECT returns zero rows — which is the entire premise for using the SECURITY
  DEFINER carve-out. **Drive the stored read as a NON-SUPERUSER app role.**
- **`usage_count` written from a stale copy is a lost update.** Named as a candidate, not fixed, not filed.
- Two module instances with separate CJS caches were driven, NOT two OS processes.
- The four platform suites were not run: service-internal change, no OpenAPI surface change.
- The fixture: 18 of 50 migrations reported an error and all 18 are the same benign
  `relation "_secuura_migrations" does not exist` (the runner's bookkeeping table, which direct `psql`
  never creates). 039's error count is exactly 1; all DDL applied; fixture-health cell green with a
  negative control.
- **RUNTIME change on validate: §5f live sweep owed.**

## SHARED CHECKOUT AND CONTAINMENT
HEAD and local `develop` still `3bad652d17cf`. `origin/develop` `0de108577e61` after my ONE disclosed
tracking-ref refresh. Total fetches: one. Lock `.push-lock-38` taken and released three times (boot
worktree, local commit, push), every release with the pid the JSON holder file recorded. No
`.push-lock-*` remains. 0 orphaned `login_stub` pids under my worktree after the push.

## STATE
- **Audit fuse: 25.3 h, computed at 2026-09-28T22:40Z.** No mail from Kam; the re-date has not arrived.
- Seat H: `seat h` is in my matcher's OTHER_SEATS with a control both ways. My worktree is on the Data
  volume, outside its scope. Invariant snapshot taken and nothing of mine has changed.
- **ITEM 2 (KS-1371) and ITEM 3 (N-1332-5) are UNRAISED**, untouched, handed over whole. Brief:
  the launch brief of 2026-09-28T21:36:22Z. They go in my handover by item number.

Needed-by: nothing blocking. Holding for gate40 on PR #1338. I will wrap cold with
`5_Project_History/HANDOVER-seatB42-2026-09-29.md` at my budget line; the GO may go to a successor.



### PR BODY (gh_body_1338.md) TEXT_SHA256 4a6f93616f55f743c10020582e6da56427d783a8acbbc923ab305bbad43fa618

#1338 KS-1370: validate answers on the stored revoke, and its usage write cannot revive one
head 42f8a5abc65ef9a6bc20c07797786089f2b9cd93

A revoked API key kept working, and using it un-revoked the key on disk.

`POST /api/keys/validate` resolved the key from `memApiKeys`, a map populated only at boot, so a revoke
performed in another process was invisible. Worse, validate's usage write went through the shared
`dbSaveApiKey` upsert, whose `is_active = EXCLUDED.is_active` then wrote the cached `true` back over the
persisted revoke — so merely *using* a revoked key restored it.

Driven on a real PostgreSQL 18.3 before the change: a stale instance answered `valid: true`, and after
its usage write the row read `is_active` false -> **TRUE** with `usage_count` 1 -> 2.

## Kam's rulings, quoted

`secuura-ks1370-revoke-undone-by-stale-process` = **(a)**, ruled 2026-09-29T07:11:50+10:00:

> **Fix both halves** — The usage write stops touching is_active (it records usage only), AND validate
> checks the stored revoke before answering valid, so a stale memory copy can neither honour nor
> restore a revoked key. A Secuura seat builds it with red-first cells for both halves, through the QA
> gate, no deploy. It re-pins #1334's validate cells, which bind the current upsert shape. It does not
> change your 20:22 ruling that a failed usage write is logged, never refused.

`secuura-ks1370-validate-when-the-revoke-check-cannot-read` = **(a)**, ruled 2026-09-29T08:05:30+10:00:

> Split: refuse on a failed read, memory-only mode answers from memory. A failed stored read with a
> database configured returns 503 'Unable to verify key'. ... A revoked key is never honoured.
> Memory-only deployments behave as today. The usage write stays log-only, as you ruled.

## What changed

**Half (i) — the usage write.** Validate now issues a usage-only
`UPDATE svc_api_keys SET last_used_at, usage_count`. Deleting `is_active` from the shared upsert is
**not** the fix: the revoke route persists its revoke through that same statement, and the KS 764
call-site guard pins exactly that shape, so removing it would stop a revoke of an existing row
persisting at all. Narrowing validate's own call site leaves revoke untouched. An `UPDATE` rather than
an upsert because every caller reaches it with a row that already exists — a usage bump must not
conjure a key.

**Half (ii) — the answer.** On a cache hit validate re-reads the stored row through the reviewed
pre-session carve-out `security_find_api_key_by_hash` (the KS 458 fail-closed carve-out, since this
route is unauthenticated and has no tenant GUC) and decides on that row, refreshing the stale cache
entry so it stops lying for later requests. The read has its own `try` and every exit from it is a
response, never a throw — this handler takes no `next`, so a throw would be an unhandled rejection.

## Two shapes, confirmed rather than assumed

Both follow from Kam's own words rather than new authority, and both were **confirmed as shapes by
Wednesday** (2026-09-28T22:28:36Z) before this was raised.

**1. A revoke is sticky in BOTH directions.** KS 888 (`secuura-ks888-revoke-validate-on-failed-save`,
option a) keeps the in-memory revoke when its save fails, so the key dies in that process while the row
still reads active. Refreshing blindly from the store would have **undone that and re-honoured a
revoked key**. So the two sources combine in the safe direction: revoked if *either* says revoked.
Stored-revoked beats cached-active (this ticket); cached-revoked beats stored-active (KS 888).
**Cell R2 of the KS 888 file is what caught this, and it now passes unchanged — the code was fixed,
not the test.**

**2. A vanished row** reads `Key not found` and the cache entry is evicted: a deleted row is a stronger
revocation than `is_active = false`. **This is a defensive path, not a live one** — grepped first,
nothing in `services/` or `migrations/` issues a `DELETE FROM svc_api_keys` outside migration 019.

## A measured cost, and a bound

`api-gateway middleware/auth.ts` re-read at this tip, not cited:
- `:229`/`:235` — a `!resp.ok` response **is** cached as a refusal for 30_000 ms, so a 503 from
  security refuses that key for up to 30 s past the fault. That is the cost of ruling (a)'s first limb.
- `:220` — a cached result is returned **without** re-validating. So half (ii)'s extra stored read fires
  **at most once per key per 30 s, not once per request.** The extra read is bounded by the gateway's
  own cache.

## Test Evidence

**Touched:** `services/security/src/index.ts`; `services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts` (re-pinned); `services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts` (new). 3 files, +331/-8.

**Ran, on this head `42f8a5abc65ef9a6bc20c07797786089f2b9cd93`:**
- `services/security` whole suite — **26 files / 275 tests, 0 failed**
- KS 888 validate file — **19/19** (baseline **19/19** at the base tip; 7 executed cases failed mid-change, see the re-pin below)
- new KS-1370 cells — **9/9 green**, and **5/9 RED** against the unmodified `index.ts` at the base (W1, V1, V2, D1, F1)
- KS 764 revoke call-site guard (`packages/shared`) — **15/15, green and untouched**, as expected: revoke was not modified
- `tsc -p services/security` — rc 0
- `eslint` on both touched source files — rc 0
- **Real-PostgreSQL drill, 16/16 arms**, product file restored byte-identical (sha256 equal) after every tamper. PostgreSQL 18.3, unix socket only; my postmaster held **0 TCP listeners** (control: the native pg@15 held 2, so the check discriminates). Raw output is in `5_Project_History/2026-09-29_seatB-42nd/ks1370/`.
- Push preflight: **12/15 legs ran, 3 SKIPPED, nothing failed.** 12/15 is not a pass. The log reports the ratio but does not name which three skipped. Shell suites 60 passed / 0 failed / 0 skipped; 13 code guards passed.

**The re-pin, and why the count is both 5 and 7:** N-1334-1's figure of 5 counts `it`/`it.each`
*declarations* (R2, C3, V1, V2, V3); V1 is `it.each(INFRA)` with three cases, so **5 declarations = 7
executed cases**. R2 moved for the sticky-revoke interaction and now passes unchanged. C3, V1 x3 and V2
all failed for one root cause: the mock answered `rows: []` to every SELECT, so the new stored read read
`Key not found`. The mock now keeps a hash-keyed store the INSERT populates, which is *more* faithful —
a failed insert leaves the store active, which is precisely R2's state. V1 and V3 counted
`state.inserts`; validate's write is an `UPDATE` now, so they count `state.usageWrites`. Same claim, new
instrument. The two `state.inserts` counters that watch **mint** are deliberately untouched.
**V2's no-key/no-hash and one-error-line pins are unchanged**, and the usage-only write keeps the
byte-identical `'DB save API key failed'` message so V2 still binds this path. No pin was weakened.

**Only 5 of the 9 new cells are red-first, and I am not claiming 9.** The other four pin preserved
invariants: W2 (usage is still recorded), S1 (the KS 888 sticky revoke), M1/M2 (memory-only mode
unchanged by design, which keeps #1334's control C4).

**NOT run / NOT covered:**
- **RLS is not exercised by the drill, and it is the premise for the SECURITY DEFINER carve-out.** The
  drill runs as `postgres` (`rolsuper=t`, `rolbypassrls=t`), so every statement bypasses RLS.
  `svc_api_keys` genuinely is `relrowsecurity=t, relforcerowsecurity=t` with both `tenant_isolation`
  and `svc_api_keys_auth_lookup` present, but the drill **cannot** discriminate whether a direct SELECT
  would return zero rows. **The gate should drive the stored read as a non-superuser app role.**
- Two OS processes vs two module instances: two **module instances** with separate CJS caches were driven.
- `usage_count` written from a stale copy is a lost update. **Named as a candidate, not fixed, not filed.**
- The four platform suites (Schemathesis, Akto, Playwright, k6) were **not** run: this change is
  service-internal with no OpenAPI surface change.
- Nothing deployed. No migration run against any environment.

**Migrations + config:** none. No migration, no environment variable, no config change. The fixture
applied the existing migrations to a throwaway local database only.

**RUNTIME change on validate: §5f live sweep owed.**

Refs KS-1370


🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN over 0de108577e6199de3c9402c0643a2944d86aee97 (oldest first) TEXT_SHA256 5e7b91c9187ab68fce807d3f6b21ecffe745afb3d9e719b5cc517f01308efb80

--- commit 42f8a5abc65ef9a6bc20c07797786089f2b9cd93
KS-1370: validate answers on the stored revoke, and its usage write cannot revive one

A revoked API key kept working, and using it un-revoked the key on disk.

validate resolved the key from `memApiKeys`, a map populated only at boot, so a
revoke performed in another process was invisible; and validate's usage write
went through the shared `dbSaveApiKey` upsert, whose `is_active =
EXCLUDED.is_active` then wrote the cached `true` back over the persisted revoke.
Driven on a real PostgreSQL 18.3 before the change: a stale instance answered
valid:true and the row went is_active false -> TRUE, usage_count 1 -> 2.

Half (i), the usage write. Validate now uses a usage-only
`UPDATE svc_api_keys SET last_used_at, usage_count`. Deleting is_active from the
shared upsert is NOT the fix: the revoke route persists its revoke through that
same upsert, and the KS 764 call-site guard pins exactly that shape, so
narrowing validate's own call site is the change that leaves revoke intact.

Half (ii), the answer. On a cache hit validate re-reads the stored row through
the reviewed pre-session carve-out `security_find_api_key_by_hash` (KS 458) and
decides on that row, refreshing the stale cache entry so it stops lying. A
vanished row is treated as not found and evicted.

A revoke is sticky in BOTH directions. Stored-revoked beats cached-active, which
is this ticket; cached-revoked beats stored-active, which preserves KS 888's
rule that a revoke whose save failed still blocks the key in this process.
Without that, refreshing from the store would have re-honoured a revoked key.

A failed stored read returns 503 'Unable to verify key'; memory-only mode
(no database configured) answers from memory, so those deployments are
unchanged. The usage write stays log-only, never refused.

Re-pins the KS 888 validate cells in the same commit, with the reason in the
mock: the stored read and the usage-only statement change what they measure, so
the mock now keeps a hash-keyed store and counts usage writes separately. Every
assertion is unchanged in substance; the no-key/no-hash and one-error-line pins
are untouched.

Refs KS-1370



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-42nd/raise/s-b42-ks1370-42f8a5abc65e-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-42nd/raise/s-b42-ks1370-42f8a5abc65e-push.out",
 "lines": 1344,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-28T22:29:36Z PUSH START",
 "end": "2026-09-28T22:35:16Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB42-2026-09-29.md TEXT_SHA256 c3718ebb343543776ab82e772ae0b749d49942212b5e9e71a91996025ff8f1cb

# HANDOVER — Seat B 42nd, Secuura/Blockchain, round 38

**Pane** `Secuura/Blockchain` (unsuffixed, tmux `fleet:main.1`). **Token** `b42`. **Tools** `*38`.
**Lock** `.push-lock-38`. **Gate** gate40. **Window** 2026-09-28 21:36Z → 22:4xZ.
**Record folder** `5_Project_History/2026-09-29_seatB-42nd/`.
**Brief** Wednesday, `2026-09-28T21:36:22Z`, `[Wednesday -> Secuura/Blockchain] LAUNCH BRIEF (Seat B 42nd): KS-1370 both halves + KS-1371 raise`.

## STATE AT HANDOVER — this is final
- **ITEM 1 (KS-1370) is RAISED: PR #1338**, head `42f8a5abc65ef9a6bc20c07797786089f2b9cd93`, branch
  `feature/ks-1370-validate-reads-stored-revoke-b42-1`, base `develop`, open, not a draft.
  **NOT merged. Holding for gate40.** READY FOR QA mailed with all five artefacts.
  ⚠ `mergeable_state` reads **`unstable`**, not `clean`. With Actions retired that carries no testing
  claim either way — the Test Evidence block does. Do not read it as a verdict.
- **ITEM 2 (KS-1371) is UNRAISED.** Untouched. The held Spark READY is at
  `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1371_spark-dsv4flash_BRIEFED-UNREVOKE-REFUSES-NEGATIVE-INDEX-PASS-7of7_2026-09-29.diff.md`,
  canonical patch at `…/local-model/runs/spark_secuura_2026-09-29_KS-1371-b/out.md.checker/patch.diff`
  (2,012 B, sha256 prefix `0238cdd9b9d224c9`). Both vc-issuer files' blobs are identical at `215cc687`
  and `0de10857`, so a strict `git apply --check` is PREDICTED to pass — **still unmeasured, run it.**
- **ITEM 3 (N-1332-5) is UNRAISED.** Untouched. `deploy-all.sh:281` and `deploy.sh:823` must read
  `/health`'s `startupMigrations` and fail the deploy step on `failed > 0`. Key on `failed`, NOT `error`
  (gate39's N-G39-2: a CORE statement failure is served `failed: 3` with no `error`). `Refs KS-1054`.
- **Nothing deployed.** No migration run against any environment. No `az`.
- **Audit fuse `2026-09-30T00:00Z`: 25.3 h at handover** (computed 22:40Z). **No mail from Kam** — the
  re-date has not arrived. It needs HIS OWN DKIM mail to `secuura-blockchain@agentmail.to`; a relay is
  not his mail. If it lands, STOP and mail Wednesday first.
- **Shared checkout never written beyond the one allowed refresh.** HEAD and local `develop`
  `3bad652d17cf`; `origin/develop` `215cc6875e2b` → `0de108577e61`, one fetch, reflog fast-forward.
  Tree at `0de10857` = `b5362672fb7f4d06aaa15a0c9c1f4d9c658040f8`, byte-equal to gate39's END.
  Lock taken/released three times, every release with the pid the JSON holder file recorded. No
  `.push-lock-*` remains. 0 orphaned `login_stub` pids under my worktree after the push.
- **Worktree on the DATA volume:** `<B 42nd's scratchpad>/wt/s-b42-ks1370`, detached base `0de10857`,
  then branched. DevMASTER is still 100% full at ~1.5 GiB free — Kam ruled deletion of stale worktree
  `node_modules`, and **Seat H does that, not you.**

## ITEM 1 IN ONE PARAGRAPH
A revoked API key kept working, and using it un-revoked the key on disk. validate resolved the key from
`memApiKeys` (boot-only), so another process's revoke was invisible; and its usage write went through
the shared `dbSaveApiKey` upsert, whose `is_active = EXCLUDED.is_active` wrote the cached `true` back
over the persisted revoke. Fixed both halves: a usage-only `UPDATE` for validate's call site (the shared
upsert keeps `is_active` because revoke persists through it and the KS 764 guard pins that shape), and a
stored-state re-read through `security_find_api_key_by_hash` on a cache hit. Failed read → 503;
memory-only mode → answers from memory. Both per Kam's two cards, option (a) each.

## FOUR THINGS TO CARRY, ONE LINE EACH
1. **A GREEN CAN BE VACUOUS BECAUSE OF THE OTHER HALF.** With both halves in, half (ii) answers
   `Key revoked` and RETURNS BEFORE the usage write, so `is_active` staying false proved only that
   nothing wrote — half (i) was untested and my green read as if it had been. If a fix has two parts,
   neutralise one to test the other. 16 arms exist because of this.
2. **A CONTROL THAT RETURNS THE SAME NUMBER AS ITS SUBJECT IS NOT A CONTROL.** `lsof -p PID -iTCP`
   without `-a` ORs the filters: subject and control both read 42, the machine-wide total. And
   `lsof -c postgres` is a NAME match that reported the native pg@15's sockets as mine. Scope by pid
   from your own `postmaster.pid`, AND with `-a`, and check the control DIFFERS.
3. **AN EDIT SCRIPT THAT WRITES ONCE AT THE END DISCARDS EVERYTHING ON AN ABORT, SILENTLY.** Mine
   printed "anchor unique: the db mock" and then `sys.exit`ed on a later non-unique anchor, so the mock
   re-pin was never written — and I read the next run's failures as "mock applied, V1 aborted". Either
   write per-edit, or treat "it printed OK" as no evidence that anything landed. For an anchor with
   several occurrences, key the edit to a LINE NUMBER plus a content assertion.
4. **A HEX COINCIDENCE CUTS BOTH WAYS, AND BOTH BIT ME.** `b41` is three chars of hex: a bare key in
   the re-key map would have rewritten `a95543f7-…-9146abd(b41)ba` inside `rekey_check`'s own fixture.
   And `rekey_check38` read MY OWN session uuid `5aacd245-…-8a4ccb(b32)d8` as a live `b32` reference,
   reporting 2 false DEFECT-LIVE. Guard both: map the whole uuid to itself in the re-key, and treat a
   token buried in a digit-bearing hex run as not-a-token in the checker. **Your own token is `b43`;
   check your uuid and every SHA in the tools for it before you run the pass.**

## THE `*38` TOOL GENERATION — 21 tools, at `2026-09-29_seatB-42nd/raise/`
Pass run ONCE at `21:55:28Z`: **20 files, 200 LIVE lines rewritten, 22 prose lines preserved.**
`rekey37.py` and B 41st's six `merge37-133*` records quarantined FIRST in `_b41_artefacts_NOT_MINE/`,
sha256 proved equal against the ORIGINALS. `_pre_rekey_snapshot/` holds the 20 inherited files.
- **BANNERCHECK38** 17 checked / 0 stale, A=PASS B=PASS.
- **NAMECHECK38** 7 checks / 0 bad, **20/20 controls fired**, 3 positives OK, P3-INVERSE OK.
- **REKEY_CHECK38** 867 hits / **0 DEFECT-LIVE**; CONTROL A **956 hits / 382 DEFECT-LIVE** on B 41st's
  originals — unchanged before and after my hex guard, which is the proof the guard is narrow.
- **TRAP 4, SEVENTH GENERATION, proved on REAL mail:** without `b 41st` in OTHER_SEATS, B 41st's real
  GO (`merge 1337 1332 on gate39`) classifies **FOR ME** and seven of its mails flip. Proof at
  `raise/trap4-seventh-generation-proof.txt` with the tampered copy beside it.
- **`b4` is in FOREIGN but deliberately in only TWO of the four FOREIGN_FORMS lists.** `FOREIGN` uses
  exact segments (`re.split(r"[-/]"`), so `b4` is safe; `FOREIGN_FORMS` uses `tok in r` (SUBSTRING),
  where `-b4` matches my own `-b42-1` and `seatb4` matches `refs/seatb42/…`. One token, two matchers,
  two different correct answers. **`b4` is a prefix of `b42` and will be a prefix of `b43` too.**
- **B 41st's census claim corrected:** `RAISE36_`/`GATE36_`/`KEYSCAN36`/`BANNERCHECK36` were counted as
  "present" but exist ONLY inside re-key maps and TOKENS lists, never as live identifiers. A census that
  counts a map's own keys as evidence cannot fail. Those four are omitted from my map with the reason.
- **All 20 authorship headers were stale**, and `push38_ff.sh`'s was TWO generations stale (it named
  Seat B 40th). Rewritten by hand, predecessor lines retained as history, flagged in the file.
- **Two control OUTPUT lines named the wrong predecessor** while scanning the right one (the rule gap
  B 41st recorded). Corrected; the `e.g.` rows now show `*37` files under a label that says `*37`.

## ITEM 1 EVIDENCE, AS RATIOS
`services/security` **26 files / 275 tests, 0 failed** · KS 888 validate file **19/19** (baseline 19/19;
**5 declarations = 7 executed cases** moved) · 9 new cells **9/9 green, 5/9 RED** at the base tip ·
KS 764 guard **15/15 untouched** · `tsc` rc 0 · `eslint` rc 0 · **16/16 arms**, product file restored
byte-identical · push preflight **12/15 legs, 3 SKIPPED, nothing failed** (the log does not name which
three) · shell suites 60/60 · 13 code guards passed · `push rc=0`.

## NOT COVERED, STATED
- 🔴 **RLS IS NOT EXERCISED BY THE DRILL** and it is the premise for the SECURITY DEFINER carve-out: it
  runs as `postgres` (`rolsuper=t`, `rolbypassrls=t`). The table IS `relrowsecurity=t,
  relforcerowsecurity=t` with `tenant_isolation` and `svc_api_keys_auth_lookup` present, but the drill
  cannot discriminate whether a direct SELECT returns zero rows. **Needs a non-superuser app role.**
- `usage_count` written from a stale copy is a lost update — candidate, not fixed, not filed.
- Two module instances with separate CJS caches, NOT two OS processes.
- The four platform suites were not run: service-internal, no OpenAPI surface change.
- **§5f live sweeps owed:** KS-1370 (this round) plus KS-888, KS-1054 (B 41st) and KS-1352, KS-1124
  (B 40th). KS-1370 moved Backlog → In Progress on its own when the branch reached origin.
- **B 41st's trap 10 does NOT reproduce here:** `tsx/dist/cjs/index.cjs` exists in tsx 4.23.1 on this
  tree. `node --require tsx/cjs` works and is what I used.
- `@secuura/shared` must be BUILT (`npm run build -w @secuura/shared`) before any drill, or every
  require fails with `dist/index.js` missing — and BOTH the drill and its control fail identically,
  which is the tell that it is a fixture fault and not "does not reproduce".

## REFUSED AND DISCLOSED
The launcher's boot pull/fetch on the shared checkout · the SessionStart hook's `POST /api/seen`
(`EXTRANET_ME=kam`, it clears **Kam's** flags) · the boot prompt's "CC Kam on every email" · its rule-7
extranet to-do. **Preflight was NOT clean:** `[F-02] No SSH identity available for git` — it did not
bite, the repo-local `core.sshCommand` carried the push. It is MINE, not another seat's: the file's
`# launch 2026-09-28T21:36:28Z` equals my own session start to the second.

## STILL KAM'S
The **audit fuse** (25.3 h at handover, needs his own DKIM mail) and the **full DevMASTER volume**
(Seat H is clearing stale worktree `node_modules` on his ruling; touch no other seat's tree).
KS-1375 / KS-1368 are ruled **(b) fail closed** and belong to a SUCCESSOR, not this seat.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-42nd/ks1370/RED-at-0de10857.txt TEXT_SHA256 b6ae3b5090ab8c111f40fc8d259c43120581eaecc5111f5381ea8d3cfef1f063

KS-1370 RED at develop 0de108577e6199de3c9402c0643a2944d86aee97, UNMODIFIED product code
Seat B 42nd, 2026-09-28T22:14:59Z. PostgreSQL 18.3, unix socket /tmp/b42s only (0 TCP on my
postmaster, control: native pg@15 pid 1278 = 2). Two module instances, separate memApiKeys.
index.ts sha256 prefix 7f29bb85765e7985 (the brief's value).

=== CONTROL 0 (fixture health): can node reach the DB through db.ts's own pool? ===
  isDbAvailable: true
  svc_api_keys rows: 1
  fn_039 present: 1
control 0 rc=0

=== THE RED DRILL at 0de10857 (unmodified product code) ===
KEY_HASH b82ff11cad971b7d
seeded: is_active = true
B db available: true
B memApiKeys.size: 1
B booted: key in B.memApiKeys = true | B cached isActive = true
CONTROL 1 (never revoked) -> {"valid":true,"organizationId":null,"tenantId":"44444444-4444-4444-4444-444444444444","scopes":[],"rateLimit":1000,"rateLimitWindow":3600,"connectorId":null}
A revoked: DB is_active = false
ANSWER 1 - B validates AFTER the revoke -> {"valid":true,"organizationId":null,"tenantId":"44444444-4444-4444-4444-444444444444","scopes":[],"rateLimit":1000,"rateLimitWindow":3600,"connectorId":null}
ANSWER 2 - DB is_active after B's usage write = true | usage_count 1 -> 2
C memApiKeys.size: 1
CONTROL 2 - C booted after the revoke: C cached isActive = false
CONTROL 2 (fresh boot) -> {"valid":false,"reason":"Key revoked"}
CONTROL 2 - DB is_active after C = false


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-42nd/ks1370/GREEN-with-fix.txt TEXT_SHA256 60a16acbfaa120b361f1536f82080138955ce9b20f2f92a55097684e16e379fe

=== CONTROL 0 (fixture health): can node reach the DB through db.ts's own pool? ===
  isDbAvailable: true
  svc_api_keys rows: 2
  fn_039 present: 1
control 0 rc=0

=== THE RED DRILL at 0de10857 (unmodified product code) ===
KEY_HASH b82ff11cad971b7d
seeded: is_active = true
B db available: true
B memApiKeys.size: 2
B booted: key in B.memApiKeys = true | B cached isActive = true
CONTROL 1 (never revoked) -> {"valid":true,"organizationId":null,"tenantId":"44444444-4444-4444-4444-444444444444","scopes":[],"rateLimit":1000,"rateLimitWindow":3600,"connectorId":null}
A revoked: DB is_active = false
ANSWER 1 - B validates AFTER the revoke -> {"valid":false,"reason":"Key revoked"}
ANSWER 2 - DB is_active after B's usage write = false | usage_count 1 -> 1
C memApiKeys.size: 2
CONTROL 2 - C booted after the revoke: C cached isActive = false
CONTROL 2 (fresh boot) -> {"valid":false,"reason":"Key revoked"}
CONTROL 2 - DB is_active after C = false


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-42nd/ks1370/ARMS-16-of-16.txt TEXT_SHA256 a19f51b7d0b77dabe1c0471cddc2d2aeb580466dcb5f2fa8167500b05f7d4026

index.ts sha256 BEFORE arms: e85bab09b73bbdcb
=== ARM W — HALF (i): the usage write must not carry is_active ===
    (half (ii) neutralised in a COPY so validate reaches the usage write at all)
    half (i) PRESENT, half (ii) off: answer={"valid":true,"organizationId":null,"tenantId":"66666666-6666-6666-6666-666666666666","scopes":[],"rateLimit":1000,"rateLimitWindow":3600,"connectorId":null} row {"is_active":false,"usage_count":"1"} -> {"is_active":false,"usage_count":"2"}
  PASS  W1  a stale instance DOES reach the usage write (the arm is not vacuous)
        got=true  expect=true
  PASS  W2  and the usage write leaves the persisted revoke ALONE
        got=false  expect=false
  PASS  W3  while still RECORDING usage (the write is usage-only, not a no-op)
        got=true  expect=true
    half (i) REMOVED, half (ii) off: answer={"valid":true,"organizationId":null,"tenantId":"66666666-6666-6666-6666-666666666666","scopes":[],"rateLimit":1000,"rateLimitWindow":3600,"connectorId":null} row {"is_active":false,"usage_count":"1"} -> {"is_active":true,"usage_count":"2"}
  PASS  W4  TAMPER: validate writing through dbSaveApiKey REVIVES the revoke (so half (i) is load-bearing)
        got=true  expect=true
=== ARM V — HALF (ii): validate must answer on the STORED revoke ===
    BOTH halves present: answer={"valid":false,"reason":"Key revoked"} row {"is_active":false,"usage_count":"1"} -> {"is_active":false,"usage_count":"1"}
  PASS  V1  a stale instance answers valid:false Key revoked
        got=[false,"Key revoked"]  expect=[false,"Key revoked"]
  PASS  V2  and the row is still revoked afterwards
        got=false  expect=false
  PASS  V3  TAMPER (half ii off, W1 above) answered valid:true — so half (ii) is load-bearing
        got=true  expect=true
=== ARM C — the stale cache stops lying after one validate ===
  PASS  C1  the cache held isActive=true before the validate
        got=true  expect=true
  PASS  C2  and the validate REFRESHED it to the stored value
        got=false  expect=false
=== ARM D — a deleted row is a stronger revoke than is_active=false ===
  PASS  D1  a stale copy of a DELETED key answers valid:false Key not found
        got=[false,"Key not found"]  expect=[false,"Key not found"]
  PASS  D2  and the cache entry is evicted
        got=true  expect=true
=== ARM E — memory-only mode (no DATABASE_URL) answers from memory, NOT 503 ===
  PASS  E0  isDbAvailable() is false in this mode
        got=false  expect=false
  PASS  E1  an ACTIVE memory-only key validates (no 503)
        got=[200,true]  expect=[200,true]
  PASS  E2  a memory-only key revoked IN MEMORY is refused
        got=[200,false,"Key revoked"]  expect=[200,false,"Key revoked"]
=== ARM F — a failed stored read returns 503 Unable to verify key ===
  PASS  F1  a stored-state read that THROWS answers 503, not valid:true
        got=[503,"SERVICE_UNAVAILABLE","Unable to verify key"]  expect=[503,"SERVICE_UNAVAILABLE","Unable to verify key"]
  PASS  F2  and it did NOT answer valid
        got=true  expect=true

ARMS: 16/16 passed
product file restored byte-identical: true
index.ts sha256 AFTER  arms: e85bab09b73bbdcb
RESTORE PROVED: byte-identical (sha256 equal)


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/5aacd245-a1d2-48d4-a516-8a4ccbbb32d8/scratchpad/drill/ks1370drill.cjs TEXT_SHA256 308ece75f22e6a760101c96fafab676910052445b8de129f71da1ec403182c22

/* Seat B 42nd — KS-1370 driven repro. MEASUREMENT ONLY. No product change.
 *
 * The claim (B 40th's source-path reading): validate resolves the key from an in-memory map
 * populated only at boot (index.ts :1326-:1335), so a revoke performed in ANOTHER process is
 * invisible here; and this process's usage write (:1369 -> dbSaveApiKey -> :316-318
 * `is_active = EXCLUDED.is_active`) then writes the CACHED is_active back over the persisted revoke.
 *
 * TWO INSTANCES, SEPARATE MEMORY MAPS — the shape the brief sanctions. Each `require` of the
 * product module happens with a cleared CJS cache, so each gets its OWN `memApiKeys`.
 * SECURITY_DISABLE_BOOT=1 stops initDb + app.listen (index.ts :1611).
 */
const path = require('path'), crypto = require('crypto'), http = require('http');
const { Client } = require(path.join(process.env.DEV, 'node_modules/pg'));

const PRODUCT = path.join(process.env.DEV, 'services/security/src/index.ts');
const CONN = { host: '/tmp/b42s', user: 'postgres', database: process.env.DRILLDB || 'ks1370' };
const KEY_PLAIN = 'ks1370-drill-key';
const KEY_HASH = crypto.createHash('sha256').update(KEY_PLAIN).digest('hex');
const KEY_ID = '33333333-3333-3333-3333-333333333333';
const TENANT = '44444444-4444-4444-4444-444444444444';

async function sql(q, p) { const c = new Client(CONN); await c.connect(); try { return await c.query(q, p); } finally { await c.end(); } }
async function isActive() { const r = await sql('SELECT is_active FROM svc_api_keys WHERE id=$1', [KEY_ID]); return r.rows[0] ? r.rows[0].is_active : null; }
async function usageCount() { const r = await sql('SELECT usage_count FROM svc_api_keys WHERE id=$1', [KEY_ID]); return r.rows[0] ? r.rows[0].usage_count : null; }

/** A fresh module instance with its OWN memApiKeys. */
function freshInstance(tag) {
  for (const k of Object.keys(require.cache)) {
    if (k.includes('/services/security/src/')) delete require.cache[k];
  }
  const m = require(PRODUCT);
  // SECURITY_DISABLE_BOOT=1 suppresses BOTH app.listen AND initDb (index.ts :1611), and
  // loadFromDb returns early on !isDbAvailable(). So the pool is initialised explicitly here.
  // My first run skipped this, loadFromDb loaded 0 keys, and CONTROL 1 caught it.
  const db = require(path.join(process.env.DEV, 'services/security/src/db.ts'));
  return { tag, app: m.default || m, memApiKeys: m.memApiKeys, loadFromDb: m.loadFromDb,
           initDb: db.initDb, isDbAvailable: db.isDbAvailable };
}

async function serve(app) {
  const s = http.createServer(app);
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  return { port: s.address().port, close: () => new Promise(r => s.close(r)) };
}

async function validate(port, key) {
  const r = await fetch(`http://127.0.0.1:${port}/api/keys/validate`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key }),
  });
  return { status: r.status, body: await r.json() };
}

(async () => {
  console.log('KEY_HASH', KEY_HASH.slice(0, 16));
  // --- seed: one ACTIVE key ---
  await sql('DELETE FROM svc_api_keys WHERE id=$1', [KEY_ID]);
  await sql(`INSERT INTO svc_api_keys (id, tenant_id, name, key_hash, key_prefix, scopes, is_active, usage_count)
             VALUES ($1,$2,'ks1370 drill',$3,'ks1370','{}',true,0)`, [KEY_ID, TENANT, KEY_HASH]);
  console.log('seeded: is_active =', await isActive());

  // --- B boots FIRST, while the key is still active: its cache is warmed with is_active=true ---
  const B = freshInstance('B');
  await B.initDb();
  console.log('B db available:', B.isDbAvailable());
  await B.loadFromDb();
  console.log('B memApiKeys.size:', B.memApiKeys.size);
  const cachedB = B.memApiKeys.get(KEY_ID);
  console.log('B booted: key in B.memApiKeys =', !!cachedB, '| B cached isActive =', cachedB && cachedB.isActive);

  // --- CONTROL 1: a key that was never revoked validates in B (the harness CAN answer valid) ---
  const sB = await serve(B.app);
  const c1 = await validate(sB.port, KEY_PLAIN);
  console.log('CONTROL 1 (never revoked) ->', JSON.stringify(c1.body.data));

  // --- A revokes. Persisted-row equivalent of A's dbSaveApiKey; A is a SEPARATE process/instance
  //     and its route requires an admin identity, so the revoke is applied as the row state that
  //     A's revoke produces. Disclosed as such - it is B that is under test. ---
  await sql('UPDATE svc_api_keys SET is_active=false WHERE id=$1', [KEY_ID]);
  console.log('A revoked: DB is_active =', await isActive());

  const beforeUsage = await usageCount();

  // --- THE MEASUREMENT: B still holds the boot-time cache ---
  const q1 = await validate(sB.port, KEY_PLAIN);
  console.log('ANSWER 1 - B validates AFTER the revoke ->', JSON.stringify(q1.body.data));

  const afterActive = await isActive(), afterUsage = await usageCount();
  console.log('ANSWER 2 - DB is_active after B\'s usage write =', afterActive, '| usage_count', beforeUsage, '->', afterUsage);

  // --- CONTROL 2: a THIRD instance booted AFTER the revoke must refuse it (the DB DOES hold it) ---
  await sql('UPDATE svc_api_keys SET is_active=false WHERE id=$1', [KEY_ID]);   // re-assert before C boots
  const C = freshInstance('C');
  await C.initDb();
  await C.loadFromDb();
  console.log('C memApiKeys.size:', C.memApiKeys.size);
  const cachedC = C.memApiKeys.get(KEY_ID);
  console.log('CONTROL 2 - C booted after the revoke: C cached isActive =', cachedC && cachedC.isActive);
  const sC = await serve(C.app);
  const c2 = await validate(sC.port, KEY_PLAIN);
  console.log('CONTROL 2 (fresh boot) ->', JSON.stringify(c2.body.data));
  console.log('CONTROL 2 - DB is_active after C =', await isActive());

  await sB.close(); await sC.close();
  process.exit(0);
})().catch(e => { console.error('DRILL ERROR', e && e.stack || e); process.exit(1); });


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/5aacd245-a1d2-48d4-a516-8a4ccbbb32d8/scratchpad/drill/ks1370arms.cjs TEXT_SHA256 fada7b6f3ca92e637c12ca32a8fe28710540632d267da61ee95a457cff69d9cf

/* Seat B 42nd — KS-1370 ARMS. One arm per decision, each isolating ONE half.
 *
 * WHY THIS EXISTS, and it is a defect in my own first green proof: with BOTH halves in place,
 * half (ii) answers `Key revoked` and RETURNS BEFORE the usage write. So `is_active` staying false
 * proves only that nothing wrote — it does NOT prove the write is usage-only. Half (i) was
 * unexercised and my green read as if it had been tested. Each arm below drives ONE half with the
 * other neutralised, so each half is shown to be load-bearing on its own.
 */
const path=require('path'), crypto=require('crypto'), http=require('http'), fs=require('fs');
const { Client } = require(path.join(process.env.DEV,'node_modules/pg'));
const PRODUCT = path.join(process.env.DEV,'services/security/src/index.ts');
const CONN={host:'/tmp/b42s',user:'postgres',database:'ks1370'};
const KEY='ks1370-arms-key', HASH=crypto.createHash('sha256').update(KEY).digest('hex');
const ID='55555555-5555-5555-5555-555555555555', TEN='66666666-6666-6666-6666-666666666666';

async function sql(q,p){const c=new Client(CONN);await c.connect();try{return await c.query(q,p)}finally{await c.end()}}
const row=async()=>{const r=await sql('SELECT is_active,usage_count FROM svc_api_keys WHERE id=$1',[ID]);return r.rows[0]||null};
async function seed(active){await sql('DELETE FROM svc_api_keys WHERE id=$1',[ID]);
  await sql(`INSERT INTO svc_api_keys (id,tenant_id,name,key_hash,key_prefix,scopes,is_active,usage_count)
             VALUES ($1,$2,'ks1370 arms',$3,'ks1370','{}',$4,0)`,[ID,TEN,HASH,active]);}
function fresh(){for(const k of Object.keys(require.cache)) if(k.includes('/services/security/src/')) delete require.cache[k];
  const m=require(PRODUCT); const db=require(path.join(process.env.DEV,'services/security/src/db.ts'));
  return {app:m.default||m, memApiKeys:m.memApiKeys, loadFromDb:m.loadFromDb, initDb:db.initDb, isDbAvailable:db.isDbAvailable};}
async function serve(app){const s=http.createServer(app);await new Promise(r=>s.listen(0,'127.0.0.1',r));return {port:s.address().port,close:()=>new Promise(r=>s.close(r))}}
async function val(port){const r=await fetch(`http://127.0.0.1:${port}/api/keys/validate`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:KEY})});
  let b=null; try{b=await r.json()}catch(e){}; return {status:r.status, data:b&&b.data, err:b&&b.error}}

const R=[];
function rec(id,what,got,expect){const ok=JSON.stringify(got)===JSON.stringify(expect);
  R.push({id,ok}); console.log(`  ${ok?'PASS':'FAIL'}  ${id}  ${what}\n        got=${JSON.stringify(got)}  expect=${JSON.stringify(expect)}`);}

(async()=>{
const SRC=fs.readFileSync(PRODUCT,'utf8');

// ---------- W: HALF (i) ISOLATED. Half (ii) neutralised so validate REACHES the usage write. ----------
// Neutralise half (ii) by making its guard false (isDbAvailable() -> a literal false in THAT branch
// only). That is a tamper on MY OWN new line, applied to a COPY, never to the product file.
const noII = SRC.replace('if (apiKey && isDbAvailable()) {','if (apiKey && false) {');
if (noII === SRC) { console.log('  TAMPER DID NOT APPLY (half ii guard anchor not found)'); process.exit(3); }
fs.writeFileSync(PRODUCT+'.bak', SRC);

async function runStale(tagSrc, label){
  fs.writeFileSync(PRODUCT, tagSrc);
  await seed(true);
  const B=fresh(); await B.initDb(); await B.loadFromDb();
  const s=await serve(B.app);
  await val(s.port);                                  // warm: one validate while active
  await sql('UPDATE svc_api_keys SET is_active=false WHERE id=$1',[ID]);   // another process revokes
  const before=await row();
  const answer=await val(s.port);                     // the stale instance validates
  const after=await row();
  await s.close();
  return {label, answer, before, after};
}

console.log('=== ARM W — HALF (i): the usage write must not carry is_active ===');
console.log('    (half (ii) neutralised in a COPY so validate reaches the usage write at all)');
const w1=await runStale(noII,'half (i) PRESENT, half (ii) off');
console.log(`    ${w1.label}: answer=${JSON.stringify(w1.answer.data)} row ${JSON.stringify(w1.before)} -> ${JSON.stringify(w1.after)}`);
rec('W1','a stale instance DOES reach the usage write (the arm is not vacuous)',
    w1.answer.data && w1.answer.data.valid, true);
rec('W2','and the usage write leaves the persisted revoke ALONE',
    w1.after.is_active, false);
rec('W3','while still RECORDING usage (the write is usage-only, not a no-op)',
    w1.after.usage_count > w1.before.usage_count, true);

// the other way: put is_active BACK into validate's write -> the revoke is revived
const revive = noII.replace('await dbRecordApiKeyUsage(apiKey);','await dbSaveApiKey(apiKey);');
if (revive === noII) { console.log('  REVIVE TAMPER DID NOT APPLY'); process.exit(3); }
const w4=await runStale(revive,'half (i) REMOVED, half (ii) off');
console.log(`    ${w4.label}: answer=${JSON.stringify(w4.answer.data)} row ${JSON.stringify(w4.before)} -> ${JSON.stringify(w4.after)}`);
rec('W4','TAMPER: validate writing through dbSaveApiKey REVIVES the revoke (so half (i) is load-bearing)',
    w4.after.is_active, true);

// ---------- V: HALF (ii) ISOLATED, both halves present vs half (ii) removed ----------
console.log('=== ARM V — HALF (ii): validate must answer on the STORED revoke ===');
const v1=await runStale(SRC,'BOTH halves present');
console.log(`    ${v1.label}: answer=${JSON.stringify(v1.answer.data)} row ${JSON.stringify(v1.before)} -> ${JSON.stringify(v1.after)}`);
rec('V1','a stale instance answers valid:false Key revoked', [v1.answer.data.valid, v1.answer.data.reason], [false,'Key revoked']);
rec('V2','and the row is still revoked afterwards', v1.after.is_active, false);
rec('V3','TAMPER (half ii off, W1 above) answered valid:true — so half (ii) is load-bearing',
    w1.answer.data.valid, true);

// ---------- C: the stale memory copy is REFRESHED, not just consulted ----------
console.log('=== ARM C — the stale cache stops lying after one validate ===');
fs.writeFileSync(PRODUCT, SRC);
await seed(true);
{ const B=fresh(); await B.initDb(); await B.loadFromDb();
  const s=await serve(B.app);
  await val(s.port);
  await sql('UPDATE svc_api_keys SET is_active=false WHERE id=$1',[ID]);
  const cachedBefore = B.memApiKeys.get(ID).isActive;
  await val(s.port);
  const cachedAfter = B.memApiKeys.get(ID) ? B.memApiKeys.get(ID).isActive : 'evicted';
  await s.close();
  rec('C1','the cache held isActive=true before the validate', cachedBefore, true);
  rec('C2','and the validate REFRESHED it to the stored value', cachedAfter, false);
}

// ---------- D: a VANISHED row is not honoured from cache ----------
console.log('=== ARM D — a deleted row is a stronger revoke than is_active=false ===');
await seed(true);
{ const B=fresh(); await B.initDb(); await B.loadFromDb();
  const s=await serve(B.app);
  await val(s.port);
  await sql('DELETE FROM svc_api_keys WHERE id=$1',[ID]);
  const a=await val(s.port);
  const evicted = !B.memApiKeys.get(ID);
  await s.close();
  rec('D1','a stale copy of a DELETED key answers valid:false Key not found',[a.data.valid,a.data.reason],[false,'Key not found']);
  rec('D2','and the cache entry is evicted', evicted, true);
}

// ---------- E: MEMORY-ONLY MODE answers from memory (Kam's ruling (a), second limb) ----------
console.log('=== ARM E — memory-only mode (no DATABASE_URL) answers from memory, NOT 503 ===');
{ // no DB at all: isDbAvailable() false. A key only in memory must still validate.
  const saved=process.env.DATABASE_URL; delete process.env.DATABASE_URL;
  for(const k of Object.keys(require.cache)) if(k.includes('/services/security/src/')) delete require.cache[k];
  const m=require(PRODUCT); const db=require(path.join(process.env.DEV,'services/security/src/db.ts'));
  rec('E0','isDbAvailable() is false in this mode', db.isDbAvailable(), false);
  m.memApiKeys.set(ID,{id:ID,tenantId:TEN,name:'mem',keyHash:HASH,keyPrefix:'ks1370',scopes:[],
    rateLimit:1000,rateLimitWindow:3600,isActive:true,usageCount:0,createdAt:new Date(),connectorId:null});
  const s=await serve(m.default||m);
  const a=await val(s.port);
  rec('E1','an ACTIVE memory-only key validates (no 503)',[a.status,a.data.valid],[200,true]);
  m.memApiKeys.get(ID).isActive=false;
  const b=await val(s.port);
  rec('E2','a memory-only key revoked IN MEMORY is refused',[b.status,b.data.valid,b.data.reason],[200,false,'Key revoked']);
  await s.close();
  if(saved) process.env.DATABASE_URL=saved;
}

// ---------- F: a FAILED stored read returns 503 (Kam's ruling (a), first limb) ----------
console.log('=== ARM F — a failed stored read returns 503 Unable to verify key ===');
{ const broken = SRC.replace("await query('SELECT * FROM security_find_api_key_by_hash($1)', [keyHash]);\n      if (storedResult.rows.length === 0) {",
                             "await query('SELECT * FROM security_b42_no_such_function($1)', [keyHash]);\n      if (storedResult.rows.length === 0) {");
  if (broken===SRC){console.log('  F TAMPER DID NOT APPLY'); process.exit(3);}
  fs.writeFileSync(PRODUCT, broken);
  await seed(true);
  for(const k of Object.keys(require.cache)) if(k.includes('/services/security/src/')) delete require.cache[k];
  const m=require(PRODUCT); const db=require(path.join(process.env.DEV,'services/security/src/db.ts'));
  await db.initDb(); await m.loadFromDb();
  const s=await serve(m.default||m);
  const a=await val(s.port);
  await s.close();
  rec('F1','a stored-state read that THROWS answers 503, not valid:true',
      [a.status, a.err && a.err.code, a.err && a.err.message],[503,'SERVICE_UNAVAILABLE','Unable to verify key']);
  rec('F2','and it did NOT answer valid', a.data===undefined || a.data===null, true);
}

fs.writeFileSync(PRODUCT, SRC);
fs.unlinkSync(PRODUCT+'.bak');
const bad=R.filter(r=>!r.ok);
console.log(`\nARMS: ${R.length-bad.length}/${R.length} passed` + (bad.length?`  FAILED: ${bad.map(b=>b.id).join(',')}`:''));
console.log(`product file restored byte-identical: ${fs.readFileSync(PRODUCT,'utf8')===SRC}`);
process.exit(bad.length?1:0);
})().catch(e=>{
  try{const b=require('path').join(process.env.DEV,'services/security/src/index.ts')+'.bak';
      if(require('fs').existsSync(b)){require('fs').copyFileSync(b,b.replace(/\.bak$/,''));console.error('RESTORED from .bak');}}catch(_){}
  console.error('ARMS ERROR', e&&e.stack||e); process.exit(1);});


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/ks1370drill.cjs TEXT_SHA256 a5207708d34d503884694297c305b5f685e0829040db24549bcc1d982131e10d

/* Seat B 41st — KS-1370 driven repro. MEASUREMENT ONLY. No product change.
 *
 * The claim (B 40th's source-path reading): validate resolves the key from an in-memory map
 * populated only at boot (index.ts :1326-:1335), so a revoke performed in ANOTHER process is
 * invisible here; and this process's usage write (:1369 -> dbSaveApiKey -> :316-318
 * `is_active = EXCLUDED.is_active`) then writes the CACHED is_active back over the persisted revoke.
 *
 * TWO INSTANCES, SEPARATE MEMORY MAPS — the shape the brief sanctions. Each `require` of the
 * product module happens with a cleared CJS cache, so each gets its OWN `memApiKeys`.
 * SECURITY_DISABLE_BOOT=1 stops initDb + app.listen (index.ts :1611).
 */
const path = require('path'), crypto = require('crypto'), http = require('http');
const { Client } = require(path.join(process.env.DEV, 'node_modules/pg'));

const PRODUCT = path.join(process.env.DEV, 'services/security/src/index.ts');
const CONN = { host: '/tmp/b41s', user: 'postgres', database: process.env.DRILLDB || 'ks1370' };
const KEY_PLAIN = 'ks1370-drill-key';
const KEY_HASH = crypto.createHash('sha256').update(KEY_PLAIN).digest('hex');
const KEY_ID = '33333333-3333-3333-3333-333333333333';
const TENANT = '44444444-4444-4444-4444-444444444444';

async function sql(q, p) { const c = new Client(CONN); await c.connect(); try { return await c.query(q, p); } finally { await c.end(); } }
async function isActive() { const r = await sql('SELECT is_active FROM svc_api_keys WHERE id=$1', [KEY_ID]); return r.rows[0] ? r.rows[0].is_active : null; }
async function usageCount() { const r = await sql('SELECT usage_count FROM svc_api_keys WHERE id=$1', [KEY_ID]); return r.rows[0] ? r.rows[0].usage_count : null; }

/** A fresh module instance with its OWN memApiKeys. */
function freshInstance(tag) {
  for (const k of Object.keys(require.cache)) {
    if (k.includes('/services/security/src/')) delete require.cache[k];
  }
  const m = require(PRODUCT);
  // SECURITY_DISABLE_BOOT=1 suppresses BOTH app.listen AND initDb (index.ts :1611), and
  // loadFromDb returns early on !isDbAvailable(). So the pool is initialised explicitly here.
  // My first run skipped this, loadFromDb loaded 0 keys, and CONTROL 1 caught it.
  const db = require(path.join(process.env.DEV, 'services/security/src/db.ts'));
  return { tag, app: m.default || m, memApiKeys: m.memApiKeys, loadFromDb: m.loadFromDb,
           initDb: db.initDb, isDbAvailable: db.isDbAvailable };
}

async function serve(app) {
  const s = http.createServer(app);
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  return { port: s.address().port, close: () => new Promise(r => s.close(r)) };
}

async function validate(port, key) {
  const r = await fetch(`http://127.0.0.1:${port}/api/keys/validate`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key }),
  });
  return { status: r.status, body: await r.json() };
}

(async () => {
  console.log('KEY_HASH', KEY_HASH.slice(0, 16));
  // --- seed: one ACTIVE key ---
  await sql('DELETE FROM svc_api_keys WHERE id=$1', [KEY_ID]);
  await sql(`INSERT INTO svc_api_keys (id, tenant_id, name, key_hash, key_prefix, scopes, is_active, usage_count)
             VALUES ($1,$2,'ks1370 drill',$3,'ks1370','{}',true,0)`, [KEY_ID, TENANT, KEY_HASH]);
  console.log('seeded: is_active =', await isActive());

  // --- B boots FIRST, while the key is still active: its cache is warmed with is_active=true ---
  const B = freshInstance('B');
  await B.initDb();
  console.log('B db available:', B.isDbAvailable());
  await B.loadFromDb();
  console.log('B memApiKeys.size:', B.memApiKeys.size);
  const cachedB = B.memApiKeys.get(KEY_ID);
  console.log('B booted: key in B.memApiKeys =', !!cachedB, '| B cached isActive =', cachedB && cachedB.isActive);

  // --- CONTROL 1: a key that was never revoked validates in B (the harness CAN answer valid) ---
  const sB = await serve(B.app);
  const c1 = await validate(sB.port, KEY_PLAIN);
  console.log('CONTROL 1 (never revoked) ->', JSON.stringify(c1.body.data));

  // --- A revokes. Persisted-row equivalent of A's dbSaveApiKey; A is a SEPARATE process/instance
  //     and its route requires an admin identity, so the revoke is applied as the row state that
  //     A's revoke produces. Disclosed as such - it is B that is under test. ---
  await sql('UPDATE svc_api_keys SET is_active=false WHERE id=$1', [KEY_ID]);
  console.log('A revoked: DB is_active =', await isActive());

  const beforeUsage = await usageCount();

  // --- THE MEASUREMENT: B still holds the boot-time cache ---
  const q1 = await validate(sB.port, KEY_PLAIN);
  console.log('ANSWER 1 - B validates AFTER the revoke ->', JSON.stringify(q1.body.data));

  const afterActive = await isActive(), afterUsage = await usageCount();
  console.log('ANSWER 2 - DB is_active after B\'s usage write =', afterActive, '| usage_count', beforeUsage, '->', afterUsage);

  // --- CONTROL 2: a THIRD instance booted AFTER the revoke must refuse it (the DB DOES hold it) ---
  await sql('UPDATE svc_api_keys SET is_active=false WHERE id=$1', [KEY_ID]);   // re-assert before C boots
  const C = freshInstance('C');
  await C.initDb();
  await C.loadFromDb();
  console.log('C memApiKeys.size:', C.memApiKeys.size);
  const cachedC = C.memApiKeys.get(KEY_ID);
  console.log('CONTROL 2 - C booted after the revoke: C cached isActive =', cachedC && cachedC.isActive);
  const sC = await serve(C.app);
  const c2 = await validate(sC.port, KEY_PLAIN);
  console.log('CONTROL 2 (fresh boot) ->', JSON.stringify(c2.body.data));
  console.log('CONTROL 2 - DB is_active after C =', await isActive());

  await sB.close(); await sC.close();
  process.exit(0);
})().catch(e => { console.error('DRILL ERROR', e && e.stack || e); process.exit(1); });


