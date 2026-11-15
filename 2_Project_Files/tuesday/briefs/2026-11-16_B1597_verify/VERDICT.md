GATE B1597: GO WITH FINDINGS @ 4522ff2 on main a9e0052

Round 1 of 2, tier G1. Head 4522ff2254149a9c75be0ac49c4b9a47b8426e7f on b1597/hpsmpoc-lane-q-question-set, one commit, parent a9e0052f. origin main a9e0052fe2f4e861a9571732d1eaa707b2968087, read at 00:2x (start) and 01:22 AEDT (just before this file); lane N (b1585*) not pushed at either read; open PRs 0 (control pulls/99999 404). All counts below are on main a9e0052f.

## Merge and deploy
- git merge-tree --write-tree a9e0052f 4522ff22: clean, tree 9126538e = the head's own tree (0 paths differ). CI at the merge = CI at the head.
- Paths: 44 (10 added, 34 modified). 0 shared with lane N's OWNED paths (lane N holds infra/README.md unchanged by its Q-5; it lists web/src/lib/**, web/src/components/snapshot/**, web/scripts/** as not its own). None under api/**/Hosting/, none in QuestionCard.tsx, no existing versioned content file changed.
- Deploy on merge: NONE. .github/workflows at the head holds only ci.yml (+ security/gitleaks.ignore). ci.yml runs on push to main but has no deploy job and no cloud login (0 hits for azure/login, webapps-deploy, az deployment, id-token); on main it only keeps the deploy packages as artifacts (deploy is a runbook step). No workflow file is changed by this head.
- Landing rule: "The landing form is a head-pinned squash" (analysis repo CLARIFICATIONS.md at origin main b7500c93, line 3617, read with gh api -X GET). The project CLAUDE.md has no landing or deploy line (grep -n -i land|deploy|squash|merge: 0 hits).

## Rows
| # | Rule | Result | Evidence (gate's own instrument) |
|---|---|---|---|
| 1 | The words | PASS | Deep string diff of 0.1.4 vs 0.1.3, 0.7.2 vs 0.7.1 and both client copies: every changed user-readable value is W1-W5 or Yes/No/Unsure (ruleset 4, package 11, client copies the same); the rest are ids/versions/type. Control: a planted label "Mostly" is flagged. W1, W2, W3 occur single-quoted inside the kit's Authority line byte for byte. W4 (134 chars) and W5 (191) are extracted from FEEDBACK.md line 11 (sha256 49e117eea7de...) and equal the files' Q-CS-05/Q-CS-07 text in ruleset and package; 0 non-ASCII. Added non-JSON code lines: no new UI string; SnapshotResult.tsx change is logic only. |
| 2 | The versions | PASS | Id-keyed deep diff: 0.1.4 PATHS 11, 0.7.2 PATHS 15, exactly the kit's lists (control: one changed text gives 12 / 16 and names it). 16 questions, same ids, weight, sectionId, scored; 5 sections, same weights. Canonical hashes by the kit's recipe: sha256:774164ccc6f7...14ad and sha256:5173dcd4d0fa...af82 (controls reproduce 0.1.3 sha256:4035158720cd and 0.7.1 sha256:0f179147c495); file sha256 6afb1222... and 76670e23...; diff lines 29 and 80. Seed vs web byte-identical (both). client-content --check: "21 client copies match" (main: 19). Ask order Q-CS-13, 02, 03, 04, 01, 08, 10, 11, 06, 05, 07, 15, 09, 12, 14, 16. |
| 3 | Scoring | PASS | Real API test hosts (ShowcaseFactory / HostedDemoOnFactory, local DB) with gate probe tests in a scratch worktree (10 of 10 green): Partly on Q-CS-01 -> R-001 only, S1 92.3 = Q-CS-01 at 50 of weight 4/26, overall 95.7; compensating on Q-CS-06 -> no finding, overall 100; Unsure on 01/06 -> R-001 and R-006. Boundaries all 422 answer.option-unknown: unknown id "maybe"; partly on Q-CS-06; compensating on Q-CS-01; partly on Q-CS-05; partly on a 0.7.1 snapshot. Hosted on 0.1.4: 0.7.2 scored "draft", an in-progress 0.7.1 refused ruleset.not-approved and stays in-progress. Recap (SnapshotResult.tsx:34/:37): web probe counts unsure 2 and lists both for revisit (control: a yes-no-unsure Unsure adds 1); with main's SnapshotResult.tsx the probe and the builder's D3 test are red ("expected +0 to be 2"), green with the head's. |
| 4 | Audience order (A05) | PASS | Of the 120 orders of the 5 audiences, exactly 1 passes A05 with 0.7.2's sections: PF, IA, NW, GR, SO, one adjacent swap from the old list; old list gives violation ['S2']. Audience objects equal as a set. Web loader (validateContentPackage) accepts 0.7.2 and refuses the old list with "(A05)"; API loader (ContentPackageLoader) accepts it and refuses the old list and PF,IA,GR,NW,SO with "(A05)" (gate probes). |
| 5 | Pin trio | PASS | appservice.bicep value (now line 143; a comment was added at 142), test_security_baseline.py:278, HostedDemoTests.cs:31 all read snapshot-policy-aligned@0.1.4 (main: all 0.1.3). test_hosted_demo_pin: 10 OK. readinessPackage = 0.7.0 (registry.ts:100), ShowcaseSeeder ReadinessPackageVersion "0.7.0". |
| 6 | PROVENANCE.md | PASS | "named by the hosted demo" (case-insensitive): 1 line, line 18, the 0.1.4 row, which ends with the sentence. Main: line 14 (0.1.2 row). |
| 7 | Census | PASS with F1 | Builder's census.tsv: 181 rows, 122 REWRITE, 59 UNAFFECTED; every UNAFFECTED row re-read. No test lost: test declarations per changed test file never decrease; vitest by name: lost 9, all renames, added 25 (16 new + 9 renamed); control drop-one raises lost to 10. Old Q-CS-05/07 texts: 0 references outside versioned content and _superseded. e2e helpers answer by id and kind, not position. One unrewritten line: F1. |
| 8 | CI | PASS with F3 | Table below. |
| 9 | Deploy notes | PASS with F5 | Read at source: CheckSeedRuleset exact ordinal compare (HostedDemo.cs:76-81) called at HostedDemoStartup.cs:86; ValidateLoaded Program.cs:96; seed idempotent (CompleteSeedInPlaceAsync); Quokka Freight in-progress sample ShowcaseSeeder.cs:132. Gate probe P7: seed 0.1.4 with setting 0.1.3 throws (the direction the builder left DERIVED). The builder's PR body states all four D6 effects and the stacked radios; the gate's pr-body.txt states both visible effects explicitly. |
| 10 | CodeQL and hand rows | PASS | CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof. CLI 2.27.4, security-extended: javascript 0 results at main and merge; python 0 and 0 (controls: planted js incomplete-sanitization and py chmod 0o777 give 1 each). Hand rows over 676 added non-JSON non-md lines: new RegExp(var) 0, hand-escape 0, innerHTML 0, child_process 0, Process.Start 0, raw SQL 0, chmod 0; sensitive-name 2, both the W4 constant (the word "authenticate" / "username/password" in content), a reviewer sentence, not a credential; each row's control fires. |

Scans: name scan (ban list + identity first/last names, underscore-aware, control _by_<name>_ fires) over 831 genuinely new added lines and the commit message: 0. B1597/H170/SEAT/Tuesday/Wednesday/Friday: 0 on genuinely new lines and the message (5 "Friday" hits are copied provenance lines verbatim in 0.7.1 on main). HPSMPOC-n / B-number in message: 0. Non-ASCII on added non-JSON lines: 0; Cf characters on any added line: 0 (control U+202E). 40-hex, GUID, hosted host, key shapes, .env: 0 (control 40-hex fires). Commit author/committer the project's noreply identity; one trailer.

## CI at main and at the merge (gate's runs, this machine, ports 10130-10135)
| Job | main a9e0052f | merge (= head) |
|---|---|---|
| web lint / typecheck / build | rc 0 / 0 / 0 | rc 0 / 0 / 0 |
| npm audit prod / audit-dev | 0 / 0 | 0 / 0 |
| client-content --check | 19 match | 21 match |
| e2e --check-shards | plan OK | plan OK |
| web unit (vitest) | 301 files, 4302 passed, 0 failed | 303 files, 4318 passed, 0 failed |
| e2e 8 shards, CI=1 | 970 passed, 0 failed, 46 skipped, 0 flaky | 970 passed, 0 failed, 46 skipped, 0 flaky (per shard identical) |
| dotnet test, default host + Azurite | 4145 passed, 0 failed, 0 skipped | 4161 passed, 0 failed, 0 skipped |
| SQL part api-assessment (ci.yml judge) | not run whole | 1474: 1473 passed, 1 failed (the known flaky test only), 321 databases (floor 100), host retries 0 -> judge rc 1 |
| SQL part api-other-and-feedback | not run whole | 1348 passed, 0 failed, 243 databases (floor 110), judge rc 0 |
| known flaky test alone on SQL Server, x5 | 5 of 5 red | 5 of 5 red (same assertion) |
| infra validate.sh, unittest (system python 3.9.6) | 325 ran, 1 failure (test_resource_hygiene ...fails_the_run) | the same 1 failure |
| infra under Homebrew python3.14 | validate rc 0, 325 OK, pin 10 OK, hidden chars 14 OK | the same |

## Findings
| # | Severity | Finding |
|---|---|---|
| F1 | Minor | web/src/components/snapshot/stamped-set.test.ts:17 (not rewritten) asserts `moduleSet.questions[0].id` is "Q-CS-01", where moduleSet is the CURRENT playbookPackage's set (0.7.2 now), commented "control: the route's set is 0.5.0's". It stays green because the array order is unchanged, but Q-CS-01 is no longer the first question asked; the census reason "0.5.0's own first question" is wrong for this line (it is right for :22). The comment was already stale before this lane. Not a red; a follow-up comment fix. |
| F2 | Minor | Claim imprecise: STATUS says "one pre-existing ellipsis" on the edited PROVENANCE row was replaced by three dots; the 0.1.2 row had three U+2026 replaced (two hash cells and "...being finalised"). Developer text only; no meaning changed. |
| F3 | Minor (not this lane) | The known flaky ForwardedProofTests test was the only red of the api-assessment SQL Server part at the merge. Alone on SQL Server it is 5/5 red at main and 5/5 at the merge (equal rates; it passed in the default-host run at both). No file under api/**/Hosting/ is changed. Hosted CI will show the same red on main. |
| F4 | Minor | Pointer moved: the Bicep value is at infra/modules/appservice.bicep:143, not :142 (a comment line was added above it). |
| F5 | Minor | The builder's pr-body.md states the audience-filter effect only inside its live-check paragraph and in the order section; the gate's pr-body.txt names both visible effects as such. Use the gate's. |
| F6 | Note | New test file web/src/components/snapshot/QuestionCard.072.test.tsx sits in a folder the kit lists as not owned except SnapshotResult.tsx; it meets the OWNS property (the named home of Step 5's card assertions, beside the rewritten SnapshotResult.tsx) and is in no other lane's OWNS. |

## Builder STATUS claims
True: refs and one commit; 44 paths (10 A, 34 M); the four hash values; PATHS 11/15; diff lines 29/80; 21 client copies; ask order; vitest 4318/303 and 4302/301; renamed 9, added 25; e2e 970/46/0 at both; dotnet 4161 and 4145; SQL 1474 and 1348 parts and database counts 321/243; infra py3.9 single failure at both and py3.14 green; CodeQL js/py 0 at both; csharp cannot extract; D3 red at base "expected +0 to be 2"; finding orders of the all-No run; landing rule line 3617.
False: "one pre-existing ellipsis" (three; F2).
Not shown by the gate: the live browser check and its 4 axe scans (scratch script, not committed); the red-at-base runs of content-072 / Content072Tests / Content072ApiTests (the gate re-proved D3 only).
Of note: the builder's SQL api-assessment part was all green where the gate's had the known flaky red; the builder's "did not fire" is a claim about its own runs.

## NOT RUN
- CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof.
- The SQL Server parts whole at main (the flaky test alone was run 5x there).
- The live-API Playwright specs (in no CI shard), including playbook-content-050-live-api.spec.ts:56-60 as edited.
- Hosted CI and hosted CodeQL (no PR opened by the gate).

## Resources
Clone and worktrees only under the gate's session scratchpad (push URL set invalid; nothing pushed). Containers g1597-azurite (127.0.0.1:10131) and g1597-mssql (127.0.0.1:10130) started and removed by name: 0 g1597 containers at the end. Listeners on 10130-10139: 0 before and 0 after (control: unfiltered list 16 and 13). The SQL password and Azurite key only in environment variables, never printed. Nothing in the HPSM-POC project folder was modified.
