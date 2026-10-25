STARTABLE: YES

# B726 DRAFTER REPORT (SEAT-H34, HPSM-POC, PR #221 round 2, HPSMPOC-353)
Drafted Mon 26 Oct 2026 about 10:0x-10:2x AEDT (clock from `date`: 10:09 and 10:11) by the Sonnet kit drafter. Kit: `2026-10-26_B726_SEAT-H34_hpsmpoc-221-round2-identity.md` (131 lines; 8 lines match the four-underscore pattern, the 7 slots and the last line; `@X@` count 0; non-ASCII bytes 0).

## BLUF
1. Startable now: branch and `refs/pull/221/head` are both `26b78914...`, main is `b069274c`, PR #221 is open, ports 9710-9719 are free, no pane or kit holds `H34` or `B726`.
2. The gate's fix-shape was verified as a PROPOSAL and works: with `step_identity` returning the triple (name, `uses:` path, one-line `run:` or "(block)") and `PINNED_STEPS` as 12 triples, F1a F1b F1c F1c2 F2a F2b F2c x16 are all RED, F4a F4b stay RED, and 9 legitimate layouts stay GREEN (34 ran, both interpreters on the layouts I ran under 3.9).
3. **The gate's fix-shape is not enough on its own: the drafter found a hole it did not list.** A YAML plain scalar that continues on the next line (a `run:` / `uses:` / `name:` value with a deeper-indented line under it) is read by `step_keys` as "lines under the key" and ignored by the identity. Plants G1 (`&& echo X=1 >> "$GITHUB_ENV"` under the pinned build line), G2 (`x # v7.0.1` under the checkout `uses:`), G3 (`and more` under the Azurite `name:`) are GREEN at the head and would stay green with the triple alone. The kit makes the seat refuse a name / uses / one-line run that has lines under it (the candidate turns all three RED). This is inside the lane's property (a pinned step must not run something else), so I put it in scope rather than leaving a round-2 NO GO waiting.
4. The kit says plainly in its first section that the error was Tuesday's (the round-1 commission prescribed the name-first rule), and carries the binding ADVERSARIAL CLAUSE with 14 starting routes and a "caught = a plant you ran, named = the docstring words quoted" rule.
5. Round 2 of 2: a NO GO hits the G-cap. The `api` checks are red for the SDK/Pkcs cause and will stay red on this PR until the B725 lane is on main; the kit says it is not the seat's and main is not merged in.

## Facts re-measured (instrument, control)
| Fact | Instrument | Control |
|---|---|---|
| branch `b708/...` and `refs/pull/221/head` = `26b78914308730b5c72fffc30bd7c52fc38ed03f`; main = `b069274cfc201bc451ab2c22dc6adc2a6e231bef` | `git --no-optional-locks ls-remote origin` | same call also printed `refs/heads/main`; the gate's own 5 reads agree |
| open PRs: #221 and #222 (`b709/hpsmpoc-timing-rows-354`, head `7b3f3c76...`); #221 files = the one reader path; #222 files = `RequestTimingLogTests.cs`; `compare b069274c...26b78914` ahead 1 behind 0, 1 file | `gh api -X GET` under the project `GH_CONFIG_DIR` | the files lists differ, so the two calls return real rows |
| reader at the head = `a3d4e27c...` (767 lines), `ci.yml` at main = `0176b491...` (679) | `git show` to scratch, `git hash-object` | both equal the gate's published figures |
| clone holds both commits | `git cat-file -t` prints `commit` twice | n/a |
| the defect: F1a F1b F1c2 F2a F2b F2c x16 GREEN at the head, F4a F4b RED, F1c RED via the old results pin | drafter harness: ci.yml plants built by literal edits whose anchor occurs once in the SHARD JOB region (the checkout line occurs 8 times in the file; an unscoped anchor asserts), run as `python3 -I -X dev <layout>/infra/tests/test_ci_workflow.py -v` on the head reader copy | c0 (unmutated) 34 ran 0 red; F4a F4b are red on the same reader, so the reader can fail |
| candidate: all 8 forgeries RED (test S, plus the old results pin for F1c / F1c2), F4a F4b RED, c0 34 OK; 9 legitimate layouts GREEN (SHA bump, tag bump, two-space bump, name comment, run comment, whole-line comment, all-jobs checkout bump, blank line, `with:` added) | same harness, candidate reader built from the head reader by string edits (identity function, 12 triples, env-test label, built-in rows, results-pin assertion added beside the old) | the same layouts on the head reader are green for the forgeries, so the candidate is what turns them red |
| continuation hole: G1 G2 G3 green at head, red with the "runs onto the next line" refusal | same harness | head reader green on all three |
| by-design greens: G4 other ref, G6 `with:` value, G7 step `working-directory`, G8 `if: false`, G10 `shell: sh`, G11 `id:`; caught: G5 other path, G9 quoted run, G12 `uses:` added to a named step, G14 folded run | same harness | n/a |
| 3.9.6: c0 OK, L1 bump OK, F2a FAILED (1), G1 FAILED (2) | `/usr/bin/python3 -I -X dev` on four layouts | the two FAILED rows are the control |
| ports 9710-9719 free | `lsof -nP -iTCP:9710-9719 -sTCP:LISTEN` rc 1 | socket bound on 9711 for 6 s: 2 listener rows, then 0 |
| kit scan (115 non-`.pre-` SEAT kits of 10-25 and 10-26) hits seven files, all 10-25 and finished (B620 B621 B622 B675 B692 B693 B704); no kit names H34 or B726 | word-boundary scan `(^|[^0-9a-f])971[0-9]([^0-9a-f]|$)` per file | `x 9711 y` reads 1, `x 19711 y` reads 0 |
| panes: tuesday, Datasec/Security-Composer-J20, HPSM-POC-H32, HPSM-POC-G137, NexusAI-M14, HPSM-POC-H31, MPS-M29, MPS-G135, NexusAI-G134, fleet-monitor; no H33, no H34 | `tmux list-panes -a -F '#{@cockpit_name}'` | n/a |
| `.tools/b726` and `.tools/wt-b726-*` absent | `ls -d` errors | `ls -d .tools/b198` lists |
| load | `uptime` 10:11: 10.64 15.63 12.71 | n/a (heavy runs will wait) |
| models and rows | `models_latest.json` line 23 `claude-sonnet-5-5`; `model-routing.md` C2 line 92, G2 line 109, G-cap line 111 | `grep -n` on the same file returns all three rows |
| round count | read from the first line of the B716 STATUS: "NO GO, round 1 of 2 on the class closing the open lists of the shard-job reader" | n/a |

## D-decisions (taken in the kit)
- **D-1 (class, not instance):** the identity change applies to every step of the pinned list, not only checkout / setup / upload; the kit forbids a narrower fix.
- **D-2 (continuation refusal in scope):** the drafter's G1-G3 finding is added to the round-2 work, as the same property (a pinned step runs something else). Reason: a round-2 NO GO is the cap; the hole would be the obvious next find.
- **D-3 (results-file pin):** the gate said the pin should read the `uses:` key. The kit ADDS a key-reading assertion beside the old `assertIn` and keeps the old one, so no assertion of the main-base reader is edited (the gate's AST no-loosening program stays clean).
- **D-4 (B716-8):** the unpinned values are NAMED in the docstring, not pinned (Tuesday's choice in the commission); the adversarial table makes the seat name more than the gate listed (the ref after `@`, step-level `working-directory`, `id`, `timeout-minutes`, `shell: sh` for `bash`).
- **D-5 (no new test):** names must be lost 0 / added 0 against the head and lost 0 / added 3 against main (34).
- **D-6 (commit shape):** one commit on top of `26b78914`, plain fast-forward push to the existing branch; a rejected push is a STOP (no force, no rebase, no merge of main).
- **D-7 (whole infra WITH the Bicep binary):** the kit asks for `Ran 262` OK, ResourceWarnings 0, files open 0 (the gate's head figure), using `.tools/bicep/bicep` by path (0.47.16 = the CI pin). The binary path is a named exception to the `.tools/b*` read-forbidden rule only because it is a binary the gate also ran.
- **D-8 (timings):** drafter's suggestion target READY 90 min after launch, hard stop 2.5 h (one helper, a few rows, about 40 plants plus the 56 and 122 gate tables under two interpreters, one whole-infra run). Tuesday sets the real times.

## Q-questions for Tuesday (each with a default)
- **Q-1: the `api` checks stay red on #221 until the Pkcs-pin lane (B725 / H33) is on main. After B725 lands, #221's branch will not contain the fix; a re-run of its old run probably reuses the old merge commit (the gate's UNMEASURED).** Who brings the fix into #221's checks (GitHub "update branch" is a merge commit onto the branch; the kit forbids the seat to do it)? **Default: you decide after the round-2 gate; the seat does nothing, and the gate reads the three red `api` checks as B716-1 (environmental, not this PR's) and grades the rest.**
- **Q-2: is the continuation refusal (D-2) accepted as in scope?** Default: yes; if you want it out, delete the "Refuse a coordinate that runs onto the next line" paragraph and G1-G3 from item 2 and ticket it.
- **Q-3: round 2 gate tier and model.** Default: tier 2 on Sonnet (G2), as the kit says; if the gate finds the continuation hole or a similar route unmeasured by the builder, the cap applies.
- **Q-4: HPSMPOC-353 after landing.** The kit says the F3 unread-body family stays out and the ticket stays open for it (the gate's FOR TUESDAY item 2). Default: records seat words it; not the builder.
- **Q-5: H33 (B725) is not started and its kit file is not present in `briefs/`.** The kit names it "if it has been started" and gives its block 9700-9709 from your commission. Default: correct the PARTITION line at stamp if H33's pane or ports differ.

## UNMEASURED
No project-tree worktree, commit or test was built (fences). Not run by the drafter: the gate's full 56-row and 122-row tables against the candidate (9 legitimate layouts only), whole infra, the three companion test files, the AST no-loosening program, the 20 repeats, the candidate on `ci.yml` plants beyond the 33 layouts; GitHub's treatment of a continued plain scalar (YAML says one scalar; nothing hosted run); the runner's Python; whether B725 has started. The candidate is a PROPOSAL: the seat must re-derive it. The drafter's scratch code is in the session scratchpad only (not a project file) and is not shipped with the kit; the kit describes the shape instead.

## Outside the fences (disclosure)
None. Reads: the B716 STATUS (lines 1-440 plus the evidence-folder listing), the B708 kit and drafter report (header), the head reader and `ci.yml` via `git show` (read verb) into the session scratchpad, `model-routing.md`, `models_latest.json`, `brief_seat.sh` header, tmux pane names, `lsof`, `gh api -X GET` (pulls, files, compare) under the project `GH_CONFIG_DIR`, and python runs of scratch copies in the session scratchpad. One bash call was refused by the `cd` hook (a `cd /tmp` I typed by mistake); it ran nothing and I re-issued it without `cd`. Wrote only the kit and this report (plus files in the session scratchpad). No fetch, pull, push, worktree, checkout, merge-tree or commit in HPSM-POC; no `decision_queue.sh`; no Jira call; no HTTP to a hosted host; no HP-NDA folder opened; no mail, chat, Artifact or Docs tool.
