# B1644 G2 gate commission (Tuesday s284, 2026-11-16) — gate for B1641 (MPS lane M-S2, MPSCALC-408)

RE-COMMISSION from this file if `2026-11-16_B1644_verify/VERDICT.md` is absent at the next boot (an in-session gate dies with the seat).

You are an independent QA gate (tier G2, Sonnet; routing row G2, `fleet/specs/model-routing.md:109`) for Tuesday, the Datasec coordinator seat. Read WHOLE first and follow:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md`
(its Output folder pattern is replaced by `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1644_verify/`; use `B1644` wherever the standard says `<Bnnnn>`).

- **Project:** MPS Calculator, `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`, repo `datasecau/MPS-Commercial-Calculator`, `GH_CONFIG_DIR=<P>/4_Credentials/.gh-config`, landing head-pinned SQUASH.
- **KIT:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1641_SEAT-M152_mps-lane-ms2-stub-followups.md`.
- **READY sha:** `c5279894be4b6f0a48115073c5977f17c571f416` on branch `b1641/mps-lane-ms2-stub-followups` (2 commits: Part A `e2b7930e` rows only, Part B the three shared titles + one comparing row); base `56bfe232cbf4c98a9752f949f1f279d755565750` = MPS main at 22:2x (re-read before VERDICT.md; sibling branches b1640 (`tests/MpsCalc.Api.Tests/FleetLineIdTests.cs`) and b1642 (`web/e2e/dashboard-390.spec.ts`) exist or may: confirm 0 shared paths; note b1642's spec runs against this stub).
- **Builder STATUS:** `<P>/1_Project_Definition/Briefs/2026-11-16_B1641_STATUS.md` (126 lines). Claims are claims: whole web 1610 -> 1613 -> 1616, 0 failed; Part A mutants mA1-mA5 and Part B mB1-mB5 as predicted; entra build + check-bundle rc 0 at head. Its RESIDUE discloses an `rm -f` that matched nothing (rule slip, nothing deleted) and an npm audit POST at `npm ci`.
- **Rule on:**
  1. Paths at the merge: only `web/src/api/stub/stubApi.test.ts` and `web/src/api/stub/purchaseQuotes.ts`. Part A removes 0 lines; Part B removes exactly the seven literal-bearing lines, each rewritten with a constant (your own program over `git diff -U0`).
  2. **The three titles are moved VERBATIM** (byte-compare each constant's text to the literal at base; a changed character is a Blocker): no new word, code, status or refusal reaches any caller; the fourth text ("Editing a draft needs the Seller role. (stub)") untouched.
  3. Red-without-the-fix in YOUR copy: at least mA1 (`c < 31`), mA3 (`c <= 158`), mA5 (`target !== undefined`) and mB1 / mB4 from the kit; each turns exactly the predicted rows red; undo and prove.
  4. The null row is not vacuous (it asserts the stored JSON holds `"targetGrossMargin":null` before the Duplicate).
  5. Whole web at main and at the merge: `npx vitest run` (lost 0 names by program, `LC_ALL=C comm`), `npx eslint .`, `npx tsc -b`; the entra build + `node scripts/check-bundle.mjs dist`; **both Playwright steps (stub and api-off) WHOLE as CI runs them, at main and at the merge: counts EQUAL** (this lane changes no stub answer). Browser web server on port **9974** only (`lsof` first; kill by pid only; print `lsof -nP -iTCP:9974 -sTCP:LISTEN | wc -l` = 0 after every run; never wrap a browser run in `timeout`). Node `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/node24/bin` first on PATH, read-only.
  6. The CodeQL CLI javascript pack over the two files (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/codeql/codeql/codeql`, database in your work folder): 0 new results vs main.
  7. The PR texts as the standard says (no seat names, B-numbers or lane names; squash body with the repo's usual Co-Authored-By trailer: read two recent squashes on main).
- **Heavy work:** start a heavy run only when `uptime` load1 < 24 on two reads 120 s apart, one heavy job of yours at a time (you take NO lock in the MPS project folder: it is read-only to you; say so). Other seats live: MPS M153 (port 9971), HPSM H176, NexusAI N138, gate B1643 in Tuesday's session.
- **Fences:** as the standard. Nothing pushed, no PR, no merge, no Jira, no mail, no board, no `az`, no hosted HTTP (npm from the machine cache: `npm ci --prefer-offline`; name any registry fetch). Write only in the verify folder and `/private/tmp/b1644-gate/`. Never write in the MPS project folder. Never delete: quarantine.
- **Final reply:** the verdict line and the file list.
