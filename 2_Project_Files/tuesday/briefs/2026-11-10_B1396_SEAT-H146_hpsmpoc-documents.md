From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail; a launch message that names a mailbox is overridden). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

# BRIEF B1396 | SEAT-H146: HPSM-POC, DOCUMENTS DRAFTER (SONNET): L5 DOCUMENTS, drafts only, NOTHING IS SENT. NEW BRANCH `b1396/hpsmpoc-documents` OF THE ANALYSIS REPOSITORY FROM ITS MAIN (read at Step 0; Tuesday does not stamp a code-repository sha here). PLAIN PUSHES OF THAT REF ONLY, NO PR. NOT MERGED, NOT DEPLOYED.

**BLUF:** lane L5 documents; tickets HPSMPOC-169, 170, 171, 173, 174, 175, 176 (seven drafts, M-L in total); branch `b1396/hpsmpoc-documents` of **`datasecau/HPSM-POC-analysis`** (not the code repository) with your own clone `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1396/analysis`. **Model: SONNET** (documents drafting from sources; the level is written inside the launch line). **Every draft is marked DRAFT in its first lines, every claim carries its provenance, no verbatim text of the statement of work, no name of any customer staff, nothing is sent to anyone.** Ports: **none** (documents; you start no listener). Your STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1396_STATUS.md`. First step is the PRIOR-WORK CHECK and the re-read of what already exists for each deliverable (several are partly drafted in earlier work; extend, do not duplicate).

**Launch (Tuesday):** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H146 "BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '<this kit's path>'"`.

## READ WHOLE FIRST (read-only)
1. The lane plan: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_sweep_drafts/lanes.md` (section L5; the lanes table, the census and the rules every lane carries). Its numbers are the drafter's readings at fa401da9, not yours: re-measure what you cite.
2. The project `CLAUDE.md` and `JIRA.md` (`/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/CLAUDE.md`, `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/JIRA.md`), then `1_Project_Definition/CLARIFICATIONS.md` (settled decisions; supersede, never delete) and `1_Project_Definition/Questions_and_Answers/00_MASTER_QA.md` (before you ask or assert anything about the customer).
3. Template for the holds and the housekeeping: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-09_B1380_SEAT-H136_hpsmpoc-playbook-partner-readiness.md` (builder form); this kit differs only in that the output is documents in the ANALYSIS repository.

## BINDING HOLD
**Nothing goes to the customer.** No send, no mail, no upload, no Jira write (not a comment, not a transition, not a create), no message to any human, no board post. UAT is on hold and nothing deploys: no `az`, no docker, no ssh, no HTTP to any hosted, demo, UAT or production host. You open no PR (Tuesday opens it). Never delete (quarantine to `.tools/b1396/_quarantine/`); no force-push, amend, reset or rebase. **Never type `cd`.** Source documents under `Source_Documents/` and the signed statement-of-work file are customer material: **read-only, never copied, never quoted.** This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only, and are never presented to the customer as done.

## THE DRAFT RULES (each checked by a program you write and print; a control for each that can fail)
1. **DRAFT marker:** the first 5 lines of every new file carry the word `DRAFT` and the line `Not sent. Not approved. For the product owner to review.` (check: `awk NR<=5` per file; control: a planted file without it is reported).
2. **Provenance:** every factual sentence or table row ends with `[src: <path or ticket>:<line or section> | MEASURED|RELAYED|UNMEASURED|TO CONFIRM]`. Program: count sentences/rows without a bracket (expected 0; control: plant one). A figure without an instrument is UNMEASURED and says so.
3. **No verbatim statement-of-work text:** program: take every run of 8 consecutive words of the SOW text (signed copy, extracted by `python3 -I -B` with `zipfile` + XML from the `.docx`, kept in scratch only) and search your drafts for it (expected 0 hits; control: plant one run in a copy and it must be found). Paraphrase with a clause reference only (for example "SOW 4.1.1"), never the sentence.
4. **No person names:** program scan of your drafts for the project's ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite) AND for any personal name you found in the SOW's parties / signature block (extract the names into scratch, scan for them, do not print them into any committed file; control: plant one). Refer to people by role: "the product owner", "the customer", "the Datasec delivery lead".
5. **No secrets, no tenant or subscription ids, no mailbox, no host name of a live system** in any file (scan; control).
6. **Placeholders are labelled** `[PLACEHOLDER: <what, who confirms>]` or `[CONFIRM: <what>]` and are listed at the end of each file; none is filled with a guess.
7. **Own what you do not know:** a statement the code or a source cannot support is written `TO CONFIRM` with who can confirm it, never smoothed.

## THE DELIVERABLES (scope sentences quoted from Jira at drafting; the agent part is lanes.md's, RELAYED, to be re-verified)

### HPSMPOC-171 | output: `1_Project_Definition/Deliverables/2026-11-10_testing-evidence/` | size L
- Jira summary, quoted whole: "[SOW final] Testing evidence and known limitations (one electronic copy)"
- Jira first paragraph, quoted: "BLUF: It is PARTIAL. The evidence exists, but it is scattered across the gate STATUS files and *_evidence folders. The acceptance matrix (design-pack/09) was last re-pointed at 33abe1a. There is no known-limitations document."
- Agent part (lanes.md): Collect the suite results from the gate STATUS files (`Briefs/*STATUS.md`, read-only, on disk in the root working copy) and the `*_evidence` folders; re-point the acceptance matrix (`Architecture/2026-10-01_SOW-deliverables-matrix.md`, read-only); list the open defects with severity from the 2026-11-10 census (the lanes.md BLUF: 144 open issues; an open-defect list is built from Jira REST reads, `project = HPSMPOC AND ( statusCategory != Done )`, read-only). **The frozen build does not exist yet: mark every result "as at <sha8>" and say which sha.**

### HPSMPOC-173 | output: `1_Project_Definition/Deliverables/2026-11-10_phase2-backlog/` | size M
- Jira summary, quoted whole: "[SOW final] Phase 2 backlog document (issued at M8)"
- Jira first paragraph, quoted: "BLUF: It is PARTIAL. The next-phase items live only in Jira (HPSMPOC-92, HPSMPOC-96, the intro video on HPSMPOC-63, the voice mode). There is no issued, prioritised document."
- Agent part (lanes.md): Draft from HPSMPOC-448 to 460 (the Phase 2 layout catalogue), HPSMPOC-92, HPSMPOC-96 and the excluded next-phase tickets that lanes.md lists; **priorities are the product owner's: the draft proposes an order and says in its first lines that it is a proposal.**

### HPSMPOC-169 | output: `1_Project_Definition/Governance/stage-gates/**` | size M
- Jira summary, quoted whole: "[SOW final] Re-base the stage-gate pack and CR log on the signed SOW (10 weeks, new payment dates)"
- Jira first paragraph, quoted: "BLUF: The stage-gate pack (Governance/stage-gates/, HPSMPOC-9) was built on the 23 Sep draft: 12 weeks, M6 at W10, M7 at W11, M8 at W12 plus 30 days. It also quotes draft SOW text. The signed SOW has 10 weeks and different gate dates and payment triggers. Every gate file and the CR log need re-basing before the M1/M2 reviews."
- Agent part (lanes.md): Mechanical re-base of the stage-gate pack and the CR log to the signed dates and clauses (the ticket lists them). The signed statement of work is a git-ignored local file (in the project root as a `.docx`; also look under `1_Project_Definition/Source_Documents/`; which one is the signed copy is UNMEASURED: say which you used and how you know). **Supersede, never delete:** an edit to an existing stage-gate file only ADDS lines (a new adjacent line marked superseded/re-based); program check: every old line of each edited file is present, in order, in the new file (diff shows additions only). New material goes in a new file `Governance/stage-gates/2026-11-10_rebase-on-signed-sow.md`.

### HPSMPOC-170 | output: `1_Project_Definition/Deliverables/2026-11-10_admin-guide/` | size M
- Jira summary, quoted whole: "[SOW final] Deployment and administration guide (one electronic copy)"
- Jira first paragraph, quoted: "BLUF: §4.1.1 lists a deployment and administration guide as a deliverable. It is PARTIAL: infra/README.md is a DRAFT runbook for the first deploy, and README.md explains how to run locally. There is no administration guide (users and roles, rulesets and content, demo reset, feedback route, data subject requests, backups)."
- Agent part (lanes.md): The administration half (users, roles, rulesets, demo reset, feedback route, data-subject requests, backups) can be written from the code and the infra scripts (read-only, a fresh read of the code repository main by `gh api -X GET` or a read-only clone of your own under `.tools/b1396/`). **The deploy half is marked UNVERIFIED until a walk-through on UAT** (UAT is on hold; nothing is verified by running a deploy).

### HPSMPOC-174 | output: `1_Project_Definition/Deliverables/2026-11-10_weekly-report-template/` | size S
- Jira summary, quoted whole: "[SOW final] Weekly written status report to HP (work done + hours, forecast + hours, issues) and weekly working-software review"
- Jira first paragraph, quoted up to its first 330 characters: "BLUF: This is NEW in the final SOW and MISSING. §4.1.5 requires a weekly written status report covering the work done and the Supplier hours spent, a forecast with estimated hours, and open issues. §3.4 accepts the development services through weekly working-software reviews. No hours are tracked today (the 36 SME hours in §6.2" [cut here by the drafter; read the rest in Jira]
- Agent part (lanes.md): A template and an hours-record FORMAT only. Hours data is the product owner's; sending is his. No figures invented: every number cell is a labelled placeholder.

### HPSMPOC-175 | output: `1_Project_Definition/Deliverables/2026-11-10_ai-tools-record/` | size S
- Jira summary, quoted whole: "[SOW final] AI tools: close the two CONFIRM placeholders and keep the record of tools and versions for HP"
- Jira first paragraph: held back by the drafter (it names a person); read it in Jira, the summary above is the scope sentence.
- Agent part (lanes.md): The list of AI tools and versions can be drafted (from the repository, the launchers and the models file `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json`, read-only). **The two CONFIRM placeholders (tenant, no-training) stay open**: they need the product owner and the customer. Nothing is marked confirmed.

### HPSMPOC-176 | output: `1_Project_Definition/Architecture/2026-11-10_privacy-update-draft.md` | size M
- Jira summary, quoted whole: "[SOW final] Privacy documents: Datasec is Data Controller under §5 (update RoPA, DPIA-lite, retention, privacy notice)"
- Jira first paragraph, quoted: "BLUF: The signed SOW §5 makes Datasec the Data Controller for this work's personal data. The design pack still says 'PROPOSED: Datasec is controller … UNDECIDED' (design-pack/security/13_data-classification-and-RoPA.md lines 9 and 56). It is PARTIAL."
- Agent part (lanes.md): Update DRAFTS of the record of processing activities (RoPA), the data-protection-impact assessment lite (DPIA-lite), the retention schedule and the privacy notice. **The controller contact is a labelled PLACEHOLDER until the product owner confirms it.** No legal conclusion is drawn: each statement is "as built" with a source, or "to confirm".

## PARTITION (from both sides; the property: you write a path only if the OWN line names it)
**OWNED by you (L5 documents):** ANALYSIS repository (datasecau/HPSM-POC-analysis), under 1_Project_Definition/: Governance/stage-gates/**, Deliverables/**, Architecture/2026-11-10_* (new files only), Demo/**.

**NOT yours:**
- `1_Project_Definition/CLARIFICATIONS.md` and `Briefs/**` (the records lane R197 owns them; your STATUS file is a channel file on disk in the root working copy and is **not added to your branch**). `Source_Documents/**` (customer material, read-only).
- **L1 web UI (B1392, seat H142)** owns: web/src/components/**, web/src/app/**, web/src/content/**, web/src/server/mock/** (EXCEPT web/src/server/mock/customer-name.test.ts, which is L4's), web/src/styles/**, web/src/assets/**, web/e2e/shell-sidebar.spec.ts, web/e2e/playbook-feedback-pill.spec.ts.
- **L2 web server and lib (B1393, seat H143)** owns: web/src/server/** EXCEPT web/src/server/mock/**, web/src/api/**, web/src/lib/**, web/src/data/**, web/src/design/**, web/src/instrumentation.ts, web/src/proxy*.
- **L3 API (B1394, seat H144)** owns: api/** EXCEPT api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs (L4's, ticket 352).
- **L4 CI and tooling (B1395, seat H145)** owns: .github/** (only the files a ticket of this lane names), infra/**, scripts/**, web/scripts/**, web/e2e/** EXCEPT the two L1 specs, web/src/e2e-runner*.test.ts, web/src/audit-dev.test.ts, web/src/standalone.test.ts, web/src/web-settings.test.ts, web/src/productName.test.tsx, api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs, web/src/server/mock/customer-name.test.ts.
- **L6 records (B1397, seat R197)** owns: ANALYSIS repository: 1_Project_Definition/CLARIFICATIONS.md; the on-disk Briefs/2026-11-09_B1387_STATUS.md (one inserted correction block); Jira project HPSMPOC comments and transitions on the listed keys only.
- **Owned by no lane (nobody touches them in this sweep):** every path that appears in no OWNS line above, for example `web/package.json`, `web/package-lock.json`, `global.json`, config files at the repository root, `.tools/`. Lanes.md MEASURED 61 such tracked paths at fa401da9. If a ticket of yours needs one: do the rest, write `NEEDS-SHARED <path> <why>` in STATUS, and continue.
- **Files the other lanes may be editing at this very moment:** the other builder lanes run in parallel on their own branches; the open pull request list (`gh api -X GET repos/datasecau/HPSM-POC/pulls?state=open`) is re-read at Step 0 and before every push; a file in an open PR that your ticket also needs is named in STATUS and left until that PR lands (the known one at drafting is PR 297, the Demo Walkthrough: 16 files, among them web/src/components/screens/SignInScreen.tsx, UatStartScreen.tsx, web/src/components/shell/AppShell.tsx, web/src/components/walkthrough/**, web/src/content/walkthrough/**, web/src/lib/walkthrough.ts, web/e2e/playbook-walkthrough.spec.ts, web/e2e/walkthrough-uat.spec.ts; read at 03:16 AEDT by `gh api -X GET .../pulls/297/files`).

**Any other shape** (a path not named by the OWN line): STOP that item with `NEEDS-SHARED <path> <why>`.

## CHECKS
None of the code CI jobs apply (no code path is yours; `git diff --name-only origin/main..HEAD` must list ONLY paths under your OWN line, printed in STATUS; control: a planted path outside is reported). The draft rules above are your checks; print each program, its output and its control. Also: markdown renders (every table has a header separator row; every relative link resolves: program), every file is UTF-8 with no tab and no trailing space.
- **PRIOR-WORK CHECK (standing line):** before you draft, list what exists for each deliverable (`ls` of each output folder in the analysis repository main, `git log --oneline -n 12 -- <path>`, `grep -rn -i` for the deliverable's words in `1_Project_Definition/`), the open pull requests of the analysis repository (`gh api -X GET repos/datasecau/HPSM-POC-analysis/pulls?state=open`, `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config`) and any Jira ticket on the topic, read-only, in the form `project = HPSMPOC AND ( text ~ "<term>" )` if you have a reader (else "Jira not searched"; never print a token). A READY without a `## PRIOR WORK` section is returned unread.

## HOUSEKEEPING
- Project dir: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`. Do not use or modify `2_Project_Files/` (stale). Do not edit the root working copy's tracked files (it is read-only to you except for your STATUS file).
- **Your own clone `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1396/analysis`** by URL `git@github.com:datasecau/HPSM-POC-analysis.git`, with the analysis deploy key `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/analysis_deploy_rw` set as repo-local `core.sshCommand` (`git -C <clone> config core.sshCommand "ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/analysis_deploy_rw' -o IdentitiesOnly=yes"`); branch `b1396/hpsmpoc-documents` from `origin/main` (print its sha at Step 0). `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config`, `gh -X GET` only.
- Untracked inputs (the gate STATUS files, `*_evidence` folders, the signed SOW) are read from the root working copy by absolute path, read-only; say in STATUS which ones you read and their `sha256`.
- STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1396_STATUS.md`. FIRST line `PROGRESS B1396: b1396/hpsmpoc-documents HOLD`; a `WORKING: <deliverable>` last line after each part and at least every 20 minutes; sections `## PRIOR WORK`, one section per ticket (what was drafted, sources, the open placeholders), `## HELD`, `## NOT RUN`, and the draft-rule checks with output and controls. **The LAST line, on finish, is exactly `READY B1396: <head sha40>` and nothing after it** (`git rev-parse HEAD` of the pushed branch = `git ls-remote` of it). Otherwise `STOPPED: NEEDS TUESDAY <one question>`.
- **HARD STOP: ____** (absolute AEDT, Tuesday writes it): push what is checked, write what is not. Commit and push after each deliverable (the drive dropped twice on 9 Nov).
- Commit messages: plain ASCII, no B-numbers, no person names, no seat ids; end with the attribution line your session reminder gives. Plain `git push origin b1396/hpsmpoc-documents` only.
- Shell: no `cd`; absolute single-quoted paths (`!CODING` contains `!`); `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a positive control from the same file for every count.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, one question; each count with a control that fires; items 1 and 2 before the clone is created)
1. `/usr/bin/grep -c -E '_''_''_''_'` of your copy of this kit prints 0 on the STAMPED copy (the unstamped copy reads 6 such lines: the HARD STOP, the four Stamp slots and the last line; control: a planted line adds 1); the last line is `READ-WHOLE-BY-TUESDAY: DONE ...`; the HARD STOP above reads a clock.
2. `tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'` is not `Datasec/HPSM-POC-H146` (control `-t %1` prints a different name); `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`.
3. `gh auth status` under `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config` fails (never print the handle), or `repos/datasecau/HPSM-POC-analysis/pulls/99999` is not 404 (control: `pulls?state=open` answers 200).
4. `git ls-remote origin refs/heads/b1396/hpsmpoc-documents` is not empty (STOP naming the sha), or an OPEN analysis-repository PR already touches a path of your OWN line (STOP naming it).
5. `df -g /Volumes/Datasec_DEV` under 25 GiB; or you are about to start a listener (you start none).
6. The signed statement of work cannot be read, or you cannot tell which file is the signed copy: ticket HPSMPOC-169 holds (`HELD (169): no signed SOW`), the other six continue.
7. Any password, token or cookie value visible in a tool result: say "a value was shown", put it first in STATUS and STOP.

## STANDING LINES
PRIOR-WORK CHECK (above). No message to any human. Jira writes: none. Never delete (supersede). Nothing is sent to the customer, ever, by this seat. This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. The records lane R197 edits `CLARIFICATIONS.md` and Jira; you do not.

## Stamp
Tuesday stamps; leave every slot as it stands.
- STAMP: ____
- LAUNCH WINDOW: ____
- Hard stop (absolute AEDT, one clock): ____
- Panes and live seats at the stamp: ____

READ-WHOLE-BY-TUESDAY: ____
