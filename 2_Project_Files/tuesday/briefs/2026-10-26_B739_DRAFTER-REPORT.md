STARTABLE: YES (after Tuesday fills the 8 stamp slots; the start does not depend on #225 or CI; one risk and one ordering question are in Q-1 and Q-2)

# B739 DRAFTER REPORT (kit `2026-10-26_B739_SEAT-H36_hpsmpoc-223-followup-stored-values.md`, 138 lines)
Drafted Mon 26 Oct 2026 13:33 to about 13:50 AEDT (clock from `date`), read-only, by the Sonnet drafter. Kit shape cloned from B718 (136 lines, read whole); B729 STATUS read whole (finding B729-1 at lines 121 and 164; FOR TUESDAY from 192).

## BLUF
- The commission is buildable as two additions to #223 with NO new words and NO new code: (1) the `heldName` allowance on five fields over three paths (action-item PUT: title, ownerRole; disposition: amendedNarrative, auditNote; narrative review edit: text); (2) a screen of the AI narrative output that stores a hit as a failed narrative with the existing `schema-invalid` code and the web's existing sentence.
- **Two facts the commission did not expect, both measured, both shaped the kit:**
  1. **The screen cannot live in `NarrativeOutputValidator`.** `Modules.Reporting.csproj` has no `ProjectReference`; `Modules.Assessment.csproj:16` references Reporting, and `FollowUpShape` is in Assessment. Calling the predicate from the validator needs a reference cycle or an edit of `FollowUpModels.cs` (a hold). So the kit puts the screen in `ReportingEndpoints.GenerateNarrative` right after `pipeline.GenerateAsync`, with two recorded costs: no live-model retry for a hit, and the pipeline has already written the `narrative.generated` usage event (`NarrativePipeline.cs:147`) for a row stored as failed.
  2. **A stacked branch cannot be merged into main after #223's squash.** The follow-up edits lines #223 added (the "no allowance" comment, README clause, the five checks), so a plain merge will very probably conflict (UNMEASURED: `merge-tree` forbidden to me). The kit therefore says the gate reads `bcb359f8..head` (clean, small) and landing needs a separate re-land seat (cherry-pick of the two commits onto the post-squash main as a NEW ref, with a byte-equality check of the two diffs). The equality is justified by a measurement: tree(`bcb359f8`) = `7a142ebd...` = GitHub's merge tree for #223.
- Model: Sonnet, row C2 (`model-routing.md:92`), tier-1 Opus gate G1 (`:108`). Launch line carries `BRIEF_SEAT_LEVEL=sonnet` (`brief_seat.sh:24` defaults to Opus).
- Port block 9550-9559 (none needed; in-process hosts).

## Facts re-measured (instrument, clock, control)
| Fact | Instrument and clock | Result | Control |
|---|---|---|---|
| main, #223 head, b718 ref, no b739 ref | `git --no-optional-locks ls-remote origin` 13:33 | main `b069274c`, b718 `bcb359f8`, no `b739*` | same call lists `b723`, `b725`, `b73` refs |
| Both shas present in shared clone | `cat-file -t` 13:33 | commit, commit | n/a (type word) |
| Open PRs | `gh api -X GET pulls?state=open` 13:33 | 225, 224, 223, 222, 221 (heads `056073be`, `0413f25c`, `bcb359f8`, `7b3f3c76`, `22d5c13c`); #223 `mergeable_state` blocked | `state=closed&per_page=3` = 3 |
| Path intersection with the follow-up's paths | `pulls/<n>/files` + `grep -c -x -F -f` 13:35 | #221 0, #222 0, #224 0, #225 0 (its one path is the Assessment csproj, not mine) | #223 against the same list = 4 (by design) |
| Tree equality | `rev-parse ^{tree}` + `commits/8cba3fba` 13:36 | `7a142ebd...` = `7a142ebd...`; main `f6932c69...` | main's tree unequal |
| #223 commits | `log b069274c..bcb359f8`, `rev-list --left-right --count` | 2 commits, `0 2` | n/a |
| Stacked-PR precedent | `pulls?state=all&per_page=100` pages 1-4, 13:36 | 225 PRs, 223 base `main`, 2 base `b03/ci` (never merged) = no landed stacked precedent | 223 rows with base main counted |
| Landing convention | `CLARIFICATIONS.md` (192 lines, local, last written 29 Sep) `grep -i squash` | 1 hit, line 138 ("squash-merged head-pinned"); B729 STATUS line 195 has the exact squash command | `NOSUCH-zz7f3a` 0 |
| HasControl census at head | `git grep -c -F HasControl bcb359f8 -- api/src` summed | 23 lines; 8 #223 call sites at ActionPlan 383/386, Reporting 269/272, Requests 245/248/260/263; `Requests.cs:146` is the `heldName` line | `NOSUCH-zz7f3a` 0 |
| "no allowance" wording to be corrected | `git grep -n -i -F 'no allowance'` | exactly 2: `ActionPlanEndpoints.cs:382` and README line 86 | n/a |
| Evidence has no update route | `git grep -E 'Map(Put|Post|Patch)\(.*evidence'` | one line, `AssessmentModule.cs:216` `MapPost` | narratives route greps 2 |
| Reporting cannot reference Assessment | `git show` both csproj, `grep ProjectReference` | Reporting: none; Assessment line 16 references Reporting | n/a (read) |
| UpdateItem order | `ActionPlanEndpoints.cs:231-255` read | validate (238) before `LiveItem` (240) and 404 (241) | B729 runtime check relayed |
| PutDisposition order | `FindingEndpoints.cs:48-114` read | shape 57-58 before `CurrentAsync` (80) and same-again branch (83-88, compares TRIMMED values) | n/a |
| Review: only `generated` drafts are reviewable | `NarrativeReview.cs:26-45` read | `not-reviewable` for any other status: so the held `text` is always model output | n/a |
| Existing failure code and web sentence | `grep schema-invalid` over api/src and web/src | `NarrativeErrorCodes.SchemaInvalid` (validator :65, :67); `web/src/content/narrative-failure.ts:23` | `content-filter` (:24) is the AI service's safety filter: false for this case |
| CI shard for the new class | head `ci.yml` read | `api-assessment` filter line 252; predicate line 303 | `NOSUCH-zz7f3a` 0 |
| Round count | python -I over 405 STATUS first lines, 13:37 | 77 verdicts, 18 `NO GO`, 0 on this class | the one B478-1 verdict line (GO WITH FINDINGS) found |
| Panes | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` 13:35 | `tuesday`, G147, MPS-M31, MPS-G143, G144, MPS-G138, fleet-monitor; no H36 | n/a |
| Port block 9550-9559 | `/usr/sbin/lsof -nP -iTCP:9550-9559 -sTCP:LISTEN` 13:35; word-boundary python scan of 129 non-`.pre-` SEAT kits of 25 and 26 Oct | lsof rc 1; scan: no hit | a `python3 -I` listener on 9551 was listed (rc 0), then rc 1 after it ended; scan with `956x` hits B738 only |
| Other seats' blocks (relayed from their kits) | kit greps | G147 (B738) 9560-9569; G144 (B733) 9930-9939; B736 9740-9749 and B737 9520-9529 (stamped, not live at 13:35) | n/a |
| `.tools/b739`, `wt-b739-base` absent; helper origins exist | `ls -d`, `ls -l` 13:39 | absent rc 1; five origins present with sizes | `ls -d .tools/b514` lists |
| Models | `models_latest.json` line 23; `brief_seat.sh` line 24 read | `claude-sonnet-5-5`; `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"` | n/a |

## D-decisions (the kit's; each is binding on the builder, Tuesday may change at the stamp)
- **D-1 Branch (the commission asked for this one, measured):** stacked `b739/hpsmpoc-343-held-values-and-narrative-screen` from `bcb359f8`, two commits (rows red, then product), pushed as a plain create. Builder decides by reads among State A (expected), B (#223 landed meanwhile and its five blobs equal `bcb359f8`'s: base on main), C (head moved: STOP). Landing is NOT a merge of the stacked branch; a later re-land seat cherry-picks onto the post-squash main and proves the two diffs byte-equal. Rejected: (a) wait for #223 to land and branch from main (simplest landing, but blocked behind #225 and a paused CI of unknown length); (b) a PR whose base is the b718 branch (merging it would move #223's gated head; no landed stacked precedent in 225 PRs); (c) merge the stacked branch (expected conflict, see BLUF).
- **D-2 "Unchanged" = ordinal equality of the value AS SENT to the stored value of the SAME field of the SAME row**; skip only that field's `*-invalid` check; never trimmed, case-folded or partial; per field, not per request; never on create.
- **D-3 Call shapes** copy `heldName`; the item is looked up before validation but the 400-before-404 order for a missing item is kept (B729 measured it); disposition current row obtained just before the shape with every other answer order kept.
- **D-4 Not allowed:** review `note`, evidence (no update route), plan title/phase, evidence source, any create.
- **D-5 Screen placement in Assessment** with its two costs written into FOR TUESDAY (no retry; extra `narrative.generated` usage event). No second usage event.
- **D-6 Hit = the validator's own failure:** `Failed`, `schema-invalid`, `Text` null, `AutoCitations` cleared; existing failed-row code does the rest; no new words, no web edit.
- **D-7 Model:** Sonnet C2 (line 92), not C3 (line 93): the decisions are made in the kit, mechanism already ruled and shipped (B482). Gate tier 1 Opus G1 (line 108).
- **D-8 Ports:** none needed; 9550-9559 only if the builder binds.

## Q-questions for Tuesday (each with a default)
- **Q-1 Opus instead of Sonnet?** The allowance weakens a security refusal; C3 reads "the decision on a security surface". Default: Sonnet (D-7), because #223 (same surface, Sonnet-built) drew no Blocker or Major on the branch and the only Major was this missing allowance, whose design is now pinned. If you read the allowance as design, change the launch line to `BRIEF_SEAT_LEVEL=opus` and the model line; nothing else in the kit moves.
- **Q-2 Screen placement:** default D-5 (Assessment endpoint, one file, no Reporting edit) with the two recorded costs. The alternative (a screen injected into `NarrativePipeline` by an optional constructor parameter plus a DI line) keeps retry and usage events consistent but edits `Modules.Reporting` and the registration; say if you want it, and the kit's paths, never-edited list and mutants S1-S8 change.
- **Q-3 Words for the failure:** default is the web's existing `schema-invalid` sentence ("... a form the checks could not read, so it was held back."). If the product owner wants words specific to "the model reply held a hidden character", that is a word pack to him first; the kit has the builder flag it, not write it.
- **Q-4 Re-land commission:** default is that you commission a small re-land seat after #223 lands (see D-1). If you prefer to hold the launch of B739 until #223 has landed (State B, no re-land), say so at the stamp; the kit already handles State B.
- **Q-5 Round count:** the kit says "round 1 of 2, NO GO 0 of 2" from a frame of 405 files / 77 verdicts measured at 13:37; confirm before the gate.
- **Q-6 Timing:** the kit suggests target READY 3 h and hard stop 5 h after launch (about 24 mutant builds); #225's gate (G144) is running dotnet, so `dn.sh` will wait.

## UNMEASURED
- That a merge of the stacked branch into squashed main conflicts, and that the two commits cherry-pick cleanly onto it (`merge-tree --write-tree` is forbidden to me; the follow-up does not exist).
- That hoisting `CurrentAsync` above the disposition shape changes no answer order (the kit makes the builder prove it).
- Whether any of #223's 35 rows would be changed by the allowance: read whole, none sends a value equal to a stored one, but they were not run against it.
- The metric effect of the extra `narrative.generated` usage event under D-5 (magnitude, and what reads it): not measured.
- A live model's output; browser round trip effects on stored line endings; stored data on the UAT or demo; the CI pause itself (relayed by the commission, not read from GitHub); the first-round gate outcome.
- Jira: not read (the kit has the builder read HPSMPOC-343, -177, -178 whole in PRIOR WORK); no ticket of its own for the follow-up is known to me.

## Outside-the-fences disclosure
- Files written: only the kit and this report, with the Write tool. I also wrote ONE scratch file in the session scratchpad (`.../scratchpad/prs.tsv`, 225 lines of PR number, base, head, merge date) to count PR bases; it holds no secret and is outside the repository.
- I started ONE short-lived `python3 -I` listener on 127.0.0.1:9551 (about 6 s, ended by itself) as the positive control for the port scan, and a second `python3 -I` ran the kit scans. No other process was started.
- Git in `2_Project_Files`: only `ls-remote`, `cat-file`, `rev-parse`, `rev-list`, `log`, `show`, `grep`, all `--no-optional-locks`. No fetch, worktree, merge-tree, checkout.
- `gh api -X GET` only, under the project's `GH_CONFIG_DIR`; no HTTP to any hosted host. No Jira call. No Artifact, Docs, mail, chat, decision-queue, scoreboard or ledger tool or file. No `.tools/b*` folder opened (I ran `ls -d` and `ls -l` on named paths, and `sed -n 1,12p` on `b514/dn.sh` to confirm its usage header and `B=` line). Did not open `4_Credentials`, `3_Access_Keys`, `HP Reporting and Docs`, any SOW, `Source_Documents`, `inbound`.
- Read in the other seats' kits (`briefs/` is a Tuesday folder, not forbidden): port lines only of B733, B736, B737, B738.
- Two tool calls were refused or advised by hooks (an unquoted `======` separator; a case-sensitive grep advisory): both re-run correctly; no state was changed by them.
- No person's name, decision-card id or card slug is in the kit (checked by grep: 0 names; the only slug-shaped hit is the branch name `b725/hpsmpoc-pkcs-pin-10014`). Stamp-slot count measured by `/usr/bin/grep -c -E '_''_''_''_'`: 9 lines (8 slots plus the last line); control: a scratch line with four underscores reads 1. At-sign pattern count 0. Non-ASCII lines 0.
