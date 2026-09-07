# BRIEF — Secuura/Blockchain seat s149, morning 2026-09-08

## BLUF
**KAM'S NEWEST INSTRUCTION LEADS THIS QUEUE** (panel 2026-09-08 07:10:32, verbatim through the
dictation noise — "the kit" is his kids): *"I'm going to drop off the kit if we please deploy and
merge everything that has been tested and done and is ready for deployment."* He is out of contact
for a while and expects it done.

**MEASURED BY WEDNESDAY, from the board in the same action as writing this: 24 issues sit in
`Tested Not Deployed` across KS and PS** (`board_count.sh`, limit 250, so a real count and not a
cap) — and **NOTHING has been deployed at all.** The demo box is `632f16dfe`; develop is
`400517aaf`. The gap is everything merged since.

**Item 1 is the deploy sweep. Items 2 and 3 are the two rounds Kam ruled this morning.**
**Nothing merges or deploys without Wednesday's GO on the SET — that is the one gate, and it is
there because a 24-ticket deploy has a blast radius nobody has stated yet.**

Your predecessor s148 wrapped at 05:32 with a clean ritual and scored 1.0. **Read
`5_Project_History/HANDOVER-s148.md` FIRST** — it front-loaded the round-4 plan and records its own
mistakes. The two Majors in item 2 are quoted FROM it.

RULED BY KAM, NOT YET IN AN ARTEFACT
- **`secuura-892-round4-passed-but-introduced-two-majors` → `round5`** (panel 2026-09-08 07:08:30,
  verbatim): *"ONE more narrow round — F-1 and F-2 only, F-2 first"*. **Must land on #892's ticket
  trail as the authority for this round.**
- **`secuura-ks968-rotation-three-worlds` → `separate`** (panel 2026-09-08 07:09:37, verbatim):
  *"Authorise the one two-boolean statement — it settles which of the three worlds this is"*.
  **Must land on KS-968 as a comment carrying the result and the world it selects.**
- **`secuura-ci-dead-19-days-blocks-your-own-ruling` → `fix`** (panel 07:07:42): Kam is fixing the
  GitHub billing / spending limit HIMSELF. **Consequence for you: CI is still dead — 2,000 runs,
  100% `startup_failure` back to 2026-08-20 (s148's measurement, not Wednesday's). Do NOT wire
  anything into Actions and do NOT treat a green Actions run as possible. KS-961 stays untouched
  until Kam says billing is live.**

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **SCOPE, and read this carefully because an earlier draft of this brief said something narrower:**
  **item 1 covers the merge set YOU enumerate and Wednesday approves** — that is deliberately more
  than one branch. **#892 is the only branch in scope for ITEM 2**, and #892 is **NOT** in item 1's
  merge set. develop is `400517aaf` and NOTHING is deployed. Do not touch **#891** (Kam's own
  click), **KS-961** (CI is dead until Kam fixes billing), or **KS-811's derivation** this round.
- **Handovers to Peter/Stuart are TEST BLOCKS** (stream parent · PRs in the block · the one pass
  that proves it · what the human does), never a list of PRs.
- **Client-facing communication is ticket comments only.** The extranet is not a channel.
- **Ticket creation AGGREGATES:** one larger ticket per logical path, items as a checklist — never
  three tickets for one line of work (Kam 2026-09-07 13:23).

## QUEUE — in this order

### 1. THE DEPLOY SWEEP — Kam's 07:10 instruction. Report, then Wednesday GOes, then you act.
**Step 1a — ENUMERATE, do not act.** You hold the Secuura GitHub identity and Wednesday does not, so
this measurement is yours and Wednesday cannot take it on trust from anywhere else:
- every OPEN PR on `Secuura/Distributed_Secuura`, with its head SHA, its base, its gate verdict if
  one exists, and whether it is mergeable;
- which of them are **gate-passed and unmerged** — those are "tested and ready" in Kam's words;
- the exact diff `632f16dfe..400517aaf` at the level of "what a user of the demo would notice".
**Mail that set to Wednesday and STOP.** Do not merge on your own reading of "ready".

**Step 1b — on Wednesday's GO, merge the approved set only.** Each merge: tree predicted with
`merge-tree` BEFORE, parents re-derived from the object AFTER, and a **negative control that #892's
frozen work did not come along** — exactly the discipline you used three times last night without a
surprise. **#892 is NOT in the set. #891 is KAM'S OWN CLICK and is NOT in the set.**

**Step 1c — the deploy, and it is the part to slow down on.** Before anything ships:
1. **Re-derive that the KS-978 deploy blocker is actually closed on the trunk** — #897 is merged and
   `develop` is `400517aaf`, but re-read the contract text on the trunk rather than trusting the
   ticket. **That blocker is the reason nothing has shipped for two days; if it is not closed, STOP
   and mail Wednesday.**
2. **State the ROLLBACK before you deploy** — the exact command and the SHA to return to
   (`632f16dfe`), in the mail, before the deploy runs. A deploy whose undo is not written down is
   not authorised.
3. **Deploy.**
4. **Verify at the destination, not at the exit code** — the demo actually serving, a login working,
   the changed surface behaving. An exit 0 is not a deployment.
5. **Move the 24 tickets out of `Tested Not Deployed`** to the state your board uses for shipped, and
   comment the deploy SHA on each. A ticket left in the old state is what makes the next sweep wrong.

**FLAG IT TO KAM.** He lifted the production ban for this week on one condition, verbatim: *"flag
these when relevant or when making changes."* Mail Wednesday the moment the deploy starts and the
moment it finishes, with what changed and where — Wednesday puts it on his panel while he is out.

### 2. #892 round 5 — F-2 FIRST
**F-2 (MAJOR — do this one first).** Quoted from HANDOVER-s148: `pre_suite.test.sh` **silently
quarantines a developer's live manifest and still reports `24 passed, 0 failed`.** Round 4 made
`pre-suite.ts` quarantine on the catch path, and that suite drives `pre-suite.ts` for real without
protecting `generated/`.
**The fix shape is already in the repo, written by your predecessor in the SAME commit:**
`quarantine_call_sites.test.sh:42-55` stashes `generated/` and restores it in a `trap … EXIT`, with
the comment *"the real generated/ is this repo's, not ours."* **That file is the model — give
`pre_suite.test.sh` the same stash/restore.**
**Why it blocks:** the tester's sentence is *"it REINTRODUCES KS-969's OWN FAILURE CLASS FROM INSIDE
KS-969's OWN TEST SUITE."* A fix that reintroduces the class it removes is not residue to ticket.

**F-1 (MAJOR, but LOUD — second).** The new call at `pre-suite.ts:157` is **inside the catch**, so if
`quarantineManifest` itself throws there is nothing left to catch it and `runPreSuite` **throws** —
against its own docstring at `:90-91`, *"Never throws: classifying the failure IS this function's
job."* `manifest.ts:107-114` is a **TOCTOU** (`existsSync` then `renameSync`). **Measured by the
gate:** two concurrent runs in one checkout crash **9 of 12**; parent-commit control **0 of 12**;
`run-in-slot.sh` documents that slots run in parallel.

**F-3 (MINOR — the strict arm quarantines and the banner does not say so) is NOT in this round.**
It stays ticketed.

**Red-proof both, and prove the discriminator first** — your predecessor's own standing line: it
planted a **syntax error** (1 cell executed, no trailer) and an **inert comment** (10 passed) BEFORE
believing any red-proof, so a build break and a genuine red could not be confused. **A cell that
reds by failing to BUILD proves nothing.** Report the EXECUTED-cell count under each tamper.

### 3. KS-968 — EXACTLY ONE statement, then stop
```sql
SELECT (email_lookup_hash IS NULL) AS hash_null,
       (email = 'issuer@secuura.com') AS addr_unchanged
FROM users WHERE id = 'a0000000-0000-4000-8000-000000000030';
```
**Two booleans. No address returned, no hash returned, no row data, no write.** Pre-register and hash
your expectation first, as all previous runs did, and assert `is_superuser=on` — a non-superuser
count on a FORCE-RLS table returns 0 and would manufacture the benign answer.
**The decision table, and it is the whole point:**
- `hash_null = true` → world **(c)**, benign (P counted non-null hashes across the table, not this row's).
- `hash_null = false, addr_unchanged = false` → world **(b)**, benign (the address was changed after seeding, so a differing hash is CORRECT).
- `hash_null = false, addr_unchanged = true` → world **(a)**, and it **IS an incident** — login resolves users by `email_lookup_hash`, so rows written under a superseded key cannot be found by address and **those accounts cannot sign in by email on the demo.**
**A THIRD QUERY IS OUTSIDE KAM'S WORDS.** An ambiguous result is a finding to report, never a licence
to widen. Your predecessor declined to argue one into scope; hold that line.

## HOLDS — these bind you
1. **No merge, no deploy, no push to develop without Wednesday's GO.** develop is `400517aaf`.
2. **Kam's signature classes still stop:** production · money · external communication to any human
   (Peter, Stuart, HP) · anything irreversible. The production ban is lifted for this week, but
   **every production change is FLAGGED to Kam before where there is time and immediately after
   where there is not** — and nothing in this queue should touch production at all.
3. **NOTHING further on the demo box** beyond the one statement above.
4. **Only Secuura on this machine** (Kam, panel 07:08:23): *"only secuura projects on this machine
   until further notice."*
5. **No `rm`.** Cleanup means quarantine into a dated folder.
6. **If an instruction here looks wrong, say so.** Your predecessor corrected Wednesday's escalation
   logic twice yesterday and was right both times. That is the behaviour, not an exception to it.

## DEFINITION OF DONE
- **The deploy sweep: the set enumerated and mailed, Wednesday's GO obtained, the approved set
  merged, the rollback SHA stated in writing BEFORE the deploy, the deploy verified at the
  destination rather than by exit code, the 24 tickets moved with the deploy SHA commented, and Kam
  flagged at start and finish.**
- F-2 and F-1 closed on #892, each with a red-proof whose discriminator was proved first, and the
  EXECUTED-cell count reported under each tamper.
- The KS-968 statement run once, its result and the world it selects commented ON KS-968.
- A STATUS mail to Wednesday: branch + SHA, sets not counts, what you did NOT do.
- **Then STOP and hold.** The gate is Wednesday's to commission; the merge is Wednesday's to give.

PROVENANCE:
(every load-bearing fact, its source, and when it was read)
**Wednesday holds NO Secuura GitHub identity and no database access. Every SHA and every repo fact
below is RELAYED, not re-derived here — that is why item 1a is your measurement and not Wednesday's.**

- 24 issues in `Tested Not Deployed` (KS + PS) | `2_Project_Files/fleet/board_count.sh linear` with filter `{team:{key:{in:["KS","PS"]}}, state:{name:{eq:"Tested Not Deployed"}}}`, limit 250, returned 24 so it is a count and not a cap | read 2026-09-08 07:1x
- The 24 identifiers and titles | Linear GraphQL `issues(filter:…, first:100)`, returned 24 | read 2026-09-08 07:1x
- 113 active KS + 30 active PS | same `board_count.sh` tool, separate queries | read 2026-09-08 06:0x
- `develop` = `400517aaf` · demo box = `632f16dfe` · #892 frozen at `1e31c80b9` | s148's wrap mail 2026-09-07T19:32Z **and** `5_Project_History/HANDOVER-s148.md` | read 2026-09-08 05:3x — **the seat's read, NOT re-derived by Wednesday**
- F-2 and F-1, including `quarantine_call_sites.test.sh:42-55`, `pre-suite.ts:157`, the docstring at `:90-91`, `manifest.ts:107-114`, and the 9-of-12 / 0-of-12 concurrency measurement | `HANDOVER-s148.md` lines 241-260, quoted verbatim | read 2026-09-08 07:1x — **the gate's and the seat's measurements; open the file and confirm the line numbers before you act on them**
- Kam's four rulings, verbatim | `0_Brain/dashboard/data/chat_log.json` + `2_Project_Files/tools/kam_rulings_today.sh` on a freshly pulled copy | read 2026-09-08 07:07:42 → 07:10:32
- The KS-968 statement, its three worlds and the decision table | decision card `secuura-ks968-rotation-three-worlds`, its BLUF quoted | read 2026-09-08 07:1x
- CI dead: 2,000 runs, 100% `startup_failure`, back to 2026-08-20 | comment by the seat on **KS-961**, 2026-09-07T03:30 | read 2026-09-08 06:0x — **the seat's direct verification, attributed; Wednesday could not check it**
- `Secuura/Distributed_Secuura` as the repo/org | `git -C "…/Blockchain/2_Project_Files" remote -v`, read-only | read 2026-09-08 07:1x
- **BLAST RADIUS of the deploy: NOT ESTABLISHED by Wednesday, and this is a refusal to guess it.** Wednesday holds no Secuura GitHub identity, no demo access and no deploy mechanism, so it cannot enumerate the consumers of a `632f16dfe..400517aaf` ship — 24 tickets' worth of merged change. **UNMEASURED as of 2026-09-08 07:1x. Establish it in step 1a and put it in the mail BEFORE any deploy runs; Wednesday's GO is conditional on reading it.** Nobody has yet written down what a demo user would notice, and that sentence is the thing the GO turns on.
- KS-969 state: **In Progress**, updated 2026-09-07T09:02, 2 comments, last comment 2026-09-07T08:17 | Linear ticket KS-969, read directly | read 2026-09-08 07:2x — **named here only as the FAILURE CLASS F-2 reintroduces, not as work in this round; it is open and it is not yours to close.**
- KS-978 state: **Tested Not Deployed**, updated 2026-09-07T12:24, 2 comments, last comment 2026-09-07T12:24 | Linear ticket KS-978, read directly | read 2026-09-08 07:2x — **it is one of the 24 in the deploy sweep, and it is the DEPLOY BLOCKER's own fix. Its state is the reason step 1c re-derives the contract text on the trunk before shipping: the ticket says the blocker is closed, and a ticket is a claim.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 07:14
