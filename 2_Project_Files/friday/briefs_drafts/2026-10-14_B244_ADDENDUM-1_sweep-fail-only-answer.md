From Friday (laptop seat), Datasec / HPSM-POC. ADDENDUM-1 to B244 SEAT-A: the answer to your ONE question (HPSMPOC-229).

Thank you for stopping on the brief's own condition rather than building the risky half. Your reading of the two sources is the reason this is easy to rule.

ANSWER: (a) FAIL ONLY. The ticket's own words allow it: "check each named path in the store, then finish the run OR mark it failed" — and the store cannot finish a run without reading blanked kept copies outside a request, which the brief excludes.

Build exactly your (a):
1. A sweep registered in `AssessmentModule.cs` (not `Program.cs`), only when `Assessment:ImportsEnabled` is true, new file under `Ingest/`.
2. It marks every run still `pending` past an age bound as `failed`. Derive the bound from the upload path's own limits and state the derivation; a fresh in-flight run is never touched (your control). It records `StoredAt` for each named file it finds in the store so its download works, and it READS NO FILE CONTENT.
3. Both providers (SQLite and the SQL Server shard), red at base / green at tip, the no-age-bound mutant turns the control red, restored equal.
4. The ONE reason sentence a user can read goes under NEW WORDS for Kam's card, verbatim, with where it renders. Write it plainly (what happened, what the user does next); do not invent a support process.
5. No migration, no contract change, no setting change; if any becomes necessary, STOP again.

Then finish the STATUS (fill @@TIP@@ and @@PINEND@@ from ls-remote after your push) and end with the brief's last line exactly: `READY FOR GATE: b244/lane1-api-tests @ <sha>`.
