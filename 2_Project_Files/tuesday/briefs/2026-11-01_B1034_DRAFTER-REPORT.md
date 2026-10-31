STARTABLE: YES

# B1034 drafter report (SEAT-H91, HPSM-POC test-only builder closing B1027-1)
Drafter: Agent-tool sub-agent for Tuesday, 2026-11-01 10:26 to about 10:50 AEDT. Kit: `briefs/2026-11-01_B1034_SEAT-H91_hpsmpoc-388-roadmap-two-scored-runs-test.md` (154 lines; 9 stamp slots plus the last line = **10** four-underscore lines; `@[A-Z_]+@` 0; non-ASCII 0). `.pre-stamp` made with `cp -n`, `cmp` equal, sha256 both `57ab1f6bebb4606074693017aeab1fc5dce4f51bebcfe68e71a2431979ce7697`. Template: the B1025 kit (read whole, 206 lines).

## BLUF
- The change is 8 added harness lines (a `resultsFor` map, empty by default, plus a per-id result route placed before the existing one) and one appended `describe` with one row in `SecurityRoadmap.test.tsx`. The row is the gate's sharper scratch row moved onto the harness. **No import line changes and no removed lines:** every name needed is already imported (MEASURED at `7f0d832d`, tree = main's).
- **Correction to your brief and the gate's fix-shape: the new row cannot be red under g18.** With two scored runs the newest run is both `runs[0]` (g18) and `top` (the head), so g18 gives the head's answer. g18 stays caught by round 2's row R3 (B1027: red 1). The kit requires the new row RED under g18b and h1 (harness map ignored), predicts RED under g18c (reviewed titles from the oldest run), and predicts GREEN under g18. That prediction is D-3, not a STOP.
- Route: the shared `2_Project_Files` does NOT hold `1f4bf7bc` (cat-file fails; it holds `7f0d832d`). The kit uses B1027's measured route: own clone, one fetch by URL with the per-command project key, worktrees from the clone, one push by URL to a NEW branch `b1034/hpsmpoc-388-roadmap-two-scored-runs`. Nothing is fetched or written in the shared repo, so it cannot touch D43.
- Seat H91 is free and ports 9070-9079 are free. B1034 is unused.

## Facts re-measured (instrument; control)
- Main `1f4bf7bc` (`gh api git/ref/heads/main`); tree `670120e9` = `7f0d832d^{tree}` (`git rev-parse` in the shared repo, `gh api` for the squash). `matching-refs/heads/b1034` 0 (control `b1016` 1). Open PRs 0.
- At `7f0d832d`: `harness.ts` is 61 lines; the result route at 57-59 answers one result for every id; `resultsFor` 0 in `web/src`. `SecurityRoadmap.test.tsx` is 160 lines with imports at lines 3-7, round 2's describe at 149-160 and `show` at 39. `useSecurityData.ts:59-78` shows `top` = the newest readable run. Anchors (each exactly 1; zero control 0): the g18 line, the `reviewed:` line, `assessmentsFor: {}, reportsFor: {},`, and the result-route line. 6 test files use the harness.
- The gate's g18b proof and scratch file 2 were read as text. Its row 1 shape (two scored runs, F-1 reviewed in both, NEW/OLD action text; OLD-ACTION absent, NEW-ACTION and NEW-REVIEWED present) passed unplanted 3 of 3 and failed planted.
- Ports: across the 802 non-.pre- SEAT kits dated 2026-10 and 11-01, every 10-port block from 9000 to 9699 is named at least once, except 9070-9079 (0). In all of `tuesday/briefs/` that block appears once, in a 10-26 drafter report; it also appears once in the project Briefs (a 10-07 STATUS). Control: `963x` hits the B1025 kit. `lsof -iTCP:9070-9079 -sTCP:LISTEN` 0 (all-listeners control 16).
- Seat: `H91` appears in 0 kits and 0 of today's project STATUS files (control `H90` 5 kits, 3 STATUS). No H91 pane at 10:29. `.tools/b1034` and `.tools/wt-b1034-fix` absent (control `.tools/b1031` present).
- Helpers: `.tools/b198/lock.sh`, `.tools/b267/waitload.sh` and `.tools/node24/bin/node` exist. gitleaks is 8.30.1. Key `3_Access_Keys/github_deploy_rw` has mode 0600, 419 bytes.
- Model: `model-routing.md:92` C2 "1st"; gate rows `:108` G1 and `:109` G2; cap row `:111`. `models_latest.json:23` is `claude-sonnet-5-5`. `brief_seat.sh:24` defaults to opus, so the launch carries `BRIEF_SEAT_LEVEL=sonnet`.
- D43 (B1031): pinned to `77c3132e`. Its tree is `.tools/b1031/` and its ports 9740-9749. It makes no ref write in `2_Project_Files` (kit line 73) and writes no records or Jira.

## D-decisions
D-1 the shared-harness map (default empty, added lines only). D-2 no new test file; an appended describe with its own reset. D-3 the g18 correction. D-4 plants c0, g18b (frame + whole suite), g18, g18c, h1. D-5 Sonnet; READY 75 min, hard stop 120. D-6 one commit. D-7 own clone, no shared-repo writes.

## Q-questions for Tuesday (each with a default)
- Q-1 GATE-ROUND class and round: default **round 1 of 2 on a NEW class "roadmap actions from the reviewed run"**. The ruling ticketed it as residue, so the closed part-B class is not reopened. The alternative is "round 3 on part B", which would need the product owner's word under G-cap.
- Q-2 Gate tier and model: default **tier 2 on Opus**. It is tests-only, but its mechanism sits on a G1 surface (`model-routing.md:109`, Opus column "1st if the follow-up's mechanism sits on a G1 surface"). The alternative is tier 1 Opus, as B1022 and B1027.
- Q-3 D-3: accept that the new row need not be red under g18 (R3 already catches it)? Default **yes**. The other way would be a second row, outside "one row".
- Q-4 Timings: target 75 / hard stop 120. Default yes.
- Q-5 H91 and ports 9070-9079. Default yes.
- Q-6 Run alongside B1033 (records) and D43 (deploy)? Default **yes**: no shared path, repository or Jira write.

## UNMEASURED
No clone, fetch, npm or test was run. Not measured: the new row on the harness; the g18c, h1 and g18 outcomes; any lint reaction to `.sort()` without a compare function; whether a new-branch push is allowed by the ruleset (earlier builders created `b1016/...`, so very likely yes); today's fetch on a fresh clone.

## Outside the fences (disclosure)
- Read-only. I wrote only this kit, its `.pre-stamp` and this report.
- `git --no-optional-locks` reads in the shared repo (`show`, `grep`, `cat-file`, `rev-parse`) and `gh api -X GET` only.
- A python read of the shared repo's `.git/config` tested the key path. The path was shell-escaped: my first parse wrongly said "missing". B1025's push with that config worked, which is one more reason for the kit's own-clone route.
