# B449 drafter report (read-only drafter, Sonnet), 2026-10-22 12:00-12:10 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B449_SEAT-WP1_mps-word-pack-hosted-f5b6f5a.md` (123 lines; 6 four-underscore lines: 5 stamp slots + last line; MEASURED by grep, stamp section reads 6 too). Shape cloned from B407 (stamp, REFUSE, standing lines, STATUS, last-line formats). Read whole: B407 brief and report, B448 drafter report, the v13 wave-1 register (421 lines), routing rows C2/C8/G2, project CLAUDE.md, B446 brief head.

## Measured (read verbs only)
- main = `f5b6f5a710258a4a36ffbcab92787a2434962500` (ls-remote); both shas local; `e6f92a5f` ancestor rc 0; 142 files, +12,022/-300; 11 first-parent PRs #83-#93 with their ticket keys (#87 and #88 titles carry none).
- Card `mps-hosted-deploy-main-f5b6f5a-1022`: `show` = ruled a, 11:51:21; option a has no words clause.
- `words448.tsv`: 314 lines / 307 distinct (column 3); per PR #83 1, #84 23, #85 73, #86 49, #87 85, #88 35, #89 14, #90 29, #91 4, #93 1. Method: wc and cut|sort -u over the file.
- NEW FINDING: that list undercounts short labels. 7 of 7 register words grepped (`Locked`, `Passed`, `Summary`, `Quote Builder`, `Expand all`, `Outcome`, `Export CSV`) are absent; controls `Ready to Export` and `Not set` found. It also has no openapi.json rows. The brief tells the seat its count will be above 307 for screens; the seat writes its own tokeniser at f5b6f5a7.
- The local `2_Project_Files` working tree is stale (HEAD `7f6ca4c0`, no `web/`); the brief mandates reading objects at the sha only.
- Tools: pandoc present; no soffice, python-docx, reportlab, LaTeX or wkhtmltopdf; Chrome app and `cupsfilter` present. Load1 17.6 at 12:03 (the seat's jobs are light).
- `Deliverables/` does not exist in the project (the seat creates it).

## Routing row proposed
C8 (tooling with arms plus a document, no code), Sonnet, no gate (Tuesday reads and spot-checks). Flag: C8's text says "Agent-tool sub-agent" and this is a brief seat; fallback C2 (pilot). Not C3/C4.

## Open questions for Tuesday (stamp slots)
1. Allow the one headless Chrome print for the PDF (default yes; else cupsfilter plain PDF)? Load is high.
2. Developer-only and dev-stub words in separate tables (default yes) or drop them?
3. Ungraded audience shown to the product owner (default yes).
4. Rule the routing row and gate (none) and confirm 12:30 stamp is feasible against the 13:45 / 14:30 times.
5. B448 will STOP at its words check regardless; consider holding B448 until this pack is ruled, and note CI on f5b6f5a7 is red.
6. Not verified by me: whether the seat's stdlib tokeniser can reach register recall near 100 percent (UNMEASURED); the brief makes recall a reported control, not a pass gate.

READ-WHOLE-BY-TUESDAY: ____
