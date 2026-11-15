GATE B1581: GO WITH FINDINGS @ 632ca83 on main 27adb70

Tier G1 (customer document: policy PDF cover wording + date logic), round 1 of 2. Gate ran 2026-11-15 16:28 to 16:49 AEDT.
Findings: 0 Blocker, 0 Major, 2 Minor.

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | No row tells the release instant apart from `generated_at` on a released version. Every released row renders with `generated_at` equal to `released_at`, so a mutant whose released branch reads `context.generated_at` SURVIVES both the new file and `b59-policy-pdf-cover.test.ts`. In production this mutant behaves the same, because `apps/api/src/outputs.ts` passes the release instant as `generated_at` for released versions. It is a test gap, not a defect. Follow-up: add one row with `generated_at` != `released_at` on different Sydney days. | mutant MA: rc 0, no row failed (head image, built, sha256 of `policy-summary.ts` restored to `7172007249cf...`) |
| F2 | Minor | `dateWordsInZone` has looser input guards than `dateWords`. (a) An `undefined` zone does not throw: it silently reads the HOST zone, which on a UTC host is silent UTC (probe: `undefined` gives `3 October 2026` under TZ=UTC and `4 October 2026` under TZ=Pacific/Kiritimati). (b) It skips `dateWords`'s `^\d{4}-\d{2}-\d{2}` shape check, so `"October 3, 2026 20:00:00"` renders where `dateWords` throws. Neither can be reached today: `time_zone` is a required `string`, the only brand any render gets is the `DATASEC_DEFAULT_BRAND` constant (`outputs.ts:316`; there are no other `brand:` sources in non-test code), and every instant comes from SQL `TS()` with a `Z` suffix (`queries.ts:9`). Follow-up: add a `typeof timeZone === "string"` check and the same shape regex. | zone probe (`out/p2-head/probe-out/zone-*.txt`) |

## Key questions, answered by program

- **Cover day across the DST edges and host TZ.** Gate's own probe at head, run under host TZ UTC, America/Los_Angeles and Pacific/Kiritimati: a 15-minute sweep from 2025-12-01 to 2027-12-31 (73,056 instants) matched an independent hand-coded NSW DST oracle every time (0 mismatches). Oracle control: a fixed +10 disagrees 732 times in 2026. Edges: 2026-10-03 13:59:59Z gives 3 Oct and 14:00:00Z gives 4 Oct; 2026-10-04 12:59:59Z gives 4 Oct and 13:00Z gives 5 Oct; 2027-04-03 12:59:59Z gives 3 Apr and 13:00Z gives 4 Apr; 2027-04-04 13:59:59Z gives 4 Apr and 14:00Z gives 5 Apr; 2026-12-31 13:00Z gives 1 January 2027. The sweep and edge lines are identical across all three host zones.
- **Red-first pair, re-run by the gate.** The new file ran on the base image (main source + the new test file) under five host zones (UTC, Los_Angeles, Sydney, Kiritimati, Pago_Pago). Every zone gave red 1, 2, 3, 5, 6, 7, 8, 12 and green 4, 9, 10, 11 (8 red / 4 green). The failing assertions are as the STATUS quotes them (`expected undefined to be 'Australia/Sydney'`, `'3 October 2026 (released, UTC)'`, `expected null to be an instance of RenderRecordError`, ...). At head: 12/12 green in all five zones.
- **Invalid zone is an error, never silent UTC.** `Mars/Olympus`, `""`, `" "`, `"Australia/Sydney "`, `AEST`, `"null"`, `null` and `123` all throw `RenderRecordError: not a time zone: ...`. Case variants, `Australia/NSW`, `Etc/GMT-10` and `+10:00` are accepted as real zones. The one exception is `undefined`, which falls back to the host zone (F2).
- **Gate mutants.** MB (catch returns the UTC `dateWords`) is killed by row 8. MC (day and month swapped) is killed by rows 2, 3, 4, 6, 7, 12 and b59 "page 1 is the cover". MD (released words keep ", UTC") is killed by rows 2, 5, 6, 7, 12. MA survives (F1). Control: a no-op pattern reports "did not apply".
- **No other output byte changes.** The gate rendered every kind (hpsm_preview, policy PDF, DOCX, evidence package, manifest, package manifest) for five inputs at base and head, under host TZ UTC, Los_Angeles and Kiritimati. The ONLY text differences are page 1's Date line of the policy PDF (for example `-3 October 2026 (released, UTC)` / `+4 October 2026 (released)` and `-12 September 2026 (draft generated, UTC)` / `+12 September 2026 (draft generated)`). Every other PDF page's text is equal, including page 3's summary `(UTC)` sentence and the appendix ISO instants. Preview, DOCX, evidence zip and manifest bytes are equal at base and head. The package manifest is equal once the brand hash and the policy PDF's sha256 are masked. Six refusals (released versions without a signature) are the same on both sides.
- **W-b.** Exactly two customer strings change in `src`: the `(draft generated, UTC)` and `(released, UTC)` template tails lose `, UTC`. The diff adds one other string, the internal `not a time zone: ${timeZone}` RenderRecordError. It mirrors `not a date:`, apps never map RenderRecordError to a message, and a constant zone cannot reach it. It is not a customer word. `dateWords` and the summary's `(UTC)` lines are byte-equal.
- **Brand hash.** The default brand hash moves from `0db6ec89...` to `3708bf15...`. Only these read it: `render.ts:174` (computes it), `routes/outputs.ts:305` (INSERT), `outputs.ts:72` / `stored-outputs.ts:67` (column lists) and `package-manifest.ts:99` (copies each artefact's own value). Nothing compares a stored `brand_profile_hash` with a fresh render's. No 64-hex brand literal exists in renderers or api.
- **PR #85's `b59-policy-pdf-cover.test.ts`.** Unedited, it gives 12/12 green at head under TZ Los_Angeles and Kiritimati, and inside the full renderers run.

## Steps

1. Refs: `ls-remote` gives branch = `632ca83c26d1fa7b4e99def6d36bc7b316c07e90` and main = `27adb70991ff3d7ec13f0732de6ecdcb1aab8043`, read at 16:28 and again at 16:49. One commit, parent = main, author = committer = `88359143+kamilDatasec@users.noreply.github.com`. 4 of 4 paths are inside the kit's closed list. Open PRs: #85 only (draft). #85 holds 0 of the 4 paths (control: `document-pdf.ts` gives 1). The sibling lane was dropped.
2. Merge: `git merge-tree --write-tree` exits 0. Tree `7e6e405b` equals the head tree, which equals main plus the 4 head blobs (control: against main^ it gives 5 paths).
3. CI (CI image, node v22.23.2, ICU 78.2, tz 2026a, `--network none`, under the project heavy lock):

| Check | main | head (= merge tree) |
|---|---|---|
| lint / format:check / typecheck / build | rc 0 each | rc 0 each |
| vitest renderers | 31 files, 266 passed, 1 skipped | 32 files, 278 passed, 1 skipped |
| vitest workspace | 2908 passed, 2 failed | 2908 passed, 2 failed |
| test-db.sh (db / api) | 674 / 1563 passed | 674 / 1563 passed |
| gitleaks over the tree (pinned image, pinned config) | no leaks | no leaks |

The 2 workspace reds at both main and head are `packages/content/src/citations.test.ts`'s two SOW rows (withheld text not mounted). Test-name multiset: renderers lost 0, added 12 (all from the new file); workspace lost 0, added 0. Control: dropping one name reports lost 1. Secret-scan self-test: 7 PASS. Repo-wide hidden-character walk: 17 locations / 28 characters at both main and head (pre-existing intentional test fixtures), 0 in the added lines.
4. Red without the fix: as above (8/4 at base in five host zones).
5. Closed lines: FACT 3 re-verified (the only render brand is the constant). FACT 4 re-verified (no stored-hash comparison).
6. Probes: as above.
7. Scans over the 166 added lines and the commit message: names (underscore-aware, ban list) 0, B-numbers / seat words 0, GUIDs 0, hosts 0, sensitive names 0, non-ASCII 0, Cf 0. The control (`_by_Kam_`, `_by_Waite_`, `B1581`, U+200B) fires on every one. CodeQL rows: 0 `new RegExp(`, 0 hand-escape, 0 innerHTML / child_process. CodeQL CLI v2.27.4 `javascript-code-scanning.qls`: 0 results at base and head, 87 rules, 839 vs 840 files extracted (the new test file is in the database). There was no planted positive control for CodeQL.
8. Claims in the builder STATUS:
   - True: red-first 8/4 and head 12/12; head checks = base + 12; renderers 266 -> 278; workspace 2908 + 2 SOW reds; test-db 674 / 1563; names lost 0 / added 12; `git diff --stat` 4 files +166 -2; hunks limited to the new function and the two cover lines; identity; branch at the stated sha; main unmoved; kit copy byte-equal (`cmp`); no `pc-b1581-*` containers or images left; brand-hash census.
   - Partly re-shown: mutants M1 to M6. The gate re-ran a different set: MB is an M5 equivalent, MD and MC are new. M1 to M4 and M6 were not re-run by the gate.
   - Not shown (fenced from the gate): the Jira GET contents and the PR-history count (129).
9. Tier: G1 as stamped. No security-shaped issue found.

## Notes for the coordinator (not findings)

- The new test file's NAME carries the work number (`b1581-cover-date-time-zone.test.ts`). The kit set this name and it follows repo convention (`b59-`, `b323-`, `b113-`). It is in a path, not in an added line or the message. `pr-body.txt` does not name the file.
- PR #85 edits `policy-document.ts`, `document-pdf.ts` and `b59-policy-pdf-cover.test.ts`. If #85 lands first, re-run the new file on the new main before landing this one.
- The cover-vs-summary day mismatch for releases between 00:00 and 10:00/11:00 Sydney time is the ruling's own scope (cover only). It is named in the PR body.
- Landing is head-pinned squash (C-101 (1) form). Read hosted CodeQL first. Merging deploys nothing: Composer deploys only on the product owner's card, and the repo holds no `.github` workflow.

## NOT RUN

- Hosted CodeQL and hosted checks (the PR does not exist yet); hosted CodeQL is the proof.
- The `ci.sh` compose-stack steps (stack up, health, RLS, egress, edge, switches) and the bridge (.NET) image and tests. This change touches only TypeScript renderer code; hosted / Tuesday's CI is the proof.
- `secret-scan.sh --history` and the hook steps (the gate's tree is an archive with no git history; gitleaks was run over the tree with the pinned image and config).
- The two `citations.test.ts` SOW rows (withheld text never mounted; red at both main and head).
- Builder mutants M1 to M4 and M6, as written.
- The Jira and PR-history claims (fenced).

Gate work: own clone and archives in the session scratchpad; heavy lock taken and released 5 times through `.tools/g1581/scripts/heavy.sh`. All `pc-g1581-*` containers and the images `pc-g1581-node:base` / `:head` were removed by exact name; no `pc-dbtest` leftovers. Nothing was pushed, opened, written to Jira or deployed.
