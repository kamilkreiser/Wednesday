# In Review census — team KS — 2026-09-13 (evening AEST)

**Total In Review: 35** (Linear GraphQL, `state.name = "In Review"`, team KS, one page of 50, `hasNextPage:false`). Matches Wednesday's 17:5x board_count of 35.

| # | Ticket | Title | PR | PR state | head7 | author | Verdict (which / head / at current head?) | TE | Class | Next action | Whose |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | KS-229 | [Tracker] 2026-06-10 platform assurance review — gap-analysi | #785 | merged | 3611f60 | kksecura | none (PR merged 09-10; Peter-approved at head) | Y | **G** | Kam rules whether a TRACKER belongs In Review; ticket's words: 'State unchanged (In Review): KS-229 is the 2026-06-10 platform assurance tracker; this PR corrects one item under it' | Kam |
| 2 | KS-577 | rotate: true mints a new key but never revokes the old one — | #880 | open | 85f8263 | kksecura | none | Y | **C** | Fix Peter's two secuura-api.yaml description lines and push ('I will approve #880 once the two descriptions are corrected'); Stuart has released the PR | ours (builder) |
| 3 | KS-643 | Security: DELETE /api/keys/:id revokes any tenant's key — no | #744 | merged | e3ef478 | kksecura | none (merged 09-01, pre-grant) | Y | **D** | Move ticket out of In Review — its own fix merged in #744 ('This ticket's own fix merged in #744 on 2026-09-01'); #799 is KS-764's sibling PR | ours (ticket write) |
| 4 | KS-657 | services/shared (@secuura/service-utils) cannot build — no t | #720 | open | fcc611d | kksecura | none | Y | **C** | Land Peter's five 2026-08-31 asks ('holding approval rather than withholding'); the retire-vs-wire-up decision the ticket reserves stays open after that | ours (builder) |
| 5 | KS-661 | Rename the `certify` lifecycle verb to `declare` | #736 | merged | a870981 | kksecura | none (merged 08-26) | Y | **D** | Ticket held In Review 'since the retirement is still outstanding' (Stuart's PS-612) — PS-612 is now Done, so verify retirement and move the ticket | ours (verify + ticket write) |
| 6 | KS-663 | The OpenAPI spec is now a consumed contract, but nothing in  | #808 | merged | 3d8b40a | kksecura | none (merged 09-10; Peter-approved at head) | Y | **G** | Peter asked to keep it open: 'Peter (2026-09-08) asked to keep KS-663 open because its third criterion' — builder completes criterion 3 (CI enforcement; coupled to KS-791/#813) | ours (builder), Peter to accept |
| 7 | KS-679 | Published Anchor.id is anc_… but anchoring only ever mints a | #922 | open | 2b5075e | kksecura | none | Y | **C** | Address Peter's three non-substance items ('not approving yet, and none of the three reasons is about the substance') | ours (builder) |
| 8 | KS-693 | M365 routes answer 503 when ENTRA_* is unconfigured — 9 perm | #809 | open | aa2270f | kksecura | none | Y | **B** | Run a QA gate at aa2270f (no review, no verdict, Test Evidence present) | ours (gate) |
| 9 | KS-726 | Write-ahead the Cardano tx hash: persist the deterministic h | #805 | open | 97e2161 | kksecura | none | Y | **G** | Answer Peter's guard-5 breadth question: 'a question rather than a verdict… if you tell me the trade is deliberate I will take your read and approve' | Kam/builder answer, then Peter approves |
| 10 | KS-734 | The e2e Playwright suite cannot run from a clean checkout —  | #920 | open | 2112a99 | kksecura | none | Y | **B** | Run a QA gate at 2112a99 (ticket: 'READY FOR QA. Not merged.') | ours (gate) |
| 11 | KS-736 | Gateway mount-auth check scores authenticateToken(false) as  | #923 | open | d127dc7 | kksecura | none | Y | **B** | Run a QA gate at d127dc7 (ticket: 'READY FOR QA. Not merged.') | ours (gate) |
| 12 | KS-739 | transfer-custody maps a 401/403 from users/lookup to 502 BAD | #919 | open | d0aff46 | kksecura | none | Y | **C** | Address Peter's 'two small, non-code items' ('I have not approved yet') | ours (builder) |
| 13 | KS-754 | updateDSRStatus silently no-ops for any non-uuid actor — ste | #914 | merged | 311dc1a | kksecura | GO WITH FINDINGS @ #914 (2026-09-09-qa-gate-ks754-pr914) | Y | **D** | Move ticket — #914 merged 09-09 (widens processed_by to TEXT), #962 merged 09-12 | ours (ticket write) |
| 14 | KS-763 | Push preflight blocks the whole repo — two qs advisories (GH | #797 | merged | b980f91 | kksecura | none (merged 09-03) | Y | **F** | No OPEN PR. Ticket's words: 'Item 1 of the corrected done-means is on #797…; the ticket stays In Review' — remaining done-means items are unbuilt | ours (builder) or Kam to descope |
| 15 | KS-773 | lockfile-cleanroom skips services/mcp-server for a reason it | #924 | open | b85f1db | kksecura | GO WITH FINDINGS @ 1497b39de (s161 batch 09-09) — head moved to b85f1db (F-924-1 fix + develop merge) | Y | **B** | Re-gate at current head b85f1db | ours (gate) |
| 16 | KS-790 | OAuth authorization_code token exchange uses getUserById (po | #812 | merged | a5542df | kksecura | n/a — #812 is KS-781's PR, not this ticket's | Y | **F** | No PR of its own. Ticket 09-13: the blind pre-auth getUserById 'is still there' at develop b3ce8c9e7 (routes/oauth.ts:799 and :849); formerly BLOCKED on KS-795/796/797 (now UAT/In Progress/Tested) | ours (builder lane) |
| 17 | KS-791 | Publish verify-file (v1+v2) in the spec — coupled with the g | #813 | open | 54225cb | kksecura | none | Y | **C** | Push the LOCAL unpushed minLength commit (ticket: 'in a LOCAL commit that is NOT pushed'); Peter COMMENTED at 54225cb; LEG-14 push hold noted | ours (builder) |
| 18 | KS-799 | The OAuth consent page cannot submit its own form — CSRF ans | #881 | open | 787771b | kksecura | none | Y | **C** | Fix round — Peter CHANGES_REQUESTED at 787771b (KS-798/841 signed off, KS-799 held) | ours (builder) |
| 19 | KS-800 | CLASS: a body parser mounted AFTER the control-byte guard is | #817 | merged | 0750499 | kksecura | re-gate PASS @ 0750499ef (s131) — merged 09-05 | Y | **D** | Move ticket — #817/#818/#828/#836 all merged; residues ticketed as KS-813/KS-816 | ours (ticket write) |
| 20 | KS-804 | Security: POST /api/oauth/authorize's resolver carries ONE o | #823 | merged | 506b450 | kksecura | TIER-1 PASS @ 506b4505e (s131) — merged 09-05 | Y | **D** | Move ticket — #823 and #835 merged; inherited Majors went to KS-822 (merged) | ours (ticket write) |
| 21 | KS-931 | safeOutboundRequest CAN throw while its own contract says it | #873 | open | 7d8a3f0 | kksecura | none | Y | **C** | Fix PR body: Peter 'holding approval on one clerical thing and one number that doesn't match — neither is about the code' | ours (builder) |
| 22 | KS-945 | The install detector enumerates verbs and so fails OPEN — `n | #879 | open | 79f1fcb | kksecura | none | Y | **C** | Push the LOCAL unpushed commit 238f8ad carrying Peter's two test asks (Peter APPROVED at current head 79f1fcb); LEG-14 push hold on #879/#813 noted | ours (builder) |
| 23 | KS-946 | Four path spellings dodge EVERY path-scoped gateway limiter  | #884 | merged | 64e4579 | kksecura | n/a — #884 is KS-858's PR (merged 09-06) | Y | **G** | Kam's second read of the P1→P3 re-price: 'Left open for a second read of the re-price, since it is a security call. My view is that it can then close' | Kam |
| 24 | KS-950 | The boot seed dies permanently at boot 2 — migration 030 dro | #973 | open | ca2a910 | kksecura | NO GO @ dfed981d0 (tier1-r1); round 2 at ca2a910 has NO verdict. (#928: GO WITH FINDINGS @ e28d64b = its current head, but HELD/superseded by #973) | Y | **B** | Gate #973 round 2 at ca2a910 | ours (gate) |
| 25 | KS-961 | The aggregate workspace suite never runs on a PR — wire it a | #887 | open | cb7a3e3 | kksecura | none | Y | **C** | Do the one re-run Peter asked for ('Holding approval on one re-run') and post it | ours (builder) |
| 26 | KS-992 | Both quarantine guards `rm -rf` the directory they may have  | #904 | merged | ba3a072 | kksecura | none (Peter APPROVED; merged 09-09) | Y | **D** | Move ticket — #904 merged; follow-ups live in KS-1027 | ours (ticket write) |
| 27 | KS-1024 | PUSH BLOCKER (repo-wide): two new advisories are unbaselined | #915 | merged | fe0fd64 | kksecura | none (merged 09-09) | Y | **D** | Move ticket — #914/#915/#917 merged; 'the four advisories are GONE, not accepted. PR #915 is on origin' | ours (ticket write) |
| 28 | KS-1027 | KS-992 follow-ups from Peter's #904 review: restore()'s own  | #927 | open | 1041d2d | kksecura | GO WITH FINDINGS @ 63e955e0f (s161) + Peter APPROVED @ 63e955e — head moved to 1041d2d (F-927-1 fix) | Y | **B** | Re-gate at current head 1041d2d | ours (gate) |
| 29 | KS-1043 | PR #811 has no ticket — the PR-status document is a point-in | #811 | open | 6200833 | kksecura | none | Y | **C** | Address Peter's asks on the docs PR ('not approving yet, and I want to be clear it is not about the writing') | ours (builder) |
| 30 | KS-1046 | `PREFLIGHT PASSED.` is printed identically whether 13 legs r | #925 | open | 8a5aff8 | kksecura | GO WITH FINDINGS @ 0956c3dbe (s161) — head moved to 8a5aff8 (F-925-1/2 fixed) | Y | **B** | Re-gate at current head 8a5aff8 | ours (gate) |
| 31 | KS-1057 | api-gateway verify is presence-keyed: confidence reads txHas | #935 | merged | dd9463b | kksecura | GO WITH FINDINGS r1 + r2 (2026-09-10-pr935-round2-tier1) — merged 09-10 | Y | **D** | Move ticket — #935 merged 2026-09-10T11:49Z | ours (ticket write) |
| 32 | KS-1059 | anchorStateSync.ts:360 — removing `inFlight &&` from the KS- | #937 | open | cf8b233 | kksecura | none | Y | **B** | Run a QA gate at cf8b233 (no review, no verdict, zero ticket comments) | ours (gate) |
| 33 | KS-1061 | F-926-2: all ten originate @secuura/shared mock factories we | #931 | open | f2e0cb3 | kksecura | none | Y | **B** | Run a QA gate at f2e0cb3; builder's 09-13 note: #965 merged first with a hand-written root jest.mock — conflict/rebase risk unmeasured | ours (gate) |
| 34 | KS-1068 | threadToken/confidence are written onto the blockchain blob  | #939 | open | 481e026 | kksecura | none | Y | **B** | Run a QA gate at 481e026 | ours (gate) |
| 35 | KS-1078 | SUPPLY CHAIN: the Code Security Gates job downloads an UNPIN | #942 | open | c167626 | kksecura | none | Y | **B** | Run a QA gate at c167626 — PR #942 (feature/ks-1078-tsx-probe-capture) is NOT attached in Linear (record defect: attach it) | ours (gate + attachment) |

## Counts per class (predicate: ticket in state In Review, team KS, classified per the rules in method.md)

| Class | Meaning | Count | Tickets |
|---|---|---|---|
| A | GO'd at current head, awaiting merge (ours) | **0** | — |
| B | PR open, no verdict or verdict on an older head — needs a gate (ours) | **11** | KS-693, KS-734, KS-736, KS-773, KS-950, KS-1027, KS-1046, KS-1059, KS-1061, KS-1068, KS-1078 |
| C | PR open, reviewer asks / findings need a fix round — builder lane (ours) | **10** | KS-577, KS-657, KS-679, KS-739, KS-791, KS-799, KS-931, KS-945, KS-961, KS-1043 |
| D | PR merged, ticket still In Review — record defect, move the ticket (ours) | **8** | KS-643, KS-661, KS-754, KS-800, KS-804, KS-992, KS-1024, KS-1057 |
| E | Peter/Stuart-authored PR — theirs | **0** | — |
| F | No open PR of its own — waiting on stated work | **2** | KS-763, KS-790 |
| G | Needs Kam/Peter/Stuart input by the ticket's own words | **4** | KS-229, KS-663, KS-726, KS-946 |
| | **Sum** | **35** | = 35 total (asserted in build_census.py) |

## Findings that answer Kam's question

1. **Class A is EMPTY.** Nothing In Review is GO'd-at-head awaiting merge. Today's merge queue (#975/#974/#976 GO'd, #978 GO'd 18:00, #980/#981 awaiting gates, #977 awaiting a fix round) sits on tickets that are **In Progress**, not In Review: KS-1126, KS-878/867, KS-876/891/894/895, KS-885/886, KS-924/901, KS-828/900, KS-877/922 (all verified via Linear `issue(id:)`). Only KS-950/#973 is in both sets. So 'In Review' is not the merge queue — it is a mix of stale records (D), gate backlog (B), and Peter-review fix rounds (C).
2. **8 tickets (D) are record defects**: their PR(s) merged between 08-26 and 09-12 and nobody moved the ticket (KS-643, 661, 754, 800, 804, 992, 1024, 1057). The KS workflow has `Tested Not Deployed` / `Deployed to UAT` / `Done` as completed states — which one applies is Kam's call (all eight are merged to develop, and the kintsugi/demo deploy is held per the 09-10 merge notes).
3. **11 tickets (B) need a gate we own** — 7 with NO verdict anywhere (#809, #920, #923, #937, #931, #939, #942) and 4 with a verdict on an OLDER head (#924, #925, #927 from the 09-09 s161 batch; #973 NO GO on r1, r2 ungated).
4. **10 tickets (C) are Peter-review fix rounds** on our own PRs — Peter has commented/held approval and the ball is with the builder; two of those (KS-791/#813, KS-945/#879) have the fix built in LOCAL unpushed commits under the LEG-14 push hold.
5. **Class E is empty**: no In Review ticket carries a Peter/Stuart-authored PR. Peter's only open PR (#959, draft, KS-1096) is In Progress.
6. **4 tickets (G) wait on a human by their own words**: KS-229 (tracker disposition — Kam), KS-663 (Peter asked to keep it open), KS-726 (Peter's design question to us), KS-946 (Kam's second read of a security re-price). **2 (F)** have no open PR: KS-763 (remaining done-means items) and KS-790 (defect still present at develop; its attached #812 is KS-781's PR).

## PRs with NO verdict anywhere (both report trees + launchers)

Open, attached to In Review tickets: **#720, #805, #809, #811, #813, #873, #879, #880, #881, #887, #919, #920, #922, #923, #931, #937, #939, #942**. (#799 has 09-03/09-04 static through-code passes at older heads b36757f7a and earlier — no GO/NO-GO-format verdict, current head 38f6377.) Not attached but in the queue: **#980, #981** (as item 4 stated).

## Verification of item 4 (today's merges) against the API

| Claim | Measured | Agree? |
|---|---|---|
| M7–M10 = #969/#970/#971/#972 merged | merged_at 06:56:51Z / 07:08:34Z / 07:21:55Z / 07:37:12Z, all kksecura; tickets KS-1069/963/941/1052 = Done | yes |
| #978 GO'd 18:00 | open at 13b767a; verdict GO WITH FINDINGS @ 13b767a7f (mail-subject) = current head | yes |
| #975/#974/#976 GO'd awaiting merge | open at 8da20ed/8da6023/0d5f5e6; GO WITH FINDINGS at each current head (#976's verdict is in verdict-mail.md, no mail-subject.txt) | yes |
| #980/#981 READY awaiting gates | open at 9c620f8/04807ea; no verdict in any tree or launcher | yes |
| #973 round 2 READY awaiting gate | open at ca2a910; NO GO @ dfed981d0 (r1); nothing at ca2a910 | yes |
| #977 GO WITH FINDINGS + F1 Major | open at a705858; verdict GO WITH FINDINGS @ a70585823; report.md: 'One Major finding (F1)' — new suite RED on CI | yes |
| (implicit) these are the In Review tickets | **NO** — none of #974–#981's tickets are In Review (all In Progress); only #973/KS-950 is | disagreement |

All `mergeable_state` values on the queue PRs read `unstable` (a failing/pending check), and `unknown` on most older PRs (GitHub had not computed it) — not measured further.
