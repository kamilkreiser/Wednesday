# B395 drafter report (2026-10-21 09:52-09:55 AEDT, clock from `date`)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B395_SEAT-G21_hpsmpoc-pr172-gate-tier2.md` (39 lines, long paragraphs; two slots `@STAMP_TIME@`, `@LAUNCH_AUTH@` counted 1 each by `grep -o -E '@[A-Z_]+@' | uniq -c`; last line `READ-WHOLE-BY-TUESDAY: PENDING`).
Read whole before drafting: B392, B389, B390 STATUS (97 lines), B390 brief (72 lines), `model-routing.md:109`.

## Measurements (read verbs; scratch parse files in the session scratchpad `.../scratchpad/b395/`)
- `git --no-optional-locks -C '.../HPSM-POC/2_Project_Files' ls-remote origin refs/heads/main refs/pull/172/head ...`: main `d76200d8c78ff9b586510031169c584197d76d89`; `refs/pull/172/head` and `refs/heads/b390/vite-advisory-ghsa-587h` both `2e02b6afdb5143a16431081d9fb78ed475e2395e`; #170 `b5ea627e`; no `b395*`.
- `gh api repos/datasecau/HPSM-POC/pulls/172`: open, draft false, `mergeable_state` blocked, commits 1, changed_files 1, +80/-80, base shown `d76200d8`. `compare 54fbceac...d76200d8`: ahead 1, behind 0, files = `FeedbackModule.cs`, `Feedback/README.md`, `Hpsmpoc226N9ExportTests.cs` (api only). `gh api repos/.../pulls`: open = #172, #171, #170, #169 (#168 is merged).
- Lock parse (Python `-I`, `main.lock.json` at `d76200d8` vs `head.lock.json` at `2e02b6af`, fetched with `gh api -H 'Accept: application/vnd.github.raw' contents/...`): 20 changed keys, 0 added, 0 removed, non-`packages` top level equal. All 20 equal the builder's table. **dev flag: 19 dev, `node_modules/nanoid` NOT dev** (dependents: `next/node_modules/postcss` 8.5.23 non-dev, and top-level postcss dev). Top-level `postcss` 8.5.31 is dev: dependents `@tailwindcss/postcss` (dev), `vite ^8.5.29` (dev); next's postcss is the nested 8.5.23 (unchanged).
- Registry packuments by `curl https://registry.npmjs.org/<pkg>` (not `npm view`; no npm was run): publish times vite 8.3.4 10-08, rolldown 1.2.14 10-14 (6 days, B390 said 7), @oxc-project/types 0.154.0 10-13 (7 days), postcss 8.5.31 10-18 (2 days), nanoid 3.3.20 10-05 (15 days). postcss 8.5.29 10-05, 8.5.30 10-12 (8 days) are inside vite 8.3.4's `^8.5.29`, so a >=7-day pin exists (8.5.30). vite 8.3.4 deps: `postcss ^8.5.29, rolldown ~1.2.12, picomatch ^4.0.7, tinyglobby ^0.2.17, lightningcss ^1.33.0`. First 30 chars of integrity and the tarball URL of vite, postcss, nanoid equal the lock; rolldown, @oxc and the 15 bindings were NOT compared (gate does all 20 in full).
- Check-runs at the head (09:52): `CodeQL` completed **neutral**; Analyze python and actions success; javascript-typescript and csharp in_progress; dependency review and gitleaks success; web build, web unit tests, api, both SQL Server shards, Bicep in_progress. Open alerts `refs/pull/172/head` 0, `refs/heads/main` 0 (the control returns 0 too, so it is not a discriminating control; the brief asks for a count, not a non-zero).
- `ci.yml` at main: step 5 `:374` and step 6 `:380` confirmed; `npm run build` = `node scripts/build.mjs` (web/package.json scripts). Whether `build.mjs` or `next.config` touches vite/rolldown was NOT read (left to the gate).
- #170 lock hunks (`gh api pulls/170/files`): `@@ -12,7`, `@@ -5989,6`, `@@ -8296,13` as in the brief. B390's own 25-hunk positions are RELAYED only; the merge was not run.
- `uptime` 09:52: load `8.44 10.50 11.44`.

## What changed versus your instruction
- You expected postcss might be a runtime entry; it is not (top-level postcss is dev-only). The runtime entry is **nanoid** (15 days old, so no Minor). The brief states the postcss rule as conditional and adds the nanoid runtime question plus the standalone-package check.
- `CodeQL` neutral at the head is new; the brief asks the gate to explain it against main.

## Questions (recommended answers)
1. Whole web suite in a tier-2 gate? Recommend yes (CI's web build and vitest are pending, 1828 tests, the toolchain moved); the brief asks for it behind the load rule, `next build` last and optional. Say no if the load stays over 8 and you want the verdict sooner.
2. Launch now with the `(CI pending: ...)` suffix? Recommend yes, as B389/B392.
3. Landing order: B390/#172 before #170 forward-merges main (B390 FOR TUESDAY 6). Recommend confirm; the brief only repeats it.
4. Stamp slots left for you: `@STAMP_TIME@` (stamp time line, like "stamped by Tuesday at <time> AEDT (...)") and `@LAUNCH_AUTH@` (authority text, same wording as B390: Kam's 2026-10-16 grant + terminal words 2026-10-21 ~07:2x + 2026-09-01 three-hop gate rule tiered 2026-09-05); the brief's Stamp paragraph ends with the slot, so end your fill with a full stop.

## Not done
No npm, node, vitest, merge-tree, Jira, or HTTP to any hosted site. No file other than the two named was written (scratch files under the session scratchpad only).
