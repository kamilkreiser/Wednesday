PR 2099: GO WITH NOTES

# Gate 267, tier 2 compare (doc-only delta), round 1 of 2: PR 2099 (KS-2060), Secuura / Blockchain

| PR | head | develop | verdict |
|---|---|---|---|
| 2099 | 8967de8b17558890dc4ace2732cb8350768df601 | 2935f723109756a60cadc5521977c7a036ec322d | GO WITH NOTES |

Head and develop by `git ls-remote`: start 2026-11-08T17:05:37Z, end 2026-11-08T17:11:44Z (17:05:45Z in my clone's fetch): both unchanged, both equal the commission's pins. `refs/pull/2099/head` = the branch. This verdict holds for SHA 8967de8b only.

## BLUF

The delta is what the seat says: one commit, a fast-forward from 0d747d09, 5 files, +16/-11, nothing under `services/`. Gate 266's F1, F3 and the F2 words are closed in the five files. Two sentences a client reads first (the BLUF of the held PR body and the held ticket comment) still say the flat thing F1 was about. Fix those two lines before posting; that is the only thing I would ask for. No product code, test, migration or yaml byte moved, so the stop line did not fire.

Findings need no Kam ruling. W1 changes a sentence in the PR body and the ticket comment, not in his DPIA.

## Q1. Is the delta exactly what the seat says

- `git diff --stat 0d747d09ab23 8967de8b1755`: 5 files, 16 insertions, 11 deletions. `git log 0d747d09ab23..8967de8b1755`: one commit (`8967de8b`). `merge-base --is-ancestor` rc 0 (fast-forward).
- Names: `Blockchain/Dev/docs/compliance/dpia-art17-...md` and four files under `Projects Documents/fragments/{cheat,flow}` (KS-2058 and KS-2060, one of each per kind). Nothing else.
- Control: `diff --quiet ... -- Blockchain/Dev/services` rc 0; the same on `-- Blockchain/Dev/docs` rc 1. Positive control for the grep I used later: the same pattern over `c0e6e744b7b2..8967de8b1755` counted 5.
- Scope note: four of the five files are under `Projects Documents/fragments/`, not `docs/`. They are docs-class (HTML fragments the docs build renders), so the stop line did not apply. Say it so no one reads "docs-only" as the `docs/` folder.
- The branch against its merge-base `c0e6e744b7b2`: 4 commits (6110311f, e3502d7d, 0d747d09, 8967de8b), 25 files, DPIA +16/-3. The body's "Four commits", "25 files" and "+16/-3" are true.

## Q2. Each gate 266 finding the addendum names

- **F1 (legacy participant row): closed in the words, except the two BLUF lines (W1).**
  - DPIA 4.2 governance row: "so a legacy participant row whose id is not the subject's id is left as it is: it keeps the wallet, its stake and its votes until the backfill".
  - DPIA Net effect: "...in governance (participant row, votes, proposals, delegations; KS-2060), except where a legacy participant row (one whose id is not the user's id) holds it. Whether any deployment holds such rows has not been measured."
  - DPIA Not yet covered: "...and so does a legacy participant row whose id is not the user's id."
  - Flow P10: "naming the old wallet finds no owner (404) unless a legacy row holds it (see the limits)".
  - Flow limits: "an admin naming that wallet still lands stake on it. Whether any box holds such rows is not measured."
  - KS-2058 cheat and flow: "except on a legacy row whose id is not the user's id".
  - Held body P10 and Stated limits, and held comment P10 and Limits, say the same.
  - The addendum asked for "Net effect + 4.1/4.2 where relevant". 4.1 (line 87) is the users-row line and says nothing about governance, so leaving it is right.
  - Not touched: the first sentence of each held draft (W1).
- **F2 (the stale-write limit): closed in part (words yes; the list of paths is one short, W2).**
  - Flow limits: "A stale write can undo the erasure. A write that read a row before the erasure and saves after it puts the address back, and nothing re-runs the handler. An admin wallet registration in that window restores the wallet, stake and DRep flag on the cleared row. Any proposal save rewrites the whole votes array with the address it read: a vote, a cancel, a finalize, an execute, or the 60-second expiry job. Measured by our QA gate 266 under a forced order on real PostgreSQL, not under real concurrency; no fix in this ticket."
  - "Read, not measured" is gone from the flow and cheat fragments. The held body adds that `proposer_address` stays blank because the upsert does not set it, which matches gate 266 (not in the SET list).
  - The verdict path is not cited in any file. The text cites "our QA gate 266". The addendum said "citing the verdict path". For a client-read text that is the better choice; stating it so the difference is seen.
- **F3 (dead letter): closed.** Flow, 059 row: "A dead-lettered event is lost, not delayed: nothing replays it, so that subject stays uncleared until the backfill." Cheat: "an erasure event dead-lettered before it arrives is lost, not delayed." Held body and comment repeat it. Evidence below (W4).
- **F5 and F6: closed in the held drafts only.** Held body: "059 has no down migration, and once one erasure has written a NULL, `SET NOT NULL` cannot be restored (our QA gate 266 measured it)"; "Two parts go wider than Kam's cards, both on the coordinator's rulings and disclosed here: 059's three statements, and the wallet link refusal, which also stops an admin-disabled user who was never erased (status `inactive` or `deactivated`) from linking until reinstated." Held comment: the same two. Matches gate 266 F5 and F6(b). Neither is in the five files, which is as the addendum asked ("one line each in the body").
- **F4:** left to a ticket by the addendum. Not in any text. Correct.
- **Ticket comment edited in place:** the draft is written as a whole replacement of comment ce1689d0. I cannot read Linear (network is git only), so whether it is edited in place and not stacked is for the poster. NOT tested.

## Findings

**W1 (Medium, an overstatement in the first sentence a client reads).** Both held drafts open with a guarantee their own limits contradict.
- Where: `pr2099_body_round_words_final.md` BLUF: "After an erasure, the user's wallet is gone from the users row and from governance. The participant row keeps no wallet, stake, power, flags or did." `ks2060_comment_round_words_final.md` BLUF: "After an erasure, the user's wallet is gone from the users row and from governance."
- Why: the same drafts say a legacy participant row keeps the wallet, stake and votes, and a stale write puts the address back. Gate 266's F1 was exactly this sentence shape ("no wallet address stays in governance"); the DPIA Net effect got its exception and these two BLUFs did not. The DPIA row and the flow fragment qualify at the point of claim; the cheat "What to know" (unqualified, "The user's address is gone from their delegations...") is saved only by the Limits note one row below it, which I accept.
- FOUND by reading both drafts against gate 266 F1 and handler comment `userErasedSubscriber.ts:5-6` ("By id only ... a legacy row whose id is no user is left to the backfill"). TESTED: not a runtime matter; the code (`CLEAR_PARTICIPANT_SQL ... WHERE id = $1`) is the evidence. HOW: sed on the drafts and the handler at the head.
- Fix shape: add "for a participant row whose id is the user's id, with the limits below" to both BLUFs (or "unless a legacy participant row holds it").

**W2 (Low, an incomplete list of the stale-write paths).** A third write path restores the wallet and the words do not name it.
- `selfRegisterParticipant` (`services/governance/src/services/governanceService.ts:698`) reads the linked wallet from the users table, then `dbRefreshSelfRegistration` (`:256-262`) runs an unconditional `UPDATE svc_governance_participants SET wallet_address = $2, did = COALESCE($3, did) ... WHERE id = $1`. A self-registration whose linked-wallet read landed before the erasure, and whose update lands after it, puts wallet and did back on the cleared row (stake and flags are not written there).
- After the erasure the same route reads no linked wallet (403 "Link a wallet to your account first"), so only the in-flight window matters. The general sentence "A write that read a row before the erasure and saves after it puts the address back" covers it; the enumeration "An admin wallet registration in that window" reads as the only row write. It understates.
- FOUND by reading (`git grep`-equivalent over the head's `governanceService.ts`: the callers of `dbSaveParticipant` are only `registerParticipant` at 656 and 668, and `dbRefreshSelfRegistration` is called at 734, so I read the list by hand). TESTED: NOT run. Evidence class: READ ONLY. Not measured, not part of gate 266's forced interleave.
- Fix shape: "an admin wallet registration, or a self-registration, in that window".

**W3 (Low, wording).** The comment draft says the DPIA's "4.1, 4.2 and Net effect ... name the legacy-row case and the stale-write limit". 4.1 names neither, 4.2 names the legacy row only, and the stale-write limit sits in the "Not yet covered" paragraph after Net effect. The DPIA Net effect sentence itself carries the legacy exception but not the stale-write one; its next paragraph does. FOUND by reading `dpia-art17-...md:98-120`. Fix shape: "the DPIA's 4.2 and its Not yet covered paragraph".

**W4 (Info, understatement).** "Lost" and "nothing replays it" are true of a replay into this handler and I confirm it: the shared bus writes the dead letter to a stream and acks (`packages/shared/src/events/index.ts:198-211`, "for later inspection"), and the only files in the tree that mention dead-letter besides that writer are the subscribers and tests; I found no reader. But the event is kept in that stream, so an operator could replay it by hand. So "lost" is the code's behaviour, not the data's. TESTED: positive control: `grep -c xreadgroup` found the bus's own read (1). Evidence class: READ ONLY. Not a defect; a note so no one reads "lost" as "destroyed".

**W5 (Info, the held body's other sentences).**
- "The same shape loses one of two concurrent votes' tallies, independently of this PR." Not measured by gate 266 and not in the old fragments I compared. It follows from `castVote` reading a proposal and `dbSaveProposal` writing the whole votes array, so I believe it; I did not run it. If it is new in this round, it is an unmeasured claim stated flat.
- "nothing re-runs the handler": a lost consumer group is re-created at '0' and replays (handler comment, `userErasedSubscriber.ts:~28`; safe on a cleared row, and would in fact re-clear a stale write). So "nothing re-runs it" is true of normal operation only.
- The comment's "Auth 1845 of 1847" is the seat's number; gate 266 measured 1847/1847 at the old head. Understates; the code did not change. No action.
- "(our QA gate 266 ...)" appears inside the DPIA, a repo compliance document a client may be given. Internal gate numbers age badly there. Taste, not a finding.

## Q3. Every sentence in the five files and the two drafts

Checked against the head: the handler (`services/governance/src/userErasedSubscriber.ts`), migration 059 (three `DROP NOT NULL`, nothing else), `governanceService.ts` (`registerParticipant` 614-670, `selfRegisterParticipant` 698-745, `delegateVote` 1197-1215 refuses a cleared row, `dbSaveProposal` 144, the six callers), and gate 266's verdict.
- True and confirmed: the handler finds every row by id (`WHERE id = $1`, `delegator_id`, `delegate_id`, `proposer_id`, `voterId`); a legacy row keeps wallet, stake and votes; an admin naming that wallet still reaches the row (`dbGetParticipantByAddress` first in `registerParticipant`); `registerParticipant` is the only caller of `dbSaveParticipant`, whose upsert writes wallet and stake; `dbSaveProposal` callers are createProposal 869, submit 914, castVote 1017, finalize 1100, execute 1147, cancel 1181 (and the expiry job through finalize); 059 is three statements and has no down file; the dead letter is written and acked with no reader found; a delegation to or from a cleared row 404s (`:1211`).
- Overstated: W1. Understated: W2, W4, W5.
- The five files' prose has no other sentence I could find false at this head. Sentences quoting counts (15/15, 31/31, 386/386, 2601/2601, 123 passed, the 970 s leg 14) are the seat's; I re-ran none of them (NOT tested).
- Both drafts: 0 `@` and 0 `/Volumes` I did not re-count; I saw none reading them whole.

## Q4. docs-fragments check at the head

- At 8967de8b: `node Blockchain/Dev/scripts/docs-fragments.mjs check --root /private/tmp/g267/repo`: "flow 117 legacy + 213 new, cheat 112 legacy + 213 new; lint clean, render passes html_docs_check", `OK`, with 2 ADVISORY lines (flow line 6249, cheat line 6235), as the seat says.
- Planted defect: a stray `<div class="note">planted` appended to the KS-2060 cheat fragment. Result: `FAIL — 2 finding(s)` ("does not end with a newline", "tags are not balanced: <div> opened 4, closed 3"), rc 1.
- Restored with `git checkout --`; `sha256sum -c` OK; `git status --porcelain` empty; check again OK rc 0, 2 ADVISORY.
- NOT done: I did not run the check on develop 2935f723 to compare the two ADVISORY lines byte for byte with the seat's claim ("byte-identical to develop's"). They are the same two page positions the seat names.

## Q5. Merge tree and overlap

- `git merge-tree --write-tree origin/develop 8967de8b1755`: clean, tree `461c4b0be5aa45de6d9b6ff3b98a1dec5fa2db63` (develop 2935f723).
- Develop moved from the merge-base `c0e6e744b7b2` to `2935f723` over 14 files: 0 on the five doc paths (control: the same grep over `c0e6e744b7b2..8967de8b1755` counts 5).
- Open PRs: no `gh` (the rules allow git only). I fetched the heads of all 73 `refs/pull/N/head` with N >= 2030 into my clone and counted the five paths against each merge-base. Hits: PR 2099 itself (planted control, 5), PR 2076 (2) and PR 2051 (2). PR 2076 is the KS-2058 follow-up whose squash is `c0e6e744b7b2` (the branch's own base); it merges clean on develop. PR 2051 is the original KS-2058 PR, whose squash `44ee04cb` is on develop; its head conflicts with develop, so it is stale, not a live overlap. I could not read their open or closed state. Anything below N=2030 or opened after 17:06Z is not covered.

## NOT tested

- Linear and GitHub as posted: only the held drafts. Whether the comment is edited in place.
- The seat's counts (suites, mutants, the hook legs), the images, a runtime check of W2, F2 under real concurrency, any box, whether legacy participant rows exist anywhere.
- PR open or closed state for 2051 and 2076; PRs below 2030.
- The old-versus-new text of the held body beyond what I could read (I had no live body to diff, so W5's "new in this round" is unknown).

## Own conduct

- Wrote only this file and `/private/tmp/g267` (scratch files `sha.before`, `plant.out`, `rest.out`, `prs.txt`, `refspecs.txt`, `gs.ts`, `dpia.md`). Posted nothing. No git write verb in any `/Volumes/DevMASTER/!CODING` checkout; there I ran `ls-remote` and `config --get` only.
- In my clone I fetched, ran `checkout --detach` and restored one planted file with `checkout --`. I set `core.sshCommand` to the project's deploy key in my clone for the partial-clone fetches.
- The clone is left in place (QA no-rm): `/private/tmp/g267`, 547M by `du -sh` at the end.
- DevMASTER 14 GiB free at the end (above the 10 GiB stop). Load1 4.99 at start, 4.53 at the end; never above 8.
- Hook refusals: one `git -C $VAR fetch` (a variable path read as an outside write; re-run with the literal path), one `echo =====` zsh word. A case-sensitive multi-word `grep` got an advisory once; after it I used `/usr/bin/grep -i` with a positive control. One `git grep` over the partial clone timed out at 120 s (blob fetches); I then checked the tree out and used plain grep.
