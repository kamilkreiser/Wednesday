## NEW SEAT: you are Seat W 13th (lane Secuura/Blockchain-W; Opus; trust $TMUX_PANE): SUCCESSOR to Seat W 12th on the KS-1384 build (train F-a, F0a, F0b, F0c, F-b, R1, R2). Your runbook is W 12th's HANDOVER plus the chain of briefs before it; this mail adds only what changed since.

model: claude-opus-5-5 -- build on a money and security DESIGN surface (routing row C3), tier-1 gates (row G1) -- P1-P4 -- gauge 86% -- cloud (80-90% band): a money-path design build; neither local tier can carry it

## START AUTHORITY
Kam, 2026-10-30 10:07:32 AEDT, live board, verbatim: "Decision secuura-wednesday-go-counts-as-kams-word-1030: a — Yes: Wednesday's GO counts for starting work inside my standing grants (recommended)". The build sits inside Kam's card secuura-ks1384-f0-build-approval-1029 (a, "Build F-a, F0, F-b and R"). Your plan confirmation goes to Wednesday; her GO on it is the start. Signature classes still pause for Kam.

## BLUF
1. READ WHOLE, in this order: (a) W 12th's HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-30_seatW-12th/HANDOVER.md` (FINAL block first: commit table, carried drivers, re-key recipe, each PR's owed steps, F-b's design pointers); (b) W 11th's HANDOVER `.../2026-10-30_seatW-11th/HANDOVER.md` FINAL block (train rule, stack-cut recipe, R2's ruled scope); (c) W 12th's brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-30_seatW12_ks1384_successor.md` (RULED sections still bind).
2. FIRST WORK — the two CARRIED DRIVERS: F-a (pid 86753, 4th in the queue at 06:4xZ, status `evidence/fa/push/real_v3/status.txt`) and F0a (pid 95416, 6th, `evidence/f0/push_f0a/real_v3/status.txt`). Both are DETACHED v3 adopt-mode drivers (ppid 1). Do NOT restart them; stop one only by PID with kill -9 while queued, and only to re-key. When F-a's push lands: open its PR from the written body (evidence/fa/pr), ticket comment, assign KS-1808 and KS-1810 to our board account, then READY FOR GATE TIER 1. Same for F0a when it lands.
3. THEN BUILD F-b (reconciler.ts again; R6 with the wait marker; the driving set; m-3; cells p6/p6b/r4/r5/j/u), reading rev 4 §4.3, rev 2 §9 (R1-R8) and rev 3's j/u cells WHOLE before writing. Money path: every new branch gets a red-proof against its mutant.
4. Every fact in the HANDOVERs is the predecessor's reading: re-read heads, develop and ticket states yourself. Develop was a8c554659cb3 at Wednesday's ls-remote, 17:5x AEDT.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Card secuura-ks1384-f0-build-approval-1029 = a (2026-10-30 07:01:37 AEDT): "Build F-a, F0, F-b and R" -> artefact: each PR body (one line) and your history entry.
- Card secuura-docs-section-collision-dirties-every-pr-1030: OPEN with Kam (per-PR doc fragments vs renumber-at-merge). Until he rules: the merging seat renumbers at merge prep with a docs-only merge-in and a push. Do not change the docs format.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- TRAIN: F-a, F0a, F0b, F0c, F-b, R1, R2 are stacked PRs, each READY FOR GATE TIER 1; NONE merges until ALL hold GOs at their current heads; then one train in stack order on pinned GOs. Every PR body carries "Part of the KS-1384 train: do not merge alone".
- At most TWO queue places for your seat at once; F0b and F0c join only as F-a and F0a land. Every NEW driver starts DETACHED (nohup/setsid), with a bounded waiter: the harness kills background tasks at 2 h.
- R1's write set (06:2xZ): adds services/originate/src/services/reanchorInFlight.ts plus two new test files; edits to the KS 1814 route test, the KS 1293 manifest, ks1385-create-anchor-...test.ts and ks520-anchor-fail-closed.test.ts (overlap checked by W 12th with a control: clean).
- R1's BEHAVIOUR CHANGE, to be named in its PR body and for Kam's Platform S comms list: outside production, an unreadable in-flight state now answers 503 and writes nothing (was a 'failed' blob plus 202).
- R split: R1 = part (a); R2 = parts (b)+(c) on F-b's head. R2's write set adds originate routes/verification.ts, routes/verificationV2.ts (verify heals only) and routes/certifications.ts (~:772 legacy certify only). certifications.ts is NOT touched until Seat U 7th's #1833 (KS-1844, same file) has merged. POST /api/anchors/own-create = a spec change in the same PR.
- A docs-section collision is resolved by a docs-only merge-in plus a PUSH at merge prep, never "at merge without a re-push" (GitHub cannot squash a dirty PR).
- Throwaway Postgres: rebuild with W 12th's tools/build_pg_w12.sh re-keyed to w13 (127.0.0.1 only, the app role first, both URLs); remove with counts.

## LIVE SEATS AT SEND (Wednesday's list)
T 8th (auth: KS-1797 #1834, KS-1791; merge prep #1826/#1827/#1830), V 11th (KS-1807 docs; #1829), U 7th (#1828 re-merge-in, #1833 KS-1844 certifications.ts, #1831), E 22nd (KS-1845/1850/1851 authz; #1832 guard script), R 66th (eight raise PRs: tenant-provisioning, api-gateway platform.ts, mcp-server http-server.ts, originate connectorOrganisationErasure.ts, staking rewards.ts, originate paged lists, five scripts/check-*.sh). Re-run the open-PR overlap with a planted control before each push.

PROVENANCE:
- W 12th's wrap mail (06:48Z, read whole by Wednesday) and HANDOVER (10,950 B) and history line 1 "## 2026-10-30 - Seat W 12th" | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-30_seatW-12th/HANDOVER.md and history.md | read 2026-10-30
- carried drivers 86753 and 95416 alive, ppid 1 | `ps -o pid,ppid,etime -p 86753,95416` | read 2026-10-30
- origin develop a8c554659cb3 | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop` rc 0 | read 2026-10-30
- ordinal: "Seat W 12th" 2 (control), "Seat W 13th" 0, "Seat W 14th" 0 | /usr/bin/grep -i -c over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-10-30

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-30 17:50
