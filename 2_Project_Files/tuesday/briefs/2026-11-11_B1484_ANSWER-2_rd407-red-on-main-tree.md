# B1484 ANSWER-2 (SEAT-N122): rd407-r2 now fails on MAIN's own tree too. Land-prep may go on, under a narrow environment rule; the hosted CI stays the gate

From Tuesday, 2026-11-11 just after 08:49 AEDT, answering your `STOPPED: NEEDS TUESDAY` of 08:49:01. Supersedes ANSWER-1 item 4 ("any red in the re-run: no push") for this one suite only; everything else in ANSWER-1 stands.

**What Tuesday measured (08:49 to 08:51, `gh run list` under the NexusAI GH_CONFIG_DIR):** hosted CI on main `1c6bd644` (#188's merge): Build **success**, Push on main success, npm-audit success, Gitleaks success, Deploy demo skipped. So main's tree passes the full verify on CI's runners today. Your measurement: the same suite fails the same three cells (M2, R1, R3) 3 of 3 on main's tree `5774a71e` on THIS machine at load1 about 3.5, after passing both full runs here before the 05:41 reboot. Reading: an environment change on this machine, not the branch (the branch's own files are `learningManager` and its test; rd407-r2 does not load it). Tuesday is commissioning a separate read-only diagnosis of why.

**The rule for the rest of your chain (rows 4b to 10), narrow on purpose:**
1. A plain or update run whose ONLY failing cells are in `__tests__/rd407-r2-missing-mid-swap.test.js` is **ENVIRONMENT for that run** if, in the SAME lock acquisition, that suite run alone on main's own tree (the previous row's P tree, whose tree equals origin main by W's check; `header-p2` for this row) fails **the same set of cells** (print both cell lists; the sets must be equal; a cell that fails on the branch's tree and not on main's is a STOP).
2. Every other suite must pass; `EADDRINUSE` 0; the measured pair must equal the PREDICTED pair (5522/329 for learning); I1 to I8 hold as written.
3. Under 1 and 2 the push gate is met. Push, and in the `## READY` section write plainly: the rd407-r2 cells that failed, the same cells failing on main's tree in the same acquisition (both lists), the load reads, and "hosted CI on the pull request is the deciding check for this suite". Tuesday merges only on ALL GREEN hosted checks, as the handshake already says.
4. **Any other red, any cell set that differs, or rd407-r2 failing on the branch tree while passing on main's tree: STOP**, as before.
5. For THIS row (learning): your plain run on K `4525a3ad` failed M2, R1, R3, and main's tree failed the same three 3 of 3. If the rest of that plain run passed with 5522/329 and `EADDRINUSE` 0, and I1 to I8 hold, you may push K now with the disclosure above. You do not need to re-run.
6. If Tuesday's diagnosis finds the cause, an ADDENDUM follows; until then this rule binds.

Name this file in ADDENDA READ.
