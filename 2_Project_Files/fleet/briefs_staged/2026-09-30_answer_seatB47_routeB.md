# ANSWER (Seat B 47th): ROUTE B, expires 2026-10-09. SUPERSEDES item 2 of the 21:31Z ruling ("no expires"). Drop the contract edit. ctx:60% at 2026-09-30 07:39

## BLUF
**Your ctx: ctx:60%** (Wednesday read of pane %77, 2026-09-30 07:39 AEST). **ROUTE B: give the GHSA-r53p row `"expires": "2026-10-09"`, and REVERT your uncommitted one-line edit to `baseline-contract.mjs`** (restore it byte-equal to the base blob, and prove it with `cmp`). **This SUPERSEDES item 2 of Wednesday's 21:31Z ruling, which said "no expires".** That ruling was Wednesday's error; your measurement caught it. **Thank you for holding rather than committing.**

## WHY (so the next reader can check it)
- The 12 undici siblings carry no expiry **because they are GRANDFATHERED**, not because a new row may omit it (your measurement). Adding a 13th to `GRANDFATHERED_NO_EXPIRY` is a **permanent acceptance**, and the contract calls that a reviewer decision.
- Wednesday's authority (Kam 2026-09-09) covers baselining **with the SHARED re-triage date, never a fresh one**, and forbids any gate change. **A permanent acceptance is outside it.** Reading it in would be arguing an action into scope, so ROUTE A is refused.
- **2026-10-09 is the one re-triage date this file already shares.** Four rows carry it (KS 528 ×2, KS 530, KS 729), re-dated by Kam's signed mail, and it is the audit fuse Wednesday already carries to Kam. So the undici row joins that single re-triage and gets no fresh date. The real fix (the undici override ticket) is due by then.
- Expect `audit:contract` to pass with no contract edit: a row WITH `expires` is not a no-expiry row. **Re-run all three gates after the change and report each rc on its own line.** If any refuses, STOP and mail.

## THE PR (as before, with this one change)
- Three files → **two**: the js-yaml lock regen (your measured MOVED=1, 274 → 274) + the baseline row with `expires 2026-10-09`. Subject `KS-470: js-yaml 5.4.2 in systemTest/performance, accept GHSA-r53p build-tree only` (your 81/89 is fine); `Refs KS-470`.
- **Your two disclosed deviations are ACCEPTED:** the verb (`npm update js-yaml` in the script's own container and flags, guarded by the outcome test) and the mount (the parent dir, because of the `file:../../observability` link). Both go in the READY and the PR body. The cleanroom script's remediation command cannot regenerate this lock, so that is a **ticket to draft in the READY**, filed after the gate.
- **Your figure for the fuse:** the row adds one more entry lapsing at 2026-10-09. Say so in the READY; Wednesday tells Kam.

## SEQUENCING — accepted as you proposed
Ship **this PR (→ gate48a)** and **ITEM 1a** (rebased on the merged develop, `cmp` proven → gate48b). **Hand ITEM 1b and ITEM 2 over** with everything measured. Do not start ITEM 1b's build. **Hard line 75%.**

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:60% | read 2026-09-30 07:39
- GRANDFATHERED_NO_EXPIRY (17 ids, 12 of 13 undici) and the three gate rc's | your STATUS mails 21:37Z + 21:38Z, DKIM/SPF/DMARC pass | read 2026-09-30 07:39
- the four 2026-10-09 rows | your STATUS 21:29Z §3 (read at 37205947ddd2) | read 2026-09-30 07:39
- the grant's clause 3 + no-gate-change | 0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md | read 2026-09-30 07:39
