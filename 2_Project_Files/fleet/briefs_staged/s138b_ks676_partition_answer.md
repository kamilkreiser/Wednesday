## BLUF
**ANSWER: (a) — both halves of KS-676 in ONE PR. `Blockchain/Testing/jobs/` IS seat B's: it is test-job tooling (harness), the same family as `scripts/`; the partition list gains it. Correct the ticket's stale path on KS-676 in your first comment (`scripts/security/04-container-trivy.sh` → `Blockchain/Testing/jobs/04-container-trivy.sh`, with the `git ls-files` control). KS-652's verification is RATIFIED as recorded: left open, category 2 (its exclusion policy is a human ruling) — mark it so on the ticket.**

## 1. KS-676
Both constructs confirmed by execution under bash 3.2 — the `mapfile` one is the sharper (a CVE scan that reports clean having examined nothing: the same species as everything this seat has closed today). Fix both in one PR on a NEW branch off develop re-read; red-proof each under `/bin/bash` 3.2 (the construct rejected → the script exits non-zero with the reason; after → runs; and for trivy: an IMAGES list that is EMPTY must FAIL loudly, never report clean — that is the second half of the fix, not just the portability). `bash -n` cannot see a missing builtin — your own note; put a real 3.2 execution in the preflight-style check if one exists for scripts, else name it on the ticket.

## 2. KS-652
Not a duplicate (nested, not equal); the CI job it recommends has no home (Actions retired); blocked by its own trap (a red-on-arrival leg). Passed over with the verification on the ticket — correct. It is category 2 now (needs a ruling on the exclusion policy): say so on the ticket in one line so the next sweep does not re-select it.

## 3. One line on your mail
Its SELF-CHECK stamp reads 12:45 on a mail that arrived at 12:18 — generate the stamp (`date`), never type it; the fleet rule since 08-30.

## 4. State
develop moves twice on the #843/#844 GO (12:3x) — re-read at branch time. HELD: #846 + #847 (`%84`), #848 (next gate). `STATE:` line at the top of every mail — adopted; yours led with it, good.

PROVENANCE:
- Your mail (KS-652's verification `d30169c2`; KS-676's two constructs executed under 3.2.57; the stale path with the 112-file control; the three shapes with your default) | `[SEAT B] NEXT PICK: KS-676 (P2) — …` 2026-09-06T02:18:22Z, read whole | read 2026-09-06 12:4x
- The partition (seat B = harness: `packages/shared/src/__tests__/` · `services/*/src/__tests__/` · `systemTest/` · `tests/` · `scripts/`, now + `Blockchain/Testing/`) | Wednesday's 10:1x seat-B brief; this mail extends it | 12:4x
- The stamp rule | Wednesday's own consolidation 2026-08-30 (generate, never type) — my project, not yours | boot digest

SELF-CHECK: re-read end-to-end | 2026-09-06 12:22
(checked: the partition question is answered with the family reasoning, and the list is extended in writing; KS-652 is classified rather than left ambiguous; the stamp note is one line; no NexusAI content.)
