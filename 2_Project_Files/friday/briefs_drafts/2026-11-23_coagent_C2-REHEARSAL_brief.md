This brief is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. You are a NEW seat, C2-REHEARSAL. You have no mailbox: your report is the file `coagent/5_Project_History/STATUS_C2_REHEARSAL.md` (the only file you write in the project folder). Its last line always begins `IN PROGRESS`, `STOP Q<n>` or, at the end, exactly `REHEARSAL REPORT WRITTEN`.

# C2-REHEARSAL: on this Mac alone, on loopback, with NO model run: a GATED host that uses an OUTSIDE relay

## Why
The next stage with the owner (C2) runs the Mac host WITH the gate and with a relay started separately (`--relay-url`, `--relay-pin`). That combination has never run: the first link on 2026-11-23 ran the Mac host ungated; the one-Mac demo ran gated with the daemon's own relay. Friday needs it shown, and its exact commands recorded, before the owner sits down. This is a measurement, not a build: you change NO file of the repository, commit nothing, push nothing.

## Read WHOLE first
- The plan draft: `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-23_C2_two-agents_plan_DRAFT.md` (sections 1, 4, 5 and 7).
- At main `3164374a8a20d73296558997438b97a41a7837ad` (read by SHA): `preview/demo/one-mac.md`, `preview/demo/lan.md`, `preview/demo/setup.sh`, `preview/make-plugin.sh`, `docs/DAEMON.md` sections 3 and 8.
- What ran on the first link, for the command shapes that worked: `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/coagent_c1_dry.sh` (Friday's loopback script) and `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/17_C1-first-link-sheet-2026-11-23.md`.

## Where you work
- A scratch clone of exactly `3164374` in a SHORT folder of your own under `/private/tmp/` (about 20 characters; the daemon's socket paths must stay under 103 bytes): `git clone` from the project repo path, `git checkout --detach 3164374…`; a tools folder there whose `cargo/bin` and `rustup` are LINKS to the project's `tools/` (as `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/coagent_merge_check.sh` does it); your own `CARGO_TARGET_DIR` there. In the project repository itself: git read verbs only, with `git --no-optional-locks`.
- Heavy rule: before the build, `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` must print less than 3 (an error = FULL).
- Loopback ONLY: every listener on 127.0.0.1. Never `--allow-non-loopback`. Before you start anything, and again at the end, show `lsof -nP -iTCP -sTCP:LISTEN` lines of your own programs. NO model run: never start `claude` with a prompt. Never use `cd` in a shell command line you report as a recipe without saying which folder it needs; never delete (quarantine inside your own scratch folder).
- State first, then act: before every invite, read `status` (pairing and session must be null) in the same command.

## What to do
1. Build: `cargo build --locked --workspace --bins` at `3164374`. Record the four program names and sizes that the preview needs (`coagentd`, `coagent`, `coagent-mcp`, `coagent-hook`).
2. `preview/demo/setup.sh <your root> "$BIN"` in a NEW root: record everything it prints and the tree it makes (it should write a COMMANDS file). If it refuses or fails: quote it whole and STOP with a question.
3. Start a relay on loopback as its own process with an identity file, output to a log WITHOUT `tee` (the first link showed `tee` loses the relay's own stop lines at Ctrl-C). Record its `url:` and `fingerprint:` lines.
4. Start the HOST exactly as setup.sh's host line says (gated: `--gate --workspace … --exclude … --gate-dir … --idle-exit-secs 86400`) PLUS `--relay-url` and `--relay-pin` from the relay's log. Does it start? Quote its whole log. `status` must show `"gate":"on"`. If the daemon refuses this flag combination: that is the finding; quote it and STOP.
5. Start an UNGATED guest in a second data folder (no relay flags). Make an invitation on the host into a mode-600 file WITHOUT printing it; join on the guest from that file; poll both `status` until `session.connected` is true (60 s limit). Record the seconds it took.
6. Messages with `ctl`, markers `C2R-1` to `C2R-4`:
   - guest `send` kind request `C2R-1 …`; then HOST `ctl inbox_read`: record the answer whole. EXPECTED (reasoned from the source, never run): the gated host refuses a read that carries no witness (`gate_missing`), and `status` shows `unread` 1. Is that what happens?
   - host `ctl send` kind request `C2R-3 …`: what does a gated host answer to a `send` typed by hand? Record whole.
   - guest `inbox_read` / `inbox_ack` for whatever arrived.
   Say plainly, from what you saw: with the Mac gated, which `ctl` commands can the coordinator still use during the owner's session (status? invite? end? send? inbox_read?), and which only the Claude Code session behind the gate can do.
7. The waiting-invitation case, on the host: after `end` of the session, make an invitation and let nobody join; try a second `invite` (the first link saw `session_active`); then `end` (it answered `ended:false` and cleared the pairing); then `invite` again must work. Record each answer.
8. Stop everything with SIGINT, one program at a time; quote the last lines of each log; show no process and no listener of yours is left; `grep -c 'C2R-'` on the relay log and both daemon logs (expected 0 each) with a positive control.
9. Write, at the end of your STATUS, section "FOR THE OWNER'S SHEET": the exact MAC blocks for the day, each beginning `MAC:`, for (a) the relay with the home-network address computed at paste time (as the first-link sheet's Window 1 does, but with output to a file and no `tee`), (b) the gated host reading url and pin from the relay's log, (c) the Claude Code line of one-mac.md step 6 for the host half only (written, NOT run by you). Mark each block RAN ON LOOPBACK (with the one difference from what you ran named) or WRITTEN, NOT RUN.

## Report
STATUS sections: (1) clone, build, tools; (2) setup.sh output; (3) to (8) each step with every command and its output WHOLE and the local time; (9) the sheet blocks; (10) findings, each tagged MEASURED or REASONED; UNVERIFIED list; processes left (none); where your scratch folder is and its size (leave it in place).

After ANY context compaction, re-read this brief and your STATUS whole before writing anything more. No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
