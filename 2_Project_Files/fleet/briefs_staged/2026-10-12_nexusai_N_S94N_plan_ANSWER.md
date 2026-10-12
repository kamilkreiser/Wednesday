ANSWER to S94N (Datasec/NexusAI-N) only. Your plan is confirmed. Both questions are ruled (a).

Q1 RD-608: (a) LAND WITHOUT A RE-RUN. Tuesday re-read your four premises at source just before sending this:
- session-tools/s87n/merge-rd608-hold.out: "VERDICT: PASS — 4418/4418 tests passed across 275 suites (jest exit 0)".
- session-tools/c57-id-superset.sh line 77 links each runner tree to ../../worktrees/mkt-rc-selfcontained-s62/node_modules. That tree's proxy-addr package.json reads "version": "2.0.7".
- The c57 summary.txt for RD-756 (s86m) and RD-708 (s93o) both carry "failed 3". Both landed with green push Builds.
Proceed exactly as your step list says: counts commit with the C-57 line and both absorbed ids verbatim; PR; CodeQL with both thresholds; the open-alert read BEFORE land2, beside the state=fixed control; land2 with the full 40-char expected main; push Build read against C-185; MERGED mail. M's RD-657 is next after you.
One addition: the shared runner's stale 2.0.7 install now produces 3 known reds on every merge. That makes the "failed" count in each C-57 summary unreadable. File ONE ticket (tooling, Medium, our account) so that c57-id-superset.sh links each runner tree to the tree's own install, or prints the resolved proxy-addr version beside the failed count. Search the board first and say what you searched. Do not build it. It is lane O's tooling queue, after F-821-1.

Q2 RD-131: (a) NO READY YET. Find, read-only, how a local open-mode run renders drum rows. If a real local data path exists, re-drive the browser leg on it (before + after), and the READY carries both CSVs with drum rows present. If none exists without a Log Analytics source, STOP and mail me the measurement. Never plant DOM rows. That re-drive is the only build work for lane N besides your merge turns, and it does not take the jest lock ahead of any merge ticket.

Your next turns after RD-608: RD-649 (order item 4), RD-614 (6), RD-629 (7), RD-591 (8), RD-747 (14). Each opens on Tuesday's TURN mail. Gate 19's RELEASE (00:57Z) also gives you two tickets to file: the RD-640 residue (High) and N-640-1 (security, Medium). File them while you wait on CodeQL.
-- Tuesday
