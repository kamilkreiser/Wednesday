# Gate batch 19 drafter — report (2026-10-07 ~05:00 AEDT) and Tuesday's rulings on it

**State:** the drafter (in-session subagent, Opus 5.5) was STOPPED by the safeguards while writing row b2 (RD-794's "no Ollama endpoint contacted" row). Its partial brief (75,473 B, @STAMP@ placeholders, cut inside b2) is quarantined at `fleet/qa-agent/briefs/_quarantine_2026-10-07/2026-10-07_nexusai-gate-batch19.md.PARTIAL-safeguards-stop-do-not-launch` — NEVER stamp or launch it; it holds the full 27-item WRONG list. No launcher was written. Saved whole: `fleet/qa-agent/briefs/2026-10-07_nexusai-rd821-READY-mail.txt`.

**Model:** Kam's 2026-09-30 Opus 4.8 ruling covers QA GATE sessions only. A drafting subagent is NOT covered, so it is not switched. The redraft describes the attack-style rows briefly (what to measure and the expected result, not attack code); the gate writes its own drivers.

## The drafter's main findings (its reads; READ-ONLY unless it says measured)
- RD-761 is not on main, and RD-794 says it merges after RD-761 (both touch server.js). → ADD RD-761 @ 141d7ea as a named NON-MEMBER merge step before RD-794 (as gate 18 did for RD-603).
- RD-697, RD-791, RD-603/RD-756 also not on main; gate 17's RD-697 cross was on round-1 dataErasure.js (6002d71) → re-run the cross against RD-640 r2's 110ad2b.
- Two locks: main d6d3b6e (proxy-addr 2.0.8) vs every member head e9063d4 (2.0.7). The gate installs per lock (L-Y1) and names which.
- RD-640 r2: builder verify on the working tree pre-commit (blob sha matches f49ee7f6db9b89a4); mutants each on the rd640 file only (not the union); Linux claim names no log; loop detection by PATH STRING not file identity (a loop through a dir symlink kept as a failure = safe but never finishes); the "kept" message may write an absolute (outside-DATA_DIR) path into the failure record.
- RD-794: renames 8 cells and parks W5 in a jest-ignored folder → 9 main test ids missing on any merged tree carrying RD-794 (C-133 accounting, "missing 0" does not apply); LLM_PROVIDER=__proto__/constructor resolves to a built-in object, not azure-openai, while the warning says "Using azure-openai" (READ); two reachable /api/status Ollama fetch sites (~19117, ~19161), the READY names one.
- RD-819: the empty-body refusal is truthiness-only — {"azureOpenAIEndpoint":" "} still reaches the writes (READ); its W5 "git mv" shows as a 40% rename (cell rewritten).
- RD-821: merge-first can file a merge AT a gate's ns when a builder yielded right behind the gate; a lower-pid merge then sorts AHEAD of the gate (contradicts C-141 ADDENDUM 6); --replace's claude-anchor uses ps (may refuse in a sandbox); "merge" is a substring match; READY cites an "arm 6" the harness lacks. --replace covers a re-file only while the old waiter is still queued (gate 18's 11:24Z case had already left), and gate 18's filer has no --replace.
- Slots E (RD-801/822) and F (RD-807): local only, no origin ref, no counts commit → not READY-shaped yet.

## Tuesday's rulings (2026-10-07 ~05:0x)
1. RD-761 as a non-member merge step before RD-794: YES.
2. Redraft: YES, by the next drafter (fresh), on Opus 5.5 with attack rows described briefly; input = this file + the quarantined partial's WRONG list. Commission after the builders answer the forwards below (their fixes may change heads).
3. RD-821 merge-sorting-ahead-of-a-gate: forwarded to O NOW as a probable defect in a live mechanism; the gate measures it with a controlled pid; severity is the gate's (Major if measured).
4. Browser leg for RD-794: NO.
5. Forwarded the READ findings to their builders (N: RD-640; R: RD-794/RD-819; O: RD-821) to check and fix BEFORE the gate, so the round is not spent on them.
