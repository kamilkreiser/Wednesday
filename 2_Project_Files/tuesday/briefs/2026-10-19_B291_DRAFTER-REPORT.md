# B291 drafter report (2026-10-19 ~19:50 AEDT)

Brief: `2026-10-19_B291_SEAT-G11_hpsmpoc-gate-pr163-tier2.md` (round 1 of 2 gate, tier 2, Sonnet, pane `Datasec/HPSM-POC-G11`) for draft PR #163 @ e3050549 (HPSMPOC-267, -293, -275, -263). Shape copied from B286 (read whole). Read WHOLE: B286 brief and drafter report, B288 STATUS, first ~80 lines of the B288 brief (REFUSE, partition, items 1-2). Read-only commands used: `ls-remote`, `gh api` GETs (pulls/163, pulls/163/files, check-runs on the head, open PR list), `git diff --name-only e4f270e 2a0c541`, `date`, `uptime`, `lsof`, `ls`. No git write verb, no dotnet, no Jira, no Artifact/Docs/mail/chat.

## Slots (three tokens, all in the Stamp line, each once)
| Slot | Default / source |
|---|---|
| `STAMP_TIME` | Tuesday's clock at stamping, `YYYY-MM-DD HH:MM AEDT` |
| `PORT_BLOCK` | Propose `7270-7279 (none expected)`. MEASURED 19:4x: `lsof -nP -iTCP:7200-7299 -sTCP:LISTEN` = 0 listeners. In-process host, no server needed |
| `B_NUMBER_CONFIRM` | `B291 confirmed` after a folder check (MEASURED: 0 B291 files in project `Briefs/`; in Tuesday's `briefs/` only these two drafter files) |
Model, pane, suffix and both shas are literal. The REFUSE line and stamp section name the token shape without writing a matching token; only the Stamp line carries the three tokens (Tuesday should confirm with `grep -o`, since `grep -c` counts lines).

## MEASURED by the drafter (19:42 AEDT)
- `ls-remote`: main `2a0c5412760346bca6482f2c61d44bf84a814f3e`; branch and `refs/pull/163/head` `e3050549f20178afa13c822827504cbde2e8bc1d`.
- PR #163: open, draft, 4 commits, 5 files, +775/-14; GitHub shows base = current main `2a0c541`, branch actually based on `e4f270e`. Files: `ImportEndpoints.cs` +57/-14; `ImportFailPathTests.cs` +173; `ImportSweptUploadTests.cs` +118; `ImportUtf7Tests.cs` +242; `ImportWordsTests.cs` +185.
- Disjointness: `git diff --name-only e4f270e 2a0c541` = `PkcsInPackageTests.cs` + 3 `web/e2e` specs; no overlap with the PR. Only open PR is #163.
- Check runs on the head: dependency review and gitleaks success; CodeQL queued; Analyze x4, api, both SQL Server shards, web unit, web build, infra in progress. CI PENDING; r8 conditional.
- Load 7.54 7.19 7.21 (at the 8 line).
- Note: bare `gh` was unauthenticated in the drafter shell; GETs used the project's `GH_CONFIG_DIR` (read-only use).

## Gate design choices
- Independent RED is two instruments per item (builder's files on the `e4f270e` tree, plus the gate's own probes), for 4 items, per-ticket tokens plus an overall.
- Seat-specific traps added over B286: T-b ("nothing was read" truth per shape), T-c (endpoint catch cannot separate causes; NotSupportedException from outside the read must stay 500, probed through the endpoint, plus charset sweep), T-d (the builder's self-declared non-idempotent ambiguous-commit retry: driven, duplicate `import.failed` audit), T-e (the -263 status read vs sweep partial state, reasoned from `ImportPendingSweep.cs`), T-f (the new 3307 operator log line: fields and exception text), SQL Server shards as the only evidence for unrun SQL Server branches.
- Word census expectation: 0 new user-facing literals, 2 removed.

## Judgement calls for Tuesday
1. The B288 brief was read only to line ~80 (REFUSE, partition, items 1-2); items 3-4 text taken from the builder's STATUS, which is the claim anyway.
2. The brief is long (about 30 KB, B286 style). Heavy rows are many (r1, r3, r4, r6); expect a long gate under load 7-8. Priority order is in the brief.
3. r7(d) asks the gate to look at `openapi.yaml:950` by `git show` only; the brief's own partition forbade the builder from the contract, and the gate is told to open nothing else of it.
4. The head may move (draft PR); the REFUSE row says test the READY sha only. If it moves, edit both the `.pre-stamp` copy and the stamped copy.
5. Unverified: the commit short sha `e305054` for the head is taken from the builder's commit list (head `e3050549`); the brief uses both consistently.
