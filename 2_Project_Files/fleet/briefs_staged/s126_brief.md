## BLUF

**You are s126, the SUCCESSOR to s125, rotated by Wednesday at the 50% checkpoint boundary (s125 wrapped 23:43Z, scored 0.90). Your standing queue is s125's handover, unchanged unless this mail says otherwise. The 2026-08-28 run-until-empty grant is IN FORCE (Kam reopened the fleet 2026-09-05 08:1x).**

**Your first item is KS-795 — door 2 of KS-781, the social-callback account-linking branch.** Then KS-796 (door 3), then KS-797, then the standing category-1 queue.

**Read first, in this order:** your own `5_Project_History/history.md` (s125's entry, newest-first — it is your handover), then this mail, then the two QA reports named below.

## STATE YOU INHERIT (verified by Wednesday at 10:5x AEST)
- develop at origin `48641bda3` (#807 KS-788 and #800 KS-731 merged today on Peter's approvals).
- **#812 (KS-781 door 1) @ `da901ffe1` — AT ITS SECOND QA GATE.** No merge before the gate report and Wednesday's GO. **If that gate returns a fix round, it is YOURS and it goes ahead of KS-795.** First report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md`.
- **s125's history.md carries a dedicated #812 cold-seat block** (four-commit chain, every touched file incl. `MFA_CODE_PATTERN` now in the shared gate with `routes/auth.ts` re-exporting it, both suite names and counts, F-1/F-3/F-6/F-7/F-8/F-10 closed, F-9 deferred by ruling, NO reviewer requested — the gate is Wednesday's, not Peter's; a fix round runs INSIDE #812 and ends at READY FOR RE-GATE again). **KS-795 carries the door-2 ruling** with the provider table as rationale and enablement stated as UNASSERTED — establish it from the running env, do not inherit the assumption.
- Peter holds #805, #801, #806, #808–#811 (one consolidated ask, #810 first), #813. Not yours to chase; act only on his comments.
- Stack: 33 containers running (guardian/queue are orphans of an older compose revision — not failures, per s125).
- Two `(conflict_on_2026-09-04)` sync artefacts and three July ones were quarantined by s125 — location in its history entry.

## QUEUE
**0. Plan-confirmation mail to Wednesday** (`[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation`), launcher preflight warnings verbatim, then start item 1 without waiting.

**1. KS-795 — door 2: the social-callback account-linking branch (`routes/auth.ts:887`, link path `:911-918`) mints a credential (full TOKENS, not a code) with no lockout, no status check, no MFA — and links an existing account by `profile.email` alone, reading `profile.emailVerified` only on the CREATE path (`:926`).** Scope this round: (a) the helper split s125 designed — `assertAccountMayReceiveCredential(user, …)`: lockout + status + second factor WITHOUT the password step, **with identifier normalisation INSIDE the shared helper** (the F-1 lesson from door 1: a padded email must never miss the lockout key), and the password path calling it too so there is one gate; (b) **a VERIFIED-EMAIL REQUIREMENT ON THE LINK PATH** — door 2's own defect: facebook derives `emailVerified` from `Boolean(profile.email)` and microsoft-personal hardcodes `true`, and the link path never reads the flag at all, so "trust the flag" is not a requirement; put the provider table on KS-795 and state which providers are enabled per deployment as UNASSERTED (do not read a deployment's env); (c) **#812's 11 cases and the 9-row drift guard must stay green under the split** — that is the red-proof that the split changed nothing on door 1; (d) new cases for door 2 with red-proofs predicted in writing, sets reconciled against the case count (s125's F-8 lesson). **Own branch off `develop` (not off #812) so the two PRs merge independently. Ends at READY FOR QA.**

**2. KS-796 — door 3: `POST /api/auth/wallet/verify` (`routes/wallet.ts:303-337`)** — same helper; **route-contract proofs only, do NOT build CIP-8 signing to prove a probe** (Wednesday's ruling; the runtime probe stays NOT RUN, stated on the ticket); its `status`-never-re-read half needs no signature at all — take that first. Own branch, READY FOR QA.

**3. KS-797 — `POST /api/oauth/authorize` validates neither `client_id` nor `redirect_uri`** (measured by the gate: 302 to an attacker URL with a code minted for an unregistered client). It BLOCKS KS-790 on the board. RFC 6749 §3.1.2.3 / §4.1.1: registered-client lookup, exact redirect_uri match against the registration, 400 before any credential logic. READY FOR QA. (KS-798 — the consent page posting the redirect URI in the `client_id` field — is linked to KS-782 and comes after KS-797; the two share the form.)

**4. Then the standing category-1 queue by priority then identifier.** KS-597/KS-598 stay HELD on Kam's plan-sheet approval. KS-790 stays BLOCKED until all three doors and KS-797 are merged.

## HOLDS (unchanged)
- Signature classes pause for Kam: prod/demo deploys, money, external comms to humans, anything irreversible. The Peter document's SEND is Kam's. Every deploy is Kam's.
- Every round ends at READY FOR QA; Wednesday commissions the gate; no merge before the gate and Wednesday's GO. Peter's review runs in parallel as the ordinary flow.
- Palette: any UI change resolves every colour to the project's style guide; an off-guide literal is a Major.
- Never delete; quarantine. Never `--no-verify` (the exception is spent). A QUESTION goes by MAIL, not the pane — s125 asked twice in the pane and Wednesday found both by capture; the pane is not the channel of record.
- Checkpoint at 50% ctx (finish the task, start nothing that will not fit), rotation inside 70–80% at a boundary on Wednesday's call; wrap by mail `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-05 (s126)`, UNPUSHED FIRST.

PROVENANCE:
- s125's wrap ADDENDUM (the #812 cold-seat block in history.md; the door-2 ruling on KS-795) | `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-05 (s125) — ADDENDUM …` at wednesday-agent@agentmail.to, 2026-09-04T23:46:41Z | read 2026-09-05
- s125's wrap (nothing unpushed; merged/pushed sets with SHAs; the s126 state; NEXT ID KS-795 with the two door-2 requirements) | `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-05 (s125)` at wednesday-agent@agentmail.to, 2026-09-04T23:43:51Z, and s125's history.md entry (your own tree) | read 2026-09-05
- develop 48641bda3 at origin; #812 head da901ffe1 open; #806/#808–#813 open | GitHub API /pulls + `git ls-remote origin` on your repo (read-only) | read 2026-09-05
- KS-795 Backlog/P2 (scope: door 2 — social-callback linking branch mints a credential without MFA/lockout/status), KS-796 Backlog/P2 (scope: door 3 — wallet/verify mints a full token pair without MFA), both sub-issues of KS-781 filed 23:21Z | Linear GraphQL, team KS, parent 781 | read 2026-09-05
- KS-797 Backlog/P2 (scope: authorize validates neither client_id nor redirect_uri; blocks KS-790), KS-798 Backlog/P2 (scope: consent page posts the redirect URI in the client_id field; related KS-782) | Linear GraphQL, team KS, createdAt > 2026-09-04T23:20Z | read 2026-09-05
- KS-781 In Progress/P1 (scope: three token-issuing doors, one ticket; door 1 = #812) | Linear ticket KS-781 description and its 2026-09-04T23:17Z correction comment | read 2026-09-05
- KS-597 Todo/P2 and KS-598 (scope: architecture P1 issuer_organization_id — held on Kam's plan-sheet approval) | Linear ticket KS-597; KS-598's hold per Wednesday's s124 and s125 briefs in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged — my project, not yours | read 2026-09-05
- KS-790 Backlog/P2 UNASSIGNED, blocked by KS-781 (relation + 22:27Z comment) | Linear GraphQL, team KS | read 2026-09-05
- The door-2 provider table, the link-path finding, the door-3 status half, the CIP-8 ruling | s125's READY FOR RE-GATE mail 2026-09-04T23:40:11Z and Wednesday's ANSWER `CORRECTION — #812 closes 1 of KS-781's 3 doors` (2026-09-05 09:3x) | read 2026-09-05
- The gate's F-1 (lockout by whitespace) and F-4/F-5 measurements | `projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md` | read 2026-09-05
- The reinstated grant and Kam's separation principle | Kam's panel messages 2026-09-05 08:1x and 08:39 — my project, not yours | read 2026-09-05

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 09:47
(checked: "own branch off develop, not off #812" against "#812's cases must stay green under the split" — consistent, the split lands in the door-2 branch and the door-1 suite is run against it; "KS-797 after the doors" against "KS-797 blocks KS-790" — consistent, the block is a board relation, the order is the queue; "if the second gate returns a fix round it goes ahead of KS-795" against "your first item is KS-795" — the first is the exception, stated as such.)
