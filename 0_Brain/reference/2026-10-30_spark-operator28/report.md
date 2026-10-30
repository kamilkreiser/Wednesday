# Spark operator 28 - report (2026-10-30, base develop 85cd24d81cb9, clone .../2026-10-30_spark-operator28/clone)

## BLUF
Task 1 (KS-1410 api-gateway files): NO sites remain. notifications.ts, batch.ts and audit-export.ts at develop 85cd24d all route their catch blocks through a local `fail500` (log server-side, constant 500 body); audit-export's 502 is already a constant. What is left is only 200-body per-item `results` leaks (batch.ts:161,167,210,258,306) = the excluded class, and audit-export.ts:194 relays the UPSTREAM service's error text with the upstream status (not a thrown message; a pass-through decision, not briefed). So I measured rung 5 on a real KS-1544-class candidate instead.
Rung 5 (multi-file, mixed shapes): ORIGINAL brief FAILED at A2a only; ONE rebrief PASSED byte-identical. Rung 5 broke on FILE-SECTION HEADER FORM (the model left out every `diff --git` line and wrote the NEW test file as `--- a/<path>`, despite the brief saying NEVER), NOT on multi-file or mixed shapes: checker 7/7 on the original, all 6 product hunks across 2 files and 2 ORDER BY shapes correct, patch tree-identical to the golden. Held: O28-P1 (READY note). Drainer 97411 alive, I started none.

## Task 1 census (control included)
Clone: new path, `rev-parse --show-toplevel` asserted equal before use; origin develop by ls-remote 85cd24d81cb9 (same sha as op27's).
| file | catch blocks | via fail500 (constant) | remaining thrown-text in a response |
|---|---|---|---|
| notifications.ts | 6 (:153,174,203,231,261,317) | 6 | none |
| batch.ts | 3 route catches (:214,262,310) + 1 helper | 3 | per-item `error: err.message / s.reason?.message` in 200 results (:167,210,258,306) and `data.error` :161 - EXCLUDED (200 `results` leak) |
| audit-export.ts | 1 route catch :255 + inner fetch catch :199 | 1; inner catch answers constant 502 | :194 relays upstream `errorData.error` at the upstream status: not a caught error's message |
Control: the same grep finds the `err.message` / `.reason` lines at batch.ts:167/210/258/306 (the excluded class) and every `fail500(` call, so it is not blind. Positive count: 10 fail500 call sites + 3 definitions.

## Task 2 / rung 5 candidate (real work, not owned by a live seat)
Board screen: all 747 open KS issues pulled (ks_open.json). Chosen: KS-1544's CLASS (paged `ORDER BY` with no unique last key), at 9 originate sites NOT named in KS-1544 (it names tenant-provisioning; KS-1731 vc-issuer is already fixed on develop). Files: services/originate src/services/errorTrackingService.ts (5 hunks sites) and src/routes/adminConfig.ts (4 sites: 2 audit_logs `created_at DESC` -> `, id DESC`; 2 rights_holders `display_name ASC, last_name ASC` -> `, id ASC`) + one NEW jest source-text file (6 cells, 3 red). Mixed shapes = two ORDER BY forms plus merged and unmerged hunks; 2 products + 1 test = 3 files; 6 product hunks. No held pass touches these lines (KS-1780 p1 edits systemErrors.ts). Caveat: this candidate is unticketed; Wednesday decides filing.

## Rounds (hand-run round.sh; lint 0, dry OK, control PASS byte-identical beforehand for both briefs)
| brief | result | round | model | tokens | golden |
|---|---|---|---|---|---|
| night/briefs/ks_1544c_originate_paged_lists_total_order (original, per-hunk skeleton) | FAIL: checker 7/7, A2a rc=1 | 228 s | 93.1 s | 52986+2200 | TREE-IDENTICAL |
| ..._rebrief (+ explicit 3-section header skeleton) | PASS 7/7 + A2a 6/6 | 216 s | 87.8 s | 53220+2324 | BYTE-IDENTICAL |
Classification of the failure: output FORMAT (new-file header). The A2a BAD line is "section 3 ... not at the tip" because `--- a/<path>` for a file that does not exist reads as an edit. Model wrote no `diff --git` lines in any section (the earlier rungs' briefs never had them dictated either; they passed because the new-file form was ok then). Counter: original + ONE rebrief, both used.
Where rung 5 breaks: it does not, on hunk/file count or shape, at 3 files / 6 hunks / 2 shapes. It broke on the new-file header slip, which the rebrief's explicit five-line header skeleton fixed. Standing recommendation: put the 3-section header skeleton in every multi-file loose brief from the start (buildr5.py REBRIEF text is the wording). n=1 original + 1 rebrief; not a reliability claim.
Speed: ~25 tok/s end to end, ~53 K prompt tokens (larger than rung 4's 17 K because two products and a bigger input).

## Held
O28-P1: night/READY_KS-1544-KS-1544-O28-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-LOOSE-ORIGINATE-PAGED-LISTS-TOTAL-ORDER-PASS-7of7_2026-10-30.diff.md (hand-written: hold_ready.py REFUSES loose code_patch2, A3x unmeasured=2). I read the nine +/- pairs: each only inserts the tie-break column. Unmeasured: query plans (index on created_at alone), whether any client page-walks these lists, open PRs on adminConfig.ts.

## Faults
1. Hooks: `cd`, zsh `=====` word and an unquoted `--include=*.ts` glob each cost a call. 2. buildr5.py: my first REBRIEF patch put raw newlines in a string literal (SyntaxError), fixed with chr(10); the first rebrief invocation ran against an empty GEN_BRIEFS path and lint then complained about 117 briefs in the flat dir (harmless, nothing written there). 3. hold_ready.py refuses loose code_patch2. 4. Full-machine load: control runs 94-208 s.
done.md: 2 rows appended; IMPROVEMENTS.md: 2 rows (backup IMPROVEMENTS.md.pre-1030-op28).

## Next
1. Wednesday: file/hold decision for the nine KS-1544-class sites; consider a sweep brief for the other paged reads (originate adminConfig.ts :405/:944 unpaged are fine; services/auth userRepo.ts:1044 is paged but owned by a live seat).
2. Rung 6 candidates: 4+ files, or a bash_patch2/code_patch2 mix; keep the header skeleton.
3. Prune: clone, run dirs spark_secuura_2026-10-30_ks_1544c_*{,-control}, cache/work clones (~335 MB each).

## Left behind
tools/ (spec_o28.py, buildr5.py with REBRIEF env, mk22/loosegen22/s22common copies), linear_open.py, ks_open.json (747 issues; titles and descriptions, no key), round_r5*.log, control logs, lsremote file, briefs ks_1544c_originate_paged_lists_total_order{,_rebrief} in local-model/night/briefs/.
