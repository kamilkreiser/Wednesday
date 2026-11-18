GATE B1702: GO WITH FINDINGS @ c72ba44 on main 6febe11

Tier G2. Head c72ba4420a7258ab4de85a8a3d1b80f9cd0b3acb (ls-remote equals READY). Base b746cb92. Main moved during the gate to 6febe112 (PR #212 squashed; it touched only src/MpsCalc.Import/PriceBookImporter.cs and tests/MpsCalc.Import.Tests/PanelSectionEndTests.cs: 0 of the five paths). Branch vs new main: diverged, ahead 2 behind 1; `git merge-tree --write-tree 6febe112 c72ba442` clean (tree 3baa977f). Compare base...head: exactly the five paths (+2-1, +1-1, +2-2, +1-1, +3-3). Commits: one parent each, author and committer the same Datasec address, attribution line present.

## AUTHORITY: holds
decision_queue.sh show: status ruled, client_project (Datasec/MPS), choice a, ruled 2026-11-18T08:38:02; option a detail "Yes to all three: contract changes with the docs; 195 recorded as agreed; 207's three words added with a test". Covers docs/api/openapi.json for MPSCALC-410.

## Findings
| # | Sev | Finding | Recommendation |
|---|---|---|---|
| 1 | Minor | docs/API.md:709 is 184 characters (the new wrapped line plus the untouched tail). The file already has 53 lines over 150 characters at base (54 at head). | Leave. A rewrap would touch bytes outside the frozen words. |
| 2 | Info | SOURCE.txt names commit e7a7436, which a squash does not carry. contract.test.ts checks only the sha256 line in SOURCE.txt and schema.ts header against the snapshot; contract.sync.test.ts compares bytes only (contract vs snapshot, schema body vs generator output). Neither reads the commit id. | Hosted CI cannot fail on it. Land as is. |
| 3 | Info | npm audit at base (lockfile blob 610a0767 identical at base and head): `--omit=dev` 0 vulnerabilities; full audit 12 high (dev toolchain, vitest path). ci.yml runs no audit step (CodeQL is the org default setup). | Optional low-priority ticket for the dev toolchain; not related to this change. |
| 4 | Info | Wording check passed: validating (lowercase) and Retired count (ordinal `is not` on the three words; rows B520States :47-54), so "a state word the server does not know" is correct and complete; Draft, Failed Validation, Expired do not count (:56-64); Validating, Active, Superseded count (:66-). The version being validated is excluded from "others" (`g.VersionId != version.VersionId`), a nuance the old and new text share. | None. |
| 5 | Info | Whole-solution dotnet test was run at head (pre-#212 base), not on the merge with #212; the two lanes share no file. | Hosted CI is the arbiter. |

No Blocker, no Major.

## Evidence
1. Words vs code: SourceDocumentChecks.cs:80-94 and :399-407, SourceGovernance.cs:9-20 read at base; E1 and E2 are true, complete, not overclaiming.
2. Diff equals FROZEN WORDS: python string comparison of whole post-edit files vs base with the replacement applied: E1 old count 1, byte-equal True; E2 old count 1, byte-equal True; planted extra space differs (control). json.load of the contract ok. `did not fail` count at head: 0 in the whole tree (4 rows at base, in the four expected files). `git diff --check` rc 0.
3. Generator: `node scripts/sync-contract.mjs e7a743646ced1d40df4fc1aa82c1371b1a6b5513` from web/ in my clone (openapi-typescript 7.13.0, Node 26): `git status --porcelain` and `git diff` empty (0 diff against commit 2). cmp contract vs snapshot rc 0 (control: one added byte rc 1). SOURCE.txt blob 7796e611... equals `git hash-object docs/api/openapi.json`; sha256 300460ba... equals shasum of the snapshot.
4. Tests at head: contract.test.ts + contract.sync.test.ts 4 passed (4); npm test 1616 passed; npm run lint rc 0; `dotnet build MpsCalc.slnx -c Release` 0 Warning(s) 0 Error(s) (SDK 10.0.404); dotnet test: Engine 743, Import 196, Api 3663, all passed (load1 10.2 then 7.3 across about 2 min; slot -1 taken by mkdir and released by moving the holder file).
5. See finding 2.
6. See finding 3.
7. Scans over added lines and both messages: names (underscore-aware, control `_by_Kam_` fired) 0; B-number pattern 0 (control fired); card ids, secrets, hosts, uuids 0; non-ASCII added lines exactly 2 (U+00B7 in SOURCE.txt line 3 and the schema.ts header, the generator's own); Cf/Cc count per file equal at base and head (all 0); gitleaks base..head rc 0. CodeQL pre-scan rows: no added code, so none apply (added lines are docs, JSON and a generated comment).
8. Step 1 and 2: every changed path inside the lane (5 of 5); merge-tree clean.

## NOT RUN
Playwright, the Entra build, scripts/package.sh, the python job, CodeQL database analysis (no code added; csharp cannot extract on arm64). Whole-solution dotnet test on the merge with #212. Hosted CI is the proof for those.
