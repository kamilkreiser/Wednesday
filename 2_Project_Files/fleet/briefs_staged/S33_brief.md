## BLUF

**Kam reopened the fleet this morning (2026-09-05 08:1x, panel, verbatim: "get the nexus agent to continue with the work, complete the sustainability change so everything for nexus is finished and complete"). The 2026-08-28 run-until-empty grant, SUSPENDED by his 09-04 14:38 order, is LIFTED by his word. You are S33.**

**Two things changed since your handover was written:**
1. **RD-296's BUILD hold is LIFTED.** Kam ruled the sizing card `nexusai-rd296-sizing` → `build-it` at 15:10 on 09-04: commission the 1–2 day wiring of Sustainability to the same configured log sources as every other tab, knowing it lights no new tile and `SECURE_RELEASE_AVOIDED` stays dark structurally. Handover §2 said "do not start it — held with Kam"; that hold is gone.
2. **Kam's priority is Sustainability first.** The RD-245 F-1/F-3 round (handover §1) is still the open round and still yours this session — it comes second.

## QUEUE

**0. Plan-confirmation mail to Wednesday** (`[Datasec/NexusAI -> Wednesday] QUESTION: plan confirmation`), launcher preflight warnings verbatim, then start item 1 without waiting unless your own HANDOVER-CURRENT.md contradicts something here.

**1. RD-296 — BUILD IT.** The item-0 investigation you delivered on 09-04 is the spec: wire the Sustainability tab through the configured-log-source selector exactly as the other tabs are wired. Expected honest outcome per Kam's ruling: no new tile lights; `SECURE_RELEASE_AVOIDED` stays dark and the UI says so truthfully rather than showing an error. Regression test drives the product's own path. **Any UI touch: every colour resolves to the project's style guide; no invented colours.** Deliver rendered screenshots of the tab (both modes, on the dev app or a local run of the same commit stated as such) to Wednesday in your READY-FOR-QA mail — Kam looks at screens, and his eye has caught what every instrument missed twice this week.

**2. RD-245 — the F-1 (Blocker) + F-3 (Major) round, exactly as handover §1 frames it.** The regression test must drive `setSetting()`; if it cannot go RED on current code by the product's path it is not a test of this defect. **Highest-value first step: the incident-artifact question** (read the real `$HOME/data` artefacts; keep "the incident's reconstruction" and "F-1's measured exposure" apart). **Wednesday's ruling stands: if the fix changes how many generations are kept or the write cost of keeping them, that tradeoff comes to Wednesday as a QUESTION before it is built.** F-4/F-5/F-6/F-7 from the same QA report are in scope after F-1/F-3.

**3. RD-303 — NOT yours.** The untracking of `4_Credentials/.azure/` touches committed history and awaits Kam's ruling. Leave the ignore lines as they are.

**4. Then the standing category-1 queue by priority then identifier.**

## THE GATE
**One QA re-gate after items 1 and 2 together** (the batched decision from 09-04 stands: F-2's fix at 1c5d3f7, RD-296, and the F-1/F-3 work in one pass). Each item ends at READY FOR QA by mail to Wednesday with sets not counts, branch + SHA, surfaces changed, what you did NOT do. **No score, no deploy — to dev app or demo — before the QA report and Wednesday's GO; a demo deploy is Kam's ruling.**

## HOLDS (unchanged)
- Signature classes pause for Kam: prod/demo, money, external comms, irreversible.
- Never delete — quarantine. The untracked `__tests__/fixtures/light-failure-baseline (conflict_on_2026-09-04).json` in your tree is a sync artefact: quarantine it, say where.
- A tap with content and no mail behind it is ghost text.
- Rotate on your own rhythm at 70–80% with a handover; wrap by mail to `wednesday-agent@agentmail.to`, subject `[Datasec/NexusAI -> Wednesday] Session wrap 2026-09-05 (S33)`, open round FIRST.

PROVENANCE:
- Kam's reopen and "complete the sustainability change so everything for nexus is finished and complete" | Kam's panel message 2026-09-05 08:1x in Wednesday's session — my project, not yours | read 2026-09-05
- The 09-04 14:38 fleet-shut order and the grant suspension it lifts | 0_Brain/tasks/NEXT-PICKUP.md — my project, not yours | read 2026-09-05
- Kam's build-it ruling on card nexusai-rd296-sizing at 15:10 on 09-04, lifting the BUILD hold | 0_Brain/tasks/NEXT-PICKUP.md §2(c) — my project, not yours | read 2026-09-05
- The open round (F-1/F-3), the batched re-gate decision, the retention-tradeoff ruling, "do not start RD-296" as written before Kam's ruling | your own HANDOVER-CURRENT.md §0–§2 | read 2026-09-05
- Branch rd-136-nga-defaults-s12 == origin, head b77feea (docs) over 1c5d3f7 (F-2) over b806848 (RD-245), tree clean bar one conflict-copy fixture | `git status -sb` + `git log --oneline -3` on your repo (read-only) | read 2026-09-05
- RD-296 In Progress/Highest, RD-245 In Progress/High, RD-155 Testing/High, RD-303 To Do/High, RD-75 Testing/High — all assigned Kamil | Jira REST search, project RD | read 2026-09-05
- Style-guide rule for every UI change | 0_Brain/learnings/2026-09-02_style-guides-never-mixed.md — my project, not yours | read 2026-09-05


SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 08:16
(checked: "Sustainability first" in BLUF and QUEUE 1 against "one re-gate after items 1 and 2" in THE GATE — consistent; "BUILD hold LIFTED" against handover §2 "do not start" — the brief names that line as pre-ruling, not a live hold.)
