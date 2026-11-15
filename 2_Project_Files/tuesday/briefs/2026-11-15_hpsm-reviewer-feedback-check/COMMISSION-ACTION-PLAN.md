# Commission: HP reviewer feedback ACTION PLAN (Tuesday s278, 2026-11-15 ~17:2x)

## Kam's ruling (live board 2026-11-15 17:16:37, view=tuesday, verbatim)
"please action the reviewers feedback.   keep the 16 questions.  and yes, the stated-by-the-customer label does print in the exported report"

Reading (Tuesday's): Kam rules that the reviewer's feedback is actioned now (it is no longer waiting on the 11-10 phase decision for these items), and the question set stays at 16 questions (no question added, none dropped: so D-003's "four added, three dropped" is NOT adopted; reorder and rewording are allowed). His last clause confirms our finding (it is not an instruction).

## Inputs (read whole)
- `FEEDBACK.md` (the 14 items F1-F14) and `RESULT.md` (the evidence: file:line at HPSM main, D-items) in this folder.
- The phase decision document `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_v21_gap_analysis/DECISION-DOCUMENT.md`: the D-items RESULT.md names (D-002, D-004, D-005, D-006, D-007, D-010, D-011, D-012, D-016, D-018, D-022) for their size, risk and dependency analysis.
- HPSM-POC code at origin main (`datasecau/HPSM-POC`, `gh api -X GET` under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'`); main was `f32b209bfa6f33c3c0268c1daa76753c816b316e` at 17:1x. NOTE an in-flight change: branch `b1577/hpsmpoc-168-industry-choice` (head fda88777) adds ruleset 0.1.3 + package 0.7.1 (the Industry field) and is in a G1 gate now; any question-set change in this plan is a LATER content version on top of it (0.1.4 / 0.7.2) and must say so.
- Jira HPSMPOC read-only (credentials in-process from the project `.env`, never printed; JQL `project = HPSMPOC AND ( ... )`).
- The project's CLAUDE.md (the phase rules: this phase builds no integration with HP tools; HP-facing words need the product owner).

## What to produce (write ONLY these files, in this folder)
`ACTION-PLAN.md`:
1. BLUF: how many items become build work now, how many need words from Kam or content from an HP SME first, how many are answers/questions only.
2. Per item F1-F14, one block: (a) what "actioned" means here, keeping 16 questions; (b) the class: BUILD-NOW (no new user-readable word, or only words the feedback itself supplies verbatim and Kam's "action" approves), WORDS-FOR-KAM (a new or changed user-readable word that is ours to propose: give the exact proposed text), HP-SME (content only HP can supply, e.g. whether WXP is released, an EWS setting, timeframes for a hardware item), ANSWER-ONLY (a reply to the reviewer, no product change), COMMERCIAL; (c) the exact ticket text (BLUF / Recommendation / Detail, the project's JIRA.md form; no person's name, no card id) or the existing ticket to comment on; (d) size and the files it touches at main (file:line); (e) dependencies and the order.
3. LANES: group the BUILD-NOW items into lanes that share no file, with an order (the question-set lane is one lane because every question change is one new content version: reorder F5/F6 + rewording F7 + answer options F1/F4 if in scope + finding text F2 + timeframe F12 belong together or must be sequenced). Say which lane can start while b1577 is unlanded and which must wait.
4. The F7 rewording: quote the reviewer's two proposed questions verbatim and say whether Kam's "action" covers them as approved words (Tuesday's default: yes for F7, since the reviewer wrote the exact text and Kam said action it; flag it as Tuesday's reading).
5. A short list of questions for HP (F2's two, F3's keep/reword, F12's timeframe for a hardware item) as the text of ONE comment for the HP question list ticket (find it: HPSMPOC-241 or -181 per RESULT.md; read both and pick).
6. What NOT to do: anything that adds or drops a question; any HP-tool integration; anything next-phase that Kam's ruling does not reach.
Measure every file:line at main; mark DERIVED/RELAYED/UNMEASURED. Read-only everywhere else: no Jira write, no git write, no message, no code. Never type `cd`; absolute single-quoted paths. Last line of ACTION-PLAN.md: `PLAN DONE: <n> items, <n> lanes, <n> word items, <n> HP items`.
