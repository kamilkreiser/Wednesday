# notes.md: Seat B 134th brief drafter, contradictions and gaps (2026-11-11, read 16:48 to about 17:0x AEDT)

Output: `brief_B134.md` (139 lines, 53,460 bytes; the two intermediate files `brief_B134.head.md` and `brief_B134.part2.md` are the pieces it was assembled from, left in place, nothing deleted). Every fact in it is either read by me (source and time in its PROVENANCE) or marked UNREAD.

## Contradictions and stale lines found (each with where, and what the brief does)

1. **The advisory card does not read as ruled in the card store.** The commission, R 96th's brief (line 32, board message `kam_msgs.sh 8`, 'card ruled_ts 16:30:23.548') and the B 133rd GO all say card `secuura-ghsa-chp3-effect-platform-shipped-1111` = a at 16:29:47. My `bash decision_queue.sh show secuura-ghsa-chp3-effect-platform-shipped-1111` at 16:49 AEDT printed `status: open (Secuura/Blockchain)` and `ruling: choice=None ruled_ts=None`. Either the board message is the authority and the card store has not caught up, or the ruling was not recorded. I did not run any write verb. The brief cites Kam's verbatim board message (as R 96th's brief and the commission do), says the card's artefact is the row 0 PR and its merge, and lists the card-store reading in PROVENANCE. **Wednesday should read the card herself before stamping.** Side effect to check: `send_brief.sh` gates on `decision_queue.sh list ruled --undelivered secuura-`; a card still `open` will not trip it, so nothing forces the section, which is why the brief carries it anyway.
2. **Fingerprint ADDENDUM versus HANDOVER (inherited from B 133rd's brief line 10).** The B 128th fingerprint ADDENDUM's check 'HEAD equals the origin develop you read' cannot hold: the shared checkout is HEAD `0e6479d7b6c0`, five squashes behind origin (B 133rd's HANDOVER), and is never a pull target. The HANDOVER says the composite `a4694cb31a596f35` was equal at B 133rd's boot. The brief states the expected value and HEAD explicitly, tells B 134th the ADDENDUM applies only to a launcher-pull difference, and says to QUESTION about that check rather than guess. I did not run the fingerprint (no git verb in the shared checkout beyond `ls-remote`).
3. **R 96th's brief is stale on three points (it was written 16:3x, before B 133rd merged):** it says develop = `249be7c8cd14` (now `6911aa643db1`; its own ROW 0 says cut from develop 'as ls-remote reads at the cut', so no defect for row 0, but the file it read, `audit-baseline.json`, is untouched by PR 2165, by my numstat of `249be7c8cd14..6911aa643db1`, two issuer frontend files); it lists B 133rd as live with PR 2165's GO 'sent 05:39Z' (B 133rd WRAPPED 05:46Z); its stamp item 6 says up to two BUILD seats may launch, while the commission for this brief says build lanes A and B are HELD. The brief follows the commission and says what is live.
4. **Counts and line numbers moved.** B 133rd's brief says 59 queued PRs including PR 2165 (merged): 58 remain (my program compare, 58 of 58 equal at 16:49:36). It cites history.md line 13 for B 132nd's entry and `Seat B 132` = 1; now B 132nd is at line 49 and `Seat B 132` = 2 (B 133rd's heading names it). The brief gives fresh controls and says to take your own.
5. **No Wednesday ANSWER to B 133rd's MERGED is on file** (briefs_staged ls at 16:48: only `_answer_plan.md` and `_go_2165.md` for B 133rd). Same pattern as B 132nd. The brief says her acceptance was inside the GO's 'after your MERGED, WRAP' and that the squash is confirmed by my ls-remote and the clone's commit object; nothing more.
6. **Row 0's tier string and gate do not exist yet.** R 96th's stamp item 8 says tier 2 (config), gate commissioned on its READY; no verdict, PR number, head, or GO tier string exists (no `feature/ks-2164*` branch on origin at 16:49:36). The brief does not invent them: it says they arrive by Wednesday's mail and the tier string is hers.
7. **B 133rd's brief text still names itself everywhere** (`_b133` kit names, 'Seat B 133rd', its BLUF/NEW SINCE/commission sections with the old develop and old live seats). Handled by pointing at named line ranges and saying which sections are SUPERSEDED, rather than copying; the risk is a B 134th that reads the whole 360 KB file. The brief says to read by line range and lists the five sections that bind.

## Things I added that the commission did not ask for (Wednesday: keep or cut at the stamp)

- Row 0 READY content list (single file, additions only, existing four keys untouched, JSON parses, `expires` equals the file's one existing value, guard split check) and a QUESTION rule on any deviation from R 96th's five-field shape.
- Row 0 MERGED lines (a) to (d), including (c): after the merge, `git show <squash>:Blockchain/Dev/scripts/audit/audit-baseline.json` in B 134th's clone parses and holds the new key with KS-2164 and 2027-02-28. The commission asks for ls-remote plus the merge commit; (c) is an extra check that the entry is really on develop.
- 'Send it at once: R 96th waits for it' (my inference from the commission's 'R 96th cuts every later row from that develop').
- The instruction to QUESTION if the advisory is cited in a merge refusal (carried from Wednesday's own plan answer to B 133rd, 2026-11-11 16:14, not new).

## UNREAD or UNMEASURED by me (the brief says so where it matters)

- Linear state of every ticket (KS-2164, KS-2091, KS-1922, KS-1875, KS-2015, KS-1954 and the 53 tail tickets), PR API state, live PR bodies and comments: UNREAD. Only ls-remote was read.
- Gate 306 and gate 307 verdict files: confirmed to exist by `ls`, NOT opened. Row text for 8y to 8zc is carried from B 133rd's queue table (lines 153 to 157), which I read whole.
- B 133rd's brief `## TRAPS CARRIED` (lines 217 to 234): not read; the brief points B 134th at it by name.
- Merge trees onto `6911aa643db1`: not computed (a merge-tree writes objects; I used read-only verbs only). B 133rd's trees onto `249be7c8cd14` are quoted as pre-PR-2165 and marked RECOMPUTE.
- The CI state (none: Actions has started no job since 2026-10-01, from the earlier gate 308 text, not re-read).
- R 96th's brief beyond lines 1 to 40; the HANDOVER's `evidence/` and `mail/` files other than `merge_trees_plan_b133.out`, `launch_preflight_b133.txt` and `drafts/wrap_body.txt`.

## Gate and format checks I ran on the brief (my own, not the send gate)

- Provenance: 77 lines after `PROVENANCE:`, each with at least two ` | ` separators, absolute source paths, `read 2026-11-11`.
- QUEUE-section ticket gate simulated with the `send_brief.sh` regex: 58 ticket ids in `## QUEUE`, 0 missing from PROVENANCE.
- The bare lines `PROVENANCE:` and (as a `##` heading the gate normalises) `RULED BY KAM, NOT YET IN AN ARTEFACT` are present. **No `SELF-CHECK:` line**: that is Wednesday's, added at the stamp (the send gate refuses without it). No stamp block is included (the placeholder I first drafted was removed).
- The brief contains no instruction to `cd`; it carries B 133rd's fault rules (no cd, `GIT_OPTIONAL_LOCKS=0`, no `.env` names, no key in argv).
- I did not write to Linear, GitHub, mail or any board; I used read-only git verbs only (`ls-remote`, `log`, `diff`) and `decision_queue.sh show` (read-only); scratch files are in the session scratchpad.
