# DRAFTER REPORT: NexusAI lane O successor (S100O) + HPSM-POC B251 (2026-10-17, about 06:0x-06:2x AEDT)

Read-only drafter for Tuesday. Nothing launched, nothing sent, no Jira, git or gh writes, no az, no HTTP to any app host. The only writes are the three files in `tuesday/briefs/`.

## 1. Files
- NexusAI body (ready for send_brief): `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_nexusai_O_successor_S100O.md`. **send_brief DRY RUN passed every gate** (`WED_AGENT=tuesday SEND_BRIEF_DRY_RUN=1 … send_brief.sh --to Datasec/NexusAI-O`, rc 0). SELF-CHECK is stamped `2026-10-17 06:19` (the drafter's re-read). **Re-stamp it after your own read**, because the attestation is the sender's.
- HPSM-POC brief_seat brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B251_SEAT-H_hpsmpoc-imports-bff-feedback-hardening.md`. STATUS: `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-17_B251_STATUS.md`. Last line `READY FOR GATE: b251/imports-bff-hardening @ <sha>` or `STOPPED: NEEDS TUESDAY` + ONE question. **Re-arm the STATUS watcher on that path** (DELTA 194 wake-source rule).

## 2. Launch commands (S99O's and B250's forms)
- NexusAI (one line): `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/brief_and_launch.sh --to "Datasec/NexusAI-O" --subject "SUCCESSOR S100O lane O: RD-848 first, then RD-801+822 and RD-802 re-checks, RD-828 slice 2, RD-837" --body-file /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_nexusai_O_successor_S100O.md`. That is how S99O went out (daily_tuesday/2026-10-16.md:27: brief_and_launch.sh rc 0, pane %2). Its usage gate runs first. The staged copy normally lives in `fleet/briefs_staged/`; I could write only in `tuesday/briefs/`, so copy it there if you want the record in the usual place.
- HPSM-POC: `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B251_SEAT-H_hpsmpoc-imports-bff-feedback-hardening.md'"`.
- Number: B251 is next. The highest is B250 in both `tuesday/briefs/` and the project's `Briefs/`; MPS uses B16x.

## 3. Corrections to the commission (measured; read these before launch)
1. **RD-801+RD-822 and RD-802 are already gated.** Gate 19 gave RD-801 @ 6613113 GO WITH FINDINGS (N-801-1 Polish) and RD-822 GO (`fleet/briefs_staged/2026-10-12_nexusai_gate19_RELEASE.md:8`). Gate 20 gave RD-802 @ a103c8e GO (T9 `…/2026-10-08-gate-batch20/report.md:18`). The gate 19 RELEASE set them as merge turns 18 and 19 (`:14`). They were never merged, and they are 134 behind main (merge-base d97039f). As you asked, the brief has the seat mail "READY FOR GATE" per branch. The body carries the verdict history, so you can choose between a re-gate kit and a merge TURN. The precedent was RD-828: a counts-only forward merge, then landing on its gated head (RD-828 comment 39408). Predicted conflict: `scripts/verify-expected-counts.json` only (gh compare: the only overlap among main's 75 changed files).
2. **RD-837's hold is cleared.** F-821-1 was fixed by RD-821 round 3, installed 2026-10-12T10:53:52Z after gate 21 GO (RD-821 comment 39361).
3. **RD-828 slice 2 has no D-F1 cell.** The ticket says "Corrected in RD-690's MERGED mail; no code". Slice 2 = B-F1, C-F1, C-P1, E-F1. The sweep's row 36 said "plus the D-F1 and E-F1 cells".
4. **Undelivered card:** `nexusai-rd846-build-broken-demo-deploy-1013`, ruled "b" at 10-16 12:15, has no delivered mark. The work it ruled on is done (PR #86, demo rev 0000100). The brief carries it under RULED BY KAM. Record the delivery with `decision_queue.sh --delivered nexusai-rd846-build-broken-demo-deploy-1013 "<RD-846 comment>"` so the next brief does not need the section.
5. **send_brief subject prefix:** the dry run shows `[Wednesday -> Datasec/NexusAI-O]`. This is the known OWED item (DELTA 193). The seat will reply to tuesday-agent@ anyway.

## 4. Verified facts the briefs rest on
- NexusAI: main 17fc6c5 (ls-remote). Code Security **enabled**, secret scanning **disabled** (`gh api …/Reporting_Dashboard_Au .security_and_analysis`). Alerts #154-#160 still open. Dockerfile :23/:74 duplicate pair and the :109 "(line 22)" comment confirmed at 17fc6c5. No rd-848 or rd-837 branch.
- HPSM-POC: code main d916baf (ls-remote), all check runs success, 0 PRs, 0 alerts. Every cited line in B251 TICKETS re-read at d916baf and matches the tickets. Records main 6f5f0dc carries C-105 and C-106.

## 5. What each seat needs that I could not verify
- NexusAI: the demo group check (left as note only). Whether ACR is reachable from this machine today. Whether the T9 stays mounted (the RD-847 lock base is there; mounted at 06:1x). Whether a ticket already holds N-801-1. The C-P1 wording (the brief has the seat propose it and you rule it).
- HPSM-POC: whether any other HPSM-POC pane is live (I read only STATUS last lines). Whether -251's guard changes hosted behaviour (imports off per the ticket; the seat confirms). The web test harness shape for formGate.ts.

## 6. HPSM-POC tickets excluded, and why
- **-254:** the exposure is the hosted runtime (B249 STATUS:17, `DOTNETCORE-10.0.12`). That is a stack setting outside the grant: **card candidate for Kam.**
- **-257:** labelled `needs-kam`.
- **-224:** hosted telemetry, which needs Azure-side work plus a new data flow from the HP-facing site. Decision-shaped.
- **-98:** a new admin screen with new words.
- **-148:** its open parts are words (C-2, C-3) or mock-only parity (N-9).
- **-259 / Terry's answers:** C-106 makes integration next phase, so the answers unblock **no build**. They are folded in as a REPORT ONLY conformance read of the C-73 Phase A import (G1-1/2/3), quoting only HPSMPOC-241 comment 39449.

## 7. Tiers in B251
Tier 1 (gate depth): -251 (the import outcome), -258 (hosted Feedback validation), -256 (hosted BFF forward/refuse). Tier 2: -252, -253, -255. The branch is tier 1 overall. New customer-facing words: possible on -256 (a new 400 body) and -251 (a reason). The seat lists them, and they block the deploy, not the build. -255's refusal strings are operator-facing words for you to classify (B243 N-10).
