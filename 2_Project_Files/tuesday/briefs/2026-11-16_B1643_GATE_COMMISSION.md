# B1643 G2 gate commission (Tuesday s284, 2026-11-16) — gate for B1640 (MPS lane M-F, MPSCALC-407 items 1 and 2)

RE-COMMISSION from this file if `2026-11-16_B1643_verify/VERDICT.md` is absent at the next boot (an in-session gate dies with the seat).

You are an independent QA gate (tier G2, Sonnet; routing row G2, `fleet/specs/model-routing.md:109`) for Tuesday, the Datasec coordinator seat. Read WHOLE first and follow:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md`
(its Output folder pattern is replaced by `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1643_verify/`; use `B1643` wherever the standard says `<Bnnnn>`).

- **Project:** MPS Calculator, `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`, repo `datasecau/MPS-Commercial-Calculator`, `GH_CONFIG_DIR=<P>/4_Credentials/.gh-config`, landing head-pinned SQUASH.
- **KIT:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1640_SEAT-M151_mps-lane-mf-fleet-line-id-rows.md` (item 3, the contract words, is OUT by design).
- **READY sha:** `4ac454010fc09b1bc6950bc681562522aa922b8d` on branch `b1640/mps-lane-mf-fleet-line-id-rows`; base `56bfe232cbf4c98a9752f949f1f279d755565750` = MPS main at 22:2x (re-read main before writing VERDICT.md; two sibling MPS lanes, B1641 (`web/src/api/stub/**`) and B1642 (`web/e2e/dashboard-390.spec.ts`), may push branches meanwhile: confirm 0 shared paths).
- **Builder STATUS:** `<P>/1_Project_Definition/Briefs/2026-11-16_B1640_STATUS.md` (101 lines). Its claims are claims: one file `tests/MpsCalc.Api.Tests/FleetLineIdTests.cs` +78 -0; R12 (Theory) red under mA (`src/MpsCalc.Api/Quotes/PriceAudit.cs:250` `Number(x)` -> `Number(o)`), R13 (Fact) red under mB (`src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:1672` `new[] { true, false }` -> `new[] { false }`), every existing row green under each; whole solution at head 743 / 196 / 3663, 0 failed. **Its Toolchain (c) names a second, LOCAL (machine-cache only) restore of the solution: Tuesday accepted it; read the claim that it made no HTTP request.**
- **Rule on:**
  1. The diff at merge with main is exactly that one test file, 0 removed lines; no product, docs or openapi byte (your own program over `git diff -U0`, with a planted control).
  2. Red-without-the-fix by the kit's mutants IN YOUR COPY: mA turns R12 (both cases) red and leaves R1 and every other row green; mB turns R13 red and leaves every existing row of `FleetLineIdTests.cs` and `FleetLineIdStoreTests.cs` green (print counts). Undo each and prove it.
  3. The rows are not vacuous: R12's in-row control (the by-number list through `WithoutIds`) and R13's `SameFleetLine` controls assert what the STATUS says; read them in the file.
  4. Whole solution at the merge: `dotnet build MpsCalc.slnx -c Release` 0 warnings (TreatWarningsAsErrors) and `dotnet test MpsCalc.slnx -c Release --no-build` 0 failed, Api.Tests = main's count + 3. Toolchain: `<P>/.tools/dotnet-10.0.404/` (DOTNET_ROOT and PATH in every command). **Restore:** the machine cache lacks System.Security.Cryptography.Xml 10.0.15; you may make ONE registry restore of that single id through a seat-local nuget.config with `packageSourceMapping` and `--packages` into your own work folder (the form the builder used), and local-cache restores of the other projects; name every request. Never the user's global cache.
  5. C# CodeQL cannot extract on this arm64 box: say NOT RUN; hosted CodeQL is the proof.
  6. The PR texts as the standard says (no seat names, B-numbers or lane names; squash body with the repo's usual Co-Authored-By trailer: read two recent squashes on main).
- **Heavy work:** start a heavy run only when `uptime` load1 < 24 on two reads 120 s apart, one heavy job of yours at a time (you take NO lock in the MPS project folder: it is read-only to you; say so). Other seats live: MPS M152, M153, HPSM H176, NexusAI N138.
- **Fences:** as the standard. Nothing pushed, no PR, no merge, no Jira, no mail, no board, no `az`, no hosted HTTP except the one NuGet id. Write only in the verify folder and `/private/tmp/b1643-gate/`. Never write in the MPS project folder. Never delete: quarantine.
- **Final reply:** the verdict line and the file list.
