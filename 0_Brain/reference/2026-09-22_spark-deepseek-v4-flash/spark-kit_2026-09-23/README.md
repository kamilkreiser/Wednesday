> **OWNER: FRIDAY (the laptop seat), not Tuesday.** Kam, 2026-09-23 ~14:1x: *"the kit is addressed to tuesday but it should be addressed to you. its yours as you will be using the spark"*. Wherever this kit says "Tuesday", read **Friday**. Banner added by Friday; the text below is Wednesday's original, unedited.

# Spark Kit — running a local coding model the way this fleet runs one

**Written by Wednesday for Kam, 2026-09-23 10:30 AEST.** Commissioned 2026-09-23 10:28 for the HP Spark box
(NVIDIA, 128 GB) running DeepSeek Flash, so that Datasec work can continue while travelling.

**This kit is METHOD, and it is client-neutral by construction.** It contains no Secuura content,
no Datasec content, and no ticket from either. It is the distilled practice of running a local
model against a real backlog since 2026-09-14 — what works, what fails, and how to tell the
difference. Tuesday applies it to Datasec tickets; nothing here decides which tickets those are.

---

## The one sentence, if you read nothing else

**The model run is free. The BRIEF is the entire cost.** A vague brief does not produce a worse
diff — it produces a *confident wrong one* that fails a check nobody wrote, or worse, passes a
check that could never have failed. Budget accordingly: a handful of good briefs beats a full
queue of bad ones, and the bad ones return FAILs that look like model weakness and are not.

## Who reads what

| File | Reader | What it is |
|---|---|---|
| `01_FOR_THE_LOCAL_MODEL.md` | **The model on the Spark** | The task contract. Goes in its system prompt, or at the head of every task. |
| `02_FOR_THE_COORDINATOR.md` | **Tuesday** (or whoever manages it) | The manual: how to advise, prompt and check a local model, and when to stop. |
| `03_BRIEF_TEMPLATE.md` | **Tuesday**, every time she queues work | The brief shape that passes. Fill it in; do not improvise it. |
| `04_KNOWN_FAILURE_MODES.md` | **Tuesday** | What this class of model gets wrong, each with the evidence and the catch. |
| `05_SETUP_PROMPT_FOR_TUESDAY.md` | **Kam → pastes into Tuesday** | **START HERE.** The block Kam pastes so she stands the loop up and PROVES it works, plus the runbook: what a checker must assert, and the smoke test. |

## Where to slot it

**Start with `05_SETUP_PROMPT_FOR_TUESDAY.md`** — paste its block into the agent that will manage
the box. It drives everything below and ends with a smoke test that must catch two deliberate
breaks before the loop is trusted.

1. **On the Spark box:** put `01_FOR_THE_LOCAL_MODEL.md` where the runner injects a system prompt.
   It is written to be pasted whole. It assumes nothing about the harness.
2. **In Tuesday's tree:** copy `02`, `03` and `04` to `2_Project_Files/local-model/` in the Datasec
   coordinator's folder, and add a line to her boot prompt telling her to read `02` before she
   queues anything at the local model for the first time in a session.
3. **Nothing here is a mechanism.** It is instructions. If a rule in `02` matters enough to hold
   under load, it needs a script that refuses — see the "checker twin" rule in `02`.

## The honest limits of this kit

- **It was learned on a 35B model, not on DeepSeek Flash.** Kam reports the Spark model scores
  ~90-something on round one and ~98 on round two, which is *better* than what this kit was
  built against. Every rule here should hold; the failure RATES will differ, and the
  known-failure list in `04` is a starting hypothesis for a new model, not a finished map.
- **Nothing in this kit has been run on the Spark.** It is untested on that hardware and that
  model. Treat the first week as a pilot and write down what differs.
- **Scoring is not in here.** How good a diff is remains a human-or-Claude judgement; this kit
  tells you how to make the judgement cheap and how to avoid needing it.
