# Drafter report: B524 (SEAT-G57), MPS Calculator tier-2 QA gate on PR #98 (B517 docs and contract words)

Drafted 2026-10-23 about 12:45-13:00 AEDT (clock `date`) by Tuesday's read-only brief drafter (Sonnet 5.5). Wrote only: the kit, its `.pre-stamp` (made with `cp`, `cmp` equal), and this report. Nothing stamped, launched, sent, published, fetched, built or run in the project; no decision-queue tool, no Artifact/Docs/mail/chat, no HTTP to any app or hosted host, no `az`, no docker, no Jira.

## Files
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B524_SEAT-G57_mps-b517-docs-gate-tier2.md` (102 lines; seat `Datasec/MPS-G57`, model `claude-sonnet-5-5`, tier 2, round 1 of 2, ports 8680-8689 reserved, none needed).
- `.pre-stamp`: the same path plus `.pre-stamp`, byte-identical.

## Slot count
Four-underscore count (`/usr/bin/grep -c -E '_''_''_''_'`): **9 on the kit and on the `.pre-stamp`** = 8 slot lines (STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop, Head/main/check-runs at launch, Model receipt and load1, Pane plus Q-1 answer) plus the last line `READ-WHOLE-BY-TUESDAY: ____`. The kit's Stamp section states "The unstamped copy reads 9 lines". Control: `printf 'x%s\n' <four underscores>` reads 1. Other scans of the kit: non-ASCII bytes 0 (I replaced the middle-dot separators with slashes), at-sign-capitals-at-sign pattern 0, person-name word list (Kam, Kreiser, Kamil, Paul, Friday, Wednesday) 0, no decision-card id, no `mps-...-10nn` shape.

## What I read
- Template: newest MPS tier-2 gate kit, `2026-10-22_B453_SEAT-G3_mps-b450-gate-tier2.md` (105 lines, whole) and its `.pre-stamp` (diffed against the stamped file to see the slot shapes). Today's conventions: `2026-10-23_B523_SEAT-G56_hpsmpoc-b510-gate-tier2.md` (73 lines, whole).
- Subject: builder STATUS `.../Briefs/2026-10-23_B517_STATUS.md` (whole), builder brief `2026-10-23_B517_SEAT-M1_mps-contract-docs.md` (145 lines, whole), drafter report `2026-10-23_B517-B520_DRAFTER-REPORT.md` (whole). The PR diff (`compare e027ebd...b63edd37`, diff media type) read whole.
- Code excerpts at the head by `gh api -X GET contents?ref=<head>` raw: `ci.yml` (job names and commands), `sync-contract.mjs` (whole), `contract.test.ts`, the Api test csproj link line, `PricingPolicy.cs:60-82`, `PurchaseCatalogue.cs:24-52`, `QuoteFigures.cs` excerpts, grep of `ENGINE.md`/`API.md` headings and rows.
- Not opened: `2_Project_Files/.local/`, `Source_Documents`, `.tools/backup-*`, the builder's `.tools/b517*`, `.env`.

## Facts and their sources (all MEASURED by me at 12:47-12:55 AEDT unless marked)
- Head/main/PR: `ls-remote` (main `e027ebd0`, branch = `refs/pull/98/head` = `b63edd37`, `refs/pull/98/merge` `aa8f6011`, b53/b54/b58 heads, no b518/b519/b524 refs); `pulls/98` (open, not draft, 7 files, +43 -26, 2 commits, mergeable true, `blocked`); `pulls/98/files` (per-file numbers match the task); `pulls/98/commits` (two, one parent each); `pulls?state=open` (#98 only); `compare e027ebd...main` identical.
- Check-runs of the head at 12:48: 8 listed, CodeQL neutral, Analyze actions/python success, five in progress (web, dotnet, python, Analyze csharp, Analyze javascript-typescript); `package` not yet present. Code-scanning: 0 open alerts on `refs/pull/98/head`; two analyses (python, actions) so far.
- `rules/branches/main`: deletion, non_fast_forward, code_scanning (CodeQL), required_status_checks with an EMPTY list; `branches/main/protection` 404. This differs from the HPSM-POC kit (which names required contexts), so the kit says not to claim a required CI context.
- `ci.yml` commands (dotnet build Release / test --no-build; web npm ci, lint, test, `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`; node 24).
- `sync-contract.mjs` takes the ref text as typed into the header (`at <ref>`), so the gate must pass the full 40-char sha the committed `SOURCE.txt` shows; the kit says so and adds a short-ref control.
- Heavy slots: slot-1 `B483 23:07 CI line at head` (stale), slot-3 `B518 12:45 216 green run`, slot-2 absent. Panes: `Datasec/MPS-M1`, `-M2`, `-M3` live, no `MPS-G57`. `.tools/b524` and `.tools/qa-b524` absent. load1 11.07/11.23/10.44 at 12:48.
- Ports: `lsof` 8670-8699 empty at 12:48 and 8680-8689 empty at 12:50; python scan of the briefs folder for a `868x` token: one hit, inside a hex sha of an old report (so no brief names that block); 8670-8679 is the HPSM-POC gate G56's block.
- RELAYED (builder STATUS): the baseline and head test counts (Engine 394 / Import 156 / Api 1967; web 126 files / 1191 tests), names lost/added 0, gitleaks rc 0, the empty-array 403 scratch finding, the replaced local commits, the unreferenced commit object. Each is marked RELAYED in the kit.

## Slot / template notes: what did not fit the template
- The B453 kit was a branch-only gate with a widener; this one has no code mutation. I replaced the widener checks with: a JSON-aware openapi diff program (description strings only), a per-sentence claim table S1-S8 against code at main (file:line), and a re-run of the project's own sync script with two controls (different ref changes the output; short ref changes the header). The three-slot Stamp of B453 became eight slots (adds launch window, hard stop, head/main/check-runs, and a Q-1 answer on a scratch xunit row, because the 403 sentences are behaviour claims that the builder measured with its own scratch row).
- B453 had no PR; here a PR exists, so the CI/CodeQL read at the verdict (C6) follows the B523 conventions: check-runs read at the verdict with `CI pending: <names>` rule, CodeQL by instance state with a control that can fail, analyses expected four, and not-scanned-is-not-clean.
- The task wanted "the Api test project that links the contract"; I added C4 (list the tests that read `Contract/openapi.json`, run by full name at base and head) in addition to the whole line in C5.
- ENGINE.md register rows: the diff changes exactly one row (X-31) and one prose paragraph (Currency). The X-31 and X-32 rows' existing text names a person, so the kit tells the gate not to quote it (and the kit itself does not).
- The kit has no person name; I avoided quoting the builder's account handle (the kit says "the project account").
- The task said the 7 files' numbers; I confirmed all seven from `pulls/98/files`.

## Leads recorded in the kit for the gate (drafter reading, not findings)
- `docs/API.md:367` "Until lane V2 fills them no row carries them" is left standing while `QuoteFigures.cs:70-76` fills the staff columns (builder's own "Open"); kit classes it as a finding of FACT / Note.
- The unchanged-save sentence states an empty `manualItems` array is also 403; `PricingPolicy.cs` shows `request.ManualItems is not null` returns the refusal (read at the head), consistent with the claim by reading; kit asks the gate to measure it (Q-1) and treats the behaviour question as not this PR's.
- `PurchaseCatalogue.cs`: the device key uses `"device|" + sku` (unescaped), the other four go through `Join` (backslash replaced first, then the bar): consistent with the new sentence by reading; kit asks for a hash check.
- Squash artefact: `SOURCE.txt` and the `schema.ts` header name commit 1 (a branch commit the squash discards): Note in the kit.

## UNMEASURED
Nothing was built, run or fetched. Not measured by me: any CI leg result beyond the 12:48 in-progress snapshot; whether the generator reproduces the committed bytes; the Api/web test counts; the JSON-aware openapi diff (I read the diff text, which shows three one-line description changes in each of the contract and its snapshot, but did not run a program); the whole-file non-ASCII, person-name and percent scans of the diff; whether `RoundingPolicy.Apply` has no caller and every identifier in the new ENGINE.md paragraph exists; whether the register ids (R-25, R-26, R-28, W-05, X-21, X-23, X-24) name the rules the paragraph says; the inventory supply/care-pack and `?class=` claims; the error-path sentence's per-list forms; the intersection of PR #98's seven paths with the b53, b54, b58 branches (not run; the builder's INTERSECTION section is RELAYED as 0); `refs/pull/98/merge` parents; the CI job logs; load1 at launch; the model id file (`models_latest.json`) was not opened (the model id is as the task gave it).
