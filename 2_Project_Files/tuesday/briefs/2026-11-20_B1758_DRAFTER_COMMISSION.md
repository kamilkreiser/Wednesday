# B1758 drafter commission -- MPS records pass for PR 218, PR 219, PR 220 and the hosted deploy of 2026-11-20 (SEAT-R281)
Commissioned by Tuesday (s295), 2026-11-20. Drafter model: Sonnet (routing row C8).
Draft ONE records kit `2_Project_Files/tuesday/briefs/2026-11-20_B1758_SEAT-R281_mps-records-218-220-deploy.md` (+ `.measured`;
return the drafter report as TEXT, Tuesday saves it) in the FORM of `2026-11-19_B1722_SEAT-R274_mps-records-216.md` (read it
whole, as STAMPED, and its STATUS `!CODING/Datasec/Datasec MPS Commercial Calculator/1_Project_Definition/Briefs/2026-11-19_B1722_STATUS.md`,
Deviations and Corrections first: fold each in by name). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole, its
2026-11-19 section included (selectors checked against the names they must match; every total recomputed from its parts;
every count of a list the kit prints counted by program; no predicted number unmeasured).

Facts to re-measure at source (repo datasecau/MPS-Commercial-Calculator, MPS GH_CONFIG_DIR, GET only):
- PR 218 (MPSCALC-316) squash -> e036c9661afab6f4339b53095afd37eb06026d5c. Review: G2 GO WITH FINDINGS (find its verify
  folder by grep of the briefs folder for 218 and 316; its finding F4 names lines 1450 and 1454). MPSCALC-316 gets ONE
  comment and STAYS OPEN (say what remains, from the ticket's own scope sentence).
- PR 219 (MPSCALC-267, the projection table, lane 1 of the v13 plan) squash -> 73eef991b4582beb06ce79f189813b82074a9793.
  Review `2026-11-19_B1752_verify/VERDICT.md` (read WHOLE). Builder STATUS `.../Briefs/2026-11-19_B1746_STATUS.md`. The
  ten words: `.../Briefs/2026-11-19_B1746_WORD-PACK.md`. Records: MPSCALC-267 comment (state by the project's own rule:
  quote it from the project CLAUDE.md as the form does); docs/ENGINE.md line 166 went stale (a docs follow-up); the
  fixture comment over-claims (Minor).
- PR 220 (the infrastructure settings-file fix; NO ticket exists: search first, then ONE create that records it as done)
  squash -> 50d2a47195957a8b0c914ab2972d0dc703f9bee3. Review `2026-11-19_B1754_verify/VERDICT.md` (read WHOLE; findings
  F1 to F6) and `FOR-THE-DEPLOY-CARD.md`. Builder STATUS `.../Briefs/2026-11-19_B1750_STATUS.md` (its Corrections name two
  kit errors of Tuesday's stamp: a total of 123 where the parts sum to 122, and 'seven anchor counts' where the kit holds
  thirteen blocks: record both).
- THE HOSTED DEPLOY of 2026-11-20: `.../Briefs/2026-11-19_B1755_STATUS.md` (242 lines; read WHOLE; last line DEPLOYED:
  50d2a471... live-check 0). Its section "For the records seat" is the seat's own draft of the history line, the BACKLOG
  candidates and the C-entry: check each sentence against the STATUS sections it summarises, never copy it unread.
  Authority to quote: the product owner's tap on the live board 2026-11-20T09:11:03.072+11:00, verbatim with the dash in
  ASCII: 'Decision mps-hosted-deploy-main-50d2a471-1119: a - Deploy now, words approved as written, seller checks skipped
  again'; print the card with `bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show
  mps-hosted-deploy-main-50d2a471-1119` (that one id; `list` is forbidden) and quote option a's label and detail word for
  word; the earlier rulings it stands on are named in the deploy kit `2026-11-19_B1755_SEAT-D68_mps-hosted-deploy-main-50d2a471.md`
  Step 0.4 (print each with show before citing it; check client_project is this project).
  To record plainly: the seller checks and the template restart check were NOT run, by that ruling; the what-if showed the
  budget start date as a Modify in written form only and nine site-config deltas, which the seat classed as known noise
  and applied, with the read-back confirming (quote the STATUS What-if section); who sees the Projection table on the
  hosted site is unmeasured; no rendered screen was looked at.

Scope of the kit: the C-entries (next free numbers and section, by program: one for the three changes, one for the deploy,
or as the form's practice says), the Jira comments above, the history PR (branch `records/b1758-history`, the project's
history file only, as the form does), and follow-up tickets, EACH SEARCHED FIRST (state the search and its control; a found
ticket on the same subject = no create, name it):
 (a) `infra/README.md` line 46: the runbook step now stops without the two ids (review F2); (b) the budget start literal
 blocks a FIRST create after October 2026 (F3); (c) `infra/tests/test_infra.py` cannot see an expression's value: pin the
 computed settings (F4); (d) the apply-time length rule is unmeasured (F6, M6 not run); (e) docs/ENGINE.md line 166;
 (f) the Dependabot notice of 1 high alert on the default branch: READ it (gh api, GET) and say what it is; ticket only if
 no ticket holds it. Fold two into one where they are one fix in one place, and say why.
Who decided: the deploy is the product owner's (his tap, quoted). Landing #218, #219, #220 on a review GO, the ids made
unblankable and not written into the repository (Q1 of the B1750 kit), and every ticket priority are the coordinator's,
written as such. No other ruling is cited unless you print its card with show and its project is this one.
Read-only everywhere while drafting; Jira GET only, credentials in-process by name; no az; no request to the hosted site;
nothing of any other project; NO HPSM-POC anything. Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s295/d1758/`.
No `cd`; no unquoted word starting with `=`; zsh; absolute quoted paths; never delete; clocks from `date`. stamp_check
exits 0; slots unfilled; ASCII; temp file then os.replace.
First line of your reply: STARTABLE: YES|NO - why. Then: files, recommended slots, the searches for each create,
corrections to this commission, D/Q defaults, UNMEASURED.
