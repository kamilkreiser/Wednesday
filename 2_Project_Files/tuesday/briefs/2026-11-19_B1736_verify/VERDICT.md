GATE B1736: GO WITH FINDINGS @ f06b080 on main 295f989

Gate G1 Tier 1 (Opus 5.5), independent of the builder: every row below was measured by this gate, at source.
- Head f06b080e3ffce9f6be869e66eb7b0e6ab0dac1d5. Main 295f989ec26f926d5f00c5ad3d58a56d2a405fa8. The branches API (14:05:37) and `ls-remote` (14:44:04) both read these. Thu 19 Nov 2026, clocks from `date`.
- Open pull requests: 0.

Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s292/g1736/`:
- My own clone, with its push URL set to `invalid://no-push`. It was never pushed.
- Trees `wt10` (head), `wt76` (main), `wt80` (plants) and `wt86` (verify). All four are jest slot 17 (band 30880-31519), printed by `worktreeSlot()` in each tree. Control: the builder's `b1733-nodot/old2` reads 5.
- No brief of 18 or 19 Nov names slot 17. The commission's list is 5, 11, 12, 13, 14 and 18. A grep of the B173x briefs finds only slots 5 and 13.
- `node_modules` is an APFS clone copy of the builder clone's install. `package*.json` is unchanged from 46050e25 to head (`diff --stat` is empty).

One lock acquisition: tag `b1736-gate`, acquired after 0 s at 14:14:31 and released at 14:43:18. `NODE_OPTIONS=unset` was printed. The band read 0 listeners before and after every step.

## Ruling
None is cited from the product owner, and none is needed.
- Scan: every commit message and every added line, with the regex `product[ -]owner|owner's ruling|owner ruled|ruled by` plus the name list. Result: 0. A planted control fires.
- The open window is the project rule C-01/C-178. The gate comment says "as on the sibling writers". No text attributes a choice to anyone.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (RD-990, new with this change) | `requestPath` takes the path part of `req.originalUrl`. That value is the request target as sent, so it can carry text the router never treated as path. Two cases were measured at head with raw HTTP. (a) An absolute-form target `http://gate-evil.invalid/api/feedback/zzabs1` writes REQUEST_DENIED and STATE_MUTATION rows with path `http://gate-evil.invalid/api/feedback/zzabs1`. On main the row read `/zzabs1`, and a plain route keeps `/api/admin/incidents`. A signed-in requester can therefore put a host-looking string of its choice into the path field. (b) A raw `#` in the target: `/api/feedback/zzfrag#rd990probe=q` is recorded with `#rd990probe=q`. Main recorded `/zzfrag`. The query-string exclusion splits on `?` only. Neither case loses the true route: it is still in the row. Browsers never send either form. | Not a landing blocker. Follow-up (the records pass can ticket it with RD-990): take the pathname, for example `require('parseurl').original(req).pathname` or `new URL(req.originalUrl, 'http://x').pathname`, and add two cells for these shapes. |
| F2 | Minor (follow-up severity, as asked; not fixed here) | The two routes left out still dial with the stored credential for a viewer. Measured at head: `POST /api/data-sources/:id/test` and `POST /api/setup/data-sources/:id/test` each answer the viewer 200. Each made one connect attempt to the sign-in host (`login.microsoftonline.com:443`), which the harness fence refused. The bodies carry the connection diagnostics: an error text, `AUTH_FAILED`, troubleshooting text. The same holds for two GET reads not on the pending list: `GET /api/data-sources/:id/discover-tables` (1 connect) and `GET /api/data-sources/:id/describe-table` (3 connects). The viewer's `GET /api/data-sources/:id` returns the stored tenant id but not the secret. No data changes. The setup `/test` route sits behind the fixed limiter of 5 per 10 minutes. | Follow-up ticket at **Medium**. It should cover the two `/test` routes AND the two dialing GET reads (discover-tables, describe-table), which the RD-793 pending list does not name. |
| F3 | Minor (stale text in a file this lane edits) | `__tests__/rd988-feedback-triage-admin-only.test.js:25` (the header comment) still says "backend/server.js holds 30". The kit's frozen rewrite moved only the title (`:234`) and the assertion (`:249`) to 34. | A one-word fix in a later lane. Not a landing blocker. |
| F4 | Minor (process, no effect on the product) | The builder's Corrections are judged as follows. **3 acquisitions:** the causes named are true. The first was the builder's own judge bug; the second was main moving on HISTORY.md, which HOLD 20 meant to be handled inside the same acquisition, but `mainmove-last` stopped the chain instead. Effect on the product: none. **Stray `cd` in a subshell:** true; no effect. **`reset: moving to HEAD`:** written by `git worktree add <path> <branch>`, which populates the new tree by an internal hard reset. Reproduced in my clone: a new branch worktree's reflog reads `HEAD@{0} 295f989 reset: moving to HEAD` over the creation entry. In the builder's `wt` reflog, `HEAD@{8}` and `HEAD@{7}` are the same sha 46050e2, so nothing was lost. **Files read by section:** true. Effect on the product: none, since every product claim was re-measured here. | None. |
| F5 | Observation | Three test-shape notes. (a) The rd793 file writes the body key as a quoted `'authMode'`. It is a request field the product requires, not a sensitive value, and quoting it only avoids a hand scan's identifier row. (b) rd990 waits on the audit rows with the harness `sleep(50)` in a bounded loop of 100. (c) The committed inventory's `meta.originMain` reads 46050e25, not 295f989e. It is the tool's own value: rows and fence are equal to my drive at 295f989e. | None. |

No Blocker, no Major. CodeQL rc 0.

## Measured rows
1. **SCOPE.**
   - `rev-list --left-right --count main...head` reads 0 7. `diff --numstat main head` lists exactly the ten paths with the commission's counts: server.js 14/2, accessAudit.js 11/2, capabilities.js 1/2, rd988 2/2, rd978 5/3, role-capabilities.json 6/6, ROLE-CAPABILITIES.md 8/8, rd793 307/0, rd990 221/0, counts 3/3. Counts 6041/382 become 6086/384.
   - Head blobs: server.js 668e343f3207, accessAudit.js d36cf0c717ab, capabilities.js 1c58b35ad9e6, rd988 60150600ae3b, rd978 ca45a65f2d8a. All equal Tuesday's.
   - The `diff -U0` hunks of server.js are exactly the kit's six: `-462 +462`, `-556 +556`, `-15947,0 +15948,3`, `-16010,0 +16014,3`, `-16031,0 +16038,3`, `-17565,0 +17575,3`. The hunk headers name only the require line, `auditMutationMiddleware` and the four data-source handlers. No other route is touched.
   - RD-994 block (AUDIT-FIELDS-BEGIN..END, starting at line 2810): sha256 prefix f0bc2a77b68d4743 at 46050e25, at 9df7d423, at ae20b99f, at main 295f989e and at head. Control: one flipped byte gives d736d855f5611553.
   - Merge M: `diff --stat K M` = HISTORY.md only (+19), and `diff --stat 46050e25 295f989e` = HISTORY.md only (+19). `merge-tree --write-tree main head` = 7d4516cff6ab, equal to the head tree, so the merge is clean.
   - `routes/entraProvisioning.js` is untouched: `diff --stat` is empty and `:167` still reads `path: req.path`.
2. **RD-793 REFUSAL.** These are live probes from my own untracked probe file. One enforced boot per tree seeds an administrator, a viewer and a non-administrator `finance` user (a role from `ROLES`). Every attempt is made on a fresh real source, and its effect is read back by the administrator before and after.
   - Shapes tried, 54 per actor: per route the canonical path; upper and mixed case; a trailing `/` and `//`; `%`-encoded letters and digits; `%2F`; a leading `//` and an inner `//`; `/./` and `/x/../`; `;x`; `%20`; a leading zero; a query. Plus the `X-HTTP-Method-Override`, `X-HTTP-Method` and `X-Method-Override` headers, `?_method=` on POST and GET, PUT, PATCH, HEAD, OPTIONS and a lower-case method.
   - **Head: 216 attempts (viewer, finance and anonymous), 0 changed a source.** The canonical path and every variant that reaches the handler answer 403 `{"error":"Admin access required"}`. Variants that miss the route answer 404. Dot-segments and `%2F` answer 400 from the path guard. Anonymous gets 401 or a 302 to /login. HEAD and OPTIONS are reads (200 or 404, no effect).
   - **Main (control): 8 changes.** The viewer and the finance user each changed a source through the four canonical paths.
   - Administrator control at head: the canonical path and the upper-case variant each changed their source (8 of 8). So the effect read can see a change, and a case variant reaches the same handler.
   - Sign-in configured with `authEnforced` false: at head the viewer gets 403 on all four, the administrator 200, anonymous 401. On main the viewer added a table.
   - Sign-in not configured with first run done: anonymous adds a table at head and at main. This is the C-01/C-178 open window, unchanged.
   - RD-535 window: my live boot did NOT reach the unproven state. The marker is ignored while the settings hold tenant and client, and the boot behaved as enforced. So the live probe of this window is NOT RUN. Unit read at head with no server: `adminGateRefuses` returns true with `signInUnproven` for an administrator and for an open-looking store (`authEnforcement.js:644`), and the global gate answers 503 in that state. The rd535 suites passed in the full verify.
3. **LEFT-OUT ROUTES:** see F2. Measured at head and at main, with the same answers at both.
4. **RD-990.**
   - The rd990 cells hold. The six keys are kept in every row of my probe: 20 rows at head, 20 at main.
   - Below no router the row keeps `req.path`: `/api/admin/incidents` and `/api/settings/costs` are equal at main and head.
   - The `?` query is absent from every row whose target carried it after a `?`.
   - Shapes tried:
     - An encoded `%3F` stays path text at both (`/zzq%3F...` on main, the full path at head). Not new.
     - A 6000-character id records 6020 characters at head against 6007 on main. The RD-994 guard bounds fields, not the audit path, both before and after: pre-existing.
     - Upper-case `/API/FEEDBACK/x` records the sent case.
     - A double slash answers 404 with the full path at both.
     - The absolute-form and `#` shapes are new: see F1.
5. **INVENTORY.** Measured inside the lock.
   - `--check` at head: rc 0, `runtime rows 203; committed rows 203`, `route set equal`.
   - `--generate` at head and at main into scratch: rc 0 each, `backups/` empty before. The 2 files each drive created were MOVED to the quarantine folder, and porcelain is 0 after.
   - Head drive against committed head JSON: 0 rows differ, and only `generatedAt` and `originMain` in meta.
   - Drift D (main drive against committed main JSON): 0 rows, meta `generatedAt` and `originMain` only.
   - Main drive against head drive: exactly the four rows differ, each in `statusByMode` (viewer only: 404/400/404/404 become 403), `gateInHandler` ([] becomes `["requireAdminFor"]`) and `capability` ("administrator only (viewer refused); handler gate: requireAdminFor"). Row order is kept. The two `/test` rows are unchanged (viewer 404, gate []). The fence is equal.
   - The committed page equals the tool's render, apart from its generated-at line.
6. **CELLS.**
   - At head (new-1 and new-2): rd793 28 of 28 and rd990 17 of 17 passed, twice. `EADDRINUSE` 0.
   - Plants in `wt80`, each reverted by copy and its blob proved equal to HEAD. Received colours (all as the kit predicts):
     - P0: 0 red over the two new files plus rd929, rd988, rd978 and rd932-unit.
     - P1: V1 E1 C1 C2, plus rd988 T7 and rd978 "the review's probe".
     - P2: V2 E2 C1 C2.
     - P3: V3 E3 C1 C2.
     - P4: V4 E4 C1 C2.
     - P5: U2-U5, H1-H4, M1-M3.
     - P6: M1-M3 C1.
     - P7: U5 H1-H4 C2.
     - P8: C3 plus the rd929 PENDING_GATE cell.
     - P9: U1 plus rd932-unit U2.
   - No asserted field is a constant written on both sides. D and O read the expected value from the committed inventory, and V, E and A are per request.
   - Census by my own grep: the only files that send DELETE or `/tables` on data sources are rd793, rd994 (a unit call of the guard), rd978 (route names in a list) and rd800 (the open-window caller). No other test pins `requireAdminFor(` 30 (the one `toBe(30)` elsewhere is a file count in rd429) or the six-route pending list. One stale comment: F3.
7. **FULL VERIFY** (`wt86` at head, tree 7d4516cff6ab, porcelain 0 before and after): `VERDICT: PASS - 6086/6086 tests passed across 384 suites`, rc 0, 14:20:50 to 14:42:42. The pair is equal to the committed 6086/384. `EADDRINUSE` 0, band 0 before and after.
8. **CODEQL** (my clone as `--checkout`, base 295f989e, head f06b080e, 14:11:48 to 14:13:16, `cq.err` empty):
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
rc=0
```
   Hand rows over the added lines: `RegExp(` 0, timer tokens 0, skip/only/each 0, `child_process` 0, `innerHTML` 0. The only new name holding a sensitive word is the quoted `authMode` key (F5).
9. **PROCESS:** see F4.
10. **TEXT.** Over the 7 commit messages and all added lines:
    - names 0 (13 names: the standard list plus the 4 literals of scanlib1114.py:20; the `_by_<name>_` controls fire; longer words do not);
    - B-numbers 0, card or decision ids 0, product-owner attribution 0, non-ASCII 0, bidi or zero-width 0, dotted quads 0 (each control fires);
    - ticket keys: RD-793 and RD-990 in the messages; RD-958, RD-964 and RD-968 appear only in the existing rd978 history comment.
    The builder STATUS holds 0 dotted-quad strings (255 lines).

## Builder STATUS claims
- **True as measured:** blobs, hunks, ten paths, RD-994 prefix, counts 6086/384, verify PASS, drift D 0, the four-row inventory diff, cells 28 and 17 green, the mutation matrix, CodeQL rc 0.
- The builder's CQ-2 was against base 46050e25; mine, against the PR's real base 295f989e, also reads rc 0.
- **Not shown:** none material.

## Landing notes
- Merge commit, head-pinned, never squash (CLARIFICATIONS:2067 as relayed). The `landing.txt` here gives the steps.
- `backend/**` is not path-ignored by deploy-demo.yml (it ignores only `**.md`, `docs/**` and `tests/**`). So the merge starts a Deploy demo run, whose build and deploy jobs are gated on `vars.CI_DEPLOY_ENABLED` and must read skipped.
- LANDING HOLD 23 stands: the branch carries Tuesday's defaults (Q-1 to Q-9 in the kit STAMP).

## TESTED / NOT TESTED / HOW
- **Tested:** everything in rows 1-10.
- **NOT tested:**
  - the RD-535 unproven window as a live boot (unit only, see row 2);
  - hosted Build and hosted CodeQL;
  - Linux;
  - a hosted instance;
  - the production setting;
  - the first-run wizard in a browser;
  - the Deploy demo run a landing starts;
  - CodeQL on the merge commit (the open alerts on server.js move down by the inserted lines);
  - Node 24 (local node v26).
- **HOW:** git read verbs and `gh api -X GET` only against the project and origin. Every write verb ran in my clone. All jest runs and servers ran under one lock acquisition.
- **Gate's own deviation:** my first probe run wrote its observation file to the same name as the jest JSON, which overwrote it. The two probes were re-run by steps appended to the running gate script, inside the same acquisition (14:42:42 to 14:43:18).
