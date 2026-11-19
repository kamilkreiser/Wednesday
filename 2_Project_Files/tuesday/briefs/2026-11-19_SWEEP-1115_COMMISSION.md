# SWEEP-1115 commission — Datasec actionable lanes, read-only (Tuesday s292, 2026-11-19)

Output: `2_Project_Files/tuesday/briefs/2026-11-19_SWEEP-1115_datasec-actionable-lanes.md`.
FORM AND INSTRUMENTS: copy `2_Project_Files/tuesday/briefs/2026-11-18_SWEEP-2305_datasec-actionable-lanes.md` (read it whole
first; its instruments live in `2_Project_Files/fleet/state/s291/sweep2305/` — read each before use, GET-only; copy them to your
scratch `2_Project_Files/fleet/state/s292/sweep1115/`). Same fences: no Jira/GitHub/git writes, no mail, no az, no deploy,
no `cd`, no token printed, `decision_queue.sh` for `show`/`prior` only, nothing under Secuura, WEDNESDAY or FRIDAY trees.

## What changed since SWEEP-2305 (verify each at source; do not trust this list)
Landed: MPS #216 (MPSCALC-414) + records (MPSCALC-415 filed); HPSM #336 (HPSMPOC-510) + records; NexusAI #227 (RD-994),
#228 (history), #229 (RD-1005 + RD-1007, merge 46050e25). Filed: RD-1006, RD-1007. A NexusAI records pass for #229 is
being drafted NOW (B1730): it will comment/move RD-1005 and RD-1007 and file follow-ups for (a) other unguarded req.body
reads, (b) the final error handler's development text, (c) the RD-523 code-string exception + chat bubble innerHTML —
so exclude those subjects from lanes (say so).

## This time NexusAI IS swept for lanes (no seat holds server.js or the jest lock now)
NexusAI has ~870 open RD keys: do NOT read all. Predicate as SWEEP-2305 (open, not held/ruled-against in the pickup
`0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` or today's/yesterday's notes `0_Brain/daily_tuesday/2026-11-1{8,9}.md` — grep each
candidate key and read DROPPED/HELD lines; ticket says what to change; no new customer words; no client human's open
question; no deploy; no Partner Center). Rank NexusAI candidates by: label security or records-pass-*, then priority,
then newest; read up to ~25 candidates' descriptions + last comments; propose up to 3 file-disjoint NexusAI lanes
(name the files each touches by reading the code at main 46050e25; backend/server.js lanes cannot run in parallel).
ALSO report the state of the NexusAI roles-UI program (Kam 2026-11-06, card nexusai-roles-ui-seven-1106 ruled a;
`2_Project_Files/fleet/state/kam_docs_1106/nexusai_roles_ui/ITEMISED-CHANGES.md` + `WORD-PACK.md`): were its rows
ticketed (search Jira for the itemised rows), which are built/landed, and what blocks the rest — measured, not inferred.

## Other three projects: refresh SWEEP-2305's census and buildable keys (HPSM-POC, MPS, Composer)
Same exclusions as SWEEP-2305 (HTML phase items wait for Kam+Paul; HP-tool integrations; UAT hold; Composer Guided hold;
customer words are Kam's). MPSCALC-415 (docs words): say whether it is a words question for Kam or buildable as written.
RD-1006 (design-sized): say whether a design-first drafter can start it without a ruling.

## Output shape
BLUF (count of buildable keys and lanes per project; recommended order, at most 4 lanes, file-disjoint), census table with
controls, per-lane: keys, files, size, gate tier guess, why buildable, what would STOP it; EXCLUDED list with reasons;
QUESTIONS for Tuesday. First line: `SWEEP-1115: <n> lanes`. Clock from `date`, never typed.
