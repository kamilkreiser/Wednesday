# Wednesday's rulings on the gate79 kit (KIT_REPORT.md §7), read WHOLE by Wednesday before launch

All at the kit's defaults:
- **Q-SEAT79:** the merge seat is **Seat K 3rd**; GO string `GO (Seat K 3rd): merge 1437 on gate79`. It lands only after gate77's seven rows have landed (docs keep-both + yaml after #1429).
- **Q-SUBJECT79 / Q-FIXPREFIX:** declared squash subject `KS-1402: originate resolves a transfer-custody holder email itself` (66, key first, no `fix(` form). The gate may propose another with its reason.
- **Q-DOCSMERGE:** stands. The merge seat does the keep-both and re-runs ks1402 / ks739 / ks697 and `check:openapi` on the merge result.
- **Q-CI79:** a GO may stand with "CI owed on the merge-in push; the merge seat lands only after it classifies".
- **Q-TENANT79 (D-1 / D-2):** the gate MEASURES what it can from code (tenant-context.ts's fallback, the RLS policies and the role originate reads `users` as), RULES severity and says plainly whether it BLOCKS. No live / DB measurement in this gate; what needs a database is named UNMEASURED.
- **Q-DEPLOYKEY79 (D-10):** deploy templates only, never a real `.env`; name the precondition. Deploy is out of scope.
- **Q-CLASS79 (D-8):** report only, with a recommended ticket; Wednesday routes it.
- **Q-MODEL79:** Wednesday types `/model claude-opus-5-5` at the gate's idle prompt.
- **Q-DOCKER79:** no Docker; the four platform suites NOT RUN.
- **Q-DISCLOSE79:** noted.
