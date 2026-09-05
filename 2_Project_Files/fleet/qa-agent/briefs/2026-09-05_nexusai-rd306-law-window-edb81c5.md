# QA Agent Invocation Brief — Datasec / NexusAI, RD-306 through-code pass: branch `rd-306-law-window-s34` @ `edb81c5` — the Log Analytics read's two halves (order before take; an undated row stays undated)

**R0 (client isolation):** exactly one client's content — Datasec / NexusAI. Report under `projects/nexusai/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. Context — a side branch, gated on its own, merged later
RD-306 was filed by the RD-296 pass (2026-09-05 09:4x): the LAW (Azure Log Analytics) path of the Sustainability figures discarded the window and sampled `take 10000` BEFORE the sort — an arbitrary sample above the cap — and its parsers defaulted a dateless row to NOW, so undated jobs were counted as today's. S34 built the two independent halves on a NEW branch while holding for an unrelated gate. **This pass is through-code only; nothing renders differently and nothing deploys.** The branch's eventual merge target is the deploy branch `rd-136-nga-defaults-s12` (now at `4e4a630`, under its own fix round by S35) — see the merge-readiness item in scope.

## 1. Target
- **Client / Project:** Datasec / NexusAI. **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files`. **The builder (S35) is LIVE and WORKING in that tree on a different branch (the erasure fix round) — its tree is not clean and not yours.** Work from your own pinned worktree created from your OWN copy; never check out, stash or modify anything in the builder's tree; never touch the dev app (`nexusaidev-app--0000096` serves `a554e52` — observe only), the demo, any workspace, the synthetic feed (RD-118), or `data/.machine-id`.
- **Branch under test:** `rd-306-law-window-s34` at **`edb81c57db826e9e1d5b05f7e2bc185eed4e073c`** — verified at origin by Wednesday at 15:2x AEST (`git ls-remote`). **ONE commit above `32e4dac`** (S33's HISTORY commit) — so its base is BELOW the deploy branch's `a554e52` and `4e4a630` (measured: neither is an ancestor of `edb81c5`; merge-base with both = `32e4dac`). 3 files +296/−9: `backend/azureLogAnalytics.js` (+35/−?), NEW `__tests__/law-window-truncation.test.js` (+264), `scripts/verify-expected-counts.json` (+6/−?).
- **Environment:** LOCAL DEV, SQLite only. **No LAW credentials exist here; the LAW path is READ ONLY and was never queried live by the builder — the strongest available claim is the product's OWN EMITTED QUERY captured at the wire boundary (the axios POST body).** No deploy, no outbound calls.

## 2. The builder's claims at `edb81c5` — inputs to FALSIFY (the commit body, read by Wednesday from the object; S34's READY FOR QA mail 00:42Z as recorded)
1. **Half 1:** `getAllPrinterLogs` emitted `| take N | order by TimeGenerated desc`; `take` is KQL's unordered sampler, so it sorted an ARBITRARY N. Now `order by TimeGenerated desc | take N`, so the cap bites the OLDEST rows. **It was the single outlier in the file: `queryJobActions`, `queryUserAccess`, `queryDeviceErrors` were already correct.**
2. **Half 2:** all four parsers set `created_at: row.TimeGenerated || new Date().toISOString()`; a source row with no time dated itself to the HTTP response's moment, inside whatever window the caller asked for; `rowInWindow` falls back to `created_at` when `Job_Start_Time_UTC` is absent, so such a row was counted in TODAY's figures on every window. Now **explicit `null` at all four sites** — parity with the SQLite path where COALESCE yields NULL. Explicit `null`, not an omitted key: `new Date(undefined)` is Invalid and `server.js:12213`'s bare `.toISOString()` would throw; `new Date(null)` is the epoch — outside "today".
3. **NOT DONE, on the record:** the full KQL predicate on the job timestamp is not attempted — it depends on the API timespan format RD-305 settles (needs one probe against a live workspace). The tab stays HONESTLY TRUNCATED above `SUSTAINABILITY_ROW_CAP` until RD-305 lands; the banner is the disclosure.
4. **Tests assert on the product's OWN EMITTED QUERY captured at the wire boundary**, not on its source text and not against a hand-rolled KQL engine; half 2's consequence is driven end to end through the real parsers and the real row source (16 tests in three `describe`s: half 1 ×4, half 2 ×3, the consequence ×3 + controls).
5. **Red-then-green with the corpus accounted for:** 9 failed / 7 passed / 16 total against the pre-fix backend; the 7 passing in both states are deliberate controls, including two that would catch a reader returning nothing.
6. **Gate: PASS 1593/1593 across 95 suites** (was 1577/94) — `scripts/verify-expected-counts.json` updated by +16/+1.

## 3. Scope
**Charter:** falsify claims 1–6 at `edb81c5`, then hunt what a fix to a query BUILDER and a fix to a row DEFAULT can each do one step further along.

**In scope:**
- **Half 1, all four builders, MEASURED at the wire:** capture the emitted KQL for `getAllPrinterLogs` AND the three the builder says were "already correct" (that is a READ claim — measure it): `order by` before `take` in each; `take` the LAST stage; and with a timespan `where` stage present, the ORDER of `where`/`order by`/`take` (a `where` AFTER `take` filters the sample, which is the RD-306 defect wearing a different stage). State the emitted strings.
- **Half 2, all four parser sites:** enumerate every `created_at` assignment in `azureLogAnalytics.js` at the head (grep with a control) and confirm the fourth is `null`, not one that still defaults; then drive the consequence: an undated row is EXCLUDED from a bounded window, INCLUDED with no window, and a dated row keeps its own date. **Then the step further: what consumes a `null` `created_at` downstream?** `server.js:12213` is the builder's example; enumerate the others (`new Date(row.created_at)`, sorts on `created_at`, the CSV export, the history views) — a consumer that sorts undated rows to the epoch or throws on `null` is a finding with the class named; a consumer that silently counts an epoch-dated row into an "all-time" figure is the RD-306 defect moved, not removed.
- **Red-proof:** re-derive independently — the builder's own 9/7/16 (revert `azureLogAnalytics.js` to `32e4dac` in your copy → predict the failing SET before running → run → compare the set, not the count; confirm all 16 EXECUTED and that the 7 controls include two that would redden on a reader returning nothing — tamper the row source to empty and confirm they do).
- **The gate floor:** `verify-expected-counts.json` moved +16 tests / +1 suite — confirm the delta equals exactly the new file's count and that no OTHER floor was lowered (RD-291's class: a floor far below the real count is a gate that cannot see loss). Run the gate in your copy; number beside 1593/95.
- **Merge-readiness (READ ONLY, in your own worktree):** `git merge-tree` (or a scratch merge on a throwaway branch of YOUR copy) of `edb81c5` onto `4e4a630` — clean, or which of the three files conflict; and whether the deploy branch touched `azureLogAnalytics.js` or the parsers since `32e4dac` (`git log 32e4dac..4e4a630 -- backend/azureLogAnalytics.js`). The branch will be rebased before it merges; this tells Wednesday whether the gate's verdict survives that rebase.
- **RD-305 boundary, stated not tested:** the two consumers of the timespan (`ago()` wants `30d`; the request body wants ISO-8601) — READ which form the head sends and say whether half 1's `where` stage would be well-formed under each; do not probe a workspace.
- **Rendered change:** the builder claims none. Confirm by diff (no UI file, no CSS, zero colour literals). No browser pass required; if you stand a surface anyway, the script is in the NexusAI REPO at `scripts/qa-surface-up.sh`, run from the repo root — never from inside a worktree (re-gate 2's tooling finding).

**Out of scope:** the erasure fix round on the deploy branch (S35's, under its own gates), RD-304/RD-305 (RD-305 is unmeasurable here — say so), the synthetic feed, LAW itself, the demo, the dev app.

## 4–6. Credentials / state / boundary — as before
`.env` only if a stand-up needs it; never echo. Exclude-and-report-only on shared state; own temp dirs; **NEVER `rm`** (quarantine); restore tampers byte-identically with hashes; **predict every tamper's failing SET before running it and compare the set.** **Findings, reports and recommendations ONLY** (Kam 2026-08-11). Evidence class on every action-recommending finding: MEASURED AT RUNTIME / PROBED / READ ONLY.

## 7. Known-fragile / carried
The RD-296 pass's F-2 (a guard that was a source-text matcher) and F-3 (12 fields not 11 — `created_at` omitted from a list, parsers defaulting to NOW) are the ancestors of this ticket: the class returned once already, one file away. A test named for a wire assertion earns the most suspicion — read what its fixture makes reachable. The 09-04 `timeout N cmd | wc -l` trap: capture rc on its own line. `git checkout --` restores from the INDEX — hash, do not assume.

## 8. Logistics
- **Time-box:** narrow — the four builders at the wire, the four parser sites + downstream consumers, the red-proof with the set, the gate floor, merge-readiness.
- **Findings sink:** `projects/nexusai/reports/2026-09-05-s34-rd306-law-window-edb81c5/report.md` + `evidence/`. Claims table (claimed → measured); new findings by severity with evidence class; NOT-TESTED (lead with the LAW path never being queried live).
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] NexusAI RD-306 @ edb81c5 (through-code)` — BLUF (PASS or NO GO in the first line), report path, claims table, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- `edb81c57db826e9e1d5b05f7e2bc185eed4e073c` = `refs/heads/rd-306-law-window-s34` at origin; one commit above `32e4dac`; merge-base with `a554e52` and `4e4a630` = `32e4dac`, neither an ancestor; 3 files +296/−9 | `git ls-remote origin`, `git log --oneline -4`, `git merge-base`, `git merge-base --is-ancestor`, `git show --stat` on the NexusAI repo's local objects — read-only, no fetch, no checkout | read 2026-09-05 15:28
- Claims 1–6 | the commit body of `edb81c5` (`git log -1 --format=%B`) and the test file's `describe`/`test` names (`git show edb81c5:__tests__/law-window-truncation.test.js`) — the builder's own words; S34's READY mail 00:42Z as recorded in Wednesday's daily note (gate 1593/95, red-then-green 9/7/16) | read 2026-09-05 15:28
- RD-306's origin (the RD-296 pass F-1/F-3) | `[QA -> Wednesday] RD-296 …` report 2026-09-05 09:4x as recorded in Wednesday's note; RD-306 on the Jira board (Testing) — Wednesday's project's records | read 2026-09-05 15:28
- S35 live in the NexusAI tree on the deploy branch's fix round | Wednesday's 15:1x SCORE + FIX ROUND mail to S35 and `tmux capture-pane` of `%4` — Wednesday's project, not the QA project's | read 2026-09-05 15:28
- The surface script's location (repo root, never a worktree) | re-gate (2)'s tooling finding, 2026-09-05T04:01:37Z | read 2026-09-05 15:28

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 15:28
(checked: "through-code only, nothing renders" against "if you stand a surface anyway" — optional, never required, and its script location is stated so it cannot nest; "base is 32e4dac" against "merge target 4e4a630" — the merge-readiness item exists precisely because they differ; "no LAW creds" against "measured at the wire" — the wire capture is the product's emitted query, which needs no workspace; stated.)
