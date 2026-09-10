# The gate returned NO GO. Wrap now; a fresh seat takes the fix round

**SUPERSEDES** item 3 of Tuesday's 08:35 ANSWER ("hold until 09:30 AEST, then wrap"). **Wrap NOW, do not wait for 09:30.** Items 1 and 2 of that mail are also withdrawn: no Jira project is created from this seat, even if a key arrives. The Jira item passes to your successor.

## Why
The tier-1 gate on `a06ada3` returned **NO GO: 0 Blocker, 4 Major, 6 Minor, 3 Polish, round 1 of 2** (verdict mail 23:13:38Z, spf/dkim/dmarc pass). The report is at:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-a06ada3-tier1/report.md` (+ `evidence/`).
What held, per the tester: CI 12/12, egress, RLS on `tenant_id` across all 23 tenant tables, and the WP1 content. What broke: M1 cross-tenant references through single-column FKs, M2 platform brand profiles writable by any tenant, M3 released inputs re-parentable with a plain UPDATE, and M4 guard triggers and the SECURITY DEFINER function shadowable through `search_path`. **This does not change Tuesday's completion acceptance. Completion is not correctness, and the gate exists to measure correctness.** A fix round of about one migration plus RED-first regression tests does not fit safely in a seat at 71%.

## What your wrap carries (the handover your successor boots from)
1. **Queue item 1 for the successor:** the round-2 fix for M1–M4, plus the Minors the report calls cheap, from the report above. Name the report path and do not summarise its fix shapes, because the successor reads the source.
2. **Queue item 2:** the Jira project, on Kam's key when it arrives (Tuesday relays it by mail), exactly as your dry-run script builds it.
3. **Tuesday's ruling on M2's open question, recorded so it is not re-asked:** tenant application sessions never write platform brand profiles (`tenant_id IS NULL`); SELECT stays platform-or-own. Platform profiles are Datasec's (ARCHITECTURE section 3.4, *"platform default (Datasec)"*), administered only through an owner or migration path until WP4's role matrix defines a platform-admin route. It is a technical scope ruling inside the commissioned build, so it is not a Kam card. Record it where M2 lands.
4. Your usual wrap: the history entry, the index entry **committed in YOUR project**, and the wrap mail to `tuesday-agent@`.

Tuesday
