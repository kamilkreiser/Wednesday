# Gate 286, TIER 1 BATCH (Opus): PR 2129 (KS-784, Seat R 91st) and PR 2130 (KS-624, Seat Y 10th). Two independent tier-1 PRs in one session (09-18 batch rule). Commissioned 2026-11-09 17:0x by the 15:3x Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth for each PR.

Pins (Wednesday's ls-remote at 17:00:19 AEDT; RE-READ at start and end, and say whether each moved):
- develop 6beac8734a2f607200e3e71371b84268e1599029 (PR 2112 squash; both PRs were cut from 204e62acdc35, one commit earlier: read what the move changed)
- PR 2129 head 902b3161e4350df9468c7459f2c402d291c4a721 (KS-784; m365-integration/src/index.ts +15/-3, a new 157-line suite, cheat + flow fragments). READY: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatR-91st/mail/ready_ks784_r91.txt. Rulings: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_R91_addendum_ks784.md and 2026-11-09_R91_answer_ks784_ovl2080.md (the check ORDER Wednesday accepted: requireCallerOrg 403 -> Zod + assertSafeOutboundUrl 400 -> requireM365's own 503 in the handler -> insert; OVL_IGNORE_PRS=2080 granted).
- PR 2130 head 11a39402623328f2ee8368284cd397630bca13d5 (KS-624; services/prism/src/index.ts +44/-91, a new 10-cell suite, fragments). READY: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatY-10th/mail/out_04_ready_ks624.md. Rulings: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_Y10_answer_plan.md (D1 constant 'mock'; D2 verify route passed:false; D3 GET /api text).

PR 2129 questions:
1. The reorder: is requireM365 removed from ONLY this route's middleware, and does no OTHER route on that router change what it receives? Is the 503 body byte-identical to requireM365's? Is assertSafeOutboundUrl (from @secuura/shared) the real SSRF guard and is it reached for every webhookUrl form (IP literals, hostnames, IPv6, decimal/hex IPs, userinfo, redirects if any)? The stated consequences (a no-organisation token on an unconfigured stack gets 403; a hostname is DNS-resolved before the 503): true, and is the DNS resolution before the 503 reachable by an unauthenticated caller (requireCallerOrg first?)
2. Red first: R1-R5 red on develop as 503, green after; C1-C3 green both sides; the seat's mutants plus ONE of your own per change. m365-integration suite 303/303.
3. The corrected notify-route comment: true?
4. Overlap with PR 2080 (head re-read): merge tree of 2129 + 2080 in both orders; all 2080's hunks survive.
PR 2130 questions:
5. POST /api/credentials answers 501 for every body with no validation, lookup or store; PR 685's shape (read PR 685's merged code and compare). Removed code (issueCredentialSchema, dbSaveCredential, an import): anything else in the repo used them?
6. D1: PRISM_MODE no longer read; the 'mock' constant reported at /health, /api, log, banner. compose:1197 and bicep:1084 still set PRISM_MODE=basic (inert now): any healthcheck, script or doc that asserts 'basic'?
7. D2: the verify route's proof check passed:false, verified false, same fields. Callers of prism's verify route in code (gateway maps only /api/did to prism by the seat's read): confirm with a control.
8. Red first 7/10 on develop, 10/10 after; the seat's per-site mutants; one of your own; prism suite 39 -> 49, the 39 unchanged.
9. The seat's finding: ks1868 prism cell C1 cold-import timeout under parallel load: reproduce or not (Info).
Both: merge trees on develop 6beac8734a2f, and the two together; open PRs sharing their paths, with a planted control.

Constraints: clone on the boot volume /private/tmp/g286 (no rm; size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; never push; never run the hook against the real remote; no real .env (fixtures only); no box, kintsugi or demo; keep load1 under 8; df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate286-tier1-pr2129-pr2130/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2129: <V>; PR 2130: <V>' with V one of GO | GO WITH NOTES | NO GO. Then FOUND / TESTED / HOW, NOT TESTED, findings with ids G286-<PR>-<n> and severities. Findings only; post nothing; mail nothing.
