GATE B1661: GO WITH FINDINGS @ c47a68b on main ca795fb

Gate G1 (Opus) for lane NX-AUTH, RD-999 (the product owner's 2026-11-17 ruling, option a). Branch b1657/nexusai-nx-auth-session-own-entry = c47a68b5380389c0c1842bcdd2d3cdc91d760fcd. Main ca795fb853cf8f79a38aee7683a29b060fd11810, re-read at 11:38:39 by gh api at 11:10 and by ls-remote at 11:38 (unchanged). Clocks AEDT 2026-11-17, 11:09-11:40. Scratch /private/tmp/b1661-gate/: clone with push URL invalid://no-push, never pushed; trees main0 / fin14 / plant27, slot 4 by the kit's program (controls b1657-nodot/old51 -> 16 and b1652-nodot/old1 -> 15).

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor | The kit's literal planted revert (own-entry line alone removed, P1L) turns only U2b and U7 red. The shape check still refuses every inherited value on its own, so U1, U2a, H1-H3 and H5 stay green under P1L. The full revert of the guard (own-entry line AND shape check removed = main's lookup, P1F) turns all 10 changed-behaviour cells red and keeps the 6 pins green. The builder disclosed this as Q1/C6 and measured the same. This is defence in depth, not a vacuous test. | Accept. Future kits: predict the planted revert against the whole guard. |
| F2 | Minor | Merge commit M 3a9cc04f keeps git's default subject, "Merge remote-tracking branch 'origin/main' into b1657/nexusai-nx-auth-session-own-entry", so a build number (lower-case branch name) enters main's history on landing. The kit prescribed the default subject; no name, secret or card id. | Accept for this landing. Future kits: give M an explicit subject without the branch name. |
| F3 | Minor | The new suite drives POST /api/chat with `constructor` only (H5). The gate drove all 12 names, `prototype` and 5 JSON forms on chat over HTTP (all 401 at head). | Optional follow-up: widen H5 to the FORMS loop. Not blocking. |
| F4 | Info | At head a JSON-array cookie wrapping a REAL token (`j:["<admin token>"]`) is refused (401/302). At main it signed in as that admin. This is an intended tightening (the `typeof` string check, kit D3); no real client sends that form. | None. Mention it in the release note if desired. |
| F5 | Info | The builder's STATUS (Corrections C5) reports that 2_Project_Files' repo-local core.sshCommand names a stale volume, and that the push printed a pre-existing Dependabot alert 145 (low). Neither is in this lane. | Tuesday to route both separately. |

No Blocker, no Major.

## Measured (each with its control)
- **Refs.** Branch at origin = READY sha (gh api ref + ls-remote). Open PRs 0 (control: closed list prints rows). compare main...head: ahead 5, behind 0. Changed paths 3 of 3 OWNS: backend/jsonStorage.js +15 -2, the new test file +320, scripts/verify-expected-counts.json +3 -3. NX-T2 not launched (heads/b1654 0; control heads/b1652 1).
- **Merge.** `git merge-tree --write-tree origin/main head`: clean, tree b0f77b17 = head tree (main is an ancestor, rc 0). M 3a9cc04f: parents K 5b2dcaed + ca795fb8. `merge-tree K ca795fb8` conflicts in scripts/verify-expected-counts.json ONLY. M's counts blob = main's 73d9a052. M vs main differs only in the two code paths, each blob = A2's. K' changes only the counts file.
- **server.js** blob bf648e29 at ed3b1aed, main and head: equal.
- **Other readers of the session store by a request value** (git grep at head, backend + scripts): getSession callers server.js :2709 :2871 :2945 :3075; updateSessionActivity :2741 (own-entry check already); deleteSession :3081 (rebuild-without-key). sessions.json is otherwise named only in customerDataFiles.js and dataExport.js, which list or redact the whole file and do no lookup. None outside the three store methods.
- **HTTP, gate's own probe** (/private/tmp/b1661-gate/tools/probe.js; `node backend/server.js` of the tree outside the harness on 127.0.0.1:10140-10143; model endpoint :10149 unbound; NODE_ENV development; sign-in enforced, zero-GUID Entra ids, aiEnabled; seeded by the tree's own JsonStorage with HOME/DATA_DIR set before the require; each server stopped by its pid; 10140-10149 0 listeners before and after). 18 forms: the 12 runtime Object.prototype names (= the drafter's 12), `prototype`, j:["constructor"], j:["toString"], j:"constructor", j:"__proto__", j:{}. Routes: /api/auth/check, /api/printers, /api/stats, /api/auth/users, /index.html (manual redirect), POST /api/chat with CSRF. Full table: http-table.txt.
  - main, no stored user (control, bypass shown): 12 names + j:["constructor"], j:["toString"], j:"constructor", j:"__proto__" -> 200 (check authenticated=true,user=null) / 200 / 200 / 403 / 200 page / chat 200. `prototype` and j:{} -> 401 SESSION_EXPIRED / 302.
  - main, stored users: the same 16 forms -> 500 AUTH_ERROR on all four APIs and chat, 302 page. 96 "Authentication middleware error" lines (TypeError toLowerCase).
  - head, both states: all 18 forms -> 401 SESSION_EXPIRED on the four APIs and chat, 302 /login on /index.html. Never 200, never 500. 0 auth-error lines.
  - Sessions file sha256 unchanged across the 18-form block and the controls, in all four servers.
  - Real sessions (stored users) main vs head: admin, viewer, no-cookie and unknown-cookie rows identical (admin 200 everywhere; viewer 403 on /api/auth/users). Expired session -> 401 SESSION_EXPIRED and removed from the file in both. Final file shape identical (keys ADMIN, VIEWER; lastActivity stamped ISO in both).
  - The server logs at head carry no cookie value (`__defineGetter__` / `propertyIsEnumerable` 0 each; positive control: toLowerCase 96 in main-U's log). 429s 0.
- **Jest** (one lock acquisition, tag qa-b1661-gate, 11:16:26-11:38:32; load1 6.98 at 11:14:17 and 4.47 at 11:16:21; NODE_OPTIONS unset; --maxWorkers=2; EADDRINUSE 0 in every run; slot-4 band 22560-23199 empty before and after):
  - Red-first at main (new file copied in untracked, cmp equal): 16 cells, 10 failed (U1 U2a U2b U6 U7 H1 H2 H3-N H5-N H5-U), 6 pins passed.
  - Head: 2 runs, 16/16 green each.
  - Plants in plant27, each reverted by blob (hash = head blob; porcelain empty after): P1L (kit literal) red U2b U7 only (F1); P1F (full guard removed) red the same 10 as red-first, pins green.
  - Inventory `--check` at head: rc 0, "runtime rows 203; committed rows 203", "route set equal" (unchanged). backups/ none.
  - Plain verify at head (fin14, porcelain empty before and after): `VERDICT: PASS - 5862/5862 tests passed across 377 suites (jest exit 0)`, rc 0, EADDRINUSE 0. The committed pair 5862/377 equals the measured pair.
- **Local CodeQL** (2.27.4, javascript-typescript, both suites, threads 2, outside the lock; rows compared by (rule, file, line text)): security-extended main 29 / head 29, new 0, gone 0. code-scanning main 4 / head 4, new 0, gone 0. Control: comparing different suites reports 25 new. Local main 29 = hosted open on main 29 by (rule, file, line); all hosted rows at commit ca795fb8; control: drop one hosted row -> only-local 1.
- **Scans** over 338 added lines and the 5 commit messages:
  - Names: underscore-aware, the scanlib1114.py:20 literals + the gh login and its prefix + the standard ban list, 14 patterns, 0 hits. Control: planted `_by_<name>_` fires 14 of 14; longer words do not fire.
  - Non-ASCII 0, Cf 0 (control 1). Card / decision ids 0 (control 1). B-number in added lines 0; in messages 1, which is F2 (control: planted B1657 fires).
  - Hand CodeQL rows (new RegExp, innerHTML, child_process, eval) 0 (control fires). No Python.
  - gitleaks over the diff and over `log -p`: no leaks. Control: an AKIA-shaped string reports 1.
  - Identity: every new commit author = committer (email length 46).
- **Deploy demo:**
  - The merge WILL start it: it changes backend/** and __tests__/**, and paths-ignore covers only **.md, docs/**, tests/**.
  - Both jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'` (deploy-demo.yml :53 and :91). Repo Actions variables 0, organization variables 0 (gh api, 11:14). So its jobs would read skipped. The last run, on ca795fb8 (43965977070), completed skipped.
  - .github diff vs main empty.
- **RD-999 done-when:**
  - 1: met (head N table).
  - 2: met (head U table, 401 never 500).
  - 3: met (real-session rows identical, expiry and removal identical, file bytes unchanged by refused lookups).
  - 4: met (red at main, green at head, red under the full planted revert, verify PASS 5862/377, CodeQL 0 new).
  - 5: this gate. Nothing is deployed.

## Builder STATUS claims (graded)
- True, measured by the gate:
  - The getSession patch text.
  - server.js blob equal.
  - Callers :2709 :2871 :2945 :3075.
  - M = clean merge whose only conflict was the counts file, resolved to main's blob.
  - K' 5862/377 and the final PASS.
  - Red-first: 10 red / 6 green.
  - Mutation matrix P1(full) / P1a / P3 as received (P2 not re-run by the gate).
  - Inventory 203/203.
  - CodeQL main 29/4 = head 29/4, 0 new.
  - Diff = exactly the OWNS paths.
  - Identity equal.
  - No PR and no merge.
- Not shown by the gate (accepted as claims): the four lock acquisitions and their clocks; the A/A2-level CodeQL vs ed3b1aed; the related-set run (86 suites / 1470 cells); P2.

## NOT RUN
- Hosted Build, Gitleaks and CodeQL on the PR and on the merge commit. These are the deciding checks; they run after the PR is opened.
- Node 24 and Linux. Local is node v26.13.0 on macOS arm64; CI is Node 24.
- The related set and P2 (the builder's claims; the plain verify covers every suite once).
- Any hosted host. No hosted read of whether an instance is in the "enforced, no stored user" state.

Fences kept: no push, PR, merge, Jira, mail, board, az or hosted HTTP; no cd; no rm (dry scratch moved to /private/tmp/b1661-gate/_quarantine); writes only in this folder, /private/tmp/b1661-gate/ and the jest lock (one acquisition, released, waiter rc 0).
