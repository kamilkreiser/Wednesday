From Tuesday (Kam's Datasec coordinator seat; Friday handed this project to Tuesday on 2026-10-15). Datasec / MPS Commercial Calculator. Questions to tuesday-agent@agentmail.to; your STATUS file is the wrap.
# BRIEF B98 · SEAT-A: pin System.Security.Cryptography.Pkcs and .Xml past the new advisories so `dotnet` CI passes (it blocks PR #41 and main)

**BLUF.** Tier 2 (dependency pin, no product code). Branch from main, smallest pin, red-first at base, green at your tip. Report `1_Project_Definition/Briefs/2026-10-16_B98_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK). Last line exactly `READY FOR REVIEW: b98/pkcs-xml-pin @ <sha>` (sha from `ls-remote` after your push) or `STOPPED: NEEDS TUESDAY` + ONE question.
**Step 0:** copy this file unchanged into your `1_Project_Definition/Briefs/` (sha256 both equal; this copy is in Tuesday's tree, read-only to you).

## MEASURED BY TUESDAY (2026-10-16 ~12:0x AEDT)
- PR #41 (B97, rental-book word fixes) was re-triggered by Tuesday with an identical-tree empty commit: head `84210f7870b10ee19cdae8ed85dc159f4d914d8d` on `b97/rental-book-word-fixes`. CodeQL + all Analyze jobs, `python`, `web` = success; **`dotnet` = failure** (run 38831974732): restore fails, NU1902/NU1903 warnings-as-errors, `System.Security.Cryptography.Pkcs 10.0.10` (moderate + high) in `src/MpsCalc.Api` and `tests/MpsCalc.Api.Tests`, and `System.Security.Cryptography.Xml 10.0.10` (high) in the tests project. #41 does not touch .NET (its files: web/src/proposal/RentalDocument.tsx, its test, template/rental.ts), so main's next CI will fail the same way.
- Friday's precedent on HPSM-POC (B248, merged as #155): an explicit direct `<PackageReference>` pin with a comment naming the GHSAs and "remove when the parent floors it"; no central package management introduced. HPSM-POC pinned Pkcs **9.0.21** (net9 line); MPS is on the **10.0.x** line, so find the fixed 10.0.x versions from the advisories / NuGet yourself (UNMEASURED by Tuesday).

## DO
1. Read `CLAUDE.md`, `CLARIFICATIONS.md`. Worktree under `2_Project_Files/.tools/wt-b98` from origin main (re-read main by `git --no-optional-locks ls-remote`; the root checkout sits on old `b03/api`: read-only verbs there).
2. Red first: at base, the CI's own restore/vulnerable-package commands (read `.github/workflows/` for the exact lines) show the rows. `dotnet nuget why` for the parent chain; record it.
3. Pin the minimum set of csproj(s) to the fixed 10.0.x versions of BOTH packages; restore clean; `dotnet build -c Release` 0 warnings; the full test suites 0 failed, no lost test names vs base; diff = csproj only (prove with a planted extra path your check catches); gitleaks over the range.
4. Push the branch only. **Tuesday opens the PR and merges once CodeQL and checks are green.** Then #41 needs main's fix: Tuesday handles the rebase/update of #41, not you.

## HOLDS
Never dismiss an alert or bypass a check; never push main; never force-push; no deploy; no Jira/BACKLOG write (B99 owns records); nothing to Paul or any human; never delete (quarantine).

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 12:0x
