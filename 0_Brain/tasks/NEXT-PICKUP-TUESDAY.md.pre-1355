---
date: 2026-09-10
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written at s4's 50% checkpoint, 2026-09-10 ~09:40 AEST, ctx 49%
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced the s3 pickup.
---

# NEXT PICKUP — Tuesday, s4. NexusAI IS RUNNING. Kam owes two clicks. Nothing is on fire.

**`2_Project_Files/tools/kam_rulings_today.sh` before writing anything.** Rotation band **80–90**; 70% is a checkpoint only.

## 🔴 WITH KAM — two items, and only the first blocks me

1. **THE NAS, unchanged since 09:00.** Finder ⌘K → `smb://KAMILADMIN@192.168.20.221/Development`, password, **tick "Remember this password in my keychain"** · then **System Settings → Privacy & Security → Full Disk Access → add Terminal.** Both required, they fail in that order, and #2 is what killed the 23:00 run (exit 126, TCC). ✅ **PROMISED HIM: the moment he says done, run `/Volumes/KK_T9_External_HDD/!SYNC FILES/devnas-sync.sh` BY HAND, watch it, confirm before tonight.** First run is long; >50-file deletion alarm; deletions recoverable from `~/.unison/backup`. **He said at 08:58 he will enter the password when asked — so ASK, do not wait.**
2. **RD-104, open since 09-07** — he ruled `youcheck` and the two answers never came. `github.com/datasecau/Reporting_Dashboard_Au/settings/environments` and `.../settings/variables/actions`. **Not blocking: nothing in S49's queue deploys.**

## 🟢 NexusAI S49 — LIVE in pane `%16`, and it is good

Briefed + answered + addendum'd, all three verified at `datasec-nexusai@`. Working in its **own worktree** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s49` @ `cd2b543`, 0 status entries. **Queue, all Kam-authorised or S48-measured:**
1. **RD-369 round 3** (Kam ruled `round3` 09-09 12:09) — guard only: remove the distance window from BOTH paths, make the certifying cell able to fail. 🔴 **He was offered `wider` (round 3 PLUS removing the RD-385 files) and DECLINED. Detection only — do not let a successor widen it.** Cap: **no round 4 without Kam.**
2. **RD-363** — forward-merge `b0dec96f` (Key Vault purge protection). 🔴 **The TICKET is SEC-07/08/11, three legs; the branch closes ONE. It must NOT close on one leg.** Tier-1 gate, merge on my GO.
3. **`PRIVACY.md:21`** — remove the HP URL, invent no replacement (the domain is Kam's). It found **no RD ticket mentions `hpauthsuite`** — it is filing one.

**Its mail now comes to `tuesday-agent@`** (addendum sent + verified). **Inbound from us still reads `[Wednesday -> …]` — a hardcoded literal in `send_brief.sh`; trust the `from` header.**

## ⚠ TRAPS — s3's still hold. These are s4's.

1. 🔴 **NEVER `git pull --rebase --autostash` in this tree.** One did, this session, and cascaded into FOUR rounds of conflict surgery, the last landing on `chat_tuesday.json` — the file holding my replies to Kam. **Commit first, then `git pull --rebase --no-autostash`.** Repair shape that worked: union both sides on `(ts, sha256(text)[:12])` with assertions made BEFORE writing.
2. 🔴 **Stop putting `0_Brain/dashboard/data/` in your own commits.** The `panel_sync` loop owns it and commits every 60s; every commit of mine that touched it was a race I chose to enter. **Four collector-file conflicts came from exactly that.** Let the loop push it.
3. **`panel_sync.log` says `(0 paths)` when ONE path is dirty** — `printf '%s' | wc -l` counts newlines. **Do not go hunting a guard that fires on an empty set; I nearly mailed that as a cause.** Reported to Wednesday; her fix, her file.
4. **`cockpit.sh launch` is still dead here** (registry pins DevMASTER; the travel fallback keys on the tree name `WEDNESDAY`). **Use `cockpit.sh add "<name>" 'bash "<real T9 path>"'` — same `add_pane`.** Worked cleanly for `%16`.
5. **Empty prompt ≠ turn ended.** The spinner and the transcript mtime are the liveness discriminators. Detector (`pane_prompt_check.sh`) FIRST, always.
6. **`board_count.sh` cannot page a Jira board** — it refuses (correctly) with "MORE PAGES EXIST". Page it yourself via `/rest/api/3/search/jql` with `nextPageToken` until `isLast`. **Datasec Jira: 543 open, RD = 296, all assigned to Kam.**

## 🔵 OPEN, NOT MINE TO FIX

- **Card `fleet-comms-names-one-coordinator`** on Kam's queue (default HOLD): the workspace `CLAUDE.md` still tells every project to wrap to `wednesday-agent@`. **Measured: zero routing tags in the Datasec launchers — the instruction comes only from his file.** Until he rules, tell each Datasec seat by hand, in its brief.
- **`panel_sync` outbound gating** — Wednesday is building it (her first `ff-only` proposal was retracted by her own measurement: `--ff-only` refuses on divergence, which is our normal state). **I owe her a red-proof on the Tuesday half when the diff lands.** Do not build it here.
- **Card `nexusai-main-tree-is-a-stale-snapshot`** still open. `2_Project_Files/` is 33 files / +248 −1230 off `cd2b543`, mtimes older than the commits above them, mechanism unexplained. **S49 re-derived it exactly. Leave it.**

## STANDING

🔴 **EVERY WRAP: `git add 0_Brain/dashboard/data/usage_tuesday.json`.**
**Scope (Kam):** *"you will work on ONLY datasec projects unless otherwise instructed."*
**Confirm EVERY chat-board instruction as received, before the work.** **Cross-seat mail is COORDINATION ONLY.** **Names, not pronouns. Never delete — quarantine.**
🔴 **DO NOT run the wrap's vault step** (`end-of-session.md:50` is `git add -A`; the vault holds Secuura paths).
**After every `chat_reply.sh`: curl `/api/chatlog` and assert your message is the newest row.**
✅ **Rule 3c RUN 2026-09-10 09:4x** — 27 rows dated 09-07 moved to **`_ledger_laptop_datasec_archive.md`** (a PER-SEAT archive, not the shared `_ledger_archive.md`: writing Tuesday's rows into a file the Studio seat is live on is the race the seat split exists to avoid — raise the merge at consolidation). **Ledger 218 KB → 169 KB, 87 rows conserved as 60 + 27, asserted both directions from disk, no row in both.** Next archive: rows dated 09-08 and older, once they age past ~3 days.

## WHAT s4 WOULD SAY IF IT COULD SAY ONE THING

**Three mechanisms caught me today and every one of them was right: the brief gate refused work finished two days earlier, its self-check found two contradictions my own renumbering had made, and the prior-ruling gate made me read a ruling's scope instead of its subject.** **I caught none of the three myself.**
**And the thing I did worst was a CORRECTION: I retracted a true finding two minutes after the counterpart confirmed it, because a later pull had the rows and I read the effect of her fix as evidence about the cause.** Then I agreed to a mechanism one `rev-list` would have killed. **Both are the same shape — I generate causes faster than I measure them, and the correction is where nobody re-checks me.** **The cheapest falsifying measurement, named out loud before agreeing, is the whole fix.**
