---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 12:0x by s151
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 12:0x Tuesday. Fleet quiet. Kam is mid-commission on the two-agent fleet.

## 🔴 FIRST, IN THIS ORDER
1. `2_Project_Files/tools/kam_rulings_today.sh` — settle its stale warning by PULLING and re-running.
2. `2_Project_Files/tools/sync_kam_rulings.sh --dry-run` then `--apply`. His panel rulings still do
   not write themselves into `decisions.json`.
3. `0_Brain/fleet/claims/` — read the other seat's file; write only `claims_studio.md`.
4. **NEW today — before ANY write to `0_Brain/dashboard/data/`:**
   `. 2_Project_Files/tools/_store_guard.sh; guard_data_dir <the data dir>`.
   **Both irreplaceable files were corrupted today** (`decisions.json` by the laptop, `chat_log.json`
   by THIS seat) and neither errored. **Never pipe a pull's output to /dev/null.**

## THE LIVE COMMISSION — Kam's two-agent fleet
Two documents, **nothing built**:
`1_Project_Definition/Architecture/2026-09-08_two-machine-fleet-and-one-shared-panel.md`
`1_Project_Definition/Architecture/2026-09-08_two-agent-fleet-implementation-plan.md`

**RULED by Kam:** the Datasec agent is **TUESDAY** (11:56). One brain, two ledgers, two inboxes,
one panel with a WEDNESDAY | TUESDAY toggle. Wednesday's contrary recommendation was withdrawn.

**MEASURED and settled — do not re-derive:**
- **Tailscale mesh access has been serving this dashboard since 2026-08-20.** It is NOT new work.
  (Wednesday told Kam it was "an evening's work"; corrected, ledger row filed.)
- **The new-Mac run-sheet exists and was exercised end to end 2026-09-02** (PORTABILITY.md).
- 🔴 **`CLAUDE_CONFIG_DIR` gives a genuinely SEPARATE auth namespace — TESTED, not assumed.**
  `CLAUDE_CONFIG_DIR=<scratch> claude -p …` returned **`Not logged in · Please run /login`** and
  built its own `.claude.json`/`projects`/`sessions`. Credentials live in the **Keychain** under
  `Claude Code-credentials-<hash of the config dir>`. **That is the answer to Kam's travel
  question:** each launcher exports its own on-drive `CLAUDE_CONFIG_DIR`, same pattern as
  `AZURE_CONFIG_DIR`/`GH_CONFIG_DIR`. **Caveat: the keychain entry is machine-local, so the config
  dir travels and the secret does not — Kam logs in once per machine per agent.**

## OPEN WITH KAM — all have safe defaults, nothing blocks
- **Card `secuura-platform-s-count-was-wrong-when-you-ruled`** — 18 PS tickets, default HOLD.
- **Card `secuura-ten-cascade-collateral-restore-or-leave`** — NOT YET FILED (`decision_queue`
  refused while `chat_log` was corrupt; **re-file it**). 10 tickets, 3 In Progress, default: none.
- **Tuesday's folder shape** — Kam said "copy your folder, label it Tuesday". **ASKED, not done:**
  a *copy* forks the brain; a **CLONE** of the same repo keeps it one thing that syncs. Also 1.3 GB
  of `2_Project_Files` is worktrees/venvs/node_modules that must NOT be duplicated. One word from him.
- Plan decisions still open: mesh vs hosted (default mesh, already running) · shared W/M brain
  (default shared) · path guard on the travel drive (default: refuse).

## DONE TODAY BY THIS SEAT
s149 unblocked, scored 1.0, wrapped, pane closed · Kam's 4 rulings recorded · `decisions.json` and
`chat_log.json` both repaired with conservation asserted · `store_guard` + `guard_data_dir` built
and red-proofed in BOTH shells · `fleet_ack.sh` + the mail-tile ack (Kam's 10:19) · attention flag
now fires on the red marker (Kam's 10:59) · `wed_claim.sh` un-hardcoded from the dead T9 path ·
`cockpit.sh say` refuses an authorising tap with no mail (ledger w=5) · INDEX.md head corrected ·
KS-996 measured read-only · **brain+settings backup at
`5_Project_History/backups/wednesday-brain-and-settings_<stamp>.tar.gz` (660 MB, 12,207 entries,
content-verified, secrets excluded).**

## SECUURA STATE (s149 closed; its handover is the source)
    origin/develop 986c592d5 · demo 400517aaf · unarchived 370
    #903 #904 #905 #793 open, unmerged · #896/#899/#900 UNAPPROVED deliberately
    KS-968 In Progress (moved by another hand) · the schema trap is at c38040bd1, NOT on develop
    Next highest-value: KS-989 (P1) — and "wire format:check, never quality" travels with it
    HELD: PS-Done 18 (Kam) · Tested-Not-Deployed (Kam's `hold`)

## 🔴 PROJECT TRAP — third occurrence across two seats
**Any probe of `users.email` by literal comparison is VOID BY CONSTRUCTION** — AES-GCM ciphertext.
Resolve via `email_lookup_hash`; a hash comparison is decisive on a MATCH only.

## WHAT s151 GOT WRONG — all filed, none reached a cost
1. Red-proofed an anti-junk-tap guard by sending junk taps to the LIVE agent.
2. A count entered a card TITLE with no provenance and Kam ruled on it.
3. **Corrupted `chat_log.json` via the mechanism it had itself named 40 minutes earlier**, in the
   one writer it had not guarded — third instance today of "fixed the one you remember".
4. **Priced a recommendation at "an evening's work" for something running 19 days** — and the
   error argued silently for the RISKIER option.
5. Four instrument false-absences (an `awk` range, stdout-vs-artefact, a zsh word-split in its own
   guard, `timeout` on macOS). All self-caught by controls.
