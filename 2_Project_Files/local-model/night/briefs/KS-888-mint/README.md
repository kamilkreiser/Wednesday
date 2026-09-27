# KS-888 mint: Spark brief + golden (POST /api/keys answers 503/500 with no key material when the save fails)

Written 07:18 AEST 2026-09-28 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and `ls-remote` were READ), mailed nobody and wrote nothing under `!CODING/`. Every write ran in this session's scratchpad, in a `cp -a` copy of `ks1346cd/base`. The base was only read: its HEAD was verified equal to the tip before copying, and its porcelain was 0 at the end.

- **Ruling:** Kam, live board 2026-09-28 06:58 AEST, card `secuura-ks888-failed-key-save-design`, option b, "Fix all three routes". **This brief is the MINT route only.** Revoke and validate go to a Claude seat after a pending card.
- **Contract:** KS-1194's, as Kam ruled it (fail-closed) and as #1032 merged it (`services/auth/src/routes/users.ts:1149`-`:1176`): a save that did not persist is never acknowledged. An infrastructure fault (auth `dbErrors.ts` classes: SQLSTATE 08/53/57, socket codes, the pool-timeout message) answers 503 `SERVICE_UNAVAILABLE`; anything else answers 500 `INTERNAL_ERROR`. Neither body carries a key, a prefix or an id.
- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (`ls-remote` at 07:07 and again at 07:18).
- **Shape:** `dbSaveApiKey`'s contract for other callers is NOT changed. It gains an OPT-IN `opts: { rethrow?: boolean } = {}`, and its catch re-throws only when the option is set. The mint alone passes `{ rethrow: true }` inside its own `try`. On failure it deletes the unsaved key from `memApiKeys`, logs one line, and answers 503/500. Revoke (`:1267`) and validate (`:1335`) call it unchanged.
- **Edit points:** 3 hunks in `security/src/index.ts`: the signature at `:292`, one `if (opts.rethrow) throw err;` after `:332`, and the mint call at `:1132`. There is one new vitest file of 145 lines.

## Files
- `KS-888.md` is the brief.
- `KS-888.golden.diff` is the golden, sha256 `db899f4e1598…`: 2 files, 167 `+` lines, 5 `-` lines (the signature, the save call, and 3 blank lines re-added as `+`).
- **Fence rebuild:** the diff rebuilt from the brief's fences is **IDENTICAL** to the golden (`cmp`). Comparator control: a one-token mutation printed DIFFER.
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote, and there are 0 blank context lines. **1 non-ASCII line**: the copied trailing context `:1134` (an em dash, U+2014). See the doubts.

## Measured (scratch copy at `ec32c40e`, node_modules as farmed in `ks1346cd/base`)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0 |
| test file alone at the tip (RED) | **5 failed / 4 passed / 9**: exactly A1, A2 x3 and A3, by ASSERTION. A1 got `status 201` with a live `sk_…` key. A3 got "expected true to be false". |
| golden applied (GREEN) | **9 / 9**; both files equal the golden byte for byte |
| whole security suite (`vitest run --reporter=json`) | tip **23 files / 247 passed / 0 failed**; golden **24 / 256 / 0** (+9). 0 "Unhandled" in either output. Control: the same grep counted 2 in the candidate arm's output. |
| `tsc --noEmit -p services/security` | rc 0 at the tip and with the golden |
| tsc with tests (temp tsconfig) | rc 2 at both, with the SAME 2 pre-existing ks952 errors and none naming the changed files |
| eslint (`index.ts` and the new test) | rc 0 at both. Control: a planted `var` + `debugger` file gave rc 1. |

**Arms** (the golden test against variant `index.ts` files; the golden was restored and checked with `cmp` after each):

| arm | result | which |
|---|---|---|
| tip | 5 failed / 9 | A1, A2 x3, A3 |
| **ticket-shaped fix** (re-throw 42/23/22 inside `dbSaveApiKey` for EVERY caller; `KS-888-r2/evidence/candidate_fix.diff`) | **6 failed + 2 Unhandled Rejections** | A2 x3, A3, and **C2 + C3 time out (revoke and validate never answer)**. A1 is green (500 through `next`). This is the control that revoke and validate are protected. |
| mint drops `{ rethrow: true }` | 5 failed | A1, A2 x3, A3 |
| `res.status(infra ? 503 : 500)` changed to `res.status(500)` | 3 failed | A2 x3 |
| (informational) `infra = false && <code regex> \|\| <message regex>` | 2 failed | the 08006 and ECONNREFUSED rows. The message-only row stays green, because `&&` binds tighter, so each class has its own row. |
| golden | 0 failed | none |

## COLLISION with KS-908: none (measured)
KS-908 (held, being raised; golden `night/briefs/KS-908/KS-908.golden.diff`) inserts `connectorId: … \|\| null` after `:1155` (the POST 201 body) and after `:1216` (the GET map).

| order | KS-888 strict apply | KS-908 strict apply |
|---|---|---|
| KS-888 alone at develop | `git apply --check` rc 0, `patch -F0 --dry-run` rc 0 | — |
| KS-908 first, then KS-888 | rc 0 / rc 0 | (applied) |
| KS-888 first, then KS-908 | (applied) | rc 0 / rc 0 |

- Both orders give a **byte-identical** `index.ts` (`cmp`).
- The whole security suite with BOTH goldens is **25 files / 260 passed / 0 failed** (247 + 9 + 4).
- KS-888's last hunk ends at old `:1136`, and KS-908's first starts at `:1153`, so no line is shared.

## build_input: rc 0 (whole file and excerpted)
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks1346cd/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-mint bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-888 <out>/input.json product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts line=1132 ctx=65536
```
The build output:
- The ticket is Backlog.
- `prompt source: WEDNESDAY BRIEF … (25444 chars)`.
- Red cells `['RED KS-888 A1', 'RED KS-888 A2', 'RED KS-888 A3']`, 19 expected `+` lines (A3c).
- `suggested_test_file` = the brief's `File:` line; the contract key set is OK.

**Size:**
- **Whole file:** 134,519 B, about **33.9K prompt tokens** (31.6K left for the answer).
- **With `NIGHT_EXCERPT_TRIGGER_BYTES=60000`:** 5 regions `[(1,69),(92,242),(263,360),(468,535),(1018,1379)]`, which keep all three edit sites. That is 100,873 B, about **25.1K tokens**. **Recommended**, as for KS-908.

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/sparkrun/round.sh KS-888-MINT KS-888 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-mint 60000 product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts line=1132 ctx=65536
```
**Round counter:** there was one Ornith round on 2026-09-15 (a PASS on mint only, now stale), and r2 briefed nothing. This is the one rebrief the counter allows. A failure here goes to the cloud.

## UNMEASURED / doubts for Wednesday
1. **Transient faults now refuse the mint (503).** The ticket's own fix shape kept SQLSTATE 08/57 log-only. This brief follows KS-1194, where every failed save is refused and only the status differs (503 vs 500). I read "the same contract Kam ruled for KS-1194" that way. **Confirm, or narrow it to structural-only**, which is a one-line change to the golden.
2. **Two shapes are new to the Spark, and unmeasured there:**
   - Blank lines written as `-`/`+` pairs (hunks 1 and 3).
   - A **non-ASCII em dash in a context line** (`:1134`). It cannot be avoided: `:1131` and `:1133` are blank. A hunk with no trailing context failed `git apply` strict (measured). A hunk with no leading context failed Apple `patch -F0` (measured). The builder has no gate for non-ASCII context. If the model writes a hyphen there, the fence will not apply strict. That is a brief/harness-class failure, not a model one.
3. With no database (`isDbAvailable()` false), the mint still answers 201 from memory (C4), as KS-1194 kept its memory-only path.
4. There was no real Postgres. The fault is planted at the mocked `query`. The OpenAPI registration was not checked for a declared 503 (`check:openapi` not run). The gateway's handling of a 503 from the mint was not read.
5. **Scope:** closes the mint third. Refs KS-888, does NOT close it.
