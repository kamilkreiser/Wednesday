## BLUF
**DEPLOY GO — Kam's word (panel 20:34: "Please deploy Nexus."; the card ruled `deploy-now` at 20:4x). Deploy `48e092c` — the head re-gate (8) PASSED — to the DEV app `nexusaidev-app`, BY SHA, now. This pre-empts the ticket filing: do the deploy first, then finish RD-308 → Testing and the N8 tickets. NOT the demo: the 09:28 ruling's shape is "dev app, then demo on your word" — the demo waits for Kam's separate word, which Wednesday is asking for.**

## The deploy, as the recipe now says (the RD-302 rule is in it)
1. Build BY SHA from a dedicated worktree at `48e092c` — state HEAD and porcelain (0) before the build; the image tag is the SHA, never `latest`; `:latest` is NOT moved (verify its digest unchanged after).
2. Read the ROLLBACK digest LIVE before anything moves (the revision currently serving = `0000096` / `a554e52`); write it in your STATUS.
3. `az containerapp update` with `--container-name` (the two-container app refuses without it — S23's catch).
4. **Verify AFTER the OLD revision has TERMINATED, not when the new one starts logging** (the RD-302 rule; the 112 s two-revision window measured today): gate on `healthState=Healthy` + `runningState=Running` on the new revision AND the old revision's `runningState` no longer Running; THEN two identical consecutive probe rounds with a DISCRIMINATING half — a file the OLD revision cannot serve (a served sha from `48e092c`'s changed files, e.g. a `dataErasure`-dependent health field, or a static file only the new build has); `/api/health` 200 alone does not discriminate. Read the boot log filtered on the NEW `RevisionName_s` for the persistence sentinel.
5. Nothing else: no `DB_PATH` change, no seed flag unless the recipe already sets it, no demo, no `:latest`.

## Receipt (STATUS by mail, then your tickets)
The new revision name, the digest, the rollback digest, the old revision's terminal state with its time, the two probe rounds with the discriminating file's sha, `:latest` unchanged by digest, the boot-log sentinel line, and the SSO boundary stated ("I have not seen the deployed dashboard render" if you cannot). Then RD-308 → Testing with the deploy revision named (Release Ready = a serving revision on this board — now it has one), RD-318's comment, the N8 tickets (N8-1+N8-2 Highest first).

## Holds
Demo: Kam's separate word. `:latest`: unmoved. Nothing deleted. Your statusline reads `ctx:43%` (captured from your pane by Wednesday at 20:3x) — room for the deploy and the tickets.

PROVENANCE:
- Kam's word "Please deploy Nexus." (panel 20:34, verbatim) + the card `nexusai-erasure-deploy-after-regate8-2026-09-05` ruled `deploy-now` 20:4x | `tools/kam_rulings_today.sh`; `decision_queue.sh` | read 2026-09-05 20:47
- `48e092c` at origin (`rd-136-nga-defaults-s12`), re-gate (8) PASS | `git ls-remote origin` from Wednesday's seat 20:4x; the QA mail 10:27:14Z | read 2026-09-05 20:47
- The dev app serves `0000096` / `a554e52` | S35's deploy STATUS today (the 112 s rollover measured) — not re-read by Wednesday; you read the live revision before you move | read 2026-09-05 17:xx
- The RD-302 verify-after-termination rule and the `--container-name` refusal | S32's RD-300/302 finding and S23's deploy, both in the deploy recipe the agent owns | read 2026-09-05 (carried; the recipe is yours to read)

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 20:47
(checked: "deploy now" against the card's `fix-first` recommendation — Kam ruled `deploy-now`; his word governs and the N8-1/N8-2 pair rides as a Highest ticket, stated; "not the demo" against "Please deploy Nexus" — the 09:28 ruling's shape is dev then demo on his word; Wednesday asks him, the agent does not guess.)
