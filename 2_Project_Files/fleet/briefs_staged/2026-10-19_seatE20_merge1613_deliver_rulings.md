## BLUF

You are **Seat E 20th** on Secuura Platform K (lane Secuura/Blockchain-E). Your predecessor signed as "Seat E 3rd", but this project's history.md already runs to Seat E 19th, so that ordinal was wrong. **Why you exist:** the Studio rebooted at 17:31 AEDT (06:31Z). Every seat died, and /private/tmp was wiped, so the predecessor's scratch clone is gone. Pushed refs survive.

**Two jobs, in this order:**
1. **MERGE #1613** (KS-1195) at head `c336de8312211a188f22a41b63e68df8046bb293`, on this mail's GO.
2. **DELIVER five Kam rulings** into the artefacts listed below.

Send a short plan confirmation before your first write, with your launcher's preflight warnings verbatim.

## QUEUE

1. **Merge #1613 (KS-1195, the S-key rate ceiling) — GO from Wednesday, under the open-ended TESTED grant** (Kam 2026-09-11, widened 17:50 that day: "merge anything that has been finished and tested").
   - Gates:
     - **X1** (Opus, tier 1): GO at the round-1 head `009749ed2565`, 0 blockers.
     - **Z1** (Sonnet, tier-2 delta, round 2 of 2): GO at `c336de831221`, 0 blockers. Its predicted landing tree is `9a3a5619e806511f2861ced32ae1aacc2a3cb8c7` on develop `722e07f19cee683ea037930e601e380a9491f7b5`. Verdict file: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_gate-Z1-pr1613-r2-delta/verdict.md`. Its hash was recomputed by Wednesday with the gate's own method and is EQUAL.
   - **Immediately before the merge, re-read** `git ls-remote origin refs/heads/develop refs/pull/1613/head`.
   - **If either has moved: STOP and mail me.** The verdict holds only for those two SHAs.
   - Squash-merge, matching the head commit. Then read develop again and compare the landed tree with `9a3a5619e806`. Mail MERGED with the landed SHA and the tree comparison.
   - Then post one BLUF comment on KS-1195 that the fix is merged, not deployed. Kintsugi takes it in the next round under the October grant.
   - **Do not close KS-1195:** "Done" requires deployed + a live check (Kam 2026-10-12).
2. **Deliver the five rulings** (section below). Each is ONE BLUF comment on the ticket named, quoting Kam's words verbatim with the card id and the time he ruled. After posting, read each comment back by id and mail me the ids. For KS-1570, also close row 7 of `DEPLOY-BLOCKERS.md`:
   - first read the file at develop and confirm row 7 is the KS-1570 condition;
   - make the edit on a branch and raise it as a one-file PR. Tier 3, hygiene. Do not merge it yourself; mail me the PR number.
3. Wrap. There is no further queue for this lane in this brief.

## RULED BY KAM, NOT YET IN AN ARTEFACT

All five were ruled on the live board on 2026-10-19 between 18:22 and 18:23 AEDT. They were recorded in Wednesday's decision store at 18:28.
- **secuura-s-signing-contract-additions-1019 = a**: *"Build all three after KS-1454, inside the KS-1384 project"*. "All three" means:
  - KS-1575 (record a signature against an existing document without a new version);
  - KS-1575's `metadata.rowHash` ask;
  - KS-1596 (a timestamp verb).
  **Artefacts:** a comment on KS-1575 and a comment on KS-1596. Nothing is built now.
- **secuura-ks1570-round-may-deploy-1019 = a**: *"I have seen it: close the blocker row"*, with the note *"keep the grant alive until further notice"*. **Artefacts:** close the KS-1570 row in `DEPLOY-BLOCKERS.md` (via the PR in queue item 2), and a comment on KS-1570. The note extends Kam's October deploy grant past 31 Oct, until he says otherwise. Say that in the comment as Kam's words. **This does not deploy anything.** Kintsugi still waits for Stuart's dev-ps deploy and for the KS-1402 500 fix (#1614, at gate Y1).
- **secuura-ks1580-erasure-revoked-key-code-1019 = a**: *"Build it after the Kintsugi round"*. **Artefact:** a comment on KS-1580.
- **secuura-ks1384-schedule-per-event-anchors-1019 = b**: *"Design now, merge after the Kintsugi round lands"*. Per the card, the KS-1603 interim ownership check goes ahead now on its own; Seat J 15th has it. **Artefact:** a comment on KS-1384.
- **secuura-ks1402-who-creates-the-holder-1019 = a**: *"K creates an invited stub user on transfer"*. Per the card, this works as certifications/issue already does for holderEmail. It is a K build with a tier-1 gate (a user row created from a connector call: the tenant boundary and PII must be proved), and S changes nothing. **Artefact:** a comment on KS-1402. Not built by you. It is the next build after #1614 merges.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- #1613's per-hour window: option (b) (explicit 3600 + pin + tamper), ruled by Wednesday at 17:0x. The delta carries it, and Z1 gated it.
- KS-1648 (60-s fallback) and KS-1649 (developer-portal 1,000/h text) were filed by your predecessor. Leave them as filed.

## PARTITION

Yours:
- the #1613 merge;
- comments on KS-1195, KS-1575, KS-1596, KS-1570, KS-1580, KS-1384 and KS-1402;
- `DEPLOY-BLOCKERS.md` row 7.

**NOT yours, live right now (shared inbox: a mail naming another seat is not yours):**
- Seat R 54th (Secuura/Blockchain-R): api-gateway `routes/audit-export.ts`; originate `utils/idNamespaceCollision.ts` and `routes/verificationV2.ts`.
- Seat J 15th (Secuura/Blockchain-J): anchoring `src/index.ts`, `anchorOverwriteGuard.ts`; originate `routes/anchors.ts`.
- Seat G 11th (Secuura/Blockchain-G): originate `routes/certifications.ts` and the ks1557 suite.
- #1614 (KS-1402, documents.ts + migration 052) is at gate Y1 with no seat live. Do not touch it.

Identify yourself by your pane's cockpit name.

## HOLDS

- **A fresh clone has NO pre-push gate.** Before any push: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`. Read back `git config --get core.hooksPath` in your plan confirmation (KS-1646).
- **Identity:** set `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY before any commit. Read back `git config --show-origin user.email`.
- **Pushing:**
  - `.githooks/pre-push:352-358` refuses a push whose tip is not the checked-out HEAD;
  - `:76-80` refuses a non-fast-forward push;
  - never `--no-verify`, never `ALLOW_FORCE`;
  - transport in full: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- No deploy. Client-facing communication is ticket comments only; the extranet is not a channel. Handovers to Peter or Stuart are test blocks, never a list of PRs.
- The launcher prompt's "CC Kam on every email" line is stale: Kam's 2026-08-12 rule says no CC on agent mail. Do not CC him.
- No Docker on this Studio. Rotate inside your 80-90 band at a clean boundary, writing your handover first.

PROVENANCE:
- #1613 head c336de831221 and develop 722e07f19cee (as quoted) | Wednesday git ls-remote on the Blockchain checkout | read 2026-10-19
- Z1 verdict GO, landing tree 9a3a5619e806, hash equal | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_gate-Z1-pr1613-r2-delta/verdict.md, sed '1d;$d' | shasum recompute | read 2026-10-19
- X1 verdict GO at 009749ed2565 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-10-19.md 17:11 entry quoting the gate's verdict line | read 2026-10-19
- five card rulings, words and options (as quoted) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json + kam_rulings_today.sh live read | read 2026-10-19
- Seat E ordinals up to 19th | your own 5_Project_History/history.md (grep) | read 2026-10-19
- pre-push refusals: non-fast-forward at :57-80 (ALLOW_FORCE decision :76-80), pushed-tip-not-HEAD at :323-358 | `git show 722e07f19cee:.githooks/pre-push` in Wednesday's own Spark cache clone | read 2026-10-19
- KS-1195 state In Progress, 11 comments, last 2026-10-19T05:58Z, not archived | Linear ticket KS-1195 (Secuura board, read-only GraphQL by Wednesday) | read 2026-10-19
- KS-1570 state In Progress, 0 comments, not archived | Linear ticket KS-1570 | read 2026-10-19
- KS-1575 Backlog 2 comments last 05:45Z · KS-1596 Backlog 1 comment last 05:45Z · KS-1580 Backlog 0 comments · KS-1384 Backlog 4 comments last 05:29Z · KS-1402 In Progress 13 comments last 06:18Z (all UTC, none archived) | Linear tickets KS-1575, KS-1596, KS-1580, KS-1384, KS-1402 | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 18:48
