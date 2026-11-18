---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Local models: running the Studio's own coding model (Ornith) as a checked, briefed, constantly fed worker

**The one idea.** The local model is a permanent, cheap worker that belongs to one seat (Wednesday, on the Studio) and one client's backlog (Secuura). Its run costs nothing; the cost is the brief and the check. So the coordinator's job is to specify its work precisely, check everything it produces, fix every failure where it lives, and keep it fed, without ever letting its output reach a repository except through a Claude seat and the normal gate. The other local box, the Spark, no longer exists.

## The rules

All rules are for the Wednesday seat unless stated.

1. **When about to route, brief or check any work on "the Spark" (all seats):** do not. It was wiped and returned to its lender on 2026-11-15. Every Spark-first, Spark-target or keep-the-Spark-busy line in an older lesson is historical; route the work to the next tier named in `fleet/specs/model-routing.md`. Never run the `local-model/spark/` scripts or name the Spark in a launch receipt. Records from the box are in `0_Brain/reference/2026-11-15_spark-return-archive/`. A new local box needs a new ruling from Kam; the retired checks come back only then. `2026-11-15_the-spark-is-gone-checks-retired-no-local-spark-tier.md`

2. **Tuesday seat. When a boot line, week instruction or shared document says to feed, brief or keep Ornith running:** it does not apply; skip it. Ornith, `night/queue.md`, `local-model/` and the night runner are Wednesday's. More hands for Datasec work means another Claude seat, partitioned by files. `2026-09-22_ornith-is-studio-only-not-datasec.md`

3. **Which model.** The local model is Ornith 1.5 (served by oMLX on port 47780); Ornith 1.0 stays installed as the named fallback, nothing removed. The serving path is armed and checked (scripted start, memory guard while seats are live, doctor check, portability item). Give it harder tasks by a measured ladder (multi-hunk, then multi-file, then looser briefs), recording each rung's pass or fail and its cause. Known defect: it rewrites a bare identifier line among quoted strings as a quoted string; the checker catches it, and any brief carrying such a line names it. One client per task. `2026-10-08_ornith-15-replaces-10-push-it-harder.md`

4. **When and whether it may run.** The original grant (2026-09-14) was night only, 23:00 to 06:00 as the outer bound, and only when no other agent pane, QA gate or drafter is live and the load is under the harness limit; the runner refuses otherwise. The standing rule of 2026-09-18 widens the duty to all hours ("the local agent works constantly on the tickets it can"); the newer rule wins on hours (`2026-09-18_ornith-works-constantly-standing-rule.md` over `2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md`). Neither lesson says the pane, load and memory gates were lifted, so read the runner before assuming they were. Before each task: unload every other model and measure free memory; if the headroom is not there, skip. A full page-cache purge needs an admin password the seat does not hold; say so, never work around it. `2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md`, `2026-09-18_ornith-works-constantly-standing-rule.md`

5. **Checked, never pushed.** Every run ends at the checker's verdict plus a source read by an agent. A PASS becomes a pull request only through a Secuura Claude seat under the normal gate; a FAIL is evidence. The model holds no board identity. Kam sees the verdict and the read, never a raw diff, and the morning brief leads with what the night produced. `2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md`

6. **What goes in the queue.** One checked ticket at a time from a prepared queue file, re-derived from the board at source (a ticket may have been closed, archived or taken by a live lane during the day). Never a ticket a live lane owns or one assigned to the client's own people. The queue is the whole Backlog/Todo, ordered easy to hard: one-file patches and test-only pins first, then tooling, then service suites, then multi-file, with authentication and security surfaces last, taken only once the model's record on easier tiers earns them. The newer lesson states that the original "no auth surfaces" is an order, not a permanent exclusion (`2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry.md` over `2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md`). State the tier in each brief header. Rank candidates by how directly a test cell can reach the defect: a pure function, helper or single handler called directly is good; a red that only appears after a request crosses the whole middleware stack is poor however good the brief. `2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`

7. **Before queueing any input:** a coordinator-written brief `night/briefs/<ticket>.md` must exist. The ticket is never the prompt. The brief carries what is wrong, the exact edits by line with the current line text, what must not change, the mode, and the test cells (red, red, control) with the file to copy the mocking shape from. If the input builder reports "prompt source: the ticket description", treat that as a refusal. Feeding the model is brief-writing, not queue-filling; a few good briefs beat a full queue of brief-less ones. Brief-writing may be delegated to a subagent. `2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix.md`, `2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`

8. **When a run fails or a source read finds its output wrong:** it is a to-do, not a verdict. Read the run, classify the cause (model sampling, harness tolerance, or prompt clarity), fix it where it lives, and add a row with its proof to `2_Project_Files/local-model/IMPROVEMENTS.md` the same session. Every prompt rule gets a checker twin with a red proof; a rule the checker cannot refuse on is a hope. A failure of the red-first check is a brief defect until proven otherwise. A red control at the untouched tip means the harness never reached the code: a reachability problem, never "the model could not do it". Score the mechanism, not the model, at weekly consolidation. `2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix.md`, `2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`

9. **The retry counter.** Original brief plus one rebrief; then the ticket goes to a Claude seat. Never a third queueing, and never spend the rebrief re-running a brief-less input. `2026-10-08_ornith-15-replaces-10-push-it-harder.md`, `2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`

10. **When the queue is empty:** never write "pool exhausted" and stand down. The pool is not exhausted while the board has open tickets; what is exhausted is the harness's reach. Extend the checker (a new runner, file class or mode) or write the next brief within the hour. "Do not manufacture tickets" stands; "do not extend the instrument" was never the rule. The gatekeeper checks, fixes, lines up what passes and rejects what does not. A seat may end its turn only with the model running or a batch queued. `2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry.md`

11. **When the next candidates look decision-shaped or too big:** that is a verdict on one ticket after reading it, never on a tier. Card the blocked one with a default, say so in one line, and take the next, down the whole list. Brief the card's default now as a held diff (reversible, merged only after QA) and let Kam's tap redirect. "Exhausted" is a claim with a count in it. Harness work substitutes for briefs only when the pool is truly empty, not merely inconvenient. `2026-09-16_if-something-blocks-move-on-to-the-next.md`

12. **At boot and at every checkpoint:** check the model's queue before choosing my own next task, and keep a scoped, ready next job in the pickup so a refill takes minutes. The qualifier "tickets it can" is load-bearing: decision-class, infeasible-in-harness and counter-spent are valid reasons not to feed it. An empty queue is acceptable only with a written, measured reason where the next reader lands (the why-line in `night/queue.md`), accepted by Kam on 2026-09-25; re-screen whenever the pool changes; silence the idle alarm with the pause file plus the reason, never by ignoring it. `2026-09-18_ornith-works-constantly-standing-rule.md`

13. **When the model is idle for a recorded reason:** do not report or apologise to Kam about it; keep the why-line current. This is the newest word and it wins over the earlier "idle over about ten minutes in daytime is a failure to report" (`2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis.md` and the 2026-09-25 extension over `2026-09-16_if-something-blocks-move-on-to-the-next.md`). What still holds from the earlier lesson: idleness with no recorded reason is a failure, and every hold leads to the next brief in the same action. `2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis.md`

14. **Choosing the worker model:** it is the coordinator's choice, made per `fleet/specs/model-routing.md`, recorded there with its measurements, and told to Kam in one line as a receipt, not a request. `2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis.md`

## What a tool already enforces

No member of this family has an enforcing tool recorded in the index. The lessons describe a night runner with pane, load and memory gates, a checker, and doctor checks; treat those as descriptions to verify at the script, not as guarantees.

## Grants and their limits

- **Kam, 2026-09-14, standing:** Ornith may work the prepared Secuura queue. Limits: checked and source-read, never pushed; no board identity; a PASS reaches the repository only via a Claude seat under the gate.
- **Kam, 2026-09-18, standing (no expiry):** the local agent works constantly on the tickets it can.
- **Kam, 2026-10-08:** Ornith 1.5 replaces 1.0 and is pushed to harder tasks. Kam overruled the coordinator's recommendation to stay on 1.0; the ruling is executed fully.
- **Kam, 2026-10-09:** model choice is the coordinator's; no report or apology owed for Ornith's idle time.
- **Stays Kam's:** merges and deploys outside existing grants, anything in the signature classes, a new local machine, and the admin-password memory purge.

## The mistakes this family keeps catching

- An empty queue described as a state ("pool exhausted") instead of treated as the next piece of work.
- A whole tier written off as "needs a decision" from titles, when the next ticket read was mechanical.
- A queue filled fast from bare ticket text, returning failures that look like model weakness and are brief defects.
- A failure filed as a verdict on the model, with no fix to harness or brief and no improvements row.
- A rule for one seat's local model reaching another seat through shared boot text and being obeyed.
- An old line about a machine that has gone still being acted on.

## Members

- `2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md` — Ornith works the prepared Secuura ticket queue at night only when no other agent pane, gate or drafter runs; unload other models first, check memory. Output is checked then source-read, never pushed; a PASS becomes a PR only via a seat under the gate.
- `2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry.md` — When Ornith's queue is empty: never write 'pool exhausted' and stand down. Extend the checker or write the next brief within the hour; queue is the whole Backlog/Todo, easy to hard, auth last; gatekeeper checks, fixes, lines up, rejects.
- `2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix.md` — When an Ornith run fails or its output is wrong: classify cause (sampling, harness, prompt), fix it there, add a local-model/IMPROVEMENTS.md row in the same session. Wednesday writes night/briefs/<ticket>.md; the ticket is never the prompt.
- `2026-09-16_if-something-blocks-move-on-to-the-next.md` — When the next candidates look decision-shaped or big: judge each ticket after reading it, never a tier. Card the blocked one with a default, brief the default as a held diff, take the next; Ornith idle over ~10 min in daytime is a failure.
- `2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md` — Before queueing an Ornith input: a night/briefs/<ticket>.md must exist; never queue one whose build says 'prompt source: ticket description'. A FAIL on A4 RED-FIRST is a brief defect first; pick tickets whose defect a test cell reaches directly.
- `2026-09-18_ornith-works-constantly-standing-rule.md` — At boot and every checkpoint: check Ornith's queue before choosing my own task; keep a scoped next job in the pickup. Empty queue only for a written measured reason where the next reader lands (accepted by Kam); re-screen when the pool changes.
- `2026-09-22_ornith-is-studio-only-not-datasec.md` — Tuesday seat: a boot or week-instruction line saying to feed or keep Ornith running does not apply; skip it. Ornith, night/queue.md and the night runner are Wednesday's. More Datasec hands means another Claude seat, partitioned by files.
- `2026-10-08_ornith-15-replaces-10-push-it-harder.md` — Ornith 1.5 (oMLX, port 47780) is the local model; 1.0 stays as fallback. Give it harder tasks by a measured ladder, one rebrief then a Claude seat, and name its known quote-rewrite defect in briefs. The Spark half is dead.
- `2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis.md` — Do not report or apologise to Kam about Ornith idling; keep the measured why-line in night/queue.md. Choose the model per fleet/specs/model-routing.md and tell Kam in one line as a receipt. Spark-first clause is dead.
- `2026-11-15_the-spark-is-gone-checks-retired-no-local-spark-tier.md` — Never route work to the Spark, check its tunnel, or brief it in a receipt: it was wiped and returned to HP 2026-11-15. Spark lines in older lessons are historical; route to the next tier in model-routing.md. A new box needs a new ruling.
