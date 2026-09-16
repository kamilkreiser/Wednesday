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

1. ~~**KAM — Full Disk Access**~~ — **CLOSED 2026-09-16 20:45. Granted, measured, card marked
   delivered.** Kam added the row at 20:33: *"it was not there. now added"* — it had been ABSENT,
   not switched off, which is why six days of "ruled grant" never took effect. Measured, not
   assumed: the isolated launchd probe went DENIED → **OK** on all three reads, `chatsync` exits 0
   with 0-byte stderr, and his board reached this seat unaided inside one 60-second cycle.
   **The trap it hid, in case anything like it recurs:** three jobs still returned EX_CONFIG(78)
   *after* the grant, because launchd was holding a STALE in-memory plist while the files on disk
   were already correct — `install_all_jobs.sh` had said "unchanged" and so never reloaded them.
   Booting all nine out and back in fixed it, and `--check` now reports `LOADED-DRIFT` (559090e08).
   *Kept here rather than deleted because the failure mode — a fix that reaches the files and never
   reaches the running system — is the one this seat met three times in one evening.*

1b. **KAM — Full Disk Access for `/bin/bash` on this Mac mini (HISTORICAL — the original entry).**
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

## Later in the same session — Wednesday's two findings against my own commit

She reviewed `56f0a020d` and found two real defects; both are fixed at `316ed56e5`, with the
lesson at `bd667484c`. Verified on this machine before changing anything rather than taken on her
word — both held exactly.

- **F1: the drain was dead code.** `/bin/bash` here is GNU bash **3.2.57**, which accepts only
  INTEGER `read -t` timeouts, so `-t 0.1` failed on its first iteration and drained nothing — and
  my `2>/dev/null` hid the reason. **Remember this for any script in this tree: `#!/bin/bash` on
  macOS is bash 3.2, not 4 or 5.** No associative arrays, no `read -t` fractions, no `${var^^}`.
- **F1's fix needed a second fix, caught by an arm and not by review.** A timed drain on a PIPE
  swallows stdin including the answer: `printf 'yes\n' | gate` DECLINED. Now guarded by `[ -t 0 ]`.
- **F2: never inject, but always BOUND.** Suppressing DEATH on a booting pane removed the injection
  and created a silence — unattended, a pane stuck at "Type yes" waits forever while the rotate log
  says "respawned OK". `monitor.sh` now posts ONE panel line past `BOOT_BOUND_MIN` (5) minutes.
  Note while FDA is ungranted: `chat_sync` is dead, so that panel line reaches Kam only when
  something pushes; the `alerts.log` line always lands.

**The 19:43 event is in this machine's own log, verbatim** — neither seat had cited it, and it
confirms the reconstruction exactly, including that the occupancy guard put up no resistance at all:
```
2026-09-16 19:43:46 [DEATH] wednesday — process exited (title reverted to the hostname on two consecutive checks)
2026-09-16 19:43:47 [monitor] tapped coordinator pane %0 (after 0 held tries): 19:43 [fleet-monitor] WAKE: pane 'wednesday' DEAD — process e…
```
`after 0 held tries` is the part to notice: the guard looks for text at a `❯ ` prompt, a launcher
prompt has no such line, so it read "nothing is happening here" and injected on the first attempt.
One second between the verdict and the keystroke. `2_Project_Files/fleet/cockpit/state/alerts.log`.

**And a failure of mine, because the next seat will be tempted by the same thing:** editing
`monitor.sh` in place while the monitor was running from it **killed the live fleet monitor** and
took its tmux pane with it. Bash reads a script by byte offset. Restored as pane `%5` with
`@cockpit_name fleet-monitor` after running `--once` against the new code. Rule:
pgrep → stop → edit → run once → re-arm.
`learnings/2026-09-16_never-edit-a-bash-script-that-is-currently-running.md`

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

## Kam's 20:22 rulings — one applied, one NOT carried out on purpose

Both taps reached this seat only because Wednesday forwarded them by mail; `chat_sync` was dead, so
`reconcile_rulings.py --apply` found nothing and both cards read `open` locally. Ruled by hand from
her verbatim forward.

- `tuesday-one-launch-on-the-mini` → **launch**. Done; that is this session.
- `tuesday-seat-self-rotate-with-liveness-check` → **rotate-after-verdicts**. **NOT carried out, and
  that is deliberate — do not "finish" it at your next boot.** The card was written before Kam
  stopped this seat on 09-14 and every fact in it has expired. Measured 2026-09-16 20:3x: the three
  HPSM gates are not running (`tmux list-panes -a` = two panes, this seat and the fleet monitor, no
  claude agent processes), session 42 is not running, no GATE VERDICT mail since 2026-09-14 in either
  inbox, and the card's "this seat has been past its context ceiling for hours" described the seat he
  stopped, not this one. Kam was told in one message with all four measurements and an explicit offer
  to restart anyway if he still wants it. **If he says restart, restart; otherwise this ruling is
  answered by events.**

## The daily-note split — census DONE, waiting on Wednesday's commit

Both seats write the same `0_Brain/daily/<date>.md` and it conflicted on rebase tonight. A claim
split is agreed (her: `note_entry.sh` seat-aware; me: boot step 5 in the launcher). **Sequencing is
one-directional and it is the whole risk: she lands hers first and tells me the hash, THEN I change
boot step 5.** Pointing boot step 5 at a directory the resolver does not yet produce creates a stray
note at my next boot.

**The census, measured 2026-09-16 20:2x — do not re-derive it, and note two of her four guesses were
wrong in each direction.** The first sweep is dominated by ~60 hits of *prose inside staged briefs*
quoting daily-note paths as provenance; those are history, not readers. The real code paths are four:

| path | role |
|---|---|
| `tools/note_entry.sh:13` | the only writer of note lines; already fronted by `WED_NOTE_OVERRIDE` |
| `voice/speak.sh:39` | **writes the speech log into that directory** — not on her list |
| `scheduler/close_wednesday.sh:158,241,256` | heaviest: reads, creates from `_template.md`, and at **:241 git-checks a HARDCODED literal path** that will not follow a variable change; fronted by `WEDNESDAY_TEST_NOTE` |
| `fleet/hooks/session_start_compact.sh:13` | prose that re-grounds a COMPACTED seat on "today's `0_Brain/daily/` note" — would send this seat to the Secuura note; not on her list, and new here tonight |
| `Launch_Wednesday.command:555` | boot step 5 — **mine** |

**Do NOT touch:** `daily_receipt.sh`, `shift_change.sh` (contains "daily" zero times),
`dashboard/generate.py` (zero), `dashboard/collect.py` (its only hit is `FREQ=DAILY` in calendar
RRULE expansion). All four were named as readers and none of them is one.

**The cheap seam:** two override variables already sit in front of the default, so a seat-aware
resolver only changes what the default expands to — no call site moves.

## A recurring mechanism worth a guard — raise it with Wednesday

The exec-bit warning came back within the hour, on a file that arrived in a pull:
`2_Project_Files/fleet/tests/doctor_exithint_arms.sh`, tracked at **100644**. That is the same
root cause as the 84 files earlier tonight, with a fresh example: scripts are being **committed**
without the executable bit, so every seat re-fixes it forever and doctor's advice ("chmod +x")
treats a symptom. The durable fix is a pre-commit check that refuses a `*.sh` with a shebang
staged at 100644 — `2_Project_Files/fleet/hooks/pre-commit` already exists and is the natural
home. **It is shared tooling, so propose it to Wednesday rather than adding it unilaterally.**

## 🔇 KNOWN FALSE WAKE — do not spend turns on it

`monitor.sh` reads **"waiting on background subagents" as idle** and wakes the coordinator with
*"likely waiting on Wednesday — check the pane now"*. It fired **three times tonight** on
`Datasec/HPSM` while that agent was running four subagents. An agent whose work is in subagents has an
empty prompt and unchanging pane text — **which is what a productive agent looks like from outside.**

**When this wake lands: look once, and if the pane shows `✻ Waiting for N background agents` or a
spinner, do nothing and move on.** Do not re-verify it every three minutes — that is the exact
activity Kam stopped this seat for on 2026-09-14.

**The second-order risk is the one to care about: a detector that cries wolf gets ignored, and this is
the same wake that would report a genuinely stuck agent.** Tonight HPSM *was* stuck for an hour behind
a typed-unsent line, and that mattered. Reported to Wednesday with the evidence and a suggested
discriminator; **her file, not this seat's to patch.**

## 📌 OWNED BY THIS SEAT, DEADLINE 24 SEPTEMBER — download the published Marketplace packages

**Partner Center stops serving previously published packages after 2026-09-24.** NexusAI has local
copies in `evidence-s62-published-packages/`, but the PUBLISHED ones can only be fetched through
Partner Center — **which this seat can reach and no agent can.** Chrome on this machine is signed into
an account with access, and *Allow JavaScript from Apple Events* is ON (Kam enabled it 2026-09-16), so
the offer and its plan pages are readable from here.

**Route:** offer `c8c0cb53-f392-4340-9fd8-204ca38cb25f` → plan `57be7273-1e64-40e0-a486-443d11e7ff11`
→ Technical configuration → *Previously published packages*.

**Deliberately NOT done overnight**, and the reasoning should survive: eight days of margin, browser
automation against a live publishing console is a poor trade unattended, and if any step needs Kam's
click it is better to ask once while he is awake. **Do it in daylight — and do not let the margin
erode into an emergency; it is a task with a date, not a someday.** NexusAI has been told explicitly
not to spend context on it.

## 🔴 TWO FINDINGS FOR KAM, both carded/boarded 2026-09-16 ~23:45. Neither woke him; reasons recorded.

### F-1 — an anonymous stranger can permanently lock the owner out. **Pre-existing, so LIVE in 2.1.1.**
On a freshly deployed instance that has not finished setup, anyone who can reach the hostname sends
two requests — create an admin user, then mark first-run complete — and afterwards auth is
**"enforced" while no identity provider can sign anyone in**: local login 401, Entra unconfigured,
admin-reset unusable because the template never sets `ADMIN_RESET_KEY`. Survives restart. **Only
recovery is hand-editing settings on the customer's Azure Files share, and nothing shipped says so.**
Measured by the gate 3× on the release head, 1× on `main`.

**Why he was not woken** — state these if challenged, and re-test them if anything changes: no
customers on the listing *by his own word*; a deployment still needs a token we hand over, so the
exposed population is one we control; and the harm is **denial of service to the owner, not
disclosure**. NexusAI is told to report immediately if it finds a deployment that is neither ours nor
accounted for — **that would change the answer.**

**Fix AUTHORISED and running in the candidate** (not a signature class), with the regression test
required to go **RED on today's code first** — a test written against a fix proves the fix compiles,
not that the bug existed. Documenting the recovery path is part of it.
**Card for him: `nexusai-live-listing-lockout-warn-now`** — only the part that is his, whether the
LIVE listing needs a warning before the fixed package lands. Recommended: no change.

### F-3 — the check that has never once run. **This is the night's real finding.**
`session-tools/marketplace-package-build.sh` **exits 141 on EVERY build** (SIGPIPE inside a pipefail
pipe, line 98). **Both submitted MANIFESTs are truncated.** A build with a nonexistent tag, the wrong
registry or a missing element is **indistinguishable from a good one**.

So the dev-registry default did not slip past a check — **it slipped past a check that never completed**,
which is exactly why the manifest recorded `wizard default containerImage = nexusaidevacrfa39…` and
nothing acted on it.

**Three instances tonight, three places:** a manifest that records and never asserts; a preflight that
passes `apiVersion 2099-01-01`; a build script that reports success by exiting 141. NexusAI is told to
make this the **headline** of the certification paper. **The resubmission question is not "is this
package right" but "what would have told us if it weren't".**

### RD-461 — CLOSED, theoretical, on real evidence
697 ticks at `sent=0`, 18 start lines all DRAFT, live mode gated on env vars that are not set, 0
references in the submitted template. A negative proved rather than assumed. Fix stays in the
candidate; its side effect (288 false ERRORs/day polluting the demo's failure signal) is worth fixing
on its own merits.

## 🔴 FIRST THING FOR KAM: "anyone who pays" is impossible on the CURRENT offer type

Card `nexusai-monetisation-model-and-public-registry` is open and is the first thing to put in front
of him. **NexusAI measured that Microsoft does not let a Solution template charge anything, and a
Solution template is what is live.** So his requirement *"anyone who pays can deploy"* cannot happen on
the published offer: today it means *anyone with an Azure subscription*, and a public image removes a
key rather than widening access. Real pay-to-deploy = a different offer model (Container offer on AKS,
SaaS, VM) = re-architecture. A Managed application can only charge a management fee.

**Recommendation on the card (theirs and this seat's):** a new dedicated Standard ACR, anonymous pull,
release images only, digest-pinned, the four credential fields deleted from the wizard. **~US$20/month
= money = his signature class. The push is his too.** Full paper: NexusAI
`5_Project_History/2026-09-16_self-contained-package-options.md`, RD-460.

**Two certification facts found, unresolved, both READ-ONLY until he says otherwise:** Microsoft Learn
says containers are **not supported** for Solution templates — yet 2.1.1 certified; and policy 300.4.7
requires all deployment artifacts in the zip. NexusAI is establishing which is true and drafting, NOT
sending, a question to Partner Center support — **contacting them is external comms and Kam's.**

**Proceeding without him:** the three other non-self-contained items (RD-451 demo probe, mail-triage
default Datasec inboxes, "unless Datasec advises" tooltips — defects against a requirement already
given), the tier-1 gate on 1470e18, and the rest of the fix order. **Do not create the registry "ready
for approval" — creating it IS the spend.**

**⏳ 24 September: Partner Center stops serving previously published packages.** Eight days. Downloading
old packages as evidence needs no permission and cannot be undone later.

## ✅ RESOLVED 23:2x — the typed-unsent line at HPSM's prompt (pane %7)

`yes, start it now with subagents` — typed, never sent. **Not enacted by this seat and it must not
be.** It cannot be attributed: possibly Kam with a swallowed Enter, possibly Claude Code's own
suggested text. Pane text is not a channel of record in either direction
(learnings: ghost text / pane prompts contain Claude's own suggestions).

**How it was resolved, and the reasoning is the reusable part.** It sat for over an hour with HPSM
idle, and it also blocked tapping — `cockpit.sh say` REFUSES an occupied prompt, so the pane could be
MAILED but not WOKEN. The line was **CLEARED (Ctrl-U), never sent**, and the pane then tapped at the
mail. So nothing unattributable was enacted, and the instruction HPSM acted on is the mailed one with
provenance. Kam was told, since the typing may have been his.

**The rule for next time:** an occupied prompt is a *stuck agent*, not just untidiness — it silently
disables the wake channel. Clear it and point at mail; never press Enter on text you cannot attribute,
and never discard it silently either — say that you did, to whoever might have typed it.

## 🌙 OVERNIGHT POSTURE — Kam signed off ~22:50 with *"good luck with getting the project submission ready"*

He has handed the resubmission to this seat. **That is permission to keep working, not permission to
widen.** Read the two lines below before anything else.

**WHAT PROCEEDS WITHOUT HIM.** Everything up to, but not including, his signature classes: the tier-1
gate and its verdict; NexusAI's fix order; the options-and-recommendation work on the self-contained
requirement; package changes in a NEW candidate; HPSM's remaining `:441` edit; both clarification
files. Usage is not a constraint — this account's cut is 95 and we are at ~70.

**WHAT STOPS AND WAITS, no matter how ready it looks.** A registry **push** (his own 09-12 ruling:
the registry is one HE names and the push is his signature class); any **resubmission** to Partner
Center; production; money; external comms; anything irreversible. **The self-contained fix cannot be
finished without him** — it ends at "here are the options, here is the recommendation". Do not let a
good night's work talk itself into the last step.

**THE REQUIREMENT THAT NOW GOVERNS THE WHOLE PACKAGE** (Kam, ~22:40, verbatim): *"the zip needs to be
self contained.  we will not give people access to the repo or keys.  the intended model is that
anyone who pays can deploy."* So `acrUsername`/`acrPassword` are **defects, not configuration**, and
the test applies to the WHOLE package — repo URLs, keys, manual steps, documents only we hold.

**HOW TO WORK, because he corrected this seat on it tonight** (~22:40): *"each project agent is very
capable and should load with the project files … work with them as Subject matter experts. Checking
yourself is great but you should not do what they should."* **Ask the agent, verify the answer, carry
it. Do not go and measure inside their project yourself** — this seat did exactly that with the
marketplace zip and got a worse answer than the agent did, then had to correct Kam.

## LIVE STATE at 2026-09-16 22:2x — both agents delivered; here is what is open

**HPSM (pane %7)** — ALL ASSIGNED WORK DONE. The `:441` edit landed at `543dc4e`
(*"flag to Tuesday/Kam BEFORE creating"*), with `:442` kept as history exactly as ruled, and counts
carrying a negative control (`Wednesday/Kam` = 0). It is now seeding its clarification file with
subagents, bounded, and will send the path and entry count when it stops. **Nothing is owed to it by
this seat.** Its own backlog — 26 open Jira tickets, none touched in 3 days — is folded into its next
plan, not tonight's work.

Earlier the same session, also done and verified: pause banner removed with the subagent standing rule kept,
both `wednesday-agent@` lines fixed, both routing tags accepted, commit `fa73832`. It caught two of
this seat's errors (line 219 was 220; the addendum asserted a fact about ITS launcher taken from a
file in OUR tree). **Owes:** the `:441` edit (Wednesday→Tuesday on the live billing-flag line; `:442`
stays as history) and its hash. Rule given for its clarification file: **change instructions, preserve
history.**

**NexusAI (pane %6)** — DONE: RD-399 unpaused, `CLARIFICATIONS.md` created with 37 entries and wired
into its boot (RD-459), and it answered **"not blocked"** on the HPSM merge-queue note while correctly
declining to assert HPSM's queue state, which is outside its scope. **GO given** on the tier-1 gate for
`mkt-round4-onto-main-s60 @ 1470e18`. **Owes:** that gate's verdict and Kam's review of what remains.

**The gate item added, and it is the lesson of the whole evening:** the 09-15 build manifest RECORDED
`wizard default containerImage = nexusaidevacrfa39...` at build time. The defect that made the offer
undeployable was in our own evidence and shipped anyway. **A fact written into evidence that nothing
asserts on is not a check.** Also flagged: the 2.1.1 package ships a 2.1.0 image tag, and nothing
checks that either.

**KAM SUBMITTED 2.1.1** (his words to NexusAI, their C-24). That package was already among the ten
checked — it points at the same closed dev registry. **So the answer is confirmed against the real
submission, not inferred, and Partner Center is no longer needed for it.**

**PENDING KAM:** (1) the registry name — still the only blocker on a correct package; (2) Azure
device-code login `P66F33WMH` as `kreiser.org@me.com`, still waiting, for the customer-path deploy;
(3) Chrome's *Allow JavaScript from Apple Events* still reports OFF, so page content is unreadable
from this seat; Screen Recording needs a restart and he cannot do it yet.

## 🔴 NEXUSAI — MEASURED: the submitted offer CANNOT be deployed by a customer

**Answered, do not re-derive.** `marketplace-submission-2026-09-15/NexusAI_plan-managed-ai_2.1.0_8f50eeb.zip`
defaults every customer to `nexusaidevacrfa39.azurecr.io/nexusai:2.1.0` (tooltip: "leave the default").
That registry **refuses anonymous clients**: an `oauth2/token` request scoped `repository:nexusai:pull`
with no credentials returns `UNAUTHORIZED — authentication required`. **Positive control:** the same
method against `mcr.microsoft.com` returns HTTP 200. So the deployment dies at image pull in any
customer tenant. **Kam's customer-path test tomorrow will fail at exactly that point** — now a
confirmation, not a discovery.

**Two of this seat's own earlier claims were WRONG and are corrected:** the "May 2.0.0 build with none
of rounds 2-4" is out of date (the package ships 2.1.0 at its own commit), and
`myregistry.azurecr.io/nexusai:1.3.0` in mainTemplate is an EXAMPLE inside a `metadata.description`,
not a defect. **The content was fine; the packaging was not.**

**CONFIRMED ACROSS ALL TEN PACKAGES (2026-09-16 22:0x), not just the submitted one:** every NexusAI
plan zip on this drive — every commit, 2.0.0 through 2.1.1 — defaults the wizard to
`nexusaidevacrfa39.azurecr.io`. Not one points elsewhere. **A third party cannot deploy any of them.**
No self-service workaround: a customer can retype the image field but has no access to the registry
and no copy of the image. **Limit on the claim, stated to Kam:** Partner Center is unreadable from
this seat, so the LIVE listing was not read — the answer only changes if the listing carries a package
absent from this drive, and the 09-15 manifest (which records the dev default at build time and says
nothing had been uploaded) makes that unlikely. **Asked Kam for Partner Center access to close that
gap properly rather than by inference.**

**PROCESS FINDING for the resubmission:** the build manifest RECORDED `wizard default containerImage =
nexusaidevacrfa39...` at build time. It was visible in our own evidence and shipped anyway — a gate we
did not have. It belongs in the pre-submission checks.

**THE ONE BLOCKER, with Kam:** which registry a customer pulls from. His 09-12 ruling makes it his to
name and the push his signature class; he has never named it. **Nothing becomes client-ready until he does.**

**MANDATE WIDENED (Kam ~21:50):** *"review the whole project and fix everything that needs fixing to
make the product as good as possible"*; a second submission only *"when it is 100% ready"*. This
SUPERSEDES the earlier "review and STOP". Bar given to the agent: **would a customer who has never met
us succeed, unaided, from the listing alone.** Told NOT to submit and NOT to modify the submitted
package — Kam deploys that exact artefact tomorrow and it is evidence now.

**INTENDED, NOT A BUG (Kam ~21:58):** *"the deployed site should work until the client finishes setting
up the entra group to authenticate against. until then, anyone can access the site."* **Do not let any
agent gate, password or IP-restrict that window** — access policy is Kam's. NexusAI is measuring how
long it stays open, how guessable the hostname is, what is reachable while it is open, and whether the
UI and docs SAY so; reporting, not acting. If they find reachable customer data, an exposed key or a
pre-setup admin action, that stops and comes to Kam.

## STANDING, fleet-wide (Kam, 2026-09-16 ~22:00) — settled decisions get WRITTEN DOWN by the agent

*"the agent knows. get the agent to make these kinds of notes so its not something we keep coming back
to. Maybe an agent generated project definition / clarification file"* — said after this seat briefed
NexusAI on a fact it already held.

Both Datasec agents now carry it as a standing duty: an agent-written clarification file in their own
tree (`1_Project_Definition/CLARIFICATIONS.md` suggested, path theirs). **The coordinator does not
write or edit it** — it has to live in their tree to be read at their boot. Contents: intended-but-
looks-like-a-bug first, settled decisions including what was decided against, Kam's rulings with date
and words, deliberate limitations, and already-answered questions. Provenance on every entry;
supersede rather than delete; keep it pruned. Open questions stay tickets; no secrets.

**The coordinator half of this rule:** check what an agent already knows before briefing it, and when
a question surfaces a second time, get it written down rather than answering it again. Ask for the
file and the entry, not for the answer.

## USAGE — this seat has NO 40% cap; that was Wednesday's

Kam, 2026-09-16 21:3x: *"the 40% was only for wednesday and Secuura projects. you are on a different
account and do not have that constraint."* and *"the message was on the wednesday chat board not
yours."* `fleet/USAGE_STOP` (40) is hers. This seat reads `fleet/USAGE_STOP.tuesday` = **95**, on his 2026-09-16 21:40 instruction
*"bump yours to 95%"* (it was briefly 90, the fleet default, before he said so). **The seats are on separate
accounts; usage is never shared** — measured at the time: Wednesday 7%, Tuesday 70%.

## TOMORROW'S DATASEC PICTURE — assembled 2026-09-16 20:4x so it is not re-derived

Nothing is running on this machine: `tmux list-panes -a` = this seat and the fleet monitor, no agent
sessions. Nothing was launched tonight and that was deliberate — Kam's autostart grant
(2026-08-12) is for the **morning** sweep, and his 20:23 note said *"i will comment on this
tomorrow. we have new actions and work to do"*. Launching at 20:45 would have been scope nobody gave.

- **All Datasec projects are reachable** at `/Volumes/KK_T9_External_HDD/!CODING/Datasec/` — ATTIO,
  Commercial Readiness, CypherKey, Feedback_System, HPAM, HPSM, Lead_Bot, Marketing_Collateral,
  myPKI, NexusAI, RESEARCH. DevMASTER is not mounted here and its absence is not a missing project.
- **HPSM is the live one and the only open Datasec card.** `hpsm-composer-monday-review-scope`
  is still `open`, and Kam said at 20:23 he comments on it tomorrow — **do not re-ask it, and do not
  rule it.** Its own default already records his 15:24:26 supersede: *"build the full website and
  fully functioning engine"*, read as the remaining MVP A build (architecture 6.1-6.3 — WP3 rules
  engine, WP4 API, WP5 web UI screens 1-10, WP6 manifest + renderers), each through its tier-1 gate,
  local-first, nothing HP-facing, no deploys; commissioned to HPSM session 39.
- **HPSM's newest history entry is session 47 (2026-09-14)**: the full release — Composer `main` at
  `7a477400f9b315f485b7257f5cb8bde78403943d`, 16 merges from `b9c6464`, both live stacks purged.
  Sessions 39 and 47 are both referenced; **reconcile which is current before briefing anyone.**
- NexusAI and HPAM have no `5_Project_History/history.md` on this drive — unmeasured rather than
  inactive. Check their boards before assuming either way.

**The morning grant applies at the next MORNING boot:** sweep Secuura/Blockchain · Datasec/NexusAI ·
Datasec/Vision read-only (skip myPKI, CypherKey, Lead_Bot), launch and brief where there are
agent-actionable tickets, no per-morning confirmation needed. Signature classes still pause for Kam.

## SCOPE — unchanged

Datasec only (Kam, 2026-09-09: *"you will work on ONLY datasec projects unless otherwise
instructed"*). Secuura and general belong to Wednesday on the Studio. Datasec projects live at
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/` — DevMASTER is not mounted on this machine and its
absence is not a missing project. Cross-seat mail to Wednesday is **coordination only**: never
Datasec code, findings, tickets or credentials.
