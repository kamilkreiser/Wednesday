SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: audit rows fixability table (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

BLUF
Step 1 is measured at develop f8c7aaa39: 10 of the 15 rows are fixable in range by pin bumps, and 5 need Kam.
- All 9 Sep-24 rows except mysql2 are in-range fixes.
- Two measurements overturn the rows' own text:
  1. The two qs rows no longer need express 5. express 4.22.3 and body-parser 1.20.8 both declare qs ~6.16.0, the fixed version. The only blocker is our own override "body-parser": "1.20.6" in 20 manifests. I flag this rather than build it, because it changes the premise of Kam's 09-03 "migrate" ruling.
  2. react-router-dom GHSA-jjmj is fixed at 6.30.6 (patch), so it is not "v7 only". react-router GHSA-wrjc and GHSA-337j do need v7.
- HIGH in the dormant tree (you asked for this in the BLUF): mobile/secuura-app's lock (not scanned, KS-769) carries js-yaml 3.14.2 and 4.1.1, non-dev, inside GHSA-2883's HIGH ranges. No bump there, per your Q2 ANSWER.
- KS-1211 filed for the 7 KS-1024 rows. Comment ids for your delivery record:
  - KS-1211 ruling comment: 0ec33ad8-a0a8-4447-b562-950a26ca4354
  - KS-763 step-1 comment: b953f63d-9ee3-4f49-b6ec-5135bdca5705

RECOMMENDATION (needs your ANSWER before I branch)
1. Block order and regroup. Every family except colord moves the root lock, Blockchain/Dev/package-lock.json, and most also share the service locks. A lock conflict is re-generated, never hand-merged. So one root-touching PR at a time, plus colord in parallel:
   - PR-1 hono x3 (rows 8-10): 3 locks, patch, runtime. Tier 1 proposed. First.
   - PR-2 colord (row 6): 2 systemTest locks, disjoint from everything. Tier 2. In parallel with PR-1.
   - PR-3 js-yaml HIGH + vitest + baseline-browser-mapping (rows 7, 4, 5): an identical footprint (service locks + root), all dev-only, one root regen instead of three. Tier 2. After PR-1 merges.
     This regroups your family grouping for that reason. Say if you want them split.
   - PR-4 qs x2 (rows 1-2): only if you or Kam rule the flag in. 29 locks + 20 manifests (the override value 1.20.6 -> 1.20.8). Tier 1.
   - PR-5 react-router-dom (row 13, Sep-30): 4 locks. Tier 1. After the Sep-24 blocks.
2. The qs flag: bump in range on express 4, or keep the qs rows on the KS-775 express 5 path? Your call whether it goes to Kam.
3. Per-row QUESTIONs:
   - Row 3 mysql2 (Sep-24): next, today.
   - Rows 11, 12 (react-router major), 14 (@hono/node-server) and 15 (ip-address HIGH): by Fri 25 Sep. Say if you want them today.

TABLE (instruments: [G] gh api /advisories; [N] npm registry via the shipped gates 07:05Z; [R] row reason text; [V] npm view versions / dependencies; [L] parse of 45 locks + 49 manifests; [D] Dockerfile runtime verbs)

Severity: [G] and [N] agree. HIGH = js-yaml (2883) and ip-address (mwp4); the other 13 are medium/moderate. The [R] disagreements are word matches, not severities:
- hono: "HIGH" appears only in a quoted sentence about the standing authority ("would NOT clear a HIGH"). Each row's own text says "(moderate)".
- ip-address and mysql2: "low" is a substring of "below" and "allows". Word-boundary control: 0 in both.

Rows 1-2 qs (KS-763, Sep-24), medium [G]
- Fixed: 6.16.0 (4mjr <6.16.0; x5fp >=6.14.2 <=6.15.3).
- In range: YES.
  - [V] express 4.22.1 -> 4.22.3 changes exactly qs ~6.14.0 -> ~6.16.0, body-parser ~1.20.3 -> ~1.20.5 and path-to-regexp ~0.1.12 -> ~0.1.13 (= our existing override).
  - [V] body-parser 1.20.6 -> 1.20.8 changes only qs.
  - Blocker: our override body-parser "1.20.6" in 20 manifests, set by KS-531 3418e9b92 under its own rule "every declaring parent's range permits the fix".
- Distance: express and body-parser patch; qs 6.14.2/6.15.x -> 6.16.0 MINOR.
- Moves: 29 locks (28 standalone + root) and 20 manifests (override value only).
- Shipped: YES. prod in 26 service/connector locks; every service Dockerfile keeps prod (--omit=dev / prune, 24 of 24) [D].
- Disposition: BUMP, FLAGGED. Tier 1 proposed (request parsing in every express image).

Row 3 mysql2 (KS-763, Sep-24), medium [G]
- Fixed: 3.23.1.
- In range: NO. [V] prisma 7.8.0, 7.9.0, 7.9.1 and 7.10.0 (latest stable 7.x) all pin mysql2 3.15.3 exactly.
- Moves: originate + root, by override only.
- Shipped: devOptional. The row's own 09-06 measurement found it in the originate image and never loaded.
- Disposition: QUESTION (override contradicts a declared range).

Row 4 vitest / @vitest/mocker (KS-1211, Sep-24), medium [G]
- Fixed: 4.1.11.
- In range: YES (^4.1.9 / ^4.1.10; @vitest/coverage-v8 ^4.1.10 -> 4.1.11, whose peer is vitest 4.1.11 exact). Patch.
- Moves: 26 standalone + root (systemTest/akto already 4.1.11). 0 manifests.
- Shipped: NO (dev in all 28 carrying locks).
- Disposition: BUMP. Tier 2. The Q3 grep runs before the §6 line is written.

Row 5 baseline-browser-mapping (KS-1211, Sep-24), medium [G]
- Fixed: 2.11.0.
- In range: YES (browserslist ^2.9.0 / ^2.10.12 / ^2.10.42 -> 2.11.24). MINOR.
- Moves: frontend admin/issuer/outlook-addin/verifier, services governance/originate/referral, root (2.10.29 dev).
- Shipped: NO (dev; governance/referral prune per KS-490).
- mobile carries 2.9.14 (in range, moderate).
- Disposition: BUMP. Tier 2.

Row 6 colord (KS-1211, Sep-24), medium [G]
- Fixed: 2.9.4.
- In range: YES (stylelint ^2.9.3 -> 2.10.0). Minor.
- Moves: systemTest/akto and systemTest/api-explorer.
- Shipped: NO (systemTest dev).
- The row is scope standalone-locks, so I confirm no CLEANUP line after removal.
- Disposition: BUMP. Tier 2.

Row 7 js-yaml (KS-1211, Sep-24), HIGH [G]
- Fixed: 3.15.2 (3.x) / 4.3.2 (4.x).
- In range: YES (@istanbuljs/load-nyc-config ^3.13.1 -> 3.15.2). Patch.
- Moves: governance, originate, referral, vc-issuer, root.
- Shipped: NO (dev; the systemTest 4.3.2/5.x copies are outside the ranges).
- Disposition: BUMP. Tier 2.

Rows 8-10 hono (KS-1211, Sep-24), medium [G]
- Fixed: 4.13.5.
- In range: YES (sdk ^4.11.4, @prisma/dev ^4.12.8, @hono/node-server peer ^4 -> 4.13.8). Patch.
- Moves: mcp-server, originate, root.
- Shipped: YES. mcp-server prod (sdk is its runtime dep); originate devOptional (the same class mysql2 was measured into that image). The rows' "0 production declarations" holds for direct declarations only.
- Disposition: BUMP. Tier 1 proposed.

Rows 11-12 react-router wrjc / 337j (KS-528, Sep-30), medium [G]
- Fixed: 7.18.0 only. MAJOR, plus client code in 3 portals.
- Disposition: QUESTION (major + source change).

Row 13 react-router-dom jjmj (KS-528, Sep-30), medium [G]
- Fixed: 6.30.6.
- In range: YES (frontends ^6.30.4; 6.30.6 pins react-router 6.30.6). Patch.
- Moves: admin, issuer, verifier, root.
- Shipped: YES (client bundle).
- Removes row 13 only.
- Disposition: BUMP. Tier 1.

Row 14 @hono/node-server (KS-530, Sep-30), medium [G]
- Fixed: 1.19.15 on v1. The row says ">=2.0.5 major", but the v2 line is not needed.
- mcp-server: sdk ^1.19.9 -> 1.19.17, in range.
- originate + root: 1.19.11 is pinned EXACT by @prisma/dev 0.24.3 (prisma 7.8.0). [V] prisma 7.9.0+ pins @prisma/dev 0.24.14+, which declares no @hono/node-server; control: 0.24.3 does declare it.
- Full fix: mcp-server patch + prisma/@prisma/client 7.8.0 -> 7.10.0 (in ^7.8.0). The client is regenerated at image build (originate/Dockerfile:38), which your brief's HOLD puts behind a question.
- Disposition: QUESTION (prisma move). Overlaps Dependabot #949 (prisma 7.10.0).

Row 15 ip-address mwp4 (KS-729, Sep-30), HIGH [G]
- Fixed: 10.3.1.
- In range: NO. 9.0.5 comes via @cardano-sdk/core 0.46.12 (^9.0.5), pinned EXACT by @meshsdk/core-cst 1.9.1 and @meshsdk/transaction 1.9.1. [V] @meshsdk/core 1.9.1 is the latest stable: no @meshsdk release fixes it, major or not.
- Moves: frontend/issuer + root.
- Shipped: issuer client bundle. SSRF reach in a browser is UNMEASURED.
- Disposition: QUESTION (override contradicts a declared range).

Open-PR overlap (GitHub PR files API, 20 of 20 open PRs read)
- audit-baseline.json: 0 PRs. Control: 10 package-lock.json lines across the same file lists.
- Root lock: #945-#949, #639, #635, #572, #575, #649 (all Dependabot). #949 = prisma 7.10.0; it does not fix mysql2.
- Manifests: #920 (KS-734).

Slips (none skipped)
- My first npm view calls also requested time.modified and peerDependencies, beyond the exact wording of (a). It is the same packument read, with no new URL. Later reads keep to versions / dependencies.
- A two-field npm view returns an un-keyed map when one field is absent, so express read "0 deps". The express 4.22.1 control caught it, and every parent pin was re-read single-field.
- My first parse folded devOptional into "non-dev" (hono, @hono/node-server and mysql2 in originate/root). A spot check caught it; everything was re-classified (control: prod 6989 / dev 7550 / devOptional 205 / optional 271). No disposition changed.

Records: 5_Project_History/2026-09-17_seatB-audit/step1/ (fixability-table.md, ghsa/, npmview/, linear/).

MEANWHILE
- Writing the row 3 mysql2 QUESTION.
- No branch, lockfile or state change until your ANSWER sets the order.

Seat B
