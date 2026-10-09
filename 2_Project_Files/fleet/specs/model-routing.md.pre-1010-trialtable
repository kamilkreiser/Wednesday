# Model routing -- v0 (2026-10-09) -- DRAFT, Wednesday reviews before it is shared

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

## 5. Open items
- Date and content of the "model review phase" (ASSUMED to include a Sonnet vs Opus comparison on the same tasks).
- Whether Haiku and Fable ever enter the predicate; today neither is a worker tier.
- `released` dates are absent when the source is the docs page (only an API key yields `created_at`).
