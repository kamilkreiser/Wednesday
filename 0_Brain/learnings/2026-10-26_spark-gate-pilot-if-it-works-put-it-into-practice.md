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
