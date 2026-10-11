# Model routing -- v0.1 (2026-10-11) -- DRAFT, Wednesday reviews before it is shared

One definition for every coordinator seat (Wednesday, Tuesday, Friday). Client-neutral: no client names, tickets or code.
Evidence tags: **RULED** = Kam's words, dated. **OBSERVED** = measured here. **SINGLE TRIAL IN PROGRESS -- pilot only** = one data point, not a rule. **ASSUMED** = reasoning, untested.

## 0. Where model IDs come from (RULED, Kam 2026-10-09)
"Check what the latest claude models are at the different levels ... you make a deliberate decision of whether to use Opus, Sonnet or either local model."
- IDs are read from `0_Brain/dashboard/data/models_latest.json`, written by `2_Project_Files/tools/latest_models.sh` from a live source (Models API when a key exists, else the public docs overview page). **Never typed from memory, never copied from an older brief.** (OBSERVED: a seat started on an older Opus because a launcher pinned it.)
- Run the tool at boot; `doctor.sh` warns if the JSON is missing or older than 24 h. A failed refresh (rc 3/4) keeps the old file and says so: treat the IDs as unverified until a refresh succeeds.
- "Newest at its level" means the highest version of that level (opus / sonnet / haiku / fable) in the JSON.

## 1. The four worker tiers and when each is chosen
| Tier | Where | Selection predicate | Evidence |
|---|---|---|---|
| 1. Ornith 1.5 | local, the Studio | One or few files; the fix shape is spelled out in the brief; a runnable test decides pass/fail; NOT an auth / credential / security surface. | Harness exists; results are per-task and recorded on each task's own receipt. ASSUMED as a general rule: SINGLE TRIAL IN PROGRESS -- pilot only |
| 2. The Spark | local | Same predicate as tier 1. Chosen alongside or instead of tier 1 by availability and fit. | SINGLE TRIAL IN PROGRESS -- pilot only |
| 3. Claude Sonnet (newest) | cloud | Raise / gate / merge seats and drafters, when Sonnet is the active default. | SINGLE TRIAL IN PROGRESS -- pilot only (trial PAUSED, see section 4) |
| 4. Claude Opus (newest) | cloud | Reserved for work a cheaper tier has measurably failed, or high-judgement security design -- **when Kam's current instructions allow**; right now they direct Opus for all Claude workers (section 4). | RULED for the current override; the "reserved" default is ASSUMED |

Local-tier counter (RULED by practice, recorded per task): the original brief plus ONE rebrief; if it still fails, the task goes to a Claude seat. No third local attempt. Deliberate choice is the point: the launch receipt must show the predicate was applied, not defaulted.

## 2. Launch receipt
Every launch (pane seat or sub-agent) states on its receipt one line:
`model: <id from models_latest.json> -- <tier 1-4> -- <why: which predicate line applied, or which override>`
A receipt with no model line, or an ID that is not in `models_latest.json`, is an incomplete receipt.

## 3. Switching a seat's model
Project launchers pin their own model, and launchers are the project's files, which a coordinator does not edit. So: after launch, send `/model <id>` into the pane (id from the JSON), then confirm by mail/receipt that the pane reports the new model. OBSERVED: `doctor.sh` lists every launcher pin that is not newest at its level (`stale_pins` in the JSON); fixing the pin itself is a request to the project's own agent, not an edit. In-session sub-agents take the model from the spawning call: set it explicitly rather than inheriting.

## 4. Current overrides (read first; each has an expiry)
1. **RULED, Kam 2026-10-09 ~09:4x (supersedes the same-morning Sonnet instruction):** "all sub agents are starting as opus 5. if you use opus for sub agents (after the next model review phase this should be a deliberate choice) use the best version of opus. for now, use Opus 5.5 for all sub agnets."
   Reading: every Claude worker -- pane seats and in-session sub-agents -- runs on the **newest Opus** from `models_latest.json` (today `claude-opus-5-5`; do not type it). The Spark and Ornith still go first wherever the section-1 predicate fits. **Expiry: the "next model review phase"** -- the date is not stated; ask Kam when that phase is, and until then this stands. After it, Opus on a sub-agent must be a recorded, deliberate choice (section 2).
2. **PAUSED:** the earlier instruction (Kam, same morning) that Claude workers run on Sonnet until Monday 2026-10-12. The Sonnet trial resumes at the model-review phase; tier 3 evidence stays SINGLE TRIAL IN PROGRESS -- pilot only until then.
3. **Stale launcher pins are prominent, not cosmetic (OBSERVED 2026-10-09):** several project launchers pin an older Opus (and older Fable). A seat launched from one runs on the pinned model regardless of this document until `/model <id>` is sent (section 3). The list is in `models_latest.json -> stale_pins` and the doctor output.

## 7. Decision ladder (v0.1, 2026-10-11 -- Kam 12:56 live board: "Work mainly on tickets with the spark and Sonnet. Priority for now is to refine a structure that identifies where to use Opus, Sonnet, Spark and Ornith. Do this on live tickets and work through the secuura tickets as you do")
This SUPERSEDES section 4 item 1 (Opus for all) for Secuura work; evidence tags below are honest: every line is a hypothesis scored by section 6 rows, not a rule.
Ask in order; the first YES picks the tier, and the receipt names the question that decided it.
1. Does the ticket's fix shape fit in ONE brief: 1-3 edits, the line text known, a runnable in-process test, no auth/credential/security/money surface? -> **Spark** first (Ornith only for the simplest one-file). Evidence: Spark 24/24 first-round PASS over 2026-09-29..10-05 (OBSERVED, ~13 min machine time); Ornith 1.5 harder rungs (OBSERVED, per-task). Counter: original + ONE rebrief, then tier 2.
2. Must a seat RAISE a PR, run a tool chain, write docs blocks, or merge on a GO, and is the surface not security/deploy? -> **Sonnet seat**. Evidence: 12+ Sonnet seat rows 0.95-0.98, one Major past a seat caught by the gate (OBSERVED, section 6 reading). Pattern: launch, switch to Sonnet at the first idle prompt, say so on the receipt.
3. Is it a BUILD that fails question 1 (multi-file, design choices) but is not decision-shaped? -> **Sonnet build seat with an Opus QA gate** as gatekeeper (Kam 2026-10-10 09:06). Evidence: one row (G 8th, 0.98), pilot only.
4. Is it a QA gate, a security/auth/money/deploy surface, or work a cheaper tier has measurably failed twice? -> **Opus** (newest in models_latest.json). Evidence: gate83 caught a Major the builder's log showed (OBSERVED); the rest ASSUMED.
5. Is it a decision for Kam (ruling, comms, money)? -> a CARD, no worker.
Each live-ticket outcome adds a row to section 6; rule text is promoted from hypothesis only at >= 5 rows of a kind.

## 5. Open items
- Date and content of the "model review phase" (ASSUMED to include a Sonnet vs Opus comparison on the same tasks).
- Whether Haiku and Fable ever enter the predicate; today neither is a worker tier.
- `released` dates are absent when the source is the docs page (only an API key yields `created_at`).

## 6. Trial table (started 2026-10-10 09:0x on Kam's question "which task and what level of complexity to route to which model")
One row per task. A row is written when the task's output has been checked at source, never before. Columns: date · tier/model · task kind · rung or size · rounds · defects found AFTER delivery (by whom) · Wednesday's corrections · outcome. **No routing rule is written from fewer than 5 rows of a kind.**

| date | tier / model | task kind | size | rounds | defects found after delivery | outcome |
|---|---|---|---|---|---|---|
| 10-10 | Sonnet (sub-agent) | merge-seat brief draft (R 30th, gate80) | 300 lines | 1 | knob line for a no-M row unread against the seat's tool (Wednesday's GO, not the draft) | used; seat landed 2/2 rows |
| 10-10 | Sonnet (sub-agent) | gate kit build (gate80, gate81) | full kit + arms | 1 each | 0 reported by either gate | used; both gates GO |
| 10-10 | Sonnet (sub-agent) | Spark carve screen (CARVE_0830) | 3 tickets carved | 1 | 0 at Wednesday's source read; 1 of 3 held back as a decision | 2 queued, 2 PASS |
| 10-10 | Sonnet (sub-agent) | merge-seat brief draft (R 31st, gate81) | 327 lines | 1 | pending (seat not launched) | pending |
| 10-10 | Spark | bash fix + new test, carved (KS-1426 p1) | rung 2, +35/-1 | 1 | 0 | PASS 7/7, byte-identical, HELD |
| 10-10 | Spark | config line + new test, carved (KS-1417 p1) | rung 2, +2/-1 | 2 (1 harness-fault resume) | round 1: unclosed output fence (format, not code) | PASS 7/7, byte-identical, HELD |
| 10-10 | Spark | run-migrations message (KS-1456) | rung 2 | 1 | 0 | PASS 7/7, HELD |

| 10-10 | Sonnet SEAT (F 8th) | raise: Spark pass -> PR #1447 (KS-1456) | 1 PR, tier 2 | 1 | 0 (gate82 GO) | landed; scored 0.97 |
| 10-10 | Sonnet SEAT (G 8th) | BUILD: KS-1434 spec + regenerated yaml + tests | 1 PR (#1448), tier 1 | 1 | 0 (gate82 GO) | gated GO; merge in flight (R 36th); 0.98 |
| 10-10 | Sonnet SEAT (F 9th) | raise: Spark pass -> PR #1449 (KS-1417) | 1 PR, tier 2 | 1 | wording only ("every clone", gate82; fixed in the squash body by Wednesday) | landed; 0.96 |
| 10-10 | Sonnet SEAT (F 10th) | raise: Spark pass -> PR #1450 (KS-1426) | 1 PR, tier 2 | 1 | **1 Major** (N-1450-1, gate83: wrong surface count from a linked worktree) | NO GO -> fix round; 0.96 |
| 10-10 | Sonnet SEAT (F 11th) | FIX ROUND on #1450 | 4 files +199/-19 | 1 | pending (gate84) | pushed; real hook proved the fix; 0.97 |
| 10-10 | Sonnet SEAT (R 31st-R 35th, 5 seats) | MERGE seat (port tools, merge-in, squash on a GO) | 1-2 rows each, 7 rows | 1 each | 0 reached develop; every squash verified at source by Wednesday | 7/7 landed; 0.97/0.96/0.96/0.96/0.97 |
| 10-10 | Opus 5.5 QA gate (gate82, gate83) | tier-1/2 gates on Sonnet output | 3 + 1 PRs | 1 each | gate83 caught the Major the builder's own log showed | 0.95 / 0.97 |

**Reading after 12 Sonnet seat rows (10-10 18:5x, Wednesday; NOT yet a rule):** Sonnet seats delivered merge and raise work at 0.96-0.98 against 0.98-1.0 for today's Opus 5.5 seats (n=3: R 29th 1.0, R 30th 1.0, F 7th 0.98; G 7th 0.98 ran its round on Opus 5 (10-10 ledger row); R 28th 0.95 was still on Opus 5 at its last recorded read, switch owed, so its model is UNMEASURED). One Sonnet delivery in 10 carried a Major past the seat (F 10th, caught by the Opus gate). **Confound:** every Sonnet seat ran ITEM 0 and its plan on Opus 5 before the switch. Unmeasured: ctx cost per task by model; wall-clock per row. Kinds below 5 rows (build, fix round) carry no rule yet.

Rows for 10-09 23:12 → 10-10 08:00 (the overnight Sonnet drafters and Spark rungs 1/3/4/6) are recorded in `0_Brain/daily/2026-10-10.md`, not yet transcribed. **NEXT TRIAL (stated to Kam 09:02, his word redirects):** the next raise seat runs on Sonnet as SEAT trial #1. Gates, merges, deploys and security surfaces stay on Opus until this table has evidence.
