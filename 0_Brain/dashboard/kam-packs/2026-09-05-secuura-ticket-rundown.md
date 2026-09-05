# Secuura / Platform K — ticket rundown for Kam

Measured 2026-09-05 14:01 AEST from the KS board (Linear, exhaustive pagination, 216 unarchived tickets) and the GitHub PR list (32 open, review states read per PR at head). Read-only, Wednesday's seat. Every set below is listed by identifier; counts are of the listed sets.

## BLUF
- **Actioned since yesterday morning (09-04 00:00 AEST): 44 tickets touched, 21 new tickets filed (KS-781 → KS-801), 2 PRs merged to develop by the agent on Peter's approvals (#807 KS-788, #800 KS-731), 2 Platform S PRs merged by Kam (PS #759, #760), 6 PRs opened (#808–#813), 1 closed as superseded (#764).** The KS-781 authorize security fix is built for door 1 (#812, at its fourth QA gate now), doors 2 and 3 are built on branches, and the client_id/redirect_uri open redirect (KS-797) has code landed.
- **Being worked on now: 16 In Progress, of which 5 are live with the agent this hour** (KS-781, KS-797, KS-795, KS-796 In Review, KS-790 blocked behind KS-781). The other 11 In Progress are earlier work, last touched 09-03.
- **Waiting on the team: 15 of our PRs sit with Peter as requested reviewer with no approval at head; 9 tickets sit in Peter's testing states (Deployed to UAT / Tested Not Deployed); 3 P1 tickets are Blocked (two assigned to Peter); 20 tickets are assigned to Peter and 8 to Stuart, none done.** Neither has commented on the board since 09-04 00:00 AEST; Peter's only recent words are five extranet replies asking which PRs are live. Two of Peter's own PRs (#792, #802) were pushed after our change requests and now wait on OUR re-review — that goes to the agent's queue.
- **Archivable: 1 ticket now (KS duplicate); the completed half is ALREADY archived. Deferred candidates come from the 92 Backlog tickets and need a text-by-text catalogue — the agent delivers it after the #812 fix round; by title alone only 2 are explicitly parked (KS-329 Phase 2 PQC hybrid, KS-692).** So expect a judgement set, not a large number. Unmeasured until the catalogue.

## 1. Actioned (since 09-04 00:00 AEST)
**Merged to develop (`492152a81 → 48641bda3`):** #807 (KS-788, the npm-advisory timeout — Tested Not Deployed) · #800 (KS-731, per-slot Postgres/Redis credentials — ticket still In Review, state not advanced; leg-5 re-run rc 0 first). **Kam merged on Platform S:** PS #759 (PS-761), PS #760 (PS-754).
**PRs opened:** #808 KS-663 · #809 KS-693 · #810 KS-792 (advisories expiring 09-06) · #811 the PR-status document · #812 KS-781 door 1 · #813 KS-791. **Re-requested to Peter:** #806 (rebased, his approval is now stale by design), #801. **Closed:** #764 (superseded by #805).
**Security work built (not merged):** KS-781 door 1 (#812 — MFA + lockout on authorize; three QA gates so far, fix round for the fourth in hand) · KS-795 door 2 tests @ e13c77131 · KS-796 door 3 READY FOR QA @ 6741d3a9d · KS-797 code @ 42848145f (green unmeasured).
**Tickets filed (21):** KS-781 KS-782 KS-783 KS-784 KS-785 KS-786 KS-787 KS-788 KS-789 KS-790 KS-791 KS-792 KS-793 KS-794 KS-795 KS-796 KS-797 KS-798 KS-799 KS-800 KS-801.
**Also touched (44 total, current state):** In Review 12 · Backlog 18 · In Progress 6 · Todo 6 · Tested Not Deployed 1 · Deployed to UAT 1.

## 2. Being worked on
**Live with the agent (s127) now:** KS-781 (P1, #812 fix round → re-gate 4 → merge on Wednesday's GO) · KS-797 (P2, measure then finish) · KS-795 (P2, rebases after #812) · KS-796 (P2 In Review, gate after #812) · KS-790 (P2, blocked-by KS-781 on the board).
**In Progress from earlier sessions (last touched 09-03), 11:** KS-256 (OpenAPI examples) · KS-487 (Review B — assigned Kam, touched 09-05) · KS-575 (Peter: Schemathesis lockout) · KS-601 (Kintsugi dev server) · KS-664 (deepmerge-ts override) · KS-665 (KS-256 follow-ups) · KS-669 (spec URLs on unowned domains) · KS-687 (Akto slot targeting) · KS-695 (S↔K erasure, K-side) · KS-762 (APP_DB_PASSWORD default) · KS-764 (decideKeyRevoke org arm — #799 frozen on Peter) · KS-771 (review stream: build/supply-chain/release gates).
**In Review, 48** — the bulk is merged-or-PR'd work inside Peter's review streams (KS-770/771/772/485 process). Full list on the board filter `state = In Review`.

## 3. Waiting on the team
**Our PRs with Peter requested, no approval at head (15):** #720 KS-487 · #721 KS-660 · #750 backlog docs · #758 KS-711 · #768 dependabot config · #793 KS-365 follow-up · #799 KS-764 (frozen at b36757f7a) · #801 KS-775 · #805 KS-726 · #806 KS-731 shell suites (his earlier approval is stale — he must re-approve) · #808 KS-663 · #809 KS-693 · #810 KS-792 (**advisories expire 2026-09-06 — first in the ask**) · #811 the status document · #813 KS-791.
**Ours needing OUR action, not Peter's:** #785 (approved twice by Peter but pushed onto since; no reviewer requested — re-request) · #728, #773 (no reviewer ever requested — request or close) · #812 (deliberately unrequested until its gate passes).
**Peter's PRs waiting on us:** #792 and #802 — we requested changes 09-04; both heads moved after; our re-review is due. #803 (KS-682) — our CHANGES_REQUESTED stands at head; waiting on Peter.
**Peter's testing states (9):** Deployed to UAT — KS-740 (P0 rfc3161 timeouts) · KS-667 (P1 migration 033) · KS-727 · KS-742 · KS-743 · KS-578 · KS-622 · KS-689; Tested Not Deployed — KS-788.
**Blocked (3, all P1):** KS-441 (Peter — Akto CI throughput) · KS-608 (Peter — systemTest integration mode) · KS-660 (CI suite jobs die in 3 s).
**Assigned to Peter, not done: 20. Assigned to Stuart, not done: 8.** Zero comments from either on the board since 09-04 00:00 AEST. **Dependabot PRs open: 10** (nobody's, all stale since 08-20/08-31).

## 4. Archivable
- **Now: 1** — the one `Duplicate` (the only completed-type ticket outside Peter's testing states).
- **Already done:** every `Done` / `Deployed To Prod` / `Canceled` ticket is already archived (KS-691 and KS-779 return only with `includeArchived`).
- **HOLD from archiving (Peter may still be testing): 9** — the Deployed to UAT / Tested Not Deployed set above.
- **Deferred candidates: the 92 Backlog tickets (P2 38 · P3 45 · P4 9).** A ticket is archived-deferred only if its own text says not-now (commercialisation, later, when X lands). By title alone, 2 qualify (KS-329 "Phase 2 — JWT RS256 → hybrid"; KS-692). The agent's text-by-text catalogue — every proposed ticket with its `RESURFACE WHEN:` line — comes to Wednesday after the #812 fix round, then to this panel as a set. The unarchive path Kam can click: label `parked-resurface`, include archived.

## Not measured / limits
Peter's and Stuart's extranet replies are not on the board and are not counted as communication (Kam's rule 13:55). "Actioned" = `updatedAt` since 09-04 00:00 AEST — it includes state moves by the projectise pass, not only code. Review states are from the GitHub reviews endpoint at head; a requested reviewer with no review is "waiting", whatever the extranet says.
