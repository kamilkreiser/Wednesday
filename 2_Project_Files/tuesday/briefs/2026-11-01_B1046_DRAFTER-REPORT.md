STARTABLE: YES

# B1046 DRAFTER REPORT - SEAT-M64, MPSCALC-355 walk-cap test gaps (B678-1 to -5), measure first

## BLUF
- **The lane is very likely already finished. The kit is a measurement-only seat whose expected last line is `READY: NO BRANCH B1046 ...`.** The sweep's lane 4 missed the prior work. Builder B821 (2026-10-27) measured all seven variants at `32b09108`: g01-g06 were already killed by committed rows, and g07 was the one survivor. B821 then added the g07 row, which landed as **#129 = `960141b3`**. Gate B829 gave GO WITH FINDINGS, Notes only. Records pass B840 posted comment **40222** on MPSCALC-355: "the acceptance check reads MET". The ticket stayed Backlog only because the old no-move rule (R-R13-1) applied at the time, and the C-79 batches have not judged it since.
- **The sweep's reading of `960141b3` needs a correction.** It covers B678-5 (g07) only, not part of B678-1. g01 and g02 were already red under `WalkCap_null_consumables_..._and_a_full_bom_walk` (from #127) before #129.
- **The product bytes are unchanged since B821 measured.** At `5c64a442`, the sha256 of `PurchaseValidation.cs` is `666064b908a3...` and of `QuoteEndpoints.cs` is `42c7885be82e...`. Both equal the base sha256s in B821's TESTED table. The last commit on each file is `2d55ee19` and `1ac8ab8a`, both ancestors of `32b09108`. `QuoteWalkCaps.cs` has changed only by #129's 13-line insertion.
- **How finishing this unblocks MPSCALC-325 (measured by reading, not run).** Records pass B1021 holds -325 clause 2 on this sentence (comment 40479): "the committed rows do not pin the cap for lines numbered 0 (B678-2 ... filed as MPSCALC-355)". That was true at #112's head `1ac8ab8a`, where the killer rows count 0. It is no longer true at main. The row `WalkCap_bom_lines_that_offend_every_check_list_the_first_twenty_of_each_check` (`QuoteWalkCaps.cs:479-481`, from #127 `2d55ee19`) sends **100,000** BOM lines (`WalkCapLines`, `:17`) numbered 0, -1, -2, ..., each with section id `"bad id!"` (signature `:132`). It asserts the exact list, which holds exactly 20 section-id entries. That is B678-2's own 100,000-line fix shape. B821 and B829 both measured g04 red under it. The kit makes the seat re-run that row alone under g04 and g03 at current main and quote the counts (WHAT THE WORK IS (iv)). With that fact, a records seat can re-judge -325 clause 2. Whether it closes the clause is the coordinator's reading: `CLARIFICATIONS.md:1887` (f) says "not ruled".
- **The seat also adds something no gate has done.** It independently re-makes g02, g03 and g05. B829 re-made only g01, g04 and g06 (plus g07).

## Facts re-measured (instrument, control)
- **main** `5c64a44226614523031a7b2d67cb9bfb477a380e`: `gh api -X GET git/ref/heads/main` at 14:01, under the project `GH_CONFIG_DIR`. `gh auth status` reads the project account, active, ssh.
- **Open PRs:** #121 and #120. Each lists files `web/package-lock.json` only. Control: `pulls/99999` returns HTTP 404.
- **Refs:** `matching-refs/heads/b1046` returns 0 (control `heads/b10` returns 59). B1043's branch is not on origin yet. There are 158 heads.
- **Live-branch sweep:** 157 `compare/main...<branch>` reads. Of the branches fewer than 11 behind, only b789 (#128) and b821 (#129) touch `QuoteWalkCaps.cs`, and both are merged PR heads. 29 older branches, 22 to 126 behind, touch one of the product files.
- **Jira** (urllib GET, project `.env` in process, no token printed; controls: MPSCALC-99999 returns 404, a nonsense text probe returns 0 issues):
  - MPSCALC-355: Backlog, 1 comment (40222), 0 links, updated 2026-10-27T19:19:37.
  - MPSCALC-325: Backlog, 4 comments. The last is 40479 (B1021, 2026-11-01 07:07), which holds clause 2 as quoted above.
- **File sha256 and line counts at `5c64a442`:** read by raw `contents?ref=` and `shasum -a 256`. PurchaseValidation.cs has 366 lines, QuoteEndpoints.cs 1611 and QuoteWalkCaps.cs 749. The test file has 40 `[Fact` and 6 lines with `contains a control character`. Control: `zzz-no-such-string-7f3a` counts 0 in both product files.
- **Anchors:** at `:32`, `:126`, `:131`, `:138` (3 copies of `int before = errors.Count;`, at :138, :149 and :167), `:140`, `:1434`, `:1451`, `:1452` and `:1561`. All are listed in the kit's PINS.
- **Killer-name counts by commit** (5 names; `[Fact` count as control):

  | Commit | Killer names | `[Fact` |
  |---|---|---|
  | `1ac8ab8a` | 0 | 20 |
  | `2d55ee19` | 4 | 38 |
  | `32b09108` | 4 | 39 |
  | `960141b3` | 5 | 40 |

- **Last commit per path** (`commits?sha=main&path=`; control: a made-up path returned nothing):
  - PurchaseValidation.cs: `2d55ee19`
  - QuoteEndpoints.cs: `1ac8ab8a`
  - QuoteWalkCaps.cs: `960141b3`
- **Gate census** (frame: `Briefs/*_STATUS.md` whose first line begins `GATE VERDICT`): 300 files, 69 verdicts, 0 naming b1046 or mpscalc-355, 8 naming walk. Control: B829's line is among the 8.
- **Panes at 14:03:** tuesday, `Datasec/MPS-M61` (B1043, live, `WORKING: Step 0 done, Step 1 starting 14:01`), `Datasec/NexusAI-M62`, `Datasec/NexusAI-M63`, fleet-monitor.
- **`.tools`:** b1043 and its two worktrees exist. There is no heavy slot and no `.git-lock`. Nothing named b1046 or m64.
- **Seat name:** `M64` appears in 0 brief files (control `M63`: 4). `B1046` appears in 0 (control `B1045`: 4).
- **load1** 3.99 at 14:03.
- **CI predicate:** `ci.yml` `:31`, `:42`, `:43`.
- **Routing:** `model-routing.md` lines 85 (L6), 92 (C2), 108 (G1), 109 (G2) and 111 (G-cap), printed by `sed -n`. `models_latest.json` line 38 reads sonnet `claude-sonnet-5-5`, checked 13:27:30.
- **Final marker:** `status_watch.sh:56` fires on `READY:*`, so the no-branch marker is caught.

## D-decisions (in the kit; override at the stamp)
- **D1 Model:** Sonnet, routing rows L6 :85 and C2 :92, the same routing B821 used for this ticket.
- **D2 Gate tier: G2, tier 2 (:109), and only if a branch exists.** I chose G2 over G1 (:108) for three reasons:
  - The lane is test-only and changes no product byte.
  - The mechanism was already measured by gate B678 (its R3). G2 explicitly covers "follow-ups whose mechanism a prior gate already measured".
  - B829 gated the earlier row for this ticket at tier 2 on Sonnet.

  The walk caps are input hardening on the size of a refusal answer. A test row does not change that surface, and G2's hand-off rule to G1 still applies. On the no-branch outcome there is no gate.
- **D3 Expected last line:** `READY: NO BRANCH B1046 ...`.
- **D4 Worktrees:** only `wt-b1046-mut` at first. The fix tree is made only if a variant survives.
- **D5 No fetch** if `5c64a442` is already in the shared object store (B1043 fetches at its Step 1). This keeps this seat's ref writes to at most a `worktree add`.
- **D6 If a variant survives:** at most 6 added test names, one commit, one push.
- **D7 Ports:** none. No listener is needed and no block is reserved.
- **D8 Clock:** target 1.5 h, hard stop 3 h. B821 took 68 minutes on the same battery.
- **D9 Commit hygiene:** the standard ASCII and no-id rules.
- **Round count, if a branch exists:** round 1 of 2 on that PR, class walk-cap. This follows the coordinator's 2026-10-27 ruling, relayed from the B821 kit line 18.

## Q-questions for Tuesday (each with a default)
- **Q-1: launch the measurement seat, or go straight to a records seat?**
  - **Default: launch.** It is cheap (Sonnet, no push expected). It gives the first independent re-make of g02, g03 and g05. It turns the -325 line-0 fact into a run at current main rather than a reading.
  - Alternative: commission records now on comment 40222 plus this report's sha-equality evidence. In that case, mark this kit unused.
- **Q-2: if all seven are killed, the lane ends with `READY: NO BRANCH` and a `FOR THE RECORDS SEAT` section. No gate, no Jira write.**
  - **Default: yes.** The records seat then judges MPSCALC-355 under C-79 (merged to main and every clause MET), and re-judges MPSCALC-325 clause 2 on the (iv) table.
- **Q-3: gate tier if a survivor appears: G2, tier 2 (:109), Sonnet, round 1 of 2 on that PR?**
  - **Default: yes.** Override to G1 (:108, Opus) only if you read the walk caps as a security surface for a test-only row.
- **Q-4: B1043's kit line 25 says "any seat writes under `2_Project_Files`: STOP".** This seat's `worktree add` writes `.git/worktrees/` metadata in the shared repo, and so does its optional fetch.
  - **Default: launch anyway.** B1043's own kit names this seat's kind from its side ("an MPS test-only builder for MPSCALC-355 ... no path shared with Yours"), and D5 avoids the fetch.
  - If B1043 stops on it, answer "expected: B1046, Api test lane, no shared path".

## UNMEASURED
- **No build, test, mutant or compile was run.** The killer rows being red at `5c64a442` is inferred from sha-equal product bytes plus an insertion-only test-file change. Test helpers in other Api test files since `32b09108` were not compared.
- **The exact counts** of the 100,000-line row under g04 and g03 at this main. Gate B678's figures ("Expected: 20 Actual: 100000" and "... Actual: 10") are RELAYED from the #112 head.
- **The Api name count** at main: 3,165, RELAYED.
- **Whether B1043 treats this seat's worktree metadata** as a moved fact (Q-4).
- **Hosted state:** fenced.

## Outside the fences (disclosure)
- **Fences 3 and 4:** none crossed. Reads only: `gh api -X GET` under the project `GH_CONFIG_DIR`, Jira GET through an in-process reader I wrote at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/b1046/issue.py` (reads the project `.env`, prints no token), and local `git log --no-optional-locks` on the root records repo.
- **Scratch only:** raw copies of three source files, the Jira text, a heads list and the sweep output, all under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/b1046/`.
- **Not read:** the decision store, `briefs_staged`, the scoreboard and `_ledger.md`.
- **Cross-project read:** one `tail -1` of B1043's live STATUS in the project `Briefs/`.
- **Files written:** only the two named in my task.
- **Hook advisories:** three case-sensitive greps drew a hook advisory. Each count that mattered was re-checked case-insensitively or with a control.
- **Card and person ids:** this report names no decision-card id. The kit names no person.
