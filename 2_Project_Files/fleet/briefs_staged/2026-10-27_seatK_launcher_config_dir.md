## NEW SEAT: you are Seat K <N>th in pane %39 (lane Secuura/Blockchain-K, a TOOLING seat, on SONNET): give the Secuura launcher its own Claude config folder, so `/model` stops writing Kam's user-global settings — PROVE the login survives first

**Routing receipt:** `model: claude-sonnet-5-5 -- C2 (one bounded launcher change with a measured precondition and the launcher's own guard suite) -- P1-P4: edits to the project-root launcher, no repo push`. Wednesday switches this pane with `/model claude-sonnet-5-5`.

**Why you exist:** Kam ruled card `wed-model-switch-writes-global-settings-1027` = **c — "Fix it in the launcher"** (live board 2026-10-27 18:18:30, and again 19:39:03). The problem, measured by Wednesday 2026-10-27 16:14: when Wednesday switches a Secuura seat's model with `/model`, Claude Code prints "saved as your default for new sessions" and writes `"model"` into `~/.claude/settings.json` — Kam's USER-GLOBAL file — because this launcher sets no `CLAUDE_CONFIG_DIR`. The workspace rule is that settings changes stay project-local. The other projects already isolate `az` and `gh` the same way (`AZURE_CONFIG_DIR`, `GH_CONFIG_DIR` under `4_Credentials/`).

## BLUF
1. **Measure before you change anything:** does a seat launched with a NEW `CLAUDE_CONFIG_DIR` stay LOGGED IN? If not, STOP and mail; change nothing.
2. If it does: the launcher exports `CLAUDE_CONFIG_DIR="$PROJECT_DIR/4_Credentials/.claude-config"` before its `exec claude`, SEEDED once from a COPY of the global settings (never a symlink: a symlink would carry `/model`'s write straight back to the global file).
3. Prove it with the launcher's own guard suite and a dry run. You do NOT relaunch any running seat; Wednesday verifies the next real launch.

## QUEUE
### 0. Boot
Read `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.launch_preflight_last.txt` first and quote it verbatim in the plan confirmation. Check `$TMUX_PANE`. **Plan confirmation** = a QUESTION mail, topic `plan confirmation`, to `wednesday-agent@agentmail.to`, subject starting `[Secuura/Blockchain-K -> Wednesday]`, body line 1 `Seat K <N>th`, BEFORE any write. Derive your ordinal from `5_Project_History/history.md` (match the dated heading, never the bare name).

### 1. The precondition (read-only on everything real)
- Read how this launcher ends: `Launch_Claude.command` lines ~625-664 (the `exec claude --dangerously-skip-permissions --model claude-opus-5 "$INITIAL_PROMPT"` line and the `SECUURA_LAUNCH_DRY_RUN` block above it). Grep it for `CLAUDE_CONFIG_DIR` (Wednesday read 0 hits at 19:4x; re-measure with a positive control).
- In a THROWAWAY dir you create under `/tmp/sk` (short path), run ONE non-interactive probe: `CLAUDE_CONFIG_DIR=/tmp/sk/cfgprobe claude -p "reply with the single word ok" --model claude-sonnet-5-5 > out 2>&1; rc=$?`. Record rc and the output's first lines VERBATIM. Logged in = an answer; not logged in = a login/auth/API-key message. **Do not run `/login`, do not type credentials, do not copy any credential or keychain item.**
- If NOT logged in: STOP. Mail Wednesday the verbatim output; change nothing. (Wednesday then takes it back to Kam: the fix would need a one-time `/login` per config dir, which is his.)
- Name what the global `~/.claude/settings.json` carries that seats rely on (Wednesday read its top-level keys: `env`, `model`, `hooks`, `tui`, `skipDangerousModePermissionPrompt`, `theme`, `agentPushNotifEnabled`). READ it; never write it.

### 2. The change (only if item 1 shows the login carries)
- Backup first: copy `Launch_Claude.command` to `Launch_Claude.command.pre-1027-configdir` (the launcher is NOT in git: the backup is the undo).
- **Never edit the launcher while a launch is running it** (a running bash script reads by byte offset): check no `Launch_Claude.command` process is mid-run (`pgrep -fl 'Launch_Claude.command'`; the live seats have already `exec`'d into `claude`, so their launcher process is gone — say what you measured).
- Add, before the `exec` line and before the dry-run block: `export CLAUDE_CONFIG_DIR="$PROJECT_DIR/4_Credentials/.claude-config"` (use the launcher's own variable for its folder; read which one it uses) and a one-time seed: if `$CLAUDE_CONFIG_DIR/settings.json` does not exist, `mkdir -p` the dir (mode 700) and COPY `~/.claude/settings.json` into it (`cp`, mode 600), but WITHOUT the `"model"` key (the `--model` flag already pins the session; a carried-over `model` would only reintroduce today's ambiguity). Never overwrite an existing seeded file. Print one line to the console saying which config dir is in use.
- Make the dry-run block print `DRY_RUN_CLAUDE_CONFIG_DIR=...` so the guard suite can see it.
- `4_Credentials/` is already gitignored for this project and lies OUTSIDE the `2_Project_Files` repo; confirm both by measurement.

### 3. Proof
- `SECUURA_LAUNCH_DRY_RUN=1 bash Launch_Claude.command` (from the project folder, as the suite does): quote `DRY_RUN_CLAUDE_CONFIG_DIR`. A second dry run must NOT re-seed (settings.json mtime unchanged).
- Run `Launch_Claude.seats.test.sh`: before your change and after, same shape; quote both totals.
- `bash -n Launch_Claude.command` and a source-boundary check: the `INITIAL_PROMPT` variable still ENDS where it ended before your change (the 2026-09-02 quote-truncation defect: `bash -n` cannot see a string boundary moving).
- Diff the launcher against its backup: your lines only.
- Re-probe item 1 with the REAL seeded dir: `CLAUDE_CONFIG_DIR=<the seeded dir> claude -p "reply ok" --model claude-sonnet-5-5`: still logged in.
- Then STOP at READY: Wednesday verifies the next real launch (its boot statusline, a `/model` switch leaving `~/.claude/settings.json` unchanged by mtime and content).

## HOLDS
- Signature classes pause for Kam: production, money, external comms to any human, anything irreversible. No box, no `az`, no deploy, no merge, no Docker.
- No push: you change no file in `2_Project_Files` (the repo). The launcher, its backup and the new config dir are outside it.
- **Never touch `~/.claude/settings.json`** or any other user-global file. Never `/login`. Never copy credentials, keychain items or tokens.
- Never delete: quarantine into a dated folder and record the move. Never `cd`; absolute paths.
- Stop ONLY processes you started, by the PID you recorded; never `pkill`/`killall` by name.
- Every other launcher defect you see (step 7's `POST /api/seen`, step 8's `coagent@` 404, the F-02 keepalive branch, the `claude-opus-5` pin vs the newest Opus) is NOT in this brief: list it in your READY mail, change none of it.
- Mail discipline: body line 1 `Seat K <N>th`; subject starts `[Secuura/Blockchain-K -> Wednesday]`; never put stop, hold, checkpoint or hand over in a subject. Shared inbox `secuura-blockchain@agentmail.to`: act only on mail naming `Seat K <N>th`.

## PARTITION
**Yours:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command` (edit), its new backup `Launch_Claude.command.pre-1027-configdir`, the new dir `4_Credentials/.claude-config/`, scratch under `/tmp/sk`.
**Read-only:** `Launch_Claude.seats.test.sh` (run it, do not edit it), `~/.claude/settings.json`, everything in `2_Project_Files`.
**NOT yours:** every other seat's worktree; the push lock and queue (you do not push).

PROVENANCE:
- Kam's ruling c on card wed-model-switch-writes-global-settings-1027 | live board, Kam's panel messages read with /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh | read 2026-10-27
- the /model dialog writes ~/.claude/settings.json "model" (mtime 16:14:10, value claude-sonnet-5-5) | Wednesday's ls -lT and grep of /Users/kamilkreiser/.claude/settings.json after the 16:14 switch | read 2026-10-27
- the launcher sets no CLAUDE_CONFIG_DIR and ends in `exec claude --dangerously-skip-permissions --model claude-opus-5` | grep and sed -n '625,664p' of Launch_Claude.command by Wednesday | read 2026-10-27
- the launcher is not in a git repo | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain" rev-parse` = "not a git repository" | read 2026-10-27
- global settings top-level keys | python3 json read of /Users/kamilkreiser/.claude/settings.json by Wednesday | read 2026-10-27

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-27 19:41
