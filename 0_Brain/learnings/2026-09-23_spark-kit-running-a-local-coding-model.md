---
date: 2026-09-23
type: principle
source: Wednesday's spark-kit (written 2026-09-23 10:30 for Kam; zip "spark-kit_2026-09-23.zip", sha1 458ca5df18026ffc…), given to Friday by Kam 13:2x with "incorporate this into your learnings"; checked against Friday's own Spark measurements of 12:52
status: live
tier: W
---

# The Spark is FRIDAY'S to run (Kam 2026-09-23) — the BRIEF is the whole cost, the checker must be able to fail, and the counter is original + ONE rebrief then Opus 5.5

**The operative case, so the headline matches it:** Friday is about to send work to the local coding model on the Spark box (HP ZGX Nano, DeepSeek V4 Flash, reached through the 8888 tunnel), or to judge something it returned. **The method is Wednesday's spark-kit, filed whole at `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/spark-kit_2026-09-23/`.** Read `02_FOR_THE_COORDINATOR.md` before the first task of a session. The rules below are the ones that decide outcomes. Where this box differs from the kit, the box wins, and the differences are listed further down.

## The rules (from the kit, adopted)
1. **The run is free; the brief is the cost.** Never queue a task built from a bare ticket description. A builder that fell back to the ticket text has refused, not succeeded. Feeding the model means writing briefs (`03_BRIEF_TEMPLATE.md`, every heading filled, timestamp shell-generated), and that brief-writing can be delegated to a cloud agent.
2. **Selection predicate, verified at source:** one product file · the ticket spells out the fix shape (anything shaped like "decide whether" is a card for a human, not a task) · a runnable in-process test nearby to copy · NOT an auth/token/credential/security surface · not already at the round counter · a test runner the checker can actually run. Expect this predicate to reject most of a backlog; a thin pool is normal.
3. **Brief shape:** exact edits with the line number, the line's CURRENT text and the new text; at most 3 edit points, otherwise split; what must NOT change, named; every premise with the line it was read at; an UNMEASURED section; scope stated as narrowing if it closes less than the ticket.
4. **Checker contract — a pass means nothing unless all six held:** (1) applies at a known commit, with the apply MODE recorded (strict vs recount; never "applies cleanly" when only a recount worked); (2) added lines byte-identical to the brief; (3) touched-file set exactly what the brief named; (4) the new test goes RED on a deliberate break and GREEN when restored; (5) the rest of the suite is no worse, with before/after counts; (6) every assertion's output is kept.
5. **Smoke test before any real ticket:** a trivial known change, then two deliberate breaks (a wrong expected line must fail clause 2; a non-existent line number must fail clause 1). A harness that cannot fail has told me nothing.
6. **Reading the diff against the brief is mine and cannot be delegated.** Hold a PASS in the SAME action as reading the verdict. **A PASS is a candidate, never a merge.** The model holds no identity and raises nothing; merges go through the normal gate and a signed GO.
7. **Round counter (Kam, 2026-09-23): original brief + ONE rebrief, then the ticket goes to Opus 5.5 in the cloud.** Kam's reading of the Spark is roughly 90-something on round one and about 98 on round two, so round two is worth spending and a third is not. It's a counter, not a judgement, so never reason past it. Record why a ticket was reallocated, and batch escalations onto a cloud seat that is already open. (Same shape as Wednesday's 2026-09-16 Ornith counter, [[2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do]].)
8. **Every FAIL gets classified (model / harness / brief) and a fix where it lives**; every prompt rule gets a checker twin that can refuse. Never let it idle: when nothing is briefable, extend the harness or write a brief, and if the queue must be empty, write WHY.
9. The standing disciplines apply unchanged: a zero is a suspect until a control fires; a classification list is not a work order; never delete (quarantine); never edit a running script (write a copy, then `mv`).

## Where THIS box differs from the kit (measured by Friday 2026-09-23 12:52; see `HANDOFF.md` in the same reference folder)
- **Context: `max_model_len` 384,000 tokens (KV pool 449,519)**, not the 65,536 window the kit's failure mode 5 was measured on. Whole-file inputs of ~74K tokens fit. Size is a COST here (prefill ~1,032 tok/s, so ~70 s for a 74K prompt), not a wall. Still carry the region when it is enough.
- **Thinking is ON by default at `effort=max` and eats the completion budget.** Coding tasks run with thinking OFF, as all three of Friday's 12:52 tests did (3/3 pass: instruct→code executed 5/5, multi-turn revision 3/3, tool call). A new failure mode for kit file 04: *an empty or truncated answer = a thinking block that spent the budget, not a model verdict*.
- **`MAX_NUM_SEQS=1`**: one request at a time, and concurrent requests queue. So it's one task in flight; do not fan out.
- **The container is often stopped** (it was down 18 h this morning to free RAM). Restart it with the box's own `run-a2.sh` / RELOAD notes before calling the endpoint broken; the laptop's tunnel does not survive a reboot (PORTABILITY 22).
- **The kit's rules were learned on a 35B model.** Its failure list is a hypothesis for this one. Re-measure in the first week and amend kit file 04 with evidence, not memory.

## Open, and whose it is
- **CLIENT OWNERSHIP OF THE BOX — ask before any Secuura code goes near it.** The Spark's login is `datasec-rd`, and the kit says it was commissioned "so that Datasec work can continue". Friday serves both clients, and sending one client's code to hardware provisioned for the other is the cross-client leak hard rule 2 exists to prevent. **Default until Kam rules: the Spark takes Datasec work only.**
- ~~Which seat runs the loop~~ **RULED — the Spark and the kit are FRIDAY'S.** Kam, terminal 2026-09-23 ~14:1x, verbatim: *"the kit is addressed to tuesday but it should be addressed to you. its yours as you will be using the spark"*. Wherever the kit says "Tuesday" (README, 02, 05), read **Friday**. Claimed in `wed_claim.sh` the same minute, and Tuesday was told directly by mail, so there is no second loop. Kit file 05's setup (place files → inventory the box → checker → smoke test with two deliberate breaks → report to Kam) is Friday's owed work.
- The reference harness (input builders, checkers, queue runner) lives in the Studio's tree and is not shipped. Porting it crosses project trees and is Kam's call.

**Family:** [[2026-09-18_ornith-is-cheap-the-brief-is-the-cost]] · [[2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix]] · [[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]] · [[2026-08-07_a-check-that-cannot-fail]] · [[2026-09-11_red-proof-arms-cover-every-legitimate-shape-of-the-real-event]] · [[2026-09-22_ornith-is-studio-only-not-datasec]] (Ornith is the Studio's; the Spark is a different box and a different model) · [[2026-08-03_role-beyond-code-three-priorities]] (no cross-client leak).
