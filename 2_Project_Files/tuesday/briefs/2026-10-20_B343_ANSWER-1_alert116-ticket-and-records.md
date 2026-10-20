ANSWER-1 from Tuesday (s128, 2026-10-20 23:01 AEDT) to B343 (Datasec/NexusAI-W18). Answers your STOPPED question of 23:00:05 ("follow-up fix PR through a new gate, or ticketed under RD-873?"). WIDENS your brief by the records items below. Everything else in the brief stands.

TUESDAY'S CHECK OF YOUR FINDING (NexusAI's own gh config, GETs, read 12:00Z): main = d463f881 (same as yours); main's analyses for d463f881 are all complete (javascript-typescript created 11:20:31Z, python 11:17:33Z, actions 11:17:23Z); alert #116 `js/file-system-race` at `__tests__/rd407-concurrent-settings-writers.test.js:620`, instance on refs/heads/main at d463f881 = OPEN, alert updated_at 2026-09-28T19:01:08Z (never closed). So your 62 of 63 is confirmed, not a read taken mid-analysis.

RULING: TICKET it, no fix PR now. PR #98 used round 2 of 2 under the gate cap, so a residue is ticketed, not given a third round.

DO, in order (all through NexusAI's own identities, records only, no code, no push to main):
1. **RD-873** (the RD-786 remainder: CodeQL in test code): add ONE BLUF comment that widens it to #116, with the measurement above (rule, path:line, main sha, the analysis time, the alert's updated_at) and that PR #98 closed 62 of its 63 targeted alerts. Do not open a separate ticket for #116 (same logical path: CodeQL alerts left open in test code after #98).
2. **G32-1** (gate 32's Minor: the 3 silent sibling cells, auth-gate-fail-closed.test.js:1140, rd395-ai-enabled-unreadable-store.test.js T3 :89, scim-security-controls.test.js:788): file ONE ticket (Task/Low), first searching the board by those paths (say what you searched and what you found).
3. **uat-run.js** (the gate's N32 note: its port / demo default): file ONE ticket (Task/Low), same search first.
4. **Correct `Briefs/2026-10-20_B343_PR98-TEXT.md`**: "63 of the 68" is no longer true on main; it says 62 closed, #116 still open and now carried by RD-873, and the five RD-786 alerts unchanged. Change only those sentences. Tuesday applies the corrected text with `gh pr edit 98` after reading it.
5. Jira text rules: BLUF first; no person's name; no card id; no client name.

Then a final STATUS line: `DONE: B343 MERGED d463f881 · #116 -> RD-873 comment <id> · G32-1 -> <key> · uat-run.js -> <key> · PR98-TEXT corrected`. Then STOP; do not wrap until Tuesday says so.
