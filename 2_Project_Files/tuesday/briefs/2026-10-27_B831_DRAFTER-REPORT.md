STARTABLE: YES (stamp, then launch at load1 below 7; four Q-questions below, each with a default; PR #234 checks were still running at the draft)

# B831 drafter report: HPSM-POC PR #234 tier-1 QA gate (SEAT-G178), the demo's open sign-in switch pinned in the template

## BLUF
- The kit is `2026-10-27_B831_SEAT-G178_hpsmpoc-234-demo-switch-gate-tier1.md` (103 lines, about 67 KB, longer than the B817/B827 shapes because it carries nine checks), 8 stamp slots (`_{4}` line count 8, as unstamped kits read; `.pre-stamp` copy beside it, `cmp` equal), 0 non-ASCII bytes, 0 `@NAME@` slots.
- Tier 1 / Opus (row G1, line 108; cap row line 111). Round 1 of 2 on the class "the template's open sign-in switch and key references". Seat `Datasec/HPSM-POC-G178`, ports 9590-9599, STATUS `.../Briefs/2026-10-27_B831_STATUS.md`, launch line in the B817 `cockpit.sh add` form with `BRIEF_SEAT_LEVEL=opus` and `WED_USAGE_STOP=100`.
- **The premise checks out on main: the demo arm is already in the code.** At `271f6932` the API (`UatOpenAuthentication.cs` 96-150, `DemoSiteName` line 60) and the web (`config.ts` 56-87, `DEMO_WEB_SITE_NAME` line 60) refuse the switch unless uat on a `-uat-` site or demo on the demo's exact site name; `git diff 271f6932 7ed38bc8 -- api web` is empty (drafter: only the stat over `main.bicep env scripts .github api web` was run, 0 rows). So the "Blocker: demo arm not on main" in the brief cannot fire unless main moves; the gate still reads it at the head.
- **The PR is now open and its checks are not done.** #234 opened between the builder's 15:36 push and my 15:40 read. At 15:42: 13 check-runs, 7 completed (6 success incl. `infra (Bicep validate)`, `secrets`, `dependency review`, three Analyze; summary `CodeQL` neutral), 6 in progress (`api`, both `api on SQL Server`, `web unit tests`, `web build`, `Analyze (csharp)`). Three code-scanning analysis rows exist (js-ts, python, actions), none for csharp yet. The kit makes the gate WAIT (C7) and caps at "conditional" if not finished.
- **One concrete defect found by the drafter, in the commit message:** it says "96 tests (86 before)"; the file's `def test_` count is 99 / 89 (builder's own Corrections 7 admits it). It is a Minor in the kit (wording), but it is what lands if Tuesday squashes with the commit message; the kit tells the gate to say which text lands and tells Tuesday to word the squash message with 99 / 89 and 277 / 267.
- Hygiene of the diff by the drafter: added lines holding `B###` 0, `HPSMPOC-n` 0, card-id shape 0, non-ASCII 0; commit has one `Co-Authored-By` trailer; commit is unsigned (a Note).

## Facts re-measured by the drafter (instrument; control)
- `ls-remote origin`: main `271f6932...`, branch `7ed38bc8...` (no control run). `pulls/234`: open, not draft, head/base as above, 3 files 400/96, `mergeable_state` `blocked`. `compare`: ahead 1, behind 0. `pulls?state=open`: #234 only (no control for a one-row list).
- Template diff and test-file rule/row names read with `git diff` / `git grep` in the shared `2_Project_Files` (read verbs only; both shas are commits there, `cat-file -t` printed `commit`). `main.bicep`: `environmentName` is `@allowed([ 'dev', 'uat', 'demo' ])`; vault name `kv-${prefix}-${suffix}`; `prefix = hpsmpoc-${environmentName}`.
- Required contexts (`branches/main/protection/required_status_checks`): `api (ASP.NET Core)`, `web (Next.js)`, `infra (Bicep validate)`, `secrets (gitleaks, full history)`, `dependency review (...)`. `web (Next.js)` is not yet among the head's check-runs.
- Round-count loop (first lines of `Briefs/*_STATUS.md`, `case "$l" in "GATE VERDICT"*`): 434 files, 75 GATE VERDICT lines printed; control B805 line printed. No line on this class (nearest: B799 on #232's code-side class, GO WITH FINDINGS). The loose-scan step is left to the gate (not run by me).
- Panes: `%75 Datasec/HPSM-POC-H46` (B825, chooser logo, `web/**` only; its STATUS at 15:37 shows an AFTER chain running behind the load rule) and `%74 Datasec/HPSM-POC-H47` (B826, finished builder, parked at READY). No other HPSM-POC pane. Ports 9590-9599: `lsof` rc 1 at 15:40; the word-boundary scan of 2026-10-26/27 non-`.pre-` SEAT kits hit two files (B737 composer, B761 hpsmpoc redeploy), both finished kits, so free per your rule; the second hit is a hpsmpoc kit, hence the kit's wording "a finished kit that merely names it is not a STOP". No positive `lsof` control run by me.
- Ruling (via `decision_queue.sh show` only): ruled `a` at 13:35:49; "UAT stays off" is Tuesday's imprecise wording (stamped Q-2 in B826); the kit judges against "UAT compiles exactly as now".

## D-decisions
- D-1: the heart is C2, an OWN ARM-expression evaluator over the compiled `main.json` for dev/uat/demo with a base x head table of every setting of both sites (not the PR's `evaluated`, not the builder's `table.py`), with planted-edit controls and a leaf-path diff; plus a declared "one instrument" caveat if no second route exists.
- D-2: C3 is a read-and-tabulate of the API/web refusal rules (no dotnet, no node build), graded PROBED/READ ONLY and labelled as a transcription of source, not a run of the product.
- D-3: mutants G1-G13 are the gate's own; the builder's M1-M8 are re-run as one table. G13 (`environmentName != 'dev'`) is a predicted equivalent survivor because of `@allowed`.
- D-4: Blocker list written for this surface: switch on in dev, wrong secret or vault, typed vault host, any uat cell moved, a merge that would deploy.
- D-5: the "deploy after landing" stays a separate kit (the builder's FOR TUESDAY 2; B810 recorded 36 API / 18 web live settings that a full template deploy would also overwrite).

## Q-questions for Tuesday (each with a default)
- Q-1: Does "uat unchanged from main byte for byte" mean the evaluated setting values, or the raw ARM expression text? Default: evaluated values, byte-equal after evaluation; the raw text of the four settings changes for every environment because one `main.json` serves all three (a Note). The kit states this.
- Q-2: Which text lands on a squash: the commit message with "96 tests (86 before)" or Tuesday's own wording? Default: Tuesday words the squash message with 99 / 89 and 277 / 267; the gate grades the commit message as Minor.
- Q-3: Class text and round count. Default: "the template's open sign-in switch and key references", round 1 of 2, because no earlier gate judged a build of it; a loose hit that is the same class goes to Tuesday as a Q-question.
- Q-4: Target verdict 90 min / HARD STOP 150 min after Step 0 (the heavy work is two whole-infra runs of about 65 s plus bicep builds, so lighter than the NexusAI tier-1 gate). Default: accept; the CI wait (up to 40 min beyond the last heavy job) is the long pole and the web/api shards run on a loaded machine.

## UNMEASURED / facts not read at source
- Not read at source: `infra/modules/appservice.bicep` site `name:` lines (the demo site names) and the module call's `keyVaultName` in the compiled JSON; `.github/workflows/ci.yml` (whether a push to main can deploy the template; C8 (a) makes the gate read it and treat "a merge would deploy" as a STOP); `test_security_baseline.py` rule bodies (I read names, constants lines 570-604 and the added `def test_` names only); the builder's evidence files.
- Not run: bicep build/lint, unittest, any mutant, any clone or fetch. The builder's numbers (277/267, 10 red-first, 8 of 8, 156 cells / 4 changed, 8 leaves) are RELAYED only.
- The demo site-name suffix `en46o7` equals the template-derived suffix only in the existing demo resource group (`uniqueString` needs the RG id); a mismatch would make the demo API refuse to start (fail closed). Noted in the kit as UNMEASURED/Note.
- The first-line loop's 75 count moves as other gates start; the gate re-measures.
- `gh` reads were GET only under the project's `GH_CONFIG_DIR`; `decision_queue.sh show` for the one card only (no `list`). No `az`, no HTTP to any hosted host.

## Outside-the-fences disclosure
Wrote exactly three files: the kit, its `.pre-stamp` copy, and this report. Everything else read-only. One drafter slip: my first Bash call used `=====` in an `echo` and was refused by the zsh hook (no effect); a later `cd`-free retry used `bash -c`.
