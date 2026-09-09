---
date: 2026-09-09
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general work are Wednesday's, on the Studio.
source: written at Tuesday s2's 70% checkpoint, 2026-09-09 ~11:40 AEST
status: live
supersede: replace this file WHOLESALE at the next pickup; never append. It replaced the s1 pickup.
---

# NEXT PICKUP — Tuesday, after s2. FIVE AGENTS ARE RUNNING. Do not launch a sixth without reading this.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything.** 🔴 **AND WHEN ITS
FRESHNESS LINE REPORTS A LAG, `curl -s http://127.0.0.1:47787/api/chatlog` BEFORE ANSWERING KAM** —
the local dashboard server sees his typing before any synced file does. That is how his 11:29 question
was found; the file was four minutes behind. Mail timestamps are UTC ≈ AEST−10.
**Rotation band 80–90%; 70% is a checkpoint only.**

## 🟢 WHAT IS RUNNING RIGHT NOW — FIVE seats on the Security Review, partitioned by component

Kam, panel 2026-09-09: *"yes, run multiple agents on the security review."*

| Pane | Seat | Partition | Rows |
|---|---|---|---|
| ~~`%3`~~ | ~~`SecRev-A`~~ **CLOSED 11:5x — partition COMPLETE 19/19, verdict on disk** | HPAuthenticationManager · infra_hpam | 19 ✅ |
| `%4` | `Datasec/SecRev-B` | License-Services · LicenseServer | 25 |
| `%5` | `Datasec/SecRev-C` | HPK_Deployment_Utility · UniversalPrint · MailFlow · CypherSharePoint · QuickAccessLibrary | 28 |
| `%6` | `Datasec/SecRev-D` | Task-Dispatcher · hpam-marketplace · datasec-administration-portal · WorkPathApplications · cc-api · hpam-api · SPDF-D1 | 25 |
| `%7` | `Datasec/SecRev-J` | **the JUNE baseline** — `Deliverables/03_Findings_Register.md`, F-01…F-31 | 31 |

**Shared method:** `2_Project_Files/fleet/briefs_staged/2026-09-09_secreview-round2-parallel-method.md`.
**Launcher:** `2_Project_Files/fleet/launch_secreview_round2_seat.sh <b|c|d>` (one script, parameterised;
seat A predates it and runs `launch_secreview_round2.sh` plus an in-flight amendment).

🔴 **THE RULE THAT KEEPS THIS SAFE: NO SEAT EDITS THE REGISTER.** Four seats, one
`13_Consolidated_Findings_Register_2026-09.md`. Each writes
`_Working/verification-2026-09/round2-<a|b|c|d>.md`. 🔴 **SEAT A IS CLOSED — THE CONSOLIDATOR IS A FRESH SEAT, NOT A.** Launch one when all five verdicts
are in; it reads the five files cold. A was closed because a rung-6 ghost (`go ahead and consolidate`)
appeared at its finished prompt, and because a consolidator with no stake in any partition is better
than one adjudicating its own five proposed band-moves. **A's verdict file is self-sufficient.**
**THE CONSOLIDATOR IS BUILT AND WAITING:**
`2_Project_Files/fleet/launch_secreview_consolidation.sh` (brief + prompt beside it). 🔴 **Its first
guard REFUSES (rc 9) unless all FIVE verdict files exist and are non-empty** — so the ghost sentence
`go ahead and consolidate` is now *unexecutable*, not merely *unwise*. Exercised both ways with a real
positive control (5 present → rc 0; 4 present → rc 9 naming the missing file; an EMPTY file → rc 9).
A second guard refuses if the register no longer reads 23 Criticals, so it cannot run twice.
**Launch it when the monitor reports the fifth verdict.** It applies all FIVE in ONE action at
the end, on Tuesday's word — do not let it start early, a partial consolidation is the worst outcome.**
The clause is a launch guard (rc 12), not a request. **`_Working/PROGRESS.md` is shared too — leave it.**

**The method, and it is the agent's own recommendation adopted:** re-derive each CVSS vector FROM
SOURCE, then compute. **Never adopt round 1's computed column.** `H-D1` is why — its recorded vector
implied Critical 9.6 and re-deriving one metric from source gave High 8.6, moving the row DOWN.

🔴 **KAM RULED `extend` ON JUNE, 2026-09-09 11:40, verbatim: *"extend the scoring pass into the June
baseline"*.** Recorded in the queue. Seat J is that ruling. **June is a SIGNED-OFF deliverable, so it is
the high-stakes partition and the only one likely to move severities UP.** Measured by Tuesday with four
reference-vector controls: `F-07` filed High 8.7 → its own vector computes **9.2 Critical**; `F-10` filed
High 8.2 → **9.4 Critical**; `F-22` filed **Medium** 7.7 → **9.0 Critical**, and 7.7 is itself a
High-band number under a Medium band, so it is wrong twice. **Round 1 recorded `F-22` as filed High —
that is wrong, June says Medium; take it from the pickup, not from round 1's table.** Round 1's
*computed* figures were all three exactly right.

⚠️ **SEAT-COUNT STALENESS, and it matters only at consolidation:** B, C and D were launched believing
there were FOUR seats and their report headers say so. **There are five verdict files, not four.** When
you give seat A the consolidation word, say **five** and name them:
`round2-a.md · round2-b.md · round2-c.md · round2-d.md · round2-june.md`.

## 🟡 VERDICTS IN SO FAR — proposed, NOTHING APPLIED, register untouched at 11:20:34

- **`round2-a.md` (43 KB, COMPLETE 19/19).** Five bands move, four up one down: **`D-01` High→Critical 9.2 ·
  `I-D1` High→Critical 9.1 · `I-D2` High→Critical 9.9** · `I-D8` Low→Medium · `D-07` Low→Informational.
  **Estate 23 → 26 Criticals on this partition alone**, total conserved at 339 (Tuesday re-added it).
  🔴 **And the mechanical band-crosser table was WRONG about A's partition 4 times out of 5** — `I-D4`,
  `I-D5`, `I-D10`, `I-D11` do not move. **That is the vindication of not adopting the computed column.**
- **`round2-d.md` (20 KB).** 24 of its 25 rows carry a **band with no score and no vector at all**.
  Tuesday sized it estate-wide rather than taking the partition as the estate: **22 tabulated rows carry a
  band with nothing checkable underneath, 2 of them High, 0 Critical affected**; 20 more are Info, which
  legitimately has no CVSS. **The vectors exist in the delta files and were dropped in assembly** — a
  register defect, mechanically fixable, no judgement needed.
- **`round2-b.md` (57 KB).** Both surviving Criticals HOLD, and seat B **executed the attack's first
  cryptographic step** rather than inferring it — the committed API key unwraps a real committed licence's
  encryption key; the root CA key as negative control fails. **It also stopped a downgrade:** round 1 would
  have published `NEW-1` at 9.3 base; B agrees `A:H` leaves the base but found round 1 never examined `C`,
  which is `C:H` (every tenant and device private key ever issued, offline, from committed material) —
  **base 10.0 on its own.** Four bands move; **net estate effect on C and H is ZERO.**
- **`round2-june.md` (22 KB).** **Three June rows move, net +1 Critical:** `F-02` Critical→High (down),
  `F-07` and `F-10` High→Critical (up). **`F-22` explicitly NOT moved** — its vector computes Critical 9.0
  against a filed Medium, but it is one of only two rows with **no scoring note at all**, so there is no
  recorded intent to check against. Named, not moved. **And the mechanism is diagnosed, refuting round 1's
  inference:** 18 of 31 numbers disagree with their own vector, but **26 of 31 are reproducible by changing
  exactly ONE metric** — the signature of *a vector edited after the score was computed and never
  recomputed*, not of scores estimated to fit a band. **Different defect, different remediation.**
- **Still to report: C only.**

## 🔴 WHAT IS ACTUALLY ON KAM'S DESK (this seat's items only)

0. 🔴🔴 **`secreview-june-register-discloses-credentials` — rec `all-three`, default HOLD. THE MOST
   URGENT ITEM ON THIS DESK AND IT IS NOT A SCORING ISSUE.** The June register — **signed off, customer
   facing, rendered to `.docx` for circulation** — prints **8 lines of secret values verbatim** in `F-16`
   (6) and `F-12` (2): 2 Entra client secrets · 1 platform API key · 1 App Configuration connection-string
   secret · 1 PFX password · 4 service/admin password literals. **Class and count only — never quote a
   value, a prefix or a length from that document, including into a ticket.** The finding that reported
   committed secrets **reproduced them into a document with wider distribution than the repository**, so
   rotating the repo secrets and scrubbing history both leave the report untouched. **NOT established:
   whether any is still live** — that needs a live pass, barred by the holds. It is a DISCLOSURE, not a
   confirmed compromise. **The one thing only Kam can answer: where has that document already been sent.**
   Also: `F-16`'s evidence pins HPAM config to tenant `fc05dcdd` — direct evidence on the question he
   reserved to himself; no conclusion drawn.


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
