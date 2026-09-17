SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1027 (Seat B)
TS: 2026-09-17T10:46:27.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

BLUF
#1027 is MERGED on your signed GO (10:39:56Z): squash 20ab16f9a80c5c3c75e613d8c670efefd8f5cafb, merged_at 10:41:50Z, verified at origin. Rows 34 -> 32, both gates rc 0 on merged develop. KS-1211 stays In Progress. Facts comment f0479af5-697c-4551-a83b-b0b8ae585f44. New ticket KS-1216 (bundled js-yaml blind spot, Backlog, severity unmeasured). PR-3b is built locally and NOT pushed; one gate item is under measurement (see PR-3b below).

MERGE
- Pre-step (10:40-10:41Z):
  - ls-remote read #1027 = d7fc6cc55 (= gated) and develop = e02515f8f (moved from 19f1e5475).
  - The move is #1018 alone (e02515f8f, parent 19f1e5475). It touches 2 files, both under services/auth (users.ts, ks1050 test): 0 of #1027's 10 files, 0 under scripts/audit/. The overlap instrument read 10/10 against #1027's own list as a control.
  - attachmentsForURL(pull/1027) = KS-1211 contributes only. Closing phrases in the body: 0; control `Refs KS-n` matches: 1.
  - mergeable true (unstable = the retired Actions runs).
- Squash: REST PUT with sha pin d7fc6cc5582b918c0773ec6f25f86407de6f86ab, http 200, merged true. Title "KS-1211: bump js-yaml 3.15.1 -> 3.15.2 and baseline-browser-mapping to 2.11.24; remove their two fixed audit-baseline rows (#1027)"; the body is the branch commit's message.
- Verified at origin (ls-remote develop = 20ab16f9a):
  - parent e02515f8f;
  - tree f62662d936bfd12fc423b3a7106f8b4a1517dd9b = `git merge-tree --write-tree e02515f8f d7fc6cc55`, predicted before the merge;
  - files vs parent 10, set-equal to the PR's 10;
  - author kksecura.
- Blob equalities at 20ab16f9a, 11/11:
  - audit-baseline.json 017f52bb5 (32 rows)
  - root package-lock.json 4831bf207
  - frontend admin 3d9acadaf / issuer b0c47af71 / outlook-addin c71cfe57a / verifier 0a13fe2b7
  - services governance 5fae8f62c / originate 040908e22 / referral 725d5d2c2 / vc-issuer 05dff4ebb
  - mobile lock 2f5f8c1f4, unchanged
  - Control: develop's pre-merge baseline blob e6f2184d2 does not match the target.
  - Both #1018 files in the merged tree are identical to e02515f8f's.
- Re-measure on merged develop (WT2 detached at 20ab16f9a, porcelain 0):
  - audit-gate rc 0: "31 distinct advisories reported, 32 baselined", 0 CLEANUP;
  - audit-locks rc 0: 43 standalone lockfiles, "30 advisories match, 30 already baselined".

AFTER THE MERGE
- KS-1211: In Progress, read before and after the comment. Facts comment f0479af5: squash sha, rows 34 -> 32, the gate re-measures, row 4 still open, the §5f sweep still owed, F1/F2/F3/F5 one line each. No @-mentions. Links after the merge: KS-1211 contributes only.
- KS-1216 filed: "Bundled js-yaml copies ship in service runtime images and are invisible to audit-gate/audit-locks". https://linear.app/secuura/issue/KS-1216
  - Filed in Backlog, priority none, assigned to our account, project Security Review — Platform K.
  - The body quotes the gate's F1 detail whole (instruments, probe table, reachability NOT traced, fix-shape), states the severity as UNMEASURED, and says Refs KS-1211.
  - Its first item is a measurement: a runtime load trace in a built originate image, and whether any path parses attacker-controlled YAML through either copy.
  - Read back 8/8 anchors (control anchor absent).
- Board search before filing (team issues incl. archived, 1205 issues + 3440 comments, literal match):
  - confbox 0/0;
  - @effect/platform 0/0;
  - YAMLException: 4 issues (KS-1117, KS-1109, KS-1108, KS-1099; k6 and Akto config-loader error handling, a different subject) + a comment on KS-1099;
  - GHSA-2883: KS-1211 only (+ comments on KS-1024, KS-1211);
  - control js-yaml: 13 issues.
- Dependabot: recorded only. 10 open Dependabot PRs share the root lock (per the gate); nothing done with them.
- F2 and F3 are carried as wording fixes into the next READY.

PR-3b vitest (row 4, KS-1211): BUILT LOCALLY, NOT PUSHED
- Branch feature/ks-1211-bump-vitest in WT1, commit 17cbb1091 on base 19f1e5475 (develop is merged in before any push).
- Scope: 26 standalone locks + 15 manifests (30 range lines, 2 per manifest).
  - Parsed across all 45 locks: vitest/@vitest/mocker is below 4.1.11 only in the root lock (4.1.10, left for after the merge-in); 27 locks are at 4.1.11; 17 carry none; control: 5 locks carry lodash.
- issuer measured first (scratch copy): FAMILY 8 + tinyrainbow 3.1.0 -> 3.1.1 (declared only by the vitest family). vite, rolldown and lightningcss did not move.
- Per lock: every changed, added or removed entry was checked for dev flag class unchanged (strict: any class change is BAD, including devOptional -> optional), OTHER entries dev, and every declarer's range satisfied (shipped semver 7.8.0, node_modules walk-up). All 26 locks: bad 0. Planted-flag, planted-range, planted-devOptional and planted-root-delta controls each fire rc 1.
  - OTHER counts per lock: issuer 1, auth 2, services/shared 2, vc-issuer 25, api-explorer 34, mcp-server 34, performance 36, analytics 6, and 41-45 for the rest.
- Default applied, to be named in the READY: npm --save-dev re-sorts the dependency maps in 15 manifests. The manifest was restored to its before-bytes with only the 2 range substitutions, asserted content-equal to npm's output (npm's output kept in records). No lock change.
- Root pre-measured on a scratch copy (root lock + all 32 workspace manifests at 17cbb1091): `npm install --package-lock-only --ignore-scripts`, rc 0. FAMILY 23, OTHER 5, bad 0, 0 flag drift. vitest 4.1.11 hoisted, all 15 nested coverage-v8 at 4.1.11. The real root regen runs after the merge-in, last and alone. The root manifest declares no vitest, so the root takes no --save-dev.
- Issuer bundle, Dockerfile-shaped host build (standalone lock, npm ci, vendor/shared, SHARED_DIR): develop 58 files == branch 58 files, byte-identical by sha256. Determinism control: a develop rebuild is identical. So the bundle does not move and tier 2 holds on this measure. Re-measured on the final head.
- Q3 consumer on 4.1.11, in isolation: child parsed "Tests  245 passed (245)", suite 3/3, 5.97 s. Control on 4.1.10: "Tests  245 passed (245)", 3/3, 6.00 s.
- Harness gates at 17cbb1091, after a real `npm ci`:
  - akto rc 0 (1233/1233);
  - api-explorer rc 0 (58/58);
  - playwright rc 0 (371 pass, 0 fail);
  - audit 0 vulnerabilities in the 3 vitest harnesses;
  - **performance rc 1: 1 failed | 1082 passed.** The one red is unitSuiteSlotIndependence.test.ts:127 ("the slot-sensitive files pass identically ... on every slot"): "Test timed out in 15000ms" at 16139 ms. It is not an assertion. The same file in isolation on 4.1.11 passes in 5.97 s. The machine load average was 30.75 at 20:45 AEST. I am NOT calling it flaky yet: an alternating A/B (4.1.10 develop copy vs 4.1.11 branch, 2 rounds each, same load, test:unit) is running now. Its result goes into the READY, or into a QUESTION if 4.1.11 is the difference.
- Schemathesis quality:static (throwaway copy + venv under scratchpad, `venv/bin/pip3 install -c constraints.txt -e '.[dev]'`, rc 0; tree diff vs develop 0 files): rc 1.
  - Ruff format, Ruff lint, MyPy src/scripts/config: all pass.
  - pip-audit red ONLY on the venv's own pip 26.1.1 (PYSEC-2026-196, PYSEC-2026-3721). 0 findings on the harness's pinned dependencies.
  - Cause: the harness's own setup upgrades pip first (scripts/runner/dependencies.py:50-52), while constraints.txt's documented install line does not. I did not widen to `pip3 install --upgrade pip`.
  - The READY will state this as NOT green, with the cause, unless you authorise the pip upgrade in the throwaway venv. The mismatch between the documented install line and setup looks like a small harness defect (systemTest, not my lane): yours to route.
- Next: the merge-in of 20ab16f9a into the PR-3b branch (merge, never rebase). issuer, referral and vc-issuer are regenerated from develop's blobs, and the root runs last and alone. Then the suites, the full preflight, push, READY.

Records: 5_Project_History/2026-09-17_seatB-succ1/ (merge-1027/, pr3b/).

Seat B

