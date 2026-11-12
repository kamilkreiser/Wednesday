# Commission: DRAFTER for Seat B 167th (Secuura/Blockchain merge seat), 2026-11-13 06:0x AEDT

Commissioned by Wednesday (the 06:00 morning seat). You are a read-only drafter. You write files ONLY in this folder and the one brief path below. Nothing merged, pushed, posted, mailed or written to Linear.

## What to produce
1. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatB167_merge.md` — the merge brief for Seat B 167th.
2. `notes.md` in THIS folder — everything Wednesday must rule or check before stamping (contradictions, UNMEASURED items, anything you could not verify).

## How: copy-and-change
- Template commission: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB166/commission.md` (read it WHOLE; its method, fences and rules all apply unless this file changes them).
- Template brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatB166_merge.md` (read WHOLE; copy its structure, standing lines, tripwires, step 8, RULED BY KAM and RULED BY WEDNESDAY sections, keep-text-short line).
- The predecessor's handover: B 166th's record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-166th/` (HANDOVER for B 167th). Read it.
- Lane source: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-next-lanes/lanes.md` (read WHOLE). Its figures are a drafter's, UNVERIFIED except where Wednesday says below.

## The queue (Wednesday's ruling; rows in this order, the seat merges as many as its tripwires allow, one at a time, head-pinned, develop re-read after each)
1. PR 2198 (KS-1868, tier 1, gate 321 GO WITH NOTES) then PR 2197 (KS-1868, tier 1, same gate). Wednesday verified at 06:03:49 by ls-remote: 2197 head 2f10c9750a90, 2198 head 5064d0e99dd8 = gate 321 verdict lines 1-2; develop 410feda1a85e.
2. Then the GO-verdict, overlap-free tier-2 set from lanes.md step 4: 2177, 2147, 2144, 2141, 2137, 2134, 2126, 2125, 2098, 2097, 2096, 2095, 2090, 2089. For EACH row you put in the brief: open its gate verdict file and quote the verdict line naming the PR and its head; re-pin the head by `git ls-remote` (read-only) in the same action; list its files from `gh pr view <n> --json files` (GH_CONFIG_DIR = the Blockchain project's 4_Credentials/.gh-config, read-only); state the gate's findings the GO must name. A row whose live head differs from the verdict's head is DROPPED with the reason in notes.md.
3. NOT in this seat: 2099, 2073, 2131, 2135, 2136 and every overlap pair (ordered merges, a later seat); 2079 (gate 345 running); 887 (NO GO); PR 2075 (owes a ticket check first).

## Must-checks for notes.md
- The PR bodies carry a "do not merge until the pre-merge suites run" block (lanes.md caveats): read how B 166th's brief handled it for 2200/2201 and say whether the same handling covers 2197/2198 and the tier-2 rows.
- The CI reds (UNSTABLE, failures at 2-3 s): what did B 164th-166th's briefs say about check-runs? Carry the same declared-non-blocker line only if it is in their briefs; quote it.
- Board-seat filing candidates from the pickup (G344-2184-4 four unguarded err?.message sites; G323-2200-1; auth tsconfig.test.json 41 develop-side diagnostics; two cwd-reading auth tests): these are NOT this seat's; list them in notes.md for the next board seat only.
- Run the brief's own SELF-CHECK and contradiction reads as B 166th's drafter did.

Model: Sonnet. Return a 10-line summary: rows kept, rows dropped and why, anything Wednesday must rule.
