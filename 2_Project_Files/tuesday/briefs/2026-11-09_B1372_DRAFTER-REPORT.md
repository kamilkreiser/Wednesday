STARTABLE: YES, after Tuesday fills the slots (S4, S5, S6, S9 carry PENDING in the slots file). Re-read main, both blobs, open PRs and the pane list at the stamp (a moved file refuses the seat).

# Drafter report: B1372 SEAT-H135, HPSMPOC-447 HostStartRetry header (drafted 05:30 to 05:35 AEDT 2026-11-09)

## BLUF
1. Kit `2026-11-09_B1372_SEAT-H135_hpsmpoc-447-retry-header.md` (83 lines, over the ~70 asked: long lines; 0 non-ASCII lines; 12 four-underscore runs = 11 slots + last line), `2026-11-09_B1372_slots.json` (12 keys). No `.pre-stamp` copy made (the rules allow only the kit and this report; Tuesday makes it).
2. Option (b): the seat adds one identical 5-line `//` block (+ one blank) in both copies, between the namespace line and the first `/// <summary>`; no code line changes; gates are a two-project build with equal warning counts and both whole projects on SQLite, head vs main; SQL Server legs NOT RUN; push branch `b1372/hpsmpoc-447-retry-header` only; G2 after.

## Facts re-measured (instrument; control)
- Main `b14b6f29fe34568472e1c6e87178b0244ec32415` (`gh api -X GET git/ref/heads/main`, project `GH_CONFIG_DIR`); it is the squash of the 446 row (commit list, 2026-11-06T21:25:59Z). Open PRs 0; `matching-refs/heads/b1372` 0 (control: `heads/b1362` 1). `.tools/b1372` absent (control: `.tools/b1295` present). H135 unused: no kit file or `.tools` entry names it (`ls` of briefs and `.tools`); panes `tuesday`, `fleet-monitor` only.
- Api copy 64 lines, blob `e402defe...6b77`; Feedback copy 63 lines, blob `d164d875...2c0b`; each equals `git hash-object` of my raw copy (contents API `.sha`). `diff` of the two prints exactly 3 lines (Api line 1, namespace). Filter line `:33` (Api) / `:32` (Feedback), `awk NR=n` over the raw files. Last commits `ee73c290` (Api), `1d1fa462` (Feedback).
- Ticket HPSMPOC-447 read whole by `.tools/b1343/jira_get.py` (Backlog; Fix shape (a)/(b) as the commission says; "60 of the gate's and 90 of the builder's repeats" is RELAYED from it).
- `api/Directory.Build.props`: TreatWarningsAsErrors true. `ci.yml` (682 lines): `:71` build, `:86`-`:87` test, `:237`/`:239` shard builds, `:251`-`:256` shard tests; the only mention of `HostStartRetry.cs` is a comment at `:262`. Code search shows no other reader of the file text (Feedback copy not indexed by the search; UNMEASURED beyond it).
- model-routing.md rows by `grep -n`: C2 `:92`, G2 `:109`, G-cap `:111`; `models_latest.json:23` = `claude-sonnet-5-5`. `brief_seat.sh:24` defaults to Opus.
- Ports: `lsof` on 9630-9639 printed 0 listeners (control: 11 overall); word-boundary scan of non-`.pre-` SEAT kits of 6-9 Nov: `963[0-9]` 0 files (control: `961[0-9]` 1 file). Neighbouring blocks in use by earlier kits: 9570-9629.
- Kits naming `HostStartRetry` (non-`.pre-`, 6-9 Nov): B1326, B1328, B1339, B1343, B1349, B1362, B1364, B1367; none live.

## D-decisions
- D-1 The block sits after the namespace line, not at file top, so the Api file's line 1 ("byte for byte from the next line on") keeps its meaning and the 3-line difference is unchanged.
- D-2 Ticket key `HPSMPOC-447` is allowed in the added text (the file already names HPSMPOC-308/313); no `B###` token, no person's name, no gate id.
- D-3 READY +45 / HARD STOP +75 (smaller than the 60/90 template; the Feedback project's SQLite run time is UNMEASURED, and a heavy-slot wait is not a finding).
- D-4 Launch form uses `tuesday/tools/launch_when_cool.sh <name> "<command>"` (its header lines 1-2); the three variables sit inside the quotes before `bash`. The path is not `fleet/cockpit/`.

## Q for Tuesday (each with a default)
- Q-1 Port block 9630-9639. Default: yes.
- Q-2 Comment placement after the namespace line (D-1). Default: yes.
- Q-3 READY +45 / HARD STOP +75. Default: yes.
- Q-4 Feedback project count unmeasured; the seat measures it at main on a sibling tree. Default: accept.

## UNMEASURED
Feedback project pass/fail/not-executed on SQLite; run time of either project; whether CI ever loses a session in the uncovered window (ticket); the Api project count at `b14b6f29` (2167/0/13 is RELAYED from the prior head); any SQL Server leg; whether the code-search miss on the Feedback copy hides a text reader; the dotnet toolchain state in `.tools/dotnet` (10.0.402 printed, nothing built).

## Outside-the-fences disclosure
Read-only everywhere except my three files. `gh api -X GET` only, under the project's `GH_CONFIG_DIR` (refs, pulls, contents, commits, tree, code search, analysis repo `CLARIFICATIONS.md`); one Jira GET through the project's reader; read `.tools/b1362` scripts by header or listing, not run; `tmux list-panes`, `lsof` list-only. One early Bash call containing `cd` was refused by the hook and re-issued without it. No card store, no ledger, no staged briefs, no other client read.
