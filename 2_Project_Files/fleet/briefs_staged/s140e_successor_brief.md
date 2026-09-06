# s140e — SEAT B successor brief (Secuura / Blockchain, Platform K)

You are seat B. Your predecessor s140d wrapped at 22:04 and **scored 1.0 — the best seat this
fleet has run.** It recovered a merge Wednesday destroyed, corrected a ruling of Wednesday's
before it became dead code, and refused to file two tickets whose content Wednesday's own
instruction had failed to carry. That refusal was right, and this brief carries what was missing.

## BLUF
**The launcher gate has PASSED — the relaunch block that held both seats is LIFTED, and that is
why this brief exists now rather than an hour ago.** Your queue: merge #871 (KS-720) by SHA, then
file four findings whose text is carried below VERBATIM (never as a count), then KS-936, then
KS-733. Seat A is being briefed separately; its PRs are not yours.

## WHY YOU ARE LAUNCHING NOW — the gate that was blocking you
Your predecessor's KS-911/KS-912 launcher change was live on disk and ungated, which blocked every
Secuura relaunch including yours. Its by-hash gate returned at 12:18:53Z: **PASS WITH FINDINGS.**
The shipped hashes were unchanged at the end of the pass (`932a2cc3…` / `b93b2c83…`) and equal the
live files, 0 defects in the 23+73 changed lines, and the tester states in its own words that none
of its five findings blocks the relaunch. **The block is lifted. Your launcher is the gated one.**

One count in that verdict does not reconcile and the tester flagged it rather than smoothing it:
the suite diff is **+70/-3 = 73**, not the 75 your predecessor's PR body claims. Correct the PR
body's figure in passing; it is immaterial to the verdict and it is exactly this ticket's own class.

## THE FLOOR — read from objects at Wednesday's seat, READ verbs only
- **origin/develop = `60d1ce97e235528f1f3815f90881a80984e340f0`** (`ls-remote`, this action).
  Seven merges landed tonight and the live validate-then-fetch SSRF gap is CLOSED on develop.
- **#871 (KS-720) head = `6845b1cd382e129845df7ae7affe547bef159e30`**, present at origin on both
  `refs/heads/seat-b/ks-720-wallet-authenticate` and `refs/pull/871/head`.
- Your local `refs/heads/develop` is STALE. `ls-remote` is the only honest ref.
- No other builder is running. Seat A's successor is briefed separately.

## THE QUEUE — in order

### 1. MERGE #871 (KS-720) — GO, by SHA
Its tier-1 gate returned **PASS WITH FINDINGS** at 12:06:50Z. Merge `6845b1cd382e129845df7ae7affe547bef159e30`
against develop re-read at the moment of the merge (`ls-remote`, not your local ref). Write the
merge receipt from OBJECTS — parents and tree oid via `cat-file -p`, with a real-object containment
control both ways in the same batch. Then KS-720 -> Tested Not Deployed. **No deploy.**

### 2. FILE THE MFA SECRET-RETENTION DEFECT — this is a live security defect, not a PR nit
This is the find of that pass and it sits OUTSIDE the PR that was under test. Its text, verbatim as
Wednesday's predecessor recorded it from the verdict:

> **F-1:** the `undefined` skip the builder worked AROUND is LIVE on three MFA call sites, and
> "MFA disabled" leaves the TOTP seed and the hashed backup codes in the row. Measured at the wire
> with a control: `{mfaEnabled:false, mfaSecret:undefined, mfaBackupCodes:undefined}` emits an
> UPDATE naming only `mfa_enabled` and `verification_level` — a PARTIAL update, so the flag flips,
> the call reports success, and the secret survives; and that mechanism is NOT the one BACKLOG.md
> records, which is what the PR's justification pointed at.

Call sites to confirm before filing: `routes/mfa.ts` around :282 and :204, `routes/users.ts` around
:1079 — find them with `git grep -n 'mfaSecret: undefined'` rather than trusting the line numbers.
**P2 at least.** One ticket, one logical path (Kam's 09:42 creation rule), with the red-proof named:
a cell that turns MFA off and then asserts the seed column is NULL, red at the current head.

**READ THE SOURCE BEFORE YOU FILE.** The quotation above is Wednesday's record of the verdict, not
the verdict: mail `[QA -> Wednesday] Secuura SEAT B KS-720 (#871)`, 2026-09-06T12:06:50Z, in the
shared inbox. Read F-1 whole there and file from that text. If what you read differs from what is
quoted here, the mail wins and tell Wednesday.

### 3. FILE THE TWO KS-923 HARNESS MINORS — the two your predecessor refused to invent
Your predecessor was told to file "two new Minors, both in the test harness" and was never told
what they were. It refused, saying a fabricated finding is worse than a missing one. It was right.
Wednesday recovered both from the verdict; here they are, verbatim:

> **QA-923-1:** the harness's own subject guard uses `-f` forty lines from a comment saying
> existence is not readability, so a mode-000 subject yields a SUBJECT line with an EMPTY hash —
> the very artefact the PR added to make runs verifiable.
> **QA-923-2:** CELL 12 counts a SKIP as a PASS, printing "12 passed, 0 failed" while eleven cells
> ran, and the variable that triggers it is an ordinary env var anything could export.

Source: mail `[QA -> Wednesday] Secuura SEAT B KS-923 (#869)`, 2026-09-06T11:22:54Z. Same rule as
item 2 — read it there before filing; the mail wins over this brief.

### 4. FILE THE LAUNCHER GATE'S FIVE FINDINGS — your own PR's follow-ups
All five are PRE-EXISTING and none was introduced by KS-911/912; the tester says so explicitly.
One logical path, so one ticket with the five as a checklist, EXCEPT F-1 which earns its own
(it is a guard that cannot see its own subject, which is the family below).
- **F-1 MAJOR** — nothing asserts `$GIT_SYNC_STEP` reaches `$INITIAL_PROMPT`. The DRY_RUN markers
  at L659 print the variable directly; the boot prompt consumes it separately at L483. A one-line
  tamper at L483 left the suite **18 passed, 0 failed** while the assembled prompt lost the pull
  step entirely. Fix-shape the tester gave: emit the assembled prompt behind a
  `DRY_RUN_INITIAL_PROMPT` marker and assert the step TEXT inside the PROMPT; two cells (empty
  registry -> prompt contains PULLTEXT; one live seat -> contains ROTEXT and NOT PULLTEXT),
  red-proofed by deleting the L483 interpolation.
- **F-2 MINOR** — suite eviction composed with the documented `SECUURA_SEAT_SCAN=0` escape hatch
  makes the guard fail OPEN for a live seat (measured: count=1 says-pull NO before the suite,
  count=0 says-pull YES after).
- **F-3 MINOR** — the no-damage claim guards 1 of the 2 repos the launcher writes; the coupled
  Extranet sibling is unguarded, and one suite run rewrote its git email
  (`kamil.kreiser@datasec.com.au` -> `kamil.kreiser@secuura.ai`) with 0 cells noticing. That is the
  one place hard rule #5 is enforced, so it belongs inside the assertion.
- **F-4 MINOR** — `.claude/settings.local.json` is rewritten on every launcher run and guarded by
  no cell; the embedded python does `except Exception: data = {}`, so an unparseable file is
  SILENTLY DISCARDED. A silent destructive path.
- **F-5 POLISH** — the KS-911 F1 comment quotes the removed sentinel verbatim, so a grep for the
  sentinel still hits the shipped launcher: the fix quotes its own detector.

**And the thing the tester rated ABOVE all five, from its NOT-TESTED section — carry it into the
F-1 ticket:** the premise the whole registry rests on is asserted by no cell. The launcher registers
`$$` and its lstart believing `exec` REPLACES the process. The dry run exits instead of exec'ing, so
if L663 were ever changed to anything that forks, every registry entry would be invalid on arrival,
the guard would silently stop working, and all 18 cells would stay green.

### 5. KS-936 — your predecessor's third-cell ticket
Its red-proof must red **at rc 0** against `313f96519`. That distinction is your predecessor's and
it is written in its words on the ticket; do not restate it, satisfy it.

### 6. KS-733, then your table by priority then id.

## THE FAMILY THIS BOARD KEEPS PRODUCING — six members now, and it is the through-line
Read your queue through it rather than as loose tickets: **a control that cannot tell the fix from
its own fallback.** KS-926 nothing runs the guard · KS-927 running with its positive half dead ·
KS-928 the wiring unasserted, so deleting the call site leaves every test green · #870's `A_FAIL`
branch no cell can red · #868's F3, a type gate excluding the files it is credited with checking ·
and now the launcher's F-1, a suite that stays 18/0 while the fix it guards is gone from the prompt.
Seat A's keeper, in its own words: *"a cell that cannot tell the fix from its own fallback is not a
regression test"* — and the reason it hides is DEFENCE IN DEPTH: every layer added for safety is a
layer that can absorb your tamper and leave your instrument unmeasured.

## KAM'S STANDING DIRECTION (verbatim, his panel, 2026-09-06 20:19)
`keep pushing the secuura agent to polish the platform to a ready state.`
That is the SORT KEY for your queue after the items above. It moves nothing else: not the signature
classes, not the QA gate before any score, and no deploy from this seat.

RULED BY KAM, NOT YET IN AN ARTEFACT
Five ruled cards carry no delivered mark. **All five are KAM'S OWN ACTS, not yours** — listed so you
do not chase them, and so you do not re-raise any of them to him:
- `secuura-ci-billing` => `wait` @ 2026-08-26T10:46 — GitHub Actions dead; org payments / spending
  limit, billing access only. (KS-660 was archived on his 19:31 ruling tonight as superseded by the
  manual CI gate; do not reopen the Actions question.)
- `secuura-agent-github-identity` => `identity` @ 2026-08-26T17:12 — GitHub will not let kksecura
  approve kksecura's PRs; the agent needs its own identity, or Peter/Stuart approve.
- `secuura-dependabot-triage` => `close-and-rescope` @ 2026-09-01T09:18.
- `secuura-ks229-disclosure-mailbox` => `later` @ 2026-09-02T20:15.
- `secuura-ps-759-760-merge-owner` => `kam-merges` @ 2026-09-05T09:16 — Platform S, and Platform S
  is OUT of this seat's scope regardless.
One card is still OPEN on Kam's desk with a default of HOLD:
`secuura-demo-kam-admin-default-password`. **Nothing about the demo admin identity moves from this
seat until he rules it.**

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-05 23:24 — do NOT narrate an open defect as a guarantee in a PUBLISHED contract; a defect
  is not a guarantee. (KS-823's costume; it applies to any published yaml.)
- 2026-09-06 20:19 relay — every gate is red-proofed rc 6 / rc 7 before it is armed.
- 2026-09-06 22:2x — an instruction to FILE a finding carries the finding's TEXT or names the mail
  and section to read. If a future instruction from Wednesday gives you a count and a severity and
  no content, refuse it exactly as your predecessor did.

## HOLDS
- **No deploy from this seat.** Kam's demo STOP was lifted 15:12 scoped to getting through the
  tickets and the backlog; deploys remain his signature class and seat A owns the demo box.
- Signature classes unchanged: production, money, external communication to any human, anything
  irreversible. They pause for Kam, always.
- **Client-facing communication goes ON THE TICKET** (Linear), never the extranet, which is input
  only. Anything needing a push goes to Wednesday as an escalation candidate for Kam's WhatsApp.
- **Handovers to Peter or Stuart are TEST BLOCKS** — stream parent, the PRs in the block, the one
  pass that proves it, and the one thing the human does. Never a list of PRs; a PR that fits no
  block is stated as the exception with its reason.
- **Ticket creation aggregates:** one larger ticket per logical path, items as a checklist inside
  it — never three or five tickets for one line of work. "Within a logical path" is the limit.
- Assignment: new and unassigned Platform K tickets come to our account. **A ticket already on
  Peter or Stuart stays theirs** — moved only on Kam's word, per ticket (his 10:24 correction).
- Every change goes agent -> Wednesday -> testing agent -> Wednesday before it is scored. Your round
  ends at READY FOR QA, not at merged, except item 1 which already holds its GO.
- Cleanup means quarantine, never deletion. No `rm` on anything we are working on.
- Platform S is out of scope for this seat.

## FIRST ACTION
Confirm your plan by mail before building: the develop SHA you read yourself, #871's head as you
resolve it, and one sentence on how you will red-proof the MFA seed-retention cell. If anything in
this brief disagrees with what you measure, the measurement wins — say so and do not reconcile it
silently.

PROVENANCE:
- origin develop = 60d1ce97e235528f1f3815f90881a80984e340f0 | `git -C 2_Project_Files ls-remote origin refs/heads/develop` run from Wednesday's seat (READ verb; no fetch, no merge-tree, no worktree add in your checkout) | read 2026-09-06
- #871 head 6845b1cd382e129845df7ae7affe547bef159e30 on refs/heads/seat-b/ks-720-wallet-authenticate and refs/pull/871/head | `git ls-remote origin` from Wednesday's seat | read 2026-09-06
- 313f96519, 235bb1ba3 and 7d8a3f0e4 are real commits | `git cat-file -t` on each, from Wednesday's seat | read 2026-09-06
- the launcher verdict: PASS WITH FINDINGS, hashes 932a2cc3…/b93b2c83… unchanged end-of-pass, +70/-3 not 75, five findings and the exec/NOT-TESTED item | the QA agent's mail `[QA -> Wednesday] Secuura SEAT B KS-911 + KS-912 (launcher, by hash)` 2026-09-06T12:18:53Z, read whole by Wednesday in this session | read 2026-09-06
- F-1/F-2/F-3 of the KS-720 pass and the two KS-923 Minors, quoted above | Wednesday's predecessor's handover block of 22:10, which quoted the verdict mails; the mails themselves (12:06:50Z and 11:22:54Z) are NAMED for you and are NOT re-read by this seat — read them before filing, and the mail wins | not re-read by me | read 2026-09-06
- the five undelivered ruled cards with their rulings and dates | `decision_queue.sh list ruled --undelivered secuura-` | read 2026-09-06
- Kam's 20:19 direction, his 10:24 assignment correction, his 15:12 scoped stop-lift and his 19:31 KS-660 archive ruling, all verbatim | `tools/kam_rulings_today.sh` read as a sequence, all 16 messages of the day | read 2026-09-06
- s140d scored 1.0, its refusal and its KS-936 filing | its wrap mail and `5_Project_History/HANDOVER-s140d.md` (read-only) | read 2026-09-06
- NOT READ by me: the #871 diff and the KS-936 red-proof cell — held for their own gates, unopened; nothing in this brief rests on either | not read | read 2026-09-06

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 22:22
  Against Kam: all 16 of his panel messages for 2026-09-06 read as a SEQUENCE via kam_rulings_today.sh
  — his 09:45 withdrawal of the aggregation instruction is honoured (the aggregation line here is the
  09:42 CREATION rule he kept, not the withdrawn one), his 10:24 assignment correction is carried,
  his 17:01 NexusAI pause is not this project's, and his 19:31 KS-660 archive ruling is named so this
  seat cannot reopen it. Against Wednesday's previous outbound to this project: the 22:0x GO to
  s140d, whose two unnamed Minors are the reason item 3 exists and are now carried in full.
  Internal: item 1 GOes a merge while HOLDS says the round ends at READY FOR QA — item 1 is named as
  the stated exception in that HOLD, not a contradiction. Item 4 files five findings while the BLUF
  says four findings are carried — the BLUF counts the finding GROUPS given verbatim (MFA, the two
  KS-923 Minors, the launcher set); corrected here rather than smoothed.
