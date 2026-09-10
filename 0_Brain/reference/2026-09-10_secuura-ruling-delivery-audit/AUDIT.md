---
date: 2026-09-10
type: reference
source: Wednesday, from decision_queue.sh + live GitHub/Linear reads
status: live
---

# Secuura ruling-delivery audit — 31 ruled cards with no delivered mark

**Why this exists.** Kam was asked three separate times to break the same GitHub
approval wall (#914 on 09-09, #934 today) that he had already ruled away on
**2026-08-26**. That ruling was never actioned and nothing in our records said so.
This is the pass I owed him: every ruled-but-undelivered Secuura card, classified
**ACTIONED / DISCHARGED / STILL OWED / DEFERRED**, with the evidence beside it.

**Method, and its limits.** Card list from
`decision_queue.sh list ruled --undelivered secuura`. Each checked against a live
source — the GitHub API for PRs, workflow runs and repo config, the Linear API for
ticket state. **Where I could not measure, the row says so rather than guessing.**
Nothing here is inferred from a card's own prose.

---

## 1. ACTIONED — evidence found, now marked delivered (6)

| Card | Ruling | Evidence |
|---|---|---|
| `secuura-934-blocks-every-push-needs-one-approval` | `kam-approves` 09-10 | **PR #934 MERGED** `2026-09-10T00:47:54Z`, commit `a1e49d15`. Checked past the merge flag: `systemTest/playwright/package-lock.json` on develop carries **smol-toml 1.8.0**, so GHSA-7w5x-hrqm-74c2 is off the trunk. |
| `secuura-merge-914-without-reviewer-approval` | `you-approve` 09-09 | **PR #914 MERGED** `2026-09-09T01:46:47Z` (KS-754). |
| `secuura-ks930-cap-vs-regression` | `one-more` 09-07 | **PR #876 MERGED** `2026-09-07T00:49:35Z`, 70 min after the ruling. |
| `secuura-ks949-round3-cap-and-the-cutoff` | `split` 09-07 | **PR #885 MERGED** `2026-09-07T02:24:47Z`, 10 min after the ruling. |
| `secuura-892-cap-spent-blocker-open` | `round3-narrow` 09-07 | **PR #892 MERGED** `2026-09-07T23:31:43Z`. |
| `secuura-892-round4-passed-but-introduced-two-majors` | `round5` 09-08 | Same merge, 81 min after the 08:10 ruling. |

---

## 2. DISCHARGED — the world moved and the ruling's premise is gone (2)

Both are about **GitHub Actions being dead**. It is not dead.

| Card | Ruling | What is actually true |
|---|---|---|
| `secuura-ci-billing` | `wait` **2026-08-26** | **Actions has been running since at least `2026-09-09T13:56Z`** and fired on the #934 merge at `00:47:56Z` today. |
| `secuura-ci-dead-19-days-blocks-your-own-ruling` | `fix` 2026-09-08 | Same. Whatever Kam did on billing worked, ~11 hours ago, and **nothing in our records noticed.** |

⚠ **But Actions coming back opened a new question, carded as
`secuura-actions-alive-but-security-gates-red`:** over the last 100 runs
(2026-09-09 13:56Z → 2026-09-10 00:47Z) the tally is **45 startup_failure · 25
failure · 22 success · 6 skipped · 1 cancelled · 1 in progress.** `PR Security
Gates (KS-168)` and `Security Scanning` **fail on every recent run I read**,
including on the #934 merge to develop. The 45 startup_failures all carry an empty
workflow name, all fall on 09-09 and stop after ~21:00Z — that burst reads as the
come-back window, not a live defect. **I have not opened a failing run's logs; that
is the seat's measurement, not my guess.**

---

## 3. STILL OWED — a concrete action nobody has taken (14)

### 3a. Kam's hands, and the first one is the expensive one

| Card | Ruling | State | Cost of it staying undone |
|---|---|---|---|
| **`secuura-agent-github-identity`** | `identity` **2026-08-26 17:12** | **NOT DONE** | **The most expensive open item in this list.** GitHub refuses `kksecura` approving its own PRs — I ran it today and got *"Can not approve your own pull request"*. It blocked **#914** (09-09) and **#934** (today). **Three times Kam's attention has been spent on a wall he ruled away 15 days ago.** With `raise-to-1` in force, **every future PR needs Kam personally** until this lands. Action: org invite for `secuura-blockchain@agentmail.to` at https://github.com/orgs/Secuura/people |
| `secuura-891-workflow-scope-merge` | `kam-merges` 09-07 | **PR #891 still OPEN** | One click. The agent's token is refused on `.github/workflows` files. |
| `secuura-required-approvals-zero-after-the-untick` | `raise-to-1` 09-10 | **NOT DONE — mine was refused** | My PAT gets 403 on ruleset writes. Kam's click: https://github.com/Secuura/Distributed_Secuura/rules/18499832 → Edit → Required approvals **0 → 1** → Save. |
| `secuura-ps-759-760-merge-owner` | `kam-merges` 09-05 | **UNMEASURED** | `Secuura/platform-s` does not resolve for this token — `gh repo list Secuura` returns only `Distributed_Secuura`. I cannot see that repo, so I cannot say whether PS #759/#760 merged. **Needs Kam or a seat with the right identity.** |

### 3b. Partially done

| Card | Ruling | State |
|---|---|---|
| `secuura-dependabot-triage` | `close-and-rescope` 09-01 | **Rescope DONE** — `.github/dependabot.yml` on develop declares only `npm` and `docker`; the `github-actions` ecosystem is gone. **The "close the 5 dead workflow-only PRs" half is unconfirmed** — 10 dependabot PRs are open now, presumably new npm/docker ones. Needs one pass over closed PRs. |

### 3c. Needs a measurement I did not run

These are all checkable; I stopped rather than spend the morning on them, and each
is one bounded read.

| Card | Ruling | What would settle it |
|---|---|---|
| `secuura-demo-kam-admin-default-password` | `b` 09-07 | **Possibly done via PR #885** ("KS-949: the demo platform admin gets a fictional identity and loses it", merged 09-07). The titles match the ruling almost exactly — but **matching titles is not evidence**, and this one is a live credential on a public demo, so it gets a read, not an inference. |
| `secuura-demo-admin-transcripts` | `redact` 09-07 | Do the 10 transcripts still carry Kam's name? |
| `secuura-archive-fifteen-platform-s-tickets` | `archive` 09-08 | Board read on Platform S — blocked by the same repo/identity gap as PS #759/760. |
| `secuura-four-advisories-ruled-after-measurement` | `bump` 09-09 | Are the four pins bumped on develop, or were they baselined instead? |
| `secuura-advisories-high-and-prod-reaching` | `measure-first` 09-09 | Was the nodemailer `resolveContent()` legacy-signature read ever done? |
| `secuura-advisory-gate-moving-set` | `both` 09-09 | Was the grace window built? |
| `secuura-org-trust-boundary-within-tenant` | `bind` 09-07 | Does the issuer/actor mismatch now 403? |
| `secuura-f5-demo-exposure-probe` | `probe` 09-07 | The probe ran (F5 confirmed live) — needs the result on a ticket. |
| `secuura-f5-demo-interim-mitigation` | `letitland` 09-07 | Did the real fix land? |
| **KS-968 family — 5 cards** (`ks968-demo-hash-probe`, `ks968-probe-control-query`, `ks968-hash-population-count`, `ks968-rotation-three-worlds`, `ks968-my-decision-table-was-void`) | probe / strong-control / count-populated / separate / hashcmp, 09-07→09-08 | All five authorise **read-only measurements**. **KS-968 is still `In Progress`.** Delivery = each result recorded on that ticket. This is the densest cluster of undelivered rulings in the list and it is one ticket. |
| `secuura-force-push-own-branch-standing` | `narrow-allow` 09-07 | A **standing rule**, not a task. Its artefact is the project's `CLAUDE.md` or the standing block of every Secuura brief. Currently in neither, so far as I can see. |

---

## 4. DEFERRED — Kam decided to wait; no action owed, but the record should say so (3)

| Card | Ruling |
|---|---|
| `secuura-ks229-disclosure-mailbox` | `later` 09-02 — leave the branch staged. KS-229 is `In Review`. |
| `secuura-demo-admin-mfa` | `later` 09-07 — leave MFA off, revisit after the suites run. |
| `secuura-f5-login-limiter-bypass` | `wait` 09-07 — wait for the full-boot confirmation, then decide. **Has that confirmation landed?** If it has, this is no longer a deferral and Kam owes a decision. |

---

## What I take from this

1. **The single highest-value item is the agent GitHub identity**, and it is not
   close. It has cost Kam three interruptions, and Kam's own `raise-to-1` ruling
   makes it cost him one per PR from here.
2. **A "delivered" mark is not bookkeeping.** Two cards described a dead CI that
   has been alive for half a day, and one described a wall Kam had already
   dismantled. Both would have been caught by a delivery check.
3. **Five of the 31 are one ticket** (KS-968). A per-ticket sweep would clear more
   than a per-card one.
4. **Two rows are unmeasurable from this seat** — Platform S is invisible to the
   identity I hold. That is a gap in what I can audit, and it should be stated
   every time rather than quietly skipped.

---

## 5. SECOND PASS — measured after the first draft (2026-09-10 10:55)

**KS-968 cluster: ALL FIVE WERE DELIVERED.** The measurements Kam authorised were
run *and* recorded; only the cards were never marked. KS-968 carries six
substantive comments, and two of them **cite Kam's authorisation by time in their
own text** (`panel 09:57, "Authorise ONE read-only comparison"`). The final
verdict is on the ticket: *"CLOSED — BENIGN. World (a), the incident, is
EXCLUDED."* All five now marked delivered, the two exact attributions distinguished
in the record from the three that rest on timing and content.

**Undelivered count: 31 → 19.**

### ⚠ The one that got worse on inspection, not better

`secuura-demo-kam-admin-default-password` (ruled `b` 2026-09-07: *"Replace the
identity everywhere now — the six files — AND set the password"*).

**Do NOT mark this delivered. It is partially done at best, and it is Kam's own
identity on a public demo.**

- **PR #885 merged** 2026-09-07 — *"KS-949: the demo platform admin gets a
  fictional identity and loses it"*. So the code change shipped.
- **But KS-949 is still `In Progress`**, P2. Its own description names **two live
  sites** (`services/auth/.../userRepo.ts` and
  `services/api-gateway/src/startup-migrations.ts`) and records that the sibling
  ticket **KS-913 is `Tested Not Deployed`** — this project's explicit state for a
  fix that exists in code and has not reached a box.
- **I have NOT measured whether the fix is deployed to the demo VM.** Merged is not
  deployed, and this repo has a whole state for the difference. **Until someone
  reads that box, we cannot say Kam's name and a published password are off it.**
- **Residue tickets are open and neither is scheduled:** **KS-986** (Backlog, P3) —
  `USER_TESTING/CREDENTIALS-AND-PORTALS.md` still advertises
  `admin@secuura.com` / `admin123` at lines **68** and **177**; **KS-951**
  (Backlog, P2) — the CI default-password gate exempts **16 published passwords by
  design** and **4 of 5 planted canaries walked past it**.

**Recommended next action:** one read-only check on the demo VM answering a single
question — *does the seeded platform admin row still carry `kam@secuura.ai`?* That
is one query, and it converts this from an argument into a fact.

### Others refined

| Card | Revised state |
|---|---|
| `secuura-f5-demo-interim-mitigation` (`letitland`) | **KS-946 is `In Review`**, not merged — *"Four path spellings dodge EVERY path-scoped gateway limiter — a CLASS"*. The real fix exists and is awaiting review, so the ruling is in flight rather than delivered. |
| `secuura-dependabot-triage` (`close-and-rescope`) | **Rescope CONFIRMED done** — `.github/dependabot.yml` on develop declares only `npm` and `docker`; `github-actions` is gone. The "close the 5" half stays unconfirmed. |
