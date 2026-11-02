# QA Gate 113 verdict (TIER 1): Secuura/Distributed_Secuura PR 1931 (KS-1868, services/auth: connector-token, OAuth authorize + token, issuer certs list + revoke, login rehash, logout denylist)

## BLUF
**GATE 113 (TIER 1) on PR 1931 at bafab56a1edc: GO WITH NOTES. Nothing has to be fixed before merge.**

- **a) The login 0 -> 1 is legitimate, not a credential on a failed check.** The only changed login catch is the UPGRADE-ON-VERIFY rehash catch, which runs strictly AFTER `enforcePasswordLoginGates` returned `ok` (lockout, user lookup, status, SSO-only, password, MFA all passed). Measured: with an unreadable rehash rejection armed, wrong password / MFA required / SUSPENDED / locked out / unknown email all give 401 or 403 with 0 sessions, 0 token pairs, and the rehash is never reached, at base and head alike. On a passing login, head-unreadable equals head-ordinary on every counted field: 200, 1 session, 1 token pair, the lastLoginAt write, the user.login event and the refresh cookie (the author did not count the last three; I did). Base answered 500 with none of these.
- **b) Fail-closed everywhere else, measured.** I covered 206 failure scenarios per run at head where a check failed or a pre-issue step threw. Shapes: 10 thrown-value shapes at every throw point of connector-token, authorize (including client-secret-less deny), token (code grant and refresh grant: client lookup, client-secret verify, code exchange, user lookup, session create, refresh-JTI denylist lookup) and issuer certs. Result: 0 sessions, 0 token pairs, 0 connector tokens, 0 auth codes, no token/code in any body or Location, no success status. The judge asserts this mechanically, in both logger formats.
- **c) Real winston, hostile non-string message:** an Error whose `message` is a revoked Proxy still makes winston throw inside the new catch. The outcomes are identical at base and head:
  - oauth, issuer-certs, connector-token: NO RESPONSE + 1 unhandled rejection;
  - login: 500, no session;
  - logout: 500, cookie kept.
  Symbol / throwing-toString / null-proto messages log and proceed, also identical. Not a regression (G113-F1).
- **d) ks1346:** the constant complies. Readable messages are still logged BY VALUE on all 7 edited lines, which is pre-existing and unchanged (G113-F5).
- **e) Outbound:** none. The only network use in these routes is the connector route's fetch to the security service, which was stubbed. Every other fetch target was recorded as outbound: `[]`. Socket connects across 4 runs: 344, all `127.0.0.1`.
- **f) Byte-identity, mutants, suite, merge-tree:**
  - All 4 product blobs and all 4 test blobs equal the held O73-P3..P6 Spark passes.
  - 35/35 mutants on the PR's 7 guards killed, each by exactly its own cells.
  - Suite: same 4 environmental failures before and after, +21 cells (G113-F8).
  - merge-tree onto develop `e2a2426d` (moved twice during the gate) is clean: exactly the PR's 10 paths, 0 shared.
- **Amend 90cc44b6 -> bafab56a:** VERIFIED. 90cc44b6 is not on origin ("not our ref"); I read it read-only from the author's worktree object store.
  - Same parent `968f1707`, same author/committer, byte-identical commit message.
  - Tree diff: exactly 1 file, 1 line, the CHEAT fragment's ks949 sentence. The product and test bytes are identical.

## 1. Heads + diffstat (logs/head_start.log, head_mt.log, head_end.log, diffstat.log, amend_diff.log)
- **PR head:** `bafab56a1edc99eac9b80bd74c402917f3a14cf5` at START (07:15:31Z), at 07:28Z and at END (07:41:33Z). Unchanged.
- **Develop:** `c234c2388a16` at START and 07:28Z, **`e2a2426d221d` at END** ("security service catches ...", i.e. PR 1930 merged).
- **Commit:** one commit, parent `968f17070208` (= merge-base). Author and committer Kam Kreiser <kamil.kreiser@secuura.ai>. Subject "Refs KS-1868: auth route catches log a constant reason for an unreadable thrown value". "Refs" only, no close word. Co-Authored-By trailer present.
- **Three-dot diff vs 968f1707:** exactly 10 files, **+868/-7**, all mode 100644. 4 M (routes: auth 14/2, internal 7/1, issuerCerts 14/2, oauth 14/2) and 6 A (4 tests 253+123+192+200, cheat 24, flow 27). Nothing outside the declared paths.
- **Old head 90cc44b6:** origin refuses it by sha (`not our ref`), so I read it from `!CODING/Secuura/Blockchain/worktrees/s-w16-auth` with read verbs only (log, rev-parse, diff).
  - Trees: `1d962bf3` vs `df9f6078`.
  - Diff: one line in `fragments/cheat/KS-1868-auth-...html`. "(KS-1053), not this change" became "on three of that file's cells (KS 1053), not this change".
  - Commit messages diff empty. The author's claim holds.
- **PR body:** NOT read (no Secuura gh auth on this host). I used the READY and BUILT mails (evidence/).

## 2. The hunks (logs/product.diff)
Seven catches, one shape: `let reason: string; try { reason = <the original expression>; } catch { reason = 'unreadable thrown value'; }`, then the original log call with `error: reason`.

| site | original expression | after the log |
|---|---|---|
| auth.ts login rehash catch (:555) | `err?.message` | unchanged; login proceeds |
| auth.ts logout denylist `.catch` (:790) | `err?.message` | unchanged; logout proceeds |
| internal.ts connector-token catch (:80) | `(err as Error).message` | 502 BAD_GATEWAY |
| issuerCerts list (:365) and revoke (:516) catches | `err instanceof Error ? err.message : String(err)` | 500 |
| oauth authorize POST (:806) and token (:1116) catches | `error.message` | 500 server_error |

- A readable value takes the identical expression and so produces the identical log line.
- No status, body, branch, SQL or event line changes.
- What changes is only that the catch can no longer throw while READING the value. Winston can still throw while FORMATTING it (F1).

## 3. Behaviour (scripts/g113_probe.test.ts, runprobe.sh, swap.sh, short.py, judge.py; logs/probe_{base,head}_{test,production}.jsonl, short_*.txt, judge_*.log)
**HOW.** One vitest file, run 4 times: base/head product (swapped by blob, sha-checked) x NODE_ENV test/production (both winston formats). Each run has 235 scenarios.
- **REAL:** `authRoutes`, `internalRoutes`, `oauthRouter`, `issuerCertsRoutes`, `passwordLoginGate` (the whole gate including `assertAccountMayReceiveCredential`), the auth `errorHandler`, and the winston logger (wrapped call-through; a winston throw propagates).
- **Served on 127.0.0.1;** real HTTP client with a 1.5 s timeout (no answer = NO_RESPONSE).
- **Replaced by stateful recorders** (counting what would be PERSISTED or ISSUED):
  - userRepo (pwHash writes, lastLoginAt writes)
  - session (created / revoked)
  - jwt (token pairs, connector tokens)
  - refreshDenylist (denylisted JTIs)
  - accountLockout (failure / success)
  - oauth service (auth codes minted, codes exchanged)
  - issuerCertRepo (revokes)
  - events (published types)
  - `fetch` for the security service
  - authenticate (sets req.user / sessionId)
- **Thrown-value shapes:** ordinary Error (message carrying an IP and `password=`), revoked Proxy, message-getter throws, null-proto object, plain string, undefined. Plus Errors whose message is a revoked Proxy / Symbol / throwing-toString / null-proto.

**Judge** (1473 checks per format, **0 fails, rc 0** in both):
- 55 scenarios differ base -> head. Every one is a base failure (NO_RESPONSE + unhandled rejection, or 500) that at head equals the same throw point's ordinary-Error record on outcome AND log shape, with exactly one constant log line.
- All other 180 records are identical base vs head (stack text masked; line numbers moved).
- Fail-closed holds on every failure scenario at head.
- No `hunter2` in any head constant-path log.
- Outbound `[]`, loopback only.

**Tamper controls:** rc 1 on each of 3 planted tampers:
- tk_secret_revoked tokenPairs=1;
- login_badpw_rehash_revoked sessions=1;
- az_verify_getter code in Location.

**The only counted state differences base -> head** (both formats):
- `login_rehash_revoked` and `login_rehash_getter`: sessions 0->1, tokenPairs 0->1, lastLoginWrites 0->1, events [] -> [user.login]. This equals `login_rehash_ordinary` at base and at head.
- Everything else that changed differs in response/hang only, with no state difference:
  - connector 502;
  - oauth 500;
  - issuer 500;
  - logout 200 + cookie cleared.

Per-site table (head; base in brackets where it differs):

| site / throw point | ordinary Error | revoked / getter | extra shapes fixed by head | state |
|---|---|---|---|---|
| login rehash (after full gate) | 200, 1 session, 1 pair | same [base 500, 0/0] | - | = ordinary |
| login refused (badpw/mfa/suspended/locked/unknown) + rehash armed unreadable | 401/403 | same, base = head | - | 0 sessions, rehash not reached |
| logout denylist | 200, cookie cleared, session revoked 1, JTI not denylisted | same [base 500, cookie kept, session revoked 1] | - | = ordinary |
| connector fetch / json / mint | 502 | same [base NO_RESPONSE, 1 unhandled] | undefined | 0 connector tokens |
| authorize app / verifyPassword / mintCode / deny-app | 500 | same [base NO_RESPONSE] | undefined | 0 codes |
| token app / clientSecret / exchange / user / session; refresh clientSecret / isDenylisted | 500 | same [base NO_RESPONSE] | undefined | 0 sessions, 0 pairs (code consumed on user/session failure, = ordinary) |
| issuer list / revoke get / revoke | 500 | same [base NO_RESPONSE] | null-proto | 0 revokes, 0 events |

- **Run vs read.** RUN: everything in the REAL list.
- **NOT run:** `index.ts` boot, the real authenticate middleware, real pg / Redis / JWT keys, the api-gateway.
- **Gateway caller (read):** `api-gateway/src/middleware/auth.ts:241` treats non-2xx and timeout alike as "no Bearer" (fail closed). So head's 502 only replaces a timeout.

## 4. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Install:** `npm ci --ignore-scripts` at Blockchain/Dev gave rc 0; `packages/shared` built, rc 0.
- **Red-first** (logs/red_base.json): the 4 new files against base product give **14 of 21 failed, all by assertion**:
  - `expected null to deeply equal {...}` x10 (the hangs);
  - `{status:500, minted:false}` vs `{200, true}` x2 (login);
  - `{status:500,...}` x2 (logout).
  The 7 ordinary-Error controls pass. Head: **21/21** (logs/new_head.json).
- **Suite** (logs/suite_{base,head}.json; base = base product with the 4 new files held out):
  - base 122 files, 1458 tests, 1454 pass, 4 fail;
  - head 126 files, 1479 tests, 1475 pass, 4 fail.
  The same 4 fail on both sides, all environmental (G113-F8). With cwd = services/auth and `--testTimeout=120000`, those 3 files pass 79/79 at head (logs/suite_cwd_head_3files.json). Adding ks1009's 13 uncollected cells gives 1471 -> 1492, matching the author.
- **tsc** (`tsc -p services/auth/tsconfig.test.json`):
  - base 42 errors, head 42 errors, the identical set (line numbers masked);
  - 0 errors in the 4 changed routes or the 4 new tests;
  - planted file: 43, named once.
- **eslint** (Dev flat config, own node_modules) on the 8 changed .ts files: 0 errors, 1 warning (`prefer-const` `cert` at issuerCerts.ts:750, outside the hunks, the author's "present at base"). Planted file: rc 1.
- **docs-fragments** (scripts/frag.sh, logs/frag_check_*.log):
  - clean run: rc 0 OK;
  - 4 planted defects (unclosed div in each fragment, `<!--n-->.` removed, `</table>` corrupted) each give rc 1 naming the fragment;
  - restored by sha, then rc 0;
  - the cheat :6235 ADVISORY is develop's own (also seen by gate 111).
- **Pre-push hook** (13/16 legs, PREFLIGHT INCOMPLETE) and CI are the author's; not re-run.

## 5. Mutants (scripts/mutants.py; logs/mutants.log, mutants_run.json; product only, tests untouched, sha256-restored after every run, all `restored: true`)
Forms per guard:
- undo guard (original unguarded expression)
- fallback rethrows
- wrong constant `'x'`
- always constant (read dropped)
- fallback reads the value (`String(err)`)

Results:
- **PR's 7 guards x 5 = 35/35 killed.** Each kills exactly its own cells: R pair for 4 forms, C cell for always-constant.
- The regex also matched 3 PRE-EXISTING guards in auth.ts (:307, :627, :907; not in this diff, unchanged blobs at base). Their 15 mutants survive: no cell covers them. This is info only, not this PR's lines.

## 6. Byte-identity to the held Spark passes (scripts/held_vs_pr.sh, logs/held_vs_pr.log)
Each `runs/spark_secuura_2026-11-02_ks_1868_o73_p{3,4,5,6}_*/out.md.checker/patch.diff` (named files only) applies rc 0 strictly with `git apply --cached` on a temporary index of 968f1707. The blobs it produces equal the PR's:
- P3: internal.ts `63bc3b80` + test `b6e16740`
- P4: oauth.ts `802144a8` + test `b7716d2c`
- P5: issuerCerts.ts `7fa838aa` + test `b1d14477`
- P6: auth.ts `2205429c` + test `70918c7c`

So there is no hand edit in code; the fragments are the author's. The control dirs carry the same patch sha, except P6-control, whose test blob differs (`0bc510a7`; it is the control, not the raised pass).

## 7. merge-tree (scripts/mergetree.sh; logs/mergetree.log, mt_paths.log, dev_paths.log)
- Re-read by ls-remote at 07:41:40Z: develop `e2a2426d`. `git merge-tree --write-tree e2a2426d pr1931` gives rc 0, tree `4d94317f`.
- The result vs develop changes exactly the PR's 10 paths (SAME_PATHS), +868/-7.
- Develop's 36 paths past 968f1707 share 0 with the PR, and 0 are under services/auth. The 4 merged route blobs = the PR's.
- The earlier merge onto `c234c238` was also clean (tree `3233ea3a`).
- Probe and fragments check not re-run on the merged tree (read only; 0 shared paths).

## 8. Kam's ks1346 logging rule
- **The 7 edited log lines** (auth.ts :561 :796, internal.ts :86, issuerCerts.ts :371 :522, oauth.ts :812 :1122): for an unreadable value they log only the constant under field name `error`. That complies.
- **For a readable value** they still log the message VALUE, as at base. Measured: `db down at 10.0.0.7 password=hunter2` verbatim at base and head. The login line also carries the `userId` value. Pre-existing (G113-F5).
- **No new value, token, code or secret reaches any log or response.** Head discloses less than base. Base login/logout routed the read's TypeError text into errorHandler's `Error occurred` line and stack; head does not.

## 9. FINDINGS
- **G113-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured).** `reason` holds whatever `.message` returned. With an Error whose `message` is a revoked Proxy, the REAL winston throws while formatting, in both formats:
  - connector/oauth/issuer: NO RESPONSE + unhandled rejection;
  - login: 500, no session;
  - logout: 500, cookie kept.

  Identical at base and head; nothing is issued. Same class as G108-F1 / G109-F1 / G111-F1. `let reason: string` is a type lie here (`err?.message` / `error.message` is `any`).
  Follow-up (PR 1924's form): `reason = String(<expr>)` inside the same try, plus one cell per file. The author's cells stub the logger, so they cannot see it.
- **G113-F2 (RECOMMENDED; measured).** Committed cells cover only revoked-Proxy and getter-throws. Head also fixes two more shapes that base hung on, and no committed cell pins either:
  - a thrown `undefined` at oauth and connector-token;
  - a thrown null-prototype object at issuer-certs.

  Suggest one cell each.
- **G113-F3 (INFO; measured) — the headline.** The login 0 -> 1 (session, token pair, plus lastLoginAt write and user.login event) occurs only after the full credential gate passed, and equals the ordinary-Error outcome. No refused login issues anything at base or head. Not a NO GO condition.
- **G113-F4 (INFO; measured).** Logout with an unreadable denylist rejection: 200, cookie cleared, session revoked (1), refresh JTI NOT denylisted, the same as an ordinary Error.
  - Base: 500, cookie NOT cleared; the session was already revoked and the JTI was not denylisted either.
  - So head is no weaker on the token. Session revocation is what breaks `/refresh`, as the code comment says.
- **G113-F5 (INFO, pre-existing).** Readable thrown values are still logged by message VALUE on all 7 edited lines, plus `userId` on the rehash line. errorHandler logs `err.message` + stack. This is against the ks1346 names-not-values card; unchanged here, and the constant complies.
- **G113-F6 (INFO, pre-existing, out of scope).** `middleware/errorHandler.ts` reads `err.message` unguarded. An unreadable value thrown elsewhere in /login (verifyPassword, createSession) or /logout (revokeSession) makes the errorHandler throw, and Express's finalhandler answers 500 HTML.
  - Under non-production NODE_ENV that body carries the thrown getter's own text (`getter boom`). Production does not.
  - Identical at base and head. It is another KS-1868 site, as are oauth.ts's `message: error.message` response bodies (:1272 ff.), which the fragment already lists as not touched.
- **G113-F7 (INFO).** Develop moved twice during the gate (c234c238 -> e2a2426d, PR 1930 merged). The merge-tree onto e2a2426d is clean, with 0 shared paths and 0 auth paths. The author's tests ran on 968f1707, not on the merge.
- **G113-F8 (INFO, harness).** My suite run used `--root` from another cwd. That makes ks1009 (13 cells, "could not locate the Dev root") and ks1467 (2 cells) fail, and ks949 hit its 5000 ms timeout (2 cells): the same 4 failures at base and head. With the service cwd and `--testTimeout=120000` the 3 files pass 79/79. The author's 1468/1471 -> 1492/1492 is consistent with my counts.
- **No FIX-BEFORE-MERGE item.**

## 10. NOT TESTED
- The live PR body, the Linear ticket, CI, the pre-push legs, and Node 24.
- A real `index.ts` boot, the real `authenticate` middleware, real Postgres / Redis, real JWT signing keys, the real security service, and the api-gateway end to end.
- Whether a real driver or library ever throws these values (all synthetic).
- The platform-admin login branch (its own catches, not in this diff).
- OAuth public-client (PKCE) paths: I used a confidential app only.
- The probe and fragments check on the merge-tree result.
- The author's own 61-check recorder: not in evidence; I built my own (1473 checks per format).
- A full-suite run with the service cwd: only the 3 cwd/timeout-sensitive files were re-run that way.
- Mutant forms beyond the 5 listed.
