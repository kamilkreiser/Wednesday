# s141b — SEAT A successor brief (Secuura / Blockchain, Platform K)

You are seat A. Your predecessor s141 wrapped at 22:07 and scored **0.95**: two merges verified from
objects, the live validate-then-fetch SSRF gap CLOSED on develop, nine tickets, KS-931 finished to
READY with nothing started after it exactly as instructed, and nothing deployed at all.

## BLUF
**Your work this round is KS-926's campaign, and its first act is to STATE THE FAMILY — not to fix
one ticket at a time.** Your predecessor's own framing, and it is right. **#870 is NOT yours this
round:** its re-gate is running as this brief is written, and its GO or its fix round will reach you
as its own DKIM-verified mail. Do not chase it, do not pre-empt it, and do not touch its branch.

## WHY YOU ARE LAUNCHING NOW
Seat B's KS-911/KS-912 launcher change was live on disk and ungated, which blocked every Secuura
relaunch including yours. Its by-hash gate returned PASS WITH FINDINGS at 12:18:53Z — shipped hashes
unchanged end-of-pass, 0 defects in the changed lines, and none of its five findings blocks a
relaunch. **The block is lifted.** Those five findings are SEAT B's to file, not yours; one of them
matters to you and only one, and it is in the next section.

## THE FLOOR — read from objects at Wednesday's seat, READ verbs only
- **origin/develop = `60d1ce97e235528f1f3815f90881a80984e340f0`** (`ls-remote`, this action).
  Your local `develop` is STALE; `ls-remote` is the only honest ref.
- **#873 (KS-931) = `7d8a3f0e48e1d0000dcbfc7ba3d36a443c6ed045`**, open at origin on
  `refs/heads/kamilkreiser/ks-931-safeoutboundrequest-can-throw`. **Its gate has not started and it
  is Wednesday's to commission, not yours to chase.**
- **#870 (KS-921) = `2f6b30fdeb6d68c32b946c3ba3b648fe4ca2d9b7`**, under its tier-1 re-gate right now.
- Seat B is running as s140e in its own worktree on #871, the MFA finding and the KS-923 harness
  Minors. **Its paths are not yours.** Conflicts are the partition's failure, reported, not merged
  through.

## THE QUEUE — in order

### 1. KS-926's CAMPAIGN — open it by stating the family, with SIX members now
Your predecessor's §5 states five, and I am handing you a sixth, measured tonight by an independent
tester on a completely different artefact. That is the point of the campaign: it is not a bug list,
it is one question that went unasked in six places — *what would this look like if it were broken?*

| # | ticket | mechanism |
|---|---|---|
| 1 | KS-926 (P2) | the check is never **run** — 3 of 20 `check-*.sh` reachable from a live entry point |
| 2 | KS-927 (P3) | it runs with the half that would **notice** already dead — the two dead cells are the POSITIVE ones |
| 3 | KS-928 (P3) | nothing asserts the code **calls** it — delete `adminConfig.ts:1824` and every test still passes |
| 4 | KS-930 F-7 (P3) | one **branch** cannot be red — neuter it and the suite stays 26/0 |
| 5 | KS-933 (P3) | it passes over a corpus it **excludes** — `npm run build` type-checks zero test files in `packages/shared` |
| 6 | **NEW — the launcher suite (seat B's ticket, your family)** | it guards a value the product **never ships** — nothing asserts `$GIT_SYNC_STEP` reaches `$INITIAL_PROMPT`; a one-line tamper at `Launch_Claude.command` L483 left the guard suite at **18 passed, 0 failed** while the assembled boot prompt lost the pull step entirely |

Member 6 is the strongest statement of the family you have, because the guard and the thing guarded
are in the same file and the suite still could not tell them apart. **Cite it in the campaign's
opening; do not fix it — it is seat B's ticket.** And carry the tester's own escalation with it: it
rated an UNCOVERED item above its own MAJOR — the launcher registers `$$` believing `exec` REPLACES
the process, no cell asserts that, and if that line ever forked, every registry entry would be
invalid on arrival with all 18 cells still green. **That is member 6's more dangerous half: a
premise no cell states.** Ask the same question of each of your five: what premise is each one
resting on that nothing asserts?

Your predecessor's keeper is the campaign's thesis and it should open the document in its own words:
> *"a cell that cannot tell the fix from its own fallback is not a regression test"* — and the reason
> it hides is DEFENCE IN DEPTH: every layer added for safety is a layer that can absorb your tamper
> and leave your instrument unmeasured.

**Kam's 09:42 creation rule applies to whatever you file out of this:** one larger ticket per logical
path with its items as a checklist, never three or five tickets for one line of work. The campaign
itself is the logical path.

### 2. Then KS-930's remaining items by priority
Its first item is that an nginx final stage has **no route to green at all** — that is a stronger
statement than a failing test and it should be stated as such, with the measurement.

### 3. Then your table by priority then id.
KS-920's prune is NOT started and needs a start probe per service; 342 is unreproduced. Neither is
urgent. If you reach for either, say so in your wrap.

## WHAT IS NOT YOURS THIS ROUND — stated so you do not reconstruct it
- **#870.** Its verdict is pending; the ruling arrives as its own mail. Do not touch the branch.
- **#873 (KS-931).** Built and READY; its gate is Wednesday's to commission.
- **#871, #872, the MFA secret-retention defect, the two KS-923 harness Minors, and the launcher's
  five findings.** All seat B's, briefed to it separately.
- **The demo box and anything touching the demo admin identity.** See HOLDS.

## KAM'S STANDING DIRECTION (verbatim, his panel, 2026-09-06 20:19)
`keep pushing the secuura agent to polish the platform to a ready state.`
That is the sort key for your queue after the items above. It moves no boundary.

RULED BY KAM, NOT YET IN AN ARTEFACT
Five ruled cards carry no delivered mark. **All five are KAM'S OWN ACTS, not yours** — listed so you
neither chase them nor re-raise them to him:
- `secuura-ci-billing` => `wait` @ 2026-08-26T10:46 — Actions dead; org payments / spending limit,
  billing access only. (KS-660 was archived on his 19:31 ruling tonight as superseded by the manual
  CI gate — do not reopen the Actions question.)
- `secuura-agent-github-identity` => `identity` @ 2026-08-26T17:12.
- `secuura-dependabot-triage` => `close-and-rescope` @ 2026-09-01T09:18.
- `secuura-ks229-disclosure-mailbox` => `later` @ 2026-09-02T20:15.
- `secuura-ps-759-760-merge-owner` => `kam-merges` @ 2026-09-05T09:16 — Platform S, out of scope here.
**OPEN on his desk at default HOLD: `secuura-demo-kam-admin-default-password`.** His own address is a
SYSTEM_ADMIN on the public demo seeded with the repository's published default password. **Nothing
about that identity moves from this seat until he rules** — not the two runtime seeders, not the
smoke script, not the fixture, not the docs, not the demo env.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-05 23:24 — do NOT narrate an open defect as a guarantee in a PUBLISHED contract.
- 2026-09-06 19:28 / 20:0x — a STOP set for a demo- or identity-affecting act is lifted only on a
  measurement that names the MECHANISM (the code path, censused across the tree), never on a
  property of a row. Wednesday lifted one on an inference tonight and was wrong; your predecessor
  swept the tree and found the second seeder. **That refusal was correct — keep making it.**
- 2026-09-06 22:2x — an instruction to FILE a finding carries the finding's TEXT or names the mail
  and section to read. If an instruction from Wednesday gives you a count and a severity and no
  content, refuse it.

## HOLDS
- **No deploy from this seat without a fresh GO.** Kam's demo STOP was lifted 15:12 scoped to getting
  through the tickets and the backlog; deploys remain his signature class.
- Signature classes unchanged: production, money, external communication to any human, anything
  irreversible.
- **Client-facing communication goes ON THE TICKET** (Linear), never the extranet, which is input only.
- **Handovers to Peter or Stuart are TEST BLOCKS** — stream parent, the PRs, the one pass that proves
  it, the one thing the human does. Never a list of PRs.
- Assignment: new and unassigned tickets to our account; **a ticket already on Peter or Stuart stays
  theirs**, moved only on Kam's word per ticket.
- Every change goes agent -> Wednesday -> testing agent -> Wednesday before it is scored. Your round
  ends at READY FOR QA.
- Cleanup means quarantine, never deletion.
- Platform S is out of scope for this seat.
- Seat B's worktree and branches are not yours; do not merge through a conflict.

## FIRST ACTION
Confirm your plan by mail before building: the develop SHA you read yourself, and one sentence on how
the campaign document will state the family so a reader who fixes only one ticket still understands
the other five. If anything here disagrees with what you measure, the measurement wins — say so and
do not reconcile it silently.

PROVENANCE:
- origin develop = 60d1ce97e235528f1f3815f90881a80984e340f0 | `git -C 2_Project_Files ls-remote origin refs/heads/develop` from Wednesday's seat (READ verb; no fetch, no merge-tree, no worktree add in your checkout) | read 2026-09-06
- #873 head 7d8a3f0e48e1d0000dcbfc7ba3d36a443c6ed045 and #870 head 2f6b30fdeb6d68c32b946c3ba3b648fe4ca2d9b7 | `git ls-remote origin` from Wednesday's seat | read 2026-09-06
- the five family members with their ticket ids and mechanisms, and your predecessor's keeper quoted verbatim | `5_Project_History/HANDOVER-s141.md` §5, read read-only from Wednesday's seat | read 2026-09-06
- family member 6 and the exec-premise escalation | the QA agent's mail `[QA -> Wednesday] Secuura SEAT B KS-911 + KS-912 (launcher, by hash)` 2026-09-06T12:18:53Z, read whole by Wednesday in this session | read 2026-09-06
- #870's re-gate is RUNNING and unreported | Wednesday's own capture of the tester pane, spinner live at 18m | read 2026-09-06
- the five undelivered ruled cards with rulings and dates | `decision_queue.sh list ruled --undelivered secuura-` | read 2026-09-06
- Kam's 20:19 direction, his 09:42 creation rule, his 10:24 assignment correction, his 15:12 scoped stop-lift, his 19:31 KS-660 archive ruling | `tools/kam_rulings_today.sh`, all 16 messages of the day read as a sequence | read 2026-09-06
- NOT READ by me: the #873 diff and KS-930's nginx item — held for their own gates, unopened; nothing here rests on either | not read | read 2026-09-06

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 22:29
  Against Kam: all 16 panel messages of 2026-09-06 read as a SEQUENCE — his 09:45 WITHDRAWAL of the
  aggregation instruction is honoured (the aggregation line here is the 09:42 CREATION rule he kept,
  not the withdrawn one), his 10:24 assignment correction is carried, his 19:31 KS-660 archive ruling
  is named so this seat cannot reopen the Actions question, and his 17:01 NexusAI pause is not this
  project's. Against Wednesday's previous outbound to this project: the 22:03 checkpoint to s141,
  whose instruction ("finish KS-931 to READY, start nothing after it") this brief COMPLETES rather
  than changes — KS-931 is READY and is explicitly not re-commissioned here. Against the sibling brief
  sent to seat B minutes earlier: the two queues are disjoint by ticket and by branch, and each brief
  names what belongs to the other seat, so neither seat can believe an item is unowned.
  Internal: member 6 is cited in item 1 and forbidden as work in the same item — deliberate and stated
  twice, because the family statement needs it and the fix does not belong to this seat.
