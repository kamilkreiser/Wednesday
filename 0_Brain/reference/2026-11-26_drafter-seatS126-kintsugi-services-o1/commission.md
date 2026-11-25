# DRAFTER COMMISSION — brief for Seat S 126th (Secuura/Blockchain-S: READ-ONLY, two questions)

Written by Wednesday 2026-11-26 (morning). You are a DRAFTER: write ONE brief file and nothing else. No launch, no mail, no post, no box contact. Every project tree is READ-ONLY to you (git read verbs only; `git --no-optional-locks status`).

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatS126_kintsugi_services_o1.md`

## Template
Copy the SHAPE of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatS125_close2111_check1699.md` (read it WHOLE; it passed the send gate). The gate needs, as BARE lines: `PROVENANCE:` with every row `- <fact> | <source> | read YYYY-MM-DD HH:MM`; `RULED BY KAM, NOT YET IN AN ARTEFACT` (may be short); a final `SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM` written by Wednesday at the stamp (leave a placeholder line starting `SELF-CHECK-PLACEHOLDER`). Keep the seat-discipline sections; replace the work.

## Authority (quote verbatim)
- Kam, live board 2026-11-26 09:14:54: "Decision wed-morning-plan-1126: a — Carry on with the plan". The plan card named the next work as more closes as the board census allows.
- Kam, live board 2026-11-25 18:21:21: "Please close and merge and archive what you can. That looks like great progress."
- Kam, live board 2026-11-25 06:57:19: "keep working.  I will log in with a new account after usage runs out".

## Question A — which of these services RUN on Kintsugi today: guardian, queue, referral, tenant-provisioning, demo-service
Context: Seat S 124th's census (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_S124_wrap.txt` and its FINDINGS file beside it) left 8 tickets hanging on this question; find the 8 ids there and list them in the brief, with each one's dependency in one line.
The seat answers by READ-ONLY box reads through a boxrun runner exactly as Seat S 125th did (its REC: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-125th/`, its tools/ and DECLARED.md; the host-key fingerprint pin and the counted re-key of the runner's scratchpad path). Reads: `docker ps -a` rows (name, image, status, StartedAt) for every container, the compose service list the box runs from (read the compose file name from Seat D 87th's tools, do not guess), and whether each of the five services exists in the repo at the Kintsugi base 9c1ecde5abd6 (gh api, read-only). Per service, the answer is one of: RUNNING (container up), DEFINED-NOT-RUNNING, NOT-DEFINED-ON-THE-BOX, or UNMEASURED with the reason.
Then, per hanging ticket: what the answer means for it (closable, needs a deploy, needs Kam), as a PROPOSAL only. No ticket write.

## Question B — O1 from Seat S 125th
S 125th's live V2 (anonymous verify of a real certification) answered `checks.blockchainAnchored: true` while the same answer's blockchain object said anchoringStatus submitted, confidence pending-onchain, txHash null; the flag is a presence test at originate certifications.ts 1361 (ref 9c1ecde5abd6). Evidence: that REC's evidence/resp_V2.txt. KS-1805 (Backlog) records the same line for a FAILED anchor. The seat reads KS-1805 WHOLE (`comments(first:50)`, client-side sort) and answers: does its scope sentence cover the PENDING case? If not, it drafts a ticket text (BLUF, evidence, the code line) as a FILE in its REC and mails its path; it files nothing.

## Holds
Read-only everywhere: no Linear write of any kind, no GitHub write, no push except the seat's own vault daily-note commit at wrap (a plain push of that one commit is allowed), no HTTP request to any stack (box reads by ssh only), no docker command that writes, no demo/demo-pk/prod contact, no mail to humans, no cards.

## Routing
Model: Sonnet (Wednesday fills the id at launch). Lane -S. Seat name exactly `Seat S 126th` (check the ordinal in history.md: must be 0, control S 125th must be 1).

## Return
Path, byte count, every UNVALIDATED fact, and every commission fact you found WRONG with its source.
