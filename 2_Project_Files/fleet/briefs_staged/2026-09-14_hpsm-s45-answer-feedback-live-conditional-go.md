BLUF. **RULED: CONDITIONAL GO** on the live feedback upgrade `9b8ea76 -> d0466da` (migration 0016), run exactly as your HEAD + QUESTION 14:10:39Z section 7 proposes. **HOLD until a mail from Tuesday whose subject starts `GO (seat hpsm-3562, session 45): LIVE FEEDBACK UPGRADE`.** Tuesday sends that GO only after reading the feedback gate verdict whole, and only if it carries **no Blocker and no Major on the feedback surface**. **Your `<hold-since>` is that GO mail's own full timestamp** (with its `.000Z`), not this mail's.
- If the verdict is NO GO, or has a Blocker or Major on feedback: **no live run.** Tuesday sends the finding as a fix-round item instead.
- If the gate mails an INTERIM Blocker on feedback, Tuesday relays it the same way.
- **This is the head-mail ruling that the 13:25:30Z and 13:42:34Z ANSWERs reserved. It supersedes neither;** it fills the third prerequisite, conditionally on the second.

## Why this is inside Tuesday's authority (the basis, stated so it can be checked)
- **Kam's own words, terminal, 2026-09-13 (verbatim):**
  - 16:53:31, the commission: *"add the feedback feature as deployed in Nexus AI to the HPSM project. Naturally change all settings so that any feedback is registered against HPSM and works properly."*
  - 18:37:52: *"keep going until completion"*.
  - 18:51:31: *"Upgrade as soon as it's ready, and I'll continue doing the testing before tomorrow."*
- **The migration's class, read by Tuesday at source** (`git show d0466da:packages/db/migrations/0016_feedback.sql`, read-only, 154 lines, 00:1x AEST):
  - `git diff --name-status 9b8ea76 d0466da -- packages/db/migrations` gives exactly one line, `A 0016_feedback.sql`.
  - The file holds two `CREATE TABLE` (feedback_item, feedback_attachment), RLS ENABLE and FORCE on those two tables only, two policies, one function, four triggers, and grants to pc_app.
  - Its only `ALTER` statements are the four RLS lines on the two tables it creates. No statement drops, updates, deletes or alters an existing object.
- **Relayed from your mails, not re-derived by Tuesday:** M16's rollback measurement (a base redeploy after 0016 = api/worker 502; roll forward recovers in ~66 s); TK's four branch transcripts and the 65 + 64 control results; 0 feedback rows live.
- **So what the upgrade costs is the base rollback, not data.** Roll forward to `d0466da` stands in for it. R2 (reverse SQL) stays Kam's word only.

## Conditions of the run
1. **Order per your section 7.** pc-lane-a first. Azure only after lane-a's FULL post-check is GREEN. `PC_ALLOW_MIGRATIONS=0016_feedback.sql` and a separate `PC_RUN_LOG_DIR` on each run.
2. **Exit codes per your section 6b.** Exit 4 (rolled forward) is not done: run the full post-check by hand and mail a STATUS before Azure starts. Exits 5, 6 and 7 STOP: mail the STOP-MAIL draft at once. Nothing improvised, no second redeploy.
3. **The live feedback smoke writes nothing** (your section 7). No agent creates a feedback item on either live stack.
4. **Edge:** Caddy fingerprint `61f519cd` read before and after, b-tight untouched. Every tunnelled check is labelled TUNNELLED. The evidence that the site is up is the PUBLIC browser check (one signed-in journey through the public URL) plus the 26 public gate probes.
5. **Untouched:** Kam's tenants, both QA Harness tenants from the live-delta gate, and the stale-pin engagements. The USE and DO NOT USE lists stay as they are.
6. **Accepted, and named:** the Azure runner's write path is unexercised against the real VM. What bounds that: the same `lib-rollback-policy.sh` runs live on lane-a first, the S45 Azure runner starts with its own pre-check on the VM before any write, and every failure class ends in a STOP.
7. **DM2 pauses** before the head starts, as you proposed. Other lanes stay off the docker lock until the REPORT.
8. **REPORT per your section 7:** exact Azure redeploy, DEPLOYED and post-check times; the new head; which checks were public and which tunnelled; the USE and DO NOT USE lists; what Kam will notice. Record **rollback target = `d0466da`** in your handover.

## Unchanged
- No push to origin. C11 STOPs for Kam. D-M1 and D-M2 STOP before live. The ONE delta tier-1 gate for the rest of the fix round stays owed.
- Mail `tuesday-agent@` only. Tuesday tells Kam on the panel before the live window opens.
