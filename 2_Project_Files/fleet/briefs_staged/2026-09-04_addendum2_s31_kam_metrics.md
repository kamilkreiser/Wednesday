# ADDENDUM 2 (S31) — Kam narrowed his own sentence five minutes later; branch (a) is now the EXPECTED answer

## BLUF
**Kam followed his logs statement with a second one, VERBATIM, 2026-09-04 09:14:11 +10:00:**

> *"of course the metrics (sustainability data) lives outside the log as no log will capture this"*

**Read together, the two sentences describe: LOGS IN → METRICS DERIVED.** The configured log sources are the
INPUT; the sustainability figures are computed from them and are not themselves logged, because no printer log
would carry a CO2e or a water figure. **That makes branch (a) of my previous addendum the expected answer and
branch (b) unlikely — so do not spend a long investigation on (b).**

## Recommendation
**Narrow the work, do not close the question.** Confirm the WRITER path into `printer_logs` — is it fed by the
configured log sources — and confirm the sustainability figures are DERIVED from those rows rather than stored
independently. **That is a much smaller job than the binary I sent you fifteen minutes ago, and it is the
whole remaining job.**

## What this changes about the fix
**If (a) holds — and it now probably does — then `SEED_DEMO_DATA` is the RIGHT demo mechanism, not a
workaround**, because it seeds the LOG data the metrics legitimately derive from. That is a materially better
answer than the one I gave you at 23:06, and it comes from Kam narrowing his own statement rather than from
any new measurement. **The config-plus-deploy GO becomes straightforward once you confirm it.**

**Still record it accurately:** the demo is empty because **no log source is configured or ingested there**,
and seeding substitutes for that. **That sentence belongs in `CLAUDE.md` and in RD-294** — it is the true
account, and it is not the same as "the seed is dormant", which is what the doc says today.

## WHAT DOES NOT CHANGE, and this is the part I will not soften
**Kam's sentences are a statement of INTENT from the principal, not a measurement, and they do not close a
code question.** They tell you what the system is meant to do; only the code tells you what it does.
**If the writer path disagrees with either sentence, the CODE governs and that disagreement is the finding —
report it and do not reconcile it away.** I would rather you spend twenty minutes proving him right than
assume it.

**Unchanged: no deploy, no demo config touched, the GO is mine and still unissued.**

PROVENANCE:
- Kam's second sentence, verbatim and unedited | his own message on the dashboard chat panel, 2026-09-04T09:14:11.523574+10:00 | read 2026-09-04 09:14
- Kam's first sentence, which this narrows | his message 2026-09-04T09:09:18.107886+10:00, relayed to you in the previous addendum | read 2026-09-04 09:14
- The reader path already established (`getAllPrinterLogs()` unconditional at `backend/server.js:20794`) and `SEED_DEMO_DATA` absent from the revision | YOUR STATUS mail 2026-09-03T23:03:56Z — your measurements | read 2026-09-04 09:14

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 09:14
