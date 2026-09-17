SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1030 KS-1211 @e43af493418a1f13cfb60c994380fb74d79ad07e (Seat B)
TS: 2026-09-17T11:04:44.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

BLUF
PR-3b is READY FOR QA as #1030 at e43af493418a1f13cfb60c994380fb74d79ad07e (head read from origin in the same action as this send). It covers row 4, GHSA-82fw (vitest / @vitest/mocker < 4.1.11): 26 standalone locks + the workspace root, the row removed (32 -> 31). Proposed tier 2 through-code, because the issuer bundle is byte-identical to develop. The consumer to re-run is systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts:96-100. Refs KS-1211 (contributes only); KS-1211 In Progress, comment 7c3010b2. KS-1218 filed (the Schemathesis install-line gap).

WHAT'S IN IT (commits on base develop)
- 17cbb1091: the 26 standalone locks + 15 manifests.
- 566107f01: merge of develop 20ab16f9a (#1018, #1027), never rebased. Tree 309e38878 = `git merge-tree --write-tree` of the two parents. #1027 had also touched the issuer, referral and vc-issuer locks, and git merged them without a conflict; each was regenerated from develop's blob with this recipe, and the result is byte-identical to git's merge, with js-yaml / bbm unchanged.
- e43af4934: the root lock (last and alone) + the row removal.
- Files vs develop (three-dot): 43 = 27 locks + 15 package.json + audit-baseline.json.

RULING (a) GUARDS, measured at the head against develop 20ab16f9a, per lock
- issuer first: FAMILY 8 + tinyrainbow 3.1.0 -> 3.1.1, declared only by vitest/@vitest/*. vite, rolldown and lightningcss did not move.
- Every changed, added or removed entry in 27/27 locks: flag class unchanged (strict, so devOptional -> optional also counts as BAD), OTHER entries dev, every declarer's range satisfied (shipped semver 7.8.0). bad 0.
  - Added 22 (all dev), removed 136 (all dev; the wasm fallback chain + tslib).
  - Planted dev->prod, devOptional->optional, out-of-range and forbidden-root-delta controls each rc 1.
  - The union of moves, with lock counts, is in the PR body (vite 8.1.3 -> 8.3.0 x20, rolldown -> 1.2.9, lightningcss -> 1.33.0, nanoid, picomatch, postcss, obug, std-env, tinyexec, es-module-lexer, @jridgewell/sourcemap-codec, @oxc-project/types). All are in service and harness locks; none in issuer.
- Manifests: 15, exactly 2 ranges each (30 lines).
  - DEFAULT, named: npm --save-dev re-sorts the dependency maps. The re-sort was not kept; each manifest is its before-bytes with the 2 range substitutions, asserted content-equal to npm's output.
- Root: `npm install --package-lock-only --ignore-scripts` (the root declares no vitest, so no --save-dev). FAMILY 23, 15 member entries with exactly the 2 ranges, OTHER 5 (integrity/resolved metadata only, versions and flags unchanged), 0 flag drift, 1970 -> 1970.
- Across 45 tracked locks at the head: 28 carry vitest/mocker (the 27 + akto), all >= 4.1.11; 17 none; mobile none; control lodash 5.

GATES (shipped scripts)
- fix (branch, row removed): audit-gate rc 0 (30 reported / 31 baselined); audit-locks rc 0 (43 lockfiles, 29/29).
- control (branch, row present): rc 0, GHSA-82fw under CLEANUP.
- negative control (develop 20ab16f9a, row removed): audit-gate rc 1 exactly GHSA-82fw; audit-locks rc 1 exactly GHSA-82fw in 26 locks.

TESTS (host npm ci at the head, 10:53-10:57Z, hoisted vitest/mocker 4.1.11, packages/shared built)
- npm test -w <member> -- --run, 25 members:
  - shared 851/851, analytics 28/28, anchoring 237/238, api-gateway 550/550, auth 755/755, billing 93/93, demo-service 72/72, guardian 1/1, kyc 26/26, m365 38/38
  - mcp-server 1/1 (placeholder), nft-certificate 38/38, prism 29/29, queue 1/1, referral 26/26, security 213/213, services/shared 11/11, staking 61/61, tenant-prov 13/13, timestamping 42/42, tokenisation 8/8, transfer 70/70, vc-issuer 108/108, wallet-connector 45/45
- issuer: npx vitest run 12/12; workspace build + check:bundle OK (250.6 KB).
- Issuer bundle, Dockerfile route (standalone-lock npm ci, vendor/shared, SHARED_DIR, build): develop 20ab16f9a 58 files == head 58 files, sha256-identical. Determinism control: 2 develop builds identical.
- lockfile-cleanroom.sh: 35/35 (mcp-server SKIP, systemTest out of its corpus; those 3 by parse).
- systemTest rule 2 (per your 10:27:52Z ruling), each after a real npm ci, no stack up:
  - akto quality rc 0 (1233/1233);
  - api-explorer rc 0 (58/58);
  - performance rc 0 (1083/1083);
  - playwright rc 0 (371/0);
  - npm audit 0 in all.
  - Schemathesis quality:static (throwaway copy + venv under the scratchpad, 0 files differ from develop):
    - run 1, documented line `pip3 install -c constraints.txt -e '.[dev]'`: rc 1, pip-audit red only on venv pip 26.1.1 (PYSEC-2026-196, PYSEC-2026-3721); Ruff x2 and MyPy x3 pass.
    - DEVIATION, per your 10:48:24Z authorisation: `pip3 install --upgrade pip` (26.1.1 -> 26.2.1).
    - run 2: rc 0, all checks pass.
    - Live `quality`: not run.
- §6 / Q3 consumer: 5 grep hits (4 prose + the consumer), control 134.
  - 4.1.10: child "Tests  245 passed (245)", suite 3/3, 6.00 s.
  - 4.1.11: 245/245, 3/3, 5.97 s.
  - At the head: 245/245, 3/3.
- Full preflight in-hook on the push: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3, 4 and 8 skipped (no stack), so this is NOT a pass. Leg 2 35/35; leg 5 59/59; leg 6 OK 30/31; leg 7 OK. Push rc 0 (SSH keepalives set on the command only).
- Post-push: 4 orphan login_stub listeners (KS-1201) ended by verified pid; CONTROL ps rows 1117; 0 of mine remain; 17 non-node controls unchanged.

RED OR ODD, ALL MEASURED (for the gate)
1. anchoring threadTokenMint.test.ts:71 "Could not serialize the data: Error: Unsupported type": PRE-EXISTING, tracked as KS-562 (Backlog) and BACKLOG.md:182. A/B on that file: develop 20ab16f9a (vitest 4.1.10) fails 2/2; head (4.1.11) fails 2/2; same error.
2. One performance quality run at 17cbb1091 (same harness lock as the head) hit "Test timed out in 15000ms" at unitSuiteSlotIndependence.test.ts:127 (16139 ms). That is a duration, not an assertion.
   - Afterwards: 4.1.11 test:unit 1083/1083 in 2 runs at load1 35-41.
   - Alternating A/B, develop worktree (4.1.10) vs head: A 1083/1083 x3 at load1 20.8 / 21.3 / 17.4, totals 6.79 / 6.38 / 6.45 s; B 1083/1083 x3 at load1 19.4 / 20.0 / 16.6, totals 6.88 / 6.40 / 6.35 s.
   - At the head, quality: 1083/1083 at load1 8.5.
   - (My first A/B's 4.1.10 side was VOID: an out-of-repo copy lacking systemTest/fixtures. It was re-run in the real worktree.)
3. Develop moved after the push: 75ad0e55c (#1026, KS-839) touches 2 services/auth files, 0 of these 43; merge-tree of develop and the head is clean. No merge-in was made.

F2/F3 WORDING (your GO #1027)
- F2: the PR body scopes "dev-only" to the 27 locks this PR touches, "not a claim about other locks".
- F3: no mobile js-yaml statement in this PR (no vitest in mobile).

NOT COVERED
- Live Schemathesis / Akto scan / Playwright e2e / k6: not run (no stack in this lane).
- No image build.
- Preflight legs 3, 4, 8 skipped.
- mcp-server and systemTest locks verified by parse, not by the clean-room.
- Whether vite 8.3.0 / rolldown 1.2.9 change any SERVICE test behaviour beyond the suites above: covered only by those suites.

OPEN PRs
- 20 open. Overlap: only Dependabot #949, #948, #947, #946, #945, #649, #639, #635, #575, #572 (root lock; #948, #649, #575 also some service manifests).
- 0 others touch audit-baseline.json. #1030 is my only open PR.

NEXT (lane rule: one PR open)
Build PR-7 (mysql2 override, row 3, KS-763) locally while #1030 is gated; push only after #1030's MERGED receipt, with develop merged in. After that: PR-4 qs.

Records: 5_Project_History/2026-09-17_seatB-succ1/pr3b/.

Seat B

