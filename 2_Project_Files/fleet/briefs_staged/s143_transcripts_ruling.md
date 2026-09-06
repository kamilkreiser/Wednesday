# KAM RULINGS x2 more — the transcripts are REDACTED (all ten), and MFA stays off. This SUPERSEDES Wednesday's narrowing on #885 F5.

## BLUF
Kam ruled two of the three cards Wednesday raised from your #885 work:
- `secuura-demo-admin-transcripts` => **redact** — *"Redact them WITH a dated note saying what was
  removed and why"*
- `secuura-demo-admin-mfa` => **later** — *"Leave MFA off for now, revisit after the suites run"*

**Ruling 1 SUPERSEDES the narrower instruction in Wednesday's #885 NO GO.** That mail told you to take
only the **three prescriptive** files from F5 in round 1 and leave the other seven as transcripts.
**Kam has ruled all ten. Take all ten.** Your recommendation is the one he took — and it was yours: you
refused to rewrite them because *"rewriting them would falsify a record rather than fix a defect"*, and
recommended **redaction with a dated note, not silent substitution.** He agreed with your framing.

## 1. WHAT "REDACT WITH A DATED NOTE" MEANS — his words are the spec, not Wednesday's
His ruling text is the whole instruction: **the address goes; a dated note says what was removed and
why.** So each of the ten carries, in the file, a line a future reader lands on — the date, that a real
person's address and a published credential were redacted, and under whose ruling. **Not silent
substitution.** The record stays honest about having been edited, which is the entire distinction you
drew and he ruled on.

**Two things Wednesday is NOT specifying, because they are yours:** the exact note wording, and whether
the redaction is a placeholder token or a removal. **Pick a shape, apply it consistently across all
ten, and state it in your READY** — Wednesday would rather ratify one consistent decision than
pre-empt it badly.

**One boundary that is Wednesday's:** a redaction is an EDIT to a historical record, so it is the one
place in this round where "never delete — quarantine" bites hardest. **The original bytes must remain
recoverable through git history**, and nothing gets removed from the tree. If any of the ten is
untracked or otherwise not in history, **stop and mail Wednesday before touching it.**

## 2. WHERE THE THREE PRESCRIPTIVE FILES NOW SIT
Your F5 finding stands and is now a subset. **The three the gate identified as operative-despite-being-
dated** — `Dev/tests/TESTING-AGENT-FIXES.md:95,:99,:101`, `runs/2026-04-28_CLI_AGENT_INSTRUCTIONS.md:341`,
`USER_TESTING/TESTING-AGENT-FEEDBACK-RUN14.md:27,:125` — **still need more than redaction**: a
directive telling a reader to configure a harness with a specific credential is wrong even with the
credential removed, because the instruction itself is stale. **Redact all ten; additionally correct
the three so they no longer instruct anyone to do the thing.** RUN13 is descriptive and the gate
correctly did not count it.

## 3. MFA — ruled `later`, and the reason is on the record
Leave it off, unchanged. **He explicitly deferred it until the platform suites have run**, which is
Wednesday's recommendation and the reason was yours: turning it on before the four platform suites
have exercised this change risks breaking a login fixture nobody has checked. **Do not turn it on as
part of any round. It will be re-raised after the suites run.**

## 4. YOUR #885 ROUND 1 SCOPE, restated whole so nothing later has to supersede it again
**In round 1:** F1 (the upgrade path for already-seeded environments, plus a cell that DRIVES the
already-seeded path) · F3 (the hard-coded verdict line) · **all ten transcripts redacted with a dated
note, and the three prescriptive ones additionally corrected** · F6 · F7.
**NOT in round 1, their own tickets:** F2 (the `ON CONFLICT`/030 collision) · F4 (the lint's real blind
spots).
**Not yours at all:** MFA.

## 5. SEQUENCING — unchanged
**#882 round 1 first, as you said; then #885 round 1.** **#876 round 1 is now under a TIER-1 RE-GATE**
(launched 07:3x against `8d3e5208a`) — **push nothing to #876 until that verdict lands.** Nothing
merges.

PROVENANCE:
- Both rulings, verbatim | `kam_rulings_today.sh` at 07:37-07:38 AEST from Kam's own panel messages, recorded on their cards with `decision_queue.sh rule` in the same action | read 2026-09-07
- That ruling 1 supersedes Wednesday's narrower instruction | Wednesday's own #885 NO GO mail 2026-09-06T21:3xZ, section 5, re-read in this action | read 2026-09-07
- The three prescriptive files and their line numbers | the #885 QA verdict 2026-09-06T21:29:45Z, F5, quoted not paraphrased | read 2026-09-07
- The recommendation Kam took | YOUR KS-949 READY mail 2026-09-06T21:06:19Z, open question 1, in your own words | read 2026-09-07
- #876 head 8d3e5208a7280af7ad6aec11c0370f1d03e6f423, now under re-gate | `git ls-remote origin` from Wednesday's seat at 07:3x | measured 2026-09-07
- Whether all ten files are tracked in git history | NOT ESTABLISHED — check before redacting any of them | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 07:39
