# hold_ready.py doc_patch arms — Tue 22 Sep 2026 11:24:35 AEST

backup: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py.pre-1118-docpatch
backup check (taken BEFORE any edit, cp -p): `cmp` against the 10:28 pre-edit code was rc=0 at creation; size 60213 B, mtime Sep 22 10:28:23 2026. Now: 673 lines (backup) -> 1016 lines (hold_ready.py).
diff stat: 354 insertions / 11 deletions (diff lines)

## Defect reproduction (OLD code — the backup — on the doc PASS 8/8 run)
hold_ready: REFUSE — input.json is neither test_only (test_file) nor code_patch (product_file + suggested_test_file): keys ['defect_line', 'files', 'product_file', 'repo', 'ticket', 'tip']
rc=2 (recorded at capture)

## Arm A — regression: test_only --dry-run on runs/2026-09-22_ks947-ornith35b-night2 (golden -) (BEFORE captured on the backup at 11:18, AFTER on the final code)
clock-normalised diff rc=0 (5 / 5 lines); raw cmp rc=1 (the clock stamp only when 1); AFTER rc=0
VERDICT: PASS (A regression)
AFTER output (first 2 lines):
DRY-RUN OK → READY_KS-947-F3F4b-R16_ornith35b-q4_BRIEFED-TESTONLY-MFA-LIMITER-OPTION-PARITY-AND-SPEC-MAX-PASS-8of8_2026-09-22.diff.md
  golden: golden not located — no byte-identity claim is made

## Arm B — regression: code_patch --dry-run on runs/2026-09-22_ks1265-ornith35b-night with golden feed3/1265EARLYGUARD-R16 (BEFORE captured on the backup at 11:18, AFTER on the final code)
clock-normalised diff rc=0 (5 / 5 lines); raw cmp rc=1 (the clock stamp only when 1); AFTER rc=0
VERDICT: PASS (B regression)
AFTER output (first 2 lines):
DRY-RUN OK → READY_KS-1265-EARLYGUARD-R16_ornith35b-q4_BRIEFED-CODEPATCH-ISSUERNAME-AT-GUARD-BEFORE-SAVE-PASS-7of7_2026-09-22.diff.md
  golden: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (cont

## Arm C — regression: bash_patch --dry-run on runs/2026-09-22_ks1139-ornith35b-night with golden feed8/ERREXIT (BEFORE captured on the backup at 11:18, AFTER on the final code)
clock-normalised diff rc=0 (5 / 5 lines); raw cmp rc=1 (the clock stamp only when 1); AFTER rc=0
VERDICT: PASS (C regression)
AFTER output (first 2 lines):
DRY-RUN OK → READY_KS-1139-1139ERREXIT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-VALIDATE-LINT-ARITHMETIC-COUNTERS-UNDER-ERREXIT-PASS-7of7_2026-09-22.diff.md
  golden: the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/ERREX

## Arm D1 — doc FAIL run (runs/2026-09-22_ks1097-ornith35b-night, RESULT: FAIL (1 failed) — stopped at D2): refused
rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1 failed) — stopped at D2; FAIL lines: ["FAIL D2 diff does NOT apply at the tip: strict: error: patch failed: Blockchain/Dev/CONTRIBUTING.md:463 error: Blockchain/Dev/CONTRIBUTING.md: patch does not apply  | reanchored: hunk 1: ambiguous — the 1 '-' line(s) occur 0x in the file; kept as written hunk 2: reanchored at 474 (1 '-' / 1 '+' lines; model header -471,7 +471,7)  error: patch failed: Blockchain/Dev/CONTRIBUTING.md:463"]
VERDICT: PASS (D1 doc FAIL refused rc 2 naming the RESULT and FAIL lines)

## Arm D2 — artefact contradiction: scratch COPY of the PASS run with apply_check.out made NON-EMPTY while the D2 line says (strict); the run dir itself is never modified
rc=2
hold_ready: REFUSE — D2 line claims (strict) but apply_check.out is 'NON-EMPTY: error: patch failed: Blockchain/Dev/CONTRIBUTING.md:608'
VERDICT: PASS (D2 strict-claim vs apply_check.out refused)

## Arm D2b — converse: copy whose D2 line names --recount --ignore-whitespace while apply_check.out is EMPTY (strict was clean) and no apply_check_lenient.out exists
rc=2
hold_ready: REFUSE — D2 line names --recount --ignore-whitespace but apply_check.out (the strict check) is EMPTY (strict was clean)
VERDICT: PASS (D2b accommodation-claim vs artefacts refused)

## Arm D3 — task-type signals disagree: copy with the D0 line deleted from checker.out while night_meta.json says tasks/doc_patch
rc=2
hold_ready: REFUSE — task-type signals disagree: night_meta.json's task path says doc_patch=True but checker.out's shape (a D0 line, no `mode:` line, no B0 line) says doc_patch=False
VERDICT: PASS (D3 signal disagreement refused)

## Arm D4 — after.md tampered: copy with must_remove line 2 re-inserted into after.md (checker.out untouched, still PASS D7)
rc=2
hold_ready: REFUSE — after.md is not byte-equal to patch.diff re-applied to before.md (strict): sha256 d662157adac38de2 vs 3062451d0224713a
VERDICT: PASS (D4 after.md vs re-applied patch refused)

## Arm D4b — RESULT line contradiction: copy with RESULT: PASS (7/7) while the input's defect_line (3 must_remove, 2 expected_plus, no insert_after) gives 8
rc=2
hold_ready: REFUSE — RESULT line 'RESULT: PASS (7/7)' does not fit the input: the checker's formula gives 8/8 for must_remove=3 expected_plus=2 insert_after=None
VERDICT: PASS (D4b RESULT total vs input refused)

## Arm D5 — golden COPY with one '+' change line altered: must say DIFFERS with a count, never CONTEXT-ONLY
rc=0
  golden: DIFFERS from the drafter's golden `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/003907dd-5b0e-44fc-ad57-43f54dd51893/scratchpad/golden_d5/out.md.checker/patch.diff` (`cmp` rc 1): 2 change line(s) (`+`/`-`, ndiff) differ (run 5 vs golden 5); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0 — read the diff before raising
VERDICT: PASS (D5 altered golden reported DIFFERS (2 = the ndiff pair))

## Arm D5b — golden COPY with only hunk 2's header given a trailer: CONTEXT-ONLY, hunk headers named
rc=0
  golden: CONTEXT-ONLY difference from the drafter's golden `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/003907dd-5b0e-44fc-ad57-43f54dd51893/scratchpad/golden_d5b/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 1110 B vs golden 1129 B): change lines (`+`/`-`, ordered) IDENTICAL (5); context/empty lines run vs golden: 7/7 context; hunk headers differ (run `@@ -613,5 +612,5 @@` vs golden `@@ -613,5 +612,5 @@ - **GitHub Actions`); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0
VERDICT: PASS (D5b header-only difference reported CONTEXT-ONLY)

## Arm D6 — golden '-': no identity claim
rc=0
  golden: golden not located — no identity claim is made
VERDICT: PASS (D6 no golden -> no claim)

## Arm D7 — --title-from-brief: (a) positional title WRONG-TITLE disagrees with the derived one; (b) the PRPROCESS brief (same ticket, other part) is not the brief located by ROWID tokens; (c) 3-positional form derives and prints the line
(a) rc=2
title-from-brief: CONTRIBUTING <- line 4 `File: `Blockchain/Dev/CONTRIBUTING.md`` (basename 'CONTRIBUTING'); heading line 1 names KS-1097: `# KS-1097-C R16B-REVIEWREQ - re-brief at develop 8c2f7b3fd of READY_KS-1097-C_ornith35b-q4_DOCPATCH-`
hold_ready: REFUSE — --title-from-brief derived 'CONTRIBUTING' but the positional title is 'WRONG-TITLE' — they must agree
(b) rc=2
title-from-brief: CONTRIBUTING <- line 4 `File: `Blockchain/Dev/CONTRIBUTING.md`` (basename 'CONTRIBUTING'); heading line 1 names KS-1097: `# KS-1097-B R16B-PRPROCESS - re-brief at develop 8c2f7b3fd of READY_KS-1097-B_ornith35b-q4_DOCPATCH-`
hold_ready: REFUSE — --title-from-brief /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1097-R16B-PRPROCESS.md is not the brief located by ticket + ROWID tokens: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1097-R16B-REVIEWREQ.md
(c) rc=0
title-from-brief: CONTRIBUTING <- line 4 `File: `Blockchain/Dev/CONTRIBUTING.md`` (basename 'CONTRIBUTING'); heading line 1 names KS-1097: `# KS-1097-C R16B-REVIEWREQ - re-brief at develop 8c2f7b3fd of READY_KS-1097-C_ornith35b-q4_DOCPATCH-`
DRY-RUN OK → READY_KS-1097-REVIEWREQ-R16B_ornith35b-q4_BRIEFED-DOCPATCH-CONTRIBUTING-PASS-8of8_2026-09-22.diff.md
VERDICT: PASS (D7 title-from-brief derive + two refusals)

## Arm D8 — copy without night_meta.json (removed in the COPY): checker.out's shape alone (D0 line, no mode:, no B0) still detects doc_patch
rc=0
DRY-RUN OK → READY_KS-1097-REVIEWREQ-R16B_ornith35b-q4_BRIEFED-DOCPATCH-CONTRIBUTING-PASS-8of8_2026-09-22.diff.md
VERDICT: PASS (D8 shape-only detection)

## Arm E — the PASS run: hold_ready.py <ks1097 night2> <feed9/REVIEWREQ> REVIEWREQ-R16B CONTRIBUTING --title-from-brief <KS-1097-R16B-REVIEWREQ.md> --dry-run
pre-measured here, independent of the tool: `cmp` run patch.diff vs golden patch.diff rc=0; after.md rc=0
rc=0
title-from-brief: CONTRIBUTING <- line 4 `File: `Blockchain/Dev/CONTRIBUTING.md`` (basename 'CONTRIBUTING'); heading line 1 names KS-1097: `# KS-1097-C R16B-REVIEWREQ - re-brief at develop 8c2f7b3fd of READY_KS-1097-C_ornith35b-q4_DOCPATCH-`
DRY-RUN OK → READY_KS-1097-REVIEWREQ-R16B_ornith35b-q4_BRIEFED-DOCPATCH-CONTRIBUTING-PASS-8of8_2026-09-22.diff.md
  golden: the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/REVIEWREQ/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0
  touched=['Blockchain/Dev/CONTRIBUTING.md'] hunks=2 plus=2 minus=3 removed=3 added=2 sections=1 mode=strict strict=True fence_same=True nonascii=0 total=8/8
  header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 11:24 2026-09-22; sha256[:16] 58b583ae7bd59f2f, 1110 B — a BYTE count; byte-equal to the out.md fence (the model's as-written block)). Checker D2 (verbatim from checker.out): `PASS D2 diff applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/REVIEWREQ/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0.
  prnote: **PR NOTES for the raise seat:** DOC_PATCH — DOCUMENTATION ONLY, zero code bytes: `Blockchain/Dev/CONTRIBUTING.md` (+2/-3 per patch.diff); one file. Apply `patch.diff` strictly (`git apply -p1`) at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Tier: tier 1 (documentation) — the gate dec
VERDICT: PASS (E REVIEWREQ BYTE-IDENTICAL + after.md identical)

## Arm totals: PASS 15 · FAIL 0 — Tue 22 Sep 2026 11:24:37 AEST
run dirs untouched: 22 Sep 10:33 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/REVIEWREQ/out.md.checker/patch.diff;22 Sep 11:05 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night/checker.out;22 Sep 11:06 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/checker.out;

## REAL HOLD — Tue 22 Sep 2026 11:24:50 AEST
(Arm D2 note: the tool refused on the FIRST run of the script too — rc 2, `apply_check.out is 'NON-EMPTY: …'` — but the ARM's grep pattern lacked the repr quote and scored it FAIL; the pattern was corrected and the whole script re-run: 15/15. A script-side slip, not a tool one.)
### REVIEWREQ — hold_ready.py <ks1097 night2> <feed9/REVIEWREQ> REVIEWREQ-R16B CONTRIBUTING --title-from-brief <KS-1097-R16B-REVIEWREQ.md>
title-from-brief: CONTRIBUTING <- line 4 `File: `Blockchain/Dev/CONTRIBUTING.md`` (basename 'CONTRIBUTING'); heading line 1 names KS-1097: `# KS-1097-C R16B-REVIEWREQ - re-brief at develop 8c2f7b3fd of READY_KS-1097-C_ornith35b-q4_DOCPATCH-`
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1097-REVIEWREQ-R16B_ornith35b-q4_BRIEFED-DOCPATCH-CONTRIBUTING-PASS-8of8_2026-09-22.diff.md
  golden: BYTE-IDENTICAL; touched=['Blockchain/Dev/CONTRIBUTING.md'] hunks=2 plus=2 minus=3 removed=3 added=2 sections=1 mode=strict strict=True fence_same=True
rc=0
## Post-hold verification (read back from the READY)
fences=1 fence1==patch.diff (bytes): True
RESULT line quoted verbatim: True -> 'RESULT: PASS (8/8)'
every PASS/INFO D-line of checker.out quoted verbatim in the READY: True (10 lines)
brief located: True; golden verdict: BYTE-IDENTICAL; H1: # READY — KS-1097-REVIEWREQ-R16B (Ornith, briefed, doc_patch, markdown) — PASS 8/8 — HELD for QA
no 'strict' claim contradiction: D2 says (strict) in checker.out = True, READY PR NOTES say strictly = True
 M 2_Project_Files/local-model/night/hold_ready.py
?? 2_Project_Files/local-model/night/READY_KS-1097-REVIEWREQ-R16B_ornith35b-q4_BRIEFED-DOCPATCH-CONTRIBUTING-PASS-8of8_2026-09-22.diff.md
?? 2_Project_Files/local-model/tests/hold_ready_docpatch_arms_2026-09-22.md
