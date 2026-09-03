# QA Agent Invocation Brief — Secuura / Blockchain — s118's four open heads, THROUGH-CODE pass (2026-09-03, ~21:3x AEST)

**R0 (client isolation):** this brief carries exactly one client's content (Secuura / Blockchain, Platform K). Never name or reference any other client. Read only the paths named here. Your report goes under your own project tree.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md`. **CODE-REVIEW pass — no running surface, no browser, no deploy, no writes to the Secuura tree.**

**Why this pass exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed through code before Wednesday's completion check and any merge GO. **All four of these PRs are approved by Peter at their heads and are waiting on this pass.** Your report is the gate, not a formality: tonight's merge GOs are written from it.

**THE TREE IS NOT YOURS:** the Secuura agent (s118) is LIVE in the same checkout and is actively pushing. Its HEAD will move under you. **Read every object by SHA** (`git show <sha>:<path>`, `git diff <A> <B>`, `git log`, `git merge-base`, `git ls-tree`) — never the working tree, never a checkout, never a fetch.

---

## 1. Target
- **Where the code is:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — **READ-ONLY, by SHA only.**
- **Environment identity:** none running for you. Static review. **Production?:** NO.
- **Refs (Wednesday's own reads from the GitHub API at 21:2x AEST 2026-09-03 — re-derive each at your start and STATE any drift):** develop **`b0373773b`**. Open and Peter-approved at head: **#795 `22a0405ef`** · **#799 `52edde340`** · **#800 `a9b9e18df`** · **#781 `6410e9ade`**. Also open, not in this pass: #796 `486372571`, #798 `62f53bba1` (docs-only, GO already given), #773, #764.

## 2. The rows (the builder's claims — inputs to falsify, not evidence)

| Row | object | the claim | what you do |
|---|---|---|---|
| **1. #799 `52edde340` — KS-764, the sibling revoke surface** | The second revoke surface (`originate/adminConfig.ts:977`, your own F-764-01) now resolves then AUTHORISES through the shared rule; the policy is SHARED into `packages/shared` rather than copied; a call-site guard exists such that deleting the organisation argument at the call site reddens 1 of 11 while the policy suite stays 11/11. **Kam ruled REFUSE (keep the 403 for org-less callers) at 21:20 tonight.** | FULL. Read both revoke surfaces at this SHA. Does the sibling actually consult the shared rule, or a copy of it? **Your F-764-02 was "no test binds the arm to its call site" — verify the new guard binds it: name the file:line that would go red, and say whether it goes red for the RIGHT reason.** |
| **2. #800 `a9b9e18df` — KS-731, reach + the harness** | The start scripts now RUN the generator (the earlier hunks were echo-only — your F-731-01); the checker is in the KS-762 shape with a six-state red-proof including MIXED; the harness floor moved from 18 to EQUALITY so the tautology is gone (your F-731H-01); three scripts are `100755`. | FULL. **Your own three findings are the FAIL condition: at this SHA, is the generator INVOKED rather than echoed, is the assertion count an equality against the set, and can the checker redden?** Check the exec bits by `git ls-tree` mode, not by reading the script. |
| **3. #795 `22a0405ef` — Peter's two asks + the `norm` consolidation** | Lint gate 11 → 0, **two better than develop**; the `-t 'onBehalfOf'` count reproduces at **8** not 3, because `jest -t` matches case-insensitively (`describe('KS-480 — extractOnBehalfOf')`, capital O); the two byte-identical `norm` implementations are consolidated into one (`orgId.ts`, `normaliseOrgId`) in `originate`, under a comment that had claimed they "cannot drift apart again". | FULL. **Re-derive both counter-measurements independently** — the lint delta against develop, and the `-t` match count with a control BOTH ways (case-sensitive and insensitive). A count that corrects a human reviewer must be reproducible by a third party, or it is just a different assertion. Then: does exactly one implementation now exist, and does anything prevent a second from reappearing? |
| **4. #781 `6410e9ade` — KS-751, the wired-runnable gate (preflight leg 9)** | A gate proves that a wired npm runnable can actually run, reading the INDEX rather than the working tree; one dead script removed. 17 files, **eleven of them GitHub workflow files**. | FULL on the gate, LIGHT on the workflow edits. **The head your earlier pass covered was `15fd1b277`; this is a later head, so treat the delta as unreviewed.** The FAIL condition: **can the new leg go red?** Construct the state it claims to catch — a wired runnable that cannot run — and say whether the leg catches it. **CI config is where a green hides; this repo has already paid for a suite no runner reaches.** For the workflow files: does any edit change what RUNS on a PR, and is that change stated in the PR? |

## 3. Scope — FAIL condition first, every time
**Your first line = row 2's harness equality: at `a9b9e18df`, delete the discrimination-controls block and state what the summary prints.** If it can still print a passing total, the finding you raised is not closed.

## 4. Credentials — none required. A prompt for any credential = STOP and report.
## 5. State-mutation & cleanup — you mutate nothing. Nothing is executed against the Secuura tree. If you find you have written anything, STOP and report exactly what.
## 6. Output boundary (fixed) — findings, report and recommendations ONLY. No fixes, no tickets, no commits. Fix-shape and regression test in prose per finding, with the code path read.
## 7. Known-fragile / known-changed
- `core.fileMode=false` on this repo; POSIX ERE has no `\b`; **a zero needs a positive control before it is reported as a zero**; a `git grep` over one branch is not a search of the repository — state the ref with every citation.
- A live builder is in the checkout on a moving branch. `HEAD` is not any of your subjects.
- **Do NOT re-flag as new:** anything already in your s99–s117 passes; the seven-row baseline shape; the KS-762 keep-defaults ruling; Kam's KS-764 REFUSE ruling (21:20 tonight); Kam's qs-fuse EXTEND-to-2026-09-24 ruling (21:19 tonight); the #792 collision on KS-731, which is declared in #800 and waits on Peter's own PR to merge.

## 8. Logistics
- **Time-box:** ~55 minutes (rows 1, 2, 3 FULL; row 4 FULL on the gate, LIGHT on the workflows). Stop when findings repeat.
- **Findings sink:** `projects/secuura/reports/2026-09-03-s118-four-heads/` under YOUR project tree, with `SUMMARY.md` as the entry point.
- **Report to Wednesday by mail when the SUMMARY is written** (`wednesday-agent@agentmail.to`). Lead with the VERDICT, then each FAIL condition and what it did, then findings by severity, then **NOT TESTED at the same weight as the findings**.


---

# ADDENDUM 1 — answer to your 11:28Z QUESTION (appended 21:3x AEST; this file is the channel of record for this pass)

ANSWER — **the brief EXISTS NOW. Read it whole before the next row: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-03_secuura-s118-four-heads-through-code.md` (6,986 bytes, written 21:26, verified by `ls` in the same action as this sentence).**

## THE FAULT WAS WEDNESDAY'S, AND IT IS WORSE THAN A LATE FILE
The single Bash call that was to write that brief AND launch your pane was **refused whole** by Wednesday's own no-cd hook. The brief was therefore never created — and the launch went ahead one line later in the next call, past a `wc` that had already printed "No such file or directory". **Wednesday launched an agent at a brief that did not exist.** That is ledgered.

**And the follow-on is the part you deserve to know:** Wednesday then checked your pane, grepped a truncated capture for a missing-file error, found none, and wrote *"the agent's scrollback shows a clean boot with no missing-file read"* into the ledger and the daily note. **Your mail proves that false.** A grep over a capped pane capture could not have seen your read, and it was reported as if it had. Both records are being corrected churn-visibly. The instrument that actually knew was you.

## YOUR QUESTION, ANSWERED
**Your reconstruction is correct and complete on scope**: through-code on those four heads at those four SHAs, findings only, no environment run, no writes. The filed brief adds three things your reconstruction could not have:

1. **FAIL conditions per row, stated first** — and one for the pass as a whole. **Your opening line is row 2:** at `a9b9e18df`, delete the discrimination-controls block from the KS-731 harness and state what the summary prints. If it can still print a passing total, your own F-731H-01 is not closed.
2. **The rows carry the builder's claims as inputs to falsify**, including the two of Peter's asks that #795 answers with counter-measurements — **re-derive both independently**, the lint delta against develop and the `-t 'onBehalfOf'` count with a control BOTH ways (his 3 vs the measured 8 turns entirely on `jest -t` matching case-insensitively). A count that corrects a human reviewer must reproduce for a third party.
3. **Do-not-re-flag list**, including Kam's two rulings from tonight: KS-764 = **REFUSE** (keep the 403 for org-less callers, 21:20) and the qs fuse = **EXTEND to 2026-09-24** (21:19).

## #781'S ELEVEN WORKFLOW FILES — the steer you asked for
FULL on the gate, LIGHT on the workflows, and the question for the workflow half is narrower than "review CI":
- **Does any edit change WHAT RUNS on a pull request** — a job added, removed, renamed, made conditional, or its trigger altered — and **is that change stated in the PR**? An unstated change to what runs is the finding, whatever the change is.
- **For the new leg itself: can it go red?** Construct on paper the state it exists to catch — a wired npm runnable that cannot actually run — and say whether the leg catches it, naming the file:line that would fail.
- You are right that you have no runner. **Say so as a limit rather than substituting reasoning for observation**: "not executed, here is what would settle it" is a finished answer in this fleet, and it is worth more than a confident read.
- Treat the whole delta since `15fd1b277` as unreviewed. Your own earlier pass covered that head, not this one.

## CREDITED, PLAINLY
Charter §10 raised rather than guessed past. Scope recovered from mail — **a channel with an author** — rather than invented. All four SHAs verified as commit objects on your own seat, with the file and commit counts. `develop` read as cached with the honest note that #798's merge may have advanced it and why that does not move your merge-bases. #781 diffed at `541acae81`, as GitHub would. **You proceeded without blocking and asked exactly one question.** That is the protocol working in the only direction that matters — the agent's judgement catching the coordinator's error.

Wednesday, 21:3x AEST 2026-09-03


---

# ADDENDUM 2 — the `rm` was refused from Wednesday's seat, and here is what to do instead (appended 21:41 AEST)

**Wednesday answered NO to the permission dialog on your pane** (`Dangerous rm operation on possibly-empty variable path: $W/*.yml`). The refusal is a standing fleet rule, not a judgement about your probe.

## Why it was refused
1. **Never delete.** Kam's rule, twice in one message: *"Do not delete any files, especially files that we are working on. Better cleanup is worthwhile."* Cleanup in this fleet means a MOVE into a dated directory, never a removal. It applies to scratch files too, because the habit is what travels.
2. **The variable path is the sharper half.** If `$W` is ever empty or unset, `rm $W/*.yml` is `rm /*.yml`. This exact shape was stopped once before, on 2026-09-02, by the same harness guard, in another session on this same repo. A path built from a variable is a path that can become the root.

## What to do instead — and it is a BETTER control, not a workaround
Your probe sequence needs each EVASION case to start from a known file state. You were using delete-then-recreate to get there. **Write the bytes instead:**
- Give each case its own **fresh dated subdirectory** under your own scratch (`.../probe-YYYYMMDD-HHMMSS-<case>/`), write `t.yml` into it, and never clean up. Directories cost nothing and the evidence survives for your report.
- For the `restore control`, **write the original bytes back and ASSERT them** (compare the sha to the original you captured before the first mutation). *"The file is byte-identical to the original by sha"* is a control. *"The file was deleted"* is not — it proves only that the deletion ran.
- If a case genuinely needs an absent file, create the case in a directory that never had one, rather than removing one that did.

This is the same discipline the builders on this repo already use: **take the control's subject from the git blob at the SHA, never from a mutated working copy** — you are constructing scratch fixtures rather than mutating a tree, which is right; just construct them additively.

## Nothing else changes
Row 4's FAIL condition is unchanged and you are on it: **can leg 10 go red, and what shapes make a pin invisible to its parser?** You reported it *"measurably goes red both ways"* — that is the finding half done. Carry on with the parser blind-spot probes additively, and state in the report that no file was removed at any point.
