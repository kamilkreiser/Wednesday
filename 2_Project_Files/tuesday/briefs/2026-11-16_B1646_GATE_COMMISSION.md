# B1646 G2 gate commission (Tuesday s284, 2026-11-16) — gate for B1642 (MPS lane M-E2, MPSCALC-409)

RE-COMMISSION from this file if `2026-11-16_B1646_verify/VERDICT.md` is absent at the next boot (an in-session gate dies with the seat).

You are an independent QA gate (tier G2, Sonnet; routing row G2, `fleet/specs/model-routing.md:109`) for Tuesday, the Datasec coordinator seat. Read WHOLE first and follow:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md`
(its Output folder pattern is replaced by `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1646_verify/`; use `B1646` wherever the standard says `<Bnnnn>`).

- **Project:** MPS Calculator, `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`, repo `datasecau/MPS-Commercial-Calculator`, `GH_CONFIG_DIR=<P>/4_Credentials/.gh-config`, landing head-pinned SQUASH.
- **KIT:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1642_SEAT-M153_mps-lane-me2-dialog-box-390.md` (its FACT 3 and FACT 4: the dialog is a flex-end item, so a widening runs off the LEFT edge; the row checks BOTH edges, Tuesday's Q1).
- **READY sha:** `3669403445736ba0d4c7e1a9e91d2619df3b0b7f` on branch `b1642/mps-lane-me2-dialog-own-box-390px`; base `56bfe232cbf4c98a9752f949f1f279d755565750`. **MPS main may move under you:** PR #206 (`tests/MpsCalc.Api.Tests/FleetLineIdTests.cs`) is in hosted CI and branch b1641 (`web/src/api/stub/**`, the stub your spec runs against) is at its gate. Re-read main before writing VERDICT.md; run your merge against the main you read and say which.
- **Builder STATUS:** `<P>/1_Project_Definition/Briefs/2026-11-16_B1642_STATUS.md` (91 lines). Claims are claims: one file `web/e2e/dashboard-390.spec.ts` 55 -> 89 lines, 0 removed; the file alone in the stub step 7 passed; mE1 (`web/src/styles.css:124` `min-width: 600px;`) the new row red with `dialog left -210 right 390 vs clientWidth 390`, control green; mE2 (control `minWidth` 390px) the control red; stub `--list` 275 -> 277, api-off 157 -> 157. **It did NOT run the whole stub step or the whole api-off step as a baseline (only `--list`): you run both whole.**
- **Rule on:**
  1. The diff at merge is exactly that one spec file, 0 removed lines (your own program, planted control).
  2. The predicate checks BOTH edges (`left < 0` or `right > clientWidth`), the message prints left, right and clientWidth, and the control plants `style.minWidth = '600px'`; in YOUR copy mE1 turns the new row red and leaves the control green; mE2 turns the control red. Also try a right-edge-only plant (width 600px, flex-shrink 0, backdrop flex-start) and say whether the row catches it.
  3. Both Playwright steps WHOLE as CI runs them, at main and at the merge: stub = main + 2, api-off equal. Browser web server on port **9975** only (`lsof` first; kill by pid only; print `lsof -nP -iTCP:9975 -sTCP:LISTEN | wc -l` = 0 after every run; never wrap a browser run in `timeout`). Whole web vitest (the `pdftotextTimeout` scanner reads e2e specs), eslint, `tsc -b`.
  4. The CodeQL CLI javascript pack over the spec (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/codeql/codeql/codeql`, database in your work folder): 0 new results vs main.
  5. The PR texts as the standard says (no seat names, B-numbers or lane names; squash body with the repo's usual Co-Authored-By trailer: read two recent squashes on main).
- Node: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/node24/bin` first on PATH, read-only.
- **Heavy work:** start a heavy run only when `uptime` load1 < 24 on two reads 120 s apart, one heavy job at a time; you take NO lock in the MPS project folder (read-only to you; say so). Other gates live in Tuesday's session: B1644 (MPS, port 9974), B1645 (HPSM); NexusAI N138.
- **Fences:** as the standard. Nothing pushed, no PR, no merge, no Jira, no mail, no board, no `az`, no hosted HTTP (npm from the machine cache: `npm ci --prefer-offline`; name any registry fetch). Write only in the verify folder and `/private/tmp/b1646-gate/`. Never write in the MPS project folder. Never `cd`. Never delete: quarantine.
- **Final reply:** the verdict line and the file list.
