---
date: 2026-11-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (she runs on the Studio).
status: live
supersede: REPLACED WHOLESALE 2026-11-11 12:2x by the Mac mini seat before the drive cut-over. The previous file (262 KB, 11-06..11-10 blocks) is archived VERBATIM at the top of NEXT-PICKUP-archive.md. Replace wholesale; never stack.
---

# NEXT PICKUP, Wed 11 Nov 2026 (written just before the DevMASTER -> new-drive cut-over)

## WHERE YOU ARE
- **Machine: the always-on Mac mini** (Kam 11-11: "you are now on the mac mini as its always on"). Lesson 2026-11-11_wednesday-lives-on-the-mac-mini. Set up this morning: brew rsync 3.5.2, postgresql@15, python3.12 + dashboard-cloud/.venv, usage publisher, live_chat_poll, 7/7 scheduler jobs (Ornith x3 paused by Kam, nassync HELD), Spark tunnel via alias `hp-loan-spark` (tunnel.sh fallback), gh logins (WEDNESDAY: KamORG454; Secuura: kksecura), Secuura folder trust accepted. Tuesday's stale com.tuesday.* jobs on the mini quarantined on Kam's word.
- **Drives:** the new TerraMaster D1 SSD Pro + Samsung 990 PRO 4TB (was named Secuura_DEV) replaces the UGREEN + Crucial P310 2TB (old DevMASTER). Kam ruled: rename new -> `DevMASTER`, old -> `DevMASTER_OLD` once the copy is verified (card wed-morning-plan-1111 = a: cut over after B 131st's merge). If you are reading this on the NEW drive, the cut-over happened: check `diskutil info /Volumes/DevMASTER` says Samsung/4 TB, and that /Volumes/DevMASTER_OLD exists. Launcher now self-locates its workspace (Launch_Wednesday.command, .pre-1111-selflocate).
- **NAS:** new NAS //DotORG@192.168.20.154 (DEV-Working, Backup, Seagate Hub). Offloads: 2_Project_Files/tools/nas_offload.sh --client secuura|general (lesson 2026-11-11_wednesday-offloads-to-dev-working-nas). Nightly mirror (nas_push.sh) repointed to /Volumes/Backup/DevMASTER-mirror (card wed-nightly-nas-mirror-old-nas-1111 = a); first real run 03:30 11-12. OWED by Kam: Full Disk Access for /opt/homebrew/bin/rsync on the mini (asked on the board 11:5x). Check ~/Library/Logs/wednesday_naspush.log after 03:30.

## KAM
Clear the Secuura board over 1-2 weeks (grant in EXPIRING-GRANTS, outer read Fri 20 Nov). Demo FROZEN. Spark ON, keep it busy. Usage: renewed by /login 11-11, 7d ~2%. Open with him: the lawyer pack (Secuura/Blockchain) only. Six old extranet items for Kam (KS-721, KS-662, KYC image disposal, GitHub Actions billing, "[Dev] Update your local", OpenAPI examples), from B 131st's boot read: relay once.

## FIRST WORK (in order)
1. **Cut-over, if not yet done:** B 131st wrap mail -> score + pane_close.sh -> floor empty -> final delta (scripts in 2_Project_Files/fleet/state/2026-11-09_migrate-to-secuura-dev/pass2_*_1111.sh; never --delete) -> verify (scratchpad verify.sh shape: dry run per tree, 0 files to send, + per-folder file counts both sides) -> tell Kam READY with numbers -> rename on his presence -> he relaunches Wednesday from the new DevMASTER -> doctor + boot test.
2. **After the cut-over:** restart the Day Dashboard server and anything that ran from the old drive; check scheduler jobs still load (paths unchanged by design).
3. **Next merge seat B 132nd:** B 131st's HANDOVER 'FOR SEAT B 132nd' -> drafter from briefs_staged/2026-11-11_seatB131_merge.md (queue now starts row 8w PR 2164; 8x 2165, 8y 2166, 8z 2168, 8za 2167, 8zb 2169 GO must say live admin API contract change, 8zc 2170 GO must name the behaviour change; then 2123 on). Stamp needs a full contradiction read (delegate it; attest on its report). Launch with SEAT_MODEL_ENV=claude-sonnet-5-5 (a hand launch MUST carry it). Answers go with `--kind answer`.
4. **Raise seat R 95th (none drafted yet):** R 94th's unraised rows (its HANDOVER: rows 4, 10 KS-1928 committed-not-pushed head 6db0230ede82 in s-r94-b, 11, 12, 13-15 = o132's KS-2158, KS-2085 p1, KS-2156 p1) + today's held Spark passes: KS-2021 (tier 1, auth password.ts; PR must state malformed-count rows now do not match), KS-2149 (tier 2), KS-2155 (tier 2). All READY_* files under 2_Project_Files/local-model/night/.
5. **Spark:** idle after o134. Next: KS-2156 p2 once p1 merges; widenings named in o133/o134 reports (planted-regression test-only tier, tsc-red tier, frontend/admin vitest config). The declared-rename allowance (A6, `## Renames`) is BUILT and proven end-to-end (report 0_Brain/reference/2026-11-11_harness-declared-rename/).
6. **Board filings owed (no board seat):** G304-2156-2, R-c ticket (CONN + DSN), residue -7, root-level-path merge-tool bug ticket, G306-2167-1, G306-2168-1, G307-2170-1 (silent skip) — after their PRs merge.

## BOOT DEBT carried
INDEX.md refresh not done 11-11. Digest read as headlines only this seat (677 KB). Weekly consolidation LAPSED (newest audit 10-19). Ledger rows past rule 3c cadence (doctor). Ledger promotion candidates from 11-11: (a) advisory hook on `<script>.sh --help` (w=3), (b) checkpoint check that a wed-morning-plan-<MMDD> card exists after 09:00 (w=2).

## RULES EARNED THIS SEAT (11-11)
- After any rebase/merge, read `git status -sb` + test `.git/rebase-merge` in the same call (the boot rebase sat unfinished for an hour).
- A pre-empted boot is RESUMED: list unrun steps in the note before the first non-boot task (morning card was missed).
- Never run a write tool to learn its usage: read its header.
- In zsh `log` is a builtin: /usr/bin/log.
