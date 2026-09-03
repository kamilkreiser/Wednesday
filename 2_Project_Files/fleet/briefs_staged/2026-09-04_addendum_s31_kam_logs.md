# ADDENDUM S31 — Kam's own words on where the data must come from, and they may change the fix

## BLUF
**Kam read your RD-294 finding and answered with a design statement. VERBATIM, 2026-09-04 09:09:18 +10:00:**

> *"great. the system must get all its info from the logs (1 or more configured in settings). good catch!"*

**This may mean `SEED_DEMO_DATA` is a workaround rather than the fix, and I am not going to decide that from
his one sentence. Establish it from the code before the config-plus-deploy GO is issued.**

## Recommendation
**Do not stop item 0 or the QA gate — both continue.** But **before I issue the GO, answer the question
below**, because if the answer is (b) then the GO I described is the wrong GO.

## THE QUESTION, and it is a code question, not a Kam question
**Is `printer_logs` the INGESTION SINK for the log sources configured in settings — or a separate store that
demo seeding fills and real ingestion never touches?**

- **(a) It is the sink.** Then an empty store on the demo means *no log source is configured, or ingestion has
  never run there*, and `SEED_DEMO_DATA` is a **demo shortcut** that makes the tab look alive without the
  product's real path being exercised. **That is defensible for a demo and it is what I provisionally
  approved — but it must be CALLED that**, in the ticket and in `CLAUDE.md`, not recorded as "the fix".
- **(b) It is a separate store, and the configured log sources feed something else entirely.** Then the
  Sustainability tab reading it **is the defect**, Kam's sentence is a statement of intended design that the
  code does not implement, and seeding would paper over a real architectural gap **on the surface he is about
  to demo from.** That is a bigger finding than RD-294 and it needs its own ticket at a higher priority.

## How to settle it
**From the code, and name the settle point.** Where do the settings-configured log sources land? Does anything
write to `printer_logs` other than `seedDemoDataIfRequested`? **Follow the writers, not the readers** — you
have already established the reader (`getAllPrinterLogs()`, unconditional, `backend/server.js:20794`). **If
there is a real ingestion path that writes there, (a) holds. If the only writer is the seeder, (b) holds.**

**A third possibility, so the question is not a false binary: it may be BOTH — a sink that real ingestion
writes to AND the seeder fills. Say so if that is what you find**, and then the question becomes whether any
log source is configured on the demo at all.

## What I am NOT asking you to do
- **Do not change the design.** Whichever answer it is, it is a finding and a ticket, not a build.
- **Do not touch the demo config.** The GO is still mine and still unissued.
- **Do not treat Kam's sentence as a spec.** It is a principal's statement of intent, relayed to you
  verbatim through a channel with an author. **It tells you what he expects the system to do; only the code
  tells you what it does** — and if they disagree, that disagreement is the finding.

PROVENANCE:
- Kam's sentence, verbatim and unedited | his own message on the dashboard chat panel, 2026-09-04T09:09:18.107886+10:00 | read 2026-09-04 09:12
- The reader path `getAllPrinterLogs()` unconditional at `backend/server.js:20794`, `DB_PATH` container-local, `SEED_DEMO_DATA` absent from the revision | YOUR STATUS mail 2026-09-03T23:03:56Z — your measurements | read 2026-09-04 09:12
- That the config-plus-deploy GO is unissued and remains Wednesday's | Wednesday's ANSWER mail to you, 2026-09-03T23:06:43Z | read 2026-09-04 09:12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 09:12
