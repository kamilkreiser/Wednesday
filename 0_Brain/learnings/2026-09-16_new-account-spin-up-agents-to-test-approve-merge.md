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
