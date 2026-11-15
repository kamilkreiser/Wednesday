# notes: drafter for Seat D 63rd (k27 resume), 2026-11-15

## Deploy grant (loud check)
EXPIRING-GRANTS.md line 37 is NOT lapsed. It reads: "EXTENDED 2026-10-19 18:22:57 AEDT by Kam ... "keep the grant alive until further notice" - this grant NO LONGER ends Sat 31 Oct; it stands until Kam changes it." Original: Kam 2026-10-05 16:21:39. (File also has 7 other lines containing the word "lapsed"; none concern this row.) The brief quotes it and says the seat acts only on Wednesday's fresh GO.

## What was read
Commission, template commission, template brief (whole), D 62nd record: mail/03_status_1.txt, in_go_01, in_ans_01, 02_status_ready, 01_plan (head), evidence/kintsugi/c4_buildlaunch.txt, b8_phase0, b9_ks535, heartbeat tail, idfp_prediction, tools listing.

## Key findings that shaped the brief
- D 62nd's GO pin was 4e4347818772 (not 48883ba5976b of the template); develop is now ce35818d50ae (PR 2140, test-comment hunk, no image).
- kyc RUNS on Kintsugi, so R = 8 / C = 25 / NOIMAGE 3 (the template's kyc doubt is resolved).
- Phase 0 tags pre-20261115k27 already exist (idfp d54e878d3d7b7907). TRAP written into the brief: never re-run Phase 0 over them if any :latest is new, it would overwrite the rollback.
- Rsync of the pin to the host tree already done 05:57Z; so a different pin in the new GO means re-sync and full rebuild (flagged for Wednesday).
- D 62nd has NO history.md entry (ordinals 63rd 0, 62nd 0, 61st 1), no HANDOVER; its watcher pid 57263 died with tmux.
- A live remote batch driver may still be running (it was launched detached on the box): brief forbids killing it or starting a second build; report and wait.

## Open for Wednesday to rule
1. Pin in the fresh GO: 4e4347818772 (recommended, everything on the box is at it) or ce35818d50ae (forces re-sync and rebuild).
2. If the driver is alive or the builds finished: let the seat continue from verify_build (shape a), or rebuild (c).

## RULED BY KAM, NOT YET IN AN ARTEFACT
Carried as in the brief: 15:07 "please archive everything that is ready..."; 15:08 "there is a lot in in progress..."; 15:19 card secuura-merge-throughput-sixty-ready-1115 = a; 15:40 "the recent merge rules override everything historic"; 17:09 card secuura-ks1897-checkout-without-customer-1115 = b; grant line 37 extension.

## UNMEASURED
The Kintsugi box in every respect (driver alive or dead, batch markers, images, containers, disk, any swap); whether D 62nd's clone/scratch survive; whether the `_d62` tools still run; Linear state of the 8 tickets; whether tmux death touched anything on the box (it should not, the driver is remote); gate verdicts; Wednesday's QA gate numbers and Kam's 15:07 to 17:09 quotes were taken from the commission, not re-read from the board.
