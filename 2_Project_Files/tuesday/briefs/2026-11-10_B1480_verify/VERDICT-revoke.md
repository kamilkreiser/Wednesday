GATE B1480-revoke: GO WITH FINDINGS @ 5fbad1b on main 849b808

Branch `b1480/nexusai-s-session-revocation-clarification`, head `5fbad1ba3ff9a13f6ee86f069b1c732b3db7b3d2`, parent `3929b794` (independent of the stack). Tickets RD-972 (a user update that changes role, active state or password now ends that user's sessions), RD-976 (confirm-clarification no longer throws on an undeclared name), plus JOB R3 (two lane-T tripwire cells replaced by behaviour cells). Tier 1 (session revocation is an auth surface).

BLUF: 0 Blockers, 0 Majors, 4 Minors. 6 of 6 paths in OWNS-S (the two lane-T files are in OWNS-S for R3 only, excluded from the T successor's block); the R3 hunks stay inside the two named describe blocks plus the `runSession` helper the kit allows. Merge clean; plain verify of main + head PASS 5499/328, EADDRINUSE 0; all four together PASS 5522/334. Every new cell red without the change. **The 5499 count is within the kit** (see F1).

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | origin = `5fbad1ba...`; commits `c6801b2` (predecessor, parent `3929b794`) and `5fbad1b` (R3, forward, no amend) | `git ls-remote`, `git log` |
| 2 | Paths | 6 of 6 in OWNS-S; the rd798/rd799 log tests are also claimed by the ORIGINAL T kit B1431 (expected: B1480 grants them for R3, and the T successor B1481 excludes both with `-` lines until this branch lands); 0 overlap with other lanes' pushed branches | partition program; control: rd798 in B1431 fires True, in B1481 False |
| 3 | R3 hunk fence | `git diff -U0 c6801b2 5fbad1b`: rd798 one hunk inside the `X-222-223` block (lines 553-565 old); rd799 one hunk in `runSession` (137-149, default-parameter change only) and one inside the `X-171` block (251-263). No other hunk | git diff |
| 4 | Merge | `merge-tree` rc 0, tree `c236725d` = head tree + main's HISTORY.md; onto the whole stack: rc 0, all-four tree `be5e838c` | merge-tree |
| 5 | Verify main + head | plain, counts file at 5499/328: `VERDICT: PASS - 5499/5499 tests passed across 328 suites`, EADDRINUSE 0 | verify-suite under the jest lock |
| 6 | Names vs main (main PASS 5493/326) and all four | PASS 5522/334; names vs the stack: +8 (rd798 B-223 S-223, rd799 B-171 S-171, rd972 x3, rd976 x1), -2 (`X-222-223`, `X-171`); failing suites added none | compare.py |
| 7 | Red without the change | the 4 test files planted on main: rd972 3/3, rd976 1/1, B-223, S-223, B-171, S-171 all RED; the other 84 tests of rd798/rd799 green (unchanged cells) | `raw/red2.json` |
| 8 | Code at source | `PUT /api/auth/users/:email` called `deleteSessionsForUser`/`getAllSessions`, neither defined (typeof-guarded), so no session ever ended; now `deleteUserSessions(email)`, which returns a count. Its other caller (user delete, server.js:3569) ignores the return value. Confirm-clarification read `conversationSessions` (undeclared); now `conversationContexts.get` | git grep |
| 9 | Deploy demo | STARTS A RUN (`backend/`, `__tests__/`); workflow untouched; jobs gated on `CI_DEPLOY_ENABLED`, expected skipped | workflow text |
| 10 | Scans | names 0 (188 added lines, 26 message lines); secrets: 1 pattern hit = a fake test password literal `'rd972-new-password'` in a test body (not a secret); GUID/hosts/Cf/non-ASCII 0; gitleaks rc 0 (control rc 1); CodeQL pre-scan 0; `node --check` OK | scans.py |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Minor (answered) | Count 5499 vs the kit's planned 5497: the kit's R3 text itself asks each replaced cell to cover two behaviours (an ordinary body, and a CR/LF body printed neutralised), and the builder wrote them as two cells each. Measured: -2 +8 over main, 5493 - 2 + 8 = 5499. The drafter's "a replaced cell changes no count" assumed one-for-one; the hunk fence (row 3) holds. Within the kit. |
| F2 | Minor | Alert 222's line ("Learned from user confirmation") is unreachable over HTTP: nothing writes `lastIntentAnalysis` (1 occurrence in server.js, the read). The B-223 cell pins counts `[0, 1]`, i.e. it asserts 222 does NOT fire. Builder's RECORDS LINE R-3 is true; when that branch is made reachable this cell will need editing. |
| F3 | Minor | `jest.setTimeout(240000)` added in rd972 and rd976 (predecessor's commit). The kit's property (4) bars an added timer unless the ticket says so; this is a test-timeout setting, used in 94 test files on main, not a timer. Noted, not counted. |
| F4 | Minor (behaviour) | Security-positive behaviour change: an administrator who changes their OWN role, active flag or password through this route now loses their own session too (the store matches by email). Intended by the ticket; the UI should expect a re-login. |

## Builder STATUS claims
| Claim | Grade |
|---|---|
| update PASS 5499/328; plain PASS 5499/328 | true (my plain run on main + head) |
| removed 2 / added 8 explanation | true |
| R3 red-first base 4/4 red | true |
| R3 plant (logSafe removed) turns S-223, S-171 red | not shown by me (I did not repeat the plant) |
| R-3 unreachable branch | true |

## NOT RUN
- Hosted CodeQL, npm-audit, arm-ttk, `CI_DEPLOY_ENABLED` read, Jira (fences).
- The logSafe-removal plant (the builder's).
