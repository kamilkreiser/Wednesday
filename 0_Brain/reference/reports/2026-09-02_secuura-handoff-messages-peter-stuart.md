# Secuura — hand-off messages for Peter and Stuart (2026-09-02, built 21:3x AEST)

**Predicate, stated:** "completed and fully tested by us" = (a) an open PR of ours with its evidence posted (the four-suite SET or, for docs/tests, the unit/QA evidence) awaiting the reviewer, or (b) a ticket merged to develop in *Tested Not Deployed*. Source: Wednesday's own reads at 21:2x — GitHub reviews endpoint for all 32 open PRs (state at head), Linear KS tickets in Tested Not Deployed / In Review (48, paginated to exhaustion) with PR attachments and Platform S relations. **Excluded on purpose (not fully tested tonight):** #790 (KS-695 ask 1 — a Major found by our own code review is being fixed now), #788 (KS-695 ask 2 — one sibling column still to blank), #786 (KS-365 — Peter's requested changes + one gate finding, being fixed), #781 (KS-751 — dirty), #739 (KS-645 — Peter already approved; conflict being resolved, comes back re-requested).

---

## Message for Peter (paste as-is)

Peter — a consolidated list of what is ready for you from our side, so you can plan one pass per stream rather than chase PRs. Everything below has its evidence on the PR (the four-suite SET, or unit + code-review evidence for docs/tests). Nothing here is waiting on us.

**Approved by you, back for a re-look (our re-request, small deltas):**
- #776 — KS-727 errorHandler leak closed as a class (rebased onto develop after #765; your earlier approval was at the old head).
- #784 — KS-659 hot-reload doc citation (one-line anchor fix from our code review; docs only).

**Awaiting your first review — security / tenancy stream:**
- #783 — KS-708 Akto ADD_USER_ID BOLA: similarity tolerance scoped to three templates and five proven endpoints (412 unit tests; amendment closed three code-review findings).
- #764 — KS-726 write-ahead the Cardano tx hash so a lost submit reply cannot orphan a proof (failing-test-first; SET posted).

**Awaiting your first review — docs / process / tests (quick reads):**
- #785 — KS-229 encryptedField header corrected (three users columns ARE encrypted, AAD-bound; old sentence quoted with its date).
- #789 — the board catalogue + "work is organised by stream" policy (DEV-PROCESS + CONTRIBUTING). This one is worth reading first: it is the one-pass-per-stream cadence written down.
- #721 — KS-660 retire the false required-checks section in CLAUDE.md.
- #750 — backlog: two standing reds recorded from the four-suite final check.
- #758 — KS-711 quick_start docs reformatted so the akto + performance quality gate passes.
- #768 — dependabot: drop the github-actions ecosystem (Actions retired).
- #779 — compose: org.opencontainers.image.revision stamped on every built image.
- #773 / #774 / #775 — the QA harness PRs (config-surface walk; KS-578 scope pinned at the real seam; migration 044 against a real Postgres).
- #720 — KS-487 restores the two webhook tests B-1/B-2 and corrects four stale BACKLOG rows.
- #728 — KS-671 anchoring /health reports chain reachability from real calls (you commented; our reply is queued tonight).

**Merged to develop, tested by us, awaiting the demo deploy (no action from you unless you want them in your next test pass):** KS-622 (#745), KS-743 (#778), KS-688 (#749), KS-689 (#748), KS-700 (#752), KS-702 (#754), KS-706 (#755).

**Already done on your side tonight, thank you:** #787 (KS-740) approved at head — we run the SET and merge; #777 approved from our side, yours to merge.

**Coming back to you later tonight, not ready yet:** #739 (KS-645, your approval stands, conflict being resolved), #786 (KS-365, your two blockers + one gate finding), #788 and #790 (KS-695 asks 2 and 1, one finding each from our code review).

---

## Message for Stuart (paste as-is)

Stuart — the K-side items that are done and tested on our side and now sit with you or touch Platform S, grouped so you can take them as a set.

**KS-695 (S↔K erasure by external_ref):**
- Ask 2 — documents.title blanked on erasure: built and tested (#788); one more column is being blanked tonight, then it goes to Peter.
- Ask 1 — POST /api/gdpr/erasures + GET /api/gdpr/erasures/{externalRef}, your paths and envelope unchanged: built (#790); a code-review finding on the failure path is being fixed tonight before Peter reviews it.
- Ask 3 — Kam has ruled the shape: one terminal, synchronous POST. K completes the org erasure and answers "completed" in the same response, and revokes the operational key last, so your client does not need to poll afterwards. Code follows once KS-643 (key-revoke tenancy) merges. If your side wants a different shape, say so before we build.

**KS-566 — shipped on K develop:** your PS-746 tripwire fired as designed; the PS-616 interim can be reverted on your side whenever suits.

**KS-661 — `certify` renamed to `declare`:** live on K develop and demo; PS-658 on your board is the S-side follow-through.

**KS-480 / KS-539 / KS-578 — S↔K ownership, agent document rules, cross-tenant revoke:** K-side work merged and in review; PS-701 / PS-690 / PS-319 are the S-side counterparts — nothing blocks on K.

**KS-721 — the anchor schema accepts your opaque identityCommitment:** merged (#763), in review; the erasure guarantee that goes with it is on KS-695.

**KS-304 — Kam will message you separately on this one.**

---

## Not on either list, and why
- #790 / #788 / #786 / #739 / #781: not fully tested tonight (see the predicate above).
- The nine dependabot PRs (#572–#649): bot-authored, not ours to claim.
- #781 (KS-751 gate): dirty, on the queue.
- Anything in In Review with no PR attached (KS-676/677/678): work in progress, nothing for a reviewer yet.
