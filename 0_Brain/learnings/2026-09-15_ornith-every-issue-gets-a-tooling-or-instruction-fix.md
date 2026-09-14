---
date: 2026-09-15
type: grant
source: Kam, panel 09:28:56 + 09:30:47 (verbatim below)
status: live
tier: W
---

# Every Ornith issue gets a TOOLING or INSTRUCTION fix, the same session — and Wednesday writes the model's task from the ticket, the ticket is never the prompt

**The operative case, so the headline matches it:** an Ornith (local-model) run has FAILED, or a source read has found its output wrong. **Do not file it as a verdict and move on.** Ask which of three things failed — the model's sampling, the harness's tolerance, or the prompt's clarity — and put the fix where that answer points: a sampler option, a checker rule with a red arm, or a clearer Wednesday-written brief. Write the row in `2_Project_Files/local-model/IMPROVEMENTS.md` in the same action. And the model never reads the ticket as its task: Wednesday reads the ticket and the code and writes `night/briefs/<TICKET>.md` — the exact edits by line with the line text, what not to touch, the test cells.

**His words, verbatim (2026-09-15 09:28:56):** *"Is there a way to fix it going red through either instructions or rules or skills? Can you please look into this and on an ongoing basis create a rule so that when you identify an issue with it, we should try to come up with the tooling or instructions to fix it? It looks like a reasonable model to use, so let's find a way to constantly improve it and hopefully after a while of working with it we'll get it to a state where it can perform well in conjunction with all the other agents."*
**And 09:30:47:** *"Maybe rather than getting it to pick up tickets directly, you pick up the ticket and create a prompt based on the ticket for the agent addressing some of the issues and rewording it so that it's clearer. If you have a better approach, use that instead."*

**Why he ruled it, in one line for the successor:** the 08:41 batch went 0/3 and Wednesday's first instinct was to narrow Ornith's contract; his instinct is the opposite — treat every failure as the next improvement, and treat Wednesday as the model's briefer, exactly as she is for the Claude seats.

**How to apply:**
1. **A FAIL row in `night/done.md` is a to-do, not a result.** Read the run (`checker.out`, `out.md`, the file at the tip), classify the cause (model / harness / prompt), fix it where it lives, and write the IMPROVEMENTS row with its proof — same session. The morning brief to Kam carries the rows, not just the verdicts.
2. **Wednesday briefs the model.** Before a ticket is queued, `night/briefs/<TICKET>.md` exists: what is wrong in one paragraph; the exact edits (line number + the line's text at the tip + the new line); what must NOT change; the test cells (red, red, control) and the file to copy the mocking shape from. `build_input.sh` uses it as the prompt when present and says so in the log. A ticket without a brief runs on its description only as a measured baseline, never as the default.
3. **Every prompt rule gets a checker twin.** "Fix every named site" became `defect_line.sites` + the A3b gate; a rule the checker cannot refuse on is a hope. Red-proof the twin on a real failing output before it is trusted (the 09:19 output is the corpus).
4. **Batch, then one pass** (Kam 06:51): the model runs its queue back to back; Wednesday reads every PASS diff in one sitting against the tickets' words and the file, and every FAIL against this rule.
5. **Score the mechanism, not the model** at the weekly consolidation: rows added, arms fired, PASS rate per brief-vs-ticket — the DGM guard (adoption ≠ improvement) applies to Ornith's harness like any other.

**Family:** [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] (the grant this extends) · [[2026-09-14_local-model-pilot-grant-qwen3-30b-simple-checked-tasks-only]] · [[2026-08-07_a-check-that-cannot-fail]] (every rule needs a checker twin with a red arm) · [[2026-08-14_i-read-representations-they-read-sources]] (a FAIL verdict is a representation of a run; read the run) · [[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]] (duty 3: commission what makes the output first-rate — here, the improvement itself) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: recorded).
