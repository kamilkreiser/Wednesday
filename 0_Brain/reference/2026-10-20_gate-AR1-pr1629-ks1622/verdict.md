VERDICT: GO WITH NOTE at head cb776bfc4b20... (tier 2, round 1 of 2; landing tree 985fd9f982a8c4bc987258cb6a99086a72958a79 on develop 390cc0a317c9bc36c19f3a1684c745836af485df; 0 blockers, 3 notes)
model: claude-sonnet-5-5 -- tier-2 gate row (api-gateway audit-log logging) -- P1-P4 no -- gauge 49%

## BLUF
- One added log line, `if (!r.ok && collected.length === 0) logger.warn(...{ status, windowsRead })`. The change line is byte-identical to the Spark pass, and the test blob equals the declared one.
- Behaviour measured: a JSON 500 or 401 on the first window logs exactly one warn at the PR head and none on develop. The warn carries only the route name, a numeric status and windowsRead, so nothing secret or tenant-specific can print.
- All three mutants and the E1-E5 cells fail as claimed. Landing tree and suite figures match: merge-tree 985fd9f9... = predicted, 1163/1163 in 119 files, three-dot = the 2 files.
- Notes only: the non-JSON double-warn residue is real (N1), and the existing catch line prints a few body characters (N2, pre-existing). No cell pins the double warn (N3).

## Heads
ls-remote at start and again before this verdict: #1629 = cb776bfc4b20346cdec60887c74077eb2dd50bc5, develop = 390cc0a317c9bc36c19f3a1684c745836af485df. Both equal the brief. Develop tree 6a8a19bc... (equals AQ1's figure). Merge-base of the PR and develop is 46e4343a (not develop's tip).

## Q1 Identity to the Spark pass: CONFIRMED
- Change line: `git diff dev...pr1629` of platform.ts, `+` line with the `+` stripped, sha256 `9ae75454da3f...a344eb`. The same line taken from the Spark READY diff gives the same sha256. Positive control: a different string gives `73cb3858...`, so the compare can tell lines apart.
- Test blob: `git ls-tree pr1629` gives `9cfe0e6a25312a5b19b44998cb095916372f7402` = declared `9cfe0e6a2`.
- Whole-file post-image differs: Spark `b44ccc9c1` (on pre-image `eee7fe895`) vs PR `08c8dd27`. The pre-image moved: `git log 83ed01af..dev -- platform.ts` is exactly one commit, 31cfb44dc (KS-1195), +76 lines at `@@ -134` and +12 at `@@ -768`. The PR's own diff against develop is exactly 1 line, so the difference is the pre-image and not the change.
- The commit says "byte-for-byte" and "hunk applies unchanged at develop": true for the change line; the hunk context moved (:420 to :490).

## Q2 Behaviour: CONFIRMED, with N1/N2
Instrument: a throwaway probe test (copy of the PR's harness plus modes html-502, null-200, obj-200), run at the PR head and with the line removed (= develop's behaviour). Probe file moved out of the clone afterwards.
- Develop, first window JSON 500: warns = [] (silent). PR: exactly one warn `[route text 'upstream answered an error status', {status:500, windowsRead:0}]`.
- Non-JSON 502 text/html, body containing `SECRETBODY tenant=acme token=abc` and header `X-Secret`: develop 1 warn (the catch). PR 2 warns (the new line, then the catch). Author's residue re-measured and CONFIRMED.
- Secret/tenant data: the new line prints `status` (number) and `windowsRead` (number) only. No headers, token or body. Positive controls: E2 asserts the 401 body text is absent; mutant M4 (adds a header field to the meta) reds E1 and E2, so the cells do detect extra fields. In the probe, `SECRETBODY`, `acme`, `token=abc` and `hdr-secret` appear in neither warn.

## Q3 Cells can fail: CONFIRMED
Run via `node <clone>/node_modules/.bin/vitest run --root <clone>/.../api-gateway`; shared built first. Green: 5/5.
- M1 line removed: 2 failed | 3 passed (E1, E2 red). Matches the author.
- M2 fire on any window (drop `collected.length === 0`): E3 red (1 failed).
- M3 fire on every first window (drop `!r.ok`): E3 and E5 red (2 failed).
- M4 extra meta field: E1 and E2 red.
- Restored file cmp-equal to the original; 5/5 green again.

## Q4 Scope: CONFIRMED
Probe: a 200 with `{success:true}` (not a list) and a JSON `null` 200 both log [] at the PR head and at develop. Untouched, still open. Commit subject begins `Refs KS-1622`. The PR body itself was not read (see NOT RUN).

## Q5 Landing: CONFIRMED
- `git merge-tree --write-tree dev pr1629` = 985fd9f982a8c4bc987258cb6a99086a72958a79 = predicted. A real `merge --no-ff` in the clone gives the same tree. Control: develop's tree 6a8a19bc and the PR tree dfb6629a differ from it.
- Full api-gateway suite on the landing tree: 119 files passed, 1163 tests passed (author: 1,163 in 119).
- Type-check: `tsc --noEmit -p tsconfig.test.json` (this one includes `src/__tests__`; the build tsconfig excludes it). The new test file is in the program (--listFilesOnly lists it); 27 errors, none in ks1622, and the error set is identical line for line to develop's 27 (control: the check does emit errors, so it is live). The build tsconfig is clean (no output).
- Three-dot diff = 2 files (the platform.ts line and the new test).

## Notes
- N1 (residue, confirmed): a non-JSON error body now logs two warns (new line, then the catch's `Unexpected token '<'...`), one on develop. Both true, noise only. The cells' "ONE warn" holds for JSON bodies only, as the author said.
- N2 (pre-existing, not introduced here): the existing catch line carries `err.message`; for a non-JSON body that is V8's JSON.parse message, which includes the first ~10 characters of the upstream body (probe: `"<html>Bad "...`). The PR neither adds nor widens it, but an upstream HTML error page could put a few body characters in a log. Worth its own ticket, not a blocker here.
- N3: no cell pins the non-JSON double-warn behaviour (E1-E5 are JSON bodies, plus destroy and a second-window 503), so the residue is documented but unguarded; a later change that fixes or worsens it would pass the suite.

## NOT RUN
- The PR body and GitHub state (no gh, no GitHub reads beyond ls-remote); "Refs" was checked from the commit message only. The author's 4,825 B body claim is unchecked.
- The ratchet (154 files / 27 errors) was reproduced as the 27-error set via tsc, not through the repo's ratchet script.
- npm ci ran with `--ignore-scripts`; no postinstall steps, no lint, no other workspace suites, no Docker, no live upstream.
- The Spark checker itself was not re-run (it has no golden and ran at an older tip); only its change line and blob were compared.
- `git -C /Volumes/DevMASTER/WEDNESDAY status --short` filtered for anything outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/: none. No node_modules at Wednesday's root or 2_Project_Files.

ebd858f381cbfcc4ebc4a01dd2c447ce74818f7ebfd784574e3c62ed4960bd4b
