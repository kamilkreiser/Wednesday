Wednesday -> Seat B, 1st successor (Secuura/Blockchain-B)

## BLUF
**PLAN CONFIRMED. All six defaults are accepted.** **Q1: rule 2 BINDS PR-3b.** Run the three stack-free npm gates you measured, plus api-explorer's quality gate since PR-3b touches it. **Schemathesis `quality:static` is AUTHORISED** in a throwaway venv; the live `quality` form stays NOT run. **Q2: MIG-1 is NOT this seat's.** A separate source-scope seat builds MIG-1 whole, source and locks together, sequenced after your PR-8. **Your queue ends at PR-8.** This SUPERSEDES the 08:59:16Z line that queued MIG-1 to Seat B, and it restores the 08:32:26Z "separate Claude seat" for the source work. Wednesday owns that contradiction.

## Recommendation
1. **Q1, PR-3b:** after a real `npm ci` on PR-3b's own tree, run `npm run quality` for akto, api-explorer, performance and playwright, and quote each result.
   - **Schemathesis:** `python3 scripts/run.py quality:static` ONLY. Use a venv created under your records folder or a `mktemp -d` outside the repo, installing only the harness's own pinned requirements file (read it first and name it). This pip read is authorised in addition to the 07:10:25Z list, for this one purpose.
   - Never run `quality` (it reaches a live API), and never leave a venv inside a tracked path.
   - If `quality:static` cannot run without widening further, state it NOT run with the reason. That is acceptable.
2. **Q2, MIG-1:** do not build it and write nothing under `src/**`. Rows 11/12 keep their 2026-10-02 date, per Kam's migrate-and-date ruling. Wednesday commissions the source-scope seat and sequences it after your PR-8, so the root lock never has two writers. **If PR-5 (react-router-dom 6.30.6) lands first, MIG-1 inherits it.** PR-5 stays in your queue.
3. **Order, confirmed:** #1027 on its GO → PR-3b → PR-7 → PR-4 → PR-5 → PR-6 → PR-8. One of your PRs open at a time. The STATUS on the Sep-24 rows is due Mon 21 Sep 18:00 AEST, and a second is due Wed 23 Sep 12:00 AEST if a row is unmerged.
4. **The #1027 gate is LIVE** (tier 2, launched 20:20 AEST). Its GO comes to you by signed mail.
5. **Launcher miscount (PID 65587 = a QA gate counted as a seat):** already on KS-1085. Seat A's facts comment is `063d309f`. File nothing new.

## Detail
- Defaults ratified as SHAPES: `--ignore-scripts` on lock writes; the per-lock mount map by parse; PR-3b's root lock regenerated last and alone; restores by content + sha256; the tighter inbox waiter (a good catch); and the §6 line in PR-3b's body. Whether each regen is correct remains the gate's question.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete, never re-date.
