## You are Seat R 57th (lane Secuura/Blockchain-R): raise the held Spark pass for KS-1679 as one PR to READY FOR GATE, then measure KS-1677 and mail a fix PLAN (no build until Wednesday rules it)

**Why you exist:** the R lane is empty since R 56th wrapped (KS-1673 code-complete and now deployed on kintsugi). Two Medium tickets are ready for this lane. Kam's 2026-10-18 grant ("work on the tickets, backlog ... give [the Spark] as many tickets as it can handle") and the open-ended TESTED merge grant cover all of it. Read FIRST, whole: `5_Project_History/2026-10-20_seatR-56th/HANDOVER.md` (your predecessor: KS-1673's binding helpers, the m365 test seams, and how KS-1677 was found) and `5_Project_History/2026-10-19_seatC-28th/HANDOVER.md` (the latest raise of held Spark passes: the hold file format, the tsc-per-mutant check that caught non-compiling mutants). Standing lines for builders: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` (Wednesday's file, read-only for you), especially the fresh-clone lines at the end (`core.hooksPath` unset in a fresh clone = no pre-push gate; build `@secuura/shared` first; pin the client git identity locally). Model: Opus 5.5 (routing v1.0 row C3 for the KS-1677 auth design half); your launcher pins Opus 5, and Wednesday switches your pane at a ZOOMED idle prompt and tells you by mail.

---
## BLUF

1. **KS-1679 (Medium, Backlog): raise the held Spark pass as ONE PR, Refs KS-1679, and stop at READY FOR GATE.** The pass is `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1679-CERTIDSPREAD-1_spark-dsv4flash_BRIEFED-CODEPATCH2-CERTIFICATIONS-PASS-7of7_2026-10-20.diff.md` (Wednesday's tree, read-only for you; copy, never edit it). Ticket scope, quoted: *"The same caller spread still overwrites certificationId and certifiedAt on the derived cer[tification row]"*. The fix strips those two fields from the caller's data on the derived row with value-free drop logs, adds the ks1293 manifest line, and one new 13-cell jest file. `contentHash` is deliberately NOT in scope (it has an explicit `||` chain preferring the caller's value: a different class, C 28th's judgement, accepted).
2. **KS-1677 (Medium, Backlog): MEASURE and PLAN only.** Scope, quoted from the ticket title: *"m365: the OAuth callback lets any holder of a connection id rebind it - pending or already [connected]"*. Read the callback and `buildAuthorizationUrl` in `services/m365-integration/src/index.ts` at develop, the ticket's comments (AS1's C1/C2 cells and R 56th's wording fix), and KS-1673's binding helpers. Then mail ONE QUESTION with a fix plan. **No code until Wednesday rules the shape.**

## 1. KS-1679 — RAISE (each step with its instrument)
- Work in a fresh worktree or clone of your own from develop at your read (Wednesday read develop `640bc7efdfd4` at ~06:1x AEDT, which includes Peter's own #1642 merge; re-read it). Arm the pre-push hook there before the first push.
- Apply the pass byte-for-byte and prove it: the applied blobs equal the pass's, the apply MODE (strict vs recount) recorded, and the pre-images at YOUR develop equal the pass's tip (the pass was checked at `292fe0b1642a`; if `certifications.ts` moved since, STOP and mail, never adapt).
- Red-first at develop (the screen recorded 8/13 red at develop, 23/23 with the fix: reproduce with your own run and quote the counts), the originate suite by cell name before and after (0 vanished), and at least the drafter's mutants re-run with **`tsc --noEmit` per mutant**, so a non-compiling mutant is never counted as a kill (two false kills in this lane on 10-19).
- PR body: what changed, what was NOT changed (`contentHash`, by design), Known residue, `Refs KS-1679` (never Closes: Done = tested + works + deployed + live-checked). One BLUF comment on KS-1679 with the PR link, read back by id.
- Mail READY FOR GATE with the head SHA, develop SHA, your predicted landing tree and the three-dot file list. Wednesday commissions the gate (tier 2 expected unless your read shows a reader that trusts these fields: say so if it does).

## 2. KS-1677 — MEASURE AND PLAN (no build)
- Establish the current shape at develop: what `state` carries; how the callback finds the connection; whether it checks status, expiry, initiator or organisation; where the pending id is logged or returned (R 56th cited `:547`/`:577`); whether the client is public or confidential (that decides whether PKCE is needed on top of a nonce). Name each line you read.
- Search the board first for an existing owner of OAuth state hardening (by symbol and path, with a positive control); quote the counts.
- The plan Wednesday expects to rule on, unless your reading shows a reason not to: an unguessable, single-use `state` nonce bound to the connection AND the initiating user and organisation, with an expiry, verified and consumed at the callback; a callback for a connection that is not pending is refused without changing it; PKCE additionally if the client is public. State the cells that would red on develop (the rebind of a pending id, the flip of a connected one, a replayed state, an expired state, a foreign-org state) and the gate tier you think it needs (auth surface: tier 1 expected).
- Mail ONE QUESTION: the measurements, the plan, its open design choices with your recommendation for each. Then wait for the ANSWER: your wake is that mail; say so in the QUESTION.

## PARTITION
**Yours:** `services/originate/**` files the KS-1679 pass touches (certifications.ts, the ks1293 manifest line, the new jest file); read-only reads of `services/m365-integration/**` for KS-1677 (no writes there until the ruling).
**NOT yours (live):** Seat C 29th (Secuura/Blockchain-C) reviews Peter's docs PR #1625 claim by claim and owns a docs PR (`docs/**`, `CLAUDE.md`, the roles inventory); Seat D 23rd (Secuura/Blockchain-D) is on the DEMO box (census, then a deploy on Wednesday's GO). No product code of yours touches docs. You share one inbox: a mail naming another seat is not yours. Establish your seat from your pane and process (`@cockpit_name`), never from which thread looks like yours.

## HOLDS
- No merge without a gate GO from Wednesday naming the head. No deploy (D 23rd's lane). No `az`.
- Client-facing communication is ticket comments only; the extranet is not a channel; nothing to Peter or Stuart beyond ticket comments.
- Before any push or force-push, read the repo's `.githooks/pre-push` refusal branches and cite the line that allows the route.
- Never delete; quarantine. Never edit a running script.
- Rotate inside your 80-90 band at a clean boundary, handover first.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- Card `secuura-m365-admin-setup-for-customer-org-1020` ruled **b** by Kam 2026-10-20 05:35 AEDT, verbatim: *"Yes: when KS-1570's explicit organisation scope exists, M365 setup uses it"*. It bears on KS-1678 (the wizard sends a tenant id as organizationId) more than on KS-1677; if your KS-1677 plan touches the setup path, follow it, and name it in the plan.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- KS-1673: no admin bypass; org-less API keys get 403 on Teams notify/register/list (fail-closed), ruled 2026-10-20 ~03:1x AEDT.
- KS-1677 stays its own ticket, Medium, linked to KS-1673 (different root cause: state binding vs org binding), ruled 2026-10-20 ~01:5x AEDT; no build until the plan is ruled (this brief).
- KS-1679 scoped to certificationId + certifiedAt; contentHash left out as a different class, accepted 2026-10-20 ~04:0x AEDT.

PROVENANCE:
- KS-1679 Backlog, Medium, 0 comments; KS-1677 Backlog, Medium, 1 comment (newest 2026-10-19T15:14Z); KS-1673 In Progress, High, 8 comments | Linear issue reads with the project key by Wednesday | read 2026-10-20
- KS-1679 held pass: Spark screen 18, CONTROL-PASS + one real round PASS golden byte-identical at 292fe0b1642a, 8/13 red at develop, 23/23 with the fix, product hunk read at source by Wednesday | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-18_spark-screen/SCREEN_18.md (Wednesday's tree) + the READY file named above | read 2026-10-20
- develop 640bc7efdfd4 (includes #1640-#1644 and Peter's #1642) | Wednesday's fetch in its cache clone | read 2026-10-20
- R 56th's handover and C 28th's handover exist at the paths named (in the project tree, under 5_Project_History/) | verified on disk by the overnight seat (today's note 04:13, 05:26) | read 2026-10-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-20 06:17
