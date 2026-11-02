# QA Gate 131 verdict: Secuura/Distributed_Secuura PR 1949 (KS-1868, AUTH service, 7 catch sites, held passes O82-P1..P4), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Head `d2b49790` was the same at start and at end.

On the key question (Q2), I ran the real `/api/auth/login` and `/api/auth/logout` routes with only the DB `query`, Redis and the event bus stubbed, at base and at head. The real logger was used, so the real winston pipeline ran. Everything else was real: the password gate, bcrypt/argon2, account lockout, sessions, the refresh denylist, JWT, TOTP, the `authenticate` middleware and the error handler (logs/probe_login_table.txt).
- **An ordinary Error** from the rehash write gets 200 with an access token, a refresh cookie and one active session, at base and at head. That holds with MFA off and with MFA on plus a valid code.
- **An unreadable value** (an Error whose `message` returns a revoked Proxy) gets something different at base: **500, no token, no cookie, no session, and no `lastLoginAt` write or `user.login` event**. The lockout counter had already been cleared by the gate. At head the unreadable value gets exactly what an ordinary Error gets.
- **The rehash runs only after the credential, lockout and MFA checks pass, at both versions.** I armed the rehash with the worst value and tried four refused logins: wrong password, locked out, MFA with no code, and MFA with a wrong code. Each one is refused the same way at base and head (401/401/403/401). None issues a session, none attempts the rehash write, and the lockout counter moves the same way.
- **No case found where an unreadable value issues a session, token or cookie that an ordinary Error would not, or skips a check.** The operator-82 flag holds on both conditions, (i) and (ii).

Logout: at base the unreadable value answers 500 with the session already revoked and the cookie not cleared. At head it answers 200 with the cookie cleared, the same as an ordinary Error. The other five sites (connector-token, issuer-cert list and revoke, OAuth authorize and token) **never answered at all at base with real winston**: the async handlers have no `next`, so the request was left open. At head they answer the same constant 502/500 that an ordinary Error gets.

The numbers re-measure:
- Hunks: identical to O82-P1..P4, line for line.
- Red first: 28 of 44, every one failing by assertion.
- Green: 44 of 44 at head (also 44/44 with real winston, and 44/44 with develop's errorHandler).
- Whole suite: base 1479+13 -> head 1523+13 = 1492 -> 1536 (the +13 is explained in Section 4).
- tsc and leg 16: 0 new errors (42 baselined).
- eslint: 0 errors.
- docs-fragments: clean, and 4 planted defects caught.
- Mutants: **27 of 28 killed**.
- merge-tree: clean onto develop `14fd8e54` and onto `73342c2f` (develop moved during the gate). The PR does not touch auth `src/index.ts`.

**Correct one claim in the commit message and the test headers (G131-F1).** With real winston 3.19.0, only the revoked-Proxy message makes the logger throw. A throwing-toString object, a null-prototype object and a Symbol are logged as `{}`, or the field is dropped, and the request is answered normally at base. For those three kinds, head changes only the log text.

## 1. Heads + diffstat
- START (logs/head_start.log, 13:38:51Z): `refs/pull/1949/head` = `d2b49790d72ca21d526f0135316e4cb0f41831dc`, develop = `14fd8e54aefae355ec5e4bf57e4c6f3f1a710883`. Parent = merge-base = `3e688ee239f2b742feb658c2763e11d5cdd99521`. One commit.
- END (logs/head_end.log, 14:14:06Z): PR head unchanged (`d2b49790`). **develop moved to `73342c2f8f490c2af76fb5dfb3cb02c6aed851c2`** (3 commits: 1439e93e KS-1942, e7a3b1fb KS-1868 security, 73342c2f KS-1724 edge log). None of them touches `services/auth`, and the merge-tree was re-run onto it (Section 6). Clone working tree clean, product files back at the head sha256 (`f69d640b9c87` auth.ts, `14cdaf34ef6c` internal.ts, `c2689e21943e` issuerCerts.ts, `114dbe5baf0b` oauth.ts).
- Diffstat (three-dot, logs/diffstat.log): **10 files, +1050/-7**, as claimed.
  - Product: auth.ts +4/-2, internal.ts +2/-1, issuerCerts.ts +2/-2, oauth.ts +4/-2.
  - 4 new test files: +310, +173, +249, +266.
  - 2 fragments: +19 cheat, +21 flow.
  - Nothing outside `services/auth/src/routes`, `services/auth/src/__tests__` and `Projects Documents/fragments`.
- **Held-pass identity (logs/heldpass_identity.log, scripts/heldpass.py):** every product and test file's `+`/`-` line sequence equals the O82 pass that carries it, line for line (P1 = auth.ts + rehash/denylist test; P2 = internal.ts + test; P3 = issuerCerts.ts + test; P4 = oauth.ts + test). I compared hashes of the line sequences: the same 8 of 8. The two fragments are not in any held pass; they are the seat's own text (read in Section 4).
- **PR body not read directly** (no Secuura `gh` login from here). I used the commit message and Seat W's READY mail instead (evidence/ready_w17_pr1949.txt).

## 2. The hunks (logs/product_diff_routes.log)
- **auth.ts (rehash catch at :554-563 and logout denylist `.catch` at :790-799), internal.ts (:79-88), oauth.ts (authorize :806-815 and token :1116-1125).** Inside the existing inner `try`, `reason = <read>;` becomes `const m = <read>; reason = m === undefined || m === null ? m : String(m);`. A `String()` that throws now lands in the existing `catch { reason = 'unreadable thrown value'; }`.
- **issuerCerts.ts (list :365-374, revoke :516-525).** `reason = err instanceof Error ? err.message : String(err);` becomes `reason = String(err instanceof Error ? err.message : err);`.
- **What does NOT change:**
  - the log message strings, levels and key names (`userId, error` / `error`);
  - every response status, body and header;
  - the order of statements;
  - the platform-admin rehash catch (auth.ts:377-382, still `error: err?.message` unguarded; G131-F4);
  - the tenant-resolution catch (:601-603);
  - `routes/index.ts`, `errorHandler.ts` and every service file.

  Unguarded `error: <x>.message` reads in auth routes and services: 17 at base, 17 at head (logs/remaining_unguarded_reads.log).
- TS note: in internal.ts `m` is typed `string`, so the guard narrows to `never` on the `undefined`/`null` arm. It compiles (tsc rc 0) and the behaviour is right.

## 3. The behaviour question: the authentication surface (THE KEY ONE)

### 3a. Probe (scripts/g131_probe_login.test.ts, run by scripts/probe.sh; copied into the clone and moved out to logs/_quarantine after each run; NOT part of the PR)
**What is real:**
- the routers `routes/auth.ts` and `middleware/errorHandler.ts`;
- `services/passwordLoginGate` (lockout, status, password, MFA);
- `services/password` (a real bcrypt hash, so `shouldRehashAfterVerify` is true and argon2 really runs);
- `services/accountLockout`, `services/session` (a fake redis injected through its own `__setRedisForTesting`), `services/refreshDenylist`;
- `services/jwt` (RS256, `initJwtKeys()`), `services/totp` (a real secret and a real code);
- `middleware/authenticate` (a real Bearer token from a real login);
- `repositories/userRepo`, with real PII crypto using runtime-generated keys;
- **the real `utils/logger` (winston 3.19.0, dev printf format)**, with a capture transport added.

**What is stubbed:**
- `../db` `query`: a SQL responder that records every statement and rejects `UPDATE users SET password_hash...` on demand;
- the redis client: an in-memory fake whose `setex('refresh_denylist:...')` rejects on demand;
- `../events.publishEvent`: records calls, which serve as the audit event.

Every reset seeds a prior lockout counter of 2, so that both `recordSuccess` and `recordFailure` show up in the results. Unhandled rejections: 0 in every cell at both versions.

| case | base | head |
|---|---|---|
| L0 login, no failure | 200, token, cookie, 1 session, counter cleared, lastLogin write, `user.login` | same |
| L1 rehash rejects **ordinary Error** | 200, token, cookie, 1 session, counter cleared, `user.login`; log `error:"db down"` | same |
| L1 rehash rejects thrown string / Error with `""` message / err = revoked Proxy / message getter throws | 200 as ordinary | same |
| L1 rehash rejects **message = revoked Proxy** | **500 INTERNAL_ERROR "An unexpected error occurred"**, no token, no cookie, **0 sessions**, no lastLogin write, no event, counter **already cleared**; no rehash line, the errorHandler logs the TypeError | **200 as ordinary**; log `error:"unreadable thrown value"` |
| L1 rehash rejects message = toString-throws / null-proto | 200 as ordinary; log `error` is an object (winston prints `{}`) | 200; log `"unreadable thrown value"` |
| L1 rehash rejects message = Symbol | 200; `error` key dropped | 200; `"Symbol(ks1868)"` |
| G1 wrong password, rehash armed | 401 UNAUTHORIZED, counter 2->3, 0 sessions, **rehash not attempted** | same |
| G2 locked out + right password, armed | 401, counter 2, locked, **rehash not attempted** | same |
| G3 MFA on, no code, armed | 403 MFA_REQUIRED, counter unchanged, **rehash not attempted** | same |
| G4 MFA on, wrong code, armed | 401, counter 2->3, **rehash not attempted** | same |
| G5 MFA on, right code, rehash rejects ordinary Error | 200, token, cookie, 1 session | same |
| G5 MFA on, right code, rehash rejects **revoked-Proxy message** | **500, no session** | **200 as ordinary** |
| G5 MFA on, right code, rehash rejects toString-throws | 200 | 200 |
| O logout, no failure | 200, cookie cleared, session revoked, jti denylisted | same |
| O logout, denylist rejects ordinary Error (or any readable kind) | 200, cookie cleared, session revoked, **jti NOT denylisted** | same |
| O logout, denylist rejects **message = revoked Proxy** | **500**, session already revoked, **cookie not cleared**, jti not denylisted | **200 as ordinary** |

**Conditions (i) and (ii) for the operator-82 flag are both proven at both versions.**
- (i) The head answer for every unreadable kind equals the ordinary-Error row cell for cell: status, body, cookie, session count, lockout keys, SQL writes and event.
- (ii) The rehash write is reached only after `enforcePasswordLoginGates` returns ok. That covers lockout (G2), password (G1), status, and MFA (G3, G4). In every refused case `rehashAttempted = 0`. The gate's `recordSuccess` has already cleared the counter before the rehash at both versions, so the lockout state is not changed by this PR.
- **Base's 500 for the revoked-Proxy message was not a designed fail-closed.** The 500 came from winston throwing inside the catch. The code's own contract ("Failure to upgrade is logged but does NOT block login", auth.ts:546-548) says 200.

### 3b. The other five sites, with real winston (scripts/realwinston/, run by scripts/rw.sh)
These are the PR's own four test files, unchanged except that the logger mock now forwards every call to the REAL auth logger after capturing it.
- **Head: 44/44** (logs/rw_head_vitest.log).
- **Base: 28 failed.** The revoked-Proxy cells show the real base behaviour:
  - connector-token R1 = **no answer** (`expected null` vs 502);
  - issuer list R1 and revoke R5 = **no answer** (vs 500);
  - OAuth authorize R1 and token R5 = **no answer** (vs 500);
  - login R1 = 500 (vs 200), logout R5 = 500 (vs 200).

  The 21 cells for the other three kinds fail only on the log field (`'<object>'` / `'<symbol>'`); their routes answered.
- With default timeouts under load (load1 11-22) two of these suites timed out in `beforeAll` while importing the route tree (logs/rw_*_default_timeouts.log). That is a load artefact; with `--hookTimeout=60000 --testTimeout=30000` they ran.

At head every site gives the same answer as the ordinary-Error control in the same file:
- connector-token: 502 `BAD_GATEWAY` "Key validation unavailable", no token;
- issuer certs: 500 `INTERNAL_ERROR`, no revoke event;
- OAuth: 500 `server_error`, nothing minted.

The bodies come from constant literals in the catch blocks (read).

### 3c. Who can produce the value
The thrown values are rejections from internal code: pg (DatabaseError / Error), ioredis, the JWT and crypto libraries, and repo helpers. No caller can make one of them carry a Proxy or Symbol `message`. JSON bodies cannot carry either, and KS-1724's body caps sit in front. The values in the cells and in this probe are synthetic. This PR is defence-in-depth for its whole class.

## 4. Re-measure (Node v26.8.1 only; NOT measured on Node 24)
- **Red first** (logs/red_base_new_tests.log): base product + the new files gives **28 failed / 16 passed of 44, every failure an `AssertionError`**: 21 `expected '<object>' to be 'unreadable thrown value'`, 7 `expected '<symbol>' to be 'Symbol(ks1868)'`. Per file: 8/12, 4/7, 8/12, 8/13, which matches the fragment's table.
- **Green:** head 44/44 (logs/head_new_tests.log). Merged with develop's `errorHandler.ts` (the only develop change on these tests' import path; KS-1725 `.errors` -> `.issues`): 44/44 (logs/merged_new_tests.log).
- **Whole auth suite (Q5: the timeout question; maxWorkers 2, `nice 10`):**

  | run | load1 at start | result |
  |---|---|---|
  | head, default timeouts | 22 | 3 failed / 1520 passed of 1523 (130 files) |
  | head, raised (`--hookTimeout=60000 --testTimeout=30000`) | 20 | 2 failed / 1521 of 1523 |
  | base without the 4 new files, raised | 8 | 2 failed / 1477 of 1479 (126 files) |
  | base, default | 6 | 2 failed / 1477 of 1479 |

  - **Load timeout:** exactly one, `ks949-platform-admin-seed-identity` "the enumeration actually finds seed sites" (`Test timed out in 5000ms`), at head default under load 22. It is gone with raised timeouts. It did not time out at base, where load was 6-8. That is the author's ks949 class. The `auth.integration` hook timeout the author named did not reproduce here.
  - **Not timeouts, and red at base and head alike:** `ks1009-wallet-status-reveals-only-existence` (file-level: "could not locate the Dev root from /Volumes/DevMASTER/WEDNESDAY") and 2 cells of `ks1467-auth-app-error-subclasses...` (ENOENT on `/Volumes/DevMASTER/WEDNESDAY/src/services/passwordLoginGate.ts`). Both read files relative to `process.cwd()`, and this gate's runner cannot `cd` (the hook rule). Re-run with cwd = services/auth through `spawnSync`: **48/48 passed** (logs/cwd_artefact_rerun_head.log). These are artefacts of this harness, not of the PR.
  - **Totals:** head 1523 + ks1009's 13 = **1536**; base 1479 + 13 = **1492**. Both equal the author's 1492 -> 1536, a delta of exactly the 44 new cells. No pre-existing cell changed state.
- **tsc:**
  - `tsconfig.json --noEmit` rc 0 (logs/tsc_plain_head.log).
  - `tsconfig.test.json`: 42 errors, all in pre-existing test files, none in the 4 new files.
  - Leg 16 `check.cjs` (logs/leg16_auth.log): "181 files, 130 under __tests__; 42 errors: 42 in the baseline, **0 new**; 0 stale", rc 0.
  - Planted control: a TS2322 + TS6133 in a new test file gives leg 16 rc 1, naming the file. The file was restored byte-identical (logs/leg16_planted.log).
- **eslint** (cwd services/auth; 4 product + 4 test files): **0 errors**, 1 warning `prefer-const` issuerCerts.ts:750. That line is outside the hunks and present on the base blob (`let cert = parsed.data.certId`). Planted file: `no-debugger` error, rc 1.
- **docs-fragments** (logs/frag_outer.log):
  - Clean: rc 0, "flow 117 legacy + 93 new, cheat 112 legacy + 93 new; lint clean, render passes".
  - Planted defects:
    - flow unclosed `<div>`: rc 1;
    - flow `<!--n-->.` removed: rc 1;
    - cheat unclosed `<div>`: rc 1;
    - cheat `</table>` corrupted: rc 1.
  - All four were restored by sha; rc 0 afterwards.
  - The cheat ADVISORY at line 6235 is the same pre-existing one gate 90 saw on develop (G90-F7). It does not come from this PR.
- **Hook "PREFLIGHT INCOMPLETE 13/16"**: quoted from the READY mail, not re-run.

## 5. Mutants (scripts/mutants.py; one site at a time, product only, tests untouched, sha256 restored after every run: all `restore True`; logs/mut_*.log, logs/mutants.json)
28 runs (4 mutants x 7 sites, each against its own file with raised timeouts): **27 killed, 1 survived.** Every kill was by assertion, and only in that site's own cells.

| site | M0 revert | M1 drop undefined/null pass-through (`String(m)`) | M2 constant for every value | M3 strings only, else constant |
|---|---|---|---|---|
| auth rehash | KILLED R1-R4 | KILLED C3 | KILLED C1 C3 R4 | KILLED C3 R4 |
| auth logout | KILLED R5-R8 | KILLED C4 | KILLED C2 C4 R8 | KILLED C4 R8 |
| internal connector-token | KILLED R1-R4 | KILLED C3 | KILLED C1 C3 R4 | KILLED C3 R4 |
| oauth authorize | KILLED R1-R4 | **SURVIVED** | KILLED C1 R4 | KILLED R4 |
| oauth token | KILLED R5-R8 | KILLED C5 | KILLED C2 C5 R8 | KILLED C5 R8 |

| site (issuerCerts mutants) | M0 base expression | M1 constant | M2 non-Error branch -> `'x'` | M3 string messages only |
|---|---|---|---|---|
| list | KILLED R1-R4 | KILLED C1 R4 | KILLED C3 | KILLED R4 |
| revoke | KILLED R5-R8 | KILLED C2 C4 R8 | KILLED C4 | KILLED R8 |

- The survivor (G131-F3): authorize has no thrown-plain-string control. C5, the cell that pins "no `error` field, not the text undefined", exists only for token. So dropping the `undefined`/`null` pass-through at authorize changes only a log line and goes unseen.
- Route or function? Every cell drives the real router over HTTP. The response is pinned by every R cell.

## 6. merge-tree
- Onto develop `14fd8e54` (the commission's figure): **rc 0, tree `7a6b3e93def5dc2242f2a4f45f219a2a4ae0e954`, clean.** The merged tree differs from develop in exactly the PR's 10 paths (logs/merge_tree.log).
  - develop since the base: 7 commits, 99 paths, **0 shared with the PR**.
  - Auth paths changed on develop: `src/index.ts` (PR 1944 / KS-1724: `express.json` -> `boundedJson`) and `src/middleware/errorHandler.ts` (KS-1725: ZodError `.errors` -> `.issues`). **The PR touches neither.** The new tests mount the router directly and never import `index.ts`. They do pass through errorHandler, and they pass 44/44 with develop's copy in place (Section 4).
- Onto develop `73342c2f` (moved during the gate): **rc 0, tree `4a75bff208925790bb0d0680176cd6bc65a31614`, clean.** Again exactly the PR's 10 paths. 0 auth paths in the 3 new commits (logs/merge_tree_develop2.log).

## 7. Kam's ks1346 rule (type and field NAMES, never values)
- **No new log line.** Every changed site keeps its message, level and key names. Only the value of the `error` key changes. That value was already the thrown message at base (and still is for an ordinary Error), as at every earlier KS-1868 gate.
- **For hostile values, head logs less than base.** At base, winston serialised an object message with its fields: measured `{"error":{"f":"VALUE_SHOULD_NOT_PRINT"}}` for a null-prototype object with one field (logs/winston_probe_*.log). At head that becomes the constant, and a plain object with a prototype becomes `"[object Object]"`. The one new piece of text is a Symbol's description (`"Symbol(ks1868)"`). The probe captured key names only.
- **P3 edge (Q4), measured (logs/p3_edge.log).** At issuerCerts only, an Error whose `message` is `undefined` (set to undefined, or a getter returning undefined) was logged with the `error` key **omitted** at base. At head it is logged as **the text `"undefined"`**. This is log text only. Both routes answer the same constant 500 either way, and nothing else reads `reason`. A `new Error()` (message `""`), a thrown `undefined`/`null` and a thrown string log exactly as before. The other five sites keep `undefined`/`null` as they are. No value is disclosed. G131-F2.

## 8. Notes for the PR body (G131-F#)
- **G131-F1 (info, wording correction, measured):** the commit message and the four test-file headers say a throwing-toString object, a null-prototype object and a Symbol make "the logger throw inside the catch and the request is never answered". With the real winston 3.19.0 (both the json and the dev printf formats; logs/winston_probe_prod.log, logs/winston_probe_dev.log, logs/rw_base_vitest.log), **only the revoked Proxy throws**. The other three print `{}`, or the field is dropped, and the route answers normally at base. The route-level change at base -> head is therefore:
  - login 500 -> 200 and logout 500 -> 200;
  - connector-token, issuer list/revoke, OAuth authorize/token: no answer -> the constant 502/500;
  
  and it applies to the revoked-Proxy kind only. For the other three kinds the change is log text only.
- **G131-F2 (info):** the issuerCerts P3 edge in Section 7. An Error whose message is undefined now logs `"undefined"` instead of omitting the key. It is log text only, it diverges from the other five sites (which omit the key), and no cell pins it.
- **G131-F3 (recommended, test gap, measured):** mutant M1 survives at OAuth authorize. Add the authorize twin of control C5 (a thrown plain string logs with no `error` field).
- **G131-F4 (info, same class, pre-existing, base = head, read not run):** two related gaps remain in the platform-admin branch of `/login`.
  - Its rehash catch (auth.ts:377-382) still reads `err?.message` unguarded and passes the value through. An unreadable value there gives a 500 with no session (fail-closed); an ordinary Error gives a 200 with a session.
  - Its rehash runs **before** its MFA check (:370 vs :419). So a platform-admin login that then fails MFA has already rewritten the password hash. The regular-user branch moved its rehash after the gate under KS-796 for exactly this reason.
  
  The PR touches neither. Both belong on the KS-1868 / KS-796 follow-up list. This gate did not run the platform-admin branch (it needs `PLATFORM_DATABASE_URL`).
- **G131-F5 (info, forward-looking, read):** among the 15 other unguarded reads that remain (logs/remaining_unguarded_reads.log), three sit in `services/accountLockout.ts` (:92 isLockedOut "failing open", :122, :133).
  - Today an unreadable Redis error there throws out of the catch, so the lockout check **fails CLOSED** (the login gives 500).
  - A future KS-1868 raise of :92 would turn that into the designed fail-OPEN, which **skips the lockout check**. The lockout is a credential check, so that raise should get its own tier-1 gate.
  
  This PR does not touch it.
- **G131-F6 (info):** logout, at base and head and for every failure kind, ordinary included: when the denylist write fails, the refresh jti is NOT denylisted. The session is revoked, so `/refresh` still fails. That is the existing defence-in-depth design, and this PR does not change it.
- **G131-F7 (info, test-harness note):** under load, the PR's suites time out in `beforeAll` while importing the route tree (10 s default hook timeout). Raising the timeouts on the command line is a load workaround and changes no assertion. Whole-suite timeouts: Section 4.

## 9. NOT TESTED
- The real PR body text (no gh auth).
- A real PostgreSQL, Redis or event bus, and a booted auth service (`index.ts`, with KS-1724's body caps in front).
- winston in production `json` mode **through the route**. Measured standalone only: the same throw set as dev mode.
- The platform-admin login branch (G131-F4).
- OAuth authorize/token, connector-token and issuer certs through a real DB and a real authenticate path. These ran through the PR's own harnesses with the real logger.
- Node 24.
- The four platform suites. CI.
- The pre-push hook legs (quoted from the mail).
- ks1009/ks1467 at base with the correct cwd (they are red at both versions here, from the cwd artefact only).
- The Linear ticket text.
