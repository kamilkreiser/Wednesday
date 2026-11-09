From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail; a launch message that names a mailbox is overridden). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

# BRIEF B1393 | SEAT-H143: HPSM-POC, BUILDER (OPUS): L2 WEB SERVER AND LIB. NEW BRANCH `b1393/hpsmpoc-web-server-lib` FROM MAIN fa401da9f7bdab21c46ad9717c964433a2d22650. COMMITS AS NEEDED, PLAIN PUSHES OF THAT REF ONLY, NO PR. NOT MERGED, NOT DEPLOYED.

**BLUF:** lane L2 web server and lib; tickets HPSMPOC-234, HPSMPOC-235, HPSMPOC-228, HPSMPOC-343 plus the follow-up named below; branch `b1393/hpsmpoc-web-server-lib` cut from main fa401da9f7bdab21c46ad9717c964433a2d22650 (main was `fa401da9f7bdab21c46ad9717c964433a2d22650` at drafting, 2026-11-10 03:16 AEDT by `gh api -X GET repos/datasecau/HPSM-POC/branches/main`; PR 297 may land before launch, so Tuesday stamps the branch point). **Model: OPUS** (the level is written inside the launch line below). **Size: M.** Seat id H143. Ports **9710-9719** only. Your STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1393_STATUS.md`. First step is to **re-read main and close as already-fixed (with evidence) every ticket or sub-item main already fixes**; then fix only what is still open.

**Launch (Tuesday):** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H143 "BRIEF_SEAT_LEVEL=opus WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '<this kit's path>'"`. `brief_seat.sh` defaults to Opus; the level is written inside the quotes.

## READ WHOLE FIRST (read-only)
1. The lane plan this kit was cut from: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_sweep_drafts/lanes.md` (read whole; it is the drafter's reading at fa401da9, MEASURED marks only for what it says it ran; **every file:line in it is a pointer you re-print with `grep -n` or `awk NR==n` at your own clone before you rely on it**).
2. The project's `CLAUDE.md` and `JIRA.md` (`/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/CLAUDE.md`, `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/JIRA.md`; read-only), and the CI workflow of your clone, `.github/workflows/ci.yml` (print the predicate of each job in CHECKS).
3. The template this kit follows: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-09_B1380_SEAT-H136_hpsmpoc-playbook-partner-readiness.md` (its holds, partition and housekeeping bind you as written below).

## BINDING HOLD
UAT is on hold (the product owner, 2026-11-06 10:12) and HPSM-POC deploys nothing. You touch no hosted host: no `az`, no docker push or registry login, no ssh, no HTTP to any hosted, demo, UAT or production host (not even a GET). **You open no PR; Tuesday opens, gates and lands it through CodeQL (never bypass, never dismiss an alert).** No Jira write (not a comment, not a transition, not a create); no message to any human. Never delete (quarantine to `.tools/b1393/_quarantine/`); no force-push, amend, reset or rebase. **Never type `cd`** (a hook refuses it). `.github/**` is touched only by lane L4 and only the files its tickets name (that is not you: never). This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. Nothing is built for the Phase 2 catalogue (tickets 448 to 460): it is not to be made now.

## STEP 0: RE-READ MAIN, THEN CLOSE WHAT MAIN ALREADY FIXES (before any edit)
1. Clone by URL into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1393/repo` (see HOUSEKEEPING), check out `origin/main`, print `git rev-parse HEAD` and compare with the branch point fa401da9f7bdab21c46ad9717c964433a2d22650 (if main has moved on from it, say so; your branch is cut from the stamped point or a later main, whichever Tuesday's stamp names; a commit between the two that touches your OWNED paths is named in STATUS).
2. For EACH ticket below, read the ticket's cited lines **at your clone's main** and decide: `STILL OPEN` / `PART FIXED` (name which sub-items) / `FIXED AT MAIN`. Lanes.md already names **109, 228, 271, 318, 399, 323** as likely stale and says that 431, 405, 234, 235, 99 and 322 may be partly built (tickets 109, 271 and 318 are the records lane's). Do not trust that either way: read.
3. A ticket (or sub-item) that main already fixes is **not re-built**. You write it in STATUS under `## CLOSED WITH EVIDENCE`, one line each, exactly `CLOSED-WITH-EVIDENCE HPSMPOC-<n> [<sub-item>]: <what main shows> | <file:line printed by grep -n at <sha8>> | <instrument> | <control that can fail>`. **You never write this to Jira**: the records lane (seat R197) reads your STATUS and posts the comment. A ticket the records lane cannot read from your line is not closed.
4. Only tickets or sub-items still open proceed to THE WORK. If NOTHING is open, finish with the section, no branch push beyond an empty-change note, and the READY line naming the branch head = main (say so).

## THE TICKETS (scope sentences are quoted from Jira at drafting 2026-11-10 by the project's Jira REST read, status Backlog for all; fix shapes are lanes.md's, RELAYED, to be re-verified)

### HPSMPOC-234
- Jira summary, quoted whole: "[B182 Q-B182-2] Web-side warm-up after a start: the first render and the first BFF→API connections are paid by the first person"
- Jira first paragraph, quoted: "BLUF: After a hosted start, nothing warms the web app. Its first page render and its first connections from the BFF to the API happen on the first person's request. B181 measured /home at 4,043 ms on its first GET. The read warm-up that went live with d323981 is API-only by design."
- Files at fa401da9 (lanes.md): `web/src/server/auth/warmup.ts`, `web/src/instrumentation.ts`, `web/src/server/bff.ts`
- State at main and why it is agent work (lanes.md): `auth/warmup.ts` and `signin-warmup.test.ts` exist at main (lanes.md MEASURED by path), so part may be built; read first. The code half is agent work (a start-up GET with no session and no non-GET, with a test). Closing needs the hosted measurement (HPSMPOC-309, excluded): the seat ends at "code merged, ticket stays open".

### HPSMPOC-235
- Jira summary, quoted whole: "[B182 Q-B182-3] BFF→API connections: keep them open longer, or open them before a burst (bursts after an idle reach the API as a staircase)"
- Jira first paragraph, quoted up to its first 330 characters: "BLUF: On hosted, a burst of reads waits before it reaches the API, and the wait grows with how many NEW BFF→API connections the burst needs. After 6-8 s of quiet, a burst of 8 reads reached the API one after another. The median wait before the API was 1,100 ms (range 190-4,351), while inside the API the reads took a median of" [cut here by the drafter; read the rest in Jira]
- Files at fa401da9 (lanes.md): `web/src/server/bff.ts`, `bff.keepalive.test.ts`
- State at main and why it is agent work (lanes.md): `bff.keepalive.test.ts` exists at main, so this may be built (UNMEASURED); read first. Same closing rule as 234.

### HPSMPOC-228 (likely stale or partly stale: read main first)
- Jira summary, quoted whole: "[B176 gate notes on B175] Site timing follow-ups N-2..N-9: dead readiness-PDF named write, R11 guard blind to the dispatcher timer, routeTemplate lowercase segments, refresh fan-out, warm-up log level, words, stale comment"
- Jira first paragraph: held back by the drafter (it names a person); read it in Jira, the summary above is the scope sentence.
- Files at fa401da9 (lanes.md): `web/src/server/bff.ts`
- State at main and why it is agent work (lanes.md): **N-2 (dead readiness regex) and N-4 (lowercase route segments) are fixed at main**: `NAMED_WRITES` has four entries and none is readiness; `routeTemplate` keeps only `ROUTE_WORDS` (`bff.ts:161-165,275-277`, lanes.md MEASURED). N-3 (R11 guard blind to the dispatcher timer) sits in an infra or API test lanes.md could not locate (UNMEASURED): it is in no lane; report it if you find it, do not edit it. Open: refresh fan-out, warm-up log level, words, stale comment.

### HPSMPOC-343
- Jira summary, quoted whole: "[B570-7] Which fields does the API refuse for the browser sites in session.ts, override.ts and action-plan.ts: trace the HasControl call sites (Note, read-only, gate B570)"
- Jira first paragraph, quoted up to its first 330 characters: "BLUF: gate B570 (GO WITH FINDINGS, round 1 of 2) read the builder list of sibling trim() sites and found its claim about which fields the API refuses incomplete: FollowUpShape.HasControl is also called at api/src/HpsmPoc.Modules.Assessment/Endpoints/Requests.cs:146 (customer name), :221 and :224 (answer notes and text values)" [cut here by the drafter; read the rest in Jira]
- Jira done-when line, quoted: "Done-when."
- Files at fa401da9 (lanes.md): read-only: `web/src/lib/session.ts`, `web/src/lib/override.ts`, `web/src/components/partner/action-plan.ts` against `api/.../Requests.cs:146,221,224`
- State at main and why it is agent work (lanes.md): A read-only trace. The output is a TABLE in your STATUS (section `## TRACE HPSMPOC-343`, one row per browser site: file, line, the field sent, the endpoint, whether the API refuses that field, the instrument) handed to the records lane for the Jira comment; **no code change**. `action-plan.ts` is under lane L1's directory: read it, never edit it.

### FOLLOW-UP (c), no Jira key: `web/src/lib/dates.test.ts` fails on Node 26 ICU ('Jul' vs 'July')
- Files: `web/src/lib/dates.test.ts` (the 'July' expectation at line 36, lanes.md MEASURED; re-print it), `dates.ts` does the formatting.
- Local only (RELAYED: lanes.md did not run Node 26; the repository's pinned Node is the CI Node). Fix by making the assertion independent of the ICU short-month spelling, or by pinning the formatter. **Prove it on Node 24 (`.tools/node24` in the project) and on Node 26**; if Node 26 is not installed on this machine, say NOT RUN and prove the reasoning by a second assertion that fails on a planted 'Jul' and a planted 'July' alike. (The product must not change for a test's sake: if the formatter is what changed, say so.)

## PARTITION (from both sides; the property: you edit a path only if one OWNS line below names it as yours)
**OWNED by you (L2 web server and lib):** web/src/server/** EXCEPT web/src/server/mock/**, web/src/api/**, web/src/lib/**, web/src/data/**, web/src/design/**, web/src/instrumentation.ts, web/src/proxy*.

**NOT yours (every other lane's paths, lanes.md both sides):**
- **L1 web UI (B1392, seat H142)** owns: web/src/components/**, web/src/app/**, web/src/content/**, web/src/server/mock/** (EXCEPT web/src/server/mock/customer-name.test.ts, which is L4's), web/src/styles/**, web/src/assets/**, web/e2e/shell-sidebar.spec.ts, web/e2e/playbook-feedback-pill.spec.ts.
- **L3 API (B1394, seat H144)** owns: api/** EXCEPT api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs (L4's, ticket 352).
- **L4 CI and tooling (B1395, seat H145)** owns: .github/** (only the files a ticket of this lane names), infra/**, scripts/**, web/scripts/**, web/e2e/** EXCEPT the two L1 specs, web/src/e2e-runner*.test.ts, web/src/audit-dev.test.ts, web/src/standalone.test.ts, web/src/web-settings.test.ts, web/src/productName.test.tsx, api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs, web/src/server/mock/customer-name.test.ts.
- **L5 documents (B1396, seat H146)** owns: ANALYSIS repository (datasecau/HPSM-POC-analysis), under 1_Project_Definition/: Governance/stage-gates/**, Deliverables/**, Architecture/2026-11-10_* (new files only), Demo/**.
- **L6 records (B1397, seat R197)** owns: ANALYSIS repository: 1_Project_Definition/CLARIFICATIONS.md; the on-disk Briefs/2026-11-09_B1387_STATUS.md (one inserted correction block); Jira project HPSMPOC comments and transitions on the listed keys only.
- **Owned by no lane (nobody touches them in this sweep):** every path that appears in no OWNS line above, for example `web/package.json`, `web/package-lock.json`, `global.json`, config files at the repository root, `.tools/`. Lanes.md MEASURED 61 such tracked paths at fa401da9. If a ticket of yours needs one: do the rest, write `NEEDS-SHARED <path> <why>` in STATUS, and continue.
- **Files the other lanes may be editing at this very moment:** the other builder lanes run in parallel on their own branches; the open pull request list (`gh api -X GET repos/datasecau/HPSM-POC/pulls?state=open`) is re-read at Step 0 and before every push; a file in an open PR that your ticket also needs is named in STATUS and left until that PR lands (the known one at drafting is PR 297, the Demo Walkthrough: 16 files, among them web/src/components/screens/SignInScreen.tsx, UatStartScreen.tsx, web/src/components/shell/AppShell.tsx, web/src/components/walkthrough/**, web/src/content/walkthrough/**, web/src/lib/walkthrough.ts, web/e2e/playbook-walkthrough.spec.ts, web/e2e/walkthrough-uat.spec.ts; read at 03:16 AEDT by `gh api -X GET .../pulls/297/files`).

**Any other shape** (a path not named by any OWNS line): prove it is yours by one of the OWNS lines above or STOP that item with `NEEDS-SHARED <path> <why>`.

## CHECKS (the CI predicates for your paths; read `.github/workflows/ci.yml` at your clone and print each job's pass predicate into STATUS; lanes.md read them at fa401da9)
- `web-build`: `npm audit --omit=dev --audit-level=high`; `node scripts/audit-dev.mjs`; lint; `npm run typecheck`; build; `node scripts/e2e.mjs --check-shards`.
- `web-unit`: `npm test` (vitest): `bff*.test.ts`, `auth/*.test.ts`, `lib/*.test.ts` run and pass.
- `web-e2e (<shard>)`: a `bff.ts` change also runs the e2e shards that call the BFF (find them by program from the shard plan, print the list).
- Run each at **main** and at **your head**, compared **by program** (counts side by side: tests passed/failed/skipped, lint/typecheck rc, build rc). A red that is not yours is named with its cause **at main too** (same command, same counts). Run heavy jobs serially within your seat (load is noisy). In `ci.yml` a step printing "SKIPPED" (typecheck, unit tests, infra) is NOT a pass.
- `secrets` (gitleaks, full history) and `dependency review` must stay green: you add no dependency and no secret.
- **Every new test you add is proven RED with your fix removed (in a copy) and GREEN with it**, both shown in STATUS.
- **PRIOR-WORK CHECK (standing line):** before you build anything, `git log --oneline -n 12 -- <each file you will touch>`, `grep -rn` the repository for the ticket's distinctive words, the open PRs (`gh api -X GET`, `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config`), and read-only Jira searches in the form `project = HPSMPOC AND ( text ~ "<term>" )` (with the parentheses) if the project has a reader (it has none for builders: write "Jira not searched" if you have none; never print a token). A READY without a `## PRIOR WORK` section is returned unread.

## HOUSEKEEPING
- Project dir: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC` (the NEW drive; anything naming `/Volumes/Laptop-DEV` is stale and that drive is not mounted). Do not use or modify `2_Project_Files/` (a stale checkout).
- **Your own clone `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1393/repo`** by URL `git@github.com:datasecau/HPSM-POC.git`, with the deploy key `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/github_deploy_rw` set as repo-local `core.sshCommand` (`git -C <clone> config core.sshCommand "ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes"`). Never touch another seat's `.tools/b13NN/` or `.tools/b139N/` folder. `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config` for every `gh` call, `-X GET` only.
- **Ports: your block is 9710-9719 and nothing else.** Before any listener: `lsof -nP -iTCP:9710-9719 -sTCP:LISTEN` must print 0 rows (at drafting, 03:2x AEDT, it printed 0 rows for 9700-9739; the drafter also scanned the non-`.pre-` SEAT kits of 9 and 10 Nov for these numbers, see the drafter's report line in the reply). Name the port in every start command; stop your servers before READY; a listener outside the block is a STOP.
- STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1393_STATUS.md`. FIRST line `PROGRESS B1393: b1393/hpsmpoc-web-server-lib HOLD`; a `WORKING: <part>` last line after every part and at least every 20 minutes; sections `## PRIOR WORK`, `## CLOSED WITH EVIDENCE`, `## HELD`, `## NOT RUN`, then the change list (every file changed), each ticket's outcome, every check with its predicate and counts at main and head. **The LAST line of the file, when you finish, is exactly `READY B1393: <head sha40>` and nothing after it** (the sha is `git rev-parse HEAD` of your pushed branch, and `git ls-remote` of the branch equals it). If you cannot finish: the last line is `STOPPED: NEEDS TUESDAY <one question>`.
- **HARD STOP: 10:30 AEDT 2026-11-10** (absolute AEDT, Tuesday writes it): push what is green, write what is not. The drive has dropped twice on 9 Nov: **commit and push as soon as a ticket is green.**
- Commit messages: plain ASCII, no B-numbers, no person names, no seat ids; say what changed and why in plain words; end with the attribution line your session reminder gives (nothing else added). One logical change per commit; plain `git push origin <branch>` of YOUR branch only.
- Shell: no `cd`; absolute single-quoted paths (`!CODING` contains `!`); `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a positive control from the same file for every count (a zero is a suspect until a control fires); a `file:line` is printed by `grep -n` or `awk NR==n` at the sha you cite, never remembered.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, one question; each count with a control that fires; items 1 and 2 before the clone is created)
1. `/usr/bin/grep -c -E '_''_''_''_'` of your copy of this kit prints 0 on the STAMPED copy (the unstamped copy reads 6 such lines: the HARD STOP, the four Stamp slots and the last line; control: a planted line adds 1); `/usr/bin/grep -o -E '@[A-Z_0-9]+@' <copy> | wc -l` prints 0; the last line is `READ-WHOLE-BY-TUESDAY: DONE ...` and not four underscores; the HARD STOP above reads a clock.
2. `tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'` is not `Datasec/HPSM-POC-H143` (control `-t %1` prints a different name); `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`.
3. `gh auth status` under `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config` fails (never print the handle), or `repos/datasecau/HPSM-POC/pulls/99999` is not 404 (control: `pulls?state=open` answers 200).
4. `git ls-remote origin refs/heads/b1393/hpsmpoc-web-server-lib` is not empty (the branch exists: someone ran this kit; STOP naming the sha), or your clone is dirty.
5. `df -g /Volumes/Datasec_DEV` under 25 GiB, or you are about to start a listener outside 9710-9719, or `lsof` shows a listener in 9710-9719.
6. A file your ticket must change is OWNED by another lane (PARTITION) or is changed by an open PR: not a stop for the whole kit, a STOP for that item (`NEEDS-SHARED`), the rest continues.
7. Any password, token or cookie value visible in a tool result: say "a value was shown", put it first in STATUS and STOP.

## STANDING LINES
PRIOR-WORK CHECK (above). No message to any human. Jira writes: none (the records lane R197 does them). Never delete (quarantine). This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. Nothing hosted: the landing, CodeQL and any deploy are Tuesday's and the product owner's. Landing rule for the code repository, quoted from the project's CLARIFICATIONS (the gate seat re-printed it at `:3617`): "The landing form is a head-pinned squash" (Tuesday lands; you never merge).

## Stamp
Tuesday stamps; leave every slot as it stands. Branch point `fa401da9f7bdab21c46ad9717c964433a2d22650` is replaced everywhere it appears.
- STAMP:  main fa401da9f7bdab21c46ad9717c964433a2d22650 read by gh api at 03:32 AEDT 2026-11-10 by the Tuesday successor seat (after s260)
- LAUNCH WINDOW:  from 03:32 AEDT 2026-11-10, through launch_when_cool
- Hard stop (absolute AEDT, one clock):  10:30 AEDT 2026-11-10
- Panes and live seats at the stamp:  %0 Tuesday, %1 shell, %11 H147 (B1398 #297 CI fix), %12 D56 (B1391 UAT deploy), H142 (B1392) launching

READ-WHOLE-BY-TUESDAY: DONE 03:32 AEDT 2026-11-10 (Tuesday successor seat after s260)
