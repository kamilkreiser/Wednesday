---
date: 2026-10-07
type: drafter-report
source: brief drafter for Wednesday (Seat D 14th, Secuura/Blockchain demo deploy)
status: staged, NOT sent
---

# DRAFTER REPORT: Seat D 14th demo deploy brief

**Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatD14_demo_deploy.md` (200 lines). Staged only: not sent, not launched. The drafter wrote these two files and nothing else. No SSH, no mail, no tmux, no git write verbs.

## CHANGES vs the D 13th brief
1. **Send amendment:** D 13th's Q1-Q8 block is replaced by a placeholder for Wednesday's amendment at send. The rulings it carried are now in RULED BY WEDNESDAY.
2. **Title, seat, token, pane:** D 14th / `d14`. The round now reads "retire old rollback sets under Kam's card, then deploy".
3. **TOP LINE:** "Never delete" becomes "the ONE deletion is ITEM 1b". The build source is D 13th's existing clone `deploy-clones/seatD13-d75bfe2deb80`, which is re-verified, not re-cloned. Its handover says it is retained, and a second 612 MB clone would add nothing. **Wednesday may prefer a fresh clone: see Q-B.**
4. **Clause / AUTHORITY:** card `-1007` = (a) replaces `secuura-headroom-before-90pct-stop-1006` as the round's card. Its text is quoted verbatim. The prune card is restated as KINTSUGI-only, and the brief now says plainly that no card authorises a demo build-cache prune.
5. **BLUF order:** inventory first → Phase 0 → prove the kept sets → ITEM 1b delete → settled disk → forecast → rsync → Gate B (change B).
6. **WHAT DEMO RUNS:** the D 12th-era "UNMEASURED since 09-10" text is replaced by D 13th's MEASURED figures, each cited to a handover line. These include no `--profile`, project `dev`, prefix `dev-`, the six sets with their fingerprints, the 31/28 sets, KS-535, the 038a no-op, the variables, `/health/deep` null, and demo-service.
7. **Removed sections:** "WHAT THIS ROUND CARRIES" (range/038a/compose-variable readings) is cut. D 13th measured all of it on demo, so the brief now cites the measurement instead of the drafter's reading. Q3's seeder hazard is carried as Wednesday's released condition.
8. **Tools:** the brief copies D 13th's `boot/` (ITEM 0 set) and D 12th's `deploy/` (D 13th never reached deploy). **New:** `disk_forecast_d13.py` has to be re-keyed so F0 and N are required arguments, because its header claims they are but lines 5-6 are literals. **New, a live trap:** `inbox_matchd13.py`:15 already holds `d 14th`/`seat d 14th`/`d14` in OTHER_SEATS (its forward half). Carried as-is, D 14th's own GO would read FOREIGN. The brief says to remove them, add the backward `d 13th`/`d13` and the forward `d 15th`/`d15`, and verify by AST import.
9. **ITEM 0 (a):** the rule "develop must == DEPLOY_SHA" becomes: read D0, prove `d75bfe2deb80..D0` is a strict ancestor with 0 image inputs (using `map_move2_d13.py`, the GitHub compare API as D 13th used it, and trap 8), then accept only D0 at every later re-read (change C).
10. **ITEM 0 (b):** re-verify the existing clone instead of cloning fresh (see 3).
11. **ITEM 0 (d):** disk and the **image inventory come FIRST**. For each retire-set ID the seat records its tags and its containers, running OR stopped, and derives the DELETABLE set and its count against 38. The KS-535 C2 control is now `7d8958f1e48a608c`. The error baseline is CLASS-level using `classify_errbase_d13.py`. Mounts are re-read with `.Mode`.
12. **ITEM 0 (e):** the forecast runs twice: once on today's F0, and once projected after ITEM 1b if unique size can be read without a write. Thresholds are 16,174 / 22,250 MiB from `disk_forecast_d13.out`.
13. **ITEM 0 (g):** the plan mail now carries the retire plan (per-ID lists, the count against 38, the exact commands).
14. **Ctx handshake:** unchanged in shape. The 50/65/80 lines are now stated as RULED rather than as Q7 proposals. Gate B also carries ITEM 1b's before/after figures and the post-delete forecast (change E).
15. **THE GO:** the subject string is `GO (Seat D 14th): deploy d75bfe2deb80 to demo` (change D). **New:** if the GO body does not name card `-1007`, ITEM 1b does not run, per NEXT-PICKUP:14 ("the body naming the card and the exact sets").
16. **ITEM 1:** adds a "prove before ITEM 1b" step. The fresh set's ids == `:latest` ids, and `pre-20260910` reads 33 at `969f8db925918256`. If either fails, the seat STOPs and nothing is deleted. The rollback recipe is the measured one: `-p dev`, no `--profile`.
17. **ITEM 1b (NEW):** the five sets by name. The deletable rule is "only tags in those sets AND no container uses it", with non-deletable IDs reported. The count gate is == 38 and == ITEM 0's count, otherwise STOP before deleting. Deletion is one `docker rmi <id>` per ID with no `-f`; a refusal means STOP. No prune or bulk verbs. The AFTER assertions are listed, then a settled disk re-read and the forecast; if F0 < 16,174 the seat STOPs.
18. **ITEM 2:** `check-startup-migrations.sh` controls move here, because the script arrives with the rsync (D 13th's finding).
19. **ITEM 3:** `-p dev`, no `--profile`, `.rebuild-seatD14/`, `--seat D14`.
20. **ITEM 4:** STOP 2-demo is no longer a full stop. It is RULED IN ADVANCE, with the precondition re-read (ANSWER_stop1:7).
21. **ITEM 5:** Q3 is replaced by Wednesday's released condition (`ALLOW_DEFAULT_SEED_PASSWORDS` PRESENT-EMPTY/ABSENT in auth/.env/.env.local AND admin `active`). The 28 and the three not-recreated services are named.
22. **ITEM 6:** class-level error comparison; demo-service compared as a RATE; `startupMigrations` is AFTER-only; DEPLOYED carries ITEM 1b's figures.
23. **ITEM 7:** the 15 + 8 rows are carried. demo-service has no row. KS-1404's BEFORE is measured ABSENT. The KS-1256 STATUS line moved from the rulings section into ITEM 7.
24. **ITEM 8:** the history entry goes to the ROOT `history.md`, not the repo copy (D 13th's two-history finding, which NEXT-PICKUP:39 dropped as by design).
25. **STOP-AND-MAIL:** adds the clone assertions, a kept set not intact, deletable != 38, an `rmi` refusal, a GO body without the card, and the post-delete forecast. The Q3/Q6 lines are rewritten as ruled conditions.
26. **CO-TENANT:** R 4th's specific lines are replaced by a generic R-lane line plus the advisory push freeze, which does not block this seat.
27. **HOLDS:** "never delete, never prune" becomes "no prune of any kind; the only deletion is ITEM 1b". Adds the D 13th trap 2 line and STANDING_LINES:419/:420.
28. **TRAPS:** adds D 13th's nine traps by name. D 12th's trap 11 (the "taper") is folded into 12 as in D 12th's list.
29. **OPEN QUESTIONS (Q1-Q8):** removed. All eight are ruled and restated under RULED BY WEDNESDAY with file:line. New questions for Wednesday are below in this report, not in the brief.
30. **New UNMEASURED section** (change G). PROVENANCE is rebuilt; anything carried unverified points at the D 13th brief's PROVENANCE block.

## FACTS RE-VERIFIED (command + time)
- **Handover sha256:** `shasum -a 256 …/HANDOVER-seatD13-demo-deploy.md` gives `077d2879ec4dff8b7d2c5dcc6595546f2dc811d5b91a3d8601d9611184f6fbf7`. This **matches** the expected `077d2879ec4dff8b`. 320 lines (`wc -l`). Read at 2026-10-07 06:48 AEDT.
- **develop:** `env -u GIT_SSH_COMMAND git -C …/2_Project_Files ls-remote origin refs/heads/develop refs/pull/1383/head refs/pull/1404/head` returned rc 0 at **2026-10-06T19:48:18Z (06:48 AEDT 10-07)**. develop = `b39051390ff6f252601d6f7b45f0ea6c21c31023` (confirms the expected b39051390ff6). #1383 = `32e8459bc0f5…` (unmerged head unchanged). #1404 = `c117c0160684…`.
- **Card -1007:** read from `0_Brain/dashboard/data/decisions.json`:27516-27580. The option (a) label and detail are verbatim as given, `status: ruled`, `ruled_choice: a`.
- **The 38 tags:** 32+2+2+1+1 = 38 (handover:90-92; probe1_structure_d13.out:153-159).
- **Disk thresholds:** 16,174 / 22,250 from `boot/disk_forecast_d13.out`. F0/N are literals at `disk_forecast_d13.py`:5-6 (`grep -n`).
- **Forward ordinal:** `inbox_matchd13.py`:15 contains "ADDED forward 'd 14th'/'seat d 14th'/'d14'" (`grep -n -i`).
- **Rulings:** ANSWER_stop1.md:1-10 and ANSWER_develop_moved.md:1-10 (`cat -n`).
- **Grants:** EXPIRING-GRANTS.md rows 10 and 12 (`grep -n -i`). The October learnings file exists (`ls -la`, 2,841 B).
- **Routing:** launchers.conf:16 is the `-D` pane and inbox_routing.conf:38 is the `-D` inbox (`sed -n`).
- **Standing lines:** STANDING_LINES.md is now 420 lines (D 13th's brief said 419). Every cited line number was spot-checked with `sed -n` and still points at the right rule. Lines 419/420 are new (R 5th) and are cited.
- **D 13th records:** `ls` of `5_Project_History/2026-10-07_seatD-13th/{boot,deploy,mail}` and `deploy-clones/`. The seatD13 clone is present. D 13th's `deploy/` holds D 12th's tools (copied, unused).
- **Not re-measured:** the `d75bfe2deb80..b39051390ff6` content (ahead 10 / 0 under `Blockchain/`). It is carried from D 13th's handover and WRAP, and the seat re-measures it at ITEM 0 (a).

## CONTRADICTIONS between the sources and the changes
1. **Ruling timestamp.** The caller gives 06:46:04 AEDT (live board). `decisions.json` records `ruled_ts 2026-10-07T06:47:17.005539+11:00`, 73 s later. This is probably the local sync time. The brief quotes 06:46:04 as instructed and records the file's value in PROVENANCE.
2. **"38 old images by id" vs tags.** The card says 38 *images by id*, but 38 is a TAG count. Demo had 107 tags over 82 images (`docker system df`), so at least 25 tags share an ID somewhere. If any retire-set image also carries `pre-20260910` (plausible for a service unchanged between 09-03 and 09-10), or is used by a stopped container, the deletable-ID count falls below 38. **Change B's strict "must match 38 or STOP" may then fire on a correct measurement.** The brief keeps the strict gate as instructed (Q-A below).
3. **"Used by a running container"** (change B) vs Docker's behaviour: `docker rmi` without `-f` also refuses an image used by a STOPPED container. demo-overlay and migrations are Exited containers, and demo-service is restarting. The brief widens the rule to "any container, running or stopped", which is stricter and so safer. Flagged here because it is a deviation.
4. **"Re-tag demo's current running images"** (change B) vs D 13th's Phase 0 = the 31 REBUILD-set images (handover:84-87). That excludes `nginx-gateway` and `pgbouncer`, which run but are not rebuilt. The brief keeps 31, derived, per the handover's reasoning (a 33 count "would mean re-tagging something not being replaced"). Under that reading, `nginx-gateway` and `pgbouncer`'s rollback is their unchanged `:latest`.
5. **The freed-space figure.** The card says "about 17 GB" and treats the 17.93 GB "reclaimable" as the six sets. That figure also includes `pre-20260910`'s non-running images, which are KEPT, and shared layers free nothing. The actual gain is UNMEASURED and may not clear 16,174 MiB. ITEM 1b's STOP covers this, but it means **the deletion could happen and the deploy still stop**, with rollback depth spent. Q-C.
6. **The D 13th brief said "never deploy a SHA but the one kintsugi carries" and STOP on any develop move.** Changes C and D 13th's later rulings supersede this. Change C asks for "any other finding is a STOP" only at ITEM 0. The brief also makes any move AFTER ITEM 0 (≠ D0) a STOP, which is the D 13th shape carried forward.
7. **NEXT-PICKUP:14 says the GO body names the card and sets.** Change D defines the GO by subject only. The brief uses both: the subject is the GO, and the body's naming of the card gates ITEM 1b only.

## OPEN QUESTIONS FOR WEDNESDAY
- **Q-A (count gate):** should the 38 gate be on TAGS (32+2+2+1+1, which a correct measurement will match) with the deletable-ID count reported, or on IDs as briefed (which may STOP on a correct measurement)? Recommendation: gate on tags == 38. Delete exactly the IDs that pass the only-retire-tags/no-container rule, and mail any shortfall in DEPLOYED rather than STOPping. That is a deviation from change B and needs your word. Alternatively, rule it from the ITEM 0 plan mail, which carries the per-ID list before any GO.
- **Q-B (clone):** re-use D 13th's verified clone (as briefed) or require a fresh `seatD14-d75bfe2deb80` clone like the D 13th brief did? Recommendation: re-use it, with the assertions.
- **Q-C (sequence risk):** should the post-delete forecast be projected BEFORE the deletion (ITEM 0 (e)(2)) and treated as a STOP if the projection does not clear? That would stop the seat spending rollback depth on a deploy that then cannot proceed. Unique size needs `docker system df -v`, which came back header-only for D 13th.
- **Q-D (forecast line):** the brief STOPs only if the post-delete F0 < 16,174 (354 MiB/image). Should clearing at 550 (22,250) also be required, or is the in-loop guard enough below that? Recommendation: 354, with the 550 figure in the Gate B mail for your release.
- **Q-E (floor):** the drafter did not read tmux. Who else is live at send, for the CO-TENANT line?
