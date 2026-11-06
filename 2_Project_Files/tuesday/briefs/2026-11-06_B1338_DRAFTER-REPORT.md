STARTABLE: YES (defaults C-130 FILE, STATE-ROWS NONE, CORRECTION NONE are safe; none of the Qs blocks launch)

Drafter report for B1338 / SEAT-R185, Composer records, B537 carry. `date` 15:43:09 to 15:46:24 AEDT Fri 6 Nov 2026. Files: `2026-11-06_B1338_SEAT-R185_composer-records-b537-carry.md` (94 lines, 6 stamp lines), `2026-11-06_B1338_slots.json`, this report. No Jira write, no removal, no deploy.

## BLUF
- C-130 is the next free number: root `main` is now `0aee3efd` (B1314's fold), highest C is C-129 (`CLARIFICATIONS.md:2442`), highest BACKLOG row #472. Work items: C-130 plus a history entry; BACKLOG only on slot.
- The gap is real: `-w B537` counts 0 in CLARIFICATIONS and 0 in history (control B986: 4 and 1); no heading between C-74 and C-113 records a main on the demo. The deploy seat left a drafted "C-next" in B537 STATUS `:226-:241` that was never filed.
- Root records live in the root repo (no remote); mechanics follow B1314: worktree branch, one commit, `merge --no-ff`.

## Facts re-measured
- Code main `a54250f4` (gh ref); PR #79 merged 2026-10-16T00:56:47Z squash `230f9fab`; compares: ef916ce2...230f9fab ahead 2; 230f9fab...308b7aa6 ahead 5; ef916ce2...308b7aa6 ahead 7; `pulls/9999` 404.
- B537 STATUS 295 lines; `:91`, `:231`, `:234`, `:295` printed by awk.
- **Fact that did not hold:** the sweep cites STATUS `:68-69` for the demo-before-swap read; it is `:70`. Kit uses `:70`.
- **The STATUS does not quote the digest**, so I read the mail (one GET, key in-process): reply 2026-10-23T03:42:07Z, text "Approved", spf/dkim/dmarc pass; the digest it quotes (header: Fri 23 Oct 11:25 am AEDT) lists exactly ONE card, the approver-email look. Its stated default read "nothing goes to the demo ... until you tap".
- Kam's words: only the 10:12 row names Composer; already verbatim in C-128 (count 1, control fires). Not re-recorded.
- Feedback watermark: project keeps none (0 in JIRA.md, CLAUDE.md); left out.
- "no tap" grep: 0 in all four record files and the STATUS (control `-w tap` in CLARIFICATIONS: 25).

## D-decisions
- D-1: C-130 draws on the STATUS's own drafted entry but no person's name, no card id, no mail domain; "the product owner" throughout.
- D-2: bounded exception to B1314's "no deployed/on the demo" property, only in attributed sentences.
- D-3: STATE-ROWS slot: ten-plus BACKLOG rows (#95, #129, #42, #99, #182, #277, #317, #318, #131, #170) still read NOT DEPLOYED with no later deployed sentence; kit holds them behind a slot.

## Q for Tuesday (default)
- Q-1 Record the "no tap" correction? [No: the records never carried it.]
- Q-2 Append State sentences to those BACKLOG rows? [NONE; I think YES is defensible as a separate small pass, but it is more than "a records gap".]
- Q-3 Record the 10:05 and 12:12 messages? [No: no Composer decision.]

## UNMEASURED
Demo itself; the two-slot inference; STATUS measurements; whether the push-to-demo grant covered the deploy (kit forbids ruling it).

## Outside the fences
Read-only: Composer project files, the B1314 kit/report/slots, the sweep, model files. One GET to the Agent Mail inbox (authorised by the brief); no card read. Scratch `mail.py` in the session scratchpad (`k/`). Two hooks advisories only; no refused command ran.
