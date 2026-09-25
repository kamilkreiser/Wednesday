# BLUF — a SHORT Vision seat. Gate 8 returned NO-GO on BCR3 round 4 (703d304) for ONE residue only: at 1-minute load ~144 the 90 s close bound still kills healthy Chrome closes (it measured closes of up to 160,525 ms). Everything else the gate measured is CLOSED. Under Kam's round cap, the closed part SHIPS and the residue becomes a TICKET: (1) merge 703d304 into QuickQuote main (0 behind d4426f8, so a fast-forward or an equivalent merge; no rebase); (2) file ONE backlog ticket for the extreme-load residue; (3) record both; then wrap. NO publish: live QuickQuote stays v2.33 until Kam types the word.

**Addressed to the cockpit seat `Datasec/Vision_Sales_Portal` only.**

## AUTHORITY
- Kam ruled card `quickquote-bcr3-round4-fourth-round` = a ("Test it", live board 2026-09-25 13:52:08). That authorised this 4th round on the BC class.
- Kam's standing QA-gate rule (2026-09-05 20:19, "Let's go ahead with your recommendation"): rounds on one class are capped; at the cap the CLOSED instances ship and the residue is ticketed, and no further round runs without his word. This round was the one he authorised past the cap, so round 5 would need his word again. Do NOT build a round 5.
- Merge = code on main only; deploys and publishes are Kam's (his typed word).

## WHY SHIPPING IS SAFE (from the gate report, measured at runtime; read it: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-25-vision-qq-gate8/report.md)
- Production makes 0 closeBrowser calls ({"closeBrowser":0,...} with two real PDFs emailed, spy fired). The bound lives on a test/print-harness path.
- The emailed PDF shows 0 differing pixels against main; only the /CreationDate and /ModDate bytes differ.
- test:print completes and exits: idle 3/3, loaded 7/7. The 9/9 forced-hang files exit. Kill attribution is clean.
- Round 4 is a measured improvement over round 3 at load ~117-118 (0 kills against 9 of 9).

## THE TICKET (one, backlog): "BC-F2 false kill at extreme CPU load (1-min load ~144): healthy Chrome close measured up to 160,525 ms against the 90,000 ms bound"
Carry the gate's numbers (A4 red at load 144.39; the 240 s discriminator: every close returned, the longest 160,525 ms; headroom 0.56x), the likely directions (a larger bound for the test harness, or a test that does not treat a slow close under starvation as a kill), and that production is unaffected. PRIOR-WORK CHECK: read your BACKLOG first. BCR2-O1 is already retracted (its tracking at 90,000 was confirmed by gate 8), so do not re-file it.

## VERIFY + REPORT
Before the merge: ls-remote QQ main (still d4426f8?) and the branch (still 703d304?). After: ls-remote main == the merge result; run test:print and unit once on merged main. Mail `[Datasec/Vision_Sales_Portal -> Tuesday] MERGED: BCR3 round 4 …` with the merged sha, the test counts and the ticket id. Then wrap.

## HELD
No publish, no deploy, no production change, no round 5, no deletion. Nothing goes to any human but Tuesday.

PROVENANCE:
- gate 8 verdict | mail [QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 8, 2026-09-25T05:11:49Z, and the report path above | read 2026-09-25
- Kam ruling on the 4th round | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh live row 2026-09-25T13:52:08 - my project, not yours | read 2026-09-25
- cap rule | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md | read 2026-09-25
Self-check note: re-read whole; merge only, no publish, no round 5.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 15:16
