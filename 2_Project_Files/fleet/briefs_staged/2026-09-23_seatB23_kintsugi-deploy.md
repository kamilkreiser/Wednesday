# SUCCESSOR BRIEF — Seat B 23rd, Secuura/Blockchain (pane `Secuura/Blockchain-B`) — round 20 close-out: the KINTSUGI deploy — from Wednesday

## BLUF
You are **Seat B 23rd**. Round 20 is **fully MERGED**: eleven PRs (#1202-#1212) are on develop (sha and tree in the VERIFIED section at the foot of this mail, read by Wednesday at source). **Your one job: deploy that develop to KINTSUGI, verify the RUNNING box, report.** Kintsugi ONLY — **never demo** (demo is UAT, Peter's nod). **No anchor** (the first anchor was 09-22's; none is commissioned here).
**Authority:** Kam, live board 2026-09-23 14:24:05 — *"…after you do merge, push, and deploy what you can."* — and his 2026-09-10 13:22 rule "kintsugi first". Deploy = kintsugi only (0_Brain/tasks/EXPIRING-GRANTS round-20 row; this deploy ENDS that lane).
**Whose / where:** the kintsugi box only (the host your project's own deploy docs name); your project's own identities; nothing written to the Secuura GitHub remote.

## THE PROCEDURE — PROVEN, COPY IT (read both WHOLE before item 0)
1. `fleet/briefs_staged/2026-09-22_seatA16_kintsugi-deploy-3bad652d1.md` in Wednesday's tree (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/`) — **ITEMS 0-5 and 7 apply; ITEM 6 (the first anchor) does NOT.** Replace `3bad652d1` everywhere with the develop sha below.
2. `5_Project_History/HANDOVER-seatA16-kintsugi-deploy.md` in YOUR tree (11 KB, 2026-09-22 19:19) — what that deploy actually met (its gotchas are this deploy's gotchas).
**Order, unchanged:** ITEM 0 MEASURE (read-only: the box, what runs, what is tagged, disk, the wallet) → mail Wednesday a plan confirmation → Phase 0 re-tag (rollback exists before anything moves) → rsync + build EVERYTHING, swap nothing → migrations in the middle → swap one service at a time → verify the RUNNING box (health, versions, a real request per service — never the steps' exit codes) → comments, handover, history, wrap.

## HOLDS
- ⚠ **KS-535 — ABSOLUTE:** kintsugi must NEVER share demo's `PLATFORM_WALLET_MNEMONIC`. Verify the wallet AFTER the redeploy, not only before (a redeploy is how it gets overwritten).
- **Kintsugi only. Demo never. Production does not exist and is not touched.** No `--no-verify`, no force-push, never delete — quarantine.
- **Client-facing:** the project's rule-7 deploy notice is a **ticket comment** under your board authority, BLUF-first, bytes mailed to Wednesday FIRST (the 09-22 pattern). **The extranet is not a channel.** Nothing to Peter or Stuart beyond the ticket comment.
- **Tickets:** the eleven stay **In Progress** — deploying is not closing; the closing pass is Wednesday's.
- If the box is down, or a migration would be irreversible, or anything reaches beyond kintsugi: **STOP and mail.**
- Wake path while you wait on Wednesday: Wednesday's mail + a pointer tap.

## RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — carried, no action in this deploy
`secuura-ks998-…-prettier` (a + "and install it also") · `secuura-ks1163-…` (a; Claude's, at the counter) · `secuura-ks974-…` (a; correct the record on KS-974) · `secuura-ks1084-part-b-…` (a).

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE (round 20)
- Seat B 22nd's `raise20.py` cumulative-count fix (ruling (a), 07:5xZ) — tooling, not deployed code; the same latent defect in `raise19.py:694-698` / the `raiseC20.py` lineage is a handover item.
- LEGD-BYTEXT (KS-781 LEG D should pin by text) — a ticket for the next round, not this deploy.
- KS-1143 / #1212's INDIRECT-INVOCATION false negative stays open on KS-1143.
