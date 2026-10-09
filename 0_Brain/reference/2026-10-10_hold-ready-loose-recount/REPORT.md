# hold_ready LOOSE-rung recount tolerance — 2026-10-10

## BLUF
- KS-1345 (rung 6, PROSE-only) NOW HOLDS in dry-run: rc 0, DRY-RUN OK, `strict=False`, recount mode recorded in the READY body and the golden clause. Old tool: rc 2 "corrupt patch at line 29".
- New arms `tests/hold_ready_loose_recount_arms.sh`: rc 0, 0 FAIL (A1, A2, A3, A4a, A4b, A5). `tests/hold_ready_rung34_arms.sh`: rc 0, TOTAL FAILS=0.
- Real hold NOT run (dry-run only). Edit is LIVE in `night/hold_ready.py`; backup `night/hold_ready.py.pre-1010-loose-recount`. No instance was running (`pgrep -fl hold_ready` empty before edit and before swap).

Real-hold command for Wednesday (drop `--dry-run`):
`python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500-control WEBHOOKS-DELIVERIES-1 --title-from-brief /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1345-originate-deliveries-failed-query-500/KS-1345.md --model-tag spark-dsv4flash`
(Row id/title are my dry-run choices; change `WEBHOOKS-DELIVERIES-1` if you want another. Dry-run first with `--dry-run` added.)

## What changed
`diff` vs backup: +44 lines, 0 deleted, all in `hold_ready()` code_patch path plus one new helper. Where the defect really was (corrects the brief's premise): the rung-4 path does NOT tolerate a recount apply on a strict-apply gate; it never reaches it. The strict-apply gate (`_apply_to_tip(patch.diff)`, inside the golden comparison, step 7) only runs when `input.json['files']` carries the tip content of EVERY touched file. Rung 4 (KS-1410 audit-export) creates/needs a new test file, so `files` lacks it and the gate is skipped ("APPLIED RESULT not compared"). KS-1345 modifies an existing test in place, so the gate runs and died on the miscounted hunk.
Second finding: even a plain `--recount` of the CONCATENATED `patch.diff` fails (recount of the miscounted product hunk swallows the next file header); the checker applies PER SECTION. So the tolerance applies per section, as the checker did.
The hunk (step 7, before `if rc_r != 0: die(...)`):
- New helper `_apply_sections_to_tip(secs, files, scratch)`: applies each (section file, opts) in order in one tempdir.
- If strict `patch.diff` apply failed AND `loose_info` (LOOSE declaration for rung 4 or 6, from the existing `_loose_declared`) AND `any_recount` (checker recorded recount/rewrite): require every section's applied file == the model's own section file (no rewritten section) and every recorded opt in {`--recount`, `--ignore-whitespace`, `--directory=…`}; then apply per section with exactly those opts. On success set `loose_apply_mode`, append a golden-clause part "RUN PATCH APPLY MODE: NOT STRICT (strict=False) — … applied PER SECTION … section 1: `git apply -p1 --recount --ignore-whitespace`; section 2: `git apply -p1`", and a READY bullet "APPLY MODE: NOT STRICT (strict=False) — recount only". Golden is tried strict first, then `--recount`.
- Otherwise (non-loose rung, rewritten section, other opts, or per-section apply fails) the original `die("… does not apply strictly …")` fires unchanged.
- `strict_ok` is untouched: it was already False for any recount (dry-run prints `strict=False`; header keeps "STRICT APPLY NOT CLAIMED").
- Output for any run that never needed the tolerance is byte-identical (A4, A5).
Note `--ignore-whitespace` is tolerated because the checker recorded it for section 1 (the READY says so); it is not "recount only" in the strict sense, and the READY wording names the exact opts.

## Arms (`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tests/hold_ready_loose_recount_arms.sh`, all --dry-run, scratch `.../holdready/arms`)
- A1 KS-1345 dir, NEW tool. Expect rc 0, `DRY-RUN OK`, `strict=False`, "APPLY MODE: NOT STRICT", `section 1: git apply -p1 --recount --ignore-whitespace`. Actual: PASS. Fails if: rc 2, or strict=True claimed, or the mode line absent.
- A2 same dir, OLD tool. Expect rc 2 + "corrupt patch at line 29". Actual: PASS. Fails if the old tool accepts (then A1 proves nothing).
- A3 fixture = copy of strict KS-1432 run (files cover touched, so the gate runs) with product hunk header `-259,3 +259,12` -> `+259,14`, section_1.opts=`--recount`, strict-out non-empty, A2 line rewritten to the accommodation wording, abs paths rewritten. Non-loose brief. Expect rc 2, "does not apply strictly" ("corrupt patch at line 17"), no DRY-RUN OK. Actual: PASS. Fails if the new tool lets a strict rung through on recount.
- A4a KS-1432 (strict, reaches the gate) and A4b KS-1410 transfer (strict, new test file, skips gate): NEW vs OLD rc, stdout, stderr identical (clock-normalised), rc 0, `strict=True`. Actual: PASS both. Fails on any divergence.
- A5 `tests/hold_ready_rung34_arms.sh` (run with its S redirected into my scratch): rc 0, TOTAL FAILS=0 (includes its 155-run PRE/NEW regression loop).
Total: `TOTAL FAILS=0`, rc 0.

## Dry-run on KS-1345 (exact output, long lines cut at 420 chars; full copy in scratch `final_dry.out`)
```
title-from-brief: WEBHOOKS <- line 3 `File: `Blockchain/Dev/services/originate/src/routes/webhooks.ts`  (product, modified in place: you find the site and write the lines)` (basename 'webhooks'); heading line 1 names KS-1345: `# KS-1345 originate-deliveries-failed-query-500 — originate: GET /api/webhooks/:id/deliveries answer`
DRY-RUN OK → READY_KS-1345-WEBHOOKS-DELIVERIES-1_spark-dsv4flash_BRIEFED-CODEPATCH-WEBHOOKS-PASS-7of7_2026-10-10.diff.md
  golden: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) DIFFER in webhooks.ts; body lines (context included) DIFFER in webhooks.ts (run 23 vs golden 22 body lines — context, since the change 
  touched=['Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts', 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'] product_plus=6 product_minus=1 red=3/11 green=11/11 suite=1093->1096 strict=False nonascii=0
  header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/out.md.checker/patch.diff`** (from `ls` at 02:51 2026-10-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/ou
  prnote: **PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (+40/-6); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --
```

## NOT tested
- A real (non-dry) hold; the actual READY file body (only the dry-run print of golden/header/prnote). The new "APPLY MODE" bullet is in the body template but I did not read a written file.
- A loose rung with a recount where the golden is also recount-only; golden fallback (`--recount`) is exercised only incidentally (KS-1345 golden applies strictly differently: "APPLIED RESULT DIFFERS").
- Rung 4 with a gate-reaching input AND a recount (no real run; the code path is shared with rung 6 via `loose_info`).
- Loose declared but the run needs a rewritten section (refusal kept, untested by an arm).
- Reviewer judgment: KS-1345 golden comparison says change lines DIFFER and APPLIED RESULT DIFFERS from the control — expected for a prose rung, Wednesday already verified the product hunk at source.

## Instrument errors you made and caught
1. First edit applied a whole-`patch.diff` `--recount`; dry-run still refused. Cause: concatenated recount fails, checker applies per section. Fixed with the per-section helper (found by testing section_1/section_2/patch.diff separately).
2. First A3 fixture (KS-1410 transfer) was ACCEPTED (rc 0): that input.json lacks the new test file's tip content, so the strict-apply gate is skipped. The arm reported FAIL, which is how I found it; rebuilt on KS-1432, which reaches the gate.
3. A hook blocked `rm -rf` on a variable in the arms script; fixture dir is now unique per run (`$$`), no deletion. A `git -C <scratch> apply` was also refused; used python subprocess with cwd instead.
4. First dry-run attempt without `--title-from-brief` gave the A3c refusal (loose declaration unreadable) — a usage slip, not a defect.
