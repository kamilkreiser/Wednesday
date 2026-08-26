# Secuura development process

**Agreed 25 August 2026 — Stuart, Peter, Kamil.**

Five stages, two roles. Authors test their own work and record it in the PR; a reviewer who is not the author approves; the author merges and deploys. Deploys stay manual, so no CI/CD minutes are billed.

## The flow

```
  01 ─────────── 02 ─────────── 03 ─────────── 04 ─────────── 05
  Author         Author         Reviewer       Author         Author
  Build on       Test it,       Review &       Merge to       Pull and
  a branch       raise PR       approve        develop        deploy
```

| # | Owner | Stage | What happens |
|---|-------|-------|--------------|
| 01 | Author | Build on a branch | Develop on a feature branch off `develop`. Commit and push as you go. **Name the branch after your own work, never after someone else's ticket** — the Linear/GitHub integration moves a ticket to *In Progress* the moment a branch or PR carries its key, and on 26 Aug that silently moved a ticket Stuart owns. |
| 02 | Author | Test it, then raise the PR | Test your own work before the PR goes up and fill in the **Test Evidence** block (below) in the description: what you touched, what you ran, what you didn't get to, any migrations or config changes. Short is fine; honest is required — a "not run" line is the point of the block, because the reviewer sample-tests on top of it and needs to know where to look. |
| 03 | Reviewer | Review & approve | Full review of auth, tenancy, migrations and anything crossing service boundaries; spot checks elsewhere, plus sample testing on top. Fixes discussed with the author, then approval. Peter is the default reviewer; **any of the three who is not the author can approve** (see *Review capacity* below). |
| 04 | Author | Merge to develop | The author merges once the PR is **approved** — and, when GitHub Actions is available, checks are green. `develop` never waits on one person being at their desk. Squash-merge preferred. |
| 05 | Author | Pull and deploy | Pull `develop` and run the deploy manually. Whoever merged deploys, verifies at the target (not just locally — demo runs real anchoring where local mocks it), and stays on hand if it goes bang. |

## Test Evidence block (paste into every PR description)

```markdown
## Test Evidence
- **Touched:** which services / packages / files
- **Ran:** which suites actually executed, and their results
- **NOT run:** what you did not get to, and why
- **Migrations / config:** any schema change, env var, or config this needs
```

This is the wording already in `CONTRIBUTING.md` (PR #733), so the two documents say the same thing.

## Why it's shaped this way

- **Review isn't testing.** Untested PRs turn the reviewer into the bottleneck and stall the automation work Peter owns.
- **Separate the ticket from the review.** The author tests, but a second pair of eyes signs it off — never the same person on both.
- **Merging doesn't wait on the reviewer.** Approval is the gate, not availability. `develop` keeps moving when someone is off.
- **Manual deploys, no billed minutes.** The reason the last stage is by hand rather than a pipeline.

## While GitHub Actions is unavailable

CI has been dead since 17 August (org billing). Until it returns:

- **The gate is: reviewer approval + a filled-in Test Evidence block.** The "checks green" rule is *suspended, not retired* — it re-arms by itself when Actions runs again.
- **`mergeable_state: clean` is not evidence that anything was tested.** With no checks running, every PR reads *clean* or *unstable* for reasons unrelated to whether the code works. The Test Evidence block carries the testing claim; the GitHub badge carries none of it. (KS-660 / PR #721 exist to bannerise exactly this.)
- **Manual equivalents of the CI gates** — which `systemTest/` runners stand in for which pipeline jobs before a merge — are defined on **KS-685** (Stuart). Until that lands, the Test Evidence block names what was run.
- **When Actions returns:** merge the frozen queue in the recorded order (#721 → #720 → #718, then #568 on Kamil's sign-off), then re-push anything opened during the outage so the checks-green leg re-arms on real runs. Dependabot PRs (15 waiting) follow the same five stages; batch them.

## Review capacity — the constraint this flow creates

On 26 Aug, **16 of our open PRs carry zero approvals**, and Peter has moved onto Platform S. A flow where every merge waits on one reviewer's approval moves the bottleneck from CI to that reviewer. Two things keep `develop` moving:

1. **Approval can come from any of the three who is not the author** — Stuart, Peter or Kamil. The rule is *not the same person*, not *always Peter*. Peter remains the default for auth, tenancy, migrations and cross-service changes.
2. **Authors make review cheap:** small PRs, the Test Evidence block filled in, and the "NOT run" lines honest so the reviewer's sample testing lands where it matters.

*(Point 1 is a proposal from this review, not yet agreed by the team — it follows from the flow's own reasoning that `develop` must not stop when one person is off.)*

## AI-agent-authored PRs

Agent sessions (Kamil's Wednesday fleet) follow the same five stages with no exceptions: the agent is the author, fills in the Test Evidence block from the start, never merges without a human approval on the PR, and never pushes to `develop`. The human who launched the session is accountable as the author.

## Branch protection on `develop`

- At least one approving review required
- Status checks must be green — *suspended while Actions is unavailable; re-arms automatically*
- No pushing straight to `develop`
- Branch-protection and org settings are changed only by the org admin (Kamil)

---

*v2 · 26 August 2026 — updated from v1 after the first day under the flow (zero approvals on 16 PRs; the branch-naming trap; `clean` ≠ tested; CI-outage gate). Repo copy: `CONTRIBUTING.md` on PR #733; process ticket KS-685.*
