# MERGE GO — Kam's own word, 07:10 this morning. Land the gate-passed set on `main`, one at a time, reporting each. RD-376 is EXCLUDED. Expect the secret scanner to fire, and do not "fix" it.

## BLUF — the authority, verbatim, both halves
**Kam, dashboard panel, 2026-09-08 07:10 AEST:**
> *"I'm going to drop off the kit if we please deploy and merge everything that has been tested and
> done and is ready for deployment."*
Read through dictation noise: **deploy and merge everything tested, done and ready.** He is stepping
out as he says it.

**Kam, ruled card `nexusai-rd367-frozen-trunk`, 2026-09-07 19:00, still standing:**
> *"Wednesday merges only branches whose gate has PASSED, one at a time, reporting each."*

**Two authorisations pointing the same way. You execute; Wednesday does not write to your repo.**

## 🔴 WEDNESDAY'S READING, STATED SO KAM CAN CORRECT IT
I have been holding these merges on **two GitHub settings only Kam can see** — whether
`CI_DEPLOY_ENABLED` is on, and whether `demo` has a required reviewer. **The hold existed for one
reason: `deploy-demo.yml` deploys FROM `main`, so a merge to main IS a deploy to the demo, and I did
not want that to happen without him knowing.** **He has now asked for the deploy.** So the thing the
hold protected against is the thing he wants, and **the hold is resolved by his instruction rather
than by the answer.**
**I measured my own access before concluding this**: the `kamilDatasec` identity in your
`4_Credentials/.gh-config` is in orgs `token-one` and `warpkey`, **not `datasecau`**, and sees zero
repos there — the deploy key reaches the repo for git, the API identity cannot, and repo settings
need admin regardless. **So the two settings remain unread, and I am proceeding on his word, not on
an answer.** If a deploy fires, it fires because he asked for it.

## WHAT TO MERGE — my list is RELAYED; build yours from the gate verdicts and correct me
**Wednesday holds no client identity on your repo, so every SHA below is second-hand.** Re-derive the
set from the gate reports and the board, and **tell me where I am wrong.**

    rd-322-root-guard-vacuity-s45     432617a   clean GO. The only unqualified GO in the set.
    rd-374-f2-guard-coverage-s46      10ddb0a   lineage closed, completion check passed
    rd-323-scheduler-failure-...      e032c7d   lineage closed (GO-with-findings, record-level, ticketed)
    rd-377-verdict-domain-s47         fabcc93   clean GO, (a) NOTHING — STACKED on rd-323
    rd-381-effective-boundary-s47     b93d3b5   accepted on Wednesday's completion check — based on e032c7d
    rd-148-round2-s45                 690bed9   GO-with-findings — the gate said it "would ship without reservation"
    rd-361-round4-s45                 731aa6e   GO-with-findings — ships ONLY with G-1/G-2 ticketed (they are: RD-376/RD-378)

🔴 **EXCLUDED — do NOT merge:** `rd-376-stripper-reconcile-s47 @ 36191eb`. **Its gate is still
running at `%24`.** "Gate-passed only" is Kam's condition and it has not passed yet. If it returns GO
while you are working, **stop and tell me** — I will give a separate GO rather than you inferring one.

**Order matters and the stacks are real:** `rd-323` before `rd-377` and before `rd-381`; `rd-374`
before anything that depends on it. **Work out the order from the actual ancestry, not from my list's
order**, and say what you derived.

## HOW — Kam's condition is "one at a time, reporting each"
Per merge: **predict the tree BEFORE, re-derive the parents from the object AFTER, and carry a
NEGATIVE CONTROL** proving nothing came along that should not have — the shape the Secuura seat used
on #897 and the one I want here. **Report each merge as it lands**, not in a batch at the end.
**Stop immediately and tell me if:** a merge conflicts, a tree does not match its prediction, a gate
verdict turns out not to cover the head you are about to merge, or anything at all surprises you.

## 🔴 EXPECT THE SECRET SCANNER TO FIRE — this is the scanner working, not an incident
`gitleaks.yml` **runs on `main` only**, and `main` has not been fed since 2026-09-01 — so **six days
of commits have never been secret-scanned**, and RD-367 records that this is the sole remaining
explanation for **a credential still sitting in `terraform.tfstate.backup`**.
**So: merging will very likely trip gitleaks on a credential that is already in the repository.**
- **That is the point of the merge.** It is the scanner seeing six days of work for the first time.
- **Do NOT rewrite history, do NOT force-push, do NOT delete the file.** All three are irreversible
  and none is yours or mine — they are Kam's signature class.
- **Report it to me with the finding and the file**, and it becomes a ticket and a card for him.
- **Never paste a secret value** into a ticket, a mail or the pane — file, line, variable, class only.

## HOLDS
- **Datasec has NO production grant.** The demo is not production; a demo deploy is in scope, anything
  production-shaped is not. **If a merge would touch production, stop.**
- **No history rewrite, no force push, no credential change** — irreversible, Kam's.
- **External comms stay Kam's.** Nothing goes to a client human.
- **Never delete — quarantine.**
- **Names, not pronouns**, in every receipt.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- 2026-09-08 07:10, panel, verbatim: *"deploy and merge everything that has been tested and done and is ready for deployment."* -> **this brief is where it lands**, and your merge receipts are the artefact that closes it.
- 2026-09-07 19:00, card `nexusai-rd367-frozen-trunk` = `mergeup`: *"Wednesday merges only branches whose gate has PASSED, one at a time, reporting each."* -> already delivered in the s44 successor brief; restated here because it is the condition on today's action.

PROVENANCE:
- Kam's 07:10 words | `2_Project_Files/tools/kam_rulings_today.sh` run by Wednesday at 07:2x, reading the dashboard panel - his own channel, quoted verbatim, not paraphrased | read 2026-09-08
- The mergeup ruling and its condition, and that `deploy-demo.yml` deploys from `main` while `gitleaks.yml` runs on `main` only | `decision_queue.sh show nexusai-rd367-frozen-trunk`, read by Wednesday in this action - the card's own text, which is the NexusAI agent's measurement, RELAYED | read 2026-09-08
- That the `kamilDatasec` gh identity is not in the `datasecau` org and sees no repos there | `gh api user/orgs` and `gh api user/repos` under your project's GH_CONFIG_DIR, run by Wednesday in this action | read 2026-09-08
- The seven SHAs and their gate verdicts | Wednesday's own gate commissioning and the reports on disk under `Testing Agent MAIN/projects/nexusai/reports/` - RELAYED to you; re-derive them | read 2026-09-08

SELF-CHECK NOTES: the deploy hold is recorded as resolved by Kam's INSTRUCTION rather than by the unread settings, and Wednesday's own inability to read them is measured rather than asserted; rd-376 is excluded by name with the reason, so "everything ready" cannot be read as including a branch still at its gate; the gitleaks expectation is stated before the merge so a firing scanner is not mistaken for an incident.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 07:25
