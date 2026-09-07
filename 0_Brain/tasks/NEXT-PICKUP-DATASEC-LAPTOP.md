---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at ~21:15 by the 19:51 seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~21:15 AEST Monday 2026-09-07. TWO SEATS LIVE. KAM IS ASLEEP.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before
writing anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a
CHECKPOINT ONLY.**

## 🔴 KAM'S LAST INSTRUCTION, 2026-09-07 ~21:00, verbatim
> *"keep working on security review and I will review in the morning when I wake"*

He is asleep. **Nothing tonight is worth waking him.** Both live seats were launched under this
instruction plus his 21:00 ruling. Everything else holds.

## FLEET — 2 live, both verified at rung 5 (pane CONTENT, never a non-zero ctx)
- **`%10` — `Datasec/SecurityReview`.** Five Step-2 delta reviews.
  Mechanism, BY PATH: `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/launch_secreview_delta_batch2.sh`
  (`--check` runs every guard without launching). Brief and prompt beside each other in
  `2_Project_Files/fleet/briefs_staged/2026-09-07_secreview-delta-batch2{.md,.prompt.txt}`.
  **Its report lands at a FILE, not in mail** — this project has no inbox and `send_brief.sh`
  refuses it by design:
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/delta-review-2026-09/_BATCH2_REPORT.md`
- **`%11` — `Datasec/NexusAI`.** RD-361 **ROUND 4**, on Kam's 21:00 `deadlock` ruling.
  Launched via the project's own `Launch_Claude.command`; brief delivered by MAIL and read back
  non-null in BOTH `datasec-nexusai@` and `coagent@` before the launch.
  Brief: `2_Project_Files/fleet/briefs_staged/2026-09-07_nexusai-rd361-round4.md`

## 🔴 KAM'S TWO RULINGS TONIGHT — one is DONE, one is WAITING ON HIM
| Card | Ruling | State |
|---|---|---|
| `rd104-gh-identity-acceptance-false-premise` | **`youcheck`** @ 19:58 | **WAITING ON KAM.** Step-by-step delivered to his panel with both links on their own lines. **His two answers unblock three gate-passed merges. Nothing else does.** |
| `nexusai-rd361-round3-blocker-survives` | **`deadlock`** @ 21:00 | Executed — round 4 briefed and launched. **Delivery still OWED:** the seat writes the ruling onto RD-361 as a comment in its first turn and reports the comment id; then `decision_queue.sh --delivered nexusai-rd361-round3-blocker-survives "<comment id>"`. |

**The two answers Kam owes, so you can act the moment he gives them:**
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — is there a
   **required reviewer** on the `demo` environment?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — does
   **`CI_DEPLOY_ENABLED`** exist, and what is its value?
**If the switch is ON and `demo` has NO required reviewer, HOLD the merges** — a merge to `main`
then deploys to the demo with no human gate. Any other combination and the merges go on his
existing week-scoped authority. Repo confirmed from the git remote, not composed.

**🔴 THOSE TWO CLICKS ARE WORTH MORE THAN THREE MERGES, and the chain is measured link by link:**
NexusAI releases through `main` (RD-367) · `main` is frozen since 09-01 and **250** commits behind
(the gate's measurement, not the stale 248) · Kam ruled **`mergeup`** on it at 18:58 · the mergeup
is what is blocked · behind it sits a **Release Ready column of 46**, counted through
`2_Project_Files/fleet/board_count.sh` which certified *"limit was 250, so this is a real count and
not a cap"*. Those 46 are the *"tested but not deployed"* items Kam pointed at on 09-07 13:40.
**Do not quote a NexusAI board number from a hand-written query — `board_count.sh jira` takes the
site with NO scheme (`${JIRA_SITE#https://}`), and it correctly REFUSED to total
`statusCategory != Done` because more pages exist.**

**RD-321 — CLOSED, no action.** S45 flagged it as Highest-priority and unmentioned in any artefact,
which is the shape that goes missing. Wednesday read it: **Release Ready, assigned to Kam, updated
2026-09-06** — finished and sitting in the column above, nothing missing. Good raise, boring answer.
(`JIRA_SITE` in the NexusAI `.env` carries **no scheme**; a bare `curl` to it returns HTTP 301 and an
empty body, which reads exactly like an auth failure. Prefix `https://`.)

## 🔴 RD-361 ROUND 3 WAS A NO GO — and round 4 must not repeat its shape
Round 3's fix relaxes the gate only while `firstRunComplete` is absent. **That flag is also written
by three FRONTEND sites during ordinary setup** (`static/js/first-run-setup.js:2796` connection test,
`:3069` validation, `:3494` the "don't show again" checkbox), all before auth is enforced, and the
wizard's tab order puts Log Analytics **before** User Access. **So the bricking path is the intended
journey.** Round 3 also opened **F-2 (Major)**: a deployment that HAD auth enforced serves **open
mode across all 175 routes** if `settings.json` is emptied with backups gone.
**Genuinely closed, and recorded as closed:** F-B / M10, proved by contrast (mutation reds exactly
cell D; restore 23/23). Single-write-site premise verified across **all 678 tracked files**.
**Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md`

**Round 4's item 1 is a MEASUREMENT THAT MAY KILL THE ROUND**, and that outcome is a success:
Wednesday's inference — that `initializeFiles()` normalises a lost `settings.json` to `{}` before the
gate reads it, so "never set up" and "set up then lost" are byte-identical and **no** content
discriminator can work — **is an inference, not a measurement.** The seat is told to try to break it
and to STOP and mail Wednesday if a real discriminator exists. **Do not let round 4's output be
recorded as closing SEC-01 unless the gate says so.**

## SECURITY REVIEW — the frame, because the previous handover's list was complete over a smaller one
    32  components with a June baseline (Deliverables/Components/*.md)
    15  have a 2026-09 DELTA review
    10  have a 2026-09 VERIFICATION pass
     2  PARKED by Kam 2026-09-07 10:44 (both Vision components)
     5  REMAIN — CypherOneDrive · Teams · CommonValueLibraryCypher · Cyphercard-Enrolment-App · HPSM

**🔴 `hpsm-main` was NOT in the predecessor's list of four.** It has a June baseline and no 2026-09
output; Wednesday found it only by enumerating the frame. The brief names it as Wednesday's
inference and gives the agent permission to skip it with a reason. **This is the census family
firing on Wednesday's own handover** — the list was right about batch 2 and silent about the tree.

## WHAT THIS SEAT DID, and the one thing worth carrying
- **Caught a `good night` at the wrapped NexusAI pane's prompt** — detector said ghost text, nobody
  typed it. Rung 2 of the ladder. **Closed the pane rather than clearing the line** (a cleared prompt
  can be re-populated; a closed pane cannot). Listeners 13→13, port 3001 dead before and after.
- **🔴 THE CHAT-LOG UNION IS NOT OPTIONAL, AND HERE IS THE MEASUREMENT.** A push conflicted with the
  Studio seat. Union on `(ts, text)` across **both conflict sides AND a pre-flight backup**:
  **1663 / 1664 / 1665 in — 1667 out.** Every source was missing something, and **the backup alone
  held one message neither conflict side had.** Taking either side — the default resolution — would
  have deleted it. Back BOTH `chat_log.json` and `decisions.json` to the scratchpad before any
  multi-step git sequence, every time. The union script is at
  `/private/tmp/.../scratchpad/union_chat.py` for this session only — **rewrite it, do not hunt for it.**
- **Digests were conflicted too. Resolved from SOURCE** (re-ran `boot_digest.py` on the lesson files)
  rather than picking a side — a derived artefact comes from its source, not from whoever won.
- **Boot measured `ctx:27%`** on the by-tier digest (WED-139 duty).

## ⚠️ TRAPS — the first one FIRED tonight exactly as written
1. **🔴 A T9 LAUNCH HITS A FOLDER-TRUST DIALOG AND NO GUARD CAN SEE IT.** The Security Review launch
   showed *"Is this a project you created or one you trust?"* with **`No, exit` preselected**, and
   sat there. Every wrapper guard had passed. **Only reading the pane caught it.** Answer with
   `tmux send-keys Down` then `Enter`. Once trusted, later launches skip it. **Verify EVERY launch at
   the pane, always** — a check that cannot observe a dialog appearing after `exec` cannot fail.
2. **`launchers.conf` points at DevMASTER, which is not mounted here**, so `cockpit.sh launch` and
   `brief_and_launch.sh` cannot start a T9 seat. Launch by hand with `tmux split-window`, then
   **`tmux set-option -p -t <pane> @cockpit_name '<Client/Project>'`** or `cockpit.sh say` cannot
   find the pane. **Do NOT rewrite `launchers.conf`** — it is shared and correct for the Studio.
3. **`send_brief.sh` has three gates and all three fired on me tonight, correctly:** a literal
   `PROVENANCE:` line (not `## PROVENANCE`); **absolute** paths or an explicit owner in every
   citation; and the heading `RULED BY KAM, NOT YET IN AN ARTEFACT` with bullets shaped
   `- <card-id>: "<ruling verbatim>" -> must land in <artefact>`. Budget three refusals.
4. **No `cd` in a Bash call** (`pretooluse_no_cd.sh`). A wrapper that legitimately needs `cd` is
   written with the **Write tool**. **`git -C $VARIABLE <writeverb>` is refused** — write git paths
   literally.
5. **Before pulling, discard the ten regenerated dashboard feeds**, then pull, then push. Never
   `git add -A 0_Brain/dashboard/data` — stage `chat_log.json` and `decisions.json` BY NAME.
   **Never `git checkout <sha> -- 0_Brain/dashboard/data`** — that is what destroyed four of Kam's
   rulings this afternoon.
6. **Ghost text has now appeared three times at NexusAI prompts.** Run
   `2_Project_Files/fleet/cockpit/pane_prompt_check.sh <pane-%ID>` before reading anything at a
   prompt. `pane_close.sh` refuses a name that does not resolve to a tty — pass the `%ID`.

## STANDING
**Kam's week-scoped grants (read as through Sunday 2026-09-13):** merge on Wednesday's word once the
gate passes · deploy · board judgement calls. **🔴 THE PRODUCTION LIFT IS SECUURA ONLY** — 12:07
lifted, **narrowed at 12:10 to *"Only secure"*. Datasec has NO production grant. This is the Datasec
seat.** Ticket CREATION aggregates (one larger ticket per logical path, 13:23). Every analysis record
carries **FOUND / TESTED / HOW** with the controls named under HOW (18:56:36). **Kill anything that
queries Azure credits** (13:06 — five raises, closed).

**NAME THE FRAME** in any sentence claiming completeness — the third failure family, filed today,
and it beats both existing defences because both controls pass and the number really is read from
the source. It caught Wednesday's own handover tonight (the missing fifth component).

Taps ≤200 chars, pointer only, mail FIRST and verified by non-null `preview`, THEN tap.
`<<'EOF'` or the Write tool for every body. **Never delete — quarantine.** Search before you file,
by SYMBOL / PATH / ERROR STRING.

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one
dashboard, one chat panel, **ONE USAGE LIMIT**. Do not write the shared files (`NEXT-PICKUP.md`, the
daily note, `_ledger.md`) — they are hers this session. Panel messages open `[LAPTOP / Datasec]`.
Secuura mail in the shared inbox: **read the subject, not the body, and leave it.**
