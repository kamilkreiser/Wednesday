---
date: 2026-09-16
seat: tuesday (Mac mini, /Volumes/KK_T9_External_HDD/TUESDAY)
type: pickup
status: live
supersedes: the 2026-09-14 pickup, kept verbatim at NEXT-PICKUP-TUESDAY.md.pre-s1-wholesale
---

# NEXT PICKUP — Tuesday

**Read this first, before anything you would otherwise choose.** Its OWED section is the session's
first work. Until 2026-09-16 no boot step named a pickup file for this seat, which is exactly why an
instruction given to Tuesday used to die at her next rotation while the same instruction to Wednesday
survived. Wednesday read hers out of habit; a habit is not a mechanism. The mechanism now exists —
use it.

**Naming, so the next seat does not hunt:** this seat's pickup is `NEXT-PICKUP-TUESDAY.md`.
`NEXT-PICKUP.md` in the same folder is **Wednesday's** and is updated by her seat on the Studio.
Wednesday's 2026-09-16 mail called mine "NEXT-PICKUP.md (your seat's own copy)", which is ambiguous
in a shared repo where both files exist. Flagged to her in the 20:0x STATUS mail.

## OWED — actions with a named owner, carried until done or withdrawn

1. **KAM — Full Disk Access for `/bin/bash` on this Mac mini. This is the live blocker.**
   He ruled `grant` on card `tuesday-mac-mini-scheduler-full-disk-access` on **2026-09-11 15:25** and
   it was never applied. Do **not** re-card it: the decision is made, the gap is delivery. Asked on
   the panel 2026-09-16 20:06, verified at origin.
   *Measured here, not inferred:* `com.tuesday.chatsync` exits **126** with
   `/bin/bash: …/2_Project_Files/tools/chat_sync.sh: Operation not permitted`. Same signature in the
   historical logs for wake, close, shiftchange and nassync. It is TCC by elimination — the same file,
   read by the same `/bin/bash`, succeeds from a Terminal-descended shell and fails from launchd, and
   a missing volume would give ENOENT, not EPERM.
   *Consequence to lead with when you raise it:* `chat_sync` is the 60-second job that puts this
   seat's replies on Kam's page. **Until the grant lands he cannot see this seat on the panel at
   all**, and every reply must be pushed to origin by hand. All nine scheduled jobs are dead the same
   way, so every 05:30 / 06:00 / 23:00 ritual silently does not fire.
   *When he says it is done:* kickstart one job, read its `.err`, and only then tell Wednesday to mark
   his card delivered. A clean log is the proof; his word that he clicked it is not.

2. **KAM — the lapsed week-scoped grants.** MERGE + DEPLOY + PRODUCTION (2026-09-07 09:40, 11:09,
   12:07, "for the rest of the week") **lapsed after 2026-09-13**. Asked 20:06, unanswered.
   **Work under protocol v1.3 scope until he answers in his own words.** Do not carry the latitude
   forward by inference, and do not read his restarting this seat as an extension of anything.

2a. **Do NOT card the lapsed grants — the prior-ruling gate refused it, and it was right.**
   Attempted 2026-09-16 20:1x as `tuesday-lapsed-week-grants-extend-or-not`; `decision_queue.sh add`
   refused and surfaced, among others, Kam's own panel line of **2026-09-14 21:56**: *"If you want me
   to merge anything, make sure it's ready and provide me the link so I can merge it."* That is a
   standing posture on the merge half of the question — he wants the link and merges it himself — so
   asking him to "extend the merge grant" would have been asking him to re-rule something he had
   already written on. The deploy and production halves remain genuinely open; if you ever raise them,
   raise those two alone and never as a bundle. Nothing is blocked on this.

3. **KAM — the launcher still pins `opus` only.** His 2026-09-06 override was for one week and has
   expired. Asked 20:06. Do not change the launcher unasked; restoring
   `--model fable --fallback-model opus` is his call, not a tidy-up.

4. **KAM — two installs only he can do on this machine:** Matilda Premium (Spoken Content) and
   Tailscale.app. Listed to him 20:06, explicitly not urgent.

5. **WEDNESDAY — the next-boot preflight output.** Her 2026-09-16 mail asks for every warning from
   the NEXT boot, verbatim, as the proof that the repairs hold. That boot has not happened yet. Send
   it when you rotate. It was flagged as outstanding in the STATUS mail rather than quietly dropped.

## DONE this session (2026-09-16, ~19:50-20:10) — so you do not redo it

Pushed at `56f0a020d`. Doctor went from **11 warnings to 7**; all seven remaining are Kam's or are
facts about this machine (DevMASTER not mounted is expected on the mini and needs no action).

- **All nine launchd plist templates hardcoded `/Users/kam_code/Library/Logs/wednesday_*`** — the
  Studio's home, which does not exist here. Every job loaded, died with EX_CONFIG(78) before running a
  line, and wrote no log. `--check` said "9 current, 0 missing" over nine jobs that could not run.
  Fixed at source with an `@HOME@` placeholder alongside `@PROJECT_DIR@` and `@SEAT@`; renders
  byte-identical on the Studio. **Fixing 78 is what made the 126 above readable** — while the jobs died
  one step earlier with stderr going nowhere, the FDA failure could not appear anywhere.
- **The two boot bugs.** (1) `doctor.sh --quiet` ran at line 281 and `render_claude_settings.py` at
  304, so a fresh seat hard-failed one step before the fix that would have passed it. Render now sits
  before the gate. (2) `monitor.sh` declared a pane DEAD on a hostname title — which is exactly what a
  pane looks like while the launcher waits at a prompt — and send-keys'd its wake text in, where
  `read -n 1` took the "1" of "19:43" as the answer and killed the boot. Now guarded by
  `pane_is_booting()` (the process table, not the title) at both the death branch and the injection,
  and the prompt requires a typed `yes` + Enter after draining buffered input.
- **84 scripts' exec bits.** Git recorded 83 of them at mode 100644, so "restore from git" was a
  no-op; the **index** mode is now 755 so the bit travels.
- **Ledger rule 3c.** 12 rows older than 2026-09-13 moved verbatim into `_ledger_archive.md`.
  Conservation asserted: 940 rows before, 940 after. 51 KB → 25 KB.
- Repo pulled and current; `.gitignore` covers the renderer's own backups.

## TRAPS this session paid for — check these before you trust an instrument

- **A green check can sit over a dead mechanism.** `install_all_jobs.sh --check` reported "9 current,
  0 missing" while all nine were unrunnable, and then reported "0 current, 9 missing" once they had
  been hand-patched into a *working* state. The checker compared the live plist to the template and
  had no opinion about whether anything ran. When a check and reality disagree, find out which one is
  measuring the thing you care about.
- **`behind 0` can be a false zero.** A cached `origin/main` equal to HEAD reports zero. Fetch first.
- **The local chat API proves nothing about what Kam sees.** He reads the panel on the **Mac Studio**.
  The destination is `origin`: verify with
  `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`. With `chat_sync` dead (item 1),
  nothing reaches him unless this seat commits and pushes.
- **`kam_rulings_today.sh` shows only this seat's tab.** At 20:03 it showed 0 of 54 for `view=tuesday`
  — every message that day was typed on Wednesday's tab. Zero here means "he did not type to this
  seat", never "he said nothing".
- **The `no_rm` hook refuses deletes outside the scratchpad.** Quarantine with `mv` instead; it
  refused a real `rm` of my own backups mid-session, which is the guard working.
- **The boot digest is 465 KB (~115 K tokens) across 173 lesson files**, and the by-tier digest is
  barely smaller than the plain one because 135 of 173 files are tier W. Reading it whole at boot
  would put a seat past 50% before it does anything. Raised as a structural question, not worked
  around — see the daily note.

## SCOPE — unchanged

Datasec only (Kam, 2026-09-09: *"you will work on ONLY datasec projects unless otherwise
instructed"*). Secuura and general belong to Wednesday on the Studio. Datasec projects live at
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/` — DevMASTER is not mounted on this machine and its
absence is not a missing project. Cross-seat mail to Wednesday is **coordination only**: never
Datasec code, findings, tickets or credentials.
