From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to your kit B1440 (SEAT-H150): the fix round after gate B1440 = NO GO, **round 1 of 2** (the next NO GO is the cap and goes to the product owner). Every rule of your kit still binds you. HARD STOP stays 15:30 AEDT.

## Read whole first
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1440_verify/VERDICT.md` and its `evidence/t07_head_failure.txt`, `evidence/e2e_summary.txt`. Its claims are claims: re-run them.

## The Blocker (HPSMPOC-417) — fix it
`web/e2e/html-layout.spec.ts:149` (T07, "the Admin header at 768 px ...", L4's file: never edit it) is GREEN at main and RED at your head in shards `journey-and-prototype` and `prototype-tablet-1`. Per the gate: the logo link now carries `min-h-11`, so T07's selector `header a.min-h-11` matches it, and the link's `font-bold` reads weight 700 where T07 expects 600.
- Fix in `web/src/components/shell/AppShell.tsx` (around `:172`; re-print it): give the logo link its 44 px box **without** the `min-h-11` class (for example an arbitrary-value height or vertical padding that yields the same box; your choice, proven), so no existing selector that targets `a.min-h-11` in the header picks the logo. Keep: link box at least 44 px at all seven widths, image classes `h-7 sm:h-10` untouched, header height unchanged per width (the gate's `measure417_*.tsv` are the baseline).
- Then run BOTH shards WHOLE (`node scripts/e2e.mjs --shard <name>` for `journey-and-prototype` and `prototype-tablet-1`) at main and at your head, plus the five specs your kit named, and `AppShell.logoLink.test.tsx`. Counts side by side. Also grep every e2e spec and test for selectors on header link classes you now use (`/usr/bin/grep -rn -i` over `web/e2e` and `web/src`), and say none collides.

## The two Minors on HPSMPOC-324's mock (fix if inside your files; say so either way)
1. The mock's refusal carries no "name is blank." message (as at main). If the mock's problem shape has a message field the API fills, fill it with exactly `name is blank.` (the API's words, `CustomerEndpoints.cs`, B1441's branch). No other words.
2. The gate's code-point sweep (`evidence/sweep_diff.txt`) found 39 Unicode 17 marks the mock refuses as blank that the API classifier accepts. Make the mock refuse **exactly** what the API refuses: derive the mock's set from the same code-point list as the API's `VisibleText.IsInvisible` on branch `b1441/hpsmpoc-api-hidden-characters` @ 792c78f2 (read it with `gh api -X GET`, raw), and re-run the gate's sweep idea yourself: 0 code points differ (control: a planted difference reads 1). If the API branch is not landed when you push, say in STATUS that the mock is aligned to that branch's list at 792c78f2.

## Not in scope (recorded for a ticket, do NOT fix)
Other surfaces where Demo still sees stored names (the gate's crawl: Home's pipeline table `PartnerDashboard.tsx:163`, customer lists, /engagements, documents, /profile for API customers, firmware-risk, the snapshot launcher, URL slugs). List them under `## FOR THE RECORDS SEAT` with file:line; change nothing.

## Prove it, under `## ADDENDUM-1` in STATUS
Red-first where a test is new; the two shards whole, main vs head; unit counts; lint, typecheck, build rc 0; one plain-ASCII forward commit per change (no amend), pushed to `b1440/hpsmpoc-web-ui-rulings`.

**Last line:** `READY B1440-2: <head sha40>` (equal to `git ls-remote`), or `STOPPED: NEEDS TUESDAY <one question>`.
