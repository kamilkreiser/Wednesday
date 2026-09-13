# method.md — In Review census, KS, 2026-09-13

Read-only throughout. No Linear mutation, no GitHub write, no comment, no mail, no `cd`. Credentials sourced by NAME (`LINEAR_API_KEY`, `GH_TOKEN`) from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`; no value printed or written. Scripts + raw pulls sit beside this file (`linear_pull.py`, `gh_pull.py`, `verdicts.py`, `build_census.py`, `linear_raw.json`, `gh_raw.json`, `gh_comments.json`, `verdict_index.json`, `queue_ticket_states.json`).

## FOUND
- Linear: 35 issues, team KS, `state:{name:{eq:"In Review"}}`, `first:50` + `after` cursor; page 1 returned 35 with `hasNextPage:false` (`linear_raw.json.pages`). Same figure as Wednesday's 17:5x board_count (35) — no difference to explain.
- GitHub: 51 open PRs in `Secuura/Distributed_Secuura` (`pulls?state=open&per_page=100&page=1` returned 51 < 100 → listing proven unbounded, one page). 10 are dependabot, 1 is PeterObeden's draft #959 (KS-1096, In Progress), 40 are kksecura.
- 52 distinct attached PR URLs across the 35 tickets (51 in Distributed_Secuura + 1 in `Secuura/platform-s#623`, which the token cannot read → 404, recorded, not classified — KS-661's S-side half, PS-612 is Done).
- One ticket (KS-1078) has NO attachment; the open-PR listing found its PR by branch name (`feature/ks-1078-tsx-probe-capture` = #942).
- QA verdict record lives in TWO trees, not one: `Testing Agent MAIN/projects/secuura/reports/` (119 dirs; names carry `<tickets>-<pr>-<head>-tier<n>-r<n>` only from 09-06 on) AND `Testing Agent MAIN/projects/secuura-blockchain/reports/` (18 dirs, incl. the 09-09 `s161-batch-six-prs` that gated #924/#925/#926/#927/#928/#929). Only 11 of 119 dirs in tree 1 carry a `mail-subject.txt`; the rest carry the verdict inside `report.md` or `verdict-mail.md` (#976), and three #962 dirs are evidence-only.
- 63 files in `WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/` (second index); no launcher exists for any of the 18 no-verdict PRs.

## TESTED (controls)
- Positive: dir-name matcher returns `2026-09-13-ks885-886-978-13b767a7f-tier2-r1` → GO WITH FINDINGS for #978 at 13b767a7f, and `2026-09-13-ks950-962-973-dfed981d0-tier1-r1` → NO GO for #973 at dfed981d0 (from report.md; the dir has no mail-subject.txt). Both as briefed.
- Negative: PR 99999 matches no dir name, no report body, no launcher; GitHub `pulls/999999` → 404.
- Pagination: Linear final page `hasNextPage:false`; GitHub listing final page short (51 < 100).
- Item-4 claims each re-read from the API (merged_at, head sha, state) and the report trees — table in census.md; one disagreement (the queue's tickets are In Progress, not In Review).
- Head-equality: every verdict's pinned head7 compared to the PR's CURRENT `head.sha[:7]`; 4 open PRs have a verdict only on an older head (#924 1497b39de→b85f1db, #925 0956c3dbe→8a5aff8, #927 63e955e0f→1041d2d, #973 dfed981d0→ca2a910).
- Review withdrawal check: reviews listed per PR with last state per reviewer; the only APPROVEDs on open PRs are Peter on #879 (at current head 79f1fcb, with two test asks stated in a follow-up comment — an approval with asks, not a withdrawal) and Peter on #927 (at 63e955e, head since moved). CHANGES_REQUESTED on #881. All other Peter reviews are COMMENTED; his substantive reviews are posted as PR *issue comments*, which is why `review_thread_count` is 0 on every PR — the inline-thread endpoint returned empty lists (checked on #799/#887), not errors.
- Test Evidence: `^#+ .*test evidence` (case-insensitive) or `**Test Evidence` in the PR body. Present on every kksecura PR attached here except #714/#717 (old, merged) and #917 (superseded duplicate of #915); absent on all dependabot PRs.

## HOW (classification rules as applied)
- Exactly one class per ticket; precedence when several could fit: G (ticket's own words name a human) > D (its own PR merged, no remaining work stated) > A (GO at current head, open) > B (open, no verdict at current head, no reviewer ask outstanding) > C (open, reviewer/gate findings awaiting a builder) > E (non-kksecura author) > F (no open PR of its own; remaining work stated).
- D refined: applies when the ticket's OWN fix PR is merged and the ticket does not state remaining work. KS-661 is D because the stated blocker (PS-612) is Done. KS-763 and KS-790 are F, not D, because their words state unbuilt work (KS-790's attached #812 is KS-781's PR, and the ticket says the defect is still present at develop b3ce8c9e7).
- G quotes are verbatim from the ticket/PR comment named in the row.
- "ours" = a Secuura seat under the 2026-09-11 grant (kksecura-authored PRs); gate = QA seat; ticket write = a Secuura seat with Linear write, NOT this census.

## NOT MEASURED
- KS-661's Platform S half (`platform-s#623`): token 404s; PS-612 state (Done) taken from Linear only.
- `mergeable_state` beyond reading it (`unstable` on the queue PRs = a failing/pending check; `unknown` on most others); which check fails was not read. CI check-runs not read.
- Whether the 4 older-head verdicts would survive a re-gate (a fix ride-along + develop merge changes the tree; only a gate can say).
- KS-1061/#931's rebase risk against merged #965 (stated by the builder, not measured).
- The remaining "done-means" items on KS-763 beyond item 1 (the corrected list in the 09-02 comment was read; which items are still open was not enumerated).
- Whether KS-790's former blockers (KS-795 Deployed to UAT, KS-796 In Progress, KS-797 Tested Not Deployed) still block it.
- Report-tree verdicts before 09-06 (s96–s135 dirs) were grepped by PR number only; their verdict wording predates the GO/NO-GO format and was not normalised.
- Linear `history` (who moved which ticket when) was not pulled; the D rows rest on PR merged_at vs. ticket state, not on transition logs.
