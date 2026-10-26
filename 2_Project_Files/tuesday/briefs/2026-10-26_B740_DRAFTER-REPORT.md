STARTABLE: YES (head, main and merge ref unmoved at 14:22:00; launch only through launch_when_cool because load1 read 7.11 at 14:13 and the one live MPS seat, G143, is mid-matrix)

# B740 DRAFTER REPORT: MPS PR #118 round-2 gate (SEAT-G148), drafted 14:12-14:22 AEDT 26 Oct

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B740_SEAT-G148_mps-118-parity-round2-gate.md` (95 lines, 8 four-underscore lines: 7 stamp slots S1-S7 + the last line `READ-WHOLE-BY-TUESDAY: ____`; grep `-c` = 8, control 1; `@[A-Z_]+@` 0 with control 1; non-ASCII 0; person names 0).

## BLUF
- **Correction to the commission first: B728 is NOT the round-1 gate of MPS PR #118.** `ls briefs | grep B728` returns the NexusAI gate of ITS OWN PR #118 (`datasecau/Reporting_Dashboard_Au`, kit `B728_SEAT-G140`), and the path you gave for the B728 STATUS does not exist in the MPS Briefs folder (my Read failed). The MPS round-1 gate of PR #118 is **B715 (SEAT-G135, tier 1)**, STATUS `Briefs/2026-10-26_B715_STATUS.md`. I used B715 as the shape template and lineage, B732 (the live MPS round-2 strict gate of PR #117) for the cap form, and B728 only as the form of the stamp/slot block you named. The kit carries a NAME WARNING about the NexusAI #118. If you meant B728 literally, say so; the findings in the kit are B715's.
- **ROUND COUNT, from the verdict lines:** B715 line 1 `NO GO round 1 of 2 (NO GO 0 of 2 before this gate)`, line 208 `NO GO (round 1 of 2; CI complete)`, line 183 `NO GO, so 1 of 2 on the class`. Kit states it as **"NO GO 1 of 2 on class 'a count-preserving panel tamper says AGREE'" before this gate; a same-class Major/Blocker here is NO GO 2 of 2 = the cap, no round 3, a card.** Frame: first lines of 251 STATUS files matching `panel|parity|multiset|MPSCALC-302|ParityProof`: 9 files, exactly one a NO GO (B715); control B715's first line matches `GATE VERDICT`.
- **Tier: 1 (G1, Opus), confirmed with an argument** (below). Launch line carries `BRIEF_SEAT_LEVEL=opus`, pane `Datasec/MPS-G148`, B740, ports 9400-9409.
- The subject is exactly as Tuesday measured: PR #118 head `db45e7a6` = ONE commit on `39e51272`, 2 paths, +5 -3 and +163 -0. main is `2e7f9d8a`; the five paths main gained since the branch point are all Api/docs, none in Import, so main moving is not a stop.
- The gate's heart (C2/C3) is built to decide the cap fairly: a stated PROPERTY and a SURVIVOR RULE (a survivor counts toward the class iff a test-only store exists where the head refuses and the mutant AGREEs; the builder's N13/N14 "different sentence only" shape is a Minor ticket line unless the gate PRINTS an AGREE-set difference), an independent oracle differential between `39e51272` and `db45e7a6` over a bounded exhaustive domain (with a control that reproduces round 1 from the un-distinct list), and the one known behaviour change (A4: a block listing a SKU twice whose records are exactly the owed set now AGREEs) fenced as a printed Note while any OTHER loosening is a Major of the class.
- **CI paused is written into the kit as a CONDITION:** `CI pending: not scanned (job not started)`; verdict at best `GO WITH FOLLOW-UPS (conditional: CodeQL not scanned)`; three reads, no loop; this overrides round 1's "analysis missing = Major" only for jobs that never started.

## Facts re-measured (instrument, clock, control)
| fact | value | instrument and clock | control |
|---|---|---|---|
| refs | main `2e7f9d8a`; branch = `pull/118/head` = `db45e7a6`; `pull/118/merge` `c8b0326b` (parents `2e7f9d8a`, `db45e7a6`; tree `9d1c4a73`); `pull/117/head` `a284048e`; `pull/119/head` `66f43cb6`; b7*: b711 b720 b74 b75 b79 | `git ls-remote` 14:12:58 and again 14:22:00 (unchanged) | `refs/heads/b711*` = 1 line |
| PR | open, not draft, 2 commits, 2 files, +324 -3, mergeable true / blocked, title MPSCALC-302 | `gh api -X GET pulls/118` 14:13:05 | `state=closed` lists #119 |
| new commit | parent `39e51272`, tree `6d78f7c5`, files +5 -3 (blob `19d5302b`), +163 -0 (blob `d37e2d60`), unsigned, one Sonnet trailer | `commits/db45e7a6`, `compare` 14:13:23 | raw files `git hash-object` equals both blobs; bad sha reads 404 |
| main drift | `compare f5a27af0...2e7f9d8a` ahead 2: `docs/API.md`, Api `.csproj`, `PurchaseValidation.cs`, `QuoteEndpoints.cs`, `QuoteWalkCaps.cs` | `compare` 14:13:05 | `1ac8ab8a...2e7f9d8a` lists the single `.csproj` |
| product file | 509 lines, 28,679 B, sha256 `e7ef58dd...d876`; `Distinct(` 3 (`:193` fix, `:446`, `:447`); fix line 1; `SequenceEqual` 1 at `:199`; sentence 1 at `:201`; `StringComparer.Ordinal` 12 | raw `contents` + grep `-c -i -F`, 14:15 | `zzz-no-such-string-7f3a` = 0 |
| test file | 312 lines, 18,151 B, 10 `[Fact]` (4+6), 1 class line, non-ASCII 0; 6 new names listed | raw read, grep, 14:15 | same control |
| checks | 8 check-runs all completed in 2-3 s: 7 failure, `package` skipped; annotation on `dotnet` 121377481148 and `Analyze (csharp)` 121377468473 = "job was not started because recent account payments have failed..."; no `CodeQL` umbrella row; runs `ci` 40262434379 and `dynamic` 40262429275 failure | `check-runs`, `annotations`, `actions/runs` 14:13:42 | `commits/1ac8ab8a/check-runs` shows 4 Analyze success |
| code scanning | 4 analyses on the PR ref, all at `39e51272`, 0 at `db45e7a6`; alerts open/fixed/dismissed 0/0/0 (uncontrolled zero); main's latest scan `1ac8ab8a`, none at `2e7f9d8a` | `code-scanning/analyses|alerts` 14:13 | main list non-empty (4 rows) |
| ruleset | deletion, non_fast_forward, code_scanning CodeQL errors / high_or_higher, required_status_checks empty | `rules/branches/main` 14:13 | n/a |
| squash settings | `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`; squash, merge, rebase all allowed | `repos/<R>` 14:14:54 | n/a |
| PR body | stale: "+9 -2", "4 rows", one Opus attribution line | `pulls/118 --jq .body` 14:14:54 | n/a |
| landing rule | `CLARIFICATIONS.md:809` "squash with the head pinned (`--match-head-commit`, the MPS convention, entry 04:52 above)"; project `CLAUDE.md:50-52` | `grep -n -i` 14:13:30 | zzz string 0 |
| routing | G1 `:108`, G2 `:109`, G-cap `:111`; model ids opus `claude-opus-5-5` (json line 17), sonnet line 23; `brief_seat.sh:24` defaults to opus | `grep -n -i -E '^\| (G1|G2|G-cap) '` 14:22:00 | zzz string 0 |
| panes | `tuesday`, `HPSM-POC-H36`, `Security-Composer-J21`, `Security-Composer-G146`, `HPSM-POC-G147`, **`MPS-G143`**, `fleet-monitor`. MPS seats live: **only G143** (B732, gate of PR #117, ports 9920-9929, `.tools/b732`); no MPS-M31, no G148 | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` 14:12:58 | n/a |
| heavy slots | `heavy-slot-2` only, holder `B732 12:37:29 mutant_matrix` (held 1 h 38 min); slots 1 and 3 free; G143 matrix scripts running at 14:15, heartbeat mtime 14:15 | `ls`, holder `cat`, `ps` 14:14-14:15 | `ls -d .tools/b732` lists |
| load | 7.11 8.97 9.27 | `LC_ALL=C uptime` 14:13 | n/a |
| names free | `B740` and `G148` in no briefs file; `.tools/b740`, `.tools/wt-b740-*`, `refs/heads/b740*` none | `grep -r -l -i`, `ls`, `ls-remote` 14:14-14:16 | `G143` appears 6 times in its kit |
| ports | **9400-9409**: `lsof` rc 1; word-boundary scan `(^|[^0-9a-f])940[0-9]([^0-9a-f]|$)` over 130 non-`.pre-` SEAT kits of 10-25 and 10-26: **0 hits** | `lsof`, scan 14:14:26 | scan for `974[0-9]` hits 14 files; python bind on 127.0.0.1:9400: rc 0 / 2 lines while bound, rc 1 after free |
| builder STATUS | 233 lines, last line `READY FOR QA: B731 ... @ db45e7a6...` (head pin count 1, control 0), `## PRIOR WORK` count 1 | grep `-c` 14:15:24 | zzz string 0 |

Port-scan hits to report: none for 9400-9409. Other live-block facts: B732 holds 9920-9929 (live); B715 9820 and B731 9730 are finished. A span census showed the only `94xx` spans are 9480-9489 (B611, B681), not overlapping.

## D-decisions (mine; Tuesday accepts or overrides at the stamp)
- **D1 Tier 1 / Opus (confirm, with the argument).** G1's literal list (`model-routing.md:108`) is security surfaces, data destruction, deploying, client-tested; it does not name the parity tool. G2 (`:109`) is "tests-only, ... follow-ups whose mechanism a prior gate already measured", which this round's mechanism arguably is. I confirm G1 because: the diff changes a PRODUCT byte (not tests-only); the round-1 gate on this very mechanism ran G1 and found the two Majors; the round-2 builder's stamp already ruled tier 1 ("the parity tool, product code"); and this is the cap, where a miss is final and a Sonnet gate has no measured record against a self-built mutant battery here. Alternative if you disagree: Sonnet with `BRIEF_SEAT_LEVEL=sonnet`, but then the cap gate is the weaker instrument.
- **D2 Round-count wording** as above, read from verdict lines, plus the rule that a non-class Major (hygiene/claims) is a NO GO that does not spend the cap and must be labelled so.
- **D3 CI-paused grading** as above (condition, three reads, no loop, override of round 1's G-6 for not-started jobs, an existing analysis with a NEW alert is still a Blocker).
- **D4 Survivor rule** (AGREE-set difference counts; sentence-only differences are Minor tickets; equivalents proved by enumeration with a failing control). This is what keeps N13/N14 from being an unfair cap-spending NO GO and also what stops a real hole hiding behind "out of scope".
- **D5 The A4 loosening** is fenced as a FACT/Note (Tuesday's accepted Q-1 in the B731 stamp, and B715's own fix shape produces it); any other loosening is a Major of the class. The gate prints both answers.
- **D6 Oracle differential** between `39e51272` and `db45e7a6` over a bounded exhaustive domain, statement-level plus store-level, with the un-distinct control. This is the "nothing loosened against the round-1 head" proof.
- **D7 Local CI line stands in for the hosted line** (whole solution once at the combined tree; hosted Linux and the hosted `PublishOutputTests.B160` are NOT TESTED).
- **D8 Port block 9400-9409**, chosen because no kit of the last two days names it (control fires) and nothing listens.
- **D9 Fences:** builder trees (`.tools/b731`, `b711`), the round-1 gate's trees (`b715`) and the live gate's (`b732`) are READ-FORBIDDEN; B715's evidence TEXT readable only after the gate's own tables exist; B731 has no evidence folder (checked). Nothing is named as REUSE (the NexusAI B728 kit names none for this repo).
- **D10 Times:** target verdict 150 min, hard stop 4 h after Step 0, never later than 18:30 AEDT (the B731 window); Tuesday stamps.
- **D11 Landing text** quotes `CLARIFICATIONS.md:809` and states Tuesday lands only after a real CodeQL scan exists (which cannot happen while jobs do not start); squash subject is the PR title with two commits; the stale PR body is Tuesday's edit.

## Q-questions for Tuesday (each with a default)
- Q-1 Is B715 (not B728) the round-1 gate you meant? Default: yes, the kit is built on B715.
- Q-2 May the gate build scratch rows, weak copies, plants and mutants only in `.tools/wt-b740-mut`? Default: YES (the same grant as B715's Q-1; without it C2/C3 are NOT TESTED).
- Q-3 Tier: G1 Opus (default) or G2 Sonnet?
- Q-4 The accepted A4 loosening: Note (default) or does the product owner want it refused with a new sentence? Default Note; a new sentence is his word and is not taken.
- Q-5 Launch order: G143 holds heavy-slot-2 and runs a long matrix; slots 1 and 3 are free, load1 is 7+. Default: one waiter through launch_when_cool at load1 below 7 on two reads; the gate takes slot 1.
- Q-6 Do you want the gate to read CI three times (start, mid, verdict) as written, in case the Actions ruling lifts? Default yes; a re-run is Tuesday's, never the gate's.
- Q-7 The PR body (stale counts, Opus attribution line) and the squash text: Tuesday's edit before landing. Default: noted in the kit as Notes.

## UNMEASURED
No build, test, mutant, clone, fetch or compile was run. Not measured: that R1-R6 are green and R1/R2 red at the unfixed head (builder claims only); that the typed sentences equal the template; the 1120-case enumeration; N13/N14 behaviour and whether they have an AGREE-set difference; the Api count at `2e7f9d8a` (3012 at `1ac8ab8a` is B715's); whether `PublishOutputTests.B160` is green locally on SDK 10.0.401; that my combined tree equals GitHub's `9d1c4a73`; why main's checks at `2e7f9d8a` failed (annotation not read); whether Actions will be re-enabled; the Jira state of MPSCALC-302 (not read); the per-check `steps` count (I read two annotations and the 2-3 s durations, not every row's steps).

## Outside-the-fences disclosure
- I wrote only the two files with Write/Edit. By shell redirection I also wrote six scratch files in the session scratchpad (`kits.txt`, `pp_head.cs`, `test_head.cs`, `prod.patch`, `ctl.txt`, `ctl2.txt`), outside the briefs folder; no project file.
- I briefly bound 127.0.0.1:9400 with `python3 -I` (a port-control, freed in the same command, rc 1 afterwards).
- I read the NexusAI gate kit B728 (another repository's kit, in Tuesday's briefs folder) because you named it; nothing of it is carried. I did not open any NexusAI project folder.
- I read the first 600 bytes and the last line of the live gate G143's STATUS, listed `ls -la` on `.tools/heavy-slot-2` and `ls -lt` on `.tools/b732/logs/` (names and mtimes only, no log content), read the holder file, and ran `ps -axo ... | grep 'Datasec MPS Commercial'` whose output included other seats' command lines (it printed part of the G143 launch prompt line). No driver, matrix script or mutant file of another seat was opened.
- `grep -n` for the routing rows was first run case-sensitively (the hook advised); re-run with `-i` and a control at 14:22:00. Every `gh api` call was `-X GET` under the MPS `GH_CONFIG_DIR`; no `git` verb other than `ls-remote`, `cat-file -t` and `hash-object` on scratch copies; no Jira, no `.env`, no decision-queue, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree.
