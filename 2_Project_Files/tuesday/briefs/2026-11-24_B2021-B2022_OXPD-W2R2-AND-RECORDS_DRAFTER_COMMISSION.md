# B2021-B2022 DRAFTER COMMISSION (Opus, in-session, READ-ONLY) -- Datasec / OXPd_2: lane W2 ROUND 2 (B2021, gate B2016's findings; lifts Tuesday's execute HOLD) and the records pass for PRs 43-44 (B2022)

Commissioned by Tuesday (s320), written after the command whose `date` printed 2026-11-24 08:16:38 +1100. Model OPUS for both drafters and both seats (OXPd `CLAUDE.md` line 7). Two drafters at once, each told its ONE lane in its prompt; each touches nothing of the other's. Return a 10-line summary with `STARTABLE: YES` or `NO` as line 1.

## FORM AND FENCES: identical to the previous wave's commission
Read whole first: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2010-B2012_OXPD-WAVE4-RECORDS-W2-CONTRACTS_DRAFTER_COMMISSION.md` (its kit form, its drafter fences, DRAFTER_RULES, the report form, the Questions-with-defaults rule). Everything there applies here except the lane text and the state. Your kit's model of a good kit: B2011's own kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2011_SEAT-X59_oxpd2-w2.md` (lane B2021) and B2010's kit `..._B2010_SEAT-R308_oxpd2-r-records-wave3.md` (lane B2022).

## AUTHORITY
- The product owner, Tuesday terminal 2026-11-24 about 08:12 AEDT, verbatim: "Please continue with the OXPd project.  Use fable to review once you are ready." (Tuesday's reading: the GATES of these lanes may run on Fable; drafters and build seats run on Opus.)
- The kick-off grant (EXPIRING-GRANTS, his 2026-11-23 10:10:14 words) runs until this evening's meeting. No kit connects to any real device; every cell runs against stubs on 127.0.0.1.

## STATE (RE-MEASURE every one you freeze)
- OXPd main `b0b26b60a37cf771a2121000ca60f420658e0088` (PR 44 W2 squash, one parent c5b103ee, tree b2a09571; HOSTED PASS 2093 total, RULES 657; Analyze x3 0; alerts 0: Tuesday's reads 2026-11-24 00:49).
- Gate B2016 verdict (W2 round 1, GO WITH FINDINGS @ 67c24d1): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2016_verify/` (VERDICT.md, FOR-RECORDS.md). Gate B2017 (CT): `..._B2017_verify/`.
- Tuesday's HOLD (00:33): no `oxpd1 write --execute` against any device until round 2 lands fixes for B2016 FOUND 1 (Major) and FOUND 2 (Minor).

## LANE B2021: W2 ROUND 2 (seat X61, Opus, G1 gate after)
Fix B2016 FOUND 1 (`undo-owed` prints "nothing is owed" / exit 0 having read NO undo list: run folder given instead of the session, session one level down, empty or header-only list: it must refuse with a non-zero exit and say what it read), FOUND 2 (read-before-register fails OPEN on a non-schema answer: same id in another namespace, deeper, unqualified: must fail CLOSED, no register sent), FOUND 3 (U+FFFE names crash after the read leaving a Pending row) and FOUND 4 (the printed undo drops --addressing/--password-name/--timeout-seconds), each with a red-proof cell that fails on b0b26b60 and passes after; read the verdict's exact text for each and its probe. Remaining Infos: list each with in or out and why. Branch from main, one push of a new branch, no PR (Tuesday opens it). Name the files; prove they are disjoint from lane B2022's (records only touches 1_Project_Definition and BACKLOG.md).

## LANE B2022: RECORDS PASS (seat R309, Opus, RECORDS WRITE)
Records only, by the B2010 form: PR 43 (CT) and PR 44 (W2) landings into history.md; gate B2016 FOUND 1-6 + Infos and B2017 Infos as owed items in BACKLOG.md (FOUND 1-4 marked "in round 2, lane B2021"); kits B2011 and B2014's FOR RECORDS; B2014's FOR RECORDS items (Test binding has 17 live ops; HP's self-signed-certificate sentence for step 3); Tuesday's execute HOLD recorded as a coordinator hold with its lift condition. Any new Kam words: grep `CLARIFICATIONS.md` first (C-78 is the newest known); none are expected.

## Out of scope for both
Anything on the printer; Azure; anything to HP or a person; the design documents in `Design/` and the new `Meeting/` folder (three other agents are editing them right now: never open them for write).
