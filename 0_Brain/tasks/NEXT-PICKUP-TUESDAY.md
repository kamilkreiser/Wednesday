---
date: 2026-09-09
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general work are Wednesday's, on the Studio.
source: written at Tuesday's s1 wrap, 2026-09-09 ~10:3x AEST
status: live
supersede: replace this file WHOLESALE at the next pickup; never append. It replaced FIRST-BOOT-TUESDAY.md.
---

# NEXT PICKUP — Tuesday, after s1 (first boot). THE MACHINE IS BUILT. NOTHING IS IN FLIGHT.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — read EVERY line.**
Mail timestamps are UTC ≈ AEST−10. **Rotation band 80–90%; 70% is a checkpoint only.**

## 🟢 STATE — the machine is done, and s1 started no work

`doctor.sh`: **19 warnings → 3**, and all three are EXPECTED, not open:
Matilda absent (Kam chose **Moira (Enhanced)**, installed) · DevMASTER unmounted (normal here) ·
Tailscale absent (**Kam ruled it out** 2026-09-09: *"no tailscale needed on this machine for now"*).

**Do not re-raise any of the three.** The reopening condition for Tailscale is written in
`PORTABILITY.md` item 8: *this machine needs reaching from outside the LAN*, and nothing else.

Full bring-up record — every tool, version, and trap — is `PORTABILITY.md`, section
**"Kamils-Mac-mini — Tuesday's machine, brought up 2026-09-09"**. Read that before touching the
machine; it is a checklist now, not an investigation.

## 🔴 WHAT IS ACTUALLY ON KAM'S DESK

**Only one thing, and it is not urgent.**

1. **The dead Secuura tenant is back in `~/.azure` on this machine** — `Secuura Subscription`,
   tenant `4012a4e8…`, `isDefault: true`; and global `gh` is `kksecura`. **Both INERT** (no valid
   token; `az account show` refuses). **This seat is isolated from both by construction** —
   `AZURE_CONFIG_DIR`/`GH_CONFIG_DIR` point at `4_Credentials/`, 0 subscriptions, not logged in.
   **Not fixed by s1 deliberately:** `~/.azure` is Kam's machine-global state and the bundle lives in
   `Setup and System/`, outside this seat's folder. **The recommendation given to him is to fix the
   BUNDLE, not this machine** — otherwise the next restore repeats it. Mechanism + durable fix:
   `learnings/2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync.md`.

2. **Schedule collision, minor, his call:** `com.tuesday.close` and `com.tuesday.nassync` both fire at
   **23:00**. His "sync at 11pm" predates Tuesday having a close ritual. Recommended 23:30 for the
   sync; his commissioned time was left alone.

**Nothing else is waiting on him.** The Jira question s1 raised was ANSWERED BY s1 and withdrawn —
see below.

## ✅ WHAT s1 SETTLED, so you do not re-derive it

- **Jira works. You already have board access** under Kam's 2026-08-03 read-only tracker grant:
  source `!CODING/Datasec/NexusAI/4_Credentials/.env` transiently, never copy it.
  🔴 **`JIRA_SITE` has NO SCHEME — you MUST prefix `https://` or you get 301 text/html, which a JSON
  parser reports as "unreachable" and which has twice been misread as "I have no access."**
  Verified 2026-09-09: authenticates as Kamil Kreiser. Board **RD**, board id **305**.
  First read: **Release Ready 51 · In Progress 6** (real counts). **Open total and To Do are
  UNMEASURED** — `board_count.sh` refuses them because more pages exist than Jira's cap returns.
  That refusal is correct; the gap is **WED-146**.
- **`gh` and `az` are unauthenticated and s1 recommends LEAVING them so.** Pushing uses the per-repo
  deploy key (`core.sshCommand`, verified), and a coordinator seat is designed to hold no client
  GitHub/Azure identity. If a task needs one, ask Kam and name which identity.
- **Docker works** (daemon 29.7.2) even with no `/usr/local/bin/docker` — the CLI is in the app
  bundle and `~/.zprofile` puts it on PATH for login shells.
- **The scheduler is agent-aware** (Kam ruled `parameterise`). Four `com.tuesday.*` jobs armed,
  each plist carrying `WED_AGENT`. Three `com.wednesday.*` plists are QUARANTINED at
  `~/Library/LaunchAgents/_quarantine_2026-09-09_wednesday-jobs-on-tuesdays-mac/` — moved, not
  deleted. **Do not arm Wednesday jobs on this machine.**

## ⚠️ TRAPS — live, and most of these fired on s1

1. 🔴 **The Bash tool runs ZSH. `${PIPESTATUS[0]}` is empty — it is `$pipestatus[1]` here.** Better:
   never branch on a pipe. `cmd > out 2>&1; rc=$?` then read the file. s1 hit this.
2. 🔴 **A `cat`/`sed` of a big file through Bash SPILLS TO A FILE and that is a FAILED read, not a
   completed one.** Read the boot digest with the `Read` tool in offset/limit chunks (~900 lines for
   the digest, ~20 rows for the ledger — rows run ~1.9 KB each) and **assert the last line landed.**
3. 🔴 **`git -C $VARIABLE <writeverb>` is REFUSED by the hook — write paths LITERALLY.** `cd` is
   refused too. Absolute paths everywhere.
4. 🔴 **The shared daily note and `decisions.json` conflict constantly — Wednesday writes them too.**
   Resolve by UNION (keep hers whole, append yours), never overwrite. **After ANY commit touching
   `decisions.json` or `chat_log.json`, parse it out of HEAD — and do it BEFORE the push, not after.**
   s1 pushed a corrupt `decisions.json` by doing it after.
5. **The pre-commit hook now guards JSON** (s1 fixed it — it excluded `.json`, the only class that has
   ever carried markers). **It is machine-local and untracked: after any fresh clone, copy
   `2_Project_Files/fleet/hooks/pre-commit` into `.git/hooks/` or you have no guard.**
6. **`decision_queue.sh add` scores the prior-ruling gate on BLUF LENGTH, not subject** — a long,
   careful BLUF gets refused and a two-character stub of the same id is accepted. Measured s1.
   Use `--override-prior-rulings` with the reason stated as the MEASUREMENT in the BLUF.
7. **`decision_queue.sh` REFUSES if origin has newer commits touching the store — pull first.** That
   refusal is the guard working; do not route around it.
8. **Kam's panel rulings do NOT reach the decision queue automatically.** After
   `kam_rulings_today.sh`, cross-check each ruling against `decision_queue.sh show` and record the
   ones in YOUR scope.
9. **No `timeout` on macOS.** And `spctl`/`codesign` BEFORE installing any downloaded app, never after.
10. **Verify a mail by a NON-NULL `preview`, never by the send's exit code.** Read the inbox at
    limit ≥ 3 — a real inbound sits under your own outbound echo.
11. **Counts come from `2_Project_Files/fleet/board_count.sh`, never a hand-written `first:`/`maxResults`.**
    It refuses rather than printing a cap as a total. Respect the refusal.
12. **No statusline here unless the seat runs inside tmux.** `tmux` is installed now, but if
    `tmux capture-pane` is unavailable the honest word for context is **"unmeasured"** — never quote
    the harness `<total_tokens>` counter, which is a budget and not the window.

## STANDING

**Scope (Kam, 2026-09-09, verbatim):** *"you will work on ONLY datasec projects unless otherwise
instructed. Wednesday will work on Secuura and general tasks."* Datasec lives at
**`/Volumes/KK_T9_External_HDD/!CODING/Datasec/`** — DevMASTER is not mounted and is not needed.
*"Your main drive is the T9 drive."*

**Cross-seat mail carries COORDINATION ONLY** — never Datasec code, findings, tickets or credentials.
Yours is `tuesday-agent@agentmail.to`; hers is `wednesday-agent@`. **CLAIM WED WORK BEFORE STARTING IT**
(`2_Project_Files/tools/wed_claim.sh`) — it writes the shared `WED-OWNERSHIP.md` keyed by hostname.

**Kam's week grants run through Sunday 2026-09-13:** merge on the gate's pass · deploy · production
changes — **production is SECUURA ONLY; DATASEC PRODUCTION IS UNGRANTED, ask rather than argue it in.**
Ticket creation AGGREGATES. **FOUND / TESTED / HOW** on every analysis. **Names, not pronouns.**
**Never delete — quarantine.** Action-first when his hands are needed, with the literal steps and the link.

🔴 **DO NOT run the wrap's vault step from this seat** — `end-of-session.md:50` is `git add -A` and the
vault's untracked set includes Secuura paths (hard rule 2). Skip it and say so in the wrap.

## WHAT s1 WOULD SAY IF IT COULD SAY ONE THING

**Every real finding today came from reading a mechanism before running it, and the one failure came
from checking after instead of before.** The scheduler would have booted Wednesday out of Tuesday's
tree at 06:00 daily — caught by reading the installer. The credentials bundle carried a dead tenant —
caught by reading the profile it wrote. But the corrupt `decisions.json` reached origin because the
standing rule says *parse it out of HEAD* and does not say *when*, so it got done after the push.
**Put the check before the irreversible step, not after it.**
