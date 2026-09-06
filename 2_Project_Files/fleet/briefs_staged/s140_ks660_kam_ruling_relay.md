## BLUF
**Kam ruled KS-660 at 19:31 on his panel, verbatim: `Decision secuura-ks660-actions-ci-disposition: a — Archive KS-660 as superseded by the manual CI gate (recommended)`.** Execute it as ONE ticket act, inserted at the front of your queue (~5 min; before the KS-913 cut, after whatever step of the #851 measurement you are mid-way through — do not interrupt a build):

1. ONE BLUF comment on KS-660: *Disposition (Kam, 2026-09-06 19:31 AEST): ARCHIVED as superseded by the manual CI gate — GitHub Actions is not being restored (`docs/DEV-PROCESS.md` v3, 27 Aug 2026, § the manual CI-gate equivalents; the 12-leg pre-push preflight gates every push today); the ticket's symptom has been unobservable for 20 days (measurement: comment `d6bfb976`); restoring Actions would be an org billing/spending-limit change and is not planned. Unarchive if that decision changes.* Quote his sentence verbatim in the comment.
2. Archive KS-660 (state untouched — archive only, the 2026-09-05 rule).
3. Receipt by mail: the comment id + "archived" as read back from the board (a read after the write, not the write's return).

Nothing else changes: the #851 measurement and the KS-913 pre-check/cut order from the 19:26 and 19:28 mails stand; this act slots in front of KS-913. No restore, no spend, nothing on the VM.

PROVENANCE:
- Kam's ruling | `tools/kam_rulings_today.sh` (message 16 of 16, 19:31; verbatim above) and `decision_queue.sh rule secuura-ks660-actions-ci-disposition a` recorded 19:3x | read 2026-09-06 19:3x
- The card's BLUF (his measurement = your `d6bfb976` comment; DEV-PROCESS v3; the billing fact) | `decision_queue.sh show secuura-ks660-actions-ci-disposition` | 19:3x
- Your KS-660 measurement | your 09:17:35Z STATE (saved `fleet/state/mail_091700_s140_state_rulings_done_010001a0.txt`) | read 2026-09-06 19:2x
- The previous mails to you (19:28 the KS-487 table ANSWER; 19:26 the #851 ADDENDUM — "KS-660: nothing further from you, as ruled" stood until Kam's word) | `briefs_staged/s140_ks487_table_answer.md`, `s140_851_runner_relink_hunt.md` | read 2026-09-06 19:3x — this relay SUPERSEDES "nothing further on KS-660" (the 19:20 ANSWER, item 3) by name; nothing else re-sequenced
- scope: one comment + archive + a read-back receipt; inserted before KS-913 | this relay, written by Wednesday | 19:32

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 19:32
(checked: the ruling quoted verbatim once; the act is the card's option a exactly; the insertion point does not interrupt the #851 build; archive-only per the 09-05 rule; the SUPERSEDES names the one clause; no NexusAI content.)
