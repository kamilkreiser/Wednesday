STARTABLE: YES

# B797 drafter report (Datasec / HPSM-POC, demo-site level chooser, code change), drafted 2026-10-27 08:48-09:0x AEDT

Kit: `2026-10-27_B797_SEAT-H42_hpsmpoc-demo-site-level-chooser.md` (123 lines). Seat H42, Opus, ports 8820-8829, branch `b797/hpsmpoc-demo-site-level-chooser`, STATUS path as commissioned.

## BLUF
Startable. The locks are in code and are narrow enough to widen safely. The kit asks for PAIRED identities: label `uat` on a `-uat-` site exactly as today, and label `demo` only when HOSTED and the site name equals ONE exact name per leg (web `app-hpsmpoc-web-demo-en46o7`, API `app-hpsmpoc-api-demo-en46o7`), compile-time constants, no pattern. Pairing is what keeps every existing UAT test green (several existing tests assert `demo` label on a UAT site, `uat` label on the demo site, and `demo` label unhosted all stay locked). It carries a binding "state plainly what an anonymous visitor can do" table built from tests, and names (does not change) the demo settings for the later deploy seat. The kit is a normal builder kit, not a refuse stub, unlike B792.

## The exact lock lines (re-read at main `d415a3fe`, via `gh api -X GET` raw and a tarball of that sha; blob not hashed, lines counted)
Web `web/src/server/auth/config.ts` (134 lines, read whole):
- line 53 `export const UAT_LABEL = "uat";`; line 54 `export const UAT_SITE_MARK = "-uat-";`
- **line 76** `if (env.HPSM_ENVIRONMENT !== UAT_LABEL) return off(...)`
- **line 77** `if (hosted && !v("WEBSITE_SITE_NAME").includes(UAT_SITE_MARK)) return off(...)` (contains test on the trimmed name; unhosted passes)
API `api/src/HpsmPoc.Api/Auth/UatOpenAuthentication.cs` (215 lines, read whole):
- line 48 `Label = "uat"`; line 51 `SiteNameMark = "-uat-"`
- **lines 104-106** label check (`string.Equals(label, Label, Ordinal)` else `Refuse(... Assessment:Environment is not 'uat' ...)`)
- **lines 107-109** site check (`HostingPlatformMarkers.Any(...)` and `WEBSITE_SITE_NAME?.Contains(SiteNameMark, Ordinal) != true` else `Refuse(... WEBSITE_SITE_NAME does not contain '-uat-' ...)`)
Control that I read the right ones: the earlier B792 report cited the same two locks (web resolveAuth, API Read lines 98-131) and these match; every web caller goes through `resolveAuth` (grep of `resolveAuth(`/`authUi(` outside tests: `proxy.ts:67,110`, `bff.ts:400`, `routes.ts:16`, `app/page.tsx:20`, `(app)/layout.tsx`), so the web lock is one function.

## Facts re-measured (instrument; control)
- F1 main = `d415a3fe172e3fe1e392c51e8c883f1a3d759990` (`gh api commits/main` and `git ls-remote`, both printed it; control: both equal). The local clone's `origin/main` is STALE at `dfdcfa27` (`cat-file -t d415a3fe` fails locally): the kit tells the builder to fetch under lock.
- F2 Guard history: `git log -S'SiteNameMark'` on the (stale) local ref prints one commit, `ae7a2c8` 2026-10-21 "UAT start page without sign-in (option a, UAT-only, two locks) (#177)"; same for `-S'UAT_SITE_MARK'`; `gh api commits?path=` on main: `config.ts` last touched by that #177 (older: #130, #60, #59), the API file by #178 (`35b2b73e`, exact switch) then #177. Controls: `-S'zzz-no-such-string-7f3a'` printed 0 lines; `-S'resolveAuth'` printed 2.
- F3 CLARIFICATIONS C-entry: the code and README cite the UAT copy as "C-52" (`UatLabelTests.cs:12`, `HostedDemo.cs:22`, `infra/README.md:227`, `uat.bicepparam:1`), but `1_Project_Definition/CLARIFICATIONS.md` (157 lines, last modified 29 Sep) has NO `C-52` and no UAT entry (`grep -c 'C-5'` = 1 for an unrelated hit; control `grep -c 'C-1'` = 18). The kit tells the builder to say what it finds when it reads, and not to edit the file (records seat's). The records seat B796/R56 may add it.
- F4 Names: bicep `appservice.bicep:62,166` `app-hpsmpoc-{api|web}-${environmentName}-${suffix}`, `main.bicep:53` one 6-char suffix per environment; `demo.bicepparam` names the web app `app-hpsmpoc-web-demo-en46o7`, `uat.bicepparam` `app-hpsmpoc-web-uat-25onzn`. The demo API name `...api-demo-en46o7` is DERIVED and also appears in an existing API test InlineData. Not verified live.
- F5 Existing-test traps (read at source): web `uatOpen.test.ts` rows with label `demo` on the UAT env (off), `uat` label on the demo web name (off), route test `HPSM_ENVIRONMENT: "demo"` on UAT env (503); API `UatOpenTests.cs` InlineData `demo` unhosted with message substring `Assessment:Environment is not 'uat'`, and the demo API name on the `uat` label with substring `WEBSITE_SITE_NAME does not contain '-uat-'`. A single shared "-demo-" contains rule, or a message rewrite, would break them; the pairing design and the "keep the quoted substrings" line avoid that.
- F6 Hidden coupling: the infra test `rule_web_settings` scans the web source for environment reads and refuses any it cannot resolve to a literal name (`test_security_baseline.py:341,478-490`); `rule_uat_only_switches` (line 579) pins the switches to uat in the bicep. The kit requires literal-name reads and tells the builder not to touch infra; hand-set demo settings or a later infra kit follow.
- F7 Ports: `lsof -nP -iTCP:8820-8839 -sTCP:LISTEN | wc -l` = 0; word-boundary scan of the 91 non-`.pre-` SEAT kits of 26/27 Oct for 8820-8839 = 0 files; control: the same scan for `\b9360\b` hit B759, B760, B761. Live panes (`tmux list-panes -a -F '#{@cockpit_name}'`): `tuesday`, `Datasec/NexusAI-R55`, `Datasec/MPS-G167`, `fleet-monitor`; no H42, no HPSM-POC seat. (Brief ranges 882x: no kit; dotted collision with prior ranges: none found.)
- F8 Model row C3, `model-routing.md:93` (Sonnet "no", Opus "1st"); `models_latest.json:17` `claude-opus-5-5`. Launch line carries `BRIEF_SEAT_LEVEL=opus`.
- F9 Open PRs: one, #222 (`b709/hpsmpoc-timing-rows-354`), one file `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs` (gh `pulls/222/files`): no overlap with the lane.
- F10 Slot count of the kit: `grep -c -E '_''_''_''_'` = 8 (seven slot lines and the last line); control: a one-line non-matching input prints 0.
- F11 CI: API tests in `HpsmPoc.Api.Tests.Auth.` run in the second SQL Server shard in docker (builder cannot); `TreatWarningsAsErrors` true in `api/Directory.Build.props`; infra job runs `infra/scripts/validate.sh`.

## What a visitor can do (drafter's reading, RELAYED, NOT verified; the kit makes the builder build the real table)
After the change and with the switch on, anyone with the demo link picks Partner, Consultant, Admin or Demo and acts as that fixed synthetic identity with that one role, no sign-in. Destructive routes (reset demo, export/erase, showcase reset, customer delete, per `infra/README.md` ~233) answer 403 `uat.action-off` for everyone including Admin; Entra sign-in is replaced (404), so named staff lose it on the demo. Admin can otherwise do what Admin does (create/edit within the sample data). The builder must state this from tests, not from this paragraph.

## D-decisions
- D-1 Option (b): build and gate today, no deploy.
- D-2 Demo identity = two compile-time exact names paired with label `demo` and a hosted requirement; no setting-named list, no pattern (a deploy-controlled list was rejected because a mis-set setting could then name a production site).
- D-3 UAT rule untouched (contains `-uat-`), so UAT tests stay green; its look-alike weakness (`x-uat-y` passes) is reported, not fixed.
- D-4 Roles, four entries, Admin untouched.
- D-5 Opus builder, tier-1 Opus gate.
- D-6 Settings named in READY for the deploy seat, none changed.

## Q-questions for Tuesday (each with a default)
- Q-1 Do you accept the exact demo API name `app-hpsmpoc-api-demo-en46o7` as derived, or will you have the deploy seat confirm it first? Default: accept (the API fails closed at start if wrong; the deploy seat verifies before it sets the switch).
- Q-2 The demo chooser will read "This is a review copy with sample customers only. Choose how you would like to see it." (UAT wording). Leave it (the kit forbids word changes) or commission a word change after? Default: leave, show the product owner.
- Q-3 Settings: after the gate, hand-set on the demo (outside the IaC) or a later infra kit that adds `demo` to the uat-only bicep and its pinned infra tests? Default: later infra kit; the hand-set is a one-off the deploy seat records.
- Q-4 Times: drafter suggests READY-by 11:15, hard stop 12:00 AEDT. Default: as suggested.

## UNMEASURED
Whether `.tools/dotnet` builds here; suite counts at main; the infra baseline without a local bicep; the demo API's real name; the settings now on demo/UAT; the demo vault contents; the exact set of routes marked `DestructiveAction`; the live state of any site. No npm, build, test or dotnet was run by me.

## Outside-the-fences disclosure
Reads only: `date`, DRAFTER_RULES.md, the B782 template kit, the B792 report (all whole), `model-routing.md` (grep and sed), `models_latest.json` (sed), `tmux list-panes`, `lsof`, `/usr/bin/grep`; `git --no-optional-locks` `cat-file`, `rev-parse`, `log` and `ls-remote` in HPSM-POC (read verbs; `log -S` ran on the stale local `origin/main`); `gh api -X GET` under the project `GH_CONFIG_DIR` (contents raw, trees, commits, pulls files, a tarball of `d415a3fe` downloaded into my scratchpad and unpacked there, never into the project). I listed (names only, `ls`) the folders `.tools/`, `.tools/b198`, `.tools/b267`, `.tools/dotnet` of HPSM-POC and the project `Briefs/` folder, and read `1_Project_Definition/CLARIFICATIONS.md` by grep. No git write, no fetch, no worktree, no az, no HTTP to a hosted host, no Jira, no card read, no mail/chat/Artifact/Docs. Only the two named files were written (scratch files lived under my session scratchpad). I did not read the B796 kit (not on disk at 08:5x) and did not open `.tools` file contents.
