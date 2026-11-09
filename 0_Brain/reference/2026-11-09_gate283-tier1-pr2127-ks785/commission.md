# Gate 283, TIER 1 (Opus): PR 2127 (KS-785, round 1), by Seat R 91st. Commissioned 2026-11-09 15:4x by the 15:3x Wednesday seat. Single PR: no other tier-1 READY is due.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth.

Pins (Wednesday's ls-remote at 15:42:39 AEDT; RE-READ at start and end, and say whether each moved):
- develop 204e62acdc351e664f9a1ca49a058275e9b3e907 (moved since the seat built: the seat's base was 4d6b7bb17fd3be7b3fde8a3babc5d59c91c959b8; the move is very likely the PR 2111 squash, documentation only, UNMEASURED by Wednesday: read what it changed and whether it touches any of this PR's paths)
- PR 2127 head 190ffa868d7d9abac61401d84d654944c042cfc7 (one commit; 5 files +175/-9: start-environment.sh +17, check-slot-credentials.sh +17/-9 claimed COMMENT ONLY, check_slot_credentials.test.sh +118, cheat + flow fragments)
- READY: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatR-91st/mail/ready_ks785_r91.txt (read whole). The seat's evidence is under the same seat folder (evidence/ks785/, evidence/ks785_prediction_declared.md): reproduce, do not trust.
- The ruling this was built under (shape (a); PR 2052 comment-only overlap on check-slot-credentials.sh, OVL_IGNORE_PRS=2052): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_seatR91_build.md and R 91st's plan answer in the same folder (name it if you find it; say so if not).

Questions:
1. The behaviour change. start-environment.sh now sources the project .env (guarded by [ -f ]) before `docker compose up`. Is that the ONLY product-path change? What exactly changes for an operator: which variables now come from .env where a shell export used to win; what happens with set -e when .env contains a line bash cannot source; what the closing banner now prints. Could sourcing .env put a SECRET value into any output, log, banner, `set -x` trace or process argv that it did not reach before? Read the script whole at the head.
2. The premise. Reproduce the ticket's shape with Compose render-only (no `up`, no containers, no real .env, fixtures only): an exported shell variable beats --env-file; after the fix the .env value wins. Also the seat's exported-but-EMPTY case. Name your Compose version.
3. check-slot-credentials.sh is claimed COMMENT ONLY (154 non-comment lines identical). Prove or refute with your own comment-stripped compare and a planted control in each direction. Are the new comments true about the code they sit beside?
4. The new suite: red first on develop for exactly the 3 predicted cells, the 4 controls green on both sides; 39/39 at the head with the 32 existing labels unchanged. Your own mutants: delete the source block; move it below `compose up`; drop the [ -f ] guard; each must redden a NAMED cell. Does the stub docker let any cell pass without exercising the real ordering?
5. Overlap: PR 2052 (head b61674e7b763 at the seat's census; re-read) also changes check-slot-credentials.sh. Merge tree of 2127 alone on develop, of 2052 alone, and of both together (in each order): rc, trees, and whether both edits survive. Any other open PR sharing a path, with a planted control.
6. The fragments: true, and the docs-fragments check ends OK with a planted defect proving it can fail.
7. The hook: the seat's push ran 13/16 legs (3, 4, 8 skipped, local stack not up). Is anything this PR changes covered ONLY by a skipped leg?

Constraints: clone on the boot volume /private/tmp/g283 (no rm; state its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; never push; never run the hook against the real remote; never source or open any real .env or credential file (fixtures only); never run `docker compose up` or start containers; keep load1 under 8 (do NOT stress the machine on purpose); df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate283-tier1-pr2127-ks785/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2127: <V>' with V one of GO | GO WITH NOTES | NO GO. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G283-<n>, each with a severity. Findings only; post nothing; mail nothing.
