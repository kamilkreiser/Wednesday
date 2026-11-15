# BRIEF: Seat AA 6th, Secuura/Blockchain-AA. DIAGNOSE-AND-FIX seat on OPUS (claude-opus-5-5, routing row C3: anchoring spends from the platform wallet, the decision is the work), TIER 1 gate. Stuart's question about a FAILED sign anchor on demo-pk. Diagnosis by read-only measurement FIRST, then a design QUESTION, then red-first build; ends at READY FOR GATE. The deploy is a SEPARATE step (a D seat), described under DEPLOY below.

BLUF (Wednesday, 2026-11-15 13:1x). Kam, terminal 2026-11-15, verbatim: *"please have a look at Stuarts message and please change things to address the issue.  deploy when ready and tested."* Stuart's message (pasted by Kam, verbatim below) reports anchor `anchor_c3d42601-7f06-44db-89d7-a0c61a1814a7` (verb sign) on demo-pk already reading FAILED at S's first poll, 94 s after submission (when K marked it is UNMEASURED), one second after a declare anchor on the same document that CONFIRMED. Your job: (1) find out from demo-pk's own records WHY it failed, (2) answer Stuart's four questions with measurements, (3) if the cause is in K's code, fix it so the declare+sign pair (sent one second apart by S) cannot fail this way, and decide with Wednesday what happens to THIS anchor (retry, re-submit, or S sends a new one). Nobody has diagnosed this yet: every cause below is a HYPOTHESIS.

## STUART'S MESSAGE (verbatim, as Kam pasted it; addressed to Kam)
> @Kam, a question on a failed anchor on demo-pk (from uat-ps) that Phil saw in a demo.
>
> Anchor reference: anchor_c3d42601-7f06-44db-89d7-a0c61a1814a7
> Verb: sign
> Document on K: root fe6bf842-ecdb-45c7-9e20-ea2a450fbd69, tip doc-1794551671422-d0d17965
> Network: preview
> Submitted: 13 Nov 2026 at 06:34:29 UTC
> K reported it FAILED when S polled at 06:36:03 UTC, and still reports FAILED on later polls (06:42:59, 06:54:59).
>
> The same document's earlier anchors all confirmed:
> •  upload, 06:22:03, tx 1fa219ef90d3...
> •  watermark, 06:30:00, tx 102b113e02ed...
> •  declare (certify), 06:34:28, tx fcd5310f96ce..., confirmed 06:35:03
>
> The sign was submitted one second after the declare, because S sends both when a user declares and signs in one step.
>
> Questions:
> 1. Why did K mark this anchor failed? What does demo-pk's log or the anchor's record show for it?
> 2. Is it the two anchors arriving one second apart (for example both spending the same wallet output)? The same pair on 2 Nov did confirm, but the sign took 19 minutes instead of the usual 2 to 3 (declare tx 3c1d54437ace..., sign tx ef23f12bb5ff...).
> 3. Will K's retry still pick this anchor up, or is it final? S keeps asking every few hours and will record it if it confirms.
> 4. If it is final, is there a way to re-submit it on K, or should S send a new anchor for the signed copy?
>
> Effect on S: the signed copy of the document has no confirmed anchor, so the document reads as not anchored, and the certified, share and share-revoke events recorded against that anchor show as failed too.
>
> Note: The second question is a guess, not a finding.

model: claude-opus-5-5 (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json`, levels.opus.model_id, checked_at_local 2026-11-15 11:01:23 +1100, warnings []; confirm it before you say it) -- routing row C3 of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md`, gate row G1 (tier 1, Opus). The Spark is GONE (returned to HP 2026-11-15): no local tier.

## NEW SEAT: you are Seat AA 6th (lane Secuura/Blockchain-AA; claude-opus-5-5; trust `$TMUX_PANE`). Act ONLY on mail whose subject names `(Seat AA 6th)`.
Ordinal check before your first write: `/usr/bin/grep -c -i -E '^## .*Seat AA 6(st|nd|rd|th)' /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` expecting 0, control `'^## .*Seat AA 5th'` expecting 1 (both MEASURED by Wednesday 2026-11-15 13:1x: 0 and 1). Record folder `REC` = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<machine date>_seatAA-6th/` (create it).

## WHAT IS ALREADY KNOWN (MEASURED by Wednesday, with the source; re-read each before you rely on it)
- **Demo is FROZEN at `07a2d62be6a0`** (Seat D 61st HANDOVER, `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatD-61st/HANDOVER.md`, FINAL). So demo-pk runs anchoring code as of that commit, NOT develop. Diagnose against the code demo actually runs; read develop for what has changed since.
- **Anchoring has been held from every deploy for Kam** since card `secuura-anchoring-second-fee-on-empty-reply-1107` = a (2026-11-08 20:31): merge PR 2081 (KS-1171), fix the "empty 2xx reply reads ABSENT and can pay a second fee" hole before anchoring next deploys. Whether PR 2081 merged and whether the empty-reply fix exists is UNMEASURED today: read both (GitHub pulls API, the board). If the fix you build overlaps either, say so in the QUESTION.
- **No demo deploy tool exists**: D 61st's `boxrun_d61.sh` refuses demo, rc 9 (HANDOVER item 3). How a seat reaches demo-pk read-only is UNMEASURED by Wednesday: find it in the project `CLAUDE.md`, `1_Project_Definition/` and the deploy seats' handovers; if no read path exists, that is a QUESTION, not an improvised ssh.
- develop = `48883ba5976b76a5e28e4de69618853ba5d29a20` (ls-remote by Wednesday 2026-11-15 13:1x).
- Floor: NO other Secuura seat is live (cockpit.sh status 13:1x: only wednesday + fleet-monitor). Open PRs and the push queue: UNMEASURED, read them at item 0.

## QUEUE
0. **Plan first.** Cockpit status, open PRs with file lists (GitHub pulls API; GH_TOKEN from the project `.env` inside a process), the push queue (`ls /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-queue`), PR 2081's state and the empty-reply ticket's. Plan-confirmation QUESTION mail (format under MAIL).
1. **Phase 1, diagnose (READ-ONLY), then ONE QUESTION.** Measure, each with its instrument:
   (a) the anchor's own record on demo-pk for `anchor_c3d42601-7f06-44db-89d7-a0c61a1814a7` (status, tx hash if any, error text, attempts, timestamps) and the declare anchor's beside it (SELECT only);
   (b) the anchoring service's log lines on demo-pk around 2026-11-13 06:34:00-06:37:00Z (and the 2 Nov pair: declare tx `3c1d54437ace...`, sign tx `ef23f12bb5ff...`, sign confirmed after ~19 min: what made that one survive);
   (c) the code path at `07a2d62be6a0`: how the submitter picks wallet inputs (UTXO selection), whether two submissions one second apart can choose the same input, what a node rejection (e.g. bad/spent inputs) or a submit error does to the row (FAILED terminal vs retryable), and what the retry/reconciler does with a FAILED row;
   (d) whether develop already changed any of (c). **If develop already fixes the cause, there is no red cell to write on develop: say so, and the work becomes a regression cell on develop plus the anchoring-only deploy; the QUESTION names which.** If the cause is outside K (the node, the network, S), say so: then there is no K fix, only the answer to Stuart;
   (e) the answers to Stuart's 1-4, each marked MEASURED or UNMEASURED;
   (f) the fix options (at least two; e.g. serialise submissions per wallet, input locking/reservation, treat an input-conflict rejection as retryable with a rebuilt tx), your recommendation, the files touched, and what each costs; and how a retry avoids a SECOND fee for an anchor whose first tx did land (the 1107 card's hazard);
   (g) THIS anchor's remediation options (re-queue on K, or S sends a new anchor), what each writes, and whether it spends (preview is a test network: say what the fee is in tADA, and still treat a submission as a write that needs the ANSWER).
   Then mail `[Secuura/Blockchain-AA -> Wednesday] QUESTION: sign anchor failed design` with (a)-(g) and a DRAFT reply to Stuart (plain language, his four questions answered, every guess labelled as a guess). Meanwhile: red cells only, no product line before the ANSWER.
2. **Phase 2, build, red-first, after the ANSWER.** A cell that reproduces the failure (two submissions one second apart on the same wallet state, red on develop by AssertionError, green at your head), a planted tamper per changed line restored by content and sha256, the existing anchoring cells (KS-1171 family: `ks1171-*`, `ks726-gate-f1-unreachable-chain`, `ks1868-*`) green by name, a cell proving no second fee when the first tx landed. Whole `services/anchoring` suite before and after (name any pre-existing red, e.g. `threadTokenMint`), tsc including test files, eslint with a planted control, `docs-fragments.mjs check` OK and FAILING on a planted defect. No chain call, no Blockfrost key, no mnemonic, no real credential in any test.
3. **The PR and the end.** Title `Refs KS-NNNN:` (file the ticket yourself on the Secuura board if none exists, after the ANSWER names it; never a closing keyword). PR body: Test Evidence block, Kam's instruction and Stuart's question quoted, the hook line verbatim, "what was NOT covered" (real chain, real Blockfrost, demo-pk itself), and "**deploy owed: anchoring only, Kintsugi first then demo-pk, by a D seat on Wednesday's GO under Kam's 2026-11-15 word; not done by this seat**". Then the PR-naming ticket comment (`--dry` then `--real`, read back, 0 mention nodes), and `[Secuura/Blockchain-AA -> Wednesday] READY FOR GATE KS-NNNN (Seat AA 6th)`, tier 1, body line 1 exactly `Seat AA 6th`. Your push runs `.githooks/pre-push` in your own clone: read its refusal branches before the push and quote the hook's final line verbatim; a refusal is mailed, never routed around. The seat ENDS there: no merge, no deploy, no state move.

## DEPLOY (not yours; written here so the plan sees the whole road)
Kam's 2026-11-15 words are his "deploy when ready and tested" for THIS fix. Road: gate GO -> merge (B seat) -> **Kintsugi first** (D seat, anchoring only, +15 min watch, a live preview-network anchor pair if the gate says it is safe) -> **demo-pk, anchoring service ONLY**. The demo freeze (card `secuura-ks1401-058-merge-demo-billing-1104` = a) exists because a demo redeploy from develop would apply migration 058 (billing totals) automatically. **If deploying anchoring alone to demo would also run any migration runner or carry 058, STOP: that is Kam's card, not this grant.** In Phase 1, measure whether the anchoring image/boot runs migrations, and say so.

## PARTITION
- **YOURS:** `Blockchain/Dev/services/anchoring/**` (src and `__tests__`) for this fix, and your own fragment pair. Anything outside, named in the ANSWER first.
- **Others:** read the open PRs at item 0; PR 2081 (anchoring, KS-1171) if still open is the one most likely to share files: merge-tree it against your branch and say what overlaps.

## HOLDS
Signature classes pause for Kam, always: production, money, external communication to any human, anything that cannot be undone. **Demo-pk is READ-ONLY for this seat**: logs and SELECTs only; no restart, no write, no re-submission, no `az` write, no config change. No chain submission of any kind (preview included) without the ANSWER naming it. No message to Stuart, Peter or Phil: your reply is a DRAFT in the QUESTION mail; Wednesday puts it before Kam. You change no assignee or state of any ticket except one you file. No `--no-verify`, no force push, no `--admin`. Never delete a file; quarantine into a dated folder, recorded. Absolute paths, NO `cd` (a hook refuses it), `GIT_OPTIONAL_LOCKS=0` before git in the shared checkout (read only; work in your own clone), `cmd > out 2>&1; rc=$?`, `/usr/bin/grep -i` with a positive control beside every zero, bounded output (`| head`), no recursive grep over `5_Project_History` or `0_Brain`. A cell is red by AssertionError, not TypeError. A migration number is a QUESTION.

## MAIL
From secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY; subject prefix `[Secuura/Blockchain-AA -> Wednesday]`; body line 1 exactly `Seat AA 6th`; no cc; no secrets; read each sent mail back by id. Plan confirmation: QUESTION mail, topic `plan confirmation`, launcher preflight warnings VERBATIM, your note on anything here that looks wrong, the model line, the live-seat list you measured, the tracked watcher pid. Questions: Context / one Question / Meanwhile / Needed-by.

## IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO
A brief item that is wrong is Wednesday's error and will be named as Wednesday's.

## PACE AND END
At ctx about 70% finish the step in hand and write the HANDOVER; wrap at about 75% at the latest. WRAP: history entry `## <machine date> - Seat AA 6th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest first; duplicate guard with a positive control); `REC/HANDOVER.md` (FINAL block first, next step named); `REC/evidence/writes_aa6.tsv`; vault commit, own lines only; wrap mail `[Secuura/Blockchain-AA -> Wednesday] Session wrap <date> (Seat AA 6th)`, body line 1 exactly `Seat AA 6th`.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam, terminal 2026-11-15 ~13:0x: "please have a look at Stuarts message and please change things to address the issue.  deploy when ready and tested." -> the authority for this seat AND for the anchoring-only deploy after the gate (Kintsugi, then demo-pk), bounded by the 058 STOP above.
- secuura-anchoring-second-fee-on-empty-reply-1107 = a (2026-11-08T20:31:42): fix the empty reply before anchoring next deploys -> if that fix is not merged, the anchoring deploy waits for it or carries it; say which in the QUESTION.
- secuura-ks1401-058-merge-demo-billing-1104 = a (2026-11-05T07:08:38): no demo redeploy from a develop containing 058 without his word -> the STOP in DEPLOY.
- secuura-wednesday-go-counts-as-kams-word-1030 = a: Wednesday's GO starts work inside his standing grants.

PROVENANCE:
- Kam's instruction and Stuart's message | Wednesday's terminal, pasted by Kam | read 2026-11-15
- develop 48883ba5976b | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin develop, Wednesday | read 2026-11-15
- Demo frozen at 07a2d62be6a0; no demo tool; anchoring held for Kam | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatD-61st/HANDOVER.md FINAL + items 3, 5, read by Wednesday | read 2026-11-15
- Cards 1107 and 1104, verbatim | decision_queue.sh show, Wednesday | read 2026-11-15
- Ordinals AA 6 = 0, AA 5th = 1 | /usr/bin/grep -c -i -E on history.md, Wednesday | read 2026-11-15
- Floor: wednesday + fleet-monitor only | cockpit.sh status, Wednesday | read 2026-11-15
- KS-1171 state In Progress, 6 comments, newest 2026-11-06T18:45:59Z (title: Guard 3's re-poll reads a MIXED window as ABSENT) | Linear ticket KS-1171, GraphQL read by Wednesday, key sourced in-process from the Secuura .env, never printed | read 2026-11-15
- Model claude-opus-5-5 | models_latest.json levels.opus, Wednesday | read 2026-11-15
- UNMEASURED by Wednesday: every cause of the failure; PR 2081 and the empty-reply fix state; open PRs; the demo read path; whether anchoring's boot runs migrations | the seat measures each | read 2026-11-15
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-15 13:09
