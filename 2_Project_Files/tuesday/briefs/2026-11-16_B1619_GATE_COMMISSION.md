# B1619 G2 gate commission (Tuesday s283, 2026-11-16) — gate for B1617 (MPS lane M-S)

RE-COMMISSION from this file if `2026-11-16_B1619_verify/VERDICT.md` is absent at the next boot (an in-session gate dies with the seat).

You are an independent QA gate (tier G2, Sonnet; routing row G2, `fleet/specs/model-routing.md:109`) for Tuesday, the Datasec coordinator seat. Read WHOLE first and follow:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md`
(its Output folder pattern is replaced here by `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1619_verify/`; use `B1619` wherever the standard says `<Bnnnn>`).

- **Project:** MPS Calculator, folder `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`, repo `datasecau/MPS-Commercial-Calculator`, `GH_CONFIG_DIR=<P>/4_Credentials/.gh-config`. Landing form: head-pinned SQUASH.
- **KIT:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1617_SEAT-M145_mps-lane-ms-stub-duplicate-and-update-pins.md` (tickets MPSCALC-404, MPSCALC-405; OWNS `web/src/api/stub/**` only).
- **READY sha:** `3bcdd21cf9c10067d88687b41ed371daa7b578c0` on branch `b1617/mps-lane-ms-stub-duplicate-and-update-pins`; BASE = MPS main `5e80009525138879031c4b07a18436242dadf46c` (the builder's read at 15:16 AEDT; 0 open PRs then). Re-read main before writing VERDICT.md.
- **Builder STATUS:** `<P>/1_Project_Definition/Briefs/2026-11-16_B1617_STATUS.md` (180 lines). Its claims are claims: 1580 -> 1610 tests, 0 lost; 7 + 3 mutants killed; Part B red under the stored-draft answer; files exactly `web/src/api/stub/purchaseQuotes.ts` and `web/src/api/stub/stubApi.test.ts`.
- **Tier G2** (dev stub + tests only, no product code, no words, no migration). Rule on: every PART A/B/C row against the tickets; red-without-the-fix for each new row (in your copy); the whole web suite, eslint, `tsc -b` at main, head and merge, compared by program (names lost/added); **`npx playwright test` in BOTH modes the CI workflow runs** (read `.github/workflows/ci.yml` at the head for the modes and the node version; CI uses node 24, the box has 26 — say which you ran); the entra build + bundle check; CodeQL CLI javascript pack over the merge (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/codeql/codeql/codeql`, database in your own work folder). Grade the builder's FOR TUESDAY items 1-5 as observations only (each true / false / not shown); they are NOT this lane's scope and are not findings against it unless the diff makes one worse.
- **Heavy work:** start a heavy run (whole suite, playwright, CodeQL) only when `uptime` load1 < 7 (wait up to 15 min, record each read); other seats are live on this machine (HPSM H173, NexusAI N137). If you start any server, read the kit for MPS's port block and `lsof` first; kill by pid only.
- **Fences:** as the standard. Nothing pushed, no PR, no merge, no Jira, no mail, no board, no `az`, no hosted HTTP. Write only in the verify folder and your session scratchpad (or `/private/tmp/b1619-gate/`). Never write in the MPS project folder.
- **Final reply:** the verdict line and the file list.
