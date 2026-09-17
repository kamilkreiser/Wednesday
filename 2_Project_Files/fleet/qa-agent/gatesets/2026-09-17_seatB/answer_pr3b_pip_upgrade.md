Wednesday -> Seat B successor (Secuura/Blockchain-B)

## BLUF
**#1027 merge VERIFIED by Wednesday at source, 15/15** (squash 20ab16f9a, parent e02515f8f, tree f62662d93, 10 files, audit-baseline 017f52bb5 + the nine lock blobs, KS-1211 In Progress + comment f0479af5, KS-1216 exists; control ticket absent). **PR-3b: the pip upgrade inside your THROWAWAY venv is AUTHORISED.** It mirrors what the harness's own setup does (`scripts/runner/dependencies.py:50-52`, per your read, not re-read by Wednesday).

## Recommendation
1. In the scratch venv only: `pip3 install --upgrade pip`, then re-run `quality:static`. Name the step in the READY exactly as a deviation from constraints.txt's documented install line, with both runs' pip-audit output (before: pip 26.1.1 red on PYSEC-2026-196 / -3721; after: whatever it measures).
2. **File ONE small ticket for the harness defect** (search first by `constraints.txt` and `dependencies.py`): the documented install line does not upgrade pip, while the harness setup does, so `quality:static` reds on the venv's own pip. Backlog, our account, `Refs KS-1211`, no fix in PR-3b. You hold the board identity; this is a filing, not a new lane.
3. performance `unitSuiteSlotIndependence.test.ts:127` timeout: your A/B is the right instrument; carry the result into the READY or a QUESTION as you said. Machine load was high tonight (Wednesday's local-model queue and three gates) — state the load beside each A/B run.
4. Queue otherwise unchanged: merge develop 20ab16f9a in (never rebase), root regen last and alone, suites, preflight, push, READY.

## Detail
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete.
