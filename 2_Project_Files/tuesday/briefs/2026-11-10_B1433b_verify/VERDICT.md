GATE B1433b: GO WITH FINDINGS @ 725dcf0 on main 849b808

Subject: branch `b1433/nexusai-b-learning-manager-log-lines` of datasecau/Reporting_Dashboard_Au, head `725dcf0ed76572af8773685769e5e5f1414745b2` (RD-798 remainder). Main read fresh: `849b808c567e4d31d78e2d50b582540ae1920c67` (HISTORY.md only since the branch base `3929b794`). Re-commission: the earlier gate for this branch died about 19:44 and left nothing here. Its scratchpad files are cited below ONLY as RELAYED context. Every result in this verdict comes from my own runs.
Verifier: read-only to origin. Own clone in the session scratchpad (push URL `INVALID-NO-PUSH`, repo-local deploy key), with worktrees main, head, merge, stack and red. No path has a dot component. No push, PR, Jira, mail or `az`. Every jest run went through `nexusai-lock.sh` (tags `qa-b1433b-gate`, `-red`, `-full`, `-tgt`) with `--maxWorkers=2`. No lock was broken.

**BLUF: 0 Blockers, 0 Majors, 5 Minors.**
- Paths: 2 of 2 are inside OWNS-B. Overlap with open PRs and sibling lanes is 0.
- Merge: clean, and equal to main plus the head blobs.
- Red-first: all 5 predicted cells fail at the base blob. The 3 controls hold. A one-slot mutant is killed.
- Suites: main's full suite PASSES (5493/326). The two suites that load `learningManager` read the same at head and merge: +8 names, 0 removed, 0 outcome changes.
- NOT RUN: the full verify at head, merge and stack. Load1 stayed 14-28, mostly Spotlight (`mds`, `mdworker`), after main finished. I released the lock rather than hold it idle. The PR Build check (full `npm run verify`) is the proof.
- Deploy: the merge WOULD start a `Deploy demo` run. Its jobs would read skipped.
- Counts: the landing counts depend on landing order (F1).

## RD-798 alerts by number (code-scanning GET on refs/heads/main, 250 alerts, 72 of them js/log-injection)
The 44 numbers come from RD-798's description list, RELAYED from `NexusAI/1_Project_Definition/Briefs/2026-11-09_B1375_STATUS.md:29`. Jira is fenced to this gate. Each number's state was read by me.
| group | alerts | state on main |
|---|---|---|
| fixed at the earlier log-sinks landing (2026-11-08) | 162, 163, 187-207, 222, 223 (25) | 25 fixed, backend/server.js |
| fixed before that | 172-186, 220, 221 (17) | 17 fixed, backend/server.js (12 on 2026-10-20, 5 on 2026-11-06) |
| **addressed by this branch** | **152 (learningManager.js:125), 153 (learningManager.js:153)** | **2 open** |
Total: 44 distinct. After this branch, 0 of the 44 stay open by code, if CodeQL closes 152 and 153. That read is main's analysis at the merge commit, after landing, and is UNMEASURED here. Open js/log-injection on main overall: exactly these 2.

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | `refs/heads/b1433/nexusai-b-learning-manager-log-lines` = 725dcf0e | `git ls-remote`; control main = 849b808c |
| 2 | Commits | 1 commit, parent 3929b794, tree d783697e | `git log --format='%H %P'` |
| 3 | OWNS-B | 2 of 2: `backend/learningManager.js` (M +5 -2), `__tests__/rd798-learning-manager-log-lines.test.js` (A +125, `+new rd<N>-*`, N=798 in QUEUE, absent at base) | fnmatch program over the kit's OWNS-B block. Controls refused: server.js, ticketStore.js, riskAlertScheduler.js, lane T's `rd798-log-injection-chat-and-learning`, rd999, counts file |
| 4 | Overlap | open PRs 0; 4 `b1431/*` and 2 `b1432/*` on origin, plus the other b1433 heads (csp on origin; 4 local-only builder heads): intersection 0 each | `gh api pulls?state=open` (control closed per_page=3 -> 185,184,183); `comm` of name lists (control self = 2) |
| 5 | Merge | `merge-tree --write-tree 849b808c 725dcf0e` rc 0, tree 220990a9. Vs main: only the 2 head paths. Vs head: only HISTORY.md (main's blob be99ded8). learningManager b511f617 = head, test 6e08d346 = head | `git diff --name-status`, `rev-parse <tree>:<path>` |
| 6 | Landing form | merge commit: the last 5 first-parent commits on main have 2 parents | `git log --first-parent --format=%p` |
| 7 | Deploy demo | WOULD trigger: `deploy-demo.yml:26-32` push to main, paths-ignore `**.md`, `docs/**`, `tests/**`; `backend/` and `__tests__/` not ignored. Jobs `build` (:53) and `deploy` (:91) gated on `vars.CI_DEPLOY_ENABLED == 'true'`. Repo variables total_count 0. Last 5 push runs `skipped`. **Jobs would read skipped.** File unchanged main vs head | `git show`, `gh api actions/variables`, `.../deploy-demo.yml/runs` |
| 8 | Full CI at main | `node -c` not re-run separately (they are syntax checks of files this branch does not touch). `npm run verify -- --maxWorkers=2` at main 849b808c: `VERDICT: PASS - 5493/5493 tests across 326 suites`, 01:42-02:02 | own run, jest JSON kept |
| 9 | Targeted at main/head/merge | suites loading learningManager: main 1 suite / 64 tests pass; head and merge 2 / 72 pass. Main->head: +8 names (all in the new file), 0 removed, 0 outcome changes. Head->merge: 0/0/0 | own runs, name/outcome diff by program |
| 10 | Red without the fix | base blob a6b5ab41 planted (`hash-object` equal). The new file reads **5 failed (B-125, B-153, B-SEP, SHAPE x2), 3 passed (C-PLAIN, C-STORE, C-SHAPE)**. Restored by blob, `git diff --quiet` rc 0, 8/8 pass. Mutant M1 (description slot unwrapped only): B-153, B-SEP and SHAPE fail; B-125 passes, as predicted | own runs 01:22, jest JSON per cell |
| 11 | Closed lines | RD-798 alerts 162-223 subset: fixed (table above). The other 42 of the 44 read fixed by GET | code-scanning GET |
| 12 | Probes (node) | hostile query/description CR/LF, NEL+U+2029, ESC, object whose toString has LF: main writes a line break on 3 of 6 cases, head 0 of 6. A 600-char query is cut to 500 plus a marker at head (F2). null description prints `null` at both | `scratchpad/g/bin/probe.js` vs wt-main / wt-head |
| 13 | Name scan | added lines 0, commit message 0, account login 0 | `(?<![A-Za-z])<name>(?![a-z])` re.I over the 9 names. Controls: planted `_by_<name>_` fired 9/9; longer words 0; `\b` form on `_by_kam_` = 0; login control 1 |
| 14 | Secrets / ids / hosts / Cf | GUIDs 0 (control 1); hosts 0; secret-shaped 0 (control 1). Cf/Cc in added lines 0. Non-ASCII only U+2192 (the arrow already in the log text). gitleaks over the branch commit rc 0 (planted `ghp_` control rc 1). Repo-wide Cf scan over tracked text: main = merge (5 files / 5 chars, same list) | `scan.py`, `gitleaks git`, `cfscan.py` |
| 15 | CodeQL pre-scan | added lines: `new RegExp(<var>` 0, hand-escape `.replace(/[...]/g,"\\$&")` 0, innerHTML 0, child_process 0. The test's `/\$\{([^}]*)\}/g` is a literal | regex over added lines; control `new RegExp(x)` fires |
| 16 | Counts | committed 5493/326; measured at main 5493/326. The branch adds 8 tests / 1 suite (row 9) | `git show :scripts/verify-expected-counts.json` |

## Findings
| ID | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor (landing precondition) | The counts this landing needs depend on order. **Landing before csp-intake:** 5501 tests / 327 suites, and a counts commit on 725dcf0 merges clean. **Landing after csp-intake (3a5d3444, 5513/327, the order ADDENDUM-2 names):** a counts commit cut on 725dcf0 CONFLICTS with main (`scripts/verify-expected-counts.json`). The branch must first take main by a forward merge (no rebase). Regeneration is then expected to read **5521 / 328**. Both pairs are predicted from measured parts (main 5493/326; +8/+1; csp 5513/327). The full verify that would print them was NOT RUN | simulated counts commit, `merge-tree` rc 0 onto 849b808c, rc 1 onto main+csp; control: the branch without a counts commit onto main+csp rc 0 |
| F2 | Minor | logSafe's 500-character cap now applies to both lines, so a long learned query or description is cut in the log with a `...[+N chars]` marker. The stored value is unchanged (C-STORE). No cell pins this. Intended by logSafe's design, so it is a note, not a defect | probe P3: head line 547 chars, main 634 |
| F3 | Minor | The 44-alert membership is RELAYED (B1375 STATUS read of the Jira description), not re-read in Jira by this gate | fence |
| F4 | Minor (claims) | Builder's full-suite PASS 5501/327 at head is not shown to me (row 8: NOT RUN). The partition row "not computed" is stale (now 0, row 4). "Needs 5501/327 at landing" holds only if this branch lands before csp (F1) | below |
| F5 | Minor (process, builder's own record) | The builder ran single-file jest without the lock (its Corrections) | STATUS Corrections |

## Builder STATUS claims (graded)
| Claim | Grade |
|---|---|
| head 725dcf0e, `HEAD^{tree}` d783697e | true |
| learningManager.js +5 -2; new test +125 | true (numstat) |
| 5 cells RED at base (B-125, B-153, B-SEP, SHAPE x2), green at head; 3 controls green at both | true (row 10) |
| +8 tests, 0 removed | true (row 9) |
| full suite from non-dot path PASS 5501/5501, 327 suites | not shown (full head run NOT RUN); counts consistent with row 9 + row 8 |
| alerts 152/153 open on main | true |
| name scan 0, gitleaks rc 0, inside OWNS-B, no skip/only/todo/.each/timer/dependency | true (rows 3, 13-15; `package*.json` unchanged) |
| pushed, ls-remote = head | true |
| partition vs other lanes "not computed" | stale: computed now, 0 |
| needs its own counts commit at landing, 5501/327 | true only if it lands before csp-intake (F1) |

## Tier
The kit has no S8 tier slot. Its line 4 leaves the post-branch gate to Tuesday (G1/G2). The change is security-adjacent (log-injection hardening) and only narrows output. No finding is a leak or a new exposure. I raise no tier-1 item.

## NOT RUN
- `npm run verify` at head, merge and stack (main + csp + head), with and without `--update-counts`. Load1 stayed at 14-28 from non-jest processes after main's run. I released the lock (02:02-03:24) instead of holding it against the queue. The PR's hosted Build check runs the full verify and must read VERDICT: PASS on the counts commit.
- `node -c` x3 and `npm run lint` at head/merge (the branch does not touch the three checked files; lint is a placeholder).
- Hosted CodeQL (UNMEASURED; main's analysis after landing decides 152/153). Hosted gitleaks full scan, npm-audit, arm-ttk (no `package*.json` or `azure-marketplace/**` change).
- Jira (fenced); the 44-alert list is RELAYED.
- RELAYED context only, not used as evidence: the dead gate's scratchpad red-first JSON (15:25, same blobs) agrees with row 10.
- Local node v26.13.0; CI pins node 24.
