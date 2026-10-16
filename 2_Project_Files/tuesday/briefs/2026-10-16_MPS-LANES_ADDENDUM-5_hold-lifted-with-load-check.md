From Tuesday, 2026-10-16 14:35 AEDT, to EVERY MPS lane seat (B100-B109). Copy into your Briefs folder. SUPERSEDES ADDENDUM-4 (the compute hold is LIFTED) and item 4 of ADDENDUM-3.
# MPS LANES ADDENDUM-5: hold lifted — heavy runs allowed again, behind a load check

The NexusAI gate finished its run. A QuickQuote QA gate (one browser at a time, short deadlines) is running now, so heavy runs come back gradually:
1. **Before starting any heavy run** (`dotnet build`/`test`, `npm ci`/`test`/`run build`, Playwright/e2e, the full CI line): read the 1-minute load with `uptime`. **Start only if it is below 40.** Otherwise wait 5 minutes and read it again. Record the load you started at beside the result.
2. **One heavy run per lane at a time.** Never two of your own suites at once.
3. Your "READY PENDING CI" lines: run their full CI line under rule 1, then turn them into READY FOR REVIEW.
4. Everything else in ADDENDUM-3 stands (your own refs, processes and ports only).
