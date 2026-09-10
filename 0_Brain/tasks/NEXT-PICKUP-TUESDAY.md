---
date: 2026-09-10
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written at s5's 66% checkpoint, 2026-09-10 ~13:55 AEST
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced the s4 pickup.
---

# NEXT PICKUP — Tuesday, s5. Three rounds delivered and verified. Kam owes four decisions. Nothing is on fire.

**`2_Project_Files/tools/kam_rulings_today.sh` before writing anything.** Rotation band **80–90**; 70% is a checkpoint only.
**Kam reads the pane on the MAC STUDIO. Verify every message AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`) — never on `127.0.0.1`, which is this machine and proves nothing. That cost him four unanswered messages this morning.

## 🔴 WITH KAM — four, and only the NAS blocks me

1. **THE NAS, unchanged since 09:00.** Finder ⌘K → `smb://KAMILADMIN@192.168.20.221/Development`, password, **tick "Remember this password in my keychain"** · then **System Settings → Privacy & Security → Full Disk Access → add Terminal.** Both required, they fail in that order. ✅ **PROMISED: the moment he says done, run `/Volumes/KK_T9_External_HDD/!SYNC FILES/devnas-sync.sh` BY HAND and watch it.** Raised three times today; he has not actioned it.
2. **NEXUSAI MARKETPLACE — he prepares containers TOMORROW.** Verdict: **GO-WITH-CONDITIONS to build, NOT READY to submit.** 🔴 **The first thing he must not do is build from `2_Project_Files`** — that tree's `.dockerignore` is the 26-April version (1042 B vs main's 4074 B), so a build there ships an **untracked RSA private key**, the pen-test report, all six runbooks and 24 extra files. Four more carriers: plaintext passwords + PII (`docs/Authorized_Users.md`), real tenant/app GUIDs **in the setup wizard UI**, a real person named in an LLM tool description sent on every AI request, and 2 of 8 marketplace listing screenshots showing a real person's name. Report: `!CODING/Datasec/NexusAI/evidence-s50-marketplace-review/`.
3. **RD-369 at its cap** — tier-1 gate returned NO GO. Ship-and-ticket recommended, **default if he stays silent**. No round 4 without him.
4. **13B COUNTS 132 FINDINGS AND ENUMERATES ~52.** 80 are tallied and never described. Four INTAKE tickets carry the gap (CWP-4, CPKEY-168, MYP-40, SEC-3). **This also bounds the evidence appendix** — 14 entries because 14 is what the register describes. I told him the appendix covered every finding before I knew this, and corrected it.

## ✅ DELIVERED TODAY, all verified independently rather than on an agent's word

- **Security Review 13A/13B rebuilt + emailed** (to `kamil.kreiser@datasec.com.au` — Datasec deliverables go to the Datasec address, NOT `kreiser.org@me.com`; he corrected me on that). Appendix E/D evidence locations, 147 entries, 663 file:line citations; 185 tables re-widthed, left column 6.00 cm; two blank lines before `###`. Verified against the pre-edit files as controls: page breaks 175→146 and 50→25, exactly the `###` counts; tables/rows unchanged.
- **NexusAI marketplace review** — see above.
- **Jira round** — 16 tickets, 5 projects; **CWP** (10555) and **TDP** (10556) created. Verified in Jira myself: CWP 4 · TDP 4 · CPKEY 3 · MYP 2 · SEC 3 · **RD 0**. 🔑 **Search-before-create saved 17 duplicates: NexusAI's entire 17 findings were already filed (RD-361/362/363 + 2).**

## ⚠ TRAPS — s4's still hold except where struck. These are s5's.

1. 🔴 **NEVER `git pull --rebase --autostash` in this tree.** Still true.
2. 🔴 **`git rebase --continue` WEDGES HERE — three times today, each with ZERO unmerged files** (`git ls-files -u` empty, `--continue` still refusing). **Do not fight it: `git rebase --abort`, then `git -c core.editor=true merge origin/main`.** Resolve collector JSON with `--theirs`, regenerate the two boot digests from source (they are GENERATED — never hand-merge), and **back up `chat_tuesday.json` first and union-check it after**: the merge silently dropped a chat row once today and only the union caught it.
3. ~~Stop putting `0_Brain/dashboard/data/` in your own commits~~ **AMENDED**: still the rule, but when `panel_sync` is dead and Kam is not receiving messages, commit it deliberately and say so. Verify at ORIGIN afterwards.
4. **`panel_sync` FIXED TODAY by Wednesday** — it no longer deadlocks on a conflict, and it advances the other seat's stream from origin when a dirty tree blocks the rebase. **The `(N paths)` undercount is also fixed.** If it skips, look for **your own** dirty files.
5. 🔴 **`setsid` DOES NOT EXIST ON macOS.** `nohup bash … &` only. I killed a healthy loop and its replacement silently failed; Kam's sync was down a minute. Always re-read `ps -o tty=` and branch on it **in code**.
6. **`cockpit.sh launch` still dead here** (registry pins DevMASTER). Launchers under `2_Project_Files/fleet/launch_*.sh` are self-locating and work — copy that pattern.
7. **Agent stdout is now gitignored** (`briefs_staged/*.out`) and the two previously-TRACKED plain `.out` files are untracked (`1a7c5aed`, copies quarantined). **A `.gitignore` rule cannot exclude what git already tracks** — check `git ls-files`, not just the rule.
8. **`board_count.sh` cannot page Jira.** For counts use `POST /rest/api/3/search/approximate-count` — and **a nonexistent project key also returns `{"count":0}`**, so discriminate with `GET /rest/api/3/project/<KEY>` (404 = absent) before believing a zero.

## STANDING

🔴 **Kam reads the STUDIO pane. Verify at ORIGIN, every time.**
🔴 **Datasec client documents → `kamil.kreiser@datasec.com.au`. Fleet/coordination → `kreiser.org@me.com`.**
**Confirm receipt when an instruction lands AND confirm completion when it is done** — both, his 2026-09-10 rule.
**He dictates (Superwhisper).** Read through the noise; where a dictated word decides an action, state your reading and check it, or ask him to type that one word.
**Cross-seat mail is COORDINATION ONLY. Names, not pronouns. Never delete — quarantine.**
🔴 **DO NOT run the wrap's vault step** (`end-of-session.md:50` is `git add -A`; the vault holds Secuura paths).
**Coordinate claims with Wednesday before starting shared work** (Kam, 12:06). She holds: `panel_sync`, the cockpit conversation heldbar, and the decision-panel freeze.

## WHAT s5 WOULD SAY IF IT COULD SAY ONE THING

**I was wrong twice about why Kam could not see my messages — the project filter, then latency — and both times I was fitting ONE sentence of his rather than all of it.** His screenshot carried the disproof of both in a detail neither Wednesday nor I had mentioned: the panel beside the frozen one was live. **The fix was in code I could have read at any point in those forty minutes.**
**The counterweight, and it is the day's real lesson: every delegated round came back better than the brief.** The document agent found my premise about the spacing was false. The Jira agent found 80 findings the register counts and never describes. The marketplace agent found a private key in the default build. **None of those were things I asked for — they came from briefs that told the agent to check the brief.**
