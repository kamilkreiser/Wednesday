STARTABLE: YES (once Tuesday stamps; load1 was 10.20 at drafting, so launch through launch_when_cool)

# B905 drafter report: main red on the timed journey (SEAT-H56)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B905_SEAT-H56_hpsmpoc-main-red-timed-journey-budget.md` (86 lines, 9 empty stamp slots incl. last line, 0 non-ASCII, 0 at-sign tokens).
Model: Sonnet, `model-routing.md` row C2 line 92 (build) and gate row G2 line 109 (tier 2); id `claude-sonnet-5-5` at `models_latest.json` line 23. Launch line carries `BRIEF_SEAT_LEVEL=sonnet`. Ports 9960-9969.

## BLUF
- The red is a flake at the 1000 ms edge, not a code change: `compare/c00e2828...88569299` is 2 infra files, 0 web bytes; c00e2828 was green; PR #239 (infra only) missed both first spans on its first try and went green on retry.
- The journey missed its first try in 5 of 14 recent `ci` runs and ended red in 2 of 14. Only the first two spans ever miss, always by 8 to 181 ms (1008 to 1181 ms). Passing runs print nothing, so the usual value is UNMEASURED; the kit's first push is a one-line log of all 14 spans so CI shows the headroom.
- The 1000 ms is NOT client-stated. It is `journey.ts:17` `NAV = 1000`, from the v0 DRAFT demo script (section 3 "PROPOSED targets ... Unmeasured"). The client figure is the 7-minute total only. It is still the product owner's own proposed target, so the kit lets the builder change what is timed (extend the server warm-up) but makes any budget change or a cold-browser warm-up a STOP with figures.
- The spec already has a server warm-up ("/" and "/customers"), by design keeps the browser cold, and does not warm the Quollridge route. The default fix extends the warm-up to every walked route; acceptance is printed headroom (floor 750 ms, Tuesday may restamp), not one green colour.

## Facts re-measured (instrument; control)
1. 14 job logs of workflow `ci.yml` runs 40458012503 .. 40841854685 via `gh api -X GET actions/jobs/<id>/logs --allow-escape-sequences`; grep for `ms ≥`: 5 runs hit (40458012503, 40813522578, 40825927125, 40827172158, 40838879441); the other 9 print the timed block with 0 hits (control: the block header `[e2e] timed journey` is present in all 14). Spans: sign in -> Customers 1067/1047/1008/1018; -> Quollridge 1084/1033/1076/1181. Desktop 3 first-try misses, tablet 2. Images `ubuntu24/20261012.334` (1) and `20261025.353` (4). Whole journey takes 5.7 to 9.5 s.
2. Outcome per run: ended red 40825927125 (main) and 40827172158 (#241); flaky-green 40458012503, 40813522578, 40838879441. Frame: the last 14 runs only; not a rate estimate beyond that.
3. Config: `playwright.config.ts` lines 17, 48-58 (timed run, `workers: 1`, desktop then tablet), line 50 retries 1 in CI; `scripts/e2e.mjs` lines 44, 52; spec lines 11-23 warm-up. `ci.yml` triggers only on push main, pull_request, workflow_dispatch (read at 88569299): a branch push without a PR runs no CI, so the kit tells the seat to wait for Tuesday to open a draft PR.
4. Partition: #240 head now `8cbd9147` (19 paths), #241 `59625e5f` (20 paths); `grep -x -F` of `journey.spec.ts`, `journey.ts`, `playwright.config.ts`, `scripts/e2e.mjs` reads 0 in both (controls: `globals.css` and `shell-sidebar.spec.ts` read 1 in #240). main = 885692995df9f650b80dd4827fa0827349a7f619 (unmoved, via `git/ref/heads/main`). Required contexts: 5, `strict` false. Repo allows squash, merge commit, rebase; landing precedent head-pinned squash (CLARIFICATIONS line 138).
5. Ports: `lsof 9960-9969` 0 (control: python3 -I listener on 9961 counted 2 then 0). Kit-scan hit: B864 line 23 only mentions the block as a scan note. Panes: tuesday, Datasec/HPSM-POC-H55, fleet-monitor. `.tools/b905*` does not exist (glob no match; control: the b198 helper exists).
6. Provenance: demo script lines 3, 9, 64-70 (read from the project folder, not the SOW); journey.spec.ts history = 3 commits (c10fab25, 7b9a4fad, 3ee9107f); CLARIFICATIONS grep for budget/1 s/timed journey/performance target: 3 unrelated hits (control: `squash` hits line 138).

## D-decisions (mine, in the kit)
- D-1 Only `journey.spec.ts` is the builder's path; `journey.ts` is excluded (shared by a11y and screenshot specs, holds the budgets).
- D-2 Three pushes: instrument (log line, also prints passing figures), fix, one correction. The log line stays in the final head (additive, `expect` lines byte-equal) unless Tuesday says remove.
- D-3 Fix shape departs from your default ("warm-up navigation before t0"): the spec's own comment says the browser stays cold on purpose, so a browser warm-up changes what the span means; it is listed as option A in a STOP, not done by default.
- D-4 Acceptance = printed first-two-span max at or below 750 ms on the new head (desktop and tablet, every attempt) plus a local N=10 fresh-server table with a CDP CPU-throttle MODEL; one green run is explicitly not evidence (12 of 14 recent runs ended green).
- D-5 Plants in a scratch tree: injected 1200 ms delay on sign-in and on Quollridge must go RED; warm-up deleted and log-line deleted reported honestly.
- D-6 Tier-2 gate (G2 line 109): spec-only, no security surface. If you prefer tier 1 say so at stamp.

## Q-questions for Tuesday
- **Q-1 (is 1000 ms product-stated?)** NO for the per-span figure: Datasec's own PROPOSED target in the v0 DRAFT demo script (`1_Project_Definition/Demo/2026-09-23_demo-story-and-7min-script-v0.md` lines 64-70), coded at `web/e2e/journey.ts:17`. The client states only the 7-minute total (SOW txt:373, quoted by that script; SOW not opened). Whether the product owner later ratified 1 s is UNMEASURED. Default: builder may change what is timed, never the value (STOP with figures). 
- Q-2 Keep the `[journey-spans]` log line permanently? Default YES (it is the instrument that was missing).
- Q-3 Open a DRAFT PR on the builder's first push so CI runs? Default YES, immediately (nothing else produces hosted figures).
- Q-4 Extra hosted samples: if the 750 ms floor can't be judged from one head's 4 attempts, may Tuesday re-run the shard for MEASUREMENT only (all figures recorded, never to get green)? Default NO unless the builder reports thin evidence.
- Q-5 Floor of 750 ms (25 percent headroom) acceptable? Default YES; restamp if you want another number.

## UNMEASURED
Passing-run span values on the runner; the cause (cold Quollridge route vs cold browser vs mock API vs CPU); the `journey-timing` artifacts in the uploaded reports (not downloaded, they sit on a blob host); Jira (no documented read helper; not read); product-owner ratification of the 1 s; runner vCPU count; whether #240 or #241 landing shifts the spans (they change what the walk clicks).

## Discrepancy
The B903 kit says main's #239 is "3 infra files"; `compare/c00e2828...88569299` returned 2 files. Kit says to report if the seat reads otherwise.

## Outside-the-fences disclosure
- Ran `gh auth status` once under the project's `GH_CONFIG_DIR` (printed only the login and a masked token prefix, no token).
- One `git ls-remote` against `git@github.com:datasecau/HPSM-POC.git` from the TUESDAY repo context failed ("Repository not found", wrong key); read-only, no effect. main was read via `gh api git/ref` instead.
- Read the project's `1_Project_Definition/CLARIFICATIONS.md` and `Demo/...script-v0.md` and listed `JIRA.md`, `.tools/` names, and the first lines of `.tools/b60-jira.py` (a Jira helper, header only, not run). Did not open the SOW, `Source_Documents`, `HP Reporting and Docs`, or any `inbound/`.
- Used `search/code` (gh GET) for 3 queries on the repo. Scratch files in the session scratchpad (logs, fetched sources). A 6 s `python3 -I` listener on 127.0.0.1:9961 as the port control. No artifact download, no HTTP to any hosted site, no `cd`, no ref write, no Jira call, no card read, no forbidden tree read.
- Wrote only the two files named.
