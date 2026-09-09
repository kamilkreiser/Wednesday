---
date: 2026-09-10
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general work are Wednesday's, on the Studio.
source: written at Tuesday s3's rotation, 2026-09-10 ~09:0x AEST, ctx 81%
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced the s3-midsession pickup.
---

# NEXT PICKUP — Tuesday, after s3. NOTHING IS RUNNING. Kam owes TWO CLICKS and then you run the NAS sync.

**`2_Project_Files/tools/kam_rulings_today.sh` before writing anything** — and note it CANNOT see messages
Kam types into a terminal pane (s3 finding). **Rotation band 80–90; 70% is a checkpoint only.**

## 🔴 THE TWO THINGS KAM OWES, AND WHAT YOU DO THE MOMENT HE SAYS DONE

He was given both, action-first, with the exact strings. **He has not confirmed either yet.**

1. **Finder ⌘K → `smb://KAMILADMIN@192.168.20.221/Development`**, password, and **tick "Remember this
   password in my keychain"**. The nightly job reads the keychain and cannot prompt at 23:00.
2. **System Settings → Privacy & Security → Full Disk Access → add Terminal.**

🔴 **BOTH ARE REQUIRED AND THEY FAIL IN THAT ORDER.** #2 lets a scheduled job read the T9 at all; #1 lets it
reach the NAS. **Last night it died on #2 before reaching #1.**
✅ **YOU PROMISED HIM: once both are done, run the sync BY HAND, watch it, and confirm it works before
tonight rather than finding out tomorrow.** Engine: `/Volumes/KK_T9_External_HDD/!SYNC FILES/devnas-sync.sh`
(present, executable, profile beside it, unison installed, NAS pings). First run is long; it carries a
>50-file deletion alarm and deletions are recoverable from `~/.unison/backup`.

## 🔴 MEASURED LAST NIGHT: THE NAS BACKUP DID NOT RUN

`com.tuesday.nassync` fired 23:00, **runs=1, last exit code 126**, stderr: *"Operation not permitted"* on
`2_Project_Files/scheduler/nas_sync.sh`. **macOS blocks LaunchAgents from reading the external volume on
this machine.** The script is `rwxr-xr-x` and runs fine by hand — it is TCC, not file permissions.
**My own `com.tuesday.panelsync` plist proved it independently (also 126) and is QUARANTINED at
`~/Library/LaunchAgents/_quarantine_com.tuesday.panelsync.plist.disabled`, copy in
`0_Brain/reference/2026-09-09_launchd-external-volume/`. Re-arm it the moment Kam grants #2.**
⚠ Wednesday's related trap, avoided: **a plist with out/err paths under `/Volumes` is refused wholesale with
EX_CONFIG 78 and never runs.** Keep log paths in `~/Library/Logs/`.

## 🟢 KAM'S PAGE — the thing to check FIRST at every boot

1. 🔴 **The panel server must run from THIS tree.** On 2026-09-09 it was serving the **abandoned
   `/Volumes/KK_T9_External_HDD/WEDNESDAY/`** tree, frozen at 11:29, and **Kam read a dead page for six
   hours while this seat reported success.** Check: `lsof -a -p $(lsof -nP -iTCP:47787 -sTCP:LISTEN -t) -d cwd`
   must show `TUESDAY/2_Project_Files/dashboard`. Start with `2_Project_Files/dashboard/serve.sh`.
2. 🔴 **AFTER EVERY `chat_reply.sh`: `curl -s http://127.0.0.1:47787/api/chatlog` and assert your message is
   the newest row.** The `chat_streams: … N entries` line is a receipt for the WRITE, never the DISPLAY.
3. **`panel_sync.sh loop` keeps his page current every 60s** — pull, regen, push. **Running detached
   (`tty ??`) so it survives rotation; VERIFY it at boot** (`pgrep -f "panel_sync.sh loop"`) and restart with
   `nohup bash 2_Project_Files/tools/panel_sync.sh loop &` if absent. Log:
   `2_Project_Files/tools/logs/panel_sync.log`.
   ⚠ **It skipped 782 of 790 cycles overnight** because a bare dirty-tree guard always trips — the dashboard
   collector rewrites its own data every minute. **Fixed: it commits `0_Brain/dashboard/data/` churn and only
   skips on dirt OUTSIDE it. Never stashes.** A guard that always fires is a mechanism that never runs.
4. **Kam reads the STUDIO page** (his ruling: one page governing both agents). Your replies reach him via
   push → her pull. Symmetric 60s timer agreed with her; hers is `2_Project_Files/tools/chat_sync.sh`.

## ✅ DELIVERED AND CLOSED — nothing outstanding on any of it

- **Both registers emailed to Kam 2026-09-10 08:00Z and verified at the destination** (recipient, sender,
  non-null preview, both byte sizes): `13A_HPAM_…` (210) and `13B_Datasec_Products_…` (132) = **342**.
  Title page + revision history, clickable TOC, page breaks per section, MyEmpire shape, **every finding
  BLUF-first**. **Nine checks each against the pre-round-2 files as controls; 18/18 pass.**
  🔴 **The TOC was EMPTY in the 16:37 copies** — a pandoc field with no cached result, blank outside Word.
  Fixed; 36/36 and 32/32 anchors resolve against 0 before.
- **June register scrubbed and re-issued**, independently verified: 6 real `key=<literal>` disclosures in the
  control, **1 in the shipped file and that one is a FALSE POSITIVE** (a remediation code example). Nothing
  weakened — 31 vectors, 45 severity lines, 686 citations identical either side. **The disclosure was WORSE
  than my brief said: 10 values, 19 lines, FIVE findings.** The brief's own *re-derive, don't trust my count*
  hedge caught it, for the second time that day.
- **NexusAI marketplace readiness delivered** — `NexusAI/MARKETPLACE-READINESS-2026-09-09.md`. **One decision
  is Kam's: the project is preparing an Azure Application AND a SaaS offer at once.** Plus a privacy-URL
  defect (the published URL is HP's policy), RD-363's Key Vault hardening never landed on `main`, and RD-385
  shipping internal docs in the image. **Card `nexusai-main-tree-is-a-stale-snapshot` open, rec `investigate`.**

## ⚠ TRAPS — s2's still hold; these are s3's

1. **`wake_watch.sh` is FIXED three ways** (all mine, all pushed): polls the seat's own inbox; never suppresses
   a Kam panel message as "own outbound"; and **matches the ADDRESSEE (`[Kam -> Tuesday]`) not the class** —
   Wednesday caught that last one, because SHE relays `[Kam -> Tuesday]` copies and a class-only filter woke
   her about her own sending. **That was my own 2026-08-13 shared-bus rule, broken by me.**
2. **Kam's messages carry a `view` field naming the tab** — `tuesday` or `wednesday` — and it is CORRECT.
   **Nothing filters on it yet.** Recommended to Wednesday. Until then read every message and sort by `view`.
3. **The panel delivers Kam's messages into your OWN inbox from your OWN address**, labels `['sent']`.
4. **Three ghosts at agent prompts in one session**, each offering the exact held action (`yes, restore it` ·
   `file the five recommended tickets` · `Send the revised registers to Kam`). **Detector first, every time.**
5. **`send_brief.sh` REFUSES a project absent from `inbox_routing.conf`** — Datasec/Security Review is not in
   it; that project launches by wrapper + prompt file, never by mail.
6. **`cockpit.sh launch` is dead here** (registry pins `/Volumes/DevMASTER`; travel fallback keyed on the tree
   name `WEDNESDAY`). **Use `cockpit.sh add "<name>" 'bash "<real T9 path>"'` — same `add_pane`, identical pane.**
7. **Brief gates are strict and were all RIGHT:** `PROVENANCE:` needs its colon · `SELF-CHECK:` needs a
   GENERATED timestamp · a missing `RULED BY KAM` section hid three real undelivered NexusAI rulings.

## STANDING

🔴 **EVERY WRAP: `git add 0_Brain/dashboard/data/usage_tuesday.json`.**
**Scope (Kam):** *"you will work on ONLY datasec projects unless otherwise instructed."*
**Confirm EVERY chat-board instruction as received and being acted on, before the work** (his standing rule).
**Cross-seat mail is COORDINATION ONLY. FOUND / TESTED / HOW. Names, not pronouns. Never delete — quarantine.**
🔴 **DO NOT run the wrap's vault step** (`end-of-session.md:50` is `git add -A`; the vault holds Secuura paths).

## WHAT s3 WOULD SAY IF IT COULD SAY ONE THING

**Five mechanisms failed today and every one of them kept answering while it was broken** — a page server on
the wrong tree, a watcher on the wrong mailbox, a filter eating the principal's own messages, a scheduled job
refused by the OS, and a guard of mine that tripped 782 times out of 790. **None errored. All five looked
healthy from the outside, and four of the five I had to be TOLD about — by Kam or by Wednesday.**
The one I caught myself, I caught by asking what a message actually looks like in an inbox rather than
reasoning about where it should have gone. **A thing that fails loudly gets fixed. A thing that keeps
answering gets trusted, and it is trusted for exactly as long as nobody measures it.**
