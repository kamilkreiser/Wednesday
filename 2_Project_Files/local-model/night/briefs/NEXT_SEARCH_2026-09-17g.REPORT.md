# NEXT SEARCH 2026-09-17g (12:54–13:05 AEST): the auth tier

**BLUF: ONE FIT, KS-623. It is the auth service's test-token environment guard: one edit plus a new in-process vitest file.** `services/auth/src/middleware/authenticate.ts:21` refuses test tokens only when `NODE_ENV === 'production'`. The fix swaps that for the gateway's allowlist, `['development', 'test']`. **The real `checker.sh` gave RESULT: PASS (7/7), strict,** on the draft input (fin0) and again on the placed input (fin1), at develop `d7e95cd9f`. A variant that puts the same allowlist at the wrong site (`:25`) gave **FAIL A3b PARTIAL FIX**. Nothing was queued.
- **Why it fits:** one product file, and the fix shape is spelled out in the ticket. The test calls the real `authenticate()` in-process with the jwt/session/logger mocks. R1 and R2 are red by assertion at the tip, and CONTROL plus COMPLETENESS are green. The auth suite goes 751 → 755 with 0 NEW reds, and tsc is rc 0.
- **Why it was held until now:** only the auth hold. `queue.md`'s 09-15 comment lists it under "security surfaces (… kept for Opus builders)".
- **Second fit: none briefed.** I stopped at the first fit, because a second premeasure would run past 20 minutes. The likeliest next ticket is KS-1009 (see Rejections).
- **Wednesday must read before queuing:** see the next section (3 items).

## Wednesday must read before queuing

1. **Closes or Refs.** The ticket says "Ideally share one helper rather than two copies". This task does NOT build a helper: that would edit the gateway's `middleware/auth.ts` (seat A's partition, 3 local heads) or `packages/shared`. It makes the two checks the SAME allowlist, which meets the ticket's Acceptance as written: with `NODE_ENV` unset and the opt-in on, the auth service refuses, and dev/test still work. Rule "Closes KS-623", or "Refs" with the helper filed as a follow-up.
2. **Behaviour change (TIER 1).** When `NODE_ENV` is unset or off the list (for example `staging` or `qa`) AND `ENABLE_TEST_TOKENS=true`, the auth service now refuses `Bearer test_token_…`.
   - The gateway's own parser already refused in that case. But the gateway's `/api/auth` mount is unauthenticated (`authenticate.ts:159-160`, read, not driven), so for auth-service routes this guard is the only one on the path.
   - Compose sets `NODE_ENV=development` for `auth` (`docker-compose.yml:739`), so the local stack does not change.
   - **Not measured:** the demo VM's and any staging host's real env values.
   - Reach is latent: the gateway FATALs at boot on production/staging/demo with test tokens on (`api-gateway/src/index.ts:78-90`, read).
3. **Auth-tier content.** This is an authentication guard. It is the second auth product edit handed to the local model, after KS-1186.

## FOUND
- **Pool: 70 tickets.** Predicate: KS Backlog/Todo at 12:55:50 (**328**, first:50, 7 pages, hasNextPage false) AND at least one of:
  - the census's "auth-shaped title (LAST)" rows (**44**, `grep` over `candidates.md`);
  - the auth-file / auth-hold rows KS-839, KS-915, KS-955, KS-986, KS-1132, KS-759 and KS-1168;
  - created since 2026-09-16T14:00Z with an auth word (auth/mfa/oauth/session/token/jwt/login/password/refresh/lockout/credential) in the title or description (19).
  - 18 of the 19 new-since tickets already carry a 17e / 17f / ROUTED / HELD record and were not re-derived. **KS-1208 is new** (filed 02:24Z, the KS-744 residue).
- **Refused only for auth, now open:** KS-623 is the clean case. Its only recorded hold is the auth-surface line, and its one comment (s147-B, 09-07) says "stays open at P4" and decides nothing.
- **Nearest misses:**
  - KS-1009 (one handler, but the published contract names the fields);
  - KS-805 (the refusal shape is unpicked);
  - KS-938 / KS-1006 (users.ts partition + open #1018).

## TESTED (KS-623)
- **Scratch clone** `/private/tmp/claude-501/night/s17g/clone`: `clone --shared --no-checkout` from a script (`clone.sh`), `checkout --detach` from a script (`checkout.sh`, 12:58:20), then `prepare_clone.sh` rc 0 (12:58:25, shared built, source tracked-modified 0). All vitest and checker runs were under `sandbox-exec nonet.sb`.
- **Test alone at the tip** (12:59:21): 4 run / 2 failed. R1 and R2 are each `expected [ 'ks623-user', 'next-ok' ] to deeply equal [ 'no-user', 'ks623-not-a-real-jwt' ]`. CONTROL and COMPLETENESS are green.
- **Golden** (12:59:29): 4 / 4.
- **Discrimination** (line 21 replaced, 12:59:39–40):
  - `if (true) {` (test tokens disabled outright) → CONTROL red only;
  - unset-only guard → R2 red only.
- **Completeness arm** (12:59:41): the graded cells deleted → `expected +0 to be 3`.
- **Test file:** 81 lines. 0 non-ASCII (control: 1 on an em dash), 0 backslashes, 0 `$`, 0 backticks, 0 double quotes. The brief's fence equals the golden (python True). The brief has 0 backslashes.
- **Real checker** (`tasks/code_patch/checker.sh`, sha256 `2f0003a87b314feb911fbd02d53f69db4f634f9b6c4510123b55af23e54ccafd`, identical before and after every run).

  **fin1**, placed input, 13:03:40–13:03:55, rc 0. Verbatim:
```
mode: code_patch
PASS A1 output is exactly one fenced ```diff block, nothing outside it
baseline suite rc=0 total=751 passed=751 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline tsc rc=0 (0 lines)
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/middleware/authenticate.ts , Blockchain/Dev/services/auth/src/__tests__/ks623-test-token-env-guard-is-asymmetric.test.ts }
PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s))
PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)
PASS A4 RED-FIRST: src/__tests__/ks623-test-token-env-guard-is-asymmetric.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks623-test-token-env-guard-is-asymmetric.test.ts passes with the product hunk (4 passed / 4 run)
INFO control cell present: 2 cell(s) passed BEFORE and 4 AFTER (the harness reaches the code both times)
after suite rc=0 total=755 passed=755 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline: total=751 failed=0 | after: total=755 failed=0
NEW reds: []
PASS A6 whole services/auth suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone: rc=0 (0 lines; not gated — vitest does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +82/-1 test=src/__tests__/ks623-test-token-env-guard-is-asymmetric.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
```
  **fin0** (draft input, 13:02:22–13:02:38) printed the same PASS lines and `RESULT: PASS (7/7)`.

  **wrong2**, placed input, 13:03:55–13:04:02, rc 1. It is the same test, with the allowlist ORed into `:25` instead of `:21`, which is behaviourally a fix at the wrong site. Verbatim:
```
FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 1 named site(s) untouched: :21 `if (process.env.NODE_ENV === 'production') {`
RESULT: FAIL (1 failed) — stopped at A3b (a partial fix; the tests are not run)
```
  **wrong1** (draft input, 13:02:42–13:02:49) printed the same two lines.

**NOT tested**
- The model run itself, and the raise.
- The real env values on the demo VM or on staging.
- Whether any live E2E caller reaches the auth service directly with an off-list `NODE_ENV`.
- The gateway `/api/auth` path end to end.
- KS-1009 and KS-805 beyond a read.

## HOW (partition, measured)
- **Linear** (GraphQL read, the Secuura key sourced transiently in python and never printed, no Bearer prefix):
  - pool pull at 12:55:50;
  - KS-623 in full at 12:57:51: Backlog, P4, assignee and creator Kam, 0 attachments, 1 comment, inverse related KS-625.
- **Open PRs** (GitHub REST GET, paginated, 12:56:48): 20 PRs / 102 paths. **0** name `middleware/authenticate.ts` or `ks623`; control: 2 name `services/auth/src`.
- **Seat A's six local heads** (`git diff --name-only d7e95cd9f <sha>`, the only verb run in `raise-0916-a`): 15 distinct paths, none `authenticate.ts`. They touch the GATEWAY's `middleware/auth.ts` ×3, `index.ts`, `rateLimitEnforce.ts`, `proxy.ts`, auth `users.ts` and originate `documents.ts`.
- **READYs:** 108; 0 mention `middleware/authenticate.ts` (control: 12 mention `services/auth/`). `queue.md`: 0 queue lines for KS-623 (it appears in one comment line).
- **Dependants:** `git grep` at the tip for `test_token_` / `ENABLE_TEST_TOKENS` under `services/auth`: 1 file, `authenticate.ts` itself (the positive control); 0 tests.
- **Source porcelain** (`--untracked-files=no`) = 0 at 13:03:01. No git write verb ran against `!CODING`.

## Tip
`d7e95cd9f153e9036ed77935a73c93504fa6e3dc`. Read by `git ls-remote <source origin URL> refs/heads/develop`, run from the scratch clone with the source's `core.sshCommand`, at 12:57:10 and 13:03:01; the builder also read it at 13:01 and 13:03. It did not move. `cat-file -t` = commit.

## Files

| file | sha256 | note |
|---|---|---|
| `night/briefs/KS-623.md` | `6a5a3a37c22e1dbdf98cb2dbb215f0bdbd6a30ee81e54dd493ca13c96ba59916` | 235 lines. Standard (not line-keyed) Where, because the `-` line is unique at the tip (count 1). Has `## Premises (measured)` P1–P12 and `## Notes for the raise` (behaviour change, TIER 1). |
| `night/inputs/code_623.json` | `ec058ff1c05a01b6929372317ae4f4bebf55251cc1ffe255c4971f91cbf56b4a` | `build_input.sh` rc 0 at 13:03:34. 4 Where sites (1 must_change), 1 expected `+`, 2 red cells, ~9.9K prompt tokens, ctx 65536. `suggested_test_file` == the brief's path. |
| golden test | `f60a055c9558a51b…` | `/private/tmp/claude-501/night/s17g/golden.test.ts` |
| golden `out.md` | `80a61f8994248ce7…` | `/private/tmp/claude-501/night/s17g/fin1/out.md` |
| `night/candidates.md` | `97c427fd73e6ea80…` | SEARCH 17g block appended in an HTML comment by `.new` + `mv`. Backup `candidates.md.pre-1305-search17g`. Backticks 278 before and after (the block has 0). |

**The queue line (NOT added):**
```
KS-623 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_623.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```

**Rebuild pins** (all required): `product=Blockchain/Dev/services/auth/src/middleware/authenticate.ts ref=services/auth/src/__tests__/ks468-authenticate-tenant-guc.test.ts line=21 ctx=65536`.

## Rejections (the rows are in `candidates.md` SEARCH 17g)

| ticket | verdict | reason |
|---|---|---|
| **KS-623** | **FITS (briefed)** | See above. |
| KS-1009 | NOT BRIEFED | One handler (`wallet.ts:402` → `{exists}`), but `auth.openapi.ts:1859` and `docs/openapi/secuura-api.yaml` publish the fields. Probably multi-file and a public contract change. Unmeasured. |
| KS-1208 | REFUSED | New. Gateway `middleware/auth.ts` (partition) plus "a shape decision first" (401 vs forward). |
| KS-805 | REFUSED | Three items; the refusal's status and shape are unspelled (a pick). |
| KS-839 | REFUSED | The wildcard behaviour is unruled. |
| KS-938 / KS-1006 / KS-1005 | REFUSED | `users.ts` (seat A head + open #1018) and/or `userRepo.ts`; two files; 1006 also asks whether the route should exist. |
| KS-1132 | REFUSED | "Decision needed, then the build"; `userRepo.ts` (KS-1186). |
| KS-855 / KS-824 / KS-840 / KS-756 / KS-1107 / KS-782 / KS-834 / KS-1177 / KS-915 / KS-986 / KS-1168 | REFUSED | Decisions, design, or shapes not chosen. |
| KS-836 / KS-1003 / KS-918 / KS-1105 / KS-925 / KS-951 / KS-1146 / KS-1149 | REFUSED | Not a vitest product file: OpenAPI + Schemathesis, nginx, package.json, frontend, launcher, CI/shell. |
| KS-619 / KS-944 / KS-1032 / KS-810 / KS-329 / KS-787 / KS-1124 / KS-759 | REFUSED | Multi-file, partitioned gateway files, jest, or a feature. |
| KS-618 / KS-668 / KS-724 / KS-977 / KS-1038 / KS-1053 / KS-1091 / KS-1017 / KS-955 | REFUSED | Live stack, e2e, flake, probe or class tickets. |
| KS-1015 | REFUSED | Creator peter@obeden.com. |
| KS-793 | REFUSED | Already fixed at tip (board close). |
| 18 new-since rows, KS-744, KS-1156 | STANDS | Recorded in 17e / 17f / ROUTED / HELD; not re-derived. |

The instrument for the refusal rows is a description read plus a keyword and file screen (`screen.py`, `screen2.py`), not a full read of every comment thread. Only KS-623 was measured.

## Deviations
- I used a hand-assembled brief (`assemble.py`: head + golden fence + tail, with the clock from `date`), not `new_brief.sh`, whose skeleton cannot carry the 81-line verbatim fence. This is the same deviation as KS-1156 and KS-1186.
- fin0 left 2 porcelain entries in the SCRATCH clone. The next checker run began clean and ended at 0. The checker quarantines its own leftovers.
- No `cd`, no `rm`: the premeasure test file was moved to `s17g/quarantine/`. No processes were left running (`ps` over `s17g`: 0 at 13:04:39). Load 5.24 at 13:04.
