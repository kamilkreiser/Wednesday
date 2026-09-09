---
date: 2026-09-09
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general work are Wednesday's, on the Studio.
source: written at Tuesday s2's 70% checkpoint, 2026-09-09 ~11:40 AEST
status: live
supersede: replace this file WHOLESALE at the next pickup; never append. It replaced the s1 pickup.
---

# NEXT PICKUP — Tuesday, after s2. FOUR AGENTS ARE RUNNING. Do not launch a fifth without reading this.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything.** 🔴 **AND WHEN ITS
FRESHNESS LINE REPORTS A LAG, `curl -s http://127.0.0.1:47787/api/chatlog` BEFORE ANSWERING KAM** —
the local dashboard server sees his typing before any synced file does. That is how his 11:29 question
was found; the file was four minutes behind. Mail timestamps are UTC ≈ AEST−10.
**Rotation band 80–90%; 70% is a checkpoint only.**

## 🟢 WHAT IS RUNNING RIGHT NOW — four seats on the Security Review, partitioned by component

Kam, panel 2026-09-09: *"yes, run multiple agents on the security review."*

| Pane | Seat | Partition | Rows |
|---|---|---|---|
| `%3` | `Datasec/SecRev-A` | HPAuthenticationManager · infra_hpam | 19 |
| `%4` | `Datasec/SecRev-B` | License-Services · LicenseServer | 25 |
| `%5` | `Datasec/SecRev-C` | HPK_Deployment_Utility · UniversalPrint · MailFlow · CypherSharePoint · QuickAccessLibrary | 28 |
| `%6` | `Datasec/SecRev-D` | Task-Dispatcher · hpam-marketplace · datasec-administration-portal · WorkPathApplications · cc-api · hpam-api · SPDF-D1 | 25 |

**Shared method:** `2_Project_Files/fleet/briefs_staged/2026-09-09_secreview-round2-parallel-method.md`.
**Launcher:** `2_Project_Files/fleet/launch_secreview_round2_seat.sh <b|c|d>` (one script, parameterised;
seat A predates it and runs `launch_secreview_round2.sh` plus an in-flight amendment).

🔴 **THE RULE THAT KEEPS THIS SAFE: NO SEAT EDITS THE REGISTER.** Four seats, one
`13_Consolidated_Findings_Register_2026-09.md`. Each writes
`_Working/verification-2026-09/round2-<a|b|c|d>.md`. **Seat A consolidates all four in ONE action at
the end, on Tuesday's word — do not let it start early, a partial consolidation is the worst outcome.**
The clause is a launch guard (rc 12), not a request. **`_Working/PROGRESS.md` is shared too — leave it.**

**The method, and it is the agent's own recommendation adopted:** re-derive each CVSS vector FROM
SOURCE, then compute. **Never adopt round 1's computed column.** `H-D1` is why — its recorded vector
implied Critical 9.6 and re-deriving one metric from source gave High 8.6, moving the row DOWN.

## 🔴 WHAT IS ACTUALLY ON KAM'S DESK (this seat's items only)

1. **`secreview-estate-wide-scoring-pass-including-june`** — rec `extend`, default HOLD. **48 of 86
   scored rows disagree with their own vector**; three of the band-crossers are in the **June baseline
   he signed off**. Round 2 proceeds either way; only the June half waits.
2. **`wed-wakewatch-hardcodes-wednesday-inbox-and-pane`** — rec `parameterise`, default HOLD. Now
   carries TWO items: the watcher, and **`send_brief.sh:24`, which hardcodes the SENDING inbox** so
   every mail through it leaves from Wednesday's mailbox. **That second one is a cross-client identity
   path — Kam's very-important #1.**
3. **The tenant question (`fc05dcdd` vs `0c57ab37`)** — his alone, on the older card
   `secrev-live-pass-blocked-on-tenant`. Blocks every live-environment item and is costing published
   severities. Not blocking round 2.

## ⚠️ TRAPS — s1's still hold; these are s2's additions

1. 🔴 **`send_brief.sh` SENDS FROM `wednesday-agent@` ON EVERY SEAT** (line 24, hardcoded; line 486
   hardcodes the subject prefix too). **Do NOT use it for anything Datasec.** Mail Wednesday by direct
   POST to `/v0/inboxes/tuesday-agent@agentmail.to/messages/send`, and **verify at her end by the
   `from` field and a non-null `preview`, never by the 200.**
2. 🔴 **`wake_watch.sh` polls WEDNESDAY's inbox** (`:54`) and names her pane (`:46`). So a mail wake
   here usually means *her* mail. **Check your OWN inbox and the shared bus; if it is in neither, it is
   hers and you do not read it.** Fired five times at this seat in one session.
3. 🔴 **`pane_current_command` IS NOT A LIVENESS SIGNAL.** It reads `zsh` whether the agent is working
   or gone. **Use the pane's last SUBSTANTIVE line plus `pane_prompt_check.sh`** — ghost text at a
   prompt means the agent is AT a prompt.
4. **`board_count.sh jira` PREPENDS `https://` itself** — pass the BARE site. (The pickup's older trap
   about prefixing `https://` applies to hand-written calls, not to this tool. Both are true.)
5. **The prior-ruling gate false-fires on generic nouns and across clients** — it refused a Datasec card
   by matching two *Secuura* messages. Read them, and if the subject is genuinely untouched, override
   with the measurement in the BLUF.
6. **`cockpit.sh say` refuses a tap over 200 chars.** A tap is a pointer; content goes in a file beside
   the brief and the tap names it.
7. **The digests conflict on every rebase** — they are GENERATED. Resolve by **regenerating from the
   lesson files**, never by merging either side.
8. 🔴 **`rebase --continue` skips the pre-commit hook** (Wednesday's finding). After ANY rebase, scan
   for markers and parse the shared JSON stores **out of HEAD, before the push.**

## STANDING

**Scope (Kam, verbatim):** *"you will work on ONLY datasec projects unless otherwise instructed."*
Datasec lives at `/Volumes/KK_T9_External_HDD/!CODING/Datasec/`. **Cross-seat mail is COORDINATION
ONLY.** Kam's week grants run through **Sunday 2026-09-13**; **DATASEC PRODUCTION IS UNGRANTED.**
**FOUND / TESTED / HOW** on every analysis. **Names, not pronouns. Never delete — quarantine.**
🔴 **DO NOT run the wrap's vault step** (`end-of-session.md:50` is `git add -A` and the vault's
untracked set holds Secuura paths). Skip it and say so.

## WHAT s2 WOULD SAY IF IT COULD SAY ONE THING

**Every real finding today came from checking the thing rather than its rendering — the mailbox rather
than the subject line, the pane's content rather than its command name, the register's tables rather
than its summary sentence. And my own instruments were wrong three times before the subject was, every
time caught by results being identical when they should have differed.** The launcher booted this seat
as the wrong agent and four surfaces agreed with it; only the tree disagreed, and the tree was right.
**When every indicator agrees and one artefact dissents, measure the artefact.**
