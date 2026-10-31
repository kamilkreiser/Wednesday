STARTABLE: YES (after Tuesday stamps: 9 four-underscore lines; D-8 GRANTED or REFUSED must be written in the stamp; Q-1 to Q-8 to answer)

# B1016 drafter report (SEAT-H89, HPSMPOC-388, customer security preview part B), drafted Sun 2026-11-01 05:05 to 05:5x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1016_SEAT-H89_hpsmpoc-388-security-workspace-part-b.md` (146 lines; sha256 `b33dc51d982639658357fac3556072167a220c96d940178d2f00e38d37406fea`), and its exact copy `.md.pre-stamp` (`cmp` equal, same sha256). Seat `Datasec/HPSM-POC-H89`, ports 9400-9409, branch `b1016/hpsmpoc-388-security-workspace-part-b` off main `77c3132e`. Shape copied from part A's kit B937 (stamped, 157 lines) and B1002 (unstamped copy, 104 lines; its drafter report read). Model row C2 line 92, `claude-sonnet-5-5`, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes.

## BLUF
- **What it builds.** Four read-only views (Gaps and findings, Remediation roadmap, Reports and evidence, Continuous assurance) on part A's pattern. Each is a 12-line page plus a view that renders through `SecurityView`. They are appended to `SECURITY_VIEWS`, so part A's no-write, no-price and alias harnesses walk them with no new loop.
- **The findings rule.** Every finding comes from `data.reviewed`, part A's single reviewed-only rule. No part-B file filters findings itself.
- **Roadmap.** It shows only ACTIONS tied to at least one reviewed finding, and lists only those reviewed findings. Owner and status are read from the remediation register (the browser `sessionStorage` store) with the same key and fallbacks the partner screen uses. The register is never written, and a spy plus a byte-equal check of the stored value proves it.
- **Reports.** "Issued and approved" means the latest issued, not-withheld report whose OWN executive-summary source is `ai-approved` or `ai-edited`. For the held customer it means `factsFor` reportIssued + narrativeApproved + report present. A failed read is never shown as a release. There is no content link.
- **Assurance.** Three tiles ("Not connected", "Not scheduled"), as the phase-scope ruling requires.
- **One data change.** One additive field (`actions`) in `useSecurityData.ts`, proven by part A's gate plants p18, p18b and p18h staying red.
- **The tail (D-8), outside the ticket's Files line.** One line each in `nav-dead-ends.test.ts` (floor 5 to 1) and `proxy.ts` (the unknown-id 404 alternation gains the four slugs), plus the two `VIEWS` lists in `proxy.test.ts` and `proxy.auth.test.ts`. Without the proxy line, an unknown id on a part-B view answers HTTP 200. HPSMPOC-411 fixed exactly that defect for part A.
- **Words.** 13 new customer-visible strings: 10 are design v1.2 text verbatim (line cited for each) and 3 are page titles made by part A's "&" to "and" rule. Everything else is imported from main by name.

## Facts re-measured (instrument; control)
- **Main:** `gh api -X GET git/ref/heads/main` = `77c3132e213b24616e6f1af9379d2fee66c889b7` (2026-10-31T16:12:30Z, #268). Open PRs 0 (control: the closed list prints 268, 267 and 266). `matching-refs/heads/b1016` 0 (control: `heads/b101` lists `b101/four-wordings`). Of 281 `heads/b*` refs, the only names matching `388|part-b|security` are `b37/security-scans` and `b937/...-preview-a` (control: `387` matches 1). `.tools/b1016` absent (control: 5 `b1002` names). Repo `allow_*` squash/merge/rebase all true. The last four main commits are single-subject squashes. Part A landed as a head-pinned squash (analysis CLARIFICATIONS line 4860).
- **Tickets (Jira GET through `.tools/b649/jira.py` by path; nothing printed but text):** HPSMPOC-388 Backlog, 0 comments, read whole. -387 and -377 each have 2 comments (landing and UAT deploy `e8ac3f29`). -393 is `gather` "NOT to be built". -410, -411, -414 and -415 were read (part A gate residue): -411 and -415 landed by #265, -414 by #262. JQL `project = HPSMPOC AND ( text ~ "security workspace" OR text ~ "continuous assurance" OR text ~ "security preview" OR text ~ "part B" )` gives 42 issues. On this ground the hits are only -387, -388, -393, -410, -411 and -415. Control `text ~ "zzqxnonexist"` gives 0, and `key = HPSMPOC-388` gives 1.
- **Code at `77c3132e`** (gh tarball, scratch): 31 files and 1492 lines of part A. `SECURITY_VIEWS` lists 3 views. `customer-nav.ts` has 5 `built: false` entries (one is held). `nav-dead-ends.test.ts:26` reads `>= 5`, and every `MAIN_NAV` entry is built, so after part B the count is 1. `proxy.ts:29` `(dashboard|fleet|assessments)`; `proxy.test.ts:42` and `proxy.auth.test.ts:78` `VIEWS` hold 3 views. `returnPath.ts:9` already holds "security". No e2e spec mentions `/security` (`grep -l` rc 1; control: `customers` gives 15 lines in `shell-sidebar.spec.ts`). The register: `remediation-store.ts` (96 lines), keyed by route id and action id (`RoadmapScreen.tsx:66-88,153`).
- **Reports:** `Report.narrativeSources` and `withheld` (`schema.gen.ts:1782`). The API's selector maps an `edited` narrative to `ai-edited` (`NarrativeReview.cs:59-78`). `latestReport` and `issuedLine` are exported from `ServiceReport.tsx:27,33`, `factsFor` from `engagement.ts:67` and `narrativeFacts` from `:82`. The held draft rule is at `ReportScreen.tsx:56`. The mock has no report service (`showcase-summary.ts:11`).
- **CI:** `ci.yml` at `77c3132e` is blob `0176b491` with 679 lines, the same blob B1002 measured. Line numbers were re-read by grep: 14-18 `on:`, 371 web-build, 390/395/396/409/413/426, 450/478 web-unit, 483/515 web-e2e, 526 `web`, 629-657 gitleaks 8.30.1. `package.json`: lint `eslint --max-warnings=0`, typecheck `next typegen && tsc --noEmit`, test `vitest run`, build `node scripts/build.mjs`.
- **A trap found:** the no-price pattern (`security.no-price.test.tsx:27`) has `AUD` with the `i` flag, so it matches inside "audit". The design's "External distribution" sentence ("... audit integration ...") would turn AC 3 red, so D-7 drops it.
- **Rulings (analysis repo `CLARIFICATIONS.md` at main `0a33f395`, 5017 lines):**
  - line 2672, phase scope (2026-10-23): "current phase of work does not require integration into any of these tools ... careful not to do too much in this phase (that we show to HP)".
  - line 4684, design v1.2: "Build all except the three held pieces"; Framework alignment is one of the three.
  - line 1904, the Done rule.
  - line 4860, part A's landing.
  - The words rulings (C-39, C-40, C-107, C-120, C-149, C-190) are per-string approvals; none covers part-B strings.
  - The sweep's own fence: "Any label that is not in the product owner's v1.2 design is NEEDS-WORDS".
- **Style:** `1_Project_Definition/Design/design-system.md` says every colour is a `tokens.css` or `brand.css` token, and severity is shown with text plus shape. The kit binds tokens only, the existing info/warning tokens for notices, and no design greys.
- **Ports:** a word-boundary census of 4-digit 9xxx tokens over the 47 non-`.pre-` SEAT kits dated 10-31 and 11-01 found 30 decades named; 9400-9409 is not one of them. `grep -l -w -E '940[0-9]'` over those kits gives rc 1; control `941[0-9]` hits the B1009 kit. `lsof -nP -iTCP:9400-9409 -sTCP:LISTEN | wc -l` read 0, then 2 with a `python3 -I -B` listener on 9401 (6 s), then 0 again.
- **Panes** (`tmux list-panes -a`, 05:1x): `%0` tuesday, `%131` `Datasec/HPSM-POC-R103` (B1014, records), `%130` `Datasec/MPS-R102`, `%1` fleet-monitor. No H89. load1 was 2.75 at 05:13 and 1.72 at 05:16.
- **Model:** `model-routing.md` row C2 at line 92 (printed by grep with C3:93, C4:94, G1:108, G2:109, G-cap:111). `models_latest.json` line 23 `claude-sonnet-5-5`. `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`.
- **Kit checks:** 9 four-underscore lines (135-142 and 146; control: a scratch file with four underscores reads 1 in prior kits). `@X@` markers 0. Non-ASCII lines 0 (control: a planted e-acute reads 1). Name forms (kam, kamil, kreiser, pete, peter, paul) 0. `C-<n>` tokens 0. Card-id shapes 0 (control: `hpsmpoc-hosted-runtime-1018` is caught).

## D-decisions (in the kit; summarised)
- **D-1** The roadmap shows actions tied to at least one reviewed finding.
- **D-2** Owner and state fall back the way the partner screen does.
- **D-3** "Issued and approved" uses the report's own `narrativeSources`. The held rule is from `factsFor`. A failed read means not released.
- **D-4** No report content link.
- **D-5** Assurance is three tiles with no answer-derived count.
- **D-6** No assurance cycle panel or next-steps list.
- **D-7** No "External distribution" card (the "audit" trap).
- **D-8** The tail: the floor 5 to 1, the proxy alternation, and the two `VIEWS` lists. It is GRANTED or REFUSED at the stamp; if refused, the seat stops with the floor row red.
- **D-9** Sonnet; target READY 240 minutes, hard stop 360.

## Q-questions for Tuesday (default first)
- **Q-1 Words: is a words card needed before shipping?**
  - **Default: NO card. Build with the 13 strings of kit item 7.** 10 of them are design v1.2 text verbatim; the sweep's fence and the 2026-10-29 "implement the design" ruling make design text approved. 3 are titles by part A's "&" to "and" rule (part A shipped "Fleet and devices" for "Fleet & devices"; gated, landed, on UAT).
  - **The new strings:**
    - Titles: "Gaps and findings", "Reports and evidence", "Continuous assurance".
    - Findings: "Security finding register".
    - Roadmap: the roadmap notice "Roadmap timing buckets are proposed priorities, not service commitments. Implementation requires customer approval, model suitability and formal change control."; "Owner:"; "Status:".
    - Reports: "Customer security review report"; "Not released"; "A customer report will become available after a consultant has reviewed findings, approved the executive narrative and issued the report in the eight-step assessment journey."
    - Assurance: "Last live fleet sync"; "Next assurance review"; "Not scheduled"; "Cadence requires agreement".
  - **Say "card" if** the product owner wants to see the 13 before they show on UAT. The roadmap notice and the "Not released" sentence are the two most prominent. "eight-step" is a factual claim the kit makes the seat measure (`WORK_STEPS.length` = 8), with a STOP if it is not 8.
  - **Alternative titles:** use the design's own heads ("Reviewed risks & gap analysis", "Prioritised remediation roadmap", "Reports & assessment evidence", "Continuous improvement") instead of the menu labels. Not the default: part A used menu-label titles.
- **Q-2 D-8 grant (the proxy and floor tail outside the ticket's Files line):** **default GRANT.** Without it the suite cannot go green (the floor row), and unknown ids on the four new views answer 200, which is a regression of HPSMPOC-411's fix. The alternative is to refuse, have the seat stop with the row red, and ticket the proxy line.
- **Q-3 Roadmap shape: default D-1** (actions tied to reviewed findings). The alternative is one row per reviewed finding, which is the design's literal shape, but the register is keyed by action, not finding.
- **Q-4 Owner/state with no saved entry: default D-2**: the action's own owner, else "Not recorded"; the state is "Not started", matching the partner screen. The alternative is "Not recorded" for both.
- **Q-5 "Approved": default D-3**, the report's own executive-summary source is `ai-approved` or `ai-edited`. `edited` is the API's reviewed-with-edit state. The alternative is to also require the CURRENT narrative to be approved (`narrativeFacts`).
- **Q-6 Report content link: default NONE (D-4).** The alternative is a plain link for a caller known to hold no Demo, mirroring `ServiceReport`.
- **Q-7 Assurance cycle panel and next-steps list: default NOT built (D-6)**, under the phase-scope ruling. The alternative is to build them as design text, which adds about 12 more strings.
- **Q-8 Gate: default tier 1 (G1, line 108), Opus first, round 1 of 2 on a NEW class "customer security preview, part B".** Part A's class closed at round 2 of 2 with a GO WITH FINDINGS (B965). If Tuesday counts part B as the SAME class, the cap is already spent and a NO GO goes straight to the product owner.

## UNMEASURED
- Nothing was run: no worktree, npm, test, build or browser.
- The unit count at `77c3132e` (part A's head printed 3325).
- Whether `WORK_STEPS.length` is 8. The comment at `engagement.ts:92` says "Step 3 of 8"; the seat measures it, and REFUSE stops it if the count differs.
- Whether `customer-text.test.ts` accepts the 13 strings. The drafter read its patterns: none matches doc-path, decision-number, person, seat, SOW, hash, schema, version or build-note forms.
- Whether a register owner (free text typed by a consultant) can carry a real customer name to a Demo viewer. The kit has the seat report it under Open.
- The jsdom hydration of `remediationStore.use()` in the new tests (the kit points at `RoadmapScreen.register.test.tsx`).
- Mock-mode reports. The mock has no report service, so the browser evidence shows "Not released" for API customers, and released reports are proven by unit rows and the canned harness only (kit NOT TESTED).

## Outside-the-fences disclosure
- **Read-only:**
  - `gh api -X GET` under the project's `GH_CONFIG_DIR`: main ref, commits, pulls, matching-refs (281 refs), repo settings, one compare (`32fc1750...77c3132e`, the kit's control), a tarball of `77c3132e`, and the analysis repo's main ref plus raw `CLARIFICATIONS.md`.
  - Jira through `.tools/b649/jira.py` (run as a script and imported by path in a `python3 -I -B` JQL reader in my scratchpad). Its `show()` prints comment author display names to my scratch file; none is copied into the kit.
  - Local reads: part A's and B1002's kits and reports, the B937 STATUS (FOR TUESDAY and sections), the B965 STATUS by grep, `design-system.md`, the design file (`python3 -I`, four functions), `model-routing.md`, `models_latest.json`, `brief_seat.sh:24`.
  - Tools: `lsof`, `tmux list-panes`, `uptime`, and a 6-second loopback listener on 9401 (self-exiting).
- **Not done:** no git verb in the project repo, no `cd`, no hosted HTTP, no `decision_queue.sh`, no card read, no mail, no Artifact or Docs tool.
- **Not opened:** `HP Reporting and Docs/`, any SOW, `Source_Documents/`, `inbound/`, and every WEDNESDAY/FRIDAY tree.
- **Writes:**
  - The kit, its `.pre-stamp` copy (made with `cp -p` and checked by `cmp`, not with the Write tool) and this report.
  - Scratch files under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2aa17213-e9fb-4717-99d9-8efe0dc321ab/scratchpad/`: the tarball tree, jira text, JQL reader, CLARIFICATIONS copy and refs list. That scratch folder already held unrelated files (MPS sources, a `ci.yml`, `tree.txt`) from an earlier use; I did not touch them.
- **Hooks:** one Bash call was refused for containing `cd`; it was re-run without it.
