STARTABLE: YES - kit complete (101 lines, 13 stamp lines by `grep -c -E '_{4}'` = 12 slots + last line, 0 non-ASCII by `LC_ALL=C grep -c -v -x -E '[ -~]*'`, slots.json 12 keys, no person names, no card ids in the kit). Launch after Tuesday stamps S1-S12; Step 0 must be at or before 00:15 AEDT 2026-11-05 (kit REFUSE).
BLUF: builder kit B1288 / seat H121 (unused: `ls | grep -i -E 'B1288|H121'` printed nothing), Sonnet row C2 (`model-routing.md:92`, id `models_latest.json:23` = claude-sonnet-5-5), ports 9210-9219 (free), ONE forward commit W3 on `b1272/hpsmpoc-visual-round-2` @ `9061c291`. Paths: exactly `api/.../Pdf/BrandTokens.cs` and `web/e2e/mock-rows.spec.ts`. READY at Step 0 + 75 min, HARD STOP + 100, never later than 01:30 AEDT.
ONE FACT TO KNOW FIRST: the API project has NO contrast test. `grep -r -l -i contrast` over `api/src` and `api/tests` (`.cs`, at the gate's tree `.tools/wt-b1280-head`, HEAD `9061c291`) printed nothing. So "re-run the PDF's own contrast rows" cannot be a named test; the kit turns it into (a) the PDF-rendering test projects by name, and (b) the seat's own WCAG ratio for every pair the renderer draws, before and after.
ANOTHER: the new PDF text pairs are lighter, not darker: info `#0872af` on `#e0f4ff` 4.60, warning `#9b6314` on `#fff4da` 4.59, severity high `#b64e3e` on `#fff0eb` 4.56, severity medium 4.59 (python3 -I -B WCAG formula, controls 21.00 / 4.54 reproduced; old pairs 7.31-7.98). All still >= 4.5, but 8 pt PDF text at 4.56-4.60 is a visible lightening for the product owner (see Q-1).

FACTS (instrument; control)
- Heads, 23:31 AEDT, `gh api -X GET` under the project's GH_CONFIG_DIR: branch ref `9061c2917b2291d5cb337f50f77a72ea6ec90935`, main `fc2bc2fc6a57c7a5453d12e4514a5ce43cc5cefc`, open PRs 0 (length of the pulls list). b1204 not re-read (RELAYED from the gate: `a26bee7e...`).
- Gate STATUS read whole (205 lines, two reads: lines 1-159 and 160-205); `residue.md` (9 lines) and `card-input.txt` (9 lines) read whole. Findings B1280-1, -2, -3, -6 are the scope; -4, -5, -7, -8, -9, -10 explicitly out.
- `BrandTokens.cs` at 9061c291 (fetched by `gh api contents?ref=`, 66 lines): `Css` dictionary `:24-51`, 25 keys; `--ds-fg` `:26` = `#172030` while `tokens.css:24` = `#102f45`. The other 10 gate-listed keys (`--ds-border`, info-bg/fg, warning-bg/fg/border, sev-high-bg/fg, sev-medium-bg/fg) differ per the gate; I printed the site-side values (`tokens.css:14,40,42,52,53`: border `#dde9f1`, info `#e0f4ff`/`#0872af`, warning `#fff4da`/`#9b6314`/`#d47f27`, sev-high `#fff0eb`/`#b64e3e`, sev-medium `#fff4da`/`#9b6314`). Note: `--ds-warning-border` site `#d47f27` vs file `#b78a1f`; `--ds-info-border` site `#5b8fc7` = file (equal, not in the 11). I did NOT print the full 25-key diff (the kit makes the seat do it by program, with a control on main's files).
- The test: `IntegrationTests.cs:102` `Brand_tokens_match_the_design_system_files`, assertion `:112`, regex `:132`; it reads `tokens.css` + `brand.css` and compares ALL keys of `Css`. Gate: red at head, green at main (22:50:59 / 22:51:05, `api-sqlite.txt`).
- `mock-rows.spec.ts` at 9061c291 (206 lines): `:24` and `:72` `await page.waitForTimeout(500);`, `:74` `expect(bottom).toBe(673);` (printed with `grep -n`).
- `rows2.cjs` (19 lines) and `rows3.cjs` (24 lines) read as text: rows2 injects 25/45 padding on the ancestor carrying `lg:px-[3.5%]` and reads `scrollHeight`; rows3 injects CSS and reads the content bottom of `main#main`, with a match-count `n` recorded but NOT asserted above 0 before the read (so the seat's instrument must add that positive control; the kit says so).
- Local render path exists: `Reports.Keep` (`Support/Reports.cs:36-42`) writes PDFs when `REPORTING_PDF_OUT` is set; `SampleReportsTests` uses it (`Pdf/SampleReportsTests.cs`). No hosted host needed.
- Ports: `lsof -nP -iTCP:9210-9219 -sTCP:LISTEN | wc -l` = 0 (control: all listeners = 12); word-boundary scan `grep -l -w -E '921[0-9]'` over 123 non-`.pre-` SEAT kits of 11-03 and 11-04: 0 hits (control `975[0-9]`: 7 files). `tmux list-panes -a`: `tuesday`, `fleet-monitor` only.
- `.tools/b1288` absent (`ls -d`: no such file; control `.tools/wt-b1280-head` exists and its HEAD = 9061c291).
- CI api job: `ci.yml:32` (name `api (ASP.NET Core)`), `dotnet build` `:71`, `dotnet test` `:87`; SQL Server legs `ci.yml:166` onward (landing condition, not run).

D-DECISIONS
- D-1 PDF values are written by a program from `tokens.css`/`brand.css` using the test's own regex, printed old/new, with a control on main's files (0 differences). The test is not edited.
- D-2 "PDF contrast rows" = named PDF test projects + the seat's own ratio table over every pair the renderer draws (no such API test exists). A pair under 4.5 is a printed finding; STOP only if the site's own token is the failing one.
- D-3 Before/after render through the repo's `REPORTING_PDF_OUT` mechanism and `SampleReportsTests`; page-1 PNG read by the seat; page count compared (changed count = finding).
- D-4 A24/A30 are corrected only in the seat's own STATUS (`CORRECTED HOLDS (for the PR body)`); B1285's STATUS is not edited. Each is re-measured with an instrument that has a positive control (selector match count > 0).
- D-5 Spec fix: condition waits (fonts ready, no running animations, two frames), the pinned 673 replaced by a property (the injected 17 px side padding must change the bottom; the real state must be stable). Plant: a tile-padding or `--ds-fg` change reds a named row; a fixed sleep re-added is not a plant (x3 green and diff `waitForTimeout` 0 instead).
- D-6 Checks: full CI-order set plus `journey-and-prototype` shard at least (it holds mock-rows per the gate, `B1280_STATUS.md:117`); the four playbook shards if the clock allows (all five were green on this head). The 75-minute READY leaves no room for a second pass; the checkpoint rule cuts the per-route table, never a check.

Q-QUESTIONS FOR TUESDAY (each with a default)
- Q-1 Lighter PDF small text (new pairs 4.56-4.60 vs 7.3-8.0 before). Default: build as decided (the product owner's palette), print the ratios, list it first in the morning report with the revert option you promised.
- Q-2 `--ds-warning-border` becomes `#d47f27` in the PDF (it is used as a border/rule; not a text pair). Default: follow the site for all 25 keys, no exceptions (the test demands it).
- Q-3 The `BrandTokens.cs:18` comment says "at main 19fba6e" (stale). Default: leave it (scope is values only).
- Q-4 Clocks 75 / 100, latest 01:30; Step 0 refused after 00:15. Default as written. If you launch later than 00:15, the seat refuses; widen the REFUSE line before stamping.
- Q-5 Run all five shards or only journey-and-prototype? Default: journey-and-prototype required, the four playbook shards if the clock allows (they cannot change: no `web/src` file changes).
- Q-6 Pane `Datasec/HPSM-POC-H121` assumes no round-2 gate pane named H121; default as launch line.

UNMEASURED
- The full 25-key old/new diff (the seat prints it); the exact set of colour pairs the renderer draws beyond the six `BrandTokens.` lines I saw in `PdfPigReportRenderer.cs` (I printed the first lines of the grep only; sibling renderer files not scanned).
- Whether any PDF golden test pins a colour value (I grepped `PdfReportGoldenTests.cs` for rgb/hex: printed nothing, which is a suspect zero without a control; the seat's whole-project run decides).
- The path of the gate's routes JSON for rows2 (`.tools/b1280/g/` listing not printed); `CustomerShell.tsx` line for `py-4` (my grep used a wrong path; the kit tells the seat to re-print it).
- That no other kit in flight names the two paths for writing (ports scanned, paths not).
- b1204's head (RELAYED, not re-read). Hosted CI, SQL Server legs and CodeQL: landing conditions.

OUTSIDE THE FENCES: none known. Reads: the three named briefs/STATUS/evidence files, `wt-b1280-head` source and `.tools/b1280` scripts (read-only), `gh api -X GET contents/trees` under the project's GH_CONFIG_DIR, model-routing and models_latest, `lsof`/`tmux list-panes`. Scratch files (tree list, fetched sources) are in the session scratchpad only. One shell command used a subshell `cd_none=1` variable name, no `cd`.
