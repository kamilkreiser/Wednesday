STARTABLE: YES, after the landing of A (PR #287) and/or B, once Tuesday fills slots S4, S5, S6, S12, S13 (and only if B is in TARGET: gate B1305 reads GO or GO WITH FINDINGS at 333ab581; at drafting it read PENDING, so B is NOT yet deployable).
BLUF: kit B1307 for seat D55 (Opus) deploys main at TARGET to hosted UAT only, in case A, B or AB (slot S6 first word), from PREV 73adb50c. It keeps B1290's structure (REFUSE, identity pass, PRE-DEPLOY SIGNALS, BUILD, way back, PART P). It adds a case-aware range proof (single squash: tree equality to the gated head; two squashes: path union + blob-per-path), an IL compare for B's one-call API change, and a counts-only, no-real-item door check (D-14).

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-05_B1307_SEAT-D55_hpsmpoc-uat-deploy-round2.md (133 lines)
Slots: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-05_B1307_slots.json (S4, S5, S6, S12, S13 are FILL placeholders; S7-S11 are drafter defaults for Tuesday to accept or change at the stamp)

## Facts (instrument; clock)
Clocks from `date`: drafting ran 14:58:03 to 15:05:27 AEDT 2026-11-05.
- RELAYED, PREV: `Briefs/2026-11-05_B1290_STATUS.md` last line `DEPLOYED: UAT @ 73adb50c (WEB + API)`; deployments web 1233d81e-..., API 340713d2-...; build BzAyBBr51ty9T48C2DvaU; run 41935305100; deployed 2026-11-05T00:25:24Z-00:28:35Z.
- MEASURED (shasum -a 256, stat -f %z, 14:59:25): way-back packages equal B1290's recorded values in BOTH `.tools/b1290/target/` and `.tools/b1290/repo/out/deploy-packages/73adb50c.../`: web 806d1a1ec06d4c5e2d1c3c66ff7fccdbb7cf68298a3aedbed8e6c48d3c07585a (16,296,145 B), API f81c8b48f053d84c2807daa29a32d63bca766493b6d21b05a20b25d23756c416 (49,591,598 B), RUN 41935305100. B1290's rollback script sha256 8894d607... (shasum), 32 lines. `.tools/b1307` does not exist (ls).
- MEASURED (gh api -X GET, project GH_CONFIG_DIR, 14:58-15:01): main = 73adb50c (= PREV); open PRs: only #287 (head f4cb85f0, base main, mergeable_state blocked). A: compare PREV...f4cb85f0 ahead 2 (9d34ad68, f4cb85f0), behind 0, 35 files all under web/, +478 -74, 12 match test|spec, tree 1e43eb645e0e82260fcc6a36e8799b7675c21ba3. B: branch head 333ab581, compare ahead 1, behind 0, 12 files +425 -37, tree c4f041e96b3a319ef6cf53c9accd061f92f56f76, parent PREV. Schema-path regex over both path lists: 0 and 0 (control NOT run by me: the regex is run with a control by the seat). Path overlap A/B: `comm -12` printed nothing (47 = 35 + 12); no control run by me beyond a visual check that both lists were non-empty.
- RELAYED gates: B1301 line 1 NO GO round 1 of 2 at 9d34ad6 (class "HPSM-POC layout round 2: the rest of the HTML mock", NO GO 0 before); B1306 line 1 GO round 2 of 2 at f4cb85f; B1305 line 1 `GATE VERDICT B1305: PENDING`; B1302 READY FOR QA at 333ab581.
- MEASURED (source read at 333ab581 via gh api raw): reviewDoor.ts opens one page and 3 calls in uat mode; FeedbackModule.cs diff removes `.Destructive()` from deleteFeedback only. Consequence recorded in the kit: once B is live anyone can approve or delete real held items, so the seat never touches a real item (D-14).
- MEASURED: ports 9920-9929: 0 listeners (lsof, 15:0x; all-listener control read 16 earlier) and 0 of 58 non-.pre SEAT kits of 4-5 Nov hit `(^|[^0-9a-f])992[0-9]([^0-9a-f]|$)`; scan controls: 999x hit 13 kits, 994x hit 5. 9930-9939 and 9960-9979 were also free; 9920 chosen.
- MEASURED panes (tmux list-panes -a): %0 tuesday, %247 Datasec/HPSM-POC-G347, %1 fleet-monitor. No D-pane present.
- MEASURED line pointers (printed by awk NR / grep -n): deploy-from-ci.sh at PREV lines 49, 50, 68, 69; model-routing.md 96, 145; models_latest.json 17 = claude-opus-5-5; B1301 lines 1, 74-79, 89-107 (T01 89, T03 91, T04 92, T05 93, T17 105); B1302 lines 62, 70, 71, 150; B1306 line 13 (landing rule); B1290 STATUS 148.
- Deploy-STATUS listing at drafting: newest rows B1290 (UAT 73adb50c) and B1297 (a deploy of the other, now decommissioned site; the kit mentions it only as "not this kit's business").

## D-decisions (defaults apply if silent)
- D-1 pin TARGET; case-aware proof: A or B alone = one squash, tree equals gated head; AB = path union (47) plus blob-per-path equals the gated heads. Reason: A's head has 2 commits, so a squash on a main that moved (B first) cannot equal f4cb85f's tree.
- D-8 closed word list is EMPTY (A: gate counted 0 customer-facing words; B: "Visible text: NONE"). I did NOT re-run either census; the seat does.
- D-11/D-14: B adds one non-GET class to UAT: DELETE of a random unknown `fb-<uuid>` (expect 404, not 403 uat.action-off), only after the local pair shows 404 with row counts equal before/after. No approve probe, no real id, no review-page screenshot or text. Following the logo link is allowed in this kit when B is in TARGET (B1290 forbade it), count-only.
- D-12: page-end "ref - head <= 64" is NOT TESTED on UAT (no old-shell reference there); UAT property = no unexplained shorter ring cell, covered 0, moves 0.
- Ports 9920-9929. Opus per model-routing C6. Hard stop Step 0 + 120, DONE Step 0 + 150.
- Slot S13 added (open door acceptance); S11 value is `UAT WORDS: NONE NEW; CLOSED LIST EMPTY`; S8 is `UAT ONLY` (no demo wording).

## Q (each with a default)
- Q-1 API restarts for a minute or two (B1290: web 15 s, API 31 s). Default: accepted.
- Q-2 If the IL compare for the Feedback assembly cannot run (no dotnet/dump tool), is the weaker PE/CLI fallback (row counts, #US set, one body shorter by 5 bytes) accepted as "UNMEASURED: IL diff, fallback met"? Default: accepted, said plainly in STATUS.
- Q-3 Port block 9920-9929. Default: accepted.
- Q-4 Should B's deploy wait for the product owner to see that approve/delete become open to anyone on UAT? The kit treats the 13:08 ruling as the authority (slot S13 ACCEPTED). Default: proceed on S13 only if Tuesday writes it.
- Q-5 If A lands first and B later, run two deploys (two seats) or wait and deploy AB once? Default: one deploy of the later TARGET (the kit supports AB).

## UNMEASURED
- Whether `dotnet`/ildump874.cs runs on this machine now (not invoked).
- Whether the API answers DELETE of an unknown `fb-` id with 404 (B1302 says R5 pins 403 for non-admin and policy; the kit makes the local pair prove 404 first).
- Whether the review page performs any write on load (the seat reads source `FeedbackReview.tsx` at TARGET in the PRIOR WORK step; I did not).
- Any hosted fact (no az, no HTTP): UAT still at 73adb50c, deployments ids, settings.
- The B-specific web bundle strings (`fb-[0-9a-f]{8}` regex source location in .next) are an expectation, not measured.
- A/B test-vs-product counts (23 / 5 product paths) are by name pattern, not by program.

## Outside the fences
None. I wrote only the three files; `decision_queue.sh` not used; no fetch/worktree/ref write; `gh` GET only under the project GH_CONFIG_DIR; no az/ssh/docker; no hosted HTTP. Read-only reads of `.tools/b1290/` (ls, shasum, sed -n) and the project's `Briefs/` STATUS files. I did read B1302's and B1305's STATUS files and the B1301/B1306 gate STATUS files (Datasec/HPSM-POC only). One hook advisory on case-sensitive greps was noted; the counts I rely on come from files read directly, not from zero-results. Scratch files (path lists) were written to the session scratchpad.
