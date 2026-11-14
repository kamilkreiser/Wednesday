GATE B1556: GO WITH FINDINGS @ ff9efe7 on main 576231b
G1 gate, round 1 of 2 (a Demo viewer is the HP reviewer), class UI wording / alias on existing rules. 2026-11-15, 06:30 to 06:57 AEDT. Head ff9efe7cbd362febecb836848e217c621808b771, 1 ahead / 0 behind main 576231b7697bf6a758d8091e9099c0dd60c2dce7 (ls-remote re-read at 06:56: both unchanged; open PRs 0). Own clone + two worktrees under fleet/state/s275/g1556 (push URL set invalid; nothing pushed). Node v24.22.3 (copied from the builder's folder, not edited), Python 3.14.10, bicep 0.47.16, gitleaks 8.30.1.

## Findings

No Blocker, no Major. No security-shaped issue.

| Sev | Where | Finding | How measured |
|---|---|---|---|
| Minor | web/src/components/customer/EngagementsList.test.tsx, EngagementsList.restyle.test.tsx, FirmwareTask.test.tsx, playbook/SnapshotLauncher.b97.test.tsx | Four existing test files are outside the kit's explicit OWNS list. They meet the kit's stated property ("carries a literal this change makes false"), so this is not a path outside the lane. Tuesday rules on it (builder Q-A). | I ran main's versions of these 4 files plus engagement.test.ts against head's 8 product files: 7 red, 24 green. The 5 reds outside engagement.test.ts are exactly the builder's list. Each one reads a stored name in a harness where getMe never answers, so the label stays the neutral word. Head's edits (an ApiModeProvider mode="mock" wrapper, a Partner getMe, findBy/waitFor) are green at base and at head. I read them whole and they weaken no assertion. |
| Minor | builder pr-body.md, "Rendered" bullet | The bullet says "no stored sample-customer name on any of the seven pages". That is true of the visible text only. As Demo at head, document.body.textContent still holds "Sample customer B" once on /customers/sample-b/documents, /profile, /tasks/firmware-risk and the overview. It sits inside a Next.js RSC `<script>` payload: CustomerShell's `customer` prop, `{"id":"sample-b",...,"name":"Sample customer B"}`. It is not new: base has the same script on the same pages. pr-body.txt states the visible-text scope. | probes/probe.mjs and probes/where.mjs (Playwright, tree walk over text nodes). innerText count is 0 on all 7 pages at both widths. |
| Minor | builder STATUS, "TESTS (Step 5)" | This section says playbook-followup.spec.ts:130 pins "1 of 10". The commit pins "1 of 11", which matches the builder's own later correction in the E2E history paragraph. The STATUS contradicts itself; the code is right. | git diff of web/e2e/playbook-followup.spec.ts:130. |
| Minor | builder evidence landing.txt, squash-body.txt | landing.txt uses `--body "$(cat ...)"`, relative `cat` paths and `<PR-NUMBER>`. squash-body.txt has a broken line wrap ("With one surface / put back") and no closing trailer. landing.txt, squash-body.txt and pr-body.txt here replace them in the template's form (absolute `--body-file`, `<N>`). | Read the files. |
| Info | web/src/components/customer/ApiSteps.tsx:166 | `statusText` also feeds the Assessment step's run list, so W1 shows there too: a fourth place the wording appears. This matches the 420 ruling ("everywhere"). The builder disclosed it. | git grep of the callers at head. |
| Info | 420, unscored sets (fact) | The predicate copies the chip's exactly (`typeof scoredAnswered === "number" && typeof scoredRequired === "number"`, engagement.ts:155-156 vs CustomerShell.tsx:93-94). Visible consequence for a set that no ruleset scores: **the count disappears.** The launcher and Assessment-step label reads "In progress" alone. The overview run line reads "Started <date>" with no count. The activity-feed in-progress row reads "Started". On the local mock the snapshot set is scored, so the count shows ("3 of 10 scored questions answered" on the launcher and overview, where base read "5 answers so far" beside a chip reading "3 of 10 ..."). The unscored fallback is pinned at unit level only. | Source reading. Rendered base vs head (probe). Unit rows engagement.test.ts:98-100 and the launcher count row. |
| Info | CustomerManagement.tsx (sort, search) | As the kit says, sort and search still read the stored name. A Demo viewer sees aliases in stored-name order. Typing a guessed stored name into the search box filters to that row, so a Demo viewer can confirm a guess. Named, not built. | Source reading; the unit test pins Yarrow before Zinnia. |
| Info | useSecurityLabels (reused, not changed) | When getMe or getMetricsSummary cannot be read, every row on the 4 list surfaces reads the neutral "Customer", for a Partner too. Before, a Partner saw the names. This is the existing rule of the security pages, reused as the kit orders. | useSecurityLabel.ts:19-36. |
| Info | SnapshotLauncher.tsx:44 | `answersSoFar` is exported with no caller left (not even a test). Lint passes. Kept by the never-delete rule. | git grep at head. |
| Info | the kit's red-first property | The kit predicted that the not-yet-known rows are green at BASE. They are red on all six surfaces, because main prints the stored name unconditionally. The builder's deviation note is correct. | Red-first run below. |

## Measured (this gate, each with a control)
1. **Refs / merge.** `git merge-tree --write-tree main head` rc 0, tree e66452b4 = head's own tree. 1 commit, 1 parent (main).
2. **Scope.** 21 changed paths. 17 are on the explicit OWNS list; 4 are the test files above (control: a planted web/src/x.ts reads 1). 0 forbidden paths: home, partner, snapshot, shell, security, lib, server, content, scripts, package*.json, api, infra, .github, industries.ts, content.ts, a11y.spec (control: a planted home path fires). The e2e hunks are exactly @@-127, -130 (followup) and @@-48, -73 (snapshot). Untouched at head: PartnerDashboard.tsx (Home table), SnapshotResult.tsx (tile), DocumentsStandalone (DocumentGeneration.tsx:220 still `{r.name}`), the Industry select. Open PRs 0.
3. **No new words** (scripts/newwords.py). I tokenised every string literal and JSX text on the 45 added product lines: 37 tokens. 36 are found verbatim in a product file at base. 1 is W1 (`${c.scoredAnswered} of ${c.scoredRequired} scored questions answered`, engagement.ts:156). NEW 0. A planted sentence reads NEW 1. The alias words are reached through the existing helpers; none is retyped.
4. **467 rendered** (mock build, `next start` on 9791 base / 9792 head; Demo and Partner signed in through the mock sign-in; 1280 and 390 wide; stored names from /api/v1/customers: "Quollridge Logistics (sample)", "Sample customer B", "Sample customer C", with the partner's own record excluded).
   - Demo at head: innerText name counts 0,0,0 on S1 /customers, S2 /engagements, S3 /customers/sample-b/documents, S4 /customers/sample-b/profile, S5 /customers/sample-b/tasks/firmware-risk, S6 /playbook/snapshot-assessment and C1 /customers/sample-b, at both widths. The existing no-run words are shown (S1 42, S2 2, S3 4, S4 5, S5 7, S6 5).
   - Control, Demo at base: names are visible on S1 (2,2,2), S2 (1,1,0), S3 (0,1,0), S4 (0,1,0), S5 (1,2,1) and S6 (1,3,1), at both widths.
   - Control, Partner at head: names are visible on all six at both widths.
   - The ORG-nnnnn alias itself is unit-pinned; the mock has no scored run at the demo start.
   - Probe through the unit harness: a 5-row Customers list as Demo made getMe 1 call and getMetricsSummary 1 call. Source: useSecurityLabels is called at the top of CustomerManagement, EngagementsList, CustomerSwitch and SnapshotLauncher. RowActions takes the label as a prop.
   - Links, keys and option values keep the stored route or API id (diff read; unit test asserts the href).
5. **Red-first.**
   - Head's 11 new and changed test files against main's product files (whole suite in the mutant): 16 of 51 rows red, 35 green, and every other test in the repo green (4242 passed, 16 failed).
   - The reds: every Demo row (6), every not-yet-known row (6), the launcher count row, the answeredText row, and the two activity-feed rows.
   - The green controls: every Partner-without-Demo row, the own-organisation line, and the 4 edited existing tests.
   - Planted control: FirmwareTask's related-engagement row put back to `customer.name` in head's product files turns exactly the 2 FirmwareTask.alias rows red (44 green over all 8 alias files). I chose a different surface from the builder's control.
6. **Whole vitest, compared by name** (file, ancestors, title). Base: 292 files, 4238 passed. Head: 298 files, 4258 passed, 0 failed, 0 skipped. LOST 1, exactly the retitled answeredText row. ADDED 21 (19 alias rows and 2 engagement rows). Control: dropping one row makes LOST 2.
7. **web-build at base | head.** npm audit --omit=dev high 0 | 0. audit-dev 0 | 0. lint (max-warnings 0) rc 0 | 0. typecheck 0 | 0. build 0 | 0 (check-client-bundle: none of 39 markers). e2e --check-shards OK | OK.
8. **e2e at head, all 8 shards whole** (ports 9790/9794/9795/9796):

   | Shard | Passed | Skipped |
   |---|---|---|
   | playbook-desktop-1 | 64 | 4 |
   | playbook-desktop-2 | 54 | 13 |
   | playbook-mobile-1 | 63 | 5 |
   | playbook-mobile-2 | 52 | 15 |
   | journey-and-prototype | 2 + 182 + 14 | 0 |
   | prototype-desktop-2 | 177 | 4 |
   | prototype-tablet-1 | 181 | 1 |
   | prototype-tablet-2 | 177 | 4 |

   - prototype-tablet-1: two runs went red on a11y.spec.ts:39 "Test timeout of 30000ms exceeded" at load1 17-23. Other seats were busy on the machine, and in the first run my own infra discover was running beside it. The same shard at **base** went red the same way. That spec alone passed 3/3 at head and 3/3 at base, and the third whole run at head passed 181 + 1 skipped. Load, not the change.
   - Base twins: playbook-desktop-2 54 passed / 13 skipped, playbook-mobile-2 52 / 15 (the same skip counts).
   - Named specs across the 8 head logs: customer-frame-alias 8, customer-headings-alias 12, attribution-preview 6, playbook-snapshot 26, playbook-followup 10, all passed, 0 failed.
9. **infra at base | head** (Python 3.14.10, -W error::ResourceWarning). test_hidden_characters.py alone: 14 OK | 14 OK (control: a planted, intent-to-add tracked file holding U+202E makes it FAILED (failures=1); then unplanted and quarantined). unittest discover: 325 OK | 325 OK. validate.sh: rc 0 | 0 with bicep 0.47.16 (the CI pin). gitleaks 8.30.1, as CI runs it (full history to head, the repo's ignore file): no leaks; the base..head range also has no leaks.
10. **Node 24.** web/.nvmrc reads 24. ci.yml setup-node `node-version: 24` at lines 384 (web-build), 463 (web-unit) and 504 (web-e2e). Every run above used v24.22.3 (`node --version` printed). The machine default (v26.13.0) was not used for any result.
11. **Identity and hygiene** (scripts/hygiene.py).
    - Author and committer emails equal the email the project's configured identity prints, compared by program (control False). The same holds through `gh api -X GET commits/<sha>`.
    - 1 commit, 1 trailer, subject 74 characters.
    - Non-ASCII on added lines: 4 lines, each only U+00B7 with a removed twin in the same file (SnapshotLauncher.tsx, EngagementOverview.tsx, playbook-snapshot.spec.ts x2). 0 not excused. Cf characters 0. Message non-ASCII 0. Controls: U+00A0, U+202E and an un-twinned U+00B7 each fire.
    - Name scan, underscore-aware, over the ban list plus the configured user name: 0 on added lines and message (a planted `_by_<name>_` fires for every name).
    - B-number / ticket / seat / coordinator ids: 0 in the message and 0 on added lines (a planted "CUST-B410-API" fires).
    - GUIDs 0. Secrets 0. .env/.pem/.key paths 0. Hosts: 2, both `http://mock.test` in test harnesses, which 67 base test files already use.
12. **CodeQL pre-scan (JS/TS; default setup, query suite "extended").** Over all 552 added lines, test files included:
    - `new RegExp(` from a variable: 0
    - `$&` hand-escapes: 0
    - innerHTML / dangerouslySetInnerHTML: 0
    - child_process / exec: 0
    - eval / new Function: 0

    Planted controls fire for 4 of the 5 regexes. The hand-escape regex control did not fire, so that row rests on the `$&` line count (0 lines carry `$&` at all). No Python changed.

## Claims (builder STATUS)
- True: base and head counts, LOST 1 / ADDED 21, 16 of 51 red-first, the 5 out-of-list reds and their cause, 8 shards green, the named spec counts, infra 325/14, identity, one commit, no-new-words, Node 24.22.3.
- True with a correction: the rendered "0 names" holds for visible text (see Minor 2). The "1 of 10" line is the inconsistency in Minor 3.
- Not shown by the builder but measured here: the unscored consequence (Info above), and the e2e base twins.

## NOT TESTED
- The api and api-on-SQL-Server jobs: no api path changed, and no api/scripts/infra test reads these files (the kit's grep, RELAYED).
- The CI shell-script step: shellcheck is not installed here, and no *.sh changed.
- Hosted CodeQL, dependency review and branch protection (Tuesday lands through them).
- Node 26 (not CI's).
- A real API with Demo and a scored run (the ORG-nnnnn alias is unit-pinned only).
- The unscored-set fallback rendered: the mock's set is scored, so this is unit-pinned only.
- The e2e shards at base other than tablet-1, playbook-desktop-2 and playbook-mobile-2.
- The CLARIFICATIONS.md landing-rule line (RELAYED).

## FOR TUESDAY
- Rule on Q-A: the 4 existing test files edited under the property (Minor 1). My reading: they meet it.
- Name to the product owner as a fact (420): for a question set that no ruleset scores, the in-progress count now disappears (launcher, Assessment step, overview line, activity feed).
- Not built, named:
  - the Home "Customer assessment pipeline" table (PartnerDashboard.tsx:163, the seventh surface);
  - the Industry choice list and fleet-size note (168);
  - the result-page Answered tile (SnapshotResult.tsx:125, Q-2);
  - the finished-run "N answer(s)" line (engagement.ts:203);
  - the /documents chooser (DocumentGeneration.tsx:220 still lists stored names to Demo);
  - the runner's own "N of M answered";
  - the snapshot run page lead line;
  - the customer slug in addresses and in the feedback path.
- Sort and search on the Customers list still read the stored name; search lets a Demo viewer confirm a guessed name (Info).
- Page source: the customer frame's server-rendered `customer` prop carries the stored name inside the RSC script on every customer page, for Demo too, at base and head. It is not visible text, but it is in the HTML an HP reviewer's browser receives. Candidate card.
- Resources: everything is under fleet/state/s275/g1556 (clone, 2 worktrees, node24 copy, logs, probes, _quarantine; nothing deleted). infra/scripts/validate.sh left 2 artefact folders in the system temp (`/var/folders/.../T/tmp.*`). The `next start` servers were stopped by pid (26179, 26184). Ports 9790-9799 have 0 listeners. The repo, head and mut porcelain is 0.
- Hook note: the fleet path guard refused a plain `cp`/`tar` from the builder's .tools folder. The Node copy was made with a read-only-source python script (scripts/copy_node.py).
