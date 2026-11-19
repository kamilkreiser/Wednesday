# B1750 drafter commission — MPS infrastructure file: make the apply change ONLY what was approved (SEAT-M166)
Commissioned by Tuesday (s293), 2026-11-19. Drafter model: OPUS (routing row C8's exception: the kit is for a change to the
file that replaces every app setting of a hosted site, sign-in settings among them). You DRAFT a builder kit; you run no
`az`, touch no host, build nothing.

THE RULING (read it from the store and quote the card's BLUF and option a's label and detail WORD FOR WORD; keep the card
id OUT of any text the seat writes into the repo, GitHub or Jira):
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show mps-deploy-apply-would-remove-feedback-setting-1119`
(the product owner's tap on the board 2026-11-19 18:39:00, verbatim: "Decision
mps-deploy-apply-would-remove-feedback-setting-1119: a - Fix the settings file first, then deploy once"; ruled in the
store 18:39:18). Option a: a small reviewed code change puts the feedback setting into the file and pins the sign-in ids
and the budget date, so the step changes only what he approved; it merges; then ONE new deploy card with the measured
before-and-after comparison. NOTHING IS APPLIED OR DEPLOYED BY THIS LANE.

Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-19_B1750_SEAT-M166_mps-infra-settings-file-fix.md`
(+ `.measured` sidecar; the drafter report comes back as TEXT in your reply). FORM: the structure of
`2026-11-19_B1741_SEAT-M163_mps-lane-mg-accepted-wording.md` (same folder) and, for infra and its tests, the most recent
MPS kit that edited `infra/**` (find it with ls and grep in the briefs folder; MPSCALC-372's lane put
`MpsCalc__Templates__Path` into `infra/modules/showcase.bicep`: read that kit and its builder STATUS whole, Corrections
first). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole, its 2026-11-19 section included.

INPUTS TO READ WHOLE FIRST: `2026-11-19_B1749_DRAFTER-REPORT.md` (the findings) and the drafted deploy kit
`2026-11-19_B1749_SEAT-D67_mps-hosted-deploy-main-317bbb14.md` (its settings comparison, FACTS and STOP list) with its
scratch `fleet/state/s293/d1749/` (the 17 hosted setting NAMES saved by the 16 November seat and the compare JSON: names
and hashes only; if any file there holds a setting VALUE, do not print it).

SCOPE (state each as a property with its proof; re-measure everything at the CURRENT MPS main, which is now
`e036c9661afab6f4339b53095afd37eb06026d5c` or later: print the sha):
1. **The feedback setting joins the file:** `MpsCalc__Feedback__Path` with the value the site holds today. The value is
   a folder path, not a secret: take it from the project's own record of the 2026-10-13 hand-set
   (`1_Project_Definition/Briefs/2026-10-13_B73_STATUS.md:146`: `/home/data/feedback/`) and from the code's own default
   or docs if they name it; say which source the kit freezes and that the deploy seat later confirms it equals the live
   value by hash.
2. **The two Entra client ids:** today they come from environment variables read by the parameter file
   (`bicepparam:8-9` per B1749) that are absent from the project `.env`, so an apply without them BLANKS four sign-in
   settings. Establish from the files and git history how they were supplied on earlier applies and what the SAFEST
   shape is: (i) the ids written into the parameter file (the file's own comment says tenant and app ids are
   identifiers, not credentials: quote it; but check the repository is private and whether any rule or earlier ruling
   keeps ids out of the repo), or (ii) the apply REFUSING to run when either variable is empty (a `@minLength` or an
   assertion), with the deploy kit supplying them. Recommend one with reasons; if the choice needs the product owner,
   make it a STOP question with a default of (ii) (refuse when empty: it changes no stored value and cannot blank
   anything).
3. **The budget start date:** `budgetStartDate` defaults to utcNow, so each apply moves it. Pin it so an apply does not
   move it (what the budget resource accepts is UNMEASURED without az: say so; choose the shape that makes an apply a
   no-op for the budget and say how the deploy seat proves it by what-if).
4. **A guard so this cannot recur:** a test in the repo's own infra static tests (the python job reads infra files: find
   it) that fails when the set of app-setting names in the infrastructure file differs from a committed list of the
   names the hosted site is expected to hold (the 18 names after this change), so a hand-set setting, or a name dropped
   from the file, turns CI red. The committed list is names only.
5. **The predicted apply difference after this lane**, by program from files: against the 17 hosted names of 16
   November: added `MpsCalc__Templates__Path` only; removed none; changed none. The kit carries that table and the
   builder re-derives it.
6. Docs: the hosted-configuration section of `docs/API.md` or `infra/README.md` if it lists the settings (developer docs,
   corrected from what the file does: C-109 b; quote C-109).
OUT OF THE LANE: any `az` command, any what-if, any apply, any hosted request, any secret, the expired test login, the
subscription-scope question (list it for the deploy card), the template-check caller question (list it), records and Jira.

REQUIRED: PRIOR-WORK CHECK (the tickets that cover this: search Jira for the feedback path, the budget start and the
client ids; MPSCALC-372 and any infra ticket; if none covers it, the kit says "no ticket: the records pass files one"
and the commit subject carries no key or the nearest true key: decide and say why); the lane property (paths owned:
`infra/**` files named one by one, the infra test file, the doc file; lane 1's web paths and everything else NOT yours);
an old-answer census BY PROGRAM of tests that pin the current infra file; every test command quoted from the earlier
infra lane's real run; test selectors checked against the names they must match, Total printed, STOP on 0; predicted
diff measured on a scratch copy; bicep build or lint ONLY if the earlier lane ran one locally without az (else
UNMEASURED and left to hosted CI: say which CI job checks bicep); the landing rule (branch push only; Tuesday opens the
PR; head-pinned squash; 9 checks); gate recommendation G1 OPUS (sign-in settings and a hosted settings file); builder
model: recommend Sonnet C2 or Opus C3 with the reason (a config-shape decision on a sign-in surface is closer to C3).

HOW: read-only everywhere except your kit, sidecar and scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1750/`. Project:
'/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' (code at origin by `gh api -X GET` under the
project's own GH_CONFIG_DIR). NO `az`, no hosted request, no build, no test run, no mail, no Jira write (GET allowed,
credentials by name in-process). `decision_queue.sh` only `show` and `list`. NEVER read `.local/`, `Source_Documents/**`,
a price book, or print any value from an env or key file (the two client ids are NOT printed: name them by variable).
Nothing of HPSM-POC or any other project. No `cd`; no unquoted word starting with `=`; zsh; absolute paths; never
delete; clocks from `date`; every zero with a positive control. `stamp_check.py <kit>` exits 0; Stamp slots unfilled;
ASCII; built whole, temp file, os.replace.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, the shape you recommend for each of scope 1 to 4 with
its reason, the predicted apply difference table, questions that need the product owner (each with a default),
corrections to this commission and to the B1749 report, UNMEASURED.
