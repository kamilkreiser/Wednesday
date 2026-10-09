# Wednesday's rulings on the gate81 kit (KIT_REPORT.md §6), read WHOLE by the gate seat

Rulings carried from gate80 and the task brief (2026-10-10). Where this file is absent the gate uses the same defaults.

- **X9 / registry exception (carried):** the QA seat MAY run `npm ci` (with `--ignore-scripts`) in `Blockchain/Dev`, exactly as the build seats' S-1 does. **Fallback:** if an install fails, every leg that needs it reads **NOT RUN with the reason**; never a pass.
- **The gate never edits, merges, comments on tickets or messages humans.** It never mails a builder seat. Its work ends at the verdict mail to Wednesday.
- **Verdict per PR, GO or NO GO, at the pinned head.** Four verdicts (#1443, #1444, #1445, #1446). A head that moved is NO GO for that PR pending a re-draft; the other PRs are gated on.
- **MERGE ADDENDUM per GO, LAST in report.md:** one line per PR plus the composition line. The proposed squash subject carries **no `(#n)` suffix arithmetic**: the declared subject is the landed subject byte for byte, at most 92 characters as declared, and TRUE of the diff.
- **Cross-PR composition proof (the new ruling for gate81).**
  - **#1443 and #1446 BOTH edit `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts`** (#1443 at `fail500` ~:25, #1446 inside the 502 catch ~:171, hunks ~145 lines apart). The gate PROVES they compose **in both orders** in a **temp index** of its own clone, **records the tree sha** of each, proves **#1443's `:25` line and #1446's ~`:171` catch survive together**, and runs both new test files on the composed file.
  - **All four append at the SAME base line of the two platform-k HTML docs** (flow `45.` #1443, `46.` #1446, `47.` #1445, `50.` #1444). The gate proves the docs compose **in the merge order #1443 -> #1446 -> #1445 -> #1444 and in at least one other order**, with `html_docs_matrix.test.sh` **0 failed on each composed tree**. A plain textual merge conflicts at that shared line; the keep-both is the merge seat's job and the gate proves it is composable.
- **Pre-existing CI (carried and extended):** `Security Scanning` (KS-1148: `Blockchain/Dev/scripts/audit/audit-locks.mjs` imports undeclared `semver`), `PR Security Gates` (KS-168) and `pr` fail on develop's own push run at `613070f29112`. The gate **verifies that attribution** (line 50, the failed step's log, develop's run, job and step names and signature) and does **not count it against any PR**. A red it cannot classify from the log BLOCKS.
- **Gate notes added by the coordinator (Wednesday, 2026-10-10):**
  - **#1443:** its PR body quotes the ruled expression as "263 bytes"; Seat R 29th measured 262 (cmp with a control) and withdrew 263 in #1446. The gate VERIFIES which. A wording fix, if any, is a **polish** finding, **not a blocker**.
  - **#1446:** carry Seat R 29th's proposed TEST BLOCK line as the live-run note (security service down -> 502 BAD_GATEWAY "Failed to reach security service" + ONE log line "Audit export could not reach the security service (GET /api/admin/audit/export)"; once with the service up, expect 200 and the export). READY: `briefs_staged/2026-10-10_seatR29_READY_1446.txt`.
  - **#1443 / #1446 expression:** it still logs a thrown STRING verbatim and an Error's `.message`. The gate measures what the cells prove, never "no longer leaks". **X4** (`RED KS-1410 X4`) is the cell that tells the ruled expression from `String(err)`.
  - **#1444:** the headline is the 32-probe WIDEN matrix (seat: 5 / 9 / 18 / 0 newly refused / 0 unexpected). Name the measured `../node_modules` gap. Whether Docker builds `USER :root` is **UNMEASURED**.
  - **#1445:** Q-4XX (are the four 4xx `error.message` sites `:85 :208 :211 :213` in KS-1410's scope?) is passed to Wednesday and Kam UNRULED; and no cell exercises a non-Error throw on the route: the gate PROBES it.

Not ruled by Wednesday (the kit's defaults, to be confirmed or re-ruled):

- **Q-SEAT81 (merge seat):** NO DEFAULT. The launch command takes `--seat "Seat X nth"` and derives the four GO strings. Wednesday must name the seat in the launch command.
- **Q-ATTR81:** the `Generated with` line is COUNTED per PR and reported, not ruled (gate77 Q-ATTR77 precedent).
- **Q-DOCKER81:** no Docker; the four platform suites NOT RUN (the prompt says run `docker info` once, quote rc, never start Docker).
- **Q-MODEL81:** the exec line carries no `--model`; Wednesday types `/model claude-opus-5-5` at the gate's idle prompt.
- **Q-CLASS81:** a class sibling or a prediction slip found by the gate is reported only; Wednesday routes it. (Residual `String(err)` / `err.message` sites in other api-gateway routes are class siblings.)
