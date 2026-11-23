# COMMISSION: draft the brief for Seat W 72nd (Secuura/Blockchain-W), the follow-up AUTH lane (KS-2316 follow-up rulings + KS-1701's deferred auth sites), design-first build on Opus

Commissioned by Wednesday (the 22:39 rotation's successor seat), 2026-11-23. You are a DRAFTER: you READ and WRITE ONE FILE. You launch nothing, mail nobody, write nothing to Linear, GitHub or any project folder.

## OUTPUT (the only file you write)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_seatW72_auth_followup_design.md`
Then reply with: the path, its line count, the PARTITION result (MEASURE 2) at the top (any STOP first), and a list of every fact in the brief with the command or file you read it from. Say plainly anything you could not measure. All scratch (TMPDIR included, keep it short, e.g. /private/tmp/w72d) under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-23_drafter-seatW72-auth-followup/_work/`.

## THE SHAPE TO COPY
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_seatW71_ks1701_design.md` (read WHOLE; the previous W seat's brief, same project) and its drafter commission `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-23_drafter-seatW71-ks1701/commission.md` plus the W70 brief and commission it names (same standing lines and holds; THIS file wins where they differ). Keep every standing line the W71 commission lists (no cd; credentials inside a python script, never argv; GIT_OPTIONAL_LOCKS=0; the launcher's boot ls-remote is Kam's ruled line, not a STOP; shared-inbox warning; MEASURE FIRST, then ONE plan QUESTION, then WAIT; red-first + mutants; ONE commit, ONE push; READY FOR GATE tier 1; the after-compaction re-read line; SKIP the seat-boot memory note at the VERY TOP; timestamps from `date`). Read W 71st's record `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-23_seatW-71st/` (HANDOVER FINAL BLOCK first) and its wrap `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_W71_wrap.txt` for faults to pre-empt (e.g. a duplicate ticket comment; leftover mail-watch loops at the pane close).

## THE WORK AND THE RULINGS (copy every ruling verbatim from `decision_queue.sh show`)
Kam ruled, live board 2026-11-23 (read each with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show <id>` and quote option label AND detail under RULED BY KAM):
1. `secuura-users-stub-org-scope-ks2316-1123` = b "Cover it too" (20:57:44): POST /api/users/stub lands in the caller's own organisation; an organisation-less admin cannot make one (read the option detail for the exact words).
2. `secuura-org-admin-create-level-cap-ks2316-1123` = b "Allow up to STANDARD on create" (20:57:47).
3. `secuura-platform-role-spellings-ks1701-1123` = a "Everything asks the shared check" (10:11): the KS-1701 auth sites W 71st deferred, per its wrap line 16: "users.ts 485, 541, 597, 629, 750 and 1589 (lines at a5ce6ee8; PR 2288 has since moved the file), oauth.ts 1246 (ks1210-coupled), authenticate.ts 228 and 249 (no product caller)". RE-LOCATE every one at develop 8c2c24d37074 by content, not by line number.
4. Context ruling: `secuura-org-admin-user-writes-scope-ks2316-1122` = a "Own organisation only" (delivered by PR 2288, squash 8c2c24d37074): this lane builds ON it; read PR 2288's users.ts at develop first.
All four live in services/auth. ONE seat (Opus, design-first). The ks1210 coupling at oauth.ts: read the KS-1210 ticket and the code; if moving that site onto the shared check changes the ks1210 behaviour, the brief makes it a named item in the plan QUESTION (not built silently).

## MEASURE (read-only; the shared checkout is STALE: read files at develop through the GitHub API, `GH_CONFIG_DIR='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config' gh api repos/Secuura/Distributed_Secuura/contents/<path>?ref=<sha>`, or clone into your own scratch; NEVER fetch/pull/worktree/checkout in the shared checkout)
1. develop by ls-remote (Wednesday read 8c2c24d37074ecaffe9139e4719b19d1a1418595 via gh api at 22:45:43).
2. The census of every auth site the four rulings touch (file, line, current behaviour) at develop, frame NAMED + a positive control. Then the PARTITION against every OPEN PR's files (paginate). **Known open PR: 2289 (KS-1701, head c8468d2880248e27d619b697e18cc3e3b98d36c0, 35 files: originate, billing, vc-issuer, gateway, packages/shared incl. the ks1536 baseline json)**; a K 85th merge seat is being drafted for it and its merge waits on Seat D 83rd's deploy. **If this lane must touch any of PR 2289's 35 files (the ks1536 baseline json is the likely one: moving auth sites onto the shared check lowers auth's inline-list counts), say so at the TOP of your reply: the seat then measures and plans now and builds that file only after PR 2289 merges (its plan QUESTION re-reads develop; Wednesday's ANSWER says whether 2289 has landed).**
3. The seat ordinal: `/usr/bin/grep -o -i -c 'seat w 72nd'` and `'seat w 71st'` over `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (Wednesday read 0 and 3 at 22:4x; 71st is the positive control); the brief says RE-MEASURE.
4. The shared check `isPlatformRole` (packages/shared) and the ks1536 guard's per-file baseline for auth files, read at develop: report before/after per file; never bump a baseline upward.
5. The STANDARD cap: where the create path sets or accepts a level today, which levels exist (read the enum at develop), and what an ORG_ADMIN may pass today. The cell set pins: org admin create at STANDARD and below admitted, above STANDARD refused, platform admin unchanged.

## DEPLOY CONTEXT (never a condition of this build)
Auth is HELD on Kintsugi (no mail transport); Seat D 83rd's census found all 3 Kintsugi ORG_ADMINs (and all 29 non-platform users) have NO organisation, so once auth ships, organisation-scoped admins there act on nobody. This lane deploys nothing; a Kam card on shipping auth comes separately.

## ROUTING
Model claude-opus-5-5 (read from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json`, never typed): row C3 (a build on an access DESIGN surface). Gauge: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/usage_wednesday.json`.

## LIVE SEATS (for the brief's parallel-seats line; seats share one inbox)
Seat D 83rd (pane Secuura/Blockchain-D, Opus) deploying Kintsugi k41 (writes nothing to the repo). A K 85th (pane Secuura/Blockchain-K, Sonnet) may be live merging PR 2289. W 72nd acts only on mail naming `(Seat W 72nd)`.

## HOLDS to carry
As the W71 commission's HOLDS, unchanged (ticket comments only for client words; no deploy; demo only on Stuart's nod; Peter's/Stuart's tickets stay theirs; no 'do not merge' sentence; packages/shared vitest whole on both arms incl. ks1536; a sibling outside the ruled scope is LISTED and STOPPED on; "while I was there" = a STOP question). Plus: this lane changes WHO may do what at the stub route and the create path; every behaviour change is a cell with red-first, and the PR body lists each site's before/after.
