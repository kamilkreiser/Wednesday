# B572 DRAFTER REPORT (2026-10-24, Sonnet drafter, read-only; clock: finalised 2026-10-24 10:03 AEDT per `date`; earlier reads in this report carry their own)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B572_SEAT-H11_hpsmpoc-test-followups-334-336.md` (124 lines; sha256 `ee5bbbac7678172b3aca17dd43a84b31d78fa6a50a4abfa85878dd6d01e81a9a`) and its `.pre-stamp` copy (`cmp` equal). Unstamped copy reads **8** lines with the four-underscore pattern (`/usr/bin/grep -c -E '_''_''_''_'` = 8; control: a scratch line holding four underscores = 1); 0 non-ASCII bytes (control: a planted 0xC3 0xA9 = 1; the first draft DID hold two raw U+0660/U+0669 characters in the X-nonascii-digit-class mutant text, found by this check and replaced by the escape text `\\u0660`/`\\u0669`); 0 HH:MM clock tokens in the brief (control: a planted "09:56" = 1). **Stamper dry-run:** `stamp_brief.py` run on a scratch copy of the brief with all 8 labels (STAMP:, LAUNCH WINDOW:, Stamped by, Launch authority, Hard stop and target READY, Head and main at launch, Model receipt line, READ-WHOLE): "OK: 8 slots stamped by label, 0 four-underscore lines left". Every slot line ENDS with the slot (the current stamper requires `rstrip().endswith`), so I moved B558's trailing parenthetical guidance out of the slot lines into one paragraph above them.

## What I read (paths, shas)
- Template shape: `briefs/2026-10-24_B558_SEAT-H8_hpsmpoc-test-followups-329-332.md` (118 lines), its `.pre-stamp` (diff = the 7 slot lines + READ-WHOLE line), `briefs/2026-10-24_B558_DRAFTER-REPORT.md`, HPSM-POC `1_Project_Definition/Briefs/2026-10-24_B558_STATUS.md` (not opened beyond what B558's brief quotes: the brief, pre-stamp and report were the template; I did not read the STATUS body, say so plainly); `briefs/2026-10-24_B571_SEAT-H10_...md` and its `.pre-stamp` (Yours list, port block 9200-9209); `tuesday/tools/stamp_brief.py` (read whole: label matching).
- Findings: `Briefs/2026-10-24_B559_STATUS.md` lines 90-104 (mutant tables), 138-172 (B559-1..-8, FOR TUESDAY), 185-194 (UNMEASURED); `Briefs/2026-10-24_B563_STATUS.md` grep of the ticket rows (lines 9, 105, 113-115, 154-156, 166-168, 191-193, 203-205) and FOR TUESDAY (320-332).
- Jira REST GET (credentials sourced inside the process, never printed; the first discovery step printed only variable NAMES): HPSMPOC-334, -335, -336 whole, 0 comments each, all Backlog, label `b563-2026-10-24`. No JQL was run (fence: every JQL begins `project = HPSMPOC AND`; none needed).
- HPSM-POC main `08af828bd0eff92c82169e240fb4d6d9f5dc2fe7` (`git --no-optional-locks ls-remote origin refs/heads/main` in `2_Project_Files`, read twice, same). Read by `git show 08af828b:<path>`: the three test files, `Support/HostStartRetry.cs`, the Feedback twin (blob only), `web/src/api/client.ts:312-330`, `ci.yml:240-262`.
- Blobs at main: attribution-preview.test.ts `78672e87...` (250 lines); client.describeFailure.test.ts `f2516a27...` (226); ApiFactoryHostStartRetryTests.cs `e4c5cb2d...` (409); HostStartRetry.cs `e402defe...` (64); client.ts `f49adb1d...` (356); Feedback twin `d164d875...` (63).
- Also read: `fleet/specs/model-routing.md` (grep only), `tmux list-panes`, `lsof`, `uptime`. Not read: decision_queue, fleet_ack, scoreboard, briefs_staged (fenced), the `.tools` of the project beyond `ls -d` of five paths.

## Premises, each with the line read
1. 334: `attribution-preview.test.ts:22` `const EXACT_NUMBER = /(?<!\d)(?:777|4321)(?!\d)/;` (count 1, control `NOSUCH-zz7f3a` 0); `:180` NUMBERS; `:206` `const DIGITS = codePoints([0x30, 0x39]);` (count 1); `:217` the self-check row title "the characters beside the numbers are whole"; header comment `:18` says "only a digit beside 777 or 4321 exempts it" (count 1).
2. 335: `client.describeFailure.test.ts:147` `it.each([`, cells `:148-155` (8), title `:156` (count 1); `:155` the `firstname` cell; `client.ts:322` `first?.field === "name"` (count 1).
3. 336: `HostStartRetry.cs:32` `for (var e = exception; e is not null; e = e.InnerException)` (count 1); `ApiFactoryHostStartRetryTests.cs:29` `Forge`, `:233` `OtherLockText`, `:265` `Wrapped` (count 1), `:344` `IsMigrationsLockLost_is_true_for_the_lock_fault_inside_other_exceptions`; 12 `[Fact]`/`[Theory]` attributes (count by `grep -c -E`); the only `InnerException` hits in the Api test file are `:211` and `:224` (chain walks in an earlier row), i.e. no row forges a fault WITH an inner exception.
4. CI: `ci.yml:249-253` the two SQL Server shard filters (`~Assessment.` and `!~Assessment.`): `Hosting.*` is on shard 2 only.
5. Ticket texts (BLUF quoted verbatim in the brief) and the gate fix-shapes (`B559_STATUS.md:142-144`).
6. Compare control: `compare/31dabc8d...08af828b` lists exactly the three paths (checked, 3 lines); `pulls/205/files` = `SnapshotLauncher.edgeTrim.test.tsx`, `SnapshotLauncher.tsx`; `pulls/205` head `b564/hpsmpoc-333-snapshot-name`, state open, mergeable_state blocked.

## Partition program (run by `python3 -I`, scratchpad `partition.py`; Yours = the 3 test paths at main `08af828b`)
Lanes: open PRs from `pulls?state=open` (1) with `pulls/<n>/files --paginate`; B571's Yours list (from its brief: web/package.json, web/package-lock.json, web/scripts/audit-dev.mjs, web/src/audit-dev.test.ts, .github/workflows/ci.yml); every live `refs/heads/b5*` (20) by `compare/main...<branch> --paginate`.
```
lane                                                            n paths  shared shared paths
PR#205 (b564/hpsmpoc-333-snapshot-name)                               2       0 []
B571 Yours (brief)                                                    5       0 []
branch b50/feedback                                                  48       0 []
branch b501/hpsmpoc-telemetry-smaller                                17       0 []
branch b503/hpsmpoc-310-bare-day-test                                 1       0 []
branch b51/collateral                                                14       0 []
branch b510/hpsmpoc-479-1-runner-env                                  4       0 []
branch b512/hpsmpoc-web-test-defects                                  3       1 [attribution-preview.test.ts]
branch b513/hpsmpoc-describefailure-400                               2       1 [client.describeFailure.test.ts]
branch b514/hpsmpoc-timing-floor                                      1       0 []
branch b515/hpsmpoc-host-start-retry-feedback-pins                    5       1 [ApiFactoryHostStartRetryTests.cs]
branch b516/hpsmpoc-n1-lease-lost-flake                               2       0 []
branch b526/hpsmpoc-edge-characters-refused                           9       0 []
branch b548/hpsmpoc-400-customer-name-only                            2       1 [client.describeFailure.test.ts]
branch b55/client-followup                                           66       0 []
branch b558/hpsmpoc-test-followups-1024                               3       3 [all three]
branch b56/content-050                                               55       0 []
branch b56/gate-notes                                                 4       0 []
branch b564/hpsmpoc-333-snapshot-name                                 2       0 []
branch b58/feedback-live                                              2       0 []
branch b59/hosted-web                                                44       0 []
branch b59/signin-hardening                                          17       0 []
TOTAL shared over all lanes: 7
CONTROL planted shared path in one list -> found (1, expect 1)
CONTROL b558 branch vs Yours -> 3 (expect 3: #204 touched the same 3)
```
**Intersection against PR #205: EMPTY. Against B571's Yours: EMPTY. Against every other open PR: there is no other (1 open PR).** The non-empty rows are five branches, all squash-merged history, classified by a second program (`pulls?state=all&head=datasecau:<branch>`): b512 -> PR #198 merged (squash `2d05b95a`); b513 -> #197 merged (`2c94b9b0`); b515 -> #201 merged (`ee73c290`); b548 -> #203 merged (`31dabc8d`); b558 -> #204 merged (`08af828b`). Owner of each: the merged PR (history, no live pane). The live panes at the read: `tuesday`, `Datasec/HPSM-POC-H10`, `Datasec/HPSM-POC-G75`, `Datasec/MPS-G74`, `MPS-M9`, `MPS-G73`, `MPS-G72`, `fleet-monitor`: none is on a shared branch. The brief states the rule for the seat's own run (a shared branch is history only if its PR is merged and no pane is on it; otherwise STOP). Live seats named NOT yours in the brief from both sides: G75 (gate on #205), H10 (B571 zod/braces lane), the MPS panes (another project); and the brief's Not-yours list names Yours as untouchable from H10's and G75's side too (their files named, and "do not touch `ci.yml`, package files").

## Ports
- `lsof -nP -iTCP:9210-9219 -sTCP:LISTEN` printed nothing, rc 1 (no positive control run by the drafter: no bind made, to avoid opening a socket; the brief gives the seat the control).
- Word-boundary scan of every `2026-10-24_*.md` and `.pre-stamp` in `briefs/` for `\b921[0-9]\b` (`/usr/bin/grep -n -o -E`): ONE hit, `9213`, line 11 of the B571 brief and its `.pre-stamp` (read in context: "zod-validation-error 4.0.2 as a peer ... (~9213)" = a package-lock line number, not a port). Control: `\b8940\b` over the B558 brief = 3 hits. The union of port ranges named by today's briefs tops out at 9200-9209 (B571); 9210-9219 is unnamed.

## UNMEASURED
No npm/dotnet/vitest/mutant run. Whether this SqlClient forges a lock fault with an inner exception (the brief gives three routes and an allowed "not forgeable" outcome). That the 160 cells/self-check kill `X-pNd-u`/`X-nonascii-digit-class`; that two padded cells kill Mtrim/Mtrim-start/Mtrim-end (reasoned). The astral block under a non-`u` regex (reasoned). Row counts at main (the 235/134/26 are RELAYED from B559). No SQL Server. The line "Tuesday Sonnet-first grant 2026-10-22" is not in `fleet/specs/model-routing.md` (v1.0 dated 2026-10-18; grep for `2026-10-22` and `sonnet.first` printed nothing): I used your model line verbatim. The positive control for the lsof read.
Load: `uptime` load1 9.91 at my read (above 7) and 7.30 at a later read: the brief's launch rule (< 7) governs; Tuesday launches when cool.

## Judgement calls for Tuesday at the stamp
1. **B559-1 design question is unanswered.** No ruling exists (B563 FOR TUESDAY item 2 asks for it). The brief follows the ticket default: rows pin "a non-ASCII digit does NOT exempt" (true), and says plainly this pins an unruled behaviour. If you would rather get the ruling first, strike Item 1 before the stamp.
2. **NARROWING (1):** the ticket's "file header would then say an ASCII digit" is NOT done (header line `:18` is an existing line, additions only); a new comment above the new table says it.
3. **NARROWING (2):** the Feedback twin test project is not touched (outside Yours; no helper change this round, so nothing to keep in step). Its gap is a FOR TUESDAY item. If you want it in the same round, the partition changes (a 4th path) and the tier stays 2, but it is a second project's test file.
4. **Item 3 hangs on a forge nobody has run.** The brief lets the seat end READY with "not forgeable, reasons in STATUS" (the ticket's own second outcome) rather than STOP.
5. **Size beyond the ticket text:** Item 1 asks for 4 Nd blocks (160 cells) plus a self-check, where the ticket says "two cells" minimum (U+0661, U+FF11). Reason: the gate's mutant `X-pNd-u` is the whole `\p{Nd}` class, so a two-cell fix would kill it but leave a block-specific widening alive; the per-code-point mutant matrix is the part to cut under time pressure (Item 1 says so). Strike to two blocks if you want it smaller.
6. **Item 2 is exactly the ticket's two cells** (at most one more only if a trim-variant mutant survives).
7. **Sequencing:** a PR of this branch opened before H10's zod fix lands will fail the same dependency-audit step #205 fails; named in the brief as Tuesday's to sequence.
8. **Standing lines carried:** SQL Server per-row question (shard 2 only for `Hosting.*`; "column constraints: none"), UNMEASURED-ON-SQLSERVER in the READY, no `pgrep -f` self-wait, `.tools/b572/heavy.lock` for heavy jobs with `.tools/.git-lock` for ref writes only, heartbeat path `.tools/b572/logs/heartbeat.txt`, PRIOR WORK required with `git log -S` / blame, no HP-tool integration, push branch only, no new user-facing words, never delete (quarantine), ports 9210-9219, load1 < 7, model line verbatim.

## Deviations from B558's shape, and why
- Stamp slot lines end with the slot and carry their guidance in a paragraph above (the current `stamp_brief.py` requires lines to END with four underscores; B558's pre-stamp lines carried a trailing parenthetical).
- Three items, not four (no "read and report" ticket like B558's 331); the ticket SCOPE sentences (BLUFs) are quoted verbatim with explicit NARROWING marks, as you asked.
- Two NARROWING marks, a "forge first" step with an allowed no-row outcome, and a guard row (Item 3), because the tickets' premise (that a lock fault with an inner exception can be built) is unmeasured.
- Heartbeat path and quote-the-tail requirement added to the locks line; PRIOR WORK now names `git log -S`/blame commands; standing line 12 for ports with the scan result; SQL Server rule rewritten as a per-row question naming the shard and column constraints.
- The partition section lists the programmed result and requires the seat's own run to classify a shared branch as history only through its merged PR; B558 said "listed, not stops" without a rule.
- Mutants: families are named per Item; the by-program per-code-point matrix is marked cuttable like B558's stamp ruling (4), without waiting for a ruling.
- Fact marks carry no clock (the stamper refuses typed clocks); drafting clocks live in this report only.
- Not copied: B558's "ticket 331 reported" clause and its READY tail; the READY line ends `PRIOR WORK section present` instead.

## Files written
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B572_SEAT-H11_hpsmpoc-test-followups-334-336.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B572_SEAT-H11_hpsmpoc-test-followups-334-336.md.pre-stamp` (byte-identical, `cmp` rc 0, made by `cp` after the final Write/escape fix)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B572_DRAFTER-REPORT.md`
Scratch only (scratchpad, not deliverables): `jira.sh`, `jget.py`, `partition.py`, `hist.py`, `slots.json`, `b572_scratch.md`. No Jira write, mail, chat, decision_queue, publish tool, fetch, worktree or HTTP to a hosted site was used. No git write in any repo.
