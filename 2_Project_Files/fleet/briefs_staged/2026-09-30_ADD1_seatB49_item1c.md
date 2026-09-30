# ADDENDUM 1 (Seat B 49th): ITEM 1c added, two held Spark passes for gate47 N-1350-7 (deploy.sh + deploy-all.sh rc-1 messages), one PR, after ITEM 1a

## BLUF
**This ADDS one item to your launch brief and SUPERSEDES its QUEUE ORDER only: 0 → 1a → 1c → 2 → 3 → (4, 5 if ctx allows).** Nothing else in the brief changes. Fold it into your ITEM 0 plan confirmation.
**ITEM 1c (Wednesday's ruling; Refs KS-1054; T1, deploy path):** raise ONE PR carrying the two held Spark passes below. Both fix gate47's **N-1350-7**: when the predicate exits 1, the caller's line claims the migrations FAILED, but rc 1 also means "could not be verified" (python3 absent, and after ITEM 1a python3 present-but-broken). Message text only; no exit code, counter or branch changes.
- `deploy.sh:857`: `log_error "  API Gateway: startup migrations FAILED — see above"` → `… FAILED or could not be verified — see above`, plus a new test `Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh` (M0-M3: M1 red at develop, M2/M3 controls: rc 1 still counts an ERROR, rc 2 still a SKIP).
- `deploy-all.sh:312`: the smoke value `"one or more failed"` → `"failed or could not be verified — see above"` (still a FAIL against "0 failed"), plus `…/ks1054_deploy_all_rc1_message.test.sh` (N0-N3, same shape). The gate did not name this twin; the Spark screen found it.
**The replacement wording is Wednesday's ruling** (the gate named the defect, not the text): keep it byte-for-byte as held.

## THE HELD PASSES (Wednesday read both diffs line by line; both first round, byte-identical to their goldens, per the screen)
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1054-DEPLOYRC1-1_spark-dsv4flash_BRIEFED-BASHPATCH-DEPLOY-PASS-7of7_2026-09-30.diff.md`
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1054-DEPLOYALLRC1-1_spark-dsv4flash_BRIEFED-BASHPATCH-DEPLOY-ALL-PASS-7of7_2026-09-30.diff.md`
- Briefs + goldens: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1054-N-1350-7/` and `KS-1054-N-1350-7b/`; screen `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-09-30_residue-screen/SCREEN.md`.
- ⚠ The READY headings/filenames were corrected by hand after `hold_ready.py` mislabelled a bash run (a known tooling gap): the DIFF blocks are the payload; `cmp` them against the goldens in the brief dirs before applying.

## HOW (the brief's rules apply; these are the item-specific ones)
1. New detached worktree `s-b49-ks1054c` at develop `3e3a68260d0e` (the two product files are disjoint from ITEM 1a's; a base of develop is fine; if you prefer ITEM 1a's head as base, say so in a STATUS). Apply per file with `raise45.py` strict; `git apply --check` first.
2. 🔴 **The exec bit:** `deploy.sh` and `deploy-all.sh` are 100755. After applying, `[ -x ]` on both ON DISK before the first test run; restore with `chmod 755` (`cmp` rc 0); read the committed modes with `git ls-tree` (100755 ×2; the two new test files 100644 like the ks1054 suite's, stated as the control).
3. **Red-first on macOS AND `python:3.12-slim`:** each new test file alone at develop (M1 / N1 red, the controls green) and with the change (all green); the whole ks1054 shell suite and the whole shell runner before/after with counts; a tamper arm per product line (revert the wording → exactly M1 / N1 red). Note that at a base WITHOUT ITEM 1a the rc-1 "could not be verified" case exists already (python3 absent); say which base you ran on.
4. Branch `feature/ks-1054-<slug>-b49-1c`; subject ≤ 84 declared (e.g. `KS-1054: rc 1 from the startup check reads as failed or unverified, not as failed`), body `Refs KS-1054`, every other key de-hyphenated. Push under lock-45; quote the preflight ratio and skipped legs.
5. **READY FOR QA** as its own mail; **gate49 T1**. No ticket comment unless drafted into the READY (it must not repeat or contradict comment `49aff833`, nor ITEM 1a's draft).
If ITEM 1a's STATUS shows you past ~55% by Wednesday's reading when 1a is READY, Wednesday may move 1c after ITEM 2 or hand it over; do not decide that yourself.

PROVENANCE:
- the two diffs, their product lines, test cells and modes | Wednesday read both READY diff blocks line by line (awk over the files) | read 2026-09-30 13:24
- N-1350-7 and the twin, base develop 3e3a68260d0e, rounds, controls | the Spark residue screen's report, SCREEN.md above (a subagent of this seat) | read 2026-09-30 13:24
