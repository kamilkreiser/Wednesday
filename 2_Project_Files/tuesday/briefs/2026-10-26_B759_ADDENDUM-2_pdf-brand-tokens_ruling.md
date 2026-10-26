From Tuesday, Datasec / HPSM-POC, to seat Datasec/HPSM-POC-H38 (brief B759). ADDENDUM-2. It widens your lane by ONE more file, because of ADDENDUM-1. Everything else in your brief and ADDENDUM-1 stands.

**Why (measured by Tuesday at the base `1e3ea8a9`, by `gh api` raw reads):** `api/tests/HpsmPoc.Modules.Reporting.Tests/Integration/IntegrationTests.cs:102` (`Brand_tokens_match_the_design_system_files`) reads `web/src/styles/tokens.css` + `brand.css` and asserts every value in `api/src/HpsmPoc.Modules.Reporting/Pdf/BrandTokens.cs` equals the CSS. That file holds `["--brand-primary"] = "#1d4f91"` and `["--brand-accent"] = "#0f766e"`, and its own comment says "when brand.css changes, this file follows". So ADDENDUM-1's brand.css change turns that API row RED and leaves the PDF reports in the old colours. This is Tuesday's miss in ADDENDUM-1, not yours.

**Your lane gains exactly: `api/src/HpsmPoc.Modules.Reporting/Pdf/BrandTokens.cs`.** Change ONLY:
- `["--brand-primary"] = "#1d4f91"` -> `"#024ad8"`
- `["--brand-accent"] = "#0f766e"` -> `"#356373"`
- in the summary comment, the sentence "Branding is UNDECIDED (QA-027, U6): when brand.css changes, this file follows." becomes a plain sentence saying the brand colours follow the HP brand palette and this file still follows brand.css. No other line changes. No id, no name.
Every other entry of the dictionary stays byte-equal (they are neutral tokens.css values ADDENDUM-1 did not touch).

**Tests:** run `Brand_tokens_match_the_design_system_files` RED at your fix tree BEFORE this edit (brand.css changed, BrandTokens.cs not: name the failing assertion) and GREEN after; then the whole `HpsmPoc.Modules.Reporting.Tests` project green (use the project's `.tools/dotnet` as brief_seat.sh puts it on PATH; record `dotnet --version`). Add mutant m11: `--brand-primary` back to `#1d4f91` in BrandTokens.cs only -> that row RED. The SQL Server shard is not needed for this row (it reads files), say so with the row's own code as evidence. Heavy job rules unchanged (your heavy.lock, load below 7).

**Property check (THE WORK 10):** your path list may now hold this ONE `api/` path; class it "(e) PDF brand tokens that must follow brand.css (ADDENDUM-2)". Any other `api/` path is still a STOP. `infra/**`, `.github/**` unchanged.

**READY line:** add `| pdf tokens follow brand.css: row red before, green after | Reporting.Tests <passed>/<failed>`. The deploy is Tuesday's later decision (web-only or full); you report only.

**Order and clock:** do it right after the brand.css change. Clock unchanged (target READY 23:30, hard stop 01:30; the 23:00 clock rule stands).

Record this addendum under Corrections (one line) and continue.
