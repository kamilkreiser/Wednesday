GATE B1724: GO WITH FINDINGS @ 34bcd31 on main 220485e

Gate G1 Tier 1 (Opus 5.5), independent of the builder. Head 34bcd31769e121c489294f03b3602c90bad668e6, main 220485eaef52541dcfa24e6409412b03edb6b8a5 (ls-remote equal at 01:20 and again at 01:51 AEDT, Thu 19 Nov 2026; clocks from `date`). Work folder /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/g1724/ (own clone, push URL set invalid, never pushed; trees head13, base32, vfy7 in jest slot 11 (band 27040-27679) and mut10 in slot 18 (band 31520-32159), printed by `worktreeSlot()`; no kit of 18 or 19 Nov names slot 11 or 18). One lock acquisition (tag b1724-gate, acquired 01:26:56, released 01:50:59). The lock wrapper's rc 1 comes from the chain's last command, an `lsof` that found no listener, and not from a failed step.

## Ruling (READ verb only)
`decision_queue.sh show nexusai-audit-entry-limits-994-1118`: status ruled, project Datasec/NexusAI, choice b, label "Refuse the request instead", detail "Same limits; the user sees an error", ruled 2026-11-18 08:36:52. The BLUF names email 254, name 256, address (URL) 2048, lists 50 items. No committed text gives the product owner any default. Commit A's body names every default (status, wording and shape, wrong-type refusal, other numbers, place before the admin checks, rememberMe) as "this change's defaults, not decided". See F2 for the block comment.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (Q-6, judged) | 400 before 403. The guard answers before the routes' own admin checks. A signed-in non-admin who pads a field gets 400, not 403, and no REQUEST_DENIED 'forbidden' row is written. Measured: viewer add-user with a 300-char name gets 400 at head and 403 at base. Viewer entra-config with 60 keys gets 400 at head and 403 at base. Viewer add with an ordinary value stays 403. N7 is green at head and red under plant P1: the STATE_MUTATION row holds status 400 and there is 0 REQUEST_DENIED rows. What the caller learns: only the fixed limits, which are public in source. The answer never repeats the request. No action is taken and no capability is gained. Padding does let a detection rule that keys only on REQUEST_DENIED miss a non-admin's failed attempts on these 13 routes. Those attempts could not have succeeded anyway, and the STATE_MUTATION 400 row still records them. Open (no sign-in) shape: anonymous add and update of users answer 200 at base and at head (pre-existing open-mode behaviour). The guard only adds refusals there (300-char name 400, 51 domains 400, 300-char login email 400). It never widens what a caller can do. | KEEP. Tell whoever owns audit detection to also key on STATE_MUTATION rows with statusCode 400 on these paths from a non-admin. Named alternative: one inline check call after each handler's admin check (about 13 insertions inside handlers, a re-gate, every handler's error path touched). It is not worth it for a monitoring-only residual. Tuesday's reasoning holds: a copy of the several setup-mode-aware admin gates in the guard would risk diverging from them. |
| F2 | Minor | The frozen block comment says "the status code, the wording, the answer's shape and every number below are this change's defaults". That also calls the four ruled numbers defaults (under-attribution, the safe direction). It does not name the wrong-type refusal, rememberMe or the guard's place. The test header omits rememberMe. Commit A's body is complete and exact. | Land as is (the block is frozen text measured byte-equal). The PR and merge bodies written here state the split exactly. |
| F3 | Minor | In the H cells, `effectDone` is measured only for H5 and H6. For the other ten it is the constant false. Their proof is status 400, the exact text and `rowHoldsValue`. Plant P1 turns all 12 H cells red, so none is vacuous. | No change. |
| F4 | Observation (pre-existing, not this lane) | Builder's Finding 1 is confirmed at BASE. `/api/auth/login` is not in `alwaysPublicPaths` (backend/server.js:2214). In the enforced shape an anonymous POST to it is answered 401 'Authentication required' by the sign-in gate, at main and at head alike (an ordinary email, and a 300-char email). In the open shape the route is reached: 300-char email gets 401 'Invalid email or password' at main and 400 'Email too long (max 254 chars).' at head. | Not this lane's fix. Tuesday to decide whether password sign-in is meant to be unreachable when sign-in is enforced. |
| F5 | Observation (pre-existing) | POST /api/auth/users with an unparsed body type (`application/merge-patch+json`, `application/vnd.api+json`, `text/plain`) answers 500 'Failed to add user', at main and head alike. The handler destructures an undefined body. | Follow-up ticket (answer 400, not 500). Not this lane. |
| F6 | Minor (process) | The builder took two lock acquisitions (STATUS Correction 8, from the rd765-766 STOP that ANSWER-1 resolved). It ran one `git reset` in a scratch worktree, in breach of HOLD 6 (Correction 1). Both are disclosed and have no product effect. | None. |

No Blocker, no Major.

## Measured rows
1. SCOPE. `rev-list --left-right --count main...head` = 0 4. `diff --numstat`: backend/server.js 97/0, __tests__/rd994-audit-field-guard.test.js 518/0, __tests__/rd765-766-linear-text-patterns.test.js 2/2, scripts/verify-expected-counts.json 3/3: exactly four paths.
   Per commit: A ff74310 is server.js 97/0, T 696148d is the new file 518/0, T2 eb31506 is rd765-766 2/2, K 34bcd31 is the counts 3/3.
   Head blob of server.js is df442bc8ca1153bf8361f422a450a7913b20c6b7 (equals Tuesday's). The difflib opcodes of main against head are two inserts only, at main 2800 (94 lines) and at main 2807 (3 lines), with no replace or delete. So auditLog, AUDIT_ACTIONS, every call site and every handler are byte-unchanged.
   Block BEGIN..END is 93 lines (server.js:2801-2893), sha256 of the lines with newlines is f0bc2a77b68d4743, and it is byte-equal to the kit's frozen text (control: one byte changed gives a5222b75...). Non-ASCII characters in server.js: 1256 at main and 1256 at head.
   rd765-766 diff: only the HTTP cell's title words ("is refused by the length check, fast") and its `attack` pair `[400, 'Email too long (max 254 chars).']` changed. `plain`, `attackUnder2s` and the FAIL comment are unchanged, as ANSWER-1 allows.
   `merge-tree --write-tree main head` is clean, and its tree 43b72644b978 equals the head tree. The only other b17/b18 head at origin (b1716) is an ancestor of main.
2. ORDER AND BYPASS. `app.use(requireAuth);` is at server.js:2896, `app.use(afterAuthGate);` at :2901 and `app.use(auditFieldGuard);` at :2904. The first table route is at :3088. No table path is registered before :2904. Only per-prefix limiters sit there (:1387, :1404, :1405). The counts of `app.all(`, method override, `req.url =` and `query parser` are all 0.
   The live probes below ran in my own trees inside the lock: an enforced-shape server and an open-shape server, with raw sockets so that nothing normalises the request. Each probe gives head status, then main status. "Effect" means the user was stored or the audit row held the marker. All path and body probes went to POST /api/auth/users as admin with a 300-char name.
   - Path variants:
     - `/API/AUTH/USERS`, `/api/auth/users/`, `/Api/Auth/Users/`, absolute-form `http://localhost:<port>/API/auth/users` and `?x=1`: head 400 'Name too long', main 200 with effect.
     - `//api/auth/users`, `/api/auth/%75sers`, `/api/auth/users;x`, `/api/auth/users//` and `/api/auth/users%20`: 404 at both. The route does not match, so the handler did not run.
     - `/api/auth/x/../users`, `/api/auth/./users`, `/api/auth/users/.` and `/api/auth/users%2F`: 400 from rejectDotSegments at both.
   - Methods:
     - HEAD callback with an 8193-char description: head 400; main 302 with a row holding it.
     - `X-HTTP-Method-Override: PUT` on a POST to /api/auth/users/<addr>: 404 at both (not honoured).
     - Override GET on a PUT: head 400; main 200.
     - Lower-case `post` and `pUt`: refused by Node's HTTP parser (400 or a reset) at both. The handler never runs.
   - Bodies:
     - urlencoded body, JSON with `; charset=utf-8`, `APPLICATION/JSON`, a JSON duplicate key (the last wins and is checked), a percent-encoded form key `%6eame` and a JSON-escaped key `name`: head 400 'Name too long'; main 200 with effect.
     - A form field twice, `name[]=` and `name[a]=`: head 400 'Name must be text.'; main 200 with effect.
     - A nested object and a top-level array: 400 'Email, name, and password are required' at both. The route does not read the nested value.
     - `+json`, `vnd.api+json` and `text/plain`: 500 at both (F5); the body is not parsed and no value is stored.
     - A JSON `__proto__` key holding a long name: 200 at both, with the short own `name` stored. JSON.parse makes an own key, so the long value is never read.
   - Callback queries:
     - `error` twice: head 400 'Error must be text.'; main 302 with the row.
     - `error[]=` and `error[a]=`: 302 no_code at both. The simple parser keeps the bracketed key, so the route never sees it and no row holds it.
     - `%65rror=` with 2000 chars: head 400 'Error too long'; main 302 with the row.
     - `error_description` twice: head 400 'Error_description must be text.'; main 302 with the row.
     - Upper-case path: 302 to /login at both. requireAuth's public-path match is case-sensitive, so the gate redirects first and no row is written.
   - Params:
     - Double-encoded (`%2561` x100, which decodes once to 300 chars): head 400 'Email too long'; main 404.
     - An encoded slash: refused before routing at both.
     - DELETE with `%61` x255: head 400; main 404.
     - PUT /api/data-sources/<200 chars>: head 400 'Id too long (max 128 chars).'; main 404.
     - A long or short malformed escape: refused before the handler at both.
     - PUT on an existing user with a 300-char name, in lower case and with `/API/auth/USERS/<addr>/`: head 400; main 200 with the name stored.
   RESULT: no probe reached a guarded handler at head with a value the table refuses. In every case where main stored the value or wrote a row, head answered 400.
3. Q-6: see F1 (Minor, keep).
4. NO REFLECTION, NO THROW. The probe markers sat inside refused values, and none appeared in any head response (reflected=false on all 59 enforced probes and 8 open-shape probes). Keys `__proto__`, `constructor`, `toString` and `valueOf` in the user-add body answer 200, the same as main. The value `name: {toString: <marker>}` gets 400 'Name must be text.'. The entra-config body with the keys `__proto__`, `constructor` and `toString` answers 200 at both. A login `email: '__proto__'` with `rememberMe: 'constructor'` gets 400 'RememberMe must be true or false.'. `additionalDomains: {length: 100, 0: x}` gets 400 'must be a list of text'. No probe produced a 500 at head that main did not also produce.
   Timing: entra-config with 100,000 keys (1.29 MB) got 400 in 50 ms end to end at head (main 200 in 64 ms). In the vm, the guard's `Object.keys` over 100,000 keys took 7.4 ms, and 1000 checks of a 50-key body took 1.1 ms in total. 1,000,000 keys (13.9 MB, under the 50 MB limit) got 400 in 293 ms at head (main 200 in 728 ms). A user-add body with 10,000 extra keys checks in 0.02 ms (vm), because the loop runs over the rule's fields only.
   The only `try` in the block is around `decodeURIComponent` (backend/server.js:2838). A throwing getter given to the check propagates out of it ('getter' rethrown), so a fault surfaces as a 500 and never as a silent pass.
5. LOGIN ROUTE. Confirmed pre-existing at BASE: F4.
6. CELLS. The new file at head ran twice: 111/111 green each time (jest JSON).
   Plants in mut10, each applied with a match count of 1 and reverted by writing the HEAD blob back, with `hash-object` equal to df442bc8ca11 proved after each:

   | Plant | Change | Cells red |
   |---|---|---|
   | P1 | mount removed | C1, C2, N7 and all 12 H cells (H1 H3 H4 H5 H6 H9 H10 H11 H12 H13 H15 H16); U and N1-N6 green |
   | P2 | `>=` on the string limit | 26 AT-LIMIT cells, N2 and U-PARAM |
   | P5 | lengthOnly removed | U-R15-F1-TYPE and N4, plus rd516-ai-test-ssrf R17 (30/31) |
   | P6 | `error_description` 1024 | U-R02-F2-LONG, U-R02-F2-AT-LIMIT, U-HEAD, N3 and H4, plus rd799-log-injection-auth-and-storage CAP-500 (22/23) |
   | P7 | request-side case fold removed | U-PARAM only |

   Each equals the builder's STATUS matrix. N7 measures the Q-6 residual (row 3).
7. FULL VERIFY at head in vfy7 (tree 43b72644b978, porcelain empty before and after, band 0 before and after, `env -u NODE_OPTIONS`, `npm run verify -- --maxWorkers=2`) printed `VERDICT: PASS - 6009/6009 tests passed across 380 suites (jest exit 0)`, rc 0, EADDRINUSE 0, 0 FAIL lines. The committed pair 6009/380 equals the measured pair, which equals 5898 + 111 tests and 379 + 1 suites. Load1 ranged 4.8 to 6.4.
8. CODEQL (local CLI 2.27.4, javascript, my own databases of main and head).
   - `javascript-code-scanning.qls`: 4 rows on main, 4 on head, 0 new.
   - `javascript-security-extended.qls`: 29 rows on main, 29 on head, 0 new, 0 gone.
   - The three `js/http-to-file-access` rows (on backend/jsonStorage.js, backend/services/emailService.js and backend/server.js, the shape of alerts 235-237) are present on both. None is claimed closed.
   - 0 rows in the guard region or in either changed test file.
   - Hand rows over the 620 added lines found no `RegExp(`, `eval(`, `new Function`, `innerHTML`, `child_process`, timer token or skip/only/each marker (the planted `setTimeout` control fired). There is one `vm.runInContext`, in a test only (the rd477 form).
9. TEXT. The 620 added lines and the 4 commit messages:
   - ASCII only: 0 non-ASCII and 0 dotted quads.
   - Ban-list names 0: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, plus the scanlib list. The `_by_<name>_` control fired for all of them, and "kamera" does not fire.
   - B, N and seat ids 0 (control fires). Card, decision-queue, "Tuesday" and "owner" words 0.
   - Attribution lines read only "The ruling chose to refuse ... with the limits named for it" and "... defaults, not decided".
   - gitleaks over `git log main..head` (4 commits): no leaks. A planted AKIA control reported 1 leak.
   - Author and committer are the project's configured identity on all four commits, the same as main's recent commits (not printed).
10. DEPLOY. The merge touches backend/** and __tests__/**, and deploy-demo.yml path-ignores only `**.md`, `docs/**` and `tests/**`. So a Deploy demo run will start on main. Its jobs are gated on `vars.CI_DEPLOY_ENABLED` and must read skipped (landing.txt step 4).

## Builder STATUS claims
These claims are true, as measured above:
- A is +97/-0, the block sha matches and the blob matches.
- 111 cells are green twice.
- The P1, P2, P5, P6 and P7 matrix rows are as claimed.
- N7 shows STATE_MUTATION 400 and 0 REQUEST_DENIED.
- Finding 1 (login not public; pre-existing).
- 6009/380 PASS, EADDRINUSE 0.
- C3 census 1/2/3/42 (C3 green).
- ANSWER-1 scope.

These are not shown by me: the 67-reader per-file equality, H2's 500 at base, H14's dropped status, P3, P4, P8 and P9. The full verify covers every reader.

## FOUND / TESTED / NOT TESTED / HOW
FOUND: no bypass and no reflection. The guard fails closed (no try). The scope and the frozen block are exact. One Minor design residual (F1, keep), one Minor text under-attribution (F2), one Minor partly-constant field (F3), two pre-existing observations (F4, F5) and process notes (F6).
TESTED: everything in rows 1-10, at head and at main, inside one lock acquisition.
NOT TESTED:
- hosted Build on Node 24 (this box runs Node 26.13.0)
- hosted CodeQL on the merge commit
- Linux
- the Deploy demo run a landing starts (it must read skipped)
- any hosted instance
- the export in the open shape: rows read empty there at both main and head, so open-shape probes are judged by status only
- the AUTHENTICATION_FAILURE row content for the open-shape login
- a browser render (no page changed)
HOW: own clone and worktrees under the work folder. A raw-socket probe test file was kept untracked in head13 and base32 and never committed. Plants were written by plant.js with asserted counts. One chain under `nexusai-lock.sh jest b1724-gate` printed `lsof` of both bands before and after (0 listeners each time). Logs and JSON are in out/.
