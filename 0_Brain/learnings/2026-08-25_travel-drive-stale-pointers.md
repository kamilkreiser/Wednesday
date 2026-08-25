---
date: 2026-08-25
type: correction
source: "First travel-drive session (KK_DEV_Local on the laptop, DevMASTER unmounted). Kam: 'I can see from the secuura agent that github was dead... make notes so next sync avoids these issues please.' Found live: s66's git dead at boot; cockpit launch refused; two dashboard surfaces rotted."
status: live
supersedes: ""
---

# A drive sync copies files, not pointers — enumerate the absolute paths before first launch on the other machine

**The lesson:** the 2026-08-25 sync/rsync carried EVERYTHING correctly — every
key, every .env, every credential worked on the travel drive (proven: Linear ×2,
Jira ×3, AgentMail, dashboard, and two projects' deploy keys authenticated).
What broke was every place an ABSOLUTE PATH to the old volume was stored in
state that travels: the sync faithfully copies the stale pointer along with the
valid thing it points at. "The logins were not copied" is the wrong model; "the
pointers came along frozen" is the right one.

**The four instances from day one (2026-08-25):**
1. **Per-project repo `core.sshCommand`** — carries the launching drive's
   absolute key path inside `2_Project_Files/.git/config`. Measured across the
   travel drive: 6 repos pointing at /Volumes/DevMASTER (unmounted), 2 at
   /Volumes/Development (a drive gone since ~May — those projects never
   launched since, so nothing ever healed them). Most launchers self-heal
   (self-locating PROJECT_DIR, rewrite the pointer each launch — verified in
   NexusAI's); **Secuura's refresh is CONDITIONAL** (keychain seeded or
   SECUURA_ALLOW_ONDISK_KEY=1), so its s66 booted with dead git and repointed
   by hand. Its preflight remedy text also names a `~/.ssh/` path that only
   exists on the Studio.
2. **`fleet/cockpit/launchers.conf`** — hardcoded /Volumes/DevMASTER launcher
   paths; `cockpit.sh launch` refused. FIXED PERMANENTLY: cockpit.sh now falls
   back to the running drive's copy (SCRIPT_DIR-derived root swap; both
   branches exercised before use).
3. **Hardcoded watch-list in `dashboard/collect.py`** — not a path but the
   same rot class: facts frozen in code, rewritten over live data every cycle.
   Two of three flags were weeks dead (KS-480 consent resolved 08-06; the
   Datasec calendar feed it was "waiting" for was live and serving events).
4. **`tickets_feed()`'s strict heading regex** — cards' evolving convention
   (`**Open / next (refreshed …):**`) silently rendered the two MOST ACTIVE
   projects as empty tiles. A parser contract is a pointer too.

**How to apply — the pre-travel / post-sync checklist (PORTABILITY.md item 18):**
1. **Before travel:** run Sync All Drives + the additive rsync (modes!), then
   verify content at the destination (verify-the-chain).
2. **At first boot on the other machine:** doctor.sh now runs a
   `travel-pointers` check — it sweeps every project repo's `core.sshCommand`
   and warns on any pointer to a path that does not exist on THIS machine.
   Warnings are routed, not worked around: the project's own launcher heals it
   at ITS next launch (self-locating), or its agent repoints repo-locally
   (s66's pattern). Wednesday never edits another project's repo.
3. **Secuura specifically:** its launcher needs the keychain seeded or
   `SECUURA_ALLOW_ONDISK_KEY=1` exported to refresh the pointer — flag it to
   the session brief when launching Secuura away from the Studio (or Kam
   ok's making its refresh unconditional like the others — his call, their
   launcher).
4. **The general test when adding any new mechanism:** "what absolute path am
   I storing, and what happens when this file wakes up on a different
   volume?" Prefer self-locating derivation (SCRIPT_DIR/PROJECT_DIR) over
   stored absolutes; where an absolute is unavoidable, add it to the doctor
   sweep the same session (gitignore-at-creation discipline, pointed at
   paths).

**Addendum, same day (evening): the laptop SLEEPS, and sleep kills agent turns
mid-response.** s66's wrap turn died TWICE to "Your computer went to sleep
mid-response" (one ~5-hour lid-closed gap at the conference, one shorter). The
Studio never sleeps; the laptop does by default. **Rule: any fleet run on the
laptop gets `caffeinate -dims` armed for its expected duration in the same
action as the launch** — and a dead turn's recovery is the 08-24 pattern:
re-verify what the dead turn wrote, mirror mail + tap to resume.

**What did NOT break, recorded so the model stays honest:** keys (0600 modes
held via the rsync), .env files, per-project gh/az config dirs, the WEDNESDAY
repo itself (launcher refreshes its pointer unconditionally), boards, mail,
dashboard, watcher, voice (fallback chain worked as designed).

**Related:** [[2026-08-25_one-drive-devmaster-is-master]] (the relocation this
is the day-two lesson of), [[2026-08-05_identities-float-verify-always]]
(machine state is a floating pointer — this is the same law for volumes),
[[2026-08-13_headline-must-match-the-operative-case]] (instance 4 is its
parser costume), [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (why
this file comes with a doctor check, not just advice)
