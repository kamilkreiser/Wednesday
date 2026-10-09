# Wednesday's rulings on the gate80 kit (KIT_REPORT.md §7), read WHOLE by the gate seat

Rulings given to the kit builder on the draft's open questions (2026-10-10). Where this file is absent the gate uses the same defaults.

- **X9 (registry exception):** the QA seat MAY run `npm ci` in the `systemTest/<pkg>` packages and in `Blockchain/Dev`, exactly as the build seats' S-1 does (the kit passes `--ignore-scripts`). **Fallback:** if an install fails, that leg reads **NOT RUN with the reason**; never a pass.
- **Docs composition order:** #1441 (flow `48.`) then #1442 (flow `49.`). The gate ALSO proves the reverse order composes (both orders, `html_docs_matrix` on the composed tree). Renumbering, if develop's tail has moved, is the merge seat's call.
- **The 32-hex id (#1441):** #1441's body says a well-formed non-UUID id "keeps its 200 []". The gate **MEASURES** it with three classes at least: a **32-hex id with no hyphens**, a **UUID**, and a **garbage string** (the kit's probe sends nine, including UPPERCASE, wrong-place hyphens, `0`, and an id that fails the id-format regex). Whether Postgres's `::uuid` cast accepts unhyphenated hex is **UNMEASURED until the gate runs it, and there is no database in this gate**: cite Postgres's documented input forms with the version, or write UNMEASURED. Any wording fix goes **back to the build seat (Seat G 6th) through Wednesday**; the gate never edits.
- **`audit-locks.mjs`:** the real path is `Blockchain/Dev/scripts/audit/audit-locks.mjs`. The gate verifies the KS-1148 attribution by **reading line 50** (at base, each head, and the reference `dce5fdc3c952` if fetched by sha) **and the failed job's step log** on each PR. The kit's `gh_gate80.py audit` is the read half; the log half is `gh_gate80.py actions`.

Not ruled by Wednesday (the kit's defaults, to be confirmed or re-ruled):

- **Q-SEAT80 (merge seat):** NO DEFAULT. The launch command takes `--seat "Seat X nth"` and derives the two GO strings. Wednesday must name the seat in the launch command.
- **Q-ATTR80:** the `Generated with` line is COUNTED per PR and reported, not ruled (gate77 Q-ATTR77 precedent).
- **Q-DOCKER80:** no Docker; the four platform suites NOT RUN (the prompt says run `docker info` once, quote rc, never start Docker).
- **Q-MODEL80:** the exec line carries no `--model`; Wednesday types `/model claude-opus-5-5` at the gate's idle prompt.
- **Q-CLASS80:** a class sibling or a prediction slip found by the gate is reported only; Wednesday routes it.
