# DRAFT 2 — reply to Peter on PR #896. **KAM SENDS THIS. Not sent by any agent.**

Separate from the protocol reply in this folder. Send them together or apart, Kam's call.
BLUR per his §4. Nothing here quotes anyone's machine-local rules as policy.

---

Peter — reviewed #896. **No blockers from us.** Both red checks attribute away from your change, and
one of them turns out to be your change fixing something. Details, because two of them are worth
your time.

**The Playwright red is not yours, and the reason is more interesting than that.** Your branch is the
only one in the repo whose `Quality gate — static` step passes. On `develop` — and on four other
branches we checked, fourteen runs in total — that step fails, so steps 7 through 10 are skipped and
`Run Playwright API tests` has **never executed** there. So #896 is the only thing that has ever
reached the actual tests. A job-level comparison reads "fails on both, ignore it"; a step-level one
reads "only red on Peter's branch, blame Peter". Both are wrong. There is no green baseline to
regress from, because a skipped step is not a passing step. Your `global-setup.ts` docblock fix is
what unblocks it, and you say so in your own diff — we measured it independently and reached the
same place.

**What is actually failing at step 10 is `BOOTSTRAP_ADMIN_PASSWORD`, which is set in zero workflow
files.** No bootstrap admin means every actor falls back to OWNER, four of five hold the wrong role,
the manifest is not published, `getTestAdminPassword()` falls back to an empty string by KS-966's
design, and the login returns 400 before authentication is even attempted. The step goes red having
run zero of eleven tests. That is KS-969, which is In Progress and assigned to Kamil.

**One thing that belongs to neither ticket, and we think you should see it.** KS-969's DEGRADED
message promises the suite keeps its correctly-roled seeded accounts. Since KS-966 site 8 that
promise is false for the admin persona, whose seeded password fallback is now empty. Two individually
correct changes compose into a guaranteed failure that surfaces as an opaque 400 inside a fixture
three steps later — and the pre-suite exits 0 on DEGRADED, so nothing stops the run. Neither ticket
owns that seam.

**And a smaller one in the same family.** The env-drift guard scans `config/` only.
`BOOTSTRAP_ADMIN_PASSWORD` is read from `fixtures/provision-actors.ts`, outside the scan, and is
documented in no template. The one variable currently red-lining CI is the one variable the drift
guard structurally cannot see. Widening the scan to `fixtures/` looks like a small change and it is
not this PR's job.

**The second red — `Dependency Audit` — is repo-wide, not yours.** The identical step fails on three
independent branches we checked, with every other step in that job green on all three. That job is
`pull_request`-triggered only, so there are no develop runs to compare against; the cross-branch
control is the instrument instead.

**On the tests.** We reproduced your suite locally — 239 tests, 22 suites, all passing, matching CI —
and bite-tested four of the guards by reverting the thing each protects. All four went red with all
239 cells running, and restored green. The artefact-path one is the one we would highlight: CI was
uploading `reports/`, a directory the suite has not written to since KS-666, with
`if-no-files-found: warn` — so the job reported green having uploaded an empty directory. You found
it, fixed both workflows, moved it to `error`, and guarded it with a test that bites. That is the
kind of thing that stays broken for months.

We also noticed your anti-vacuity cell next to the env guard — the one asserting the scan really does
find the variables the suite reads. We spend a lot of effort imposing that discipline; good to find
it already in the diff.

**We ran no suites, deliberately.** Akto, Schemathesis and k6 are all green on this exact head, and
Playwright cannot answer anything while `BOOTSTRAP_ADMIN_PASSWORD` is unset — it is determined to
fail at auth setup with zero tests executing. If you want an end-to-end proof of the slot isolation,
the order is: set the variable, then one Playwright run. Not four suites.

Nothing else from us. We have not approved, commented on or touched the PR — `systemTest/` is your
ground and this is advisory.

---

## Notes for Kam — NOT part of the message

- **Every claim is measured, with a control.** Step enumeration on both sides · 14 runs across 6
  branches · cross-branch control on 3 branches for the audit red · `BOOTSTRAP_ADMIN_PASSWORD` in
  zero workflows with `API_BASE_URL` returning 6 files as the positive control · 4/4 bite tests with
  cells-run quoted.
- **What I left out on purpose:** the KS-1081 env-template disagreement (doesn't bear on this PR),
  and the `akto-autoheal` root+docker.sock finding — still separate, still yours to time.
- **Two things in here are arguably his to action** (the KS-969/KS-966 seam, and widening the
  drift-guard scan). I've framed both as "you should see it" rather than as asks. **Cut either if
  you'd rather not hand him work while he's waiting on us.**
- **This does not approve the PR.** #896 still has zero reviews and the approval is yours to give —
  and worth noting his Schemathesis pre-merge box is unticked while its CI job is green, so that's
  an untidy box rather than a real gap.
