GATE B1647: GO WITH FINDINGS @ 0dc6a0d on main dcac002

Tier G1 (Opus), independent gate of B1633 (NexusAI lane NX-S2, storage-family CodeQL), branch `b1633/nexusai-nx-s2-storage-family-codeql`.
Clocks AEDT 2026-11-16: start 22:50:46; jest lock `qa-b1647` held 23:02:14 to 23:24:52 (one acquisition, released); main re-read 23:25:03.
Work folder `/private/tmp/b1647-gate/` (own clone, push URL `invalid://no-push`, nothing pushed). Every number below was printed by a program in that folder.

## Refs, merge, scope
- `git ls-remote`: branch = `0dc6a0d32e068002793af9044aa7fbb95d16d4ba` (= READY sha); main = `dcac002d31e1360e9b8d4a4933670a7ac6ce445c` at 22:50 and again at 23:25 (main did not move).
- 8 commits on BASE, each author = committer: A 928ad47c, B 2cc526e8, C 636d2cde, D 6415a211, C2 f8d34918, D2 755abda7, E 04516baf, K 0dc6a0d3.
- `git diff --stat main head`: 13 files, +1291 -54. Every path is in OWNS-B1633 (13 of 15; F's two paths are absent, as Q3 NO requires). Outside OWNS: 0. Part 8 paths (server.js, serverGuards.js, encryptionService.js, customerDataFiles.js, static/, routes/, docs/, workflows): 0.
- C2 changes only `__tests__/rd767-check-then-write-races.test.js`; D2 changes only `__tests__/rd421-sentinel-machine-id-follows-store-dir.test.js`. Both files were created by C and D (name-status per commit).
- `git merge-tree --write-tree main head`: rc 0, tree `87c1cf53d297` = head tree (main is an ancestor; the merge is main plus the head blobs).
- Overlap: open PRs 0 (gh api GET). Sibling lane NX-P (B1634) OWNS shares only `scripts/verify-expected-counts.json`; no `b1634*` ref at origin.
- Deploy demo: `on: push: branches: [main]`, `paths-ignore` `**.md`, `docs/**`, `tests/**`. The merge changes `backend/**`, `__tests__/**` and `scripts/**`, so **it WILL start Deploy demo**. Both jobs are gated `vars.CI_DEPLOY_ENABLED == 'true'` (lines 53, 91); repository variables read 0 (gh api GET `actions/variables`: total_count 0) and the last three main pushes (dcac002d, d83eab99, d1152289) concluded `skipped`. Its jobs should read skipped; C-224 demo hold: nothing deploys. Workflow file unchanged by the branch.

## CodeQL (CLI v2.27.4, run by the gate, both suites, BASE and head from `git archive`)
| suite | BASE | head | gone (rule, file, statement text) | new at head |
|---|---|---|---|---|
| javascript-security-extended | 47 | 33 | 14 | 0 |
| javascript-code-scanning | 15 | 8 | 7 | 0 |
- Gone (extended): js/polynomial-redos intentRouter.js:90, queryPreprocessor.js:155, :157, :167, :168, ticketStore.js:63; js/file-system-race costCentreMap.js:72, jsonStorage.js:263, :307; js/prototype-polluting-assignment jsonStorage.js:4054; js/remote-property-injection jsonStorage.js:4061, marketplaceStore.js:118, :146, validators.js:280. That is every row the kit names for RD-766, RD-765, RD-767 and RD-769.
- Still open, moved only: js/http-to-file-access (#235) jsonStorage.js:491 -> :524; js/insecure-temporary-file (#112) :2600 -> :2642. #113/#236 emailService.js:168 and #147/#148/#149 emailService.js:387/:393 are unchanged (Part 6 and Part 7 are read-and-report only).
- Instrument control: BASE local rows equal the hosted open rows on main (47 rows, 43 distinct (rule, file, line) triples on each side; only-local 0, only-hosted 0).
- These are local results. CodeQL on the merge commit decides each ticket. An alert that is absent on the PR head does not prove it is fixed.

## Tests
- **Red without the fix:** the five new files were copied untracked into a BASE tree (`cmp` equal) and run with jest inside the lock. 54 cells: 24 RED, 30 GREEN. RED by file: rd766 7 (2 fuzz TypeErrors because the helpers are absent, 3 attack cells at 1533-1833 ms against a 250 ms bound, 2 source cells), rd765 2 (attack 1672 ms against 500, source), rd767 3 (source only), rd421 4 (stray file, HMAC binding, second boot, source), rd769 8 (3 session globals, 2 marketplace, 3 source). The pins are GREEN (equivalence tables, ordinary-bytes tables, reload and machine-id scenarios). Every new file has at least one red cell at BASE.
- **Head:** the same 5 files, 54/54 green (jest JSON: 12/6/14/7/15).
- **Plain verify at head = merge tree** (slot 6, `npm run verify -- --maxWorkers=2`, 23:02:52 to 23:24:40): `VERDICT: PASS - 5828/5828 tests passed across 374 suites (jest exit 0)`. The counts file at head reads 5828/374. EADDRINUSE 0, porcelain 0 after.
- **Inventory `--check` at head:** rc 0, `runtime rows 203; committed rows 203`, `route set equal`. BASE gives the same lines. No route, status or handler-gate change.

## Probes
- **RD-766 linear (in-process timing, node 26):** BASE `preprocessQuery` gives 1000 chars 1.6-1.8 s and 2000 chars 10.8-12.6 s over 6 whitespace shapes (tabs, spaces, NBSP, `i`+tabs, `a`+tabs, tabs only). BASE `matchKnownQuestion` gives 11.2-11.9 s at 2000. The BASE negation strip gives 127-190 ms at 16,000 (quadratic). Head over 11 shapes x 3 functions at 1,024,000 chars: max 199 ms, and the time doubles with the length (64,000 -> 1,024,000 is about 16x). Head at 2000 chars: 0.0-0.7 ms.
- **RD-766 equivalence (the gate's own generators; oracle = BASE module loaded beside head):** 200,000 free-form cases with 0 mismatches over preprocessQuery, _stripBenignNegation and matchKnownQuestion. 300,000 grammar-shaped cases with 0 mismatches (prefix fired 187,703, suffix 179,470, strip 61,149). Controls: two planted one-token changes in scratch copies were caught (2,069 and 895 mismatches in 20,000 cases).
- **RD-765:** old pattern vs `isPlausibleEmail`: 600,000 cases (two generators, 21,579 accepted), 0 mismatches. The 80,005-char attack takes 1745 ms with the old pattern and 0.02 ms with the helper.
- **RD-421 (DATA_DIR unset and set; two boots in the same directory; BASE->BASE, BASE->head, head->head; a temp HOME):**
  - Explicit dir, DATA_DIR unset: BASE writes a stray `home/data/.machine-id` and binds the sentinel to it. Head writes only `store/.machine-id` and binds to it. The ticket's defect is gone.
  - Explicit dir, DATA_DIR set: identical in all three pairs (intact).
  - Default store (DATA_DIR set) BASE->head: intact.
  - Server shape (DATA_DIR unset, resolve once and pass) BASE->head: intact.
  - Only the explicit-dir-with-DATA_DIR-unset shape, BASE->head, reads `sentinel-invalid` once. Only scripts and tests build that shape: `git grep` finds no `new JsonStorage(` outside `__tests__` besides `server.js:4332` and `:4847`, which pass the resolved directory. `BACKLOG.md:16` documents this symptom.
  - `/var/lib/printer-dashboard` was absent before and after.
- **Scans:**
  - Name scan, underscore-aware (scanlib names plus the standard's ban list): 0 over 1291 added lines and every message. Controls: a planted `_by_<name>_` fires for every name; `kampala` does not fire.
  - B-number, seat and card ids: 0 (controls fire).
  - Secrets and hosts: gitleaks over `git log -p main..head` found no leaks (control: AKIA-shaped plant reports, rc 1). Tenant ids and hosts: 0.
  - Non-ASCII introduced: 0. Bidi and zero-width in added lines: 0. Repo-wide hidden-character scan of tracked files: BASE 5 files, head the same 5 files, no difference.
  - CodeQL hand rows over added lines: `new RegExp(var)` 0, eval/Function 0, child_process template 0, innerHTML 0, hand-escape 0, timer and skip tokens 0. chmod hits: 4 in test files, modes 0o000, 0o700 and 0o600 (owner-only, JavaScript, and the head analysis found no new row).
  - Ticket keys in added lines and messages: RD-240, RD-421, RD-765, RD-766, RD-767, RD-769 (all on HOLD 19's list).

## Builder claims graded
| claim | grade |
|---|---|
| 8 commits, 13 files +1291 -54 | true |
| counts 5774/369 -> 5828/374 | true (plain verify PASS at the committed pair) |
| CodeQL extended 47 -> 33, code-scanning 15 -> 8, new rows 0 | true |
| C2/D2 change only their own new test files (amend forbidden) | true |
| inventory 203/203, route set equal | true |
| red-first 24 red / 30 green, head 54 green | true |
| linear readers and identical answers (RD-766), identical email language (RD-765) | true (gate's own timing and fuzz) |
| RD-421 reproduces at BASE, fixed at head, server/default HMAC unchanged | true |
| getSession FINDING (viewer with no stored user, 500 with one; head removes only the pollution) | true, now measured over HTTP (F1) |
| Step 1c(i) "/api/chat: a model-free drive is not established; NOT TESTED over HTTP" | false: the route answers 200 model-free over HTTP on a local server (F2), so an HTTP cell was possible |

## Findings
| id | severity | finding |
|---|---|---|
| F1 | security, pre-existing (not introduced, not worsened) | Reserved session cookie passes requireAuth. See section F1. |
| F2 | ticket, pre-existing (the branch removes the polynomial part) | Chat message length still unbounded. See section F2. |
| M1 | Minor | Commits C and D do not stand alone green under jest; C2 and D2 fix the cells. The landed history keeps two red intermediate commits (bisect only). Disclosed by the builder. |
| M2 | Minor | The RD-767 race fix is pinned only by source cells (at BASE only the 3 source cells are red). The EEXIST-meanwhile path is NOT TESTED; the builder disclosed it. |
| M3 | Minor | The builder's claim that /api/chat is not drivable over HTTP is false (see the claims table). The HTTP cell the kit asked for when the route is drivable is missing. |
| M4 | Minor | rd766's "filler prefix" attack cell is slow at BASE because of the suffix step, not the prefix read (disclosed). The prefix reader's linearity rests on the fuzz and the source cell. The gate's timing confirms it independently. |
| M5 | Info | A sentinel written by BASE for an explicit directory with DATA_DIR unset reads `sentinel-invalid` once under head. Only scripts and tests build that shape (see RD-421 probe). |
| M6 | Info | recordEvent answers "duplicate" for an operation id that is an inherited name, so such a webhook event is never processed. Pre-existing; the builder reported it. |

## F1 (MEASURED over HTTP): a reserved session cookie passes requireAuth
Instrument: `node backend/server.js` booted locally on 127.0.0.1:10110 (BASE tree) and :10111 (head tree):
- `NODE_ENV=development`.
- Fresh DATA_DIR and HOME under `/private/tmp/b1647-gate/http/runs/`.
- Model endpoint pointed at 127.0.0.1:10119, where nothing listens.
- Seeded through the tree's own JsonStorage: `authEnforced` true, `firstRunComplete` true, Entra ids zero-GUID, `aiEnabled` true.
- A `-r` preload writes, on SIGUSR2, what the built-ins carry.

Cookies sent: none, an unknown token, `__proto__`, `constructor`, `toString`, `prototype`. Server logs name only localhost URLs.

| state | cookie | BASE | head |
|---|---|---|---|
| enforced, NO stored authorized user | none / unknown | 401 / 401 | 401 / 401 |
| same | `__proto__`, `constructor`, `toString` | **200** on /api/auth/check (`authenticated:true,user:null`), /api/printers, /api/stats; 403 on admin /api/auth/users; POST /api/chat 200 | **identical (200 / 403 / chat 200)** |
| same | `prototype` | 401 | 401 |
| enforced, ONE stored user (admin) | `__proto__`, `constructor`, `toString` | 500 AUTH_ERROR on every route | 500 AUTH_ERROR on every route |
| any state, after the requests | built-ins | BASE: `Object.prototype.lastActivity`, `Object.lastActivity` and `Object.prototype.toString.lastActivity` SET (every `{}` carries lastActivity), in both enforced states | head: none set |

Reading: getSession (`jsonStorage.js`) reads `sessions[cookie]`, which returns the inherited built-in for these three names. Its `expiresAt` is undefined, so `new Date(undefined) < now` is false and the session is never expired. With an empty authorized-user list, `getAuthorizedUser(undefined)` returns undefined and requireAuth assigns role `viewer`. With a stored user, `undefined.toLowerCase()` throws and the request gets 500.

The state is reachable in the product:
- The enforce route (`server.js` about :3943) checks only the Entra configuration.
- The first Entra sign-in adds its user (`server.js:3384`).
- So every deployment passes through enforced auth with an empty list, between enforcement and the first sign-in.
- The same holds if the authorized-users file reads empty.

In that window an unauthenticated client with the cookie `session_token=constructor` reads viewer data and drives the chat. The head removes only the pollution half; the bypass is unchanged at head.

**Recommendation: SECURITY CARD for the product owner** (an authentication bypass to viewer level on a reachable state), plus a ticket for the fix:
- getSession reads only an own entry and refuses a session without a string `email` and a valid `expiresAt`.
- The same applies to the other `getSession` callers: `server.js:2871`, `:2945`, `:3075`.

The fix is outside this lane's files and must not be folded into this landing.

## F2 (MEASURED over HTTP): chat-length hold, and whether /api/chat needs sign-in
Instrument: the F1 servers, plus an open-mode seed (`aiEnabled` true, auth not enforced). POST /api/chat with a CSRF token from /api/csrf-token and the body `{message: <N tabs>+"x"}`. A concurrent GET /api/health every 100 ms measures how long the whole server is blocked. No model call is made (the answer is the rule path's "I'm not sure how to interpret").

| reachable WITHOUT sign-in? | BASE | head |
|---|---|---|
| open mode / first run (auth not enforced), no cookie | yes (chat 200) | yes (chat 200) |
| enforced, no cookie | no (401) | no (401) |
| enforced, no stored user, cookie `constructor` (F1) | yes (chat 200) | yes (chat 200) |
| enforced, a stored user, cookie `constructor` | no (500) | no (500) |

| message | BASE request / health blocked | head request / health blocked |
|---|---|---|
| 1,000 tabs + x | 4416-4992 ms / 4366-4941 ms | 8-14 ms / 0 ms |
| 2,000 tabs + x | 30111-33177 ms / 30061-33125 ms | 8-10 ms / 0 ms |
| 100,000 tabs + x | not run | 62-73 ms / 14-22 ms |
| 1,000,000 tabs + x | not run | 506-622 ms / 454-570 ms |
| 10,000,000 tabs + x (20 MB JSON) | not run | 4840 ms / 4799 ms |
| 20,000,000 tabs + x (40 MB JSON, under the 50 MB limit) | not run | 8762 ms / 8619 ms |

Reading:
- At BASE one 2,000-character message holds the only event loop for about 30 s, and the whole server (health included) waits.
- The head makes the hold linear: 2,000 chars in about 10 ms.
- Nothing bounds the message: a 40 MB body under the 50 MB limit still holds the server for about 8.8 s at head. Part of that time is the body parse and the route's other passes, not this lane's readers.
- Reachable without sign-in in open mode, and through F1 under enforced auth with no stored user.

**Recommendation: TICKET.** Bound /api/chat's message length and the JSON body limit for that route; the product owner decides the bound. Raise it to a security card only together with F1, which is what makes it reachable under enforced auth.

## NOT RUN
- Hosted Build. It is the deciding check and is Tuesday's; the local plain verify is not hosted CI.
- CodeQL on the PR and on the merge commit (hosted). Main's analysis decides every ticket.
- Node 24 (this machine runs node v26.13.0), and Linux.
- `node scripts/assert-browser.js`. It reads no changed file; the builder ran it with rc 0.
- npm-audit and arm-ttk workflows (no package or template change).
- The Deploy demo run a landing would start. It should read skipped.
- A full verify at BASE. The branch's red-first ran at BASE; main's own verify is the counts pair 5774/369.
- An HTTP drive of the RD-765 ticket intake (/api/support/ticket).
- The legacy system machine-id source (/var/lib, absent here).

## Disclosures
- The jest lock was taken ONCE (`qa-b1647`, 0 s wait, load1 5.09 at 23:00:07 and 4.35 at 23:02:10). The lock's command was a hold script that waited for a release file. The gate's jest runs, the verify, the server boots and the inventory check ran inside that hold; the lock was released at 23:24:52.
- The verify ran in tree `/private/tmp/b1647-gate/head` (slot 6, band 23840-24479), the red-first in `base2` (slot 10, band 26400-27039), and the HTTP probes in a separate head tree `hprobe` on ports 10110-10112. `lsof` read 0 listeners in each band and in 10110-10119 before and after. Every server was stopped by pid.
- The test harness and jest wrote their own temp directories under os.tmpdir().
- One gate probe file was placed in this folder before the verify ended and then moved to `/private/tmp/b1647-gate/quarantine/` (never deleted), so that a re-commission check does not read a draft as a verdict.
