GATE B1440-3: GO @ d49be88 on main 009421a

This gate covers the LANDED head d49be881 of PR #304 as a delta on round 2 (GATE B1440-2, GO WITH FINDINGS @ fc90f07). PR #304 is merged (squash 2211608 on main). Round-2 findings G1 to G3 are not re-opened here. Gate clone is in the session scratchpad, push URL INVALID_NO_PUSH, never pushed. No hosted write, no PR, no Jira, no az.

## Findings

| # | Sev | Check | Result | Instrument and control |
|---|---|---|---|---|
| 1 | none | Delta fc90f07..d49be881 paths | 1 commit, 1 file of 1: web/src/components/partner/PartnerDashboard.alias.test.tsx (+1 -1). Test only; no product, package, workflow or e2e file. | `gh api compare` (ahead_by 1, behind_by 0, total_commits 1) equals `git diff --stat` in the clone. Branch ref and PR head both read d49be881. PR is merged, squash 2211608, base 78d4b3c; main is now 009421a. |
| 2 | none | Test still pins what round 2 relied on | Yes. Only the Partner-control row changed (line 50). The Demo row (alias ORG-00007/8 shown, stored names absent) and the unknown-answer row are byte-identical. The control row now uses `getAllByText((text) => text.includes(NAME_A) \|\| text.includes(NAME_B))`, which asserts the same thing as before (a Partner without Demo sees a stored name; no ORG- alias). | Vitest on the file, by program: fc90f07 3 passed / 0 failed; d49be881 3 passed / 0 failed (vitest 5.0.5, Node 26.13.0, deps from `npm ci` on d49be881 lockfile). Control that the new matcher can fail: planted `text.includes("NOPE_ZZ")` makes the control row fail (1 failed, 2 passed). |
| 3 | none | Red without the fix | Holds. d49be881 copy with PartnerDashboard.tsx put back to its pre-#304 state (6b0c5f2): 2 failed (Demo row, unknown-answer row), 1 passed (Partner control row, which passes either way by design). Same as the builder's claim. | `git show 6b0c5f2:.../PartnerDashboard.tsx` placed in a copy; confirmed the file is among the files #304 changed. |
| 4 | none | CodeQL pre-scan of added lines | 0 hits in the delta and 0 over the whole PR range 78d4b3c..d49be881 for `new RegExp(`, `replace(/[`, `innerHTML`, `dangerouslySetInnerHTML`, `child_process`. The line-50 hand-escape (which escaped only the brackets, no backslash) is replaced by a plain text comparison, so no RegExp is built from a variable. | Positive control: the same scan over 78d4b3c..fc90f07 fires on exactly the old line 50. Delta also: 0 non-ASCII bytes in diff and commit message, 0 ban-list hits (underscore-aware regex; planted `_by_Kam_` is caught). |
| 5 | none | Hosted CI and CodeQL on d49be881 | `check-runs`: every run completed success: 3 sets of CI jobs (web build, vitest, 8 e2e shards, api, api on SQL Server x3, infra, gitleaks, dependency review) (web build, vitest, 8 e2e shards, api, SQL Server, infra, gitleaks, dependency review), plus CodeQL and Analyze (javascript-typescript, csharp, python, actions) all success. 0 non-success. | `gh api -X GET commits/d49be881.../check-runs`. Open code-scanning alerts: main 0, repo-wide 0. Control: alerts #16 and #17 (js/incomplete-sanitization, this file) list as `fixed` on refs/pull/304/head; main also lists an older alert #1 as `fixed`. |
| 6 | Minor | Builder claim "full vitest 289 files / 4216 passed, lint and typecheck rc 0" | Not re-run here (delta gate). Hosted `web unit tests (vitest)` and `web build (... lint, typecheck ...)` are success at d49be881, which supports it. | Hosted proof only. |

## Builder ADDENDUM-2 claims

- True: diff is 1 file, 1 insertion, 1 deletion; no product file; the line now matches by text; 3 passed at head; 2 of 3 fail with PartnerDashboard.tsx at main state; Partner row passes either way; plain push (ref equals d49be881); commit message plain ASCII with attribution.
- Not shown: positive-control scan result and full vitest 4216 (the gate re-ran the scan with the same positive control; vitest proved by hosted CI only).

## NOT RUN

- Full local vitest, lint, typecheck, build and the e2e shards at d49be881: the delta is one test line, and hosted CI is the proof (all success).
- api, infra, gitleaks, dependency review, CodeQL locally: hosted only.
- Landing files (pr-title, squash-*, landing.txt): not written; the PR is already landed.
