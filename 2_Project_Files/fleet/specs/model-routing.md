# Model routing -- v1.0 (2026-10-18) -- IN FORCE: Kam approved all seven recommendations, live board 2026-10-18 20:55:59 (card wed-model-routing-v10-approve-1018 = a, "Approve all seven recommendations")

Drafted 2026-10-18 for Kam's request (terminal, ~19:0x AEDT, verbatim): *"new account so please work on the tickets, backlog and definition of which agent to use for what. Spark connected so give it as many tickets as it can handle"* (`0_Brain/learnings/2026-10-18_new-account-tickets-backlog-routing-definition-spark-max.md`).
Replaces v0.1 (2026-10-11) on approval. v0.1's sections 0, 2 and 3 (model IDs, launch receipt, switching a seat) carry over unchanged in substance and are restated short in section 1 and 8.
One definition for every coordinator seat (Wednesday, Tuesday, Friday). Sections 1-8 carry no client code. **The evidence appendix (it names one client's tickets) lives in Wednesday's brain, not here: 0_Brain/reference/2026-10-18_model-routing/EVIDENCE.md. This file carries no client code and may be read by every coordinator seat.**

**Evidence tags used on every rule line:**
- **RULED** = Kam's words, quoted with date and the lesson file that holds them.
- **MEASURED n=...** = counted for this draft from the named file, method in section 9.
- **single instance, pilot** = one data point. Not a rule yet.
- **unmeasured** = no data in the files read. Reasoning only.
- A rule is promoted from pilot only at >= 5 rows of its kind (v0.1 section 6 rule, carried).

---

## 0. Status of the boot-prompt override (read first)

`Launch_Wednesday.command:763` says: *"Current override: Opus 5.5 for every agent until the model review."*
- That line comes from Kam, terminal, 2026-10-09 ~09:4x (verbatim, in `0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md`): *"all sub agents are starting as opus 5. if you use opus for sub agents (after the next model review phase this should be a deliberate choice) use the best version of opus. for now, use Opus 5.5 for all sub agnets"*.
- Three later rulings narrowed it. Kam has not lifted it in words:
  1. 2026-10-09 23:12:40, live board: *"keep pushing harder and harder tickets to the spark as a way of testing it. Also use Sonnet 5.5 as part of the workflow to determine its limits and a good way of judging when to use Opus, Sonnet or local LLM"* (`2026-10-08_sonnet-trials-and-a-shared-model-routing-definition.md`, EXTENSION).
  2. 2026-10-10 09:04:22, live board: *"Keep going today, using mainly the Spark and Sonnet. Put them both to actual tasks, but to make sure that nothing problematic gets through, double check everything i'm still experimenting."* Expired end of 2026-10-10 (`2026-10-10_today-mainly-spark-and-sonnet-double-check-everything.md`).
  3. 2026-10-11 12:56, live board: *"new account logged in. Work mainly on tickets with the spark and Sonnet. Priority for now is to refine a structure that identifies where to use Opus, Sonnet, Spark and Ornith. Do this on live tickets and work through the secuura tickets as you do"* (source: `0_Brain/daily/2026-10-11.md:44`; **not in a lesson file**, a gap).
- The choice between the models after the Sonnet analysis is Wednesday's: Kam, 2026-10-09 13:55:34, *"once we finish the analysis of Sonnet, you can decide between the three models available"* (`2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis.md`).

**How v1.0 treats the override:** this document IS the model review's output. It does not lift the override. Lifting it is Kam's call (SUMMARY decision 1).
- **On approval:** the boot line is replaced with "route by `fleet/specs/model-routing.md` v1.0". Every Opus use then needs a table row that names Opus, recorded on the launch receipt (Kam 10-09: *"after the next model review phase this should be a deliberate choice"*).
- **Until approval:** v0.1 section 7 keeps running, as it has since 2026-10-11, and the boot line stays as written.

---

## 1. Model IDs: read them, never type them (RULED, Kam 2026-10-09)

*"Check what the latest claude models are at the different levels ... you make a deliberate decision of whether to use Opus, Sonnet or either local model."* (v0.1 section 0.)
- Read IDs from `0_Brain/dashboard/data/models_latest.json`. At this draft, `checked_at_local` = 2026-10-18 15:52:05 +1100 and `warnings` = []. It names opus, sonnet, haiku and fable. The newest at each level is the one to use.
- **Opus 4.8 is NOT in `models_latest.json`.** The JSON lists only the newest per level. A gate reaches Opus 4.8 only through Claude Code's own safeguard dialog, then `/model` in that pane (section 4, row G1). Do not type a 4.8 ID. Recording it in the JSON is an owed tooling item (unmeasured).
- **Stale launcher pins:** `stale_pins` lists 13 launcher pins that are older than the newest at their level. Two of them are Opus pins on the Secuura Blockchain launcher. A seat started from one of those runs on the pinned model until `/model <id>` is sent to it (v0.1 section 3, MEASURED in the JSON).
- Local models: **Ornith 1.5** = `Ornith-1.5-35B-A3B-MLX-8bit` on oMLX at the Studio, night default since Kam's 2026-10-08 18:12:53 ruling (`2026-10-08_ornith-15-replaces-10-push-it-harder.md`, `local-model/README.md:177`). Ornith 1.0 (`ornith:35b`, Ollama) is the named fallback. **The Spark** = `deepseek-v4-flash-0731` (`local-model/SPARK_LADDER.md` instruments line). It runs one request at a time (`MAX_NUM_SEQS=1`, 10-18 lesson).
- Haiku 5.5 and Fable 5.1 are not worker tiers. No row routes to them (unmeasured). **Fable 5.1 is a level ABOVE Opus in `models_latest.json` and has never been trialled here: put to Kam as decision 7 (Wednesday's review addition, 2026-10-18), recommendation a trial on one tier-1 gate and one coordinator task before any rule.**

---

## 2. The four checks before the table (in this order; the first that fires decides)

| # | Check | If YES | Basis |
|---|---|---|---|
| P1 | Is the action in Kam's signature class: production, money, external communication to a human outside the team, an irreversible action, or authority that would originate with the coordinator? | **A card for Kam, no worker.** A worker may draft; nothing is sent or run. | RULED, protocol v1.3 (`2026-08-07_protocol-v1.3-signed-delegation.md`: "His signature only — and he wrote that I cannot waive these") |
| P2 | Weekly gauge >= 90% (`fleet/usage_gate.sh` rc 3)? | **No Claude launch of any kind, no drafters.** Wednesday plus the local models only. | RULED, 2026-09-14 hard stop, restated unchanged in `2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark.md` |
| P3 | Weekly gauge 80-90%? | Use the table, but a cloud launch only for raise / gate / merge of work already done, or a local counter already spent. The receipt carries `cloud (80-90% band): <why not Spark/Wednesday>`. Brief drafting is Wednesday's own work. | RULED, Kam 2026-10-14 ~06:47: *"going forward once we reach 80 - 90% should be the start of limited cloud model usage and a focus on you and the spark"* (same file) |
| P4 | Is the task Datasec work, or any client other than the one the local tier is cleared for? | **No local tier.** Use the Claude columns only. | RULED for Secuura only, Kam 2026-09-25 11:45: *"yes, Secuura code can go to the Spark"* (`2026-09-25_three-tier-routing-ornith-spark-cloud-always-on.md` rule 5). Datasec on the Spark: not ruled. Ornith "is the Studio's and is not Datasec's" (10-08 lesson rule 5). One client per local task, always. |

Below 80%, with P1-P4 all NO, the table below applies as written. Basis: RULED, 10-14 lesson ("Below 80%: the normal routing").

---

## 3. The local-model predicate (a brief is LOCAL-ELIGIBLE only if every line holds)

Each line is a refusal the harness already makes, or a measured failure. A coordinator checks each one; none is a judgement call.
1. **Spelled out.** The brief gives the exact `-` / `+` lines. Rungs 1-3 qualify. Rung 4 (fix shape only) and rung 6 (prose) are pilot rungs (section 4 rows L4, L5). Evidence: section 9, tables A and B.
2. **Runnable in-process.** The checker can run the test with no real PostgreSQL, no docker rebuild and no browser. MEASURED refusals: needs real Postgres (two tickets, `spark/queue.md:38,42`); needs a docker rebuild (one ticket, `queue.md:30`).
3. **A tier exists for the shape.** The Spark (`spark/round.sh`) runs code_patch, code_patch2, bash_patch and bash_patch2. **test_only is not wired there** (`spark/brief_lint.py:18`; wiring claimed 2026-10-18 in commit `4e623043d`, unmeasured until its arms pass). Ornith's night runner (`night/night_run.sh`) runs code_patch, bash_patch, doc_patch and test_only. It has **no multi-file tier** (grep for code_patch2 or bash_patch2 in `night_run.sh` returns 0).
4. **Not a frontend product.** The builder refuses these (v0.1 section 6, 10-12 row: two tickets).
5. **No decision inside it.** There is no owner question and no ruling owed. Kam's ruling is quoted in the brief where one applies.
6. **The coordinator ran the dry run.** `round.sh <dir> --dry-run` rc 0 and `--control` CONTROL-PASS with the golden byte- or tree-identical. Do not queue a brief whose header says it is not runnable. MEASURED: one wasted round on 2026-10-05 (`IMPROVEMENTS.md`, 10-05 11:4x row).
7. **No held PASS for the same item already exists** (grep `night/READY_<ticket>`). MEASURED: one duplicate brief written (`IMPROVEMENTS.md`, 10-10 01:0x row). The refusal tool is owed.

**Auth and security files (proposal; SUMMARY decision 4).** The design decision on an auth, credential, security or money surface never goes local. A fully spelled-out mechanical edit inside such a file MAY go to the Spark. Its PR is then **always a tier-1 Opus gate**. MEASURED basis: 9 Spark rounds on 8 items in security or auth service files. 7 items PASSed on round 1; the eighth (an auth test file) PASSed on its one rebrief (`SPARK_LADDER.md` rows 15, 18, 24, 31, 32, 35, 38, 40; `spark/done.md` 2026-10-12 16:30:13). What their gates found downstream is **unmeasured** in this draft. v0.1 section 1 excluded these surfaces outright. Practice has not matched v0.1, so the rule is written to match the practice and is put to Kam.

---

## 4. THE DECISION TABLE

Key: **1st** = default worker · **2nd** = takes it when the 1st is busy (defined in the row) · **gate** = the independent check after delivery · **esc** = where it goes when the counter is spent · **no** = never routed here · — = not applicable.
Columns: **O15** = Ornith 1.5 (Studio) · **SPK** = the Spark (DeepSeek V4 Flash) · **S55** = Claude Sonnet 5.5 · **O55** = Claude Opus 5.5 · **O48** = Opus 4.8, only for a gate flagged by 5.5's safeguards.

### 4a. Local-eligible work (section 3 predicate holds)

| Row | Task class | O15 | SPK | S55 | O55 | O48 | Evidence basis | Counter / escalation |
|---|---|---|---|---|---|---|---|---|
| L1 | **One-file, one-hunk, spelled-out fix** (rung 1) | **2nd**: when the Spark queue already holds a waiting brief | **1st** | esc (build seat); raises the PASS | tier-1 gate if the file is auth/security (section 3) | — | Spark: rung 1 **13/13** first-round PASS in the ladder (MEASURED n=13, `SPARK_LADDER.md`), plus the queue era below. Ornith 1.0: **112/172** items PASS on round 1, **138/172** within two rounds (MEASURED, `night/done.md`, method in section 9). Ornith 1.5: **1 real ticket, PASS** (single instance, pilot) plus an A/B of **17/20, the same as 1.0** (`0_Brain/reference/2026-10-08_omlx-flash-next/ORNITH15_AB.md`). Spark-first: RULED, Kam 2026-10-09 13:55:34 *"It's now up to you to use the Spark as much as possible"*. Ornith for "the simplest": RULED 09-25, re-ranked here by measurement (SUMMARY decision 6). | Original + ONE rebrief, then a Claude seat (RULED, Kam 2026-09-16 07:57:59Z: *"Rebriefing once is ok and might generate positive results. Doing it more would be a waste with diminishing results."*). Reallocate *"not urgently but when it makes sense"* (RULED 09-16). What counts as a round: section 5. |
| L2 | **One file, multi-hunk, spelled out** (rung 2) | 2nd, as L1 (single instance, pilot: the one 1.5 ticket was rung 2) | **1st** | esc; raises | gate as L1 | — | Spark rung 2: **19/19** round-1 PASS in the ladder (MEASURED n=19). Queue era: 9 rung-2 items labelled in `queue.md` or v0.1 section 6, all PASS; one PASSed only after a format FAIL (section 9, table B). | as L1 |
| L3 | **Two- or three-file fix, spelled out** (rung 3: code_patch2 / bash_patch2) | **no** (no multi-file tier in `night_run.sh`) | **1st** | esc; raises | gate as L1 | — | Spark rung 3: **16/16** PASS in the ladder (2 of them PASS on re-check after harness faults). Queue era: 4 rung-3 items, 3 PASS. The fourth failed twice on one inserted byte (cause: model) and went to Claude. MEASURED n=20 items. | as L1 |
| L4 | **Looser brief: fix shape, cell names and data, NOT the lines** (rung 4) | no (unmeasured on 1.5) | **1st, pilot** | esc; raises | gate as L1 | — | **7 tickets: 5 PASS on round 1, 1 on its rebrief, 1 counter spent and sent to Opus** (MEASURED n=7: ladder rows 2-3, 13, 15/18, 19; queue era 3). The model's typical miss is hunk-header arithmetic and not copying the `-` line (`SPARK_LADDER.md` "What the rows say"). Above 5 rows, but 2 of the 7 needed help, so it stays pilot. | as L1 |
| L5 | **Ticket in prose only** (rung 6) | no | **pilot only** | esc | gate as L1 | — | **1 PASS** (single instance, pilot; the queue era rung-6 row). The bash builder refuses prose briefs (`queue.md:21`). | as L1 |
| L6 | **Test-only pin** (new or extended cells, product untouched) | **1st today** via the night runner's test_only tier (Ornith 1.0 history; **1.5 on test_only: unmeasured**) | **1st once** the test_only wiring passes its arms (claim `4e623043d`, 10-18). Before that: refused by `brief_lint.py` | **1st fallback**: a Sonnet raise seat applies the ready golden | — | — | Spark test-only: **1 PASS** through the night path (single instance, pilot; ladder row 21). A held golden is waiting for a raise seat (`queue.md:42`). | as L1. A ready golden is not a local round: it is raise work (row C1). |

### 4b. Claude work

| Row | Task class | O15 | SPK | S55 | O55 | O48 | Evidence basis | Counter / escalation |
|---|---|---|---|---|---|---|---|---|
| C1 | **Raise a held local PASS as a PR** (apply, run the package lint and a tsc that includes test files, push, write the PR text) | no | no (local workers never merge or push, RULED 09-25 rule 2) | **1st** | esc | — | **8 Sonnet raise-seat rows**, scores 0.94-0.97, mean 0.956 (MEASURED n=8, `scoreboard.md`). One Major got past a Sonnet raise seat (a wrong surface count); the Opus gate caught it (v0.1 section 6). One cost defect in a local PASS (38 MB x 25 images) was caught BY the Sonnet raise seat. The lint and test-tsc duty is MEASURED: 3 raise rounds were lost to it (`IMPROVEMENTS.md` 09-26 18:59, 23:32; 09-27 19:43). | Gate NO GO: one fix round on the same seat model. Two NO GO on one class: the two-NO-GO cap (row G-cap). Two measured failures by Sonnet on one item: Opus (v0.1 section 7 Q4). |
| C2 | **Multi-file build or feature that fails the local predicate, not decision-shaped, not auth-design and not a destroying path** | no | no | **1st** (RULED, Kam 2026-10-10 09:06:47: *"also get Sonnet to do some of the harder tasks that you would not give to the spark. You ( an opus agent you spin up - your choice) acts as the gate keeper"*) | gate (tier 1 or 2 per G rows) | — | **1 build-only row (0.98)** plus **10 mixed build/raise/merge lane rows**, 0.93-0.96, mean 0.946 (MEASURED n=11, `scoreboard.md` 10-12 and 10-13 rows). Lane seats are not split by task kind, so builds alone are below 5 rows: **pilot**. | as C1 |
| C3 | **Build on an auth, credential, security or money DESIGN surface** (the decision, not a spelled-out edit) | no | no | **no** (proposal; SUMMARY decision 3) | **1st** | — | Sonnet on such surfaces: **1 auth front-door PR, clean** at an Opus gate (single instance, pilot). Opus gates found real Majors on 3 Sonnet-built PRs on hook, wallet and front-door surfaces on 10-12 (v0.1 section 6). Opus builders also take NO GO rounds (one Opus build row with a Major on round 1). So whether Opus builds better here is **unmeasured**. The rule rests on RULED caution: 2026-10-09 23:12 extension, *"Security surfaces, deploys and QA gates stay on Opus until the trial has evidence"* (Wednesday's receipted reading, not Kam's words). | Gate cap as G-cap. A third round needs Kam's word. |
| C4 | **Data-destroying path** (erasure, delete, migrations that drop or blank, tenant operations) | no | no | **no** (proposal; SUMMARY decision 3) | **1st**, read-only measurement first; the irreversible step itself is P1 (Kam) | — | Sonnet built one destroying-path PR across rounds 4 and 5. An Opus gate went NO GO twice: once on a real cross-organisation blanking Major, once on a coordinator ruling (single instance, pilot; `scoreboard.md` 10-12 and 10-13 rows). The 09-05 cap was priced on an 8-round erasure class that Opus built (`2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`). Opus versus Sonnet here: **unmeasured**. | G-cap. Every irreversible step: P1. |
| C5 | **Merge on a GO** (port the tools, merge-in, squash; the coordinator verifies the squash at source) | no | no | **1st** | esc | — | **12 Sonnet merge-seat rows**, 0.95-0.97, mean 0.958. **0 Majors reached develop** (MEASURED n=12, `scoreboard.md`; v0.1 section 6). Merge authority is Wednesday's under v1.3 (RULED, 08-07). | A refused or failed merge goes back to the gate. No second merge attempt on the same head without a new GO. |
| C6 | **Deploy** (dev, staging, test or demo, in the order Kam's October grant sets: kintsugi first, then demo) | no | no | no (unmeasured) | **1st** | — | **2 Opus 5.5 deploy-seat rows, 0.96 each, 0 rollbacks** (MEASURED n=2, `scoreboard.md` 10-12 and 10-13). Opus: RULED caution (as C3). **Production is P1** (Kam's signature). | A failed deploy is fixed at the root and re-verified (workspace hard rule 7). Any rollback: Kam is told. |
| C7 | **Client-facing ticket comment** (on a client's board) | no | no | **drafts 1st**; posts only a body the coordinator has approved byte for byte | drafts if the comment explains a security finding | — | 1 Opus seat posted 1 comment byte-identical to an approved body (single instance, pilot). 3 Sonnet lane rows posted verify-and-close comments with their facts (MEASURED n=3, `scoreboard.md` 10-13 rows). Error rate: **unmeasured**. A message to a human outside the team is **P1** (RULED v1.3). | A wrong comment is corrected by a new comment, never by deleting the old one (deletion is irreversible: P1). |
| C8 | **Brief drafting, board screens, gate kits, tooling with arms** (Agent-tool sub-agent) | no | no | **1st** (`model: sonnet` on the Agent call) | only if the brief is for a C3 or C4 build | — | **8 Sonnet drafter or tooling jobs**: 4 v0.1 rows, 2 queued briefs that both PASSed round 1, and 2 harness fixes with arms (MEASURED n=8: v0.1 section 6; `queue.md:25-26`; `IMPROVEMENTS.md` 10-10 02:5x rows). 1 defect, attributed to the coordinator's GO, not the draft. 10-18 reading: *"brief drafters (Agent tool, Sonnet first) are allowed again on this account"* (Wednesday's receipted reading of Kam's 10-18 words). At 80-90%: Wednesday drafts (P3). | The coordinator reads every golden at source before queueing (rule 6 of section 3). A drafter's defect is fixed by the coordinator; there is no second drafter. |
| C9 | **Coordination** (Wednesday, Tuesday, Friday seats) | no | no | no | **1st** (the coordinator seat keeps its own model, newest Opus) | — | RULED, 2026-10-09 ~09:3x reading item 4: *"This seat (the coordinator) is not a worker and keeps its own model"* (Wednesday's receipted reading, `2026-10-09_spark-ornith-sonnet-only-until-monday.md`). Opus versus Sonnet as coordinator: **unmeasured**. | — |
| C10 | **A decision for Kam** (a ruling, money, comms, scope) | — | — | — | — | — | RULED v1.3, and v0.1 section 7 Q5. | A card, no worker (P1). |

### 4c. QA gates (tier by what the change touches, RULED 2026-09-05)

The tier comes from Kam's 2026-09-05 20:19 ruling, *"Let's go ahead with your recommendation."* (`2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`). The model in each row is v1.0's proposal.

| Row | Gate | O15 | SPK | S55 | O55 | O48 | Evidence basis | Counter / escalation |
|---|---|---|---|---|---|---|---|---|
| G1 | **Tier 1**: security surfaces, data destruction, anything deploying, anything handed to a client tester | no | no | **no** | **1st** | **only if** the session is stopped by 5.5's safeguards: switch THAT session (never "Switch automatically") | Opus 5.5 gates 82-86 scored 0.95-0.97 (MEASURED n=5, `scoreboard.md`). Opus gates caught real Majors on 5 PRs that Sonnet seats had built or raised (v0.1 section 6; `scoreboard.md`). Opus 4.8: RULED, Kam 2026-09-30 09:07:30 (`2026-09-30_qa-gates-may-switch-to-opus48-when-flagged.md`): *"Decision nexusai-gate11-opus55-safeguard-model-switch: b — Let QA gates switch to Opus 4.8 when flagged"*. 4 gate rows used it; 1 is scored, 0.97 (MEASURED n=4, all on one client's gates). | The cap (G-cap). |
| G2 | **Tier 2**: tests-only, spec-only, docs, config/CI, tooling, and follow-ups whose mechanism a prior gate already measured | no | no | **1st** (proposal; SUMMARY decision 2) | 1st if the follow-up's mechanism sits on a G1 surface | no | **11 Sonnet-tier gates on 10-12**, 1 first-pass NO GO, 1 real Major found and verified at source (MEASURED n=11, v0.1 section 6, 10-12 rows). Whether a Sonnet gate MISSED anything: **unmeasured** (no second gate re-checked them). Opus has gated tier 2 until now (10-08 reading). | The cap (G-cap). A Sonnet G2 that finds a security-shaped issue hands the PR to G1. |
| G3 | **Tier 3**: backlog or citation fixes, ticket hygiene, comment corrections | — | — | — | — | — | No gate: the builder's own red-proof plus Wednesday's completion check (RULED 09-05). | — |
| G-cap | **Two NO GO rounds on one class: STOP.** Ship the closed instances, ticket the residue with the tester's cells attached. A third round needs Kam's word on a card. | | | | | | RULED 2026-09-05 (same file). | — |

---

## 5. What counts as a round for the local counter (proposal; SUMMARY decision 5)

Kam's rule is a counter, not a judgement: *"His rule is a COUNTER; mine was a judgement call"* (`2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do.md`). The open question is what one round is. That lesson put Wednesday's reading to Kam (a brief defect keeps the ticket local); the file records no answer since. Practice has since treated brief and harness faults as "counter not spent" (`IMPROVEMENTS.md` 09-21 rows, 10-05 13:4x row).

**v1.0 proposal (countable):**
- **A round counts** when the model produced an output AND the checker judged that output. This holds whatever the cause of a FAIL: model, brief or format.
- **A round does not count** in three cases. Each is recorded on its row as "harness, not a round".
  1. The builder refused before the model ran, or the verdict was lost.
  2. The model's output is shown correct by a byte or tree compare: tree-identical to the golden, or a PASS on re-check of the SAME output under a fixed checker.
  3. A re-run of the SAME brief on a flaky checker, where the earlier output was tree-identical.
- Basis: MEASURED in the queue era. 7 of 63 items needed more than one run. Under the proposal, 3 of them spent a round (one twice); under current practice, 1 did. Section 9, table B.

---

## 6. Launch receipt (v0.1 section 2, carried)

Every launch states one line: `model: <id from models_latest.json> -- <row id from section 4> -- <check P1-P4 result> -- <gauge %>`.
A receipt with no model line, an ID not in the JSON, or no row id is incomplete. A row marked **pilot** is named "pilot" on the receipt.

## 7. Switching a seat (v0.1 section 3, carried)

Project launchers pin their own model, and a coordinator does not edit them. Send `/model <id>` into the pane right after launch, confirm the pane reports it, and tell the seat by mail. A fixed pin is a request to that project's own agent.
**Confound carried from v0.1:** every Sonnet seat in the evidence ran ITEM 0 and its plan on Opus 5 before the switch. Switch before ITEM 0 where the pane allows it.

## 8. Open items (each unmeasured)

1. Usage per seat-hour by model. Kam's "8x" for Sonnet is his estimate (10-08 lesson item 4). No measurement exists in the files read.
2. Wall-clock and context cost per task by model (v0.1 section 6: unmeasured).
3. Ornith 1.5 on test_only, and on rungs 3-6. One real ticket so far.
4. Downstream gate findings on Spark rounds in auth and security files (section 3).
5. Sonnet as coordinator, as deploy seat, or as tier-1 gate: no rows.
6. Datasec rows: every Sonnet row above is one client's work. Tuesday's seats have no Sonnet trial rows.
7. The 10-11 12:56 ruling lives only in a daily note. Owed: a lesson file.

---
