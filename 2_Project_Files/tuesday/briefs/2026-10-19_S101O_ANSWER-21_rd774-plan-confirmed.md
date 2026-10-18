BLUF: PLAN CONFIRMED for RD-774 + RD-836 as you wrote it (A templates by id, stored sql_query never executed again and left on disk; B request SQL refused 400 code-only SQL_TEXT_NOT_ACCEPTED on the three writers, raw-SQL log line removed, settings.js stops sending SQL; C admin gate via requireAdminFor on POST/PUT/DELETE/sync + PUT field allow-list; the cells as listed). RULED P1 = (ii); P2 = ticket, not built here. Build now.

P1 ruled (ii): POST /api/test-custom-query refuses SQL text with the same 400 code and runs nothing; testing.html's box stays but can no longer run anything. Reason: Kam's ruling (b) says the endpoint stops accepting SQL, and (ii) is exactly that with no removal and no new words; removing a shipped page control (iii) or repurposing it (i) changes what ships, which is a scope decision for Kam, not an application of his ruling. File ONE ticket (search first by symbol: test-custom-query, testing.html) "testing.html's SQL box can no longer run anything after RD-774 (b): remove the page control, repurpose it, or keep it" with your (iii) recommendation, labelled for Kam's decision; Tuesday cards it later.

P2 ruled: a ticket for client-sent KQL (POST's validated kqlQuery; PUT closed by your allow-list), searched first, filed now, not built here. Agreed with your reasoning.

Item 5 (the dropped .params defect): characterise on today's main FIRST, as you planned, and report main vs bound-template results per template in the READY. Correcting the SQLite-fallback results is in scope (it is the same code path Kam's ruling replaces); state in the READY which UI paths now return different rows than main and why. If a difference reaches a customer-visible screen on the demo path (LAW), STOP and ask: the demo uses kql_query, so it should not.

Unchanged: tier-1 gate before any merge; NEW WORDS as you wrote (code only, "Admin access required" reused verbatim); no production, no demo deploy; C-170 stays held for gate 28's delta item and Tuesday's GO; jest lock FIFO with gates 27/28.

-- Tuesday
