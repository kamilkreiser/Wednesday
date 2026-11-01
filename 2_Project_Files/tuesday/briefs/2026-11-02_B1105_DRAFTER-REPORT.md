STARTABLE: YES (all Stamp slots left as four underscores for Tuesday; two launch-time cautions below: load1 13.07 and `heavy-slot-1` held by another seat at drafting)

# B1105 DRAFTER REPORT (routing row C8) - gate kit for B1093 / MPSCALC-269, tier 1, round 1 of 2

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1105_SEAT-G278_mps-269-templates-gate-tier1.md` (33,568 bytes; see C-1). Drafted 07:36 to 07:55 AEDT 2026-11-02 from DRAFTER_RULES.md (whole), the B1091 kit (whole, the template), the B1093 builder STATUS (whole), ADDENDUM-1 (whole), the B1093 kit (lines 5-22, 36-39, 66-72, 79-87).

## BLUF
- The kit attacks in the commissioned order: (1) merged tree on main 19d084fa plus the two commits, with the two-read rule; (2) Tuesday's readings R1-R3 tested against CLARIFICATIONS 1205/472, the prototype lines 521-522/771-772/788-789 and master prompt 100-101; (3) auth on six operations by trying them, then the file store (restart, concurrent writers, two processes, kill -9, bad file, identifiers, archived items, bounds); (4) done-when with clause 4 judged as a split; (5) the EntraAuthTests edit proved as exactly the allowed edit; (6) Node pin measured then run seat-local; word list completeness. Mutants GT1-GT35 (no GT31), a 300-sequence sweep against a model, severity, refuse list, stamp slots (8 four-underscore lines), launch line (BRIEF_SEAT_LEVEL=opus), last line `READ-WHOLE-BY-TUESDAY: ____`.
- Port block 9950-9959, chosen free (see below).
- Main moved 19d084fa touches 4 Engine paths, 0 overlap with the 14. Merged `web` tree equals the head's (main's web = base's), so unlike B1091 the web job is affected by this branch.

## Facts re-measured (instrument; control where one exists)
- `ls-remote` branch 717da6f8e6b1074c74e30a499215e92593852e2e, main 19d084fa8018094bf7ea9360433d0d87f8720e45 (07:36:24). `gh api -X GET compare main...717da6f8`: ahead 2, behind 1, 14 files, numstat identical to the builder's (+2532 -11 by sum of the per-file lines: docs/API.md 23, openapi 171/2, Program.cs 3, TemplateDtos 37, Endpoints 266, Rules 45, Store 470, EntraAuthTests 8/2, three test files 536/69/405, SOURCE.txt 2/2, snapshot 171/2, schema.ts 326/3). `compare b7cf1ad0...main`: ahead 1 behind 0, one commit "MPSCALC-257 ENGINE HALF: purchase sites on device groups...", 4 files (docs/ENGINE.md +2, PurchaseCalculator +44, PurchaseInput +9 -1, PurchaseSiteAllocationTests +553).
- Root trees (git/trees): `.github` 1eda8e1f, Directory.Build.props 6c7e9320, MpsCalc.slnx 69675730, global.json 512142d2 equal at base, main, head. `web`: base = main = d34ff342; head 1ae16b05. `docs`, `src`, `tests` differ at all three. `ci.yml` blob 212b0da1... equal at main and head.
- Contract blobs: main (19d084fa) and base docs/api/openapi.json 6adc6e0f1a41...; head contract and head snapshot both b3de93e55c70...; SOURCE.txt names 125450dd and that blob. Snapshot at 125450dd is still 6adc6e0f (commit 2 updates it): consistent with the builder's order rule.
- Commits: both end with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`; head commit unverified (`verification.verified` false); one parent each (717da6f8's parent is 125450dd). Actions runs for the head: total_count 0. Open PRs 121, 120 (dependabot). `pulls?state=all&head=datasecau:b1093/...` length 0. Squash settings COMMIT_OR_PR_TITLE / COMMIT_MESSAGES, allow_squash_merge true.
- EntraAuthTests patch (compare): +8 -2, three hunks; six rows with id tpl_000000000000000000000000 (24 zeros: valid under TemplateRules.cs:26 by its shape); lines 76 and 124 are the two `Assert.Equal(43, ...)`.
- Pointers printed by grep -n / awk NR==n over the raw files at 717da6f8 (fetched with `gh api -X GET ... contents?ref=`), re-verified at 07:44: TemplateEndpoints.cs 17, 21-26, 32, 73, 96, 107, 123, 176; TemplateStore.cs 35, 92, 176-180, 225, 278, 287, 292, 316, 353, 369, 406, 432; TemplateRules.cs 26; QuoteFileStore.cs 226, 232, 306, 453; QuoteEndpoints.cs 1110; ci.yml 30, 33, 42, 43, 45, 58, 61-66, 68; Directory.Build.props 6; web/package.json 7-8 (engines `>=20.19.0`); CLARIFICATIONS 472, 688, 758, 774, 1205, 1712, 1714, 1927 (printed). Node: only v26.8.1 installed (brew `node@26`); no nvm/fnm/volta; no .nvmrc / .node-version at head (404 x4); ci.yml node-version 24 at :58.
- Round count: of 75 project STATUS files whose first line starts `GATE VERDICT`, one names template word-bounded (B332, GO WITH FINDINGS, a web gate); control pattern for B1091 reads 2. NO GO 0 before on this class.
- Ports: `lsof -nP -iTCP:9950-9959 -sTCP:LISTEN` 0 rows at 07:41:26 (control: unrestricted listen listing 15 rows). Live panes (07:41:26): tuesday, HPSM-POC-R128, -G276, -H98, -H97, Security-Composer-J41, MPS-M73, fleet-monitor. Word-boundary scan `995[0-9]` over the six live-pane kits: 0 each (control: `996[0-9]` over B1094 reads 2). Over 106 non-`.pre-` SEAT kits of 11-01/11-02: hits B1044 (NexusAI, no pane), B1093 (closed builder, reserved and never bound), B1099 (records seat, no pane). Alternatives 9940-9949 is also free of live panes.
- Load 13.07 (uptime 07:38); `heavy-slot-1` holder `B1094 07:37:36 merged-test` (read from the holder file).
- Tool versions: dotnet 10.0.401 (project SDK), gitleaks 8.30.1; global.json 10.0.100 latestFeature.
- Model: routing row G1 `model-routing.md:108`, G-cap `:111`; `models_latest.json:17` claude-opus-5-5 (grep -n).
- Kit checks by program: 8 four-underscore lines; 0 non-ASCII; 0 occurrences of the owner's first name; no `cd`.

## D-decisions
- D-1 Shape by reference: the B1091 kit is about 140 KB; copying it breaks the 30 KB limit, so the kit names the B1091 kit, its STATUS and its evidence files as the form for the heavy slot, clone, mutant discipline, CLOCK, STATUS-NOW/RESUME, verdict form, squash-file checks and LANDING CHECKLIST, and states only the differences.
- D-2 Two-read rule stated in the builder's form, not the commission's short form (C-2).
- D-3 Squash trailer: exactly one `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (both commits carry it); the default COMMIT_MESSAGES body would carry both messages and two trailers, so Tuesday lands with an explicit body.
- D-4 The role-ruling words live at CLARIFICATIONS.md:1205 (and :472 for the earlier statement); the B1093 kit cited :686, which only says K-01 has no C-entry. Gate told to say which is right.
- D-5 Source_Documents opened only at the lines the commission and the B1093 kit name (prototype 521, 522, 771, 772, 788, 789 in two identical HTML copies; master prompt 100-101); the kit allows the same lines only, by `sed -n`.
- D-6 Tuesday's reading R1 tested for a real gap: the route array is Seller, Approver, Administrator; the Pricing analyst role maps to the internal-metrics permission, not an API role, so a token holding only it should be refused on all six. The kit has the gate measure it and report; not a finding.
- D-7 Mutant list GT1-GT35 over the builder's 19, covering roles per operation, immutability, archive, baseVersion, events, lock and reload, atomic write, guards, bounds, routes, overlap, contract enum, registration; GT33 pins the source-scan isolation test.
- D-8 A binding sweep of at least 300 operation sequences against a reference model, with restarts; its control must see GT8, GT15 and GT18.
- D-9 Port block 9950-9959, loopback only, 9950-9953 at most, for two-process and kill rows; in-process hosts bind nothing.

## Q-questions for Tuesday (each with a default)
- Q-1 Pricing analyst: the kit makes the gate measure that a Pricing-analyst-only token is refused on templates, against R1 "any signed-in role". Default: report it as a named question for the product owner, not a finding.
- Q-2 Template fields: the master prompt (line 100) lists optional/required, licence and care assumptions, pricebook versions, approver, validation status, recommended volumes; the build holds name and components. Default: gate lists the omissions as a question; Tuesday decides whether the product owner sees it.
- Q-3 Can Node 24 be fetched seat-local (official tarball or `npm exec`) under launch authority S4? Default: yes, under `.tools/b1105/node24/` only; else the web line is run at v26.8.1 and labelled not the CI predicate.
- Q-4 Apply ticket wording for clause 4: the kit asks the gate to say what MPSCALC-271 must carry. Default: records step files it after the verdict.
- Q-5 Launch timing: load1 13.07 and `heavy-slot-1` held by M73. Default: launch_when_cool, one waiter, as in the template line.
- Q-6 Squash body mentions the in-memory default (no `appsettings` path). Default: yes, as a held part ("no default path") in plain words.

## Contradictions with the commission, and other findings against it
- C-1 Size: the kit is 33,568 bytes, over the 30 KB limit by about 3.6 KB. I cut prose through six passes (the template's heavy-slot, clone and squash-check text is by reference); what remains is checks. Default: accept, or tell me which checks to drop (candidates: GT list tail, sweep, step 4(h)).
- C-2 "contract blob at main equals snapshot blob at head at landing" cannot hold literally: main's openapi.json blob is 6adc6e0f1a41 and the head's snapshot is b3de93e55c70 (and always will differ, since the branch changes the contract). The kit states the builder's form: read 1 main's contract blob equals the base's; read 2 the head's snapshot equals the head's contract and the merged tree's. rc 1 on either means a re-sync kit.
- C-3 Commission: "ahead 2, behind 0 on b7cf1ad0"; against current main 19d084fa the branch is ahead 2, behind 1 (consistent with "main has moved"; no contradiction of substance).
- C-4 "Copy ... its ON GO squash files": B1091's squash-file rules are referenced, not copied; one difference (Sonnet trailer, two commits) is stated in the kit.
- C-5 The B1093 kit cites :686 for the quoted role ruling; it is at :1205 (see D-4).
- C-6 "Repo's pin may say otherwise": measured: `engines.node >=20.19.0` at web/package.json:7-8, CI 24 (ci.yml:58), no .nvmrc/.node-version; local only v26.8.1, so "run the pin" needs a seat-local download.
- C-7 Builder STATUS says the kit asked for two `Program.cs` lines and it added three (a `using`); the compare confirms +3. Left for the gate to judge.
- C-8 B1099 (records seat R129, pane absent) and B1093 name the 9950-9959 block; neither is live. If R129 launches before the gate, its kit would need a re-scan (the kit tells the gate to re-run it).

## UNMEASURED
Nothing was built, tested or run. Not read: the three new test files, TemplateStore.cs beyond structure lines, the builder's mutant text, Jira. Not measured: whether the API runs in DevStub mode on loopback without a flag; whether Node 24 is obtainable; the Pricing-analyst token's answer; the actual word list (the builder's 20 / 22 / 22 are claims); whether the web job passes; `Mapping.cs` and the web reach of the sentences. B332 is described as a web gate from its first line only.

## Outside the fences (disclosure)
- Opened `Source_Documents/` prototype and master-prompt files for the exact lines named above (521, 522, 771, 772, 788, 789 in both HTML copies; MP 100-101), and ran sha256 on two of those files; no other Source_Documents content read.
- Read other seats' kits (B1094, B1099 and the live-pane kits B1096-B1098, B1102) only to grep port numbers and, for B1094, its Yours/HOLDS lines; did not read their trees.
- Ran `gh api -X GET` (contents, compare, git/trees, commits, pulls, actions/runs, repo settings) under the project's GH_CONFIG_DIR; no write verb, no Jira, no card, no `decision_queue.sh`, no briefs_staged, scoreboard, ledger, WEDNESDAY/FRIDAY tree or non-Datasec project.
- Invoked `dotnet --version`, `gitleaks version`, `node --version`, `uptime`, `lsof`, `tmux list-panes` (read-only). No `cd`. Scratch files only under the session scratchpad (raw copies of source files at 717da6f8, and the python edit scripts).
- Wrote only the kit and this report.
