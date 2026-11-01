STARTABLE: YES (MPSCALC-317 only; MPSCALC-295 is NOT startable and is excluded from the kit)

# B1063 drafter report (lane M2, seat Datasec/MPS-M67), drafted 2026-11-01 21:45-22:20 AEDT

## BLUF
- The two tickets cannot share a seat because **one of them is not buildable**: the product owner ruled on 2026-10-24 09:24 (live message, verbatim in `CLARIFICATIONS.md` C-58, :1156-1163) "leave the words as they are"; the ruling's Settles line says nothing is built for the new sentence or the Review check and MPSCALC-295 stays open for his review. Jira agrees (1 comment, 2026-10-24T15:39, same effect). The sweep lane M2 read the ticket body but not that comment or C-58. The kit builds **MPSCALC-317 alone**; no Engine byte.
- MPSCALC-317 changes no sentence staff read and touches no figure on an existing quote. It touches a money default (the 7% rebate) only by deciding WHEN a new section may be added. The ticket's second option (apply the default on arrival) is refused in the kit as a design: a cleared rebate field and an early-click section both hold `undefined`, so a write on arrival would change figures on a priced draft (that is the STOP case the commission named; it is closed by choosing the first option, "Add section is not offered until the price list has loaded", which the acceptance check allows verbatim).
- Words gate: the fix is a `disabled` state, no `title`, hint or message (kit forbids any; a disabled button with no explanation is a Q for the seat to STOP on, not to fix with words). So no words gate applies and merge needs none under C-79 (:1712, "Done means merged to main"). Nothing deploys.
- Launch: STARTABLE once Tuesday stamps. Seat `Datasec/MPS-M67`, ports 9760-9769, Sonnet C2 (line 92), gate G2 (line 109) with Q-3, clock 2 h target / 4 h hard stop.

## Facts re-measured (instrument, control)
- main `3496da33ab3d7d2c6b7d7ec2c3014ae03518e020` (`git/ref/heads/main`, 21:59). Open PRs #121, #120 (control `pulls/99999` 404). `matching-refs/heads/b1063` 0 (control `b10` 60; all heads 159).
- Jira GET (project `.env` in process, JQL `project = MPSCALC AND ( key in (MPSCALC-295, MPSCALC-317, MPSCALC-99999) )`): returned 295 and 317 only (absent key = control). 317: Backlog, 0 links, 0 comments, updated 10-23. 295: Backlog, 0 links, 1 comment (10-24).
- Seat name: word-bounded `M67` over 90 non-`.pre-` SEAT kits of 10-31 and 11-01: 0 files (control `M6[0-9]`: 21 files). Ports: `lsof` 9760-9769 0 rows (control: 13 listeners overall); word-bounded `976[0-9]` over the same 90 kits 0 files (control `964[0-9]`: 2 files). Live panes: wednesday, HPSM-POC-R115, MPS-R117, NexusAI-R116, Security-Composer-J38, fleet-monitor.
- Live-branch sweep: `compare main...<branch>` over all 159 heads, counting files under QuoteScreen, `bom/`, ReadinessEvaluator, bomModel: of 9 heads fewer than 11 behind, 0 touch them (control: `b445/rebate-default-160-usage-screens-150` counts 25; merged PR #97, 40 behind).
- Source at main (raw `gh api -X GET`): the mechanism lines are in the kit (`QuoteScreen.tsx` :99-100, :547; `PurchaseBomEditor.tsx` :142; `bomModel.ts` `addSection` and `DEFAULT_REBATE_FRACTION = '0.07'`). `ReadinessEvaluator.cs` still holds "The quote has at least one device line.".
- CI web job predicate read from `ci.yml` at main: `npm ci`, `npm run lint`, `npm test`, then `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist` (Node 24), working-directory `web`. Written into the kit. Stamp-slot count of the kit: 8 (control for the REFUSE check).
- One suspect control: `zzz-no-such-string-7f3a` printed 1 against `CLARIFICATIONS.md` (it appears in the file's own text, from an earlier seat's recorded check), so I did not use that file for any absence claim; absence claims in the kit use the tree listing and raw source reads (control strings printed 0 there).

## D-decisions (all in the kit, override at the stamp)
D1 Sonnet C2. D2 one commit, at most one more. D3 hold only for a pricing-eligible caller; a failed read ends the hold. D4 one optional prop, default off; `bomModel.ts` untouched. D5 no register row (the register is engine-only), no doc edit. D6 MPSCALC-295 excluded. D7 pane/ports. D8 one plain push. D9 ASCII messages. D10 clock.

## Q-questions for Tuesday (each with a default)
- Q-1: Confirm 295 is excluded and the file name keeps "295" only because the task fixed the path. Default: YES excluded; a later kit if the product owner's review rules the words.
- Q-2: When the price list read FAILS, should a section added then carry the default? Default: no, keep today's behaviour (hold ends, no default), recorded as residual in the seat's decisions. (Applying a rebate when the server may refuse it risks a 403; not a design for a Sonnet seat.)
- Q-3: Gate G2 (tier 2, label `tier-2`, nothing deploys) rather than G1 (line 108)? Default: G2, round 1 of 2 on class "web: Add section waits for the price list". Tuesday should re-count the class in the project's gate verdict lines at the stamp (I did not read the 69+ STATUS files).
- Q-4: Sonnet C2 (line 92) rather than Opus C3 (money design, line 93)? Default: Sonnet C2, because the money default and its recipient are already ruled and the edit is spelled out in the ticket.

## UNMEASURED
No build, test, lint or run. `web/package.json`, node and npm were not probed. Whether any existing web test finds Add section while the read is pending; whether a second `setCatalogueError` site (count 2) or `checkOverlay` can re-open a hold; hosted behaviour (fenced); the gate-class count (Q-3). Lane M1 (B1062) kit is not on disk: its path set is inferred (Engine, Engine tests, `docs/ENGINE.md`, possibly the contract and web API copies), disjoint from the four paths in this kit; the kit refuses overlap and re-checks at Step 0 and before the push.

## Outside the fences
None. Reads only: Jira GET (project `.env` read in-process by a script in my session scratchpad, no token printed), `gh api -X GET`, tmux, lsof, local reads of the project's `CLARIFICATIONS.md` and `BACKLOG.md`. No decision-store read, no `decision_queue.sh`, no fetch/pull in a project repo, no cd. Read the sibling sweep's Jira snapshot (`mps.json`, 21:42) for the ticket bodies, then re-read status, labels, links and comments live. Wrote only these two files (plus session-scratchpad scratch).
