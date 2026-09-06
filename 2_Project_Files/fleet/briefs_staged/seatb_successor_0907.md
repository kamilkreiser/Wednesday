# SEAT B successor brief — Secuura / Blockchain (Platform K), 2026-09-07 morning

You are seat B. Your predecessor **s140e wrapped 2026-09-06 23:57 and scored 1.0** — it took F5 from
"measured in a copy" to CONFIRMED on the real running gateway, ran the control that could have
destroyed its own result on a fresh boot, and corrected its own MFA evidence downward in the same
message. Wednesday is a fresh coordinator seat (09-07 morning), successor to the seat that rotated at
23:59. Your standing queue is below; nothing merges without a gate and Wednesday's GO.

## BLUF
**Your first act is to CLOSE OUT F5's coverage on the LOCAL booted gateway — never the demo box — and
then hand Wednesday the F5 FIX OPTIONS as a decision, not a fix.** s140e confirmed the login limiter
bypass on 2 of 8 protected routes on the real gateway; the other 6 look identical and it refused to
claim them. Confirm them locally, then design options (the obvious "canonicalise the URL before the
guard" turns one bypass into a general one — that is exactly the shape to enumerate, not to pick).

## THE FLOOR — verify from objects at your own seat, READ verbs only
- **origin/develop was `306d0db923183f3b62b053f0242549e37bdf362c`** at the 23:40 handover (source:
  s140e wrap mail, DKIM-verified). Your local develop is STALE. **`ls-remote` is the only honest ref
  — re-read it in the same action before trusting any SHA, including this one.**
- **Seat A (s141b) is RUNNING in its own worktree on KS-945** (the install-verb / package-manager
  guard). **Its file family is not yours.** You work gateway/auth (F5) in YOUR OWN git worktree.
  Conflicts are the partition's failure — reported, never merged through (Kam's 09-06 09:42 parallel
  grant).

## THE QUEUE — in order
1. **F5 coverage completion (P1).** Boot the gateway + auth LOCALLY in your own copy. Drive the four
   spellings (`//mfa/disable`, `%6Dfa`, `mfa;x=1`, `mfa%2Fdisable`) against the remaining 6 of 8
   protected routes, canonical spelling as the control, severity per result. **NEVER drive a bypass
   against anything deployed / the demo box — whether a deployed system carries this code is KAM's
   question, not a probe you take.**
2. **F5 fix OPTIONS as a decision doc for Wednesday → Kam.** Enumerate the options with their blast
   radius (the pre-guard canonicalisation is the dangerous one — say why); recommend, do not pick.
   **KS-733 must NOT close as if the 450x gap were fully shut** — F5 is a limiter-layer question, not
   just MFA.
3. **KS-486 bounded sweep** (11 tickets, 9 unexamined; 2 of 2 checked were stale — suggestive, not
   evidence). Cold-startable.
4. **KS-946 remedy OPTIONS** (a decision, not a build; the remedy constraint is in its description).
5. **The six inferred mounts.**

RULED BY KAM, NOT YET IN AN ARTEFACT
Kam's two live desk cards (both on HOLD):
- **Demo admin default password** — HOLD. **Nothing on the demo identity moves.** -> lands when Kam rules the card.
- **F5 disclosure to Peter/Stuart** — HOLD; timing is Kam's, tied to the F5 fix options above. You do
  not communicate with any client human; that is Kam's signature class. -> lands on the review-stream ticket once Kam rules.

Older Secuura rulings the delivery gate flags as still-undelivered — carried verbatim so a reader lands
on them. **Most are KAM-ACTIONS or "leave"/"wait", NOT seat-B build work; Wednesday will put their
disposition to Kam at the morning sweep. Do NOT act on these beyond noting them:**
- **secuura-ci-billing** (ruled 'wait' 2026-08-26): "Leave until the team cost discussion lands" — GitHub Actions stays dead (billing); fleet is push-only, gates run via the QA agent, not Actions. -> Kam's billing action.
- **secuura-agent-github-identity** (ruled 'identity' 2026-08-26): "Create an agent GitHub identity in the Secuura org; from then on Kam approves" -> Kam's one-time org action + the agent launcher's PAT/deploy-key switch.
- **secuura-dependabot-triage** (ruled 'close-and-rescope' 2026-09-01): "Close the 5 workflow-only dependabot PRs + scope dependabot away from github-actions" -> Peter's repo config / a Kam-or-Peter action, not a seat-B build.
- **secuura-ks229-disclosure-mailbox** (ruled 'later' 2026-09-02): "Leave the branch staged; KS-229 stays open, no PR" -> no action; waits on Kam choosing a monitored mailbox.
- **secuura-ps-759-760-merge-owner** (ruled 'kam-merges' 2026-09-05): "Kam merges PS #759/#760 on GitHub" -> **Platform S, isolated from Platform K — NOT your scope**; Kam's two clicks.

## RULED BY WEDNESDAY, STILL OPERATIVE
- **F5 is P1** and its coverage-completion is your first act (this brief).
- **Client-facing communication = ticket comments only** (Linear); the extranet is INPUT-ONLY, never
  a channel. Anything needing a push comes to Wednesday as an escalation candidate for Kam.
- **A gate's subject is a SHA, not a branch.** New work on a NEW branch; any instruction that could
  cause a push names the gates running against that branch. Re-read `ls-remote` before trusting a SHA.
- **Never `fetch`/`merge-tree --write-tree`/`worktree add` in another checkout; never delete —
  cleanup means quarantine.** A relayed claim carries the counterpart's sentence VERBATIM INCLUDING
  ITS HEDGE. A red that proves nothing is as blind as a green that proves nothing; a hash proves the
  bytes, only a run proves the file still works.

## HOLDS
No merge and no deploy without a QA gate pass and Wednesday's GO. No probing of deployed/demo systems.
No external comms. Signature classes (prod, money, external comms, irreversible) pause for Kam.

## WRAP
Wrap at your rhythm-§2 boundary with a handover to Wednesday (sets not counts, branch + SHA read from
objects, surfaces changed, what you did NOT do). Overnight is working time — run until the queue is
dry, then say so.

— Wednesday

PROVENANCE:
- origin/develop `306d0db92…` at 23:40 handover, 10 merges | s140e session-wrap mail (DKIM) + NEXT-PICKUP.md | read 2026-09-07
- F5 confirmed on 2 of 8 protected routes on the real gateway, 6 unclaimed | s140e wrap mail + dashboard chat_log 2026-09-06T23:53 | read 2026-09-07
- Seat A (s141b, %130) running on KS-945 in its own worktree | Wednesday's own answer mail this session + cockpit.sh status (%130 alive) | read 2026-09-07
- Kam's two desk cards (demo-admin password; F5 disclosure) both on HOLD | dashboard chat_log 2026-09-06T23:59 + NEXT-PICKUP.md | read 2026-09-07
- Second Blockchain seat sanctioned in parallel with worktree partition | boot digest lesson 2026-09-02_coo-actionable-tickets extension "2026-09-06 09:42" | read 2026-09-07
- F5 four spellings + KS-733 must-not-close-shut + KS-486/KS-946/six-mounts queue | NEXT-PICKUP.md (22:1x seat handover) | read 2026-09-07
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 00:16
