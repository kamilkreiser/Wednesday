# B589 drafter report (SEAT-M15, MPS lane M1 part 1, Sonnet builder, row C2, tier 1 gate after)

Drafted 2026-10-24 about 15:20-15:40 AEDT, read-only. Brief: `2026-10-24_B589_SEAT-M15_mps-m1-docs-and-refusal-order.md` (122 lines; 8 lines carry the four-underscore pattern, lines 101-107 and 122; non-ASCII bytes 0 by `python3 -I`) plus a byte-identical `.pre-stamp` (`cmp` identical, count 8 in both; sha256 of the brief `2d43dc9aa7314171f72c3fb3c1598378b058213f55825bbc40eb1c937fcf16a4`).

## Reads (how)
- Sweep `0_Brain/projects_index/2026-10-24_datasec-completable-tickets-1500.md` (whole): lane M1 table (lines 29-41) and lane M2 table.
- Template B585 brief (whole, 116 lines) and its drafter report; B583 brief (grep of its lines 29, 64-85 and the ruling table rows 69-80) for the C-number plan and landing order.
- Jira GET (credentials by name, in-process, never printed): MPSCALC-316, -290, -204 whole with comments (all Backlog, 0 comments); MPSCALC-322, -325, -169, -176 whole (for the NOT YOURS list). Every call was a key GET.
- `decision_queue.sh show <exact id>` for the two rulings (the script lives at `2_Project_Files/tools/decision_queue.sh`, not under `tuesday/tools/`; no `list` call): both `ruled`, answer a, 2026-10-24 11:53.
- Code and docs at main `05c598f3...` via `gh api -X GET contents?ref=` (raw), saved to the drafter's scratchpad and counted there (controls `zzz-no-such-string-7f3a` = 0): `docs/API.md`, `docs/api/openapi.json`, `QuoteEndpoints.cs` (excerpts 60-80, 119-175, 210-235, 495-535, 1440-1545), `PurchaseValidation.cs` (125-235 and a whole-file count of `below 0` = 0), `web/scripts/sync-contract.mjs`, `web/package.json`, `contract.test.ts`, the three generated files, `ci.yml` (grep), five Api test files (grep), the recursive tree (717 paths), `gh api commits?path=` for the contract files.
- `ls-remote origin refs/heads/main` = `05c598f3cd8eb4d36f10e31d9a4effa013d4a717`; `matching-refs/heads/b` (no `b589`); `pulls?state=open --jq length` = 0 (quoted URL); `tmux list-panes` (no `MPS-M15`); `lsof` 9390-9399 (nothing, rc 1); `ls .tools` (`b585` and `wt-b585-*` exist, no `b589*`, `heavy-slot-1` exists and is another seat's); `uptime` (load1 5.62 at 15:23).

## Findings that shaped the brief
1. **-290 is probably already met in `docs/API.md`.** Line 263 (the unchanged-save bullet) already carries the restricted-caller exception (PR #98 commit `4c593517`, 2026-10-23, after the ticket of 2026-10-20). The OpenAPI PATCH-draft description (line 218) still says "a draft saved back unchanged is not a change" with no exception. The brief therefore makes -290 "one OpenAPI clause built only from the API.md words, or no commit", and flags the clause for the words gate (the ticket says new words go there before any deploy).
2. **-316 wording is in different places than the ticket says.** `docs/API.md:425` holds `at most 100 characters` twice (body clause and cut clause); the OpenAPI text at `:369` says `stays within 100 characters` (not "at most"). The ruled sentence goes into all three. The OpenAPI `maxLength: 100` (lines 849, 897) counts characters under JSON Schema: a gap the ruling does not cover, listed FOR TUESDAY. The user-facing sentence `quoteRef is at most 100 characters and customer at most 200.` at `QuoteEndpoints.cs:1418` is left alone (the ruling says no code change), also FOR TUESDAY.
3. **The generated web copy rule is read, not guessed.** The snapshot is byte-equal to `docs/api/openapi.json` at main (`cmp` rc 0; sha256 in `SOURCE.txt`); `sync-contract.mjs` is the only writer; `contract.test.ts` pins the sha; the last six commits that changed the contract each changed the snapshot. So any OpenAPI byte change is followed by a regeneration commit by the script, last, from the commit holding the final contract. This needs `npm ci --ignore-scripts` (an extra network allowance, stated in STANDING LINE 3 and 7). If the final head changes no OpenAPI byte, no web path is touched (the brief says so).
4. **-204 touches only `UpdateDraft` and `InRange`.** `Create` has no quote yet; `Duplicate` already finds the source and checks the reader role before `InRange`. In `UpdateDraft` the chain `Validate`, `TaxRateFixed`, `InRange`, `InternalInputs` runs before `store.Find`, `NotOwner` and `NotEditable`. The brief moves only `InRange` (after `NotOwner` and `NotEditable`, before the stale check, to keep today's range-before-stale relation) and records the consequence it creates: a restricted caller's body that is both out of range and carries a hidden internal input now answers 403 `INTERNAL_INPUT_FORBIDDEN` instead of 400. The seat must measure and pin it; moving `InternalInputs` too is a STOP. The duplicate line exists for five fleet fields (`NotNegative` then `Check`); `PurchaseValidation.cs` has none, so it is not in Yours. No existing test row was found that pins the old order (grep of five files; not read whole).
5. **Launch gate by text, not by number.** B583 plans the rulings as C-62 (refusal order) and C-64 (reference length); those are its plan, so the brief makes the seat find the headings by question text, with a control (`### C-56` reads 1 today; root head `83ea99f`, newest heading C-56) and refuse with `STOPPED: NEEDS TUESDAY records not landed (B583)` if either is absent. The sibling table also shows C-61/C-65 are the feedback-triage rulings (ticket 176, part 2, not cited).
6. **Ports 9390-9399.** `lsof` clean; `9390` and `9399` appear in other briefs only as scan statements and range limits, never as an allocation; allocations read: 9300, 9310, 9320, 9330 (B585), 9350, 9380 blocks.

## Decisions I made (Tuesday strikes any at the stamp)
1. Gate tier 1 (Opus): -204 changes refusal status codes. Tier 2 would only fit -316 and -290.
2. Commit order 316, 290, 204, regeneration (the regeneration last so it covers every OpenAPI edit).
3. Reading 2 allows one OpenAPI clause for -290 built from existing API.md words and flagged for the words gate; a seat that cannot build it from those words STOPs with a WORDS-DRAFT.
4. `InRange` placement (reading 3) keeps range before stale-revision, an unruled relation, and pins it.
5. Mutants O1-O8 and rows (a)-(i); no row for the docs tickets (proved by program counts). One mutant line (O2) was reworded after drafting; the final text is in the file.
6. Partition: Yours = `docs/API.md`, `docs/api/openapi.json`, `QuoteEndpoints.cs` (two places), the three generated web files (regeneration commit only), new `QuoteRefusalOrder*.cs` tests. Intersection with B585's YOURS list (ActiveSources.cs, ReferenceStoreDocument.cs, StoreReopen/StoreTierPoolNull/StoreMembersNull/StoreLoadFaultMapping/BodyRefusedLastBranch tests, Import StoreMembersNull) is empty by reading. Seam: B585's last ticket reads `BodyRefused` in `QuoteEndpoints.cs`; the brief forbids any hunk in `BodyRefused`, `QuotedAfter` and `:1418` (a property check).

## What I could not measure (and the brief says so)
No build, test, mutant, probe, npm or fetch. Not measured: counts against the git object itself; whether the local clone holds the base object; the exact lines of `store.Find` and the stale check; any existing row for a body that is both out of range and carries a hidden internal input (tests read by grep, not whole); whether `npm ci` and the script run on this box; the C-numbers; load at launch.

## What the reviewer checks first
1. Decision 3 (a contract clause for -290) and whether to strike -290 to "verify only, report already met".
2. Decision 4 and the internal-input-plus-range status change (403 where 400 answered).
3. The extra `npm ci --ignore-scripts` network allowance for the regeneration commit.
4. Tier 1 for the gate, and the launch condition (B583 `RECORDS COMMITTED`).

## Files written (and nothing else)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B589_SEAT-M15_mps-m1-docs-and-refusal-order.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B589_SEAT-M15_mps-m1-docs-and-refusal-order.md.pre-stamp`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B589_DRAFTER-REPORT.md`
(Scratch only, in the session scratchpad: the fetched copies of the files above and a small Jira GET script.)
