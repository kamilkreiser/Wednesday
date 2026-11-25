This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-26_coagent_MEASURE-2_brief.md`. Seat MEASURE-2 only. Report under "## ADDENDUM 1 (answers Q1, Q2, Q3)" in your STATUS file.

If your context was compacted: re-read your brief, this addendum and your STATUS file WHOLE before doing anything.

# MEASURE-2 ADDENDUM 1: answers to Q1, Q2 and Q3 (your STATUS, 39 lines, read whole by Friday)

All three questions were the right ones to stop on. No run has been spent, so every change below is a change BEFORE the first run: rehearse it with no model like the rest.

## Q1 (the owner's settings keys): proceed as your option (a), with three conditions
1. **`model`** in either file: accepted. Every run passes `--model` on the command line, and section 5's per-run check (dispatch lines name the smallest model alone, with its two controls) decides; any other model in a run is still a `STOP Q<n>`.
2. **`hooks` and `env` in `~/.claude/settings.json`: this is the one that matters for the measurement itself.** A hook of the owner's on `PreToolUse` or `PermissionRequest` could change or answer what cases E1, E2, E3 and W1 measure, and it would read as the host's behaviour. So, before the first run and with NO model:
   - Look for a documentation line that says which user settings file Claude Code reads when `CLAUDE_CONFIG_DIR` is set; quote it with the page and the date, or write "no line found".
   - Add to the per-run checks of section 5: in the run's debug log, the number of hook dispatches whose command is NOT one of your stubs = 0, with two controls: your own stub's dispatch lines read 1 or more in the same log, and the same check on a scratch copy of a log with ONE planted line naming a made-up foreign hook command reads 1. Record names of hook EVENTS and counts only; never a command line or path from the owner's file.
   - The same for `env`: the variable NAME your key list shows must be absent from the child's environment names as your hook stub logs them (names only), or, if present, said so plainly; it concerns subagents and no case of this lane starts one.
3. **If run 1 (I1, headless) shows ANY foreign hook dispatch: `STOP Q<n>` before run 2**, with the count and the event names. I1's own verdict then stands or falls by what the capture shows; the run is spent. Do NOT use `--restricted` or any other flag that leaves out the user settings (the brief's R-8 stands); if you come to think the measurement cannot be made clean without it, that is the STOP.
4. Read no VALUE from either settings file, now or later. Keys, event names, counts and checksums alone.

## Q2 (P1 and `--strict-mcp-config`): your option (c). P1 keeps the flag and drops its parts (b) and (c)
- P1 runs as written WITH `--strict-mcp-config`. It measures (a) the exec-form hook against the shell-form hook, loaded with `--plugin-dir`, and (d) the count of plugin variables the agent's Bash sees. Its prompt loses the MCP half: "Run the shell command `env | grep -c '^CLAUDE_PLUGIN_'` and reply with its output." The plugin's `.mcp.json` stays in the scratch plugin as the template has it; you record whether the `init` tool list holds any tool of it (expected by the CLI reference's line you quoted: none; that reading is recorded as "skipped by the flag, as documented", never as a fact about the path with a space).
- **Parts (b) (an MCP server started through a path with a space, from a plugin) and (c) (`mcp_server` in the hook input for a PLUGIN's MCP call) are NOT MEASURED in this lane.** Reason, to be written in RESULT as it stands here: without the flag, the MCP servers of the account and of the user scope would join a test session, which the lane's safety rules do not allow. `mcp_server` for a server passed with `--mcp-config` is still read in I1 (its evidence (e)).
- Run budget: P1 stays 1 planned, 1 at most.

## Q3 (S1): the case changes, before any run. S1 runs WITH one allow rule, in the scratch skill alone
- The documentation line you quoted ("`PreToolUse` hooks don't fire for injected commands that run as the skill loads") is the reading the product's backlog entry needs; the run's job is to show it on this version, and as written it would end "not run" and show nothing.
- **Ruled (the case table now says so, as section 9's rule requires): the scratch skill's frontmatter carries `allowed-tools: Bash(echo *)`** (syntax from the skills page, quoted with the date), and nothing wider. The body's line stays the `echo S1-MARK $ARGUMENTS > s1.txt` line of the brief. No allow rule anywhere else; no other case changes.
- Evidence and its opposite, unchanged in form: (a) hook entries with `tool_name` Bash whose command holds `S1-MARK`: 1 or more = the line goes through the gate; 0 = it does not. (b) `s1.txt` holds `XYZ7` = ran and substituted. The reading "(a) = 0 with (b) present" is "ran outside the gate": by the brief's R-9, in STATUS at once in plain words with the run number, and beside it the documentation line, so the row says "measured, and as documented". Positive control in the same run, as before: the hook logged the `Skill` call itself; if not, VOID.
- Rehearsal with no model: the skill file parses as the page describes (say how you checked); the hook stub fed a hand-made Bash input holding `S1-MARK` logs it.
- In RESULT, word the row for what it shows: an `echo` line pre-approved by the skill's own frontmatter. It does not show what happens to a line that is not pre-approved in the default mode (the page says the invocation is aborted: quote it, tagged READ).

## What does not change
The ceiling of 20 and its ledger; the order of the cases; every other rule of the brief and its section 12. Your last-but-one line stays the run count. When Q1's no-model steps are done and shown in STATUS, go on to the runs without waiting for another word.

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
