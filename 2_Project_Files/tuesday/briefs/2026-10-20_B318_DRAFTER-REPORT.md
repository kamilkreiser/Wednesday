# B318 drafter report (Tuesday's read-only drafter, 2026-10-20 ~12:55 AEDT)

Brief written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B318_SEAT-G14_mps-gate-pr85-tier1.md` (tier 1, round 1 of 2, Opus: launch WITHOUT `BRIEF_SEAT_LEVEL`; pane `Datasec/MPS-G14`, ports 7450-7459, findings B318-n, report `<project>/1_Project_Definition/Briefs/2026-10-20_B318_STATUS.md`). Size ~51 KB, over the ~45 KB target (see open question 6).

## What I read
- RELAYED, whole: the B305 gate brief and drafter report (template); `B309_STATUS.md` (240 lines); the B309 builder brief (177 lines); ANSWER-1.
- MEASURED code at the head `b451239…` with `git --no-optional-locks` read verbs only (via a scratchpad bash script, because zsh rejects `${H}:path`): `Proposal.cs` and `QuoteEvents.cs` diffs; `QuoteEndpoints.cs` lines 140-200 (UpdateDraft), 803-845 (VersionDiff), 1085-1137 (SubmittedBlocked, CallerCan); `PriceAudit.cs` 112-135 (SameDraft); `Mapping.cs` 250-300 (Restrict, DraftChanges, FigureChanges); `Dtos.cs` 445-462; the diff of the six edited existing test files; `git grep` of `QuoteSummaryDto|ToSummary`; `brief_seat.sh` whole.
- Not opened: `.local/`, `Source_Documents/`, `4_Credentials`, `3_Access_Keys`, any `.tools/` file, the real book, Jira, CLARIFICATIONS.md.

## Measurements (12:53-12:55 AEDT, read verbs only)
- `ls-remote`: main `acfcf5dec5d4…` (equals the PR base); `refs/heads/b309/v0-quote-contract` and `refs/pull/85/head` both `b451239b6fde…`; `b318*` = 0; `cat-file -t` head = commit.
- `gh api pulls/85` (project `.gh-config`): open, draft false, commits 9, files 28, +1898/-56, mergeable true, mergeable_state blocked (required checks pending).
- Open PRs: #85 and #86 (B313, head `925caf8b…`, 18 files, all `web/src/screens/**`): no path shared with #85's 28.
- `git diff --stat`: 28 files as the builder says; `Proposal.cs` +3/-0 (one comment, four NotShown entries); `QuoteEvents.cs` `Accepted` appended to `Kinds`.
- Check-runs on the head: `CodeQL` neutral; `Analyze (actions)`, `(javascript-typescript)`, `(python)` success; `dotnet (build Release…; test)`, `web`, `python`, `Analyze (csharp)` in_progress. Code-scanning: 3 analyses at `b451239` with 0 results, csharp not yet present; open alerts on the PR ref 0 (not "clean" until csharp reports).
- `lsof 7450-7459`: 0 lines (control: 15 listeners unfiltered). `brief_seat.sh:24`: `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`, id read from `models_latest.json`: confirmed, so Opus without the variable.
- `ls .tools | grep heavy-slot`: `heavy-slot-1` exists (another seat's; I did not read its holder). The brief tells the gate to expect contention. Load1 `4.60 4.50 7.71` at 12:53.
- Single producer/consumer of the list row: `ToSummary` (`QuoteFigures.cs:41`) and `ListQuotes` (`QuoteEndpoints.cs:666-676`).

## My own traps (written into the brief as things to break, not findings)
1. **Restricted echo vs `SameDraft`.** `next` is built after `PricingPolicy.Apply` and the target-GP overwrite; a restricted Seller echoing a redacted purchase draft may be judged "no-op" (correct) or may churn; the gate probes it.
2. **Diff leak surface.** Redaction rests on `RedactDraft` plus `Restrict` over reflection-built paths and every decimal of `portfolio.*` / `purchase.*`; the builder's token check uses the repo's own `InternalFieldNames` list, so a name outside it is untested; no purchase-pair test (builder admits it). Side mix (draft side with a "latest calculation" vs a snapshot side) is the other hole.
3. **`SubmittedBlocked` is stricter than the sentence.** It also refuses when `Status != "Succeeded"` with zero Blocking issues, giving "has 0 blocking issue(s)". Submit's condition is `!Priced || HasBlockingIssues`; the gate compares.
4. **`callerCan.Approve` now reads the snapshot store once per row** (Home list); a size Note at most.
5. **Race on the no-op check:** builder did not test it (stated); the lock covers it by reading, the gate runs 50 rounds.
6. **MPSCALC-236:** two of five Done-when clauses are not met by ruling (no `issued`, nothing records `accepted`). The brief makes the gate say so line by line and caps the token at GO WITH FINDINGS when that is the only gap.
7. **`GateB36.cs:182` stays green with a NotShown line removed** (builder's own note): the gate sizes whether the field class is guarded by one test only.
8. **Generated client pointer:** the interim `SOURCE.txt` named `382d713`; the gate checks that the final one names the head's contract.
9. **`EntraAuthTests.cs` is outside the brief's "Yours" text** (inside "existing tests may gain rows"); the gate states whether a count-pin edit is a row.

## Numbered open questions with recommended answers
1. **Model.** Opus, no `BRIEF_SEAT_LEVEL`. Now confirmed by reading `brief_seat.sh:24`. Recommended: launch as written.
2. **Heavy slot.** `heavy-slot-1` is held by someone now. Recommended: launch when a slot is free and load1 is below 8; the gate waits per the rule anyway.
3. **CodeQL csharp and the dotnet job were still running at drafting.** Recommended: launch now; the brief makes the verdict conditional on them and forbids calling pending green.
4. **Gate Jira comments.** I allowed one per ticket (six; none on T-V0-8) if byte-equal read-back is possible, following the B309 builder's pattern, but the B305 template says "no Jira write". Recommended: keep (the task text permitted "one gate comment per ticket if the template allows it"); if Tuesday prefers the stricter B305 rule, delete the sentence in the "You may not" paragraph and the six comment lines in r11/VERDICT.
5. **Ticket-vs-brief divergence on -236.** Brief caps that ticket at GO WITH FINDINGS when the ruled gap is the only gap. Recommended: keep; the records seat carries it.
6. **Brief size ~51 KB vs ~45 KB target.** The B309 surface is wider than B305 (7 tickets, 28 files, 8 questions). Recommended: accept; if Tuesday wants it smaller, cut r7 and the T-k/T-j detail first (the gate probes those without hand-holding).
7. **Merge prediction.** main equals the PR base, so GitHub reports mergeable true; the gate still runs `merge-tree` in its own scratch clone at verdict. No action.
8. **Idle B309 trees and a running dotnet server.** Not measured; the brief forbids touching them. No action.

## UNMEASURED
Jira ticket states and the six comments (39737-39742), CLARIFICATIONS text, the decision-queue card (the brief repeats the builder's relay); the openapi.json-vs-code agreement and the generated client equality (the gate regenerates); whether any leak exists (I read the redaction code, ran no probe, built nothing); `Mapping.RedactDraft` and `PurchaseMapping.Restrict` bodies; whether `heavy-slot-1`'s run has ended; CI results beyond the 8 states listed; the 22-item NEW WORDS count (the gate recounts); whether `AGENTMAIL_API_KEY` is set.

Files written: the brief and this report only (plus two scratch scripts in the session scratchpad).
