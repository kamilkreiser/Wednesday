GO WITH NOTES
DEVELOP YAML IN SYNC (at 7eda23b34d3b7a413ca8f9c0945c7843708ce9f4; PR 2072 was NOT yet merged at that SHA)

Item A: PR 2092 head 3d8423f71024af5bbaf9b12d733923d86d7d14b0 (unchanged start to end), tested against develop 7eda23b34d3b (develop moved from the pinned 765701307eb3; merge-base cfb6c1573ba9). Tier 2, compare gate on gate 230 F1, F2 wording, F3. Item B: develop 7eda23b34d3b (read at start 23:44 and at end 23:51, same SHA).

## Item A

### BLUF
- F1 CLOSED, measured. F3 CLOSED, measured. F2 wording: fixed in the texts, the 61-of-63 figure is the builder's and I did not repeat it (it belongs to the round-1 head, which no longer exists as a separate head).
- Verdict and exit code unchanged: 26 value shapes through validateBaseline and validateOutOfScope, develop vs head: pass/fail pattern IDENTICAL on both validators. Only wording moves.
- Merge tree on develop 7eda23b34d3b: rc 0, tree 1a2661be345f8188dfd3af8d9e1080adf76ced95, no conflicted files.
- audit:contract at head: 75 tests, 75 pass, 0 fail; expected-case-count file = 75 (equal).
- Notes, none blocking (below).

### F1 (wrong-type expires printed as missing): CLOSED
FOUND: baseline-contract.mjs isWrongTypeExpiry/showValue (new), validateBaseline branch; lock-discovery.mjs ~281-292; printBaselineProblems splits the malformed text out.
TESTED / HOW: probe.mjs (in scratchpad) feeds 26 shapes to both validators and the printer at develop and at head.
- Develop (control, the defect): number, 0, true, false, [], ['2099-01-01'], {}, Date, BigInt, function, symbol, NaN, cyclic object all print `missing expires` in both validators (44 `missing expires` lines in the develop output). Positive control that the defect exists as F1 said.
- Head: every one of those prints `expires is present but malformed (not an ISO YYYY-MM-DD date: <value>)` on its own line, value quoted; BigInt/function/symbol print `<bigint>`/`<function>`/`<symbol>` (no crash); cyclic object and revoked Proxy print `<object>`.
- undefined, null, "", "   " still `missing expires` at head, in both validators.
- Grandfathered row with wrong-type expires: not reported (cell pins it; passes).
- Verdict pattern develop vs head: identical for all 26 (diff of the two pass/fail tables empty; table has 26 rows).

### F3 (padded dates): CLOSED
Padded " 2099-01-01 ", "2099-01-01\n", "\t", leading, trailing: malformed in both validators at head (probe: padded, nl, tab). My tamper D in BOTH validators (`isIsoDate(entry.expires.trim())` in validateBaseline, and in validateOutOfScope), run on the head worktree: baseline D1 74/75, 1 red "a date with whitespace around it is MALFORMED, not accepted by a trim (F3)"; lock-discovery D2 74/75, 1 red "...not read as a lapsed date (F3)". Clean control run 75/75. Restored by git checkout, sha256 of both files equals the original (shasum -c OK).

### F2 wording
Cheat and flow fragments say "the round-1 test file run against base source" 61 of 63, attributed to Seat R 86th, not repeated; follow-up red-first is stated separately (73 tests, 71 pass). Wording is honest about provenance. My own measurement of a related figure: the HEAD's 75-case test files run against develop source = 75 tests, 68 pass, 7 FAIL (rc 1), the seven reds being the F1/F3/print cells; so the new cells have teeth against develop. (This is not the builder's 71-of-73 figure and is not offered as repeating it.)

### Anything beyond the findings in the 7 paths
Seven paths: baseline-contract.mjs, baseline-contract.test.mjs, expected-case-count, lock-discovery.mjs, lock-discovery.test.mjs, two fragments (cheat, flow). Beyond F1/F3:
- The round-1 printer change (baseline sibling, printBaselineProblems now prints malformed apart from missing, `startsWith(MALFORMED_EXPIRES_PREFIX)` split, data shape `{id, missing[]}` unchanged) is part of this diff: it is the KS-1209 baseline half, and the fragments say so. Judged fine. My tamper M2 (disable the "missing" print line) goes 72/75, 3 red.
- My tamper M1 (null counted as wrong-type) goes 73/75, 2 red (the null/absent control cells). Cells are not passing for the wrong reason.
- The new count math is right: 62 + 13 new cases (4 printer, 5 baseline follow-up... counted by diff: baseline file 9, lock-discovery file 4) = 75, and runner total 75.
- check-npm-audit.mjs still imports isIsoDate and nonEmpty only and keeps its own wording (read); the fragment's claim about it is true.
- Fragment claims "both gates rc 0 on the real baseline (8 reported, 8 baselined)" and the real-bad-baseline CLI run: NOT repeated (needs advisory fetch).

### Notes
1. NOTE, info. showValue(NaN) prints `date: null` (JSON.stringify(NaN) is "null"), so a NaN expires is quoted as null while null itself prints `missing`. Verdict unchanged (refused); wording slightly confusing. Probe row "NaN". MEASURED. Fix shape: add NaN/Infinity to the type-name branch.
2. NOTE, info. A boxed `new String('2099-01-01')` is quoted as "2099-01-01" (JSON.stringify unwraps it) and so reads like a valid string; still refused and still malformed. Probe row "strObj". Very low reach (JSON baseline cannot carry it).
3. NOTE, info. Fragment text "thirteen new cases (four first round, nine follow-up)": consistent with 62 -> 75 and with the per-file diff, I found no mismatch.

### Merge tree
git merge-tree --write-tree --name-only origin/develop pr2092 (develop 7eda23b34d3b): rc 0, tree 1a2661be345f8188dfd3af8d9e1080adf76ced95 (same at start and end).

## Item B: OpenAPI drift on develop

Checked SHA: 7eda23b34d3b7a413ca8f9c0945c7843708ce9f4. This develop contains PR 2077 (merged, 765701307eb3 is its ancestor) and does NOT contain PR 2072: ls-remote refs/pull/2072/head = 14f402572f1a still open, develop head moved only by KS-1448 on top of 2077. So the "second edit merged by a text union" has NOT happened on the SHA I checked; I could not test it. Re-run after 2072 merges.

Command found: `check:openapi` in Blockchain/Dev/package.json = `npm run generate-openapi -- --check && npm run check:spec-examples`; generate-openapi = `npm run build --workspace=packages/shared && tsx scripts/generate-openapi.ts` (read before running; --check compares yaml.stringify(doc, lineWidth 100) to docs/openapi/secuura-api.yaml byte for byte, exit 1 on difference, exit 2 on the KS-424 security guard). Run as `npm --prefix .../Blockchain/Dev run check:openapi`, TMPDIR=/private/tmp/g262t.
- generate-openapi --check: rc 0, "CHECK PASS: on-disk YAML matches generated" (41615-line yaml).
- full check:openapi: rc 0, check-spec-examples "422 example blocks ... OK".
- PLANTED CONTROL: appended " X" to line 20 of the committed yaml in my clone: --check rc 1, "CHECK FAIL: generated YAML differs from on-disk version". Restored by git checkout; sha256 equals the pre-edit hash (shasum -c OK).
- Environment note: my first attempt used the project checkout's node_modules (zod 3.25.76, stale vs lockfile's 4.6.7) and failed `tsc` in packages/shared (10 type errors in zod3-compat.ts): my environment, not develop. The passing run used node_modules copied from another gate's install (/private/tmp/g258, zod 4.6.7, package-lock.json sha1 identical to develop's 295b276a...). Worth knowing: the project's own 2_Project_Files node_modules is stale and cannot run this check.

## Controls
- F1 defect positive control: develop prints `missing expires` for 13 wrong-type shapes (probe_base.out); head does not.
- Absence controls: undefined/null/""/blank still missing at head (probe rows); valid future date PASS, lapsed 2020-01-01 stays the LAPSED message (probe rows valid, lapsed).
- audit:contract clean 75/75 before every tamper; restored files sha256-checked.
- Item B drift positive control above.

## NOT TESTED
- The merged tree (merge-tree only; audit:contract not run on it).
- Real audit:gate / audit:locks CLI runs (advisory fetch, network), the builder's "8 reported, 8 baselined" figure, and a real bad-baseline CLI print.
- Builder's 6 tampers (I ran 4 of my own: D1, D2, M1, M2), round-1's 61 of 63, red-first 71 of 73.
- Node 24 / an LTS Node (everything ran on v26.8.1).
- Item B after PR 2072 merges (the union-merged yaml). Also not run: Schemathesis/Akto and other consumers of the yaml; the pre-push hook's own spec-drift leg (I ran the package script it wraps).
- The docs-check on the fragments (read only).

## Conduct
Clone /private/tmp/g262 (partial blobless, 186M) plus worktrees /private/tmp/g262w (4.5G total, three worktrees including copied node_modules; head, base, dev2) and /private/tmp/g262t (3.2M). Not removed (no-rm); I left them for quarantine. Git write verbs only inside /private/tmp/g262. Worktree base also holds head's two test files copied over develop's (a red-first run). One network use: git fetch via the project deploy key. Nothing under !CODING written; DevMASTER free 25 GiB at end; load1 peaked about 5. Probe script: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/feffd0e4-3700-4424-8fe3-694754982c10/scratchpad/probe.mjs. Nothing posted. Early commands were refused by hooks (cd, write verb through a variable path, `======` word); no writes escaped.
