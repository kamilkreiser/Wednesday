---
date: 2026-09-16
type: grant
source: Kam, panel 2026-09-16 20:40:59 (view=wednesday)
status: live
tier: W
---

# Grant: on the new account, spin up agents to test, approve, merge and move things forward — while the local model keeps going

**The operative case, so the headline matches it:** Wednesday has held Ornith diffs (READY files) and a staged raise brief, and is deciding whether to wait for Sunday. **On this account, it does not wait.** A Secuura seat raises the held fixes as PRs in bundles; a QA gate tests each one; Wednesday approves and merges what passes under the TESTED grant, one at a time. The local model keeps working the backlog in parallel.

**His words, verbatim (20:40:59):**
> *"while that happens, keep working with the local model.  also, as I have signed you into a new account we have context.  you have the approval to spin up other local agents to test, approve, merge and move things forward"*

**Wednesday's reading, stated to him on the panel within the minute (20:4x), with a default of "starting now unless you narrow it":**
**CONFIRMED by Kam 20:41:47 (panel, verbatim): *"yes.  claude agents"* — reading 1 is his word, not an assumption.**
1. "Local agents" means **Claude agent seats on this Studio** (the fleet), not the local model. The local model cannot raise a PR, run a gate, or merge.
2. It **brings forward** the 2026-09-15 16:36 "QA on Sunday night, merge all at once" shape for the held Ornith diffs. It does not cancel it; the grant row in EXPIRING-GRANTS still names Sunday as that grant's end.
3. **Not covered, because he did not name it:** deploys (kintsugi or demo), anything demo/UAT (Peter's nod), external communication to Peter or Stuart, `.github/workflows` PRs (his `kam-merges` card), and other authors' PRs. The v1.3 signature classes are unchanged.
4. **Approval = Wednesday's GO naming the head SHA** after a QA gate verdict at that head plus a Test Evidence block (the 2026-09-11 TESTED grant, which is still open-ended).

**Constraints that still bind:**
- The usage gate (`fleet/usage_gate.sh`, 90% cut) applies to every seat and gate launch. The gauge read 6% at 20:32.
- The 2026-09-13 standing rule: as many agents as the code partition allows, and no two seats on the same files.
- Kam's 13:32 "minimal or limited Secuura work on this account … until Sunday" is **superseded by this line for this purpose**, because he said "we have context". Wednesday's reading; his word corrects it.
- Kam's 09-16 counter on local-model failures is unchanged.

**Expiry:** none stated. It is tied to "this account" having context. When the usage gate trips, or he switches accounts, re-read before relying on it.

**Family:** [[2026-09-11_secuura-we-approve-and-merge-our-own-tested-work]] · [[2026-09-13_as-many-agents-as-possible-partitioned-by-code]] · [[2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once]] · [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5).

## SECOND INSTANCE 2026-09-20 21:5x — same shape, his words after `/login`: *"keep going and once you fix the launch screen, keep going with secuura tickets using both claude and local agents"*
The 90% cut had tripped at 21:15 on the previous account (statusline `7d:91%`); he signed the seat into a new account and the statusline read `7d:0% renews 6d 14h`. Wednesday's reading, said back on the panel at 21:5x and not corrected: fresh allowance; Claude seats to raise, gate and merge while Ornith works the backlog; merges one at a time on Wednesday's signed GO under the open-ended TESTED grant; kintsugi only, never demo; the signature classes pause (KS-1250 his); the away-week's 23:00 merge cut-off does not apply now he is here. **What it adds to the 09-16 clauses:** "fix the launch screen" was an instruction to make the cockpit fix TONIGHT (it answered a question Wednesday had put to him with a Monday default — his word moved it); and drafter subagents, forbidden at the 90% cut, are allowed again on the new account. Expiry: none stated — tied to this account having context, as on 09-16. Kept in this file rather than a new one: Kam ruled `b` on the boot digest at 16:44 (shrink the corpus).
