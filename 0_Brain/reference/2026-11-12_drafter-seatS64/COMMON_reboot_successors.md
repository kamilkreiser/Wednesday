# COMMON to the four reboot-successor drafter commissions (S 64th, R 104th, B 146th, A 23rd). Wednesday, Mac mini relaunch seat, 2026-11-12 ~08:0x AEDT.

## WHY
macOS restarted the Mac mini without approval at about 07:49 AEDT (Kam, live board 07:50:57: "Mac OS restarted the mini without approval.  relaunching everything"). Every Claude session on it died at once, all four Secuura/Blockchain floor seats included. None of them wrote a final HANDOVER or a wrap. Kam approved relaunching the floor at about 07:57 (terminal: "good plan.  go ahead"). The standing commission is Kam 2026-11-11 14:0x (terminal, verbatim): "please work your way through the In Progress and backlog tickets for Secuura.  Use the spark as much as you can and use as many agents as it takes to get through it."

The precedent is R 96th to R 97th on 2026-11-11, after the drive drop. Its commission is /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-seatR97/commission.md and its output is brief_R97.md + notes.md in the same folder. Read all three whole: they are the shape you produce.

## WHAT WEDNESDAY FOUND IN THE MAIL (wednesday-agent inbox, UTC; read each mail whole yourself; Wednesday has read only the subjects)
The previous Wednesday seat left these UNANSWERED between 07:02 and 07:49 AEDT. Each is now the successor's FIRST item, and Wednesday rules it at the stamp, not you:
- A 22nd: 20:02:54Z QUESTION plan confirmation; 20:34:38Z STATUS "no ANSWER in 30 min; KS-2170 builds locally, its push waits on PR 2079"; 20:41:45Z STATUS "KS-2170 committed locally (b528ed7ada56); its push waits on your ruling about PR 2079".
- B 145th: 20:07:53Z STATUS "set-up closed at 35.7, row 2186 cycle starting"; 20:19:58Z READY TO MERGE PR 2186 (KS-2160), awaiting its GO.
- S 63rd: 20:03:29Z "Session wrap 2026-11-12" (it WRAPPED, then evidently resumed on Wednesday's 20:31:13Z KS-663 ADDENDUM); 20:33:26Z QUESTION "byte round for the KS-663 comment".
- R 103rd: STATUS 1 to 8 (19:58Z to 20:31Z: row 39 = PR 2197 pushed and verified; rows 30+33 committed and pushing); 20:47:14Z READY FOR GATE round 1.
Mail is read through the AgentMail API: GET https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages (and /messages/<id> for a body), header 'Authorization: Bearer <AGENTMAIL_API_KEY>'. Source the key from /Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env with `set -a`; never print it. READ ONLY: never send.

## STATE (measured by Wednesday 07:55 to 08:0x; re-measure each)
- No push lock exists: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/ holds only lock-holder.json and lock-released.txt, both from October. There is no .push-lock directory.
- develop was c78c80bd5370 at 06:5x (PR 2183). Re-read it with `git ls-remote` (B 145th had not merged 2186: it was waiting on its GO).
- The Spark is serving V4 Flash. A five-model A/B operator (0_Brain/reference/2026-11-12_five-model-ab/) is using the SPARK ONLY: no Secuura checkout writes. Do not touch the Spark.

## RECONSTRUCTION (the core of each brief)
After an unclean shutdown the successor's FIRST act is to re-measure its predecessor's state, before any write: every worktree it owned (git status; fsck --connectivity-only in its OWN worktrees only), every branch it pushed (ls-remote), every PR it opened, every Linear comment or filing it made (for the S lane: read back by key). This goes into a reconstruction table (row · worktree · branch · commit sha or 'uncommitted' · pushed? · PR?) in its plan confirmation. Nothing is pushed, merged or re-filed before Wednesday's ANSWER.

## HARD LIMITS for you, the drafter (verbatim from the R 97th commission)
Never `cd`. Quote heredoc delimiters. Read-only git verbs only in client checkouts and worktrees (ls-remote, show, log, diff, status, ls-tree, cat-file, grep; NEVER fetch, pull, worktree, checkout, reset or merge). No writes to Linear, GitHub, mail or boards. No .env values printed. Write only into YOUR drafter folder.

## OUTPUT (each drafter)
- brief_<seat>.md, send_brief-ready. It has a literal `PROVENANCE:` line, then `KS-NNNN | <source> | read YYYY-MM-DD` for EVERY KS key the brief names anywhere. No lesson-file names that look like card ids. Keep it LEAN: point at the predecessor's brief for unchanged procedure, copy-and-change it, and carry its stamp rulings unless superseded. Target under 55 KB. Model claude-sonnet-5-5. PACE: wrap at 60 percent.
- notes.md: the reconstruction table, contradictions, what you could not measure, and the predecessor's open item quoted whole for Wednesday to rule.
- Return notes.md in full, plus the brief's line count and size.
