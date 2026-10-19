# B286 drafter report (2026-10-19 ~16:55 AEDT)

Brief: `2026-10-19_B286_SEAT-G10_hpsmpoc-gate-pr162-tier2.md` (round 1 of 2 gate for HPSMPOC-290, draft PR #162 @ 6dbe394, tier 2, Sonnet). Shape copied from B283 and B279 (REFUSE with split-pattern control, LOAD, PINS, own clone and `wt-b286-*`, r-rows, verdict first/last lines, HOLDS, NOT TESTED, stamp). Read WHOLE: B283 brief, B279 brief, B284 STATUS, B284 brief. Read-only commands used: `ls-remote`, `gh api` GETs (pulls/162, pulls/162/files with patch, contents of `Hpsmpoc290Tests.cs` at the head sha, check-runs on the head, code-scanning analyses count), `date`, `uptime`, `ls`. No git write verb, no Artifact/Docs/mail/chat, no HTTP to hosted systems, no dotnet, no Jira.

## Slots (three tokens, all in the Stamp line, each once)
| Slot | Default / source |
|---|---|
| `STAMP_TIME` | Tuesday's clock at stamping, `YYYY-MM-DD HH:MM AEDT` |
| `PORT_BLOCK` | Propose `7240-7249 (none expected)`. Re-check `lsof -nP -iTCP:7200-7299 -sTCP:LISTEN` at stamp. B282 holds 7200-7209, B283 7210-7219, B284 7220-7229, B285 7230-7239 by their briefs. No server is needed (in-process TestServer) |
| `B_NUMBER_CONFIRM` | `B286 confirmed` after a folder check for B286 hits (at drafting only these two drafter files named B286 in `briefs/`) |
Model, pane (`Datasec/HPSM-POC-G10`), suffix and both shas are filled literally. Count check on the unstamped file: 3 tokens on one line (`grep -o` shows 3; `grep -c` prints 1 because it counts lines). Tuesday copies `.pre-stamp` before stamping (not made by the drafter). The REFUSE line and the stamp section name the token shape without writing a matching token (verified).

## MEASURED by the drafter (16:48 AEDT)
- `ls-remote`: main `befd45e77b391467a1313af8b7b5e0fc580f7b63`; branch and `refs/pull/162/head` `6dbe394f8a0b81dfbc5d2c781ab876db57e31198`.
- PR #162: open, draft, 1 commit, 2 files (`FeedbackFiles.cs` +40/-3, `Hpsmpoc290Tests.cs` +177), title "HPSMPOC-290: 400, not 500, for a utf-7 encoded part name (B284)".
- Patch read: `TryName`/`TryFileName` wrap only the property reads, catch `NotSupportedException`; call sites at about `:348` and `:370` (derived from hunk headers; the gate re-reads); old catch untouched.
- Test file read whole: 21 cases (1 Fact + 15 `Rows` + 4 `NeverThrew` + 1 guard); the guard calls `FeedbackFormReader.ReadAsync` directly; `Echoes` list = canary, its base64, `ZmlsZXM`, `utf-7`, `x-no-such-charset`.
- Check runs on the head: dependency review and gitleaks success; CodeQL queued; Analyze x4, api, both SQL Server shards, web unit, web build, infra in progress. Analyses list for `refs/pull/162/head` had 1 entry (its commit not read). So CI is PENDING; r8 is conditional.
- Load: `uptime` read 13.91 11.10 10.55. The brief's heavy-job limit is load1 below 8 (the builder's own limit), so the gate will wait; priority order is in the brief.

## RELAYED (from B284 STATUS, to be re-measured by the gate)
The 500 for exactly four shapes; 27 neighbour inputs (22 API + 5 framework); RED 5 of 21; Feedback 270 -> 291; other projects unchanged; 8 of 9 mutants red; m3a survives; census table for -226; Jira comments 39690/39691; gitleaks results.

## Gate design choices (why the rows are shaped this way)
- **Independent RED** is two instruments: the builder's file on the base tree, and the gate's OWN probe written from the Done-when (so a bad test cannot confirm itself).
- **Narrowness** is attacked three ways: code reading, a through-the-endpoint body-fault probe (the builder's guard only calls the reader directly, trap T-b), and a charset sweep for other 5xx (trap T-d), plus the mutants including "widen to Exception" (m3a survives; the gate must argue equivalence or name the missing row, trap T-c).
- **Echo/log** uses a second canary outside the builder's `Echoes` list and a log capture over all categories (trap T-e).
- **Counts**: Feedback project plus every `api/tests` project at base and head, name multisets, lost 0 / added 21.
- **-226** is spot-checked, not tokened: 2 BUILT rows re-run (N-4 theory, N-7 delivery tests), cites held at `befd45e`, N-8 accepted out of lane, comments 39690/39691 read byte-equal. Builder's own note that it ran a `git grep` under `web/src/server` (Correction 3) is not re-examined by the gate; Tuesday may want to look.
- **FOR TUESDAY 2** (import endpoint) is context only: the gate confirms 0 bytes under `api/src/HpsmPoc.Modules.Assessment` and tests nothing there.

## Risks and judgement calls for Tuesday
1. Load is high (13.9); heavy rows will queue. If Tuesday wants the gate sooner, raising the limit is Tuesday's call (the brief says below 8, matching the builder; B283 used below 6).
2. The through-the-endpoint body-fault probe (r3 b ii) may be impossible in `TestServer` (the builder says it hands a failing body back to the caller). The brief allows NOT TESTED with output, then settles from code.
3. The head can move (PR is a draft); the REFUSE row says test the READY sha only and say so. If it moves, edit both the `.pre-stamp` copy and the stamped copy (the sha is written literally in both places).
4. `6dbe394` message says "27 inputs" (22 API). Brief classes it Note at most (no force push).
5. The brief is one long line per section in the B279 style, about 27 KB; the Jira-line shape is given as a template for the gate's STATUS, and nothing is posted.
6. The gate reads the builder's `Briefs/2026-10-19_B284_evidence/neighbour-table.txt` (a summary, not a `.tools` tree) as a claim; if Tuesday wants STATUS-only reading, strike that sentence in r2.
