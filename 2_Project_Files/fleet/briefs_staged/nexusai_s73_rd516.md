# BLUF

**You are S73 on Datasec/NexusAI. ONE item: RD-516 — the `ai-test` SSRF. It is the LAST thing
between us and the marketplace resubmission package, and it is unstarted.**

**Kam tonight, verbatim: *"I would much rather it done properly than quickly."*** There is no
deadline on this. A NO GO costs a round; a wrong fix on a security endpoint costs a customer.

**Do NOT start anything else.** RD-518 is at its gate in another pane; RD-464 r3 is merged;
RD-578 and RD-579 are filed and are not yours tonight.

# 1. THE TICKET (read it at source before you act — this is a summary, not the record)

**RD-516, High, To Do.** `POST /api/setup/ai-test` makes the server connect to **any caller-named
URL** when a key is in the body — no `*.openai.azure.com` host check, which `ai-config` *does* have.
**Server-side request forgery, reachable ANONYMOUSLY in the open first-run window.**

Its own Recommendation: *measure what the response reveals and whether internal addresses are
reachable from Container Apps; then restrict the ai-test endpoints to the same Azure OpenAI host
rule as ai-config (and refuse private/link-local targets), red-first.*
Found by the RD-486 builder 2026-09-17 (S64). Related: **RD-511** (IMDS probe on page load).

# 2. 🔴 PRIOR WORK — IT EXISTS, IT IS GOOD, AND THE BRANCH IS A TRAP

S70 authored a design and cells that were lost outside version control and later rescued.
**Branch `rd-516-cells-s70-recovered` @ `89fbea58114e1f8ed3fdc49bacab5d51d8935da1`, at origin.**

**Measured by Tuesday before writing this, so you do not have to:**
- Its merge-base with main is **`354d9ff`** — the branch is **9 commits BEHIND current main
  (`60c76d7`)** and adds **exactly ONE commit** on top of that base.
  *(It was 5 behind `34ad321`, which was main when Tuesday first measured it; r3's merge landed in
  between. The number is stated against `60c76d7` because that is what you will diff against.)*
- 🔴 **THEREFORE: `git diff 34ad321..89fbea5` shows ~2,400 "deletions". THEY ARE NOT DELETIONS.**
  They are main's own nine newer commits (RD-545, RD-549, RD-464 r3 and the rest) absent from the
  older base — and the count grows every time main moves, so measure it, do not quote this number.
  **Tuesday's first reading of that diff was wrong and the merge-base is what settled it.**
  **DO NOT merge this branch into main. DO NOT rebase it. DO NOT treat that diff as a change set.**
- **Take the five files by PATH.** They are the whole of the one commit, and **none of the five
  exists on main** (checked both directions):
  - `docs/rd516/2026-09-18_S65_rd516-ssrf-design.md` (996 lines — the design)
  - `__tests__/helpers/rd516-cells-s70-NOT-RUN/rd516-ai-test-ssrf.test.js`
  - `__tests__/helpers/rd516-cells-s70-NOT-RUN/rd516-net-harness-preload.js`
  - `__tests__/helpers/rd516-cells-s70-NOT-RUN/README.md` and `RESCUE.md`

🔴 **THE CELLS ARE AUTHORED, NEVER RUN AND UN-GATED.** They sit under
`__tests__/helpers/`, which is in `testPathIgnorePatterns`, so **jest does not collect them today —
that is deliberate, and it is the only reason they are inert.** This project sets **no `testMatch`
and no `roots`**, so jest's default collects `*.test.js` from anywhere under rootDir: **the moment
you move them out of `helpers/`, they ARM.** Move them only when you intend them to run, and prove
what you armed with `jest --listTests` plus a control, exactly as S71 did for the rescue.

**Read the design before writing anything.** Keep what is right, improve what needs work, remove
only with a stated reason — and **your READY must carry a PRIOR WORK section** saying what of S70's
you kept, changed or dropped, and why. A handover without one comes back.

# 3. WHAT THE FIX HAS TO DO — and the order matters

1. **MEASURE FIRST, per the ticket's own Recommendation.** What does the `ai-test` response actually
   reveal to the caller — status, headers, body, timing? And is a link-local / private target
   reachable from the runtime at all? **Measure it locally; do NOT probe any real Azure endpoint and
   do NOT deploy.** A finding of "unreachable from Container Apps" narrows the severity and is worth
   knowing; a finding of "reachable, and the body comes back" widens it.
2. **RED FIRST.** A cell that fails on today's code for the right reason, before the fix exists.
   **The cell asserts the PROPERTY THAT MUST HOLD AFTER the fix, never the defect that exists
   before it** — test it by its future: if the cell would go red when the ticket is closed, it is a
   bug-pin, not a guard.
3. **Then the fix:** the same host rule `ai-config` already applies, plus refusal of private and
   link-local targets. **Read `ai-config`'s existing check and reuse it — do not write a second
   implementation of the same rule.** Two implementations of one idea disagree by default.
4. **Mutation-prove it.** For each guard, a mutation that reddens ITS OWN cell and, ideally, nothing
   else. Restore and verify sha256 after each.
5. **Counts:** predict tests/suites BEFORE regenerating, then **read the number OUT OF THE FILE** —
   `--update-counts` does not write on a failed run, so a command's exit proves nothing. If the file
   disagrees with your prediction, **the disagreement is the finding**; do not reconcile the file.

# 4. 🔴 HARD STOPS

- **No deploy, no merge to main, no real Azure, no real credentials.** Your round ends at
  **READY FOR QA**.
- **Do not touch RD-518's branch `rd-518-kv-identity-s72` or `6ea15a0`** — a gate is measuring it
  right now, and a second writer invalidates the verdict.
- **Do not widen into RD-511** (the IMDS probe). If your measurement shows they must be fixed
  together, **say so and STOP** rather than folding it in.
- **The signature classes are unchanged**: production, money, external communication, anything
  irreversible. Kam's ruling tonight lifted a SPEND constraint, nothing else.
- Anything that changes what a deployment DOES rather than what it REPORTS comes to Tuesday first.

# 5. STANDING LINES

- **PRIOR-WORK CHECK** (above) — mandatory section in your READY.
- **A pane is not a channel.** When you want an answer, the turn ends on a MAIL, not on a message in
  your pane. Tuesday's watcher catching an idle pane is a backstop, not the mechanism.
- **Every claim carries its instrument inline** — *"by the diffstat"*, *"read from the file"*,
  *"`ls-remote` at 21:4x"* — or the honest word **unmeasured**.
- **Every zero gets a control** in the same action that could have produced a non-zero, and the
  control must be able to fail independently of the failure you are testing for.
- **A 204 or a 201 says the server accepted a request; it does not say what it kept.** Read it back.
- Never `--no-verify`. Never delete — quarantine.
- **zsh: brace a ref before a colon** (`${SHA}:path`), or `:r` is parsed as a variable modifier —
  it cost S72 a push tonight and it is on RD-464's comment 37879.

# 6. WHAT TO SEND, AND WHEN

- **A plan confirmation first** (mail, not pane), naming: what you will measure in step 1, the cells
  you will write, and anything in S70's design you intend to drop.
- Then work. **READY FOR QA** when steps 1–5 are done, with the PRIOR WORK section, the branch and
  head SHA, sets-not-counts, and what you did NOT do.
- **If something blocks, mail Tuesday and move to the next thing you can do** — do not wait idle.
  If nothing else is available, say so.

**Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`.
⚠ **Its working checkout is at `cd2b543`, which is NOT origin/main (`60c76d7`) — pull before you
branch, and say what you pulled.**

# RULED BY KAM, NOT YET IN AN ARTEFACT

- **`nexusai-degraded-flip-and-live-deployments`**: *"Decision nexusai-degraded-flip-and-live-deployments: a — Tell me the deployment count and I decide from there (Recommended)"* (panel, Tuesday tab, 2026-09-20T21:14:57 AEST) → **must land in a comment on RD-518**, recording that the DEGRADED status flip stays unshipped until Kam has a live-deployment count and rules on it.
  **NOT yours to action tonight and it does not touch RD-516** — it is listed because this section must be complete, and because it is the reason RD-518 shipped without the flip. Tuesday is handling the count question with Kam directly.

- `nexusai-privacy-keyvault-claim-rd518` (*"a — Fix RD-518 before submission; change no documents"*) is **DELIVERED** — RD-518 comment 37877 / C-105, read back out of Jira. Listed so you do not re-raise it.


PROVENANCE:
- RD-516 is To Do / High, and its summary + BLUF + Recommendation are quoted verbatim above | Jira REST GET /rest/api/3/issue/RD-516?fields=summary,description,status,priority, flattened ADF | read 2026-09-20 by Tuesday
- rd-516-cells-s70-recovered is at origin @ 89fbea58114e1f8ed3fdc49bacab5d51d8935da1 | git ls-remote --heads origin rd-516-cells-s70-recovered, in your own tree /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-20 21:4x by Tuesday
- its merge-base with main is 354d9ff42cac5db6d32d5ecec6b89a6da95abe0d; main (34ad321) is NOT an ancestor of it; main is 5 commits ahead of that base and the branch adds exactly 1 commit | git merge-base 89fbea5 34ad321; git merge-base --is-ancestor 34ad321 89fbea5 (non-zero); git rev-list --count on both ranges | read 2026-09-20 21:4x by Tuesday
- the ~2,400 "deletions" in git diff 34ad321..89fbea5 are main's own newer commits, not changes made by the branch | derived from the merge-base measurement above, after Tuesday's first reading of the diffstat was wrong | read 2026-09-20 21:4x by Tuesday (Tuesday's own earlier misreading, corrected by this measurement)
- the branch is 9 commits behind main at 60c76d7 (and was 5 behind 34ad321, the earlier main) | git rev-list --count 354d9ff..60c76d7 and 354d9ff..34ad321 in your own tree /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-20 21:5x by Tuesday
- the branch's one commit carries exactly 5 rd516 paths, and 0 of them exist on main | git ls-tree -r --name-only 89fbea5 | grep -ic rd516 = 5; the same on 34ad321 = 0 (both directions checked) | read 2026-09-20 21:4x by Tuesday
- the cells sit under __tests__/helpers/, which is in testPathIgnorePatterns, and this project sets no testMatch and no roots | measured at source by Tuesday 2026-09-20 afternoon, recorded in the seat ledger; S71 proved the placement inert with jest --listTests plus a control | read 2026-09-20 by Tuesday
- main is 60c76d7 at origin and the NexusAI working checkout is at cd2b543 | git ls-remote --heads origin main; git rev-parse HEAD in your own tree /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-20 21:3x by Tuesday
- RD-518 is at 6ea15a0 with a tier-1 gate running in pane %19 | cockpit.sh add output and usage_gate --check, Tuesday's own launch | read 2026-09-20 21:3x by Tuesday
- Kam's words "I would much rather it done properly than quickly" | his panel message, Tuesday tab, 2026-09-20 ~21:2x AEST | read 2026-09-20 by Tuesday
- the zsh :r refspec footgun cost S72 a push tonight and is recorded on RD-464 comment 37879 | S72's wrap mail 10:26:13Z, and the comment id it names | read 2026-09-20 by Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-20 21:25
