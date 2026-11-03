# QA GATE 161: Secuura Platform K PR 1978 (KS-1868, auth cert sweep, OAuth state, password, email), TIER 1, round 1

**Verdict: GO WITH NOTES. Nothing has to be fixed before merge. MERGE on the class bar: no HOLD-FOR-KAM, because no head cell at any changed site is more permissive than base with an ordinary Error. The isPasswordBreached fail-open is real but identical to base, and the function has no caller (G161-F2, a pre-existing finding for a Kam card, not caused by this PR).**

The class bar holds at all eight changed catch sites. I ran 19 value kinds through 10 recorder paths (the 8 sites, with ACS split into "SMTP behind it" and "nothing behind it" and OAuth state split into GETDEL and the MULTI fallback). I ran each under both the development and production logger formats, with the real auth winston logger. Head ends in exactly the state that base with an ordinary Error reaches in **380 of 380** head cells. In every one of those cells the site also logged its line with text.

On the TIER 1 questions, in short:
- **isPasswordBreached** answers `false` (fails open) for every hostile value at head, which is what base gives an ordinary Error. At base, 6 kinds in development and 4 in production made it **reject** instead.
- **No caller:** I confirmed it, with the positive control giving 4 call sites for verifyPassword (G161-F2).
- **verifyPassword** refuses (`false`) for all 19 kinds at head, the same as base with an ordinary Error.
- **sendEmail:** I drove the register and forgot-password routes with the real email.ts. At head, a hostile value gives the same status, the same stored rows and the same calls as base with an ordinary Error. Head also **closes** a base existence oracle: forgot-password answered 500 for an existing account and 200 for an unknown one.
- **consumeOAuthState:** no hostile value lets a state be accepted, and a replay is refused in every cell.
- **Cert sweep:** no path leaves an expired cert valid where base with an ordinary Error would have flipped it. One unchanged sibling catch in the same loop (EXPIRING_SOON publish) still crashes the process at head (G161-F4).

Subject:
- Head `1062b621269dac98f618a89f10baa51ff49c8c34`. It equals `git ls-remote origin refs/pull/1978/head`, run from the read-only checkout at 00:23:21Z (`logs/head_start.log`) and again during this gate.
- PR parent and build base `66cbe4e52d5afadc9d13ca141200026cc68d5095`. Develop is `19fc68309c254227e751b3186970360f921fdc74`, one commit past the base.
- The clone `repo/` is a `git clone --shared` of the Secuura checkout. It already held the head commit, so no fetch was needed.
- Host Node v26.8.1, typescript 5.9.3 (clone).

## Answer to question 1 (isPasswordBreached fails open; no caller)

**Measured** (`logs/matrix_all.json`, path `hibp`). The real base and head password.ts and the real winston logger were used, with `fetch` rejecting with each kind:

| | base, ordinary Error | base, hostile | head, all 19 kinds | control: fetch answers, suffix present |
|---|---|---|---|---|
| development | `false` + "HIBP lookup failed — failing open" | **REJECTED** for 6 of 19: revokedProxy, messageGetterThrows, bigintMessage, messageToJSONThrows, messageIsRevokedProxy, cyclicMessage | `false`, 19 of 19, one line with text | `true` |
| production | `false` | **REJECTED** for 4 of 19 (the same set without bigint and cyclic, which production's json() serialises) | `false`, 19 of 19 | `true` |

- So head turns "reject" into "fail open" for those kinds.
- For every kind, head equals what an ordinary Error already gets at base.
- The positive control shows the instrument can see a `true`.
- This is consistent with the author's "4 of 12 rejected" and wider.

**No-caller claim: CONFIRMED** (`logs/q1_grep.log`, `logs/q1_grep2.log`). I ran `git grep` on the object database at head **and** at develop 19fc6830, so the result does not depend on the working tree.

| Search | isPasswordBreached | verifyPassword (positive control) |
|---|---|---|
| A: author's scope (`Blockchain/Dev/{services,packages,scripts}`; ts/tsx/js/cjs/mjs; node_modules and dist excluded), non-test hits | 2: the definition `password.ts:130` and the header comment `password.ts:12` | **4 call sites**: `routes/auth.ts:360`, `routes/mfa.ts:358`, `routes/users.ts:988`, `services/passwordLoginGate.ts:414`, plus imports and comments. This equals the author's 4. |
| B: all of `Blockchain/Dev`, **including frontend**, mobile, sdk and tests; ts/tsx/js/jsx/cjs/mjs/mts/cts | same 2 non-test hits | same 4 |
| C: whole repository, **any file type**, case-insensitive substring | 12 at head: 7 in the PR's own new test, 2 in password.ts, 3 in the PR's two new doc fragments. 2 at develop (password.ts only). | 80 at head / 70 at develop |
| D: dynamic or namespace imports of the password module (non-test) | only `passwordLoginGate.ts:413`, which destructures `verifyPassword` | n/a |
| E: `pwned`, `haveibeenpwned`, `breached password` or `k-anonymity` anywhere | only password.ts and the two new fragments. One e2e spec matched only on the word "pwned" in an attack string, which is unrelated. | n/a |

- No module imports `isPasswordBreached` by name. The named imports of the password service are in auth.ts:14, users.ts:15 and mfa.ts:30, and none of them includes it.
- Search C covered the whole repository, so nothing outside the author's scope calls it either. That includes the frontend, the gateway, the other services and the scripts.

**What password.ts documents** (read). The file header (lines 5-15) is titled **"Pen-test F-12 fixes:"** and lists three items:
1. Argon2id.
2. Minimum length 12/14.
3. "HaveIBeenPwned k-anonymity check — `isPasswordBreached(pw)` … Network failure fails OPEN".

The function's own doc comment (:123-129) says it "fails OPEN … so an HIBP outage doesn't block authentication". It also says it can be disabled with `HIBP_ENABLED=false`.

So the file documents the HIBP check as **the third remediation of pen-test finding F-12**. Nothing in the repository calls it, so that step **never runs**:
- the register, reset-password and change-password routes accept a known-breached password, provided it passes `checkPasswordStrength`;
- the `HIBP_ENABLED` switch controls nothing.

The author called it "step 3 of the password policy". The exact wording is item 3 of "Pen-test F-12 fixes". I did not read the pen-test report, so I cannot say whether F-12 item 3 was accepted as residual.

**Plain answer for Kam:** this PR does not create the fail-open. An ordinary network error already made the breached-password check say "not breached". The PR makes the unusual thrown values say the same, where before they made the function throw.

The bigger fact is that nothing anywhere in the repository calls the breached-password check. The password service's header lists it as part of the pen-test F-12 fix. So that part of the fix has never run in production: a password that appears in a public breach list is accepted, as long as it meets the length and character rules.

That is pre-existing and unchanged by this PR, and merging the PR neither helps nor hurts it. You may want a card covering two things: whether to wire the check into register, reset and change-password, and whether failing open on an HIBP outage is still the policy you want.

I measured the fail-open behaviour by running it. I established the no-caller fact by search: every code file and every file type at head and at develop, with the verifyPassword control finding its 4 callers.

## Findings

**G161-F1 (INFO, positive): the class bar holds at all eight changed sites, 19 kinds x 10 paths x 2 logger formats.**
- FOUND: head equals base-with-ordinary-Error in **380 of 380** head cells at the changed sites. "Equal" covers alive/died, the resolved value or rejection, the call sequence, and for OAuth the "still stored" and replay results. For the sweep it also covers the logged counts.
- The reference states are:
  - verifyPassword `false`.
  - isPasswordBreached `false`.
  - ACS with nothing behind it: `false`.
  - ACS with SMTP behind it: `true`, and SMTP is called.
  - SMTP `false`.
  - consumeOAuthState `false`. The state was not consumed, and the replay is `false`.
  - Sweep markExpired failure: all three windows still run and publish.
  - Sweep find(7d) failure: the 30d and 1d windows still run.
  - Sweep EXPIRED publish failure: alive, and every later step runs.
- **Head cells more permissive than the reference: 0.** `harness/summarise.js` flags verify or OAuth accepted, an OAuth replay accepted, a sweep that skipped markExpired or find steps, and a process death. The Up controls show that verify `true`, HIBP `true`, OAuth `true` (both GETDEL and MULTI) and the full sweep can all be detected.
- FOUND, base exposure (cells not equal to the reference):

  | Site | development | production |
  |---|---|---|
  | ACS (either path) | 6/19 reject: revokedProxy, messageGetterThrows, symbolMessage, messageToStringThrows, messageIsRevokedProxy, nullProtoMessage | 6/19 |
  | SMTP | 8/19 reject (the 6 above + null, undefined) | 8/19 |
  | verify, HIBP | 6/19 reject | 4/19 |
  | OAuth GETDEL, MULTI | 7/19 reject | 5/19 |
  | sweep markExpired, find(7d) | 7/19: the sweep aborts, later windows skipped | 5/19 |
  | sweep EXPIRED publish | 7/19: **process dies** (unhandled rejection, exit 1) | 5/19 |

  This is consistent with the author's 4/12 and wider.
- Logged text at head:
  - `'unreadable thrown value'` for a revoked Proxy, a throwing getter, a revoked-Proxy message, a null-prototype message or a message whose toString throws.
  - `"Symbol(g161)"`, `"10"` and `"[object Object]"` for Symbol, BigInt and cyclic or toJSON-throwing messages.
  - At the sweep and OAuth sites, `"undefined"` / `"null"` for an Error with no message. At the password sites the field is omitted, as at base.
  - At SMTP, `'unreadable thrown value'` for null/undefined (`error.message` throws), and `undefined` for a plain string.
  - Every changed site logs one line per failure event. OAuth logs 2 because the harness consumes twice, and EXPIRED logs 2 because there are two rows.
- TESTED: `harness/cell.js`, `harness/run_matrix.js` (860 cells, including 24 controls) → `logs/matrix_all.{json,tsv}` and `logs/summary.txt`.
- HOW:
  - The real base and head `password.ts`, `email.ts`, `oauthState.ts`, `issuerCertSweep.ts` and `utils/logger.ts` were extracted by blob. `logs/blobs.log` shows each blob sha equal to the extracted file's hash-object. They were transpiled verbatim (`harness/transpile.js`).
  - Replaced through `Module._load` only: argon2, global fetch, nodemailer, `@azure/communication-email`, `./session` (getRedisClient), `../events` (publishEvent), `../repositories/issuerCertRepo`, and `runWithPlatformScope` for the sweep.
  - Email uses the **real** `@secuura/shared` (allow-list). Winston and bcryptjs are the real ones from the clone's install.
  - The sweep runs through the real `startIssuerCertSweep(0)`, the production entry, so its outer `.catch` is the real one.
  - No process handlers are registered, so an unhandled rejection takes Node's default (exit 1), as auth registers none (grep: `unhandledRejection` / `uncaughtException` appear only in tests).

**G161-F2 (HIGH, PRE-EXISTING, base = head, not caused by this PR): the documented pen-test F-12 HaveIBeenPwned check is dead code.**
- FOUND: as in the question-1 section. `isPasswordBreached` has 0 callers at head and at develop, across every file type in the repository. The password.ts header lists it as remediation item 3 of "Pen-test F-12". Breached passwords are therefore accepted at register, reset and change-password (read: those routes call only `checkPasswordStrength`), and `HIBP_ENABLED` is inert.
- Its fail-open on a network failure (`false`) is base behaviour. This PR extends the same `false` to hostile thrown values, which made it reject at base. That is moot while the function has no caller.
- Rated HIGH because a security control documented as a pen-test fix does not run. If Kam treats F-12 item 3 as accepted residual, read this as MEDIUM. For a Kam card; not merge-blocking.
- TESTED: `logs/q1_grep.log`, `logs/q1_grep2.log`, and the recorder `hibp` / `hibpUp` cells.

**G161-F3 (INFO, positive, question 3): sendEmail `false` instead of a rejection. Head equals base-with-ordinary-Error at both routes, and closes a base existence oracle.**
- FOUND (`logs/route_compare.txt`), with the real base and head email.ts, the real router and the real error handler, and nodemailer's `sendMail` rejecting with each of 8 kinds plus none:

  | Route | base, ordinary Error | base, hostile (8 kinds) | head, every kind |
  |---|---|---|---|
  | POST /register | 201 + tokens; createUser, storeEmailToken, sendMail, createSession | **500 INTERNAL_ERROR after createUser + storeEmailToken were written**, no session | 201 + tokens; same 4 calls |
  | POST /forgot-password, existing account | 200 "If the email exists…"; storeResetToken, sendMail | **500** (reset token stored) | 200; same calls |
  | POST /forgot-password, unknown account | 200 | 200 | 200 |

- At base, a hostile send failure made forgot-password answer 500 for an existing account and 200 for an unknown one. An outside caller could read that difference. Head removes it.
- Register already reveals existence by design: 409 "Email already registered" (read, auth.ts:199-200). So register has no new oracle either way. At base the hostile 500 left an orphan user row plus a token the user could not use. Head carries on, exactly as for an ordinary Error.
- No status, stored row or call differs between head and base-with-ordinary-Error in any of the 27 route cells.
- TESTED and HOW:
  - `harness/g161-route-driver.test.ts`, run by `scripts/routes.sh`.
  - The driver was copied into the clone's `__tests__` for the run only, then moved out to `harness/_moved_out_of_clone/`. email.ts was swapped base, then head, then restored by `git checkout --`, and the clone was clean afterwards.
  - The mocks are those of the PR-adjacent `ks1868-auth-register-publish-event-unreadable-throw.test.ts`: userRepo, jwt, session, hashPassword, events and db.
  - Vitest rc 0 for both runs.

**G161-F4 (LOW, unchanged sibling site, not disclosed exactly): the ISSUER_CERT_EXPIRING_SOON publish `.catch` in the same sweep loop (issuerCertSweep.ts:127-133) is still unguarded. A hostile rejection there still crashes the auth process at head.**
- FOUND: path `sweepPubSoon`. Head **dies** (exit 1, unhandled rejection from inside the `.catch` handler) for 7 of 19 kinds in development and 5 in production. That is identical to base, so it is not a regression.
- The PR's README disclosure lists only "the two outer .catch handlers in startIssuerCertSweep" as uncovered. The flow fragment says "three in issuerCertSweep.ts (…, the event-publish .catch, …)" and "a failed event publish is a logged warning, not an unhandled rejection". That is true for EXPIRED only. There are two publish `.catch` handlers, and only the first was guarded.
- Reachability (read): the real `publishEvent` (`events.ts:124-152`) catches everything inside its own try and resolves, so in production neither publish `.catch` can fire today. Hence LOW.
- Suggest that the next KS-1868 pass, or held pass O89-P6, take the second publish catch, and that the fragment's wording be corrected.
- TESTED: the recorder (38 head cells, 12 DIED; base the same 12 kinds).

**G161-F5 (INFO, question 4): consumeOAuthState never accepts under a hostile value.**
- FOUND: in all 76 head cells (GETDEL and MULTI x 19 kinds x 2 formats), the result is `false`, the state was not consumed by the refusal (in the harness the stub throws before deleting), and the replay is `false`.
- The positive controls `oauthUp` / `oauthMultiUp` return `true` on first consume, then `false` on replay. So the instrument can see acceptance, and burn-on-use works.
- At base, 7 (development) or 5 (production) kinds made consume reject. The route then reached the generic error path (500, read). Head gives the authored 403 OAUTH_STATE_INVALID (read: `routes/auth.ts:1141-1143`).
- The only `true` path is `stored === provider` after a successful read. That path is unchanged.
- Mutant O3 (catch returns `true`) is killed by 9 tests and changes 76 of 76 recorder cells.
- I did not drive the route itself for OAuth.

**G161-F6 (INFO, question 5): the cert sweep has no path that leaves an expired cert valid beyond base-with-ordinary-Error.**
- FOUND: when `markExpiredCerts` fails, it is a single `UPDATE … RETURNING`, so the rows stay `active` at base and at head alike, until the next tick (6h). Head then runs all three expiring-soon windows. Base with a hostile value aborted them; base with an ordinary Error ran them.
- When `findExpiringSoon(7)` fails, head skips only that window, exactly as an ordinary Error does.
- When the EXPIRED publish fails, the flip has already happened (the events follow the UPDATE). Head warns and carries on. Base with a hostile value **killed the process**.
- Read, pre-existing: `routes/issuerCerts.ts:783-791` refuses an `active` cert whose `validUntil` has passed ("Awaiting next sweep tick"). So a missed flip does not let an expired cert sign at that route.
- I did not check every other consumer of `status='active'`.

**G161-F7 (LOW, test gaps): 24 of 28 mutants killed by the PR's 44 tests. 4 survive.**
- **E5** (`String(error.message)` → `String(error?.message)` at SMTP) and **P3 / P7** (`err?.message` → `err.message` at verify / HIBP) are text only. The recorder shows that only null/undefined log differently, and the state is unchanged. The tests have no null or undefined cell at those sites.
- **E7** (the ACS catch returns `true` instead of `false`): this is a **state** mutant. The recorder flags 76 of 76 cells: sendEmail claims delivery without trying SMTP, or with no provider at all. The tests survive it because the ACS cells assert only the final `true`, not that SMTP was called.
  - The `return false` line is not changed by this PR. Still, the PR's own RED R1-R3 claim "falls through to SMTP", and the tests do not check it.
  - Nice-to-have: assert the SMTP call in the ACS cells, and add null cells.
- Killed, and the recorder agreed:
  - E1-E4, E6 (SMTP rethrow: 5 tests, 38 cells)
  - P1, P2, P4 (verify returns `true`: 5 tests, 38 cells)
  - P5, P6, P8 (HIBP returns `true`: 5 tests), P9
  - O1-O4
  - S1-S7, plus S3 (markExpired catch aborts the sweep: 6 tests, 38 cells)
  - S8 (`continue` deleted: 5 tests; my recorder signature does not include the per-window counts, so it showed 0 differences)
- TESTED: `harness/mutants.py` → `logs/mutants.out` and `logs/mutants.json`.
- HOW:
  - Each mutant is one exact replace whose target lies within 700 chars after its anchor. Every mutant's distance was printed and checked first.
  - Each run executes the 4 new test files (vitest, cwd = auth, `--root` auth) and that file's recorder paths against `harness/build_mut/<id>`.
  - The mutated file is restored by `git checkout --` with the blob sha asserted. The clone is at head, with 0 status lines, at the end.

**G161-F8 (INFO, pre-existing, read and lint): residuals in the touched files.**
- `issuerCertSweep.ts:171-183`: the two outer `.catch` handlers are unguarded (disclosed by the author). They are unreachable from the body at head, because every body catch now resolves.
- `password.ts:65` and `email.ts:140`: `err?.message` in the argon2 loader catch and the ACS init catch are unguarded. That covers import-time failures only.
- `issuerCertSweep.ts:102`: eslint gives `no-useless-assignment` (warn) on `let rows = []`. The line is unchanged from base; the author linted only the test files.
- The email catches still write the recipient address in clear into the console line, as the author disclosed, unchanged. A PII candidate for the `pii` skill owner.

**G161-F9 (INFO, merge-tree): clean, exactly the PR's paths.**
- `git merge-tree --write-tree 19fc6830 1062b621` gives rc 0 and tree `95a5a72b`. The merged tree differs from develop in exactly the PR's 10 paths. The merge-base is 66cbe4e.
- base..develop is 1 commit touching 7 originate paths. None are under services/auth, and none overlap the PR. Head and the merged tree have 0 differences under services/auth.
- Control: base..develop does list 7 paths, so the overlap test could match.
- The PR shares no path with PR 1977 (db.ts, session.ts, their 2 tests and 2 `KS-1868-auth-session-db` fragments).
- TESTED: `scripts/mergetree.sh` → `logs/merge-tree.log`.

## Figures (re-measured; author's figure in brackets)

| Item | Result | Author |
|---|---|---|
| Red-first (4 base product files, 4 new tests) | 28/44 failed, all 28 by AssertionError: sweep 10/14, email 6/10, OAuth 6/10, password 6/10. The 16 controls are green. | [28/44, by assertion, 16 controls] match |
| New tests at head | 44/44 | [44] match |
| Auth vitest, head | 137 files / 1605 tests, 1603 pass, 2 fail (ks949-platform-admin-seed-identity, the 2 tree-walk cells, STACK_TRACE_ERROR) | [137/1605, 1603 pass, 2 fail ks949] match |
| Auth vitest, base 66cbe4e | 133 files / 1561 tests, 1559 pass, 2 fail (the same 2 ks949 cells) | [133/1561, 1558 pass, 3 fail] totals match; I saw 2 ks949 failures, not 3 (the flake class) |
| Test-types ratchet (check.cjs services/auth) | base 184 files (133 tests), 42 errors, 0 new, 0 stale, rc 0. Head 188 (137), 42/0/0, rc 0. A planted TS2322 in password.ts gave rc 1, "1 new". | [188, 42 baseline, 0 new, 0 stale; planted fails] match |
| tsc, service tsconfig, head | 0 errors | n/a |
| eslint, the 4 product + 4 test .ts at head | 0 errors, 1 warning (pre-existing, F8). A planted `debugger` and an unused const gave rc 1. | [0/0 on the 4 test files] match for the tests |
| docs-fragments check, head | rc 0, "lint clean, render passes html_docs_check". A planted unclosed `<div>` in the flow fragment gave rc 1; rc 0 after restore. The cheat ADVISORY at line 6235 is pre-existing (also seen at gate 160). | [OK, planted refused] match |
| Recorder | 860 cells; head = reference in 380 of 380 changed-site cells; 0 more-permissive cells | [12 values x 2 functions, 24 outcomes] holds, wider (all 8 sites) |
| Route driver | 27 cells per version; head = base-ordinary in 27 of 27 | [read, not run] now measured |
| Mutants | 28 run: 24 killed, 4 survived (F7) | n/a |
| Install (previous gate agent, verified from logs) | `npm ci --ignore-scripts` rc 0, 1798 packages; packages/shared built, rc 0 | n/a |

## NOT TESTED

- Node 24 or any LTS Node (host v26.8.1 throughout).
- A real argon2, HIBP, ACS, SMTP, Redis or Postgres, or a real client producing a hostile value. Reachability is read only: argon2, fetch, pg and ioredis reject with Errors, and the real publishEvent never rejects.
- The OAuth callback route itself (the 403 is read from `auth.ts:1141`), and the change-password route.
- A booted auth service, or any deploy. The four platform suites.
- Whether consumers other than `routes/issuerCerts.ts:786` re-check `validUntil` on an `active` cert (F6).
- The pen-test report itself: whether F-12 item 3 was accepted as residual (F2).
- The held Spark-pass byte equality (O84-P1, O84-P3, O85-P3) and the email golden diff. I did not have the pass files, so these were not compared.
- docs-fragments `check` on the merged tree, and `check --committed`.
- The other KS-1868 sites.

## Housekeeping

- Every write stayed in this workdir: `repo/`, `harness/`, `scripts/`, `logs/`, and `verdict.md`. `evidence/` holds the author's file, untouched. The runners were anchored: vitest `--root` auth with cwd auth via spawnSync, tsc `-p`, and eslint with an explicit cwd.
- The Blockchain checkout was touched only by read verbs (`ls-remote`). No fetch was needed, and the clone's origin is still the local checkout path.
- The clone is at the PR head `1062b6212`, `git status` is clean, and every product-file swap was restored by `git checkout --` with the blob asserted.
- No files were deleted. The temporary route driver was moved to `harness/_moved_out_of_clone/`, and mutant builds are kept under `harness/build_mut/`.
- All background jobs have finished. `ps` shows no process with `gate161` in its command line.
- Nothing was written to any Secuura repo, board, ticket or GitHub.
