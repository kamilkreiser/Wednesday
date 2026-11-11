STARTABLE: YES

# B1494 DRAFTER REPORT | SEAT-M113 | MPSCALC lane L2 (API stores)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1494_SEAT-M113_mps-lane-l2-api-stores.md` (85 lines), with an identical `.pre-stamp` (sha256 both `f7cf80b4def2455d5795c0000a6115223676c4f88fdcb05377459c9660ddae57`, `cmp` equal). The drafter worked 13:44-13:55 AEDT 2026-11-11 (`date` prints).

## BLUF
- **5 of the sweep's 6 L2 tickets are in; MPSCALC-163 is dropped.** Its only open clause ("20 group runs green under load") needs a loaded machine (load >= 30) that no seat may make (gate record B157-13), and the kit's HEAVY rule forbids heavy jobs above load 7.
- What each ticket still needs, read from its newest records comment:
  - **122:** the three missing hosted rows (400, 500, 503). Tests only.
  - **123:** the ticket's streaming option. The concurrency-bound option needs a setting and is not built.
  - **98:** a recorded mutant run. It makes no commit.
  - **99:** the stage route's lock-wait bound counted from arrival.
  - **217:** clause (b), a repeated supply row refused.
- **217 carries a precondition.** The earlier builder (B518 D4) did not refuse repeated supply rows because "the importer may write such a store". The drafter read the source (DERIVED): the importer has refused a repeated (model sheet, supply SKU) as a Blocking finding since its first commit. The kit makes the seat prove that again before it edits anything, and STOP if the proof fails. The gates B538 and B552 said a ticket-scope decision was owed on this narrowing. See D2/Q2.
- **Set-up:**
  - Branch `b1494/mps-api-stores`: one branch, 4 commits (122, 123, 99, 217). 98 makes no commit.
  - Base: drafter read main `54ed7627`. Open PRs 0. No `b1494` ref.
  - Ports 9620-9629 (free). Pane `Datasec/MPS-M113`.
  - Model: Sonnet, row C2 `model-routing.md:92`. Gate G1 `:108`.
  - Clocks: READY +210, HARD STOP +300. Context band and HANDOVER included.
- **Git identity follows the 11-11 rule.** The clone takes the identity the project repo itself configures in `2_Project_Files/.git/config`, read by program. No `-c`, no `GIT_*` variables. READY prints `%ae | %ce` for every commit. This differs from B1405 (round of 11-10), which set the GitHub noreply identity. See Q5.

## Facts re-measured (instrument; control)
1. Ticket reads. Jira GET by an in-process reader of the project `.env`, nothing printed. JQL `project = MPSCALC AND ( key in (MPSCALC-122, MPSCALC-123, MPSCALC-98, MPSCALC-163, MPSCALC-99, MPSCALC-217) )`, 13:44:29. All six read Backlog.
   - Comment counts: 217 2, 163 3, 123 0, 122 1, 99 1, 98 3.
   - Control: `key = MPSCALC-361` read Done.
   - Newest comments: 122 at 2026-11-10 15:47:39 and 99 at 2026-11-10 15:47:04. Both say a build releases the open clause; neither asks for a ruling.
2. Origin main `54ed76273cf5e7eb804315635c413034f28b3372`. Read by `gh api -X GET .../git/ref/heads/main` at 13:44:53 and again at 13:52:08.
   - Open PRs 0.
   - `matching-refs/heads/b149` read 0 and `b1494` read 0. Control: `heads/b1405` read 1.
   - Tree: 777 blobs, `truncated=false`.
3. Merged PRs that name lane keys. Instrument: `pulls?state=closed` paginated, 175 rows (#1-#175), full-key regex.
   - Hits: #171 (122), #170 (99), #58 (163), #34 (98), #146 (361, the control).
   - **This regex MISSED #102 for 217.** #102's body writes "-217", and the records comment names #102. That is a false absence in the drafter's own instrument. The kit's PRIOR WORK line now matches the short form and requires #102 as its control.
4. Every `file:line` in the kit was printed by `grep -n`/`awk NR` over raw `contents?ref=54ed7627` at drafting.
   - One pointer was wrong in the first write and is corrected: the B157-13 quote is at `2026-10-16_B157_STATUS.md:382`, not `BACKLOG.md:382`. `BACKLOG.md:3489` names the finding.
5. CI file `ci.yml`, 123 lines.
   - dotnet job: `:31`, `:42`, `:43`.
   - python loop: `:86`.
   - package job: `:114`.
   - `global.json` reads 10.0.100 with `latestFeature`. The local SDK `--version` printed 10.0.401.
6. Rule 8 check (CI tests that read changed files): `scripts/tests/test_deploy_pre1.py:36` opens `CatalogueOverlayStore.cs`. That is 98's mutant file. The kit forbids committing to it, keeps the mutant throw-away, and has the seat run its own search.
   - Instrument: `grep -c -i -E` over 4 python test files. The search hit 2 files; `test_package_scan.py` returned 404 (it does not exist).
7. Ports and panes.
   - `lsof -nP -iTCP:9600-9699 -sTCP:LISTEN` printed 0. Control: unfiltered 12.
   - A `-w` scan for `96[2-3][0-9]` over the 63 non-`.pre-` SEAT kits of 10-11 Nov found 0. Control: `95[0-4][0-9]` hit 4 kits.
   - No `Datasec/MPS-*` pane.
8. Machine and tooling.
   - Load 4.19 at 13:50. 1337 GiB free.
   - Node 24 `v24.22.2` present.
   - The NuGet machine cache now holds `microsoft.identity.web/4.16.0` and `system.security.cryptography.xml/10.0.13`, the two packages B1405 had to fetch.
9. Git identity.
   - `git config --show-origin --get user.email` in `2_Project_Files` printed `file:.git/config`, a Datasec corporate address. `user.name` is set too: 2 `user.*` keys.
   - Main's commits carry the `kamilDatasec` noreply address as author.
10. 217 precondition (DERIVED from source, over the stale local checkout's history).
    - `PriceBookImporter.cs:195` `Duplicates(map.Supplies, ... "DATA-IMP-005")`.
    - `:61` `Block` = `ImportSeverity.Blocking`.
    - `:16` `Succeeded` is false on any Blocking finding.
    - `git log -S 'Duplicates(map.Supplies'` and `--diff-filter=A` both printed `6e65e6c`. Control: `-S` of a no-such string printed 0.

## D-decisions (the drafter's, in the kit)
- **D1 Drop 163.** Reason above. Built evidence would need either synthetic load on a shared machine or a ruling on how "under load" is produced.
- **D2 Keep 217, gated by P217.** The ticket text asks for the refusal. The only stated reason against it is refuted by source. The one test removal allowed is the control method `StoreLoadRows.cs:134`, whose assertion is the behaviour the ticket reverses.
- **D3 123: streaming only.** The ticket offers two shapes and says the setting one is the coordinator's call. Streaming needs no new setting, status or word. RSS is recorded as a measurement; it is a pass/fail row only if stable over 3 runs.
- **D4 99: "arrival" = the handler's entry, before the body read.** This matches the overlay's existing endpoint-count reading. Clause 5's overlay-alongside row is not asked; records read it "NOT RE-DERIVED", not NOT MET.
- **D5 122: red-first by planted fault.** The fix is already on main, so new rows are green at base.
- **D6 Sonnet, row C2.** The sweep sets L2 to Sonnet. The G1 gate covers the product surfaces.

## Q-questions for Tuesday (each with a default; also in Stamp S4)
- **Q1** Drop 163? Default **yes**.
- **Q2** Build 217 (b) on P217's proof without a product-owner word? The gates said "a ticket-scope decision owed (Tuesday / the product owner)". Default **yes**: the ticket's own text is the decision, and the precondition answers the builder's caution. If Tuesday reads it as the product owner's, drop 217 from S4 and the seat leaves it.
- **Q3** 99 arrival = handler entry? Default **yes**.
- **Q4** 123 streaming only, the bound left as RESIDUE? Default **yes**. Consider Opus for this seat if Tuesday reads the upload path as a C3 security-design surface. Default: no, Sonnet plus a G1 gate.
- **Q5 Git identity.** The kit follows the new DRAFTER rule: the project repo's configured corporate address, not the noreply identity B1405 used. If GitHub's email-privacy setting refuses the push, the seat STOPs. Default: as written. Tuesday may prefer to rule that the repo's configured identity in a seat clone means the noreply one.
- **Q6 NuGet registry fallback** (after the machine cache) is allowed into a seat-local cache. Default **yes**, as earlier MPS seats did. The cache now holds the two missing packages, so it is likely unused.

## UNMEASURED
- Whether the hosted rig can reach 400 ACT_AS_INVALID and 503 for the download. The source suggests yes. The kit STOPs if not.
- The full dotnet suite duration on this machine.
- Whether any hosted reference store holds a repeated supply row. Not readable by any seat; P217 covers only importer-written stores.
- RSS figures for 123 at head.
- Whether L1/L3/L4/L5 kits are being drafted now with overlapping port blocks. The drafter scanned only kits on disk at 13:48.

## Outside the fences (disclosure)
- Scratch: `/private/tmp/b1494-drafter/` holds `jira.json` (ticket text, no secrets), `tree.json`, `prs.jsonl` and raw source copies under `src/`. Not in any project folder. Left for Tuesday to remove.
- The Jira reader ran inline (python on stdin). No helper file was written.
- No git ref, Jira, GitHub or project write. Git verbs in the project repo: `log`, `config --get`, `rev-parse` only, with `--no-optional-locks`.
- No `decision_queue.sh`, no `briefs_staged`, scoreboard, `_ledger.md` or non-Datasec tree read.
- Three files written as instructed: the kit, its `.pre-stamp`, and this report. The rules file names two; the commission names the third.
