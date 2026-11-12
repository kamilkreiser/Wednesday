# Commission: DRAFTER for Seat R 116th (Secuura/Blockchain RAISE seat), 2026-11-13 06:0x AEDT

Commissioned by Wednesday (the 06:00 morning seat). You are a read-only drafter: write files ONLY in this folder and the brief path below. Nothing raised, pushed, posted, mailed or written to Linear.

## What to produce
1. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatR116_raise.md` — the raise brief for Seat R 116th.
2. `notes.md` in THIS folder — everything Wednesday must rule or check before stamping.

## Copy-and-change
- Template commission: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatR115/commission.md` (read WHOLE; its method and fences apply).
- Template brief: the R 115th raise brief it produced (find it in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`, name containing `seatR115`; read WHOLE: push lock, overlap gate, held-patch builder, READY FOR GATE shape, grants).
- R 115th's HANDOVER in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/` (folder named for R 115th; read it).
- Lane source: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-next-lanes/lanes.md` step 3 (UNVERIFIED drafter figures).

## The rows (two batches; disjoint files per lanes.md)
- Batch A (admin frontend): KS-1105 (READY file O136-P1 CODEPATCH2 LOGIN.TSX), KS-1913 (O136-P1 PLATFORMAUDITLOG.TSX), KS-1912 (O137-P1 CLIENTLIST-APITS).
- Batch B: KS-1197 (ks_1197_p1 CODEPATCH ENFORCEMENT, api-gateway services/enforcement.ts), KS-1776 (ks_1776_p1 CODEPATCH AUTH, auth routes/auth.ts).
- READY files live in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/` (find each by ticket key). For EACH: quote its header (date, target files); state whether Wednesday read every +/- line (search the daily notes `0_Brain/daily/2026-10-28.md`, `2026-11-11.md` and the 11-11 pickup for a "read every +/- line" line naming it); if not found, mark it **UNREAD BY WEDNESDAY** in notes.md (Wednesday reads it before stamping).
- **Applies-check at develop 410feda1a85e54b82a65464607f4761c2da3bb1b:** in a scratch clone in THIS folder (`git clone --filter=blob:none`, read-only on the source), `git apply --check` each patch; report PASS/FAIL per row with the command output. A FAIL row is dropped with the reason.
- **Tier per row:** KS-1776 touches `services/auth/src/routes/auth.ts` and KS-1197 an enforcement service: say whether each is a tier-1 surface (its gate will be Opus). KS-1105 is a Login page: same question.
- Board check per ticket (Linear read-only): state, assignee (never Peter's or Stuart's: those are not ours to raise), and that no open PR already carries the key.

Model: Sonnet. Return a 10-line summary: rows kept, dropped and why, tier per row, anything Wednesday must read or rule.
