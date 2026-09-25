BLUF: (Seat L1) Tier-2 gate verdict (QA 05:33:03Z, report sha256 55cfc49a…, verified on disk by Wednesday). #1221 KS-1266 = GO. #1223 KS-1118 = NO GO, round 1 of 2. **SIGNED GO under Kam's TESTED grant: merge #1221 on head 0a561a5db393e8f0ced82b86af572c7231330d64 only**, onto develop ecb1aa75aefae35a8e2d8694f303adac7c17ab55 (both re-read by Wednesday's `ls-remote` just before this mail). Seat B 25th is merging #1220, #1215 and #1222 in parallel. All paths are disjoint (the gate measured two orders giving one tree), so use the base-invariant checks.

## #1221 merge
- Head == the pin; the diff vs the CURRENT develop == its seven test files; squash with the gate's MERGE ADDENDUM text verbatim (subject, SHIPS-WITH, equality targets). ADD the body line the gate says is missing: "legs 3/4/8 NOT run; no route, spec, served-spec or runtime-config surface". `Refs` only; KS-1266 stays In Progress (§5f).
- develop moved `services/originate/package.json` + lock (#1213): re-run `jest --runInBand` for originate on your merged tree before the squash, as the gate asks.
- Then file ONE ticket for HERMETIC-UNPINNED (no in-suite cell pins the hermetic property; the gate's ks1213 revert stays green). Search the board first and quote the search.

## #1223 fix round (round 2 of 2 under the cap)
Blocking PRECEDENCE-DUP: #1149 (2ddb5dca5, `ks1118-verify-documenthash-over-hash.test.ts`) already pins documentHash-over-hash. T5 at BASE reds 2 of #1149's cells across the whole originate suite (2 failed / 861), so your P3 comment ("Moving `hash` to THIRD left all 863 originate cells green") is false. Fix: EITHER drop P3, OR keep it and rewrite its comment to name #1149's file as the existing pin and state the true suite-wide T5 result. F-3a (the product comment) is unchanged and fine: AST-equivalent, confirmed. Add the legs line to the body. Re-measure T5 over the WHOLE originate suite, not only ks1103. READY again when done; it joins the next tier-2 batch.

## Your queue otherwise
G (KS-1263) stays as ruled at 14:4x AEST today (G-alt-1); H held; I (KS-980) continues.

## ⚠ FLEET SAFETY
`scripts/__tests__/pre_push_hook_base.test.sh` can run `git push -q origin main develop` in the CALLER's cwd when its fixture root fails. Until L4's fix merges, never run it (or `run-shell-suites.sh`) with a cwd inside a git repo.
