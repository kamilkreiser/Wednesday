---
date: 2026-09-10
type: reference
source: Peter (Secuura reviewer), sent by Kam on the panel 2026-09-10T20:27:50 with the file attached; adopted by Kam 20:29:36
status: live
---

# Peter's PR verification protocol — and what it obliges US to do

**Full document (624 lines):** `0_Brain/dashboard/uploads/2026-09-10_202745_pr-verification-request.md`
**Kam's adoption, verbatim (panel 20:29:36):** *"Peter knows what he's doing and has considered this
item carefully, so please look at implementing the flow and process he has outlined, unless you see
anything that needs to be challenged, in which case let me know."*

## The one structural thing to understand before anything else

**This is Peter's REVIEWER-side protocol. It is not a checklist we run.** What binds us is the
**AUTHOR side it assumes** — the state a PR must already be in before his protocol can be run
against it at all. His document says so in three places: *"the gate is the reviewer's APPROVAL plus
a Test Evidence block … filled from LOCAL runs by the author"*, *"the AUTHOR merges, not the
reviewer"*, and *"ticket and review must not sit with the same person."*

**So: reading it as a to-do list is the wrong reading. Reading it as the acceptance criteria for
every PR we hand him is the right one.**

## What every Secuura PR we open must now carry

1. **A RISK MAP FIRST (§1b)** — a table of every touched file classified HIGH / MEDIUM / LOW, placed
   ahead of the summary. **If any HIGH area is touched, the first line of the PR says so.**
   HIGH areas: authN/authZ/tenancy/IDOR · migrations/schema · crypto/PII/secrets · on-chain/anchoring
   · Zod validation · api-gateway routing/spec-auth · S↔K channel/shared contracts · **systemTest gate
   /report/baseline logic** · dependency bumps with a security surface.
2. **UNIT TESTS THAT BITE (§10)** — and *bite* has a specific meaning: **revert the fix, confirm RED,
   restore, confirm GREEN, and SAY you did it.** *"A test that stays green with the fix reverted is
   not a test."* **A HIGH-risk area with no biting test is an automatic NO whatever every suite says.**
   Watch the **KS-688 shape**: a test that shares the defect's own assumption and returns a confident
   green.
3. **A Test Evidence block** — touched / ran / NOT run / migrations+config — filled from LOCAL runs.
   **`mergeable_state: clean` is NOT "tested".**
4. **Config-drift completeness (§3b)** — a new env var must appear in `Blockchain/Dev/.env.example`,
   the docker-compose service block, `docs/ENVIRONMENT-VARIABLES.md`, and
   `deployment/azure/services.bicep` commonEnvVars. *"A var read in code but absent from the template
   is a finding — it is exactly how LOCAL_LOGIN_LIMITER_DISABLED went missing."*
5. **Both HTML docs moved in the same commit** if a test changed — platform-k:
   `"Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html"` and
   `"Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html"` (quote the path; the space
   kills unquoted globs). Timings must agree across both, quoted with host + date, **from a SERIES
   run only**, ceilings ~2× the measurement.
6. **PR body:** the Linear URL and both pre-merge ack checkboxes.
7. **Branch + diff hygiene** — Git Flow direction, branch name matches Linear's `gitBranchName`, no
   generated folders, no run artefacts, no unrelated lockfile churn, no TODO/FIXME without a ticket.

## The SERIES RULE (§6) — adopt it for our own gate runs, not just his

**One suite at a time, machine-wide. Nothing builds while a suite runs.** Measured by Peter
2026-08-20: Playwright + Schemathesis + k6 concurrently gave **300 engine errors across 289
operations, all login rate-limiting — and the report still read PASSED.** *"A run that tests nothing
and reports success is worse than a red one."*
- Announce the order first; report each suite's **ordinal and clock window**.
- **Rate limiting appears → stop, wait 15 minutes.**
- **A failure is re-run ONCE, alone, after the suite has fully exited.** Same = regression.
  Different = flake — **and a flake still gets a ticket, because a flaky test is a defect in the
  test.** Never count the green re-run as the result.
- Slot isolation (KS-682) is **not** a licence to overlap: the slots share one CPU allocation, one
  host IP and one per-IP login limiter, so a parallel run *"buys speed by making its own numbers
  unquotable."*

## Known-failure discipline (§2b) — the rule that stops us burying the one that matters

*"Never report a Schemathesis failure as new until you have checked it against the baseline AND
Linear."* Baseline: `systemTest/schemathesis/config/schemathesis-baseline.json`, 97 triaged pairs
keyed `CHECK::OPERATION`, enforced by `baseline_gate.py`. **Entries expire 2026-10-31 — an expired
or malformed entry fails the gate too.** Counts are evidence, never a gate condition (the tool
reseeds each run). **Never hand-edit the baseline to make a run green.**

**The KS-595 anti-pattern:** a live finding pointing at a **closed** ticket. A DONE ticket is not
coverage and must not be commented on — open a new one and link the closed one as related.

## The ticketing rule (§2c) — and it is stricter than ours

Search Linear by **check name, operation path, failure class, service name, spec/test name and
error string** — not by the ticket number quoted in a baseline entry. Then: a ticket in **Backlog,
Todo, In Review, In Progress or Blocked → COMMENT, never create.** Create **only** when nothing
exists in any of those states. **Coverage counts even when the wording differs.** Comments append —
**never rewrite a description or retitle someone else's ticket.**

⚠ **Scope:** §2c ticketing and the §2d PR comment are pre-authorised **to Peter's own verification
run**. They are **not** authority for us to file findings from code reading or to comment on PRs.

## Authority rule (§3.2) — worth encoding

**platform-k base code → Kamil decides · platform-s code → Stuart decides · `systemTest/` on BOTH
platforms → Peter decides.**

## What blocks approval (§2c)

- **platform-s PR:** only a **platform-s failure with no covering Linear ticket** blocks.
- **platform-k PR:** any **NEW** (unbaselined, untracked) failure in any suite blocks.
- **Either:** a **HIGH-risk area changed with no biting unit test** blocks, regardless of suites.

## BLUR (§4)

Brief, blurred edges — diplomatic, kind, polite. **Never quote Peter's machine-local rules at
another developer as policy.**

## 🔴 WHERE HIS DOCUMENT IS NOW FACTUALLY OUT OF DATE — measured by us 2026-09-10

**§3.7 states: *"GitHub Actions is RETIRED for this repo, so there is no CI to read."* That is no
longer true.** Card `secuura-actions-alive-but-security-gates-red`, Kam ruled `measure-then-decide`
at 11:00 on 2026-09-10: Actions came back ~11 hours earlier and **its security gates now fail on
many PRs — but NOT all.** ⚠ **"essentially every PR" was an OVERSTATEMENT this file carried until 21:2x.** Measured on **#896: `PR Security Gates (KS-168)` PASSES**; its two reds are a real `Run Playwright API tests` failure (inside the Playwright suite that PR rewrites) and a `Dependency Audit` failure in the gates' own validator. **The failing SET varies per PR — do not generalise from the three s170 measured.** Consequences his protocol has no rule for yet:
- There **is** CI signal again, and it is red.
- `mergeable_state` reads **`unstable`** on six of seven open PRs — which is what a live-but-failing
  checks run produces. (Measured by s170, 2026-09-10 ~20:2x. Cause not yet confirmed.)
- His protocol's gate — *"the reviewer's APPROVAL"* — is **not technically enforced**: measured the
  same evening, `required_approving_review_count = 0` and `required_status_checks` is **absent** from
  the `require-pr-gates` ruleset. Kam ruled `raise-to-1` at 10:32 and it is **unapplied**.

**Drafted for Kam to send. It is external comms to a client human — never sent by an agent.**

## Tension worth holding, not a challenge

Peter's protocol is **heavyweight and per-PR** (up to six suites in series, full teardown and rebuild
between). Kam's standing instruction (2026-09-03) is that **Peter would rather review three big
things with sub-issues than thirty**. Both can be true only if PRs reach him **batched into review
streams**. This makes the batching Kam already asked for more load-bearing, not less.
