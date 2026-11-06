# Gate 215 commission — Secuura / Blockchain, BATCH of already-MERGED PRs, tier 1 read, ROUND 1 of 2

Written by Wednesday 2026-11-06. Model: Opus (row G1; credential and auth surfaces). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub; network only for git fetch into your own clone and read-only GitHub or Linear reads. Write verdict.md here at the end: line 1 the batch line (the WORST), then one labelled verdict per PR, each exactly GO, GO WITH NOTES or NO GO (<reason>).

Why this gate: these PRs merged earlier with Test Evidence but no gate verdict that a close-out seat could find, and they touch credential, auth or money-adjacent code. Wednesday ruled that such tickets stay open until a gate reads them. The question is NOT whether to merge (they are merged) but: does the merged change do what its ticket says, on the real path, so the ticket may close?

The PRs: PR 1319 (KS-908, API-key mint body and list row echo connectorId, squash aee347c5f60a per the drafter's git show); PR 1934 (KS-1413, removes a printed password); PR 1345 (KS-1360, wallet-session delete response body); PR 1408 (KS-1435, transfer reject schema declares signature); PR 1343 (KS-1371, VC revocation path; the close-out seat reports 13 unreproduced guard firings there). Those descriptions are a seat's, not read by Wednesday: read each PR and ticket yourself and say where they differ.

Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md. For the close-out seat's reasons: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-06_seatS-25th/HANDOVER.md FINAL block. Clone: git clone --shared /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files to a subfolder here, then fetch origin develop by ls-remote's sha into YOUR clone only; deps from a finished worktree by copy, never npm install into a shared tree. Linear read-only: key LINEAR_API_KEY sourced inside a Python process from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, never printed; header Authorization with no Bearer prefix; comments(first:50) sorted client-side. Absolute paths, no cd; vitest cache inside your folder; never a recursive grep or find over 0_Brain/reference, local-model/ or 5_Project_History. Suites one at a time, machine shared, stop every process you start.

## Questions, per PR
1. What the ticket asked (its scope sentence, quoted) against the merged diff at develop today: is the change still there, unreverted, and complete for that scope? Anything named by the ticket and undelivered?
2. Behaviour: run the PR's own cells at develop's tip; prove one of them bites by a mutant of your own. For a credential surface, does any response, log or error now expose a secret, or does an authorisation path change who is admitted? Quote the code lines, not a paraphrase.
3. PR 1343 / KS-1371: are the 13 guard firings a defect, a test artefact, or unknown? Say which and how you know, or UNMEASURED.
4. Is each ticket closable on this evidence under card secuura-done-rule-unit-pinned-deployed-no-live-check = a (read with decision_queue.sh show, READ verb only)? Whether its fix is in the running Kintsugi build is NOT yours to measure: say UNMEASURED.

## Output
verdict.md (batch line, per-PR verdicts, BLUF, findings with severity, file:line, evidence path, what was NOT tested, your own conduct). Final message: verdict lines plus one line per finding.
