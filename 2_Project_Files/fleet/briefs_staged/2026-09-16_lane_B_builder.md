# s240 — Secuura/Blockchain LANE B, systemTest harness builds (pane `Secuura/Blockchain-D`): KS-1076 item 2 (reproduce the CI-only unit-cell failure FIRST, then a test-only fix if it is confirmed) → KS-998 item 1 (Kam ruled `a`). Each ends READY FOR QA → Wednesday's GO naming the head SHA → you squash-merge as author. Nothing deploys and nothing goes to Peter or Stuart.

## BLUF
- **Who and where.** You are **s240**, LANE B, pane **`Secuura/Blockchain-D`**. Remote `git@github.com:Secuura/Distributed_Secuura.git` (identity `kksecura`, board account `kamil.kreiser@secuura.ai`). Every branch is cut **from `origin/develop`**, and all work happens in **your own git worktree**, one per item: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s240-ks1076` and `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s240-ks998`. Never switch branches, pull or edit in the shared checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. The one write you make there is the `fetch` in ITEM 0.
- **Authority (Kam, panel 2026-09-16 20:40:59, verbatim):** *"you have the approval to spin up other local agents to test, approve, merge and move things forward"*. Confirmed 20:41:47: *"yes.  claude agents"*. **Approval of a PR = Wednesday's GO mail naming its head SHA**, sent after a QA gate verdict at that head plus your Test Evidence block (the 2026-09-11 TESTED grant). **NOT covered:** deploys (kintsugi or demo), demo/UAT, external communication beyond ticket comments, `.github/workflows` PRs, other authors' PRs.
- **develop at drafting: `0b25f823f6660ac52b665f14055799ff0c3b616d`** (Peter's merge of #997, 2026-09-15T14:22:41Z). This SHA is **not in the local object store**, which has M55 `48e65c435` (read with `git cat-file` at 20:5x). **M55 → tip touched 36 files, all under `systemTest/schemathesis/**`, `systemTest/CLAUDE.md` and `Projects Documents/`.** None of your four files moved.
- **Your partition (write).** Nothing outside these four files:
  - `systemTest/playwright/tests-unit/slot-required.test.ts`
  - `systemTest/playwright/config/slotRequired.ts`. Only if ITEM 1 proves the product is the defect, and only after a QUESTION.
  - `systemTest/scripts/check-package-format.sh`
  - `systemTest/__tests__/package_format_gate.test.sh`
- **NOT yours. Other seats run in parallel.**
  - Raise seat A: `Blockchain/Dev/services/{api-gateway,demo-service,auth}/**` and `Blockchain/Dev/packages/shared/**`.
  - Raise seat B: `Blockchain/Dev/services/{security,originate,anchoring,vc-issuer,kyc}/**`, `Blockchain/Dev/docs/openapi/secuura-api.yaml` and `Blockchain/Dev/docs/VOCABULARY.md`.
  - Raise seat C: `Blockchain/Dev/scripts/**`, **`.githooks/**`**, `Start_Up/**`, `systemTest/{akto,performance}/**`, `systemTest/schemathesis/validate-lint.sh`, `Blockchain/Dev/deployment/**`, `Blockchain/Dev/CONTRIBUTING.md`, `Blockchain/Dev/docs/DEV-PROCESS.md` and repo-root `CLAUDE.md`.
  - Lane C seat s241: `Blockchain/Dev/services/timestamping/**`, plus the files of open PRs #995, #922, #927, #989, #923 and #920 (merge duty, by ADDENDUM).
  - **Also never touch `systemTest/fixtures/**` or `systemTest/__tests__/{pre_suite,quarantine_call_sites}.test.sh`.** Those are #989 and #927.
  - **`.githooks/pre-push` calls your gate, but it is raise seat C's file. READ it and never edit it.**
  - A change that seems to need a file outside your partition is a QUESTION mail, never an edit.
- **The shared inbox.** All five Blockchain panes read **`secuura-blockchain@agentmail.to`** (`inbox_routing.conf`). **A mail that names another seat (Seat A/B/C, s241) or a PR/ticket not in your QUEUE is not yours.** Wednesday's mails to you carry `s240` in the subject.
- **Ends at:** both items merged, or READY and waiting with the queue dry (then a STATUS mail and end the turn), or Wednesday's 70% mail.

## QUEUE
1. **ITEM 0**: fetch, pins, plan mail.
2. **ITEM 1: KS-1076 item 2** (Urgent · Todo · board account). Scope, the ticket's own words, item 2: *"Then confirm the suite actually runs and report what it finds — three days of unrun e2e may be hiding real failures. A green job after the lint fix is not the same as a suite that was green all along, and it must not be reported as one."* Where that item stands now (s215's comment 2026-09-13T22:19Z): *"step 7 `Quality gate — unit suite (test:unit)` FAILS on the Playwright harness's own unit test — `✖ assertSlotNamedForLocalTarget › refuses every slot's gateway when no slot is named, naming both forms of the slot command` (`AssertionError: Missing expected exception: slot 1`) … Steps 8 … 9 … 10 `Run Playwright API tests` are SKIPPED"*. **Item 1 is already fixed and recorded. Item 3 is Kam's workflow call and not yours.** The ticket therefore stays OPEN after your PR (`Refs KS-1076`, never `Closes`).
3. **ITEM 2: KS-998 item 1 ONLY** (High · Backlog · board account). Scope, the ticket's words, item 1: *"`check-package-format.sh` prints `SKIP (advisory)` and **exits 0** when `node_modules/.bin/prettier` is missing, so on a fresh clone the red is pushed and nothing says so."* The fix is Kam's ruling `a` (below). **Items 2–4 are NOT this PR.** The card says they are *"a Sunday Claude seat's in one PR"*. So `Refs KS-998`, never `Closes`.

## ITEM 0: measure, then the plan mail
1. `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" fetch origin > <records>/fetch.out 2>&1; rc=$?`. This is your write.
2. Then read the pins. **A moved pin means STOP on that item and mail.**
   - `ls-remote` develop = `0b25f823f` **or a child**. If it is a child, `git diff --name-only 0b25f823f <new>` must touch none of your four files.
   - Blob of `systemTest/playwright/tests-unit/slot-required.test.ts`, and the lines `assertSlotNamedForLocalTarget` → `if (isCi(process.env[CI_ENV])) { return; }` in `systemTest/playwright/config/slotRequired.ts`. **Wednesday read them via the GitHub contents API at `0b25f823f`: the early return sits at `:88-90` (the test's `afterEach` at `:42-46`, the failing cell at `:49-62`).**
   - `check-package-format.sh` `:142-148`, the advisory SKIP. Read at the same ref.
   - KS-1076 Todo, KS-998 Backlog. Linear `issue(id)` with `comments(first:50)`, sorted client-side.
   - **No open PR touches your four files.** Walk every open PR's `/files`. Wednesday read 18 open at 20:5x, and none did for the 8 `kksecura` PRs.
3. Mail `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation s240`. Put **every warning your launcher printed at boot VERBATIM** in it.
4. **Proceed WITHOUT waiting for the ANSWER if every pin holds and you deviate from nothing** (Wednesday's default at drafting, to be confirmed at send). A moved pin or a deviation makes it a real QUESTION.

## ITEM 1: KS-1076 item 2, reproduce FIRST
- **The hypothesis, from reading the source. NOT reproduced by anyone yet:**
  - `assertSlotNamedForLocalTarget` returns early when `isCi(process.env.CI)`.
  - The first cell of the `describe` never clears `CI`. The file's `afterEach` deletes `CI` only AFTER each cell.
  - On a GitHub runner `CI=true` is inherited, so cell 1 sees CI, nothing throws, and the result is "Missing expected exception: slot 1".
  - Cells 2+ run after the first `afterEach`, so they throw as intended. That matches `tests 371 · pass 370 · fail 1` on develop's own push run at `0b25f823f` (the survey's read of the Actions job log).
- **(a) Reproduce in your worktree** (detached at develop, `npm ci` in `systemTest/playwright`):
  - `npm run test:unit` with `CI` unset: expect all green.
  - `CI=true npm run test:unit`: expect exactly that one cell red.
  - **Redirect both to files; `rc=$?` on its own line.**
  - **If the unset run is ALSO red, or the CI run is green, the hypothesis is wrong.** STOP, mail a QUESTION with both outputs, and build nothing.
- **(b) If confirmed, the fix is TEST-ONLY.** The cell (or the file, in a `beforeEach`) must start from a known environment: `CI` and the two slot variables cleared before the assertion. **The CI exemption is by design** (the test file's header, and the thrown message's *"CI (CI=true) is exempt"*), so the product file stays untouched.
  - **Control that must stay green:** the existing cell `exempts CI, whose local per-suite stack is deliberately unslotted` (`:93-98`, it sets `CI=true` itself and asserts no throw). It proves the exemption still returns, so the fix cannot pass by deleting the exemption. Name it in the READY with its result under both runs.
  - **Red-proof:** the fix removed → `CI=true` red on exactly that cell; the fix present → green under both. Anchor uniqueness is proven before the tamper, and the restore is checked by sha256 (STANDING_LINES).
- **(c)** Branch `feature/ks-1076-item2-slot-cell-ci-env` from `origin/develop` → ONE commit → push (the hook runs; never `--no-verify`) → PR `Refs KS-1076`.
  - The Test Evidence block goes in the body: Touched / Ran (with ratios) / NOT run / Migrations+config.
  - One facts comment on KS-1076 naming the PR.
  - **Commit and comment attribution:** the cell came from commits `0882f7661` (KS-1167) and `3537c9828` (KS-1016), author field `t`. Say that as a fact, with no @-mention.
- **(d) "Confirm the suite actually runs"** is the ticket's own DoD for item 2, and your PR's own Actions `pr` run is where it is measured.
  - Read the run for your head: job `Playwright suite`, steps 7–10 by name, conclusions, and the step-10 test tally from its log.
  - **Actions is advisory, not a required check. You change nothing about workflows.**
  - If steps 8–10 run and step 10 has failures, that is the finding the ticket predicted. Put ONE facts comment on KS-1076 with the failing set, and fix NOTHING in this PR. Wednesday decides where it goes.
  - If no `pr` run exists for your head, write *"unmeasured: no Actions run at <head>"*, never a pass.
- **(e) READY FOR QA.** The tier is Wednesday's to name. The survey proposed tier 1. Your READY states that the change is test-only and names the one cell.

## ITEM 2: KS-998 item 1, the spec is written; measure its premises
- **Spec (read whole):** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-998.md`. It gives the exact hunk at `check-package-format.sh:142-148`, and CASE 6 of `package_format_gate.test.sh:131-138` flipped to pin the REFUSAL. CASE 9 (`--all` still skips) stays as the CONTROL.
  - It was written for the local model at M55 and failed twice there on patch FORMAT (`done.md` rows 184 and 185: *"FAIL B3b"* and *"FAIL B2 … corrupt patch"*), not on design. **Apply it by hand. The spec is the content, not a patch to `git apply`.**
- **Premise 1, unmeasured. Measure it in your first turn.** Kam's ruling says *"a tracked file under that package is in the push"*. The script's non-`--all` path selects a package when a path on STDIN lies under `systemTest/<pkg>/`. **READ** `.githooks/pre-push` (`:229-250` at M55) and establish what `$all_changed` holds.
  - If it is the tracked paths of the pushed range, the spec's `MODE != all` branch is the ruling.
  - If it is anything else (the working tree, or untracked files), mail a QUESTION before building.
- **Premise 2, read from the hook at M55. A residue you REPORT and do not fix:** when the hook cannot compute a base (`st_all=1`, KS-854/KS-882), it runs the gate with `--all`. **The advisory skip then survives even for a push that touches the package.** Put that in the READY's NOT-covered block, with the hook line. `.githooks/pre-push` is raise seat C's file.
- **Red first:** the new CASE 6 checks on the untouched tree fail by value (the tip prints `SKIP (advisory)`, exits 0 and counts `1 skipped, 0 failed`). After the hunk, all four pass and CASE 9 stays green.
  - **Tamper:** the inner `if [ "$MODE" != "all" ]` block removed → CASE 6 red, CASE 9 green.
  - Print the suite ratio, never "all".
- Branch `feature/ks-998-item1-format-gate-refuses-missing-deps-in-push` from `origin/develop`. Move KS-998 **Backlog → In Progress** when you start: one CAS state write, read back. ONE commit, then the PR `Refs KS-998`.
  - The PR body cites the card `secuura-ks998-format-gate-fails-open-on-missing-deps` → `a`, with its option text verbatim.
  - ONE facts comment on KS-998 naming the PR and saying items 2–4 stay open.
  - READY FOR QA.

## THE FLOW (every PR)
1. **Build:** own worktree, branch from `origin/develop`, red-first, then green, then the tamper.
2. **Own tests:** the package suite whole. The ratio is printed.
3. **PR:** body with the Test Evidence block you wrote from your own runs, NOT-covered lines, and the ticket link. A facts comment on the ticket names the PR.
4. **Mail** `[Secuura/Blockchain -> Wednesday] READY FOR QA — PR #<n> @ <full sha> s240`. Read the head with `ls-remote` in the same action. The body carries the PR URL, the ticket comment id, the files, what ran, and what was NOT run.
5. **STOP that PR until Wednesday's GO.** The GO arrives as `[Wednesday -> Secuura/Blockchain-D] GO s240: #<n> @ <sha>` and must be spf/dkim/dmarc `pass`. **Merge only if `<sha>` equals the PR head read from origin NOW.** If they differ, do not merge; mail a QUESTION. **An old GO never covers a new head.** Meanwhile, start the next queue item.
6. **Squash-merge as author:** `gh pr merge <n> --squash --match-head-commit <sha>`. **No `--admin`.**
   - If GitHub refuses (for example a required approval appeared: 422, because kksecura cannot approve kksecura), STOP and mail. Never route around it.
7. **Re-read develop at origin** (`ls-remote`). The PR must be `MERGED`; note the merge commit. Ticket state stays open (both items leave residue): ONE facts comment with the merge SHA. Undo any state move the Linear integration made, by CAS, and say so.
8. **Findings from the gate:** fix on the same branch, taking develop in by `merge --no-ff` (never rebase, never force), re-run, and send a new READY with the new head.

## HOLDS: standing, every Secuura brief
- **Read whole and apply:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`. READY = five artefacts; `cmd > out 2>&1; rc=$?`; three-dot diffs; unique tamper anchors; verdicts as ratios.
- **Usage (Kam, panel 2026-09-16 21:1x): *"try not to go beyond 40% token allocation"*** (the weekly gauge; `fleet/USAGE_STOP` = 40, read 8% at 21:1x). Every QA gate for your PRs is a launch through `usage_gate.sh` and refuses past the cut. **If Wednesday mails STOP for usage: finish the step in hand (a push completes), mail the PR's state, and wrap.** A READY that gets no gate before the cut waits; it is not re-asked.
- **Signature classes pause for Kam, always:** production · money · external communication to any human · anything irreversible. **Never guess** (Kam 2026-09-14 16:19: *"do not guess. Analyze and check."*).
- **Never deploy.** No kintsugi, no demo, no remote `docker compose`, no `.env` or wallet touched. KS-535 is absolute. Project hold: no deploy without migration 048 first (KS-1031).
- **Never `--no-verify`, never force-push, never `--admin`, never `-u` on someone else's branch.** A hook that stops you is a question; answer it.
- **Client-facing communication is TICKET COMMENTS ONLY**, facts only, with **0 at-signs**. The extranet is input only. Nobody but Kam messages Peter or Stuart.
- **Handovers to Peter/Stuart are TEST BLOCKS, never a list of PRs.** Wednesday composes them; you do not hand over.
- **A ticket on Peter or Stuart stays theirs.** New or unassigned tickets go to the board account. Both of yours are already on the board account.
- **Filing:** search the board by SYMBOL / path / error string first and say what you searched. The unit of a ticket is the TEST PASS (Kam 2026-09-07 13:23). Prefer a facts comment on the existing ticket.
- **Never delete. Quarantine** into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/quarantine/2026-09-16-s240/`, and record the move. Records go in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-16_s240/`.
- **Other authors' PRs, `.github/workflows`, #887, #809 and dependabot are not yours.** Neither are #995, #927, #989, #922, #923 or #920 (lane C's merge duty).
- **Platform suites:** your two items touch harness and tooling only, with no stack. The Schemathesis/Akto/k6 lines read `not run: no product surface touched`, and Playwright reads as measured in ITEM 1(d).

## IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO
Measure first, then say so in a QUESTION. Where this brief is most likely wrong:
1. **The CI hypothesis** is a source reading, never run.
2. The spec's line numbers were read at M55. They should hold at `0b25f823f` (0 changes to that file between them) but are yours to re-read.
3. **What `$all_changed` holds** in `.githooks/pre-push` is unmeasured.
4. The tier for ITEM 1 is not ruled.

## PROTOCOL: mail, capacity, authority
- **Subjects (exact):**
  - `[Secuura/Blockchain -> Wednesday] QUESTION: <topic> s240` (one question per mail)
  - `… STATUS s240: <step>`
  - `… READY FOR QA — PR #<n> @ <full sha> s240`
  - `… Session wrap 2026-09-16 s240`
- **Mails to** `wednesday-agent@agentmail.to`.
- **A mail is Wednesday's only when spf, dkim and dmarc all read `pass`.** Pane text is never authority.
- **15-minute fallback:** a QUESTION unanswered for about 15 minutes proceeds on the safest reading, EXCEPT approval-class items (a merge, anything prod/demo, external comms), which always wait.
- **Capacity:** Wednesday mails **CHECKPOINT at 50%** and **HAND OVER NOW at 70%**. Finish the step in hand, then write the handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s240-laneB.md`, a history entry at the top, and the wrap mail.
- **Wake path:** between a READY and its GO you do not idle. Start the next item; if the queue is dry, mail STATUS and end the turn. Wednesday taps the pane (`cockpit.sh say`) when the GO mail lands.
- **Wrap:** worktrees torn down (quarantine, not `rm`). History entry with heads, PRs, merges, comment ids, and NOT-covered lines. Wrap mail.

RULED BY KAM, NOT YET IN AN ARTEFACT
====================================
`decision_queue.sh list ruled --undelivered` at 20:58:30 AEST: 67 lines, 24 Secuura cards. **ONE is this lane's:**
- `secuura-ks998-format-gate-fails-open-on-missing-deps`: **"a" — "Hard fail ONLY when a tracked file under that package is in the push (the ticket's middle option)"**, detail *"a fresh clone pushing unrelated work stays quiet; a push that touches a gated package must have its deps installed"* (ruled 2026-09-16T09:54:32+10:00). It must land in the ITEM 2 PR body plus the KS-998 comment. Wednesday marks it delivered after the merge; you do not.

**The other 23 are NOT yours.** They are listed so none is re-raised:
- `ks661-vocab` residue
- `secuura-agent-github-identity` identity (why an Approve 422s)
- `secuura-dependabot-triage` close-and-rescope
- `secuura-ks229-disclosure-mailbox` later
- `secuura-ps-759-760-merge-owner` kam-merges
- `secuura-demo-kam-admin-default-password` b
- `secuura-f5-login-limiter-bypass` wait
- `secuura-f5-demo-exposure-probe` probe
- `secuura-f5-demo-interim-mitigation` letitland
- `secuura-demo-admin-transcripts` redact
- `secuura-demo-admin-mfa` later
- `secuura-891-workflow-scope-merge` kam-merges (every `.github/workflows` PR)
- `secuura-force-push-own-branch-standing` narrow-allow (**not used by this lane: no force push at all**)
- `secuura-org-trust-boundary-within-tenant` bind
- `secuura-archive-fifteen-platform-s-tickets` archive
- `secuura-advisory-gate-moving-set` both
- `secuura-advisories-high-and-prod-reaching` measure-first
- `secuura-four-advisories-ruled-after-measurement` bump
- `secuura-required-approvals-zero-after-the-untick` raise-to-1 (STILL UNAPPLIED: `required_approving_review_count: 0` per the survey's GH-RULES read; if it is applied mid-run your merge 422s, so STOP and mail)
- `secuura-ks1011-stack-marker-unknown-on-restore` b (raise seat C)
- `secuura-ks1081-two-env-templates-which-is-canonical` a (raise seat C)
- `secuura-ks1168-ilike-search-on-encrypted-pii` a (sequenced after raise seat A's KS-999)
- `vault-add-a-stages-another-clients-files` grant-both (fleet)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **(2026-09-14, AUTH4 answers) The merged-tree rule:** where develop also moved a file the PR touches, the equality target is the gate's MERGED-tree blob, not the raw head blob. **In your path:** unlikely, since develop has not moved your files since M55. If it does before your merge, STOP and mail.
- **(2026-09-13 L1) No `@` mention anywhere.** Reviewer questions are answered by file:line on the PR.
- **(2026-09-14 07:2x) Develop merge-ins are `--no-ff`, never rebase, never force.** A file outside your partition that must change is a QUESTION with a 15-minute default.
- **(2026-09-15 07:57Z counter) Local-model failures:** KS-998 was REALLOCATED to a Claude seat after two failed rounds. Do not hand it back to the local model.

PROVENANCE:
- develop tip 0b25f823f6660ac52b665f14055799ff0c3b616d; PR heads #995 b8155636e #927 1041d2d32 #989 e62fd23cd #922 e60a24c50 #923 d127dc7d4 #920 2112a99e3 #809 aa2270fe1 | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin (20:56:23 AEST) | read 2026-09-16
- local origin/develop = 48e65c435 (M55); 0b25f823f absent from the object store | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files rev-parse origin/develop | read 2026-09-16
- M55...0b25f823f = 4 commits, 36 files, all systemTest/schemathesis/**, systemTest/CLAUDE.md, Projects Documents/; none of this lane's four files | GitHub REST GET /repos/Secuura/Distributed_Secuura/compare/48e65c435...0b25f823f with Secuura GH_TOKEN (never printed) | read 2026-09-16
- slotRequired.ts early CI return at :88-90; slot-required.test.ts afterEach :42-46 deletes CI after each cell, failing cell :49-62, exemption control cell :93-98 | GitHub REST GET /contents/<path>?ref=0b25f823f (raw), saved to the drafter scratchpad | read 2026-09-16
- last commits on those two files 0882f7661 (KS-1167, 2026-09-14) and 3537c9828 (KS-1016, 2026-09-11), author field t | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files log 48e65c435 -- <both paths> | read 2026-09-16
- test:unit = node --import tsx --test ./tests-unit/*.test.ts | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files show 48e65c435:<the playwright package.json> (your repo, commit M55) | read 2026-09-16
- develop push run at 0b25f823f: step 7 unit suite failure, tests 371 pass 370 fail 1, steps 8-10 skipped | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-16_attention_RANKED.md row 1 (GH-ACTIONS job 104424719141, the survey's read; not re-read by this drafter) | read 2026-09-16
- KS-1076 Todo, Urgent, board account, item 2 scope sentence, s215 comment 2026-09-13T22:19Z (step 7 cell failure, steps 8-10 skipped) | Linear GraphQL issue(id:"KS-1076") comments(first:50) sorted client-side, Secuura LINEAR_API_KEY | read 2026-09-16
- KS-998 Backlog, High, board account, item 1 scope sentence, 0 comments | Linear GraphQL issue(id:"KS-998") comments(first:50) | read 2026-09-16
- check-package-format.sh advisory SKIP at :142-148, stdin selection by ^systemTest/<pkg>/, trailer :193 | GitHub REST GET /contents/systemTest/scripts/check-package-format.sh?ref=0b25f823f | read 2026-09-16
- package_format_gate.test.sh CASE 6 at :131-138 | GitHub REST GET /contents/systemTest/__tests__/package_format_gate.test.sh?ref=0b25f823f | read 2026-09-16
- .githooks/pre-push :229-250 calls the gate with --all when st_all=1, else pipes $all_changed | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files show 48e65c435:<the pre-push hook> (your repo, commit M55) | read 2026-09-16
- KS-998 spec and hunk | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-998.md | read 2026-09-16
- KS-998 local-model rounds FAIL B3b and FAIL B2, reallocated 18:0x | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/done.md rows 184-185 | read 2026-09-16
- card secuura-ks998-format-gate-fails-open-on-missing-deps => a, option text, ruled_ts 2026-09-16T09:54:32 | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-ks998-format-gate-fails-open-on-missing-deps | read 2026-09-16
- 24 undelivered Secuura cards | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered (20:58:30) | read 2026-09-16
- raise seats A/B/C partitions (who else writes; the scope of every other seat) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-16_raise_PLAN.md section 3 table | read 2026-09-16
- 18 open PRs, none of the 8 kksecura PRs touches this lane's four files | GitHub REST GET /pulls/{n}/files for #995 #927 #989 #922 #923 #920 #809 | read 2026-09-16
- inbox shared by Secuura/Blockchain and -B..-E = secuura-blockchain@agentmail.to | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-09-16
- Kam's grant 20:40:59 and 20:41:47 verbatim | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-16_new-account-spin-up-agents-to-test-approve-merge.md | read 2026-09-16
- weekly usage 8% (< 40 cut) | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check (21:1x) | read 2026-09-16
- usage cut 40% and Kam's words "try not to go beyond 40% token allocation" | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/USAGE_STOP lines 1-2 | read 2026-09-16

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-16 21:20
