# B385 drafter report (Tuesday's drafter, Sonnet 5.5, 2026-10-21 07:4x AEDT)

Brief: `2026-10-21_B385_SEAT-R13_nexusai-follow-redirects-audit.md` (130 lines). Stamp slots: main-pin x3 (REFUSE, Stamp, worktree command), stamp-time x1, authority x1 (5 occurrences on 3 lines; the REFUSE grep counts lines). No `.pre-stamp` copy written (outside the two permitted paths); Tuesday makes it before stamping.

## Key findings (MEASURED unless marked)
- main = `115a775b6d5808629f493ef7a3f602d8c5853a22` (ls-remote, 07:43:46; control: same call form printed the line). Open PRs: #103 `rd-780-regex-anchors-r12` @ 138b78eb, #102 @ 6dcbedb9, #101 @ 48a17df8, #67 @ 94b288cc. Panes: no NexusAI pane live; no `Datasec/NexusAI-R13`.
- CI command (copied from `.github/workflows/npm-audit.yml` at main): `npm audit --omit=dev --audit-level=moderate --json`, after `npm ci --no-audit --no-fund`, node 24.
- Parent: `node_modules/follow-redirects` = 1.16.0 (`package-lock.json:4068`, production, no dev flag). Parents: `axios` 1.20.0 (`:2162` declares `^1.16.0`; axios is a DIRECT dependency `^1.18.0`, `package.json:52`) and dev-only `http-proxy` (`^1.0.0`). Both ranges admit 1.16.1, so NO override and NO package.json change are expected; `npm update follow-redirects` should change one lock entry. Precedent: `745978b` RD-816 (proxy-addr, lockfile only, 7+/3-).
- Existing ticket: none found. Jira text search (project RD) for `follow-redirects` (only RD-516, unrelated), the two GHSA ids (0), `audit-production-deps`, `npm audit`; summary search `audit|advisory|redirects`; newest ticket RD-878. Brief has the builder file ONE Jira ticket (shape of RD-816: Task, Highest, labels dependencies+security, assignee Kamil Kreiser, the assignee on every comparable ticket).
- CLARIFICATIONS: no rule on follow-redirects, accepted advisories, audit baseline or overrides policy. Applicable: C-196 (`:2134-2140`, security fixes to shipped code go first; major bump of a direct dependency during an advisory fix = STOP), C-210 (`:2287`, RD-816 method), C-190/C-209, C-57/C-68/C-89, C-185, C-192, C-110/C-114. Last entry still C-218 at `:2362`.
- Existing `overrides` in package.json (`tar`, `uuid`, `@tootallnate/once`) each carry an `overridesNotes` entry; the brief makes any new override carry one too (fallback only).
- Five tests mention `package-lock` or `follow-redirects` (listed in the brief); none opened.

## Proposed routing
Row C2 (pilot), Sonnet 5.5, launch with `BRIEF_SEAT_LEVEL=sonnet`. P1 NO (branch only; the ticket create is a Jira write assigned to Kam's account, see Q1), P2/P3 per gauge at launch (Tuesday records it), P4 Datasec so Claude columns only (no local tier). Honest note: this is a one-entry lockfile change, the smallest NexusAI brief so far; C2 is the nearest row, no row names "dependency bump".

## Questions (recommended answers)
1. The brief authorises ONE Jira create (RD ticket assigned to Kamil Kreiser, Highest). B374 forbade all Jira writes. Recommend YES (you asked for the builder to file; precedent RD-816/RD-741 were filed by seats) or Tuesday files it herself before launch and the brief cites the key.
2. Priority: Highest or High? The drafter has no rule; RD-816 (critical) was Highest, RD-741 Medium/Bug. Recommend Highest because it blocks every PR's required check.
3. Allow the builder network access to the npm registry only (`npm update/ci/view/audit`)? Required to do the work; B374 had none. Recommend YES, registry only.
4. Full `npm run verify` (about 28 min under the lock) for a lockfile-only change? Recommend YES: five tests read the lockfile or package and the audit change touches the shipped dependency tree.
5. Priority over PR #103's landing: C-196 lets a security fix take the next merge turn by Tuesday's word. Recommend land B385 first, then forward-merge main into PR #103 (Tuesday's step).
6. Land by C-190 same-commit fast-forward after QA gate (tier 2 as tooling/config); a tier-1 gate is not needed unless `npm update` moves anything beyond the one entry. Recommend tier 2.

## Could not verify
- That follow-redirects 1.16.1 exists and clears both advisories (no HTTP to the registry made); what `npm update` actually changes.
- The CI job logs of PR #103's two failed jobs (relayed from Tuesday's finding, not re-read).
- That `npm audit` is red locally at the pin; npm major version equivalence with the lock writer.
- Whether the jest lock is held now; the three tool sha256s (B355 values relayed).
- Whether any of the five lockfile-mentioning tests pins a version.
- Reachability of the advisory in NexusAI's configuration (deliberately out of scope, C-210 method).
