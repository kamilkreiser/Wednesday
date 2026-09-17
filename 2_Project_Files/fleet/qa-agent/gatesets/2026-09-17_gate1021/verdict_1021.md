SUBJECT: [QA -> Wednesday] TIER 2 GATE #1021 (KS-1211) 742e1c608 — GO WITH FINDINGS
TS: 2026-09-17T08:17:51.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

QA agent — TIER 2 GATE, ROUND 1 — Secuura/Blockchain PR #1021 (KS-1211, Seat B) @ 742e1c6080f2527973268146611930e4a70edef2
VERDICT: GO WITH FINDINGS — on 742e1c608 AND on the merged tree 207ba797c (squash onto develop 581c9db0db4201c42cbbf702f339b750989acdb1).
One finding, F1 Minor (process, target SEAT EVIDENCE). Nothing is wrong in the bytes.

BLUF
The PR does exactly what it says. Each lock: 1 packages entry changed (node_modules/colord: version/resolved/integrity; dev:true kept), 0 others, 0 root drift, planted change detected. Baseline: 38 -> 37, only GHSA-2wm5-q62r-hmrv removed, 0 added, 0 altered, planted alteration detected.
Shipped gates from Blockchain/Dev:
- head: audit-locks rc 0 (43 scanned, 0 CLEANUP), audit-gate rc 0.
- head + develop baseline: rc 0 + the single CLEANUP GHSA-2wm5.
- base without the row: rc 1, exactly GHSA-2wm5, 2.9.3, 2 locks (x2, identical).
- audit-gate: blind by construction (rc 0 without the row), but reds on GHSA-2883 removal (rc 1).
Advisory range, from the gate's own response: "<2.9.4". Shipped semver 7.8.5: 2.10.0 outside it and inside stylelint ^2.9.3, controls both sides.
READY gap closed:
- Clean-room is blind to a garbage integrity (rc 0); a real npm ci rejects it (EINTEGRITY rc 1).
- Real npm ci head/base: rc 0, lock sha unchanged, npm ls stylelint@17.14.1 -> colord@2.10.0 / 2.9.3.
- npm run quality head: akto Tests 1233 passed (1233), api-explorer 58 passed (58), found 0 vulnerabilities. Base identical.
- colord is loaded 0 times across the full traced quality gate (85 / 31 hooked processes; stylelint control 1152 / 1155).
NEW since the brief: #1022 (KS-1211 hono, Seat B) is open and shares audit-baseline.json. It merges clean in both orders to the same tree 1b03e6951 (34 rows, GHSA-2wm5 still gone).

F1 · Minor · process · target SEAT EVIDENCE
systemTest/CLAUDE.md (blob 357015b94) :459-470:
- Rule 1: "After changing any file in a systemTest project, run that package's quality gate ... before committing".
- Rule 2: "Creating OR updating a systemTest PR -> run ALL FOUR full gates".
The READY lists the harness suites and stylelint as NOT COVERED ("verification is by parse + clean-room only"), and the rule text has no lock-only exemption.
Cured as evidence by this gate for akto + api-explorer (green, base-identical).
NOT cured: rule 2's Schemathesis / Playwright / Performance gates; nobody ran them (bytes identical base/head).
Real as evidence, empty as a defect.

ITEMS 1-6
1. Scope: CONFIRMED with planted controls. Counts 423=423 / 361=361. numstat 0/8, 3/3, 3/3; diff -w == plain; 1 commit on f8c7aaa39. Seat round-trip claim holds with a trailing newline.
2. Advisory gone through the shipped gates: CONFIRMED (table in report). CLEANUP by line:
   - audit-locks.mjs:298-300 builds stale standalone-locks rows, printed at :336 after OK.
   - audit-gate.mjs:203-205 filters scope standalone-locks out, so it never prints one.
   Merged tree re-run: audit-locks rc 0 with 43 scanned and 0 CLEANUP; +develop baseline gives rc 0 + 1 CLEANUP; audit-gate rc 0 (36 reported / 37 baselined).
3. Fixed and in range: CONFIRMED.
   - The tee'd bulk response at base carries GHSA-2wm5 moderate "<2.9.4" CWE-1333; at head the request carries ["2.10.0"] and the response has no colord key.
   - Clean-room controls: C0 unmodified OK; C1 bad integrity OK (blind), real npm ci EINTEGRITY rc 1; C2 stylelint colord ^3.0.0 FAIL rc 1.
   - Clean-room alone was NOT sufficient. The MUST is ruled a FINDING (F1), not a RECORD.
   - colord in the harness: forced color-named config loads colord (5 resolutions) and flags "red" identically on 2.9.3 and 2.10.0; the shipped configs never load it.
4. Reach:
   - colord is in 2 of 45 tracked locks (the two harnesses), both dev:true. Control: express 30.
   - 0 in any package.json / Dockerfile / workflow. Controls: stylelint 2 package.json, FROM 37 Dockerfiles, npm ci 11 yml.
   - CI that installs a harness: systemTest/akto via npm ci in pr-platform-suites.yml:514, nightly-platform-suites.yml:460+, pre-merge-platform-suites.yml:230+. api-explorer: 0 workflow lines.
   - GitHub Actions is RETIRED (pr-platform-suites.yml:64). The 7 runs on the head are 6 failure + 1 skipped, so there is NO CI signal; the local runs are the only evidence.
   - Reaches no service, frontend, package or image.
5. Linear + GitHub, merged tree:
   - attachmentsForURL(pull/1021) = 1: KS-1211 [In Progress], linkKind contributes, completedAt null (re-read just before this mail: see LINKKIND RE-READ). Control pull/99999 = 0.
   - Closing phrases: 0 in title, body (Refs KS-1211 x1), commit message, 1 linear[bot] comment, 0 reviews. Regex planted controls hit/miss as expected.
   - Merged tree 207ba797c = develop 581c9db0d + exactly the 3 PR files at the PR's blobs. Develop delta (#1019) is 3 api-gateway files. Control: develop x develop = 99df1503e.
   - Overlap: 21 other open PRs; 20 share 0 files; #1022 shares audit-baseline.json only, merges clean (above), benign.
6. §5f (secuura-test-discipline SKILL.md :526): NOT a runtime-behaviour change (dev-only, harness trees only, no image/service, not loaded by the harness gate). KS-1211 STAYS In Progress (6 rows remain: hono x3 in #1022, js-yaml, vitest/@vitest/mocker, baseline-browser-mapping). No ticket moves to Done on #1021.

MERGE ADDENDUM
Squash 742e1c608 onto develop 581c9db0db4201c42cbbf702f339b750989acdb1. File-disjoint from every open PR except #1022, which shares audit-baseline.json and merges clean in either order (tree 1b03e6951).
#1021 attaches to KS-1211 only, linkKind contributes.
KS-1211 stays In Progress (6 rows remain; Refs, never Closes; no ticket to Done under §5f).
Equality targets:
- audit-baseline.json blob c73fcebed (37 rows)
- systemTest/akto/package-lock.json c4d30077f
- systemTest/api-explorer/package-lock.json 78589de7e
audit-locks rc 0 with 43 scanned and 0 CLEANUP (re-measured on head AND the merged tree).
Records:
- R1 Clean-room is blind to integrity, and leg 2's default corpus excludes systemTest (lockfile-cleanroom.sh:46).
- R2 colord is not loaded by either harness quality gate, so green there cannot falsify this bump.
- R3 #1022 overlap is benign (see above).
- R4 Evidence was taken on node v24.7.0, below akto's engines >=24.11.0 (EBADENGINE for 6 packages, same at base).
- R5 2.10.0 is 4 releases past the 2.9.4 fix and carries 2.9.5/2.9.6 numeric changes. It is inert here; 2.9.4 would have been the minimal pin.
- R6 The round-trip holds with a trailing newline.
- R7 The feed says moderate, the PR says medium.
- R8 mergeable_state is now unknown; compare now reads ahead 1 / behind 1.
- R9 One of my overlap controls was malformed and is void (disclosed; the valid control is rc 1).
- R11 Brief D5 wording: only stylelint color-named/colordUtils.mjs imports colord directly.
- R12 4 surviving baseline rows mention colord in KS-1025 history prose.

NOT TESTED (same prominence)
- Schemathesis / Playwright / Performance quality gates (rule 2): skipped, not required; bytes identical; NOBODY has run them for this PR.
- preflight.sh whole and the real pre-push hook: forbidden / not-applicable. Legs 2, 6 and 7's commands were run directly.
- Preflight legs 3/4/8, any stack, kintsugi, demo, Schemathesis/Akto scans, Playwright e2e, k6: not-applicable (dev-only lock change).
- Any service or packages/* suite (incl. packages/shared 851): not-applicable, no workspace byte moved.
- Harness integration suites (test:all/test:pr/test:security): skipped, they need the Akto stack.
- L4 and G4 on the merged tree: skipped; inputs byte-identical (develop delta is api-gateway source only).
- Image byte search: not-applicable, no image built.
- colord ReDoS timing probe: skipped. The fix is evidenced by the registry range + CHANGELOG 2.9.4 "Reject malformed color strings in linear time".
- Brief C3 manifest-drift control: skipped (C2 already reds).
- The seat's regen method (container / npm 11.19.0): not re-derivable from the bytes.
- KS-1211 transition history: not re-read (state read directly).
- #1021+#1022 combined tree through the audit gates: out of scope (separate gate).
- Harness runs on node >= 24.11.0: host not available.

CHECKOUT READINGS (Secuura 2_Project_Files, read-only)
start 18:06:17: porcelain 0 | .git/config sha256 d7e7298b02c45f5267520f79985ae97abe51ac3d8b82a7e8cb35c50059a09f66 | refs 924 | .git/worktrees 112
close 18:13:55: porcelain 0 | .git/config sha256 d7e7298b02c45f5267520f79985ae97abe51ac3d8b82a7e8cb35c50059a09f66 | refs 925 (+1, seats fetch) | .git/worktrees 112
No push, hook or preflight anywhere. No seat worktree or other gate clone entered. No fix, comment, filing or ticket write.

REPORT
/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1021-742e1c608-tier2-r1/report.md (+ evidence/)

LINKKIND RE-READ (immediately before send): linear 2026-09-17 18:17:48 AEST attachmentsForURL 1021 1    on KS-1211 [In Progress] completedAt None linkKind='contributes' status='open' attachmentsForURL 99999 0
Sent: 2026-09-17 18:17:50 AEST (from date)
