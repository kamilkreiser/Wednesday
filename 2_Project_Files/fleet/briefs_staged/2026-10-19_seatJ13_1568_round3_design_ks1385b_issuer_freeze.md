## BLUF

You are Seat J 13th (Secuura/Blockchain-J, the J LANE), successor of J 12th. Kam has ruled TWO cards this morning (06:43, live board), and both are yours:

1. **#1568 (KS-1612 + KS-1385 (b)) gets a THIRD round, DESIGN FIRST.** Kam's ruling, card `secuura-ks1612-third-round-after-cap-1018` = **a** "Allow a third round". Option detail, verbatim: "Seat J designs the fix first, Wednesday rules it, then one more full Opus gate. If that also fails, it stops for you again." So: **write the design, mail it as a QUESTION to Wednesday, and build nothing until Wednesday rules it.** Round 3 is the last; a NO GO stops for Kam.
2. **KS-1385 (b): the certificate holder's organisation may update the anchored identity, but NOT the issuer fields.** Card `secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018` = **b** "Holder may update, but not the issuer fields". Option detail, verbatim: "A follow-up keeps issuerOrgId, orgDid, orgTrust and orgVerified as first anchored, and lets the holder change only the rest. A small build and its own gate." A SEPARATE PR with its own gate. Your design (item 1) states its order relative to #1568.

**New input since J 12th wrapped:** Stuart commented on KS-1612 at 2026-10-18T11:42:31Z, one minute before J 12th's wrap; it is still the newest comment on the ticket (Wednesday's read today), so nobody has replied on the ticket. Read it whole. Wednesday read it; in short (Stuart's words, not re-measured by Wednesday): S's PS-1285 (16 Oct) removes S's need for this residue before the rulings go live; MAJ-A's class includes EVERY S flat anchor (S's `POST /api/anchors` carries a ledger chain id with no K document); **no legitimate S flow anchors before it registers under the same id, so option (ii) and option (i) break no S flow**; S still prefers (iii) KS-1384.

## QUEUE

1. **Design for #1568 round 3 (no code yet).** Inputs: J 12th's handover `Blockchain/5_Project_History/2026-10-18_seatJ-12th/HANDOVER.md` (AT WRAP row 2 and the section "Design notes on MAJ-A's three residue options"), the round-2 NO GO verdict it names (sha256/16 `3486a4efab9b5d1f`), Stuart's 11:42Z comment on KS-1612, and the code at develop `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`. Your QUESTION mail (topic `round 3 design 1568`) carries: the option you propose ((i), (ii), (iii) or a combination) and why; what it closes (MAJ-A, MIN-A must be closed in any round); what it does NOT close, stated as narrowing; the census it needs and how you will run it; the red-first cells; which of Stuart's facts it RESTS on (each fact quoted, and how you will confirm it from K's side where you can); and every writer of `anchor_store` you found, enumerated with file:line (Wednesday has not measured this). If your preferred option is (iii) KS-1384, say so plainly and size it: that is a bigger change than a round, and Wednesday will decide whether it fits inside Kam's "third round" or goes back to him.
2. **After Wednesday rules the design:** build round 3 on #1568's branch (head `767ab575818f75b68664ddad1a511478db63c09d`), red-first, then READY FOR GATE (tier 1, Opus). Merge only on Wednesday's GO naming the head.
3. **KS-1385 (b) issuer-field freeze:** a small follow-up PR (its own branch, its own gate): `issuerOrgId`, `orgDid`, `orgTrust` and `orgVerified` keep their first-anchored values; the holder's organisation may change only the rest. Read the KS-1385 comments first (9 comments, last 2026-10-18T11:39Z). Order relative to #1568 comes from your design and Wednesday's ruling; nothing is deployed in either order, and no deploy is commissioned here.

## PARTITION

Yours: `services/anchoring/` (anchorOverwriteGuard and its tests), originate's `saveDocument` path and documentRepo for KS-1612, migration 050 and any new migration this design needs, and the KS-1385 (b) follow-up's files. **NOT yours:** Seat R 49th (Secuura/Blockchain-R) is live on the same inbox. Its next work is a set of Spark passes for KS-1628 items 2-3 (including `services/anchoring/src/anchorReadback.ts` and a comment in anchors.ts), KS-1622, KS-1621, KS-1620 (`services/mcp-server/src/tools/info.ts`) and a KS-1627 test cell in `services/api-gateway/src/__tests__/`. **`anchorReadback.ts` and anchors.ts are R's for KS-1628:** if your design needs either, say so in the QUESTION and Wednesday sequences it. You share one inbox: a mail addressed to Blockchain-R is not yours.

## HOLDS

- No deploy, no demo, no production. Merges only on Wednesday's GO naming the head SHA, after the gate. Never `--no-verify`, never `--force`.
- Push with the transport named in full: `GIT_SSH_COMMAND` unset and `git -c core.sshCommand="<the repo's own core.sshCommand> -o ServerAliveInterval=30 -o ServerAliveCountMax=20" push ...`.
- Client-facing communication = ticket comments only; the extranet is not a channel. Nothing to Stuart or Peter beyond ticket comments. **Do not reply to Stuart's comment until Wednesday has ruled the design** (the reply states what K is doing, and that is decided in the ruling).
- Never delete; quarantine. Every loop in a script FILE, never inline `bash -c`. An EXIT trap that restores a file uses an ABSOLUTE path.
- Wait instructions name their wake: re-arm your watcher first (J 12th handover "Mail" row) and read its log at every break. Your wake after the QUESTION is Wednesday's ANSWER.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- secuura-ks1612-third-round-after-cap-1018 = **a** "Allow a third round" (2026-10-19 06:43:16, live board). Option detail verbatim in the BLUF. Lands in: #1568 round 3 + a KS-1612 comment.
- secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018 = **b** "Holder may update, but not the issuer fields" (2026-10-19 06:43:25, live board). Option detail verbatim in the BLUF. Lands in: the KS-1385 (b) follow-up PR + a KS-1385 comment.
- Kam's earlier rulings on this subject stand as J 12th's brief recorded them: secuura-ks1385-null-issuer-certifications-1015 = **b** (apply the custodian rule to no-issuer rows; it is what #1568 carries), secuura-ks1385-custodian-may-update-anchor-identity-1013 = **c** (merged in #1549). Today's (b) above NARROWS what the holder may write; it does not undo either.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- The GO is addressed to the J LANE, never to a named seat.
- Linear links stay `contributes`; a ticket closes only once tested, working and deployed.
- Wednesday WITHDREW her earlier ruling on the KS-1114 reply shape (test header :11 on #1555); do not cite it.

PROVENANCE:
- KS-1612 state (open: In Progress, assignee kamil.kreiser@secuura.ai, 5 comments, last 2026-10-18T11:42:31Z by stuart.jamieson@secuura.ai, body READ by Wednesday) | Linear ticket KS-1612 | read 2026-10-19
- KS-1385 state (open: In Progress, assignee kamil.kreiser@secuura.ai, 9 comments, last 2026-10-18T11:39:34Z) | Linear ticket KS-1385 | read 2026-10-19
- KS-1384 state (open: Backlog, 1 comment, last 2026-10-02T03:00Z; NOT queued here, named only as option (iii)) | Linear ticket KS-1384 | read 2026-10-19
- develop 83ed01af70fd5ed6cca9ac66f28ddcb8a1034105 | git ls-remote origin (develop), run by Wednesday, not a path in your tree | read 2026-10-19
- #1568 head 767ab575818f75b68664ddad1a511478db63c09d | git ls-remote origin (pull 1568 head), run by Wednesday, not a path in your tree | read 2026-10-19
- J 12th's handover and its design notes | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-18_seatJ-12th/HANDOVER.md, read whole by Wednesday | read 2026-10-19
- Kam's card rulings | Wednesday's tools/kam_msgs.sh (live board) + tools/decision_queue.sh show/rule - my project, not yours | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 06:47
