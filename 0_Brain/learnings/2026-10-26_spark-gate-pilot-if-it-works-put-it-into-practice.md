---
date: 2026-10-26
type: grant
source: "Kam, Wednesday's terminal (laptop), 2026-10-26 ~09:2x AEDT, verbatim: 'launch another agent once the load drops.  also, most of the usage per week is eaten up by the tests.  Is it possible to do all validation, review and test by the local LLM (Spark).  if so, it might need better instruction or clearer tooling.  if this works, please put it into practice'"
status: live
tier: W
---

# Grant (conditional): move QA validation, review and test to the Spark wherever the measurement shows it works — tooling and instructions first, tier by tier, never on a guess

**The operative case, so the headline matches it:** Wednesday is about to commission a QA gate. **Ask whether a measured Spark gate covers that tier yet.** If it does, run the Spark gate (the deterministic runner plus the Spark review) and keep the Claude gate only where the calibration says the Spark misses things. If it does not, the Claude gate runs as today and the Spark gate runs beside it as a SHADOW, adding a calibration row.

**Wednesday's reading, said back to Kam:** the gate has two halves. (1) MECHANICAL validation (fetch the head, red/green on base vs head, suite counts, lint, planted violations): that needs no model at all, so it becomes a script. (2) REVIEW judgement (is the change bounded, are the client-facing sentences true, does it meet the ticket): that is the Spark's job, with a fixed checklist and a strict output schema. The Spark had never been measured on review on 2026-10-26; its record was spelled-out edits (5/5 round-1 PASS that day).

**How to apply:**
1. **Measure before moving.** The first calibration is PR #1687 (KS-1719) at both rounds, against the two Sonnet verdicts in `0_Brain/reference/2026-10-26_gate-pr1687-ks1719/`. Score recall of the known findings, false positives checked at source, verdict match, and whether the facts match.
2. **Promote one tier at a time, on evidence:** tier 3 (hygiene) and tier 2 (tests, docs, config, already-gated follow-ups) first. Tier 1 (security surfaces, data destruction, deploys, client handovers) keeps the Opus gate until the Spark has a record on that tier: Kam-approved routing v1.0 says tier 1 = Opus, and this grant moves it only "if this works".
3. **Shadow first:** until a tier is promoted, every Claude gate on that tier gets a Spark shadow run, so the record grows from real work.
4. **Report the numbers to Kam** when a tier is promoted, as a receipt with the calibration table, not as a request.
5. Unchanged: the QA gate before every merge; Wednesday's completion check; the signature classes.

**Mechanism:** `2_Project_Files/local-model/gate/` (spark_gate.sh, spark_review.py, REVIEW_CHECKLIST.md), built by a Sonnet tooling drafter on 2026-10-26 with arms, and calibrated on PR #1687.

**Family:** [[2026-09-05_qa-gate-tiers-and-the-two-nogo-cap]] · [[2026-10-18_model-routing-v10-approved-route-by-the-table]] · [[2026-09-25_spark-calibrate-like-ornith-start-high-oversight]] · [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 4: pilot, measure, review; rule 5: every grant recorded).

## CALIBRATION 1, 2026-10-26 ~09:4x — PR #1687 rounds 1 and 2 against the two Sonnet verdicts (tooling drafter; Wednesday re-ran the runner's arms: 3/3 PASS once the deploy key was set)
- **Deterministic half: WORKS.** spark_gate.sh's facts matched the Sonnet gates exactly (r1 9F/7P -> 16P, unit +16; r2 14F/7P -> 21P, unit +21; ruff; mypy aborts the same way), in ~85 s, with no model.
- **Spark review half: NOT READY for tier 2.** r1 found the two biggest findings (the unbounded cancel; the cause stated as fact) but called NO GO, missed the structural reds, caught 1 of 8 overstated sentences, and raised 3 false positives. r2 found 0 of 3 overstated sentences and raised 5 empty or wrong findings out of 10. Single runs, not repeats.
- **IN PRACTICE from now (what works, per Kam's "if this works, put it into practice"):**
  1. **Every gate runs `local-model/gate/spark_gate.sh` FIRST** (the mechanical half: head asserted, red/green on base vs head, suite before/after, lint, facts.json). The Claude gate is handed facts.json and told NOT to re-run what it already proves. It spends its tokens on judgement only: risk, scope, claim-checking, planted violations the runner does not do.
  2. **Tier 3 (hygiene):** the runner alone plus Wednesday's completion check. No Claude gate.
  3. **Tier 2:** Claude gate (Sonnet) on facts.json + a Spark review as a SHADOW. Each shadow run adds a calibration row here.
  4. **Tier 1:** Opus gate as routing v1.0 says; Spark not measured there.
- **Next improvements to the Spark review** (from the drafter, to build before calibration 2): a planted-violation step in the runner; include the cited upstream handlers, not only the cited line; a recommendation field; a one-sentence-at-a-time pass over client comments; findings capped to evidence-verified ones.


## CALIBRATION 2, 2026-10-26 ~16:3x — PR #1690 (KS-1717, TIER 1) plus nine tier-2 shadows (Sonnet shadow agent; Wednesday read its report, findings not re-checked at source by Wednesday)
- **#1690 tier 1: FAIL.** The deterministic half matched Claude round 2 (anchoring 390 passed with 1 red threadTokenMint; originate 1655 passed). The Spark review produced NO verdict: both attempts hit the 8000-token cap in a repetition loop (one finding repeated 22 times) and failed schema validation, 629 s on ~449K prompt tokens. Recall 0 of 7 round-1 findings and 0 of 4 round-2 notes; both distinct claims were false at source (mount order is intended; `emitterSignature.ts:31,109` does hash the Authorization). **Tier 1 stays Opus. No case for promotion.**
- **Nine tier-2 shadows** (#1689, #1692-1695, #1697-1700): all returned valid JSON at `--max-tokens 6000`; Spark NO GO on 6 of 9, which looks high for test-pinning PRs (e.g. a #1699 Major contradicted by identical base results). **Unscored until the Claude tier-2 batch gate verdict lands** (0_Brain/reference/2026-10-26_gate-r2-nine/verdict.md); score recall and false positives then.
- **Tooling owed (fix before the next calibration):** (1) `spark_gate.sh` is pytest-only; the TS/bash harness the shadow agent wrote is now tracked at `2_Project_Files/local-model/gate/shadow_facts.py` (moved out of the session scratchpad 16:3x); (2) `spark_review.py` needs a repetition guard, and its retry resends the whole prompt; (3) PR bodies were not supplied, so the overstated-sentence check never ran.
- Evidence: `0_Brain/reference/2026-10-26_spark-shadow-gates/pr<n>/` (facts.json, review/review.json, verdict.md).
