---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 13:0x by s152
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 13:0x Tuesday. Kam's commission is largely BUILT; two things are open.

## 🟢 KAM'S STANDING INSTRUCTION FOR THIS SEAT (verbatim, 2026-09-08 ~12:1x)
> *"Okay, rotate, and after you've rotated, keep working on this new Wednesday, Tuesday, and chat structure."*

**s152 did that.** Phases 0, 1, Tuesday's home, her launcher, her inbox and her brief are
built, pushed and proven. **`main` = `9c33d004`.**

## 🟢 BOTH ANSWERED THEMSELVES — the path guard is BUILT and SECUURA IS RUNNING
The question put to Kam at 13:0x ("path guard or Secuura?") went unanswered; s152 did the
declared default (finished the guard) and then started Secuura anyway, because on re-reading
**it was never blocked on him**: his 07:10 instruction plus the week-scoped merge and deploy
grants already authorised it, and the COO rule says such a ticket is executed, not listed.

**🔴 YOUR LIVE DUTY — ONE agent is running and it reports to you, not to Kam.**

`%171` = **Secuura s150** (NOT s153 — its own history is the authority for its seat number).
At 14:0x it holds a GO to **merge #906**, then file ONE ticket for F1–F4, then act on three
Kam rulings, then return to the **P2 In Review queue** (29 tickets, category-1).
**Watch for its MERGED receipt and score it.** The QA pane `%172` is CLOSED — its verdict is
delivered and its work is done.

**KAM RULED THREE CARDS AT 14:00 and all three are relayed with their artefacts named:**
- `secuura-ks963-getuserbyid-swallows` → **rethrow** — KS-963 is ACTIONABLE now; its own
  "do not fix yet" line is superseded by his word.
- `secuura-platform-s-count-was-wrong-when-you-ruled` → **all18** — **the Platform S hold is
  LIFTED**; the remaining three get archived.
- `secuura-61-archived-while-still-open` → **three** — unarchive KS-174, KS-796, KS-802 only.

**#906 verdict: GO-WITH-FINDINGS** (gate scored 1.0). Wednesday's completion check passed all
six requirements and the merge GO is given under Kam's week-scoped grant. **F1 (gate fails OPEN
when a gated package's deps are absent) and F2 (gate reads the WORKING TREE, not the pushed
commits) are MAJOR and neither is a regression** — they go into one ticket, same logical path.
Relaunch that gate by its PATH if ever needed:
`2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks989_906.sh [--check]`

**LAUNCHER CHANGE (Kam, 14:05):** it no longer opens the dashboard in a browser — the server
still starts, he refreshes his own saved tab. `WED_OPEN_DASH=1` restores it for a machine with
no saved tab yet (Tuesday's). Exercised both ways with a stub `open`; boot prompt byte-identical.

**🔴 INSTANCE 6 IS LIVE ON THE TRUNK until #906 merges:** `systemTest/akto` `format:check` RED
on `develop 986c592d5`, arriving via merge `512480ef1` (#892) — the PREVIOUS seat's own merge,
~4 hours before it was found (the gate corrected "three hours" to four).

## WHAT WAS BUILT TODAY — do not re-derive any of it
| Thing | Where | Commit |
|---|---|---|
| **Phase 0** — one writer per chat file. `chat_log.json` is DERIVED + gitignored; writers append to `chat_wednesday/tuesday/kam.json`; `chat_legacy.json` (1778) frozen | `2_Project_Files/tools/chat_streams.py` | `a02f5528` |
| **Phase 1** — the `WEDNESDAY \| TUESDAY` toggle, both surfaces, filtering chat + fleet + tally + chips on `agent` | `dashboard/cockpit.html`, `chat.html` | `8105f925` |
| **Tuesday's clone + ONE parameterised launcher** (`WED_AGENT` decides; `Launch_Tuesday.command` is 20 lines) | root launchers | `0666f7b5` |
| **`tuesday-agent@agentmail.to`** + inbox keyed on the AGENT, never the hostname | `fleet/inbox_digest.sh` | `29063f0c` |
| **Guard scratchpad exemption + launcher own-repo ssh pointer heal** | `hooks/pretooluse_no_cd.sh`, launcher | `acc7440e` |
| **Tuesday on the T9 (2.1 GB) + her first-boot brief** | `/Volumes/KK_T9_External_HDD/TUESDAY`, `0_Brain/tasks/FIRST-BOOT-TUESDAY.md` | `9c33d004` |

**MEASURED and settled — do not re-derive:** Tailscale mesh has served this dashboard
since 2026-08-20 (NOT new work) · the new-Mac run-sheet exists and was exercised
2026-09-02 · **`CLAUDE_CONFIG_DIR` gives a genuinely separate Claude auth namespace,
TESTED**, and the keychain entry is MACHINE-LOCAL so Kam logs in once per machine per
agent.

## 🔴 WHAT IS NOT BUILT — stated so no successor assumes it
1. **The path guard is now BOTH halves and armed** (`hooks/pathguard.py`, 17-case matrix
   through the full hook, both agent directions, doctor check exercised in three states
   including present-but-INERT). **What it still does NOT do: gate READS.** Nothing stops a
   `cat`. On the travel drive both clients are mounted for both agents, so that is the mode
   where discipline is ALL there is — the strongest mode is two machines.
   Override for deliberate provisioning: `WED_ALLOW_CROSS_TREE=1`, and every use is stated.
2. **DONE:** PORTABILITY.md has a "Headless second agent (TUESDAY) — bring-up" section, and
   the pre-commit hook now has a TRACKED master at `2_Project_Files/fleet/hooks/pre-commit`
   with a doctor check that also detects DRIFT. (The earlier claim here that no doctor check
   existed was wrong — one existed since 2026-09-02; the real gap was that the hook's BODY
   lived only in a commit message.)
3. **Tuesday's MSGraph credentials** — deliberately withheld, on Kam's desk.
4. **`/Volumes/DevMASTER/TUESDAY`** (the staging clone) is still at `8105f925` and lacks
   `Launch_Tuesday.command`. **The T9 copy is the real one and is current.** The guard
   refuses this seat a `git -C` write there, correctly; it is Kam's one command or simply
   irrelevant now that the T9 is the deployment target.

## 🔴 THINGS THAT BIT s152 — read before repeating them
1. **The hook block in `pretooluse_no_cd.sh` is inside a SINGLE-QUOTED shell string.** An
   apostrophe in a comment there BRICKS THE HOOK and blocks every Bash call including the
   restore. Recover with the **Edit tool**, not `cp`. (Second occurrence in two days; the
   warning now sits in the file.)
2. **The guard fails CLOSED on `$VAR` paths** — `git -C $S/x init` is refused even when
   `$S` is the scratchpad. Write literals.
3. **The guard also refuses a command QUOTED inside a message.** To send Kam a command,
   write the text to a file and pass `"$(cat file)"`.
4. **Screenshots from the browser tool are a CROP of a 3491px viewport.** Do not read
   geometry from them — `getBoundingClientRect` + `elementFromPoint` is the instrument.
5. **`cockpit.sh say --mail` NOW REFUSES a cited mail older than 15 minutes** (fixed 14:0x
   after it went green on a tap carrying content no mail held — sixth instance of that
   family, agent-caught). Send the mail, read it back at the destination, THEN tap a bare
   pointer. `SAY_ALLOW_OLD_MAIL=1` exists for a genuine continuation and must be said aloud.
6. **`setsid` does not exist on macOS.** `nohup … </dev/null >log 2>&1 &`, then verify
   `tty` is `??`.

## SECUURA STATE (from s149's handover, 10:56 — nothing has moved since)
    origin/develop 986c592d5 · demo 400517aaf · unarchived 370
    #903 #904 #905 #793 open, unmerged · #896/#899/#900 UNAPPROVED deliberately
    KS-968 In Progress · the schema trap is at c38040bd1, NOT on develop
    Next highest-value: KS-989 (P1) — "wire format:check, never quality" travels with it
    HELD: PS-Done 18 (Kam's card) · Tested-Not-Deployed (Kam's `hold`)
🔴 **PROJECT TRAP:** any probe of `users.email` by literal comparison is VOID BY
CONSTRUCTION (AES-GCM). Resolve via `email_lookup_hash`; decisive on a MATCH only.

## OPEN CARDS ON KAM'S DESK (all with safe defaults; nothing blocks)
`secuura-platform-s-count-was-wrong-when-you-ruled` (18 PS tickets, default HOLD) ·
`hpsm-credential-bearing-prd-outside-every-snapshot` (Tuesday's) ·
`secrev-live-pass-blocked-on-tenant` (Tuesday's) ·
`nexusai-rd369-round3-or-ship-at-the-cap` (Tuesday's) ·
**NOT FILED and still owed:** `secuura-ten-cascade-collateral-restore-or-leave` — the
`decision_queue` refused it while `chat_log` was corrupt this morning; re-file it.

## FLEET
**s150 Secuura/Blockchain LIVE in `%171`** (launched 13:14). QA gate ran 13:45→14:00 and its pane is CLOSED. The Datasec/laptop seat WRAPPED
at 12:21; NexusAI S47 wrapped at 12:15 (`main` = `cd2b543`). No Tuesday seat exists yet —
she is provisioned on the T9 and waits on Kam's Claude login.
Kam was answering within minutes until ~12:53 and has been quiet since.
