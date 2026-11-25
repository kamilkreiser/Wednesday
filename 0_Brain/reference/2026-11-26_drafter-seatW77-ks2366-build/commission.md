# DRAFTER COMMISSION — BUILD brief for Seat W 77th (Secuura/Blockchain-W: KS-2366, certification anchoring honesty + confirm path)

Written by Wednesday 2026-11-26. You are a DRAFTER: write ONE brief file and nothing else. No launch, mail, post, push or box contact. Project trees are READ-ONLY to you (git read verbs only; `git --no-optional-locks status`).

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatW77_ks2366_build.md`

## Template
For BUILD-seat discipline (own worktree from origin develop, branch naming, push of the seat's branch only, PR opened with a Test Evidence block, READY FOR QA, no merge, no deploy) copy the SHAPE of the most recent W-lane build brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/` files matching `*seatW76*` (find them; read the brief WHOLE). For the gate-line format (bare `PROVENANCE:` with rows `- <fact> | <ABSOLUTE path, URL or command> | read YYYY-MM-DD HH:MM`; bare `RULED BY KAM, NOT YET IN AN ARTEFACT`; a `SELF-CHECK-PLACEHOLDER` line) follow `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatS127_ks1971_ks2366.md`. Read the project's own `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md` and the Secuura client CLAUDE.md for branch/PR/merge rules and quote what governs a build seat.

## Authority (quote verbatim; re-read on the live board with `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh 5 --source live`)
- Kam, live board 2026-11-26 10:28:40: "Decision secuura-ks2366-what-anchored-means-1126: a — Anchored = confirmed on chain". The card's option a detail (decisions.json, id secuura-ks2366-what-anchored-means-1126): "verify says true only for a confirmed anchor (the rule another verify surface already uses); a seat also builds the missing confirm path for certifications; gated, deployed to Kintsugi first".
- Kam, live board 2026-11-25 06:57:19: "keep working.  I will log in with a new account after usage runs out".
Put the first in RULED BY KAM, NOT YET IN AN ARTEFACT -> lands in the PR and, after merge, KS-2366.

## The work (two parts, ONE PR, on KS-2366)
Sources to read WHOLE first: KS-2366 description and its comment 693f1d9e (Linear); Seat S 127th's STATUS `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_S127_status.txt` (the writer list, file:line at 9c1ecde5abd6, identical at develop 59e89c87719e for originate/src); `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-127th/HANDOVER.md`.
1. HONEST FLAG: `checks.blockchainAnchored` on POST /api/certifications/:id/verify (originate routes/certifications.ts ~1361, `!!certification.blockchain`) becomes true ONLY for a confirmed anchor. Reuse the existing stricter rule rather than inventing one: `routes/verification.ts` `isAnchoredHonestly` (~119-140) — the seat decides how to share it, and says why. Keep every other field of the answer and the anonymous/charge behaviour (KS-1699 rulings) unchanged; name the tests that pin them.
2. CONFIRM PATH: a certification row must be able to reach `blockchain.status: 'confirmed'` (with txHash/blockHeight) when its anchor confirms. Today every confirm writer keys on `external_id`, which certification rows lack (documentRepo.ts writeAnchorBlobIf ~996). The seat designs the smallest correct change (e.g. the conditional writer matching a certification row by primary key with the same status guards, and the poller/reconcile/heal reaching certifications) — a DESIGN step: its plan QUESTION must state the design, the alternatives considered, and the cross-tenant / overwrite guards (anchorOverwriteGuard.ts) it keeps, BEFORE any code. It must not touch a document row's existing behaviour; name the tests that prove that.
3. Tests: red-first (a cell that fails on develop for each part), then green; the paired-mutation discipline of the fleet; unaffected suites green. A migration is NOT expected; if the design needs one, that is a STOP and a QUESTION (data-changing path, row C4).
4. Stop at READY FOR QA: push its own branch, open ONE PR on develop with a Test Evidence block (what ran, what did NOT run), mail READY. No merge, no deploy, no Linear write, no comment.

## Holds
No merge, no deploy, no box contact, no Linear write, no mail to humans, no cards; no force push; no edit outside the files the design names (list them in the plan). The QA gate (tier 1: security/verify surface) and Wednesday's GO precede any merge; Kintsugi first after merge, by a D seat.

## Routing
Model: OPUS (routing row C3; Wednesday fills the id at launch from models_latest.json levels.opus). Lane -W. Seat name exactly `Seat W 77th` (Wednesday measured: score 0, history 0; control W 76th: history 2 — re-check).

## Return
Path, byte count, every UNVALIDATED fact, every commission fact you found WRONG with its source, and the file list you expect the change to touch (by reading, not as a ruling).
