STARTABLE: YES (after Tuesday's stamp; defaults make it comment-only)

# B1316 DRAFTER REPORT (SEAT-R180, MPS records, Done pass over ten keys)

## BLUF
- Kit: `2026-11-06_B1316_SEAT-R180_mps-records-done-pass.md` (template R172, `.pre-stamp` copy read whole); slots: `2026-11-06_B1316_slots.json`.
- **MPS has its own Done rule: C-79.** `CLARIFICATIONS.md:1712` (heading), `:1714` ("Done means merged to main, the same as Composer"), `:1716` (Settles), `:1727` (the three conditions: slot, every Done-when clause MET, no gate/review line or red run contradicts; "a merge is necessary and never sufficient"). MPS `CLAUDE.md` has none (82 lines; only `:44`, `:67` mention "done", both setup status). The sweep's quote is HPSM-POC's `CLARIFICATIONS.md:5114`; the kit says so and quotes C-79 instead.
- **-341 cannot move under C-79 as written:** `:1716` names it among tickets whose work is a ruling or measurement with no merged change ("stay as they are"). Its "acceptance reads MET" comment is a measurement with nothing pushed. Comment only.
- Drafter's first read of the ten (seat re-derives): none moves on defaults. Holds: -98 (mutant red-proof is the builder's own record only, reading q), -335 / -374 (residuals held only as backlog rows, reading k), -336 (gate NO GO at the cap, reading j), -340 (see Q-3), -358 (contract text NOT MET: `docs/API.md` names `quantityRule` on 0 lines, control `pricingMethod` 5; the editor is not built), -362 (Api half: reason for "open" has gone, see below), -375 (coordinator regrade NO GO at the cap; clause B not re-derived), -377 (optional sign row not built).
- The sweep is STALE on -340: B765-1/-2/-3 are MPSCALC-352, Done 1 Nov (MPS #128, gate GO WITH FINDINGS). -336's residue is filed as -340 and -341.
- -362 changed since its last comment: `PurchaseMapping.cs:36,:103` now map the rule (MPS #150) and `QuoteApiTests.QuantityRule.cs:94` asserts the key absent by default (`:101`, `:103`). Whether a gate ran a mutant for it is the seat's read (B1165).
- The product owner's 6 Nov 10:12:54 words are recorded verbatim as C-95 (slot REC-CLAR-95; heading question defaults because the card's question is unknown to the drafter). The entry says it does not change C-79, grant a slot or lift a hold.
- -384 (and -383) NEVER; no create; at most 10 comments and the stamped moves.

## Facts re-measured (instrument; control)
- Clock `date`: Fri 6 Nov 2026 10:30:29 AEDT at the Jira counts.
- Root: `git --no-optional-locks rev-parse HEAD main` both `3f6657b8ea5fb3d4e105c4d76f43e982c87088dd`; CLARIFICATIONS 2569 lines, highest C-94 at :2560 (anchored scan; `^### C-95( |$)` 0, control C-94 1); dirty tree = BACKLOG.md, JIRA.md, history.md only. `.tools/.git-lock` absent; `.tools/b1316` absent; `.tools/b1277`, `.tools/wt-b1277-records` exist (read-only for the seat). `df -g /` 358 GiB.
- Code main `3b1ec832...` by `gh api -X GET .../git/ref/heads/main` (unchanged since R172); open PRs 0 (control `pulls/99999` 404). `pulls/N` merged true for #34, #111, #114, #117, #126, #137, #141, #150, #151, #152, #153 (squash shas in the kit).
- Jira (own GET, project `.env` in-process): 384 issues = highest key; Backlog 238, Done 146; all ten Backlog; comment totals -98 2, -335 2, -336 2, -340 2, -341/-358/-362/-374/-375/-377 1 each; transitions 11/21/31/41 read on -98 and -336; `text ~ "B1316"` 0 (control `B1196` 6), `labels = "mpscalc-b1316"` 0, `key = MPSCALC-269` 1, nonsense 0.
- Pointers printed by `grep -n`/`awk NR==n` at the squash: `B74.cs:66,:99`; `QuantityAudit.severalDevices.test.tsx:157` (c5; no negative-quantity row, control `counted` 39); `contract.sync.test.ts:20-25`; `check-bundle.mjs:37`; `QuoteApiTests.QuantityRule.cs:94`; `openapi.json:1705,:1893`.
- Ports: `lsof -nP -iTCP:9900-9999 -sTCP:LISTEN | wc -l` 0; word-boundary scan of 21 non-`.pre-` SEAT kits of 5-6 Nov for R180, MPS-R180, b1316, B1316: 0 each, control R177: 1. Pane list: `wednesday`, `fleet-monitor` (no `Datasec/MPS-` pane). B1316 is free (only B1311 of the B131x range exists).
- Model: `model-routing.md:98` (C8), `:110` (G3); `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` defaults opus (launch line carries `BRIEF_SEAT_LEVEL=sonnet`).

## D-decisions the kit takes
- D-1 Rule is C-79. D-2 Defaults comment-only (MOVE-KEYS NONE, CAP-READING NO, ROW-RESIDUAL NO, RESIDUE-CLOSED NO). D-3 -341 comment-only regardless. D-4 -384 and every other key untouched. D-5 One comment per key with the present table; earlier comments never edited.

## Q-questions for Tuesday (each with a default)
- Q-1 Does MPS hold any Done rule other than C-79? Default: no; C-79 as quoted. (If you say none exists, the kit would only comment and move nothing: set MOVE-KEYS NONE, which is already the default.)
- Q-2 Which keys may move? Default NONE. Drafter's read: with CAP-READING YES, -336 would be the only candidate as worded (reading i); with ROW-RESIDUAL YES, -335 and -374 (and -362 if its item 3 reads MET). Each is the coordinator's reading, not the product owner's; the kit lets the seat re-derive each before any move.
- Q-3 Should -340 be released, given its residue (B765-1/-2/-3) is closed by Done -352? Default NO (slot RESIDUE-CLOSED NO): reading (i) is worded for the cap and its gate was round 1 of 2; releasing it needs a NEW coordinator reading, which the kit names but does not apply unless stamped YES.
- Q-4 Is -377's optional item 2 (sign row) a clause? Default YES (the Acceptance names it), so -377 holds.
- Q-5 What question did the 6 Nov 10:12:54 words answer (for the C-95 heading)? Default: the kit's phrase "What is the order of work now that user acceptance testing is held?" and "(the product owner's 2026-11-06 ruling)"; the entry says the heading's question is the record's phrase, not the card's.
- Q-6 CARD-REF: default NONE (no card id known to the drafter; I did not query any card store).
- Q-7 Comment on every key even where the last comment already says the same (-341, -358)? Default YES (the ask was a comment with evidence on each); set COMMENTS HOLD to skip all.

## UNMEASURED
No test run; no Jira write; gate STATUS files read only at verdict lines; whether a gate ran the "key written by default" mutant (-362 item 3); -375 clause B under the gate's mutants; hosted state; whether M94 is launched (no M94 kit on disk at drafting); the product owner's words/time are as relayed by the commissioning message, not read from the decision store.

## Outside-the-fences disclosure
Read-only throughout. I used a scratch Python reader in the session scratchpad (`jr.py`, `jc.py`) that reads the MPS project `.env` in-process, never printing a token, for Jira GETs only (issue, comments, transitions, search). I used `gh api -X GET` under the MPS `GH_CONFIG_DIR` for pulls, ref, contents and a tree read. I read the MPS root records files (CLARIFICATIONS, CLAUDE.md line counts) and `.tools/b1242/showjira.py` and `lib1242.py` for the reader shape. A first Bash attempt containing `cd` was refused by the hook and re-issued without it. No `decision_queue.sh`, no card store, no fleet/briefs_staged, no scoreboard, no _ledger.md, no WEDNESDAY/FRIDAY tree. Files written: the three B1316 files in the briefs folder only (plus scratch in the scratchpad).
