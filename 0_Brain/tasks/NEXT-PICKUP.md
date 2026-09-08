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

## 🔴 THE QUESTION ON KAM'S DESK RIGHT NOW (asked 13:0x, unanswered when this was written)
**"Which do you want next: the rest of the path guard, or Secuura?"**
- **If he says path guard** → §"WHAT IS NOT BUILT" below, item 1.
- **If he says Secuura** → §SECUURA STATE. His 07:10 instruction (*"deploy and merge
  everything that has been tested and done and is ready for deployment"*) and his 10:14
  (*"archive any tickets that have been closed or deployed"*) have had NO seat on them
  since s149 wrapped at 10:56.
- **If he is silent** → default: finish the path guard. It is inside the commission he
  named, it is the last structural piece, and Secuura is a bigger swing that deserves his
  word first.

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
1. **The path guard is HALF built.** `pretooluse_no_cd.sh` refuses git WRITE verbs pointed
   outside this tree (8-case matrix, proven). It does **NOT** refuse general shell writes
   (`rm`/`mv`/`cp`/`tee`/`>`/`sed -i`) into another client's folder or the sister tree, and
   **nothing anywhere stops a read**. On the travel drive both clients are mounted for both
   agents, so that is the mode where discipline is ALL there is.
2. **PORTABILITY.md has no "Headless second agent — bring-up" section**, and there is no
   doctor check for the untracked `.git/hooks/pre-commit` (a clone does not carry it — a
   fresh Tuesday clone will happily push conflict markers).
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
5. **`setsid` does not exist on macOS.** `nohup … </dev/null >log 2>&1 &`, then verify
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
No agents running. The Datasec/laptop seat WRAPPED at 12:21; NexusAI S47 wrapped at 12:15
(`main` = `cd2b543`). Kam is at the panel and answering within minutes.
