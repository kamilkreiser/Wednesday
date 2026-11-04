GO WITH NOTES — MERGE (no HOLD-FOR-KAM)

# QA Gate 181 (Tier 2, round 2): PR 1995 / KS-1320 CONTRIBUTING says the 92-character squash subject is a convention, not a check

Merge tree for the merge seat: `17da150e2b65ad1e9d5df2cd9d37fb1dc941dafa` (merge-tree of head onto develop, rc 0). Expected squash tree = the same tree (one file changed; see Q4).

## Subject
- Start and end pin (identical, read by `git ls-remote origin` in my clone): `refs/pull/1995/head` = `eb2cef57d279837257b5100611dd935123249215`; `refs/heads/develop` = `8f4e745227391acf474d4a565f17785a2d32f1c0`. Equal to the commission and to R 83rd's READY. Head did not move.
- Clone: `git clone --shared` of the read-only checkout into `<workdir>/repo`, origin re-pointed to the GitHub SSH URL, PR ref and develop fetched into my clone only. Checkout got read verbs only.
- Method: diff of head against round-1 head and against base, then `git grep` on the head commit (hooks, workflows, whole repo) with a control per zero. Ran on git only; no Node, no tests (docs-only gate).

## Findings
None at FIX-BEFORE-MERGE. Two notes:

### G181-N1 — LOW (note): the sentence is true of the repository, but a seat-side tool outside it does refuse long titles
**FOUND:** The clause "a longer title is not rejected when the PR is opened" is unqualified by "in this repository" in its own text, and R 83rd's READY says a seat-side tool outside the repo (`subject_check_ks_v17.sh`) does refuse a subject over 92 bytes when a seat creates a PR. The repo and GitHub reject nothing, so the clause is true as the commission ruled ("what the repository shows"). A reader could take it to mean no process anywhere refuses.
**TESTED:** Repo side only (below). The seat tool was not run or read by me.
**HOW:** Not a defect; Wednesday's call whether it matters. Round 3 is not available under the cap.

### G181-N2 — NOTE: Q3 (title and body) not verifiable by me
**FOUND:** The repo is private, `gh` in the project's config dir is logged out, and unauthenticated API returns 404. I could not read the PR title or body.
**TESTED:** Only the exact title string in the commission: 92 characters, 92 bytes, ASCII (python len). The body's "Round 2 (gate 179)" section, G179-F1 naming, no close-word, no `@` are NOT checked by me; they rest on R 83rd's READY (which reports a close-word scan with a planted control). Wednesday should read the live body once before merge.

## What passed (measured)
**Q1 G179-F1 closed — yes.** The three added lines at head (`Blockchain/Dev/CONTRIBUTING.md` 107-109): "Our convention is a squash subject of 92 characters or fewer, so keep the PR title within that. Nothing in this repository checks it, and a longer title is not rejected when the PR is opened (KS-1320)."
- The round-1 text "and ASCII only" and "the merge gate finds it" are gone (diff against old head 15c32a6ef: 3 removed lines, all replaced).
- "Nothing in this repository checks it": `.githooks/` holds one file, `.githooks/pre-push`; `git grep -ciE 'title|subject'` on it = 0 hits. `.github/` holds 20 files; grep for `pull_request.title|PR_TITLE|pr_title` = 0 hits; `.github/pull_request_template.md` has no title/subject/squash/92/ascii line; grep for ascii in `.githooks`/`.github` = 0. Repo-wide grep (title|subject|squash within 80 chars of the number 92, both orders) = exactly 1 hit, the new CONTRIBUTING line itself. Controls in the same runs: that regex hits the new sentence (non-zero); "pre-push" in `.githooks` = 26; "pull_request" appears in 3+ workflow files, so the search could fire. (My first repo-wide regex returned 0 and failed its own control because of a `[^\n]` ERE slip; I rewrote it and it passed. The 0 above is from the corrected one.) Also `systemTest/playwright/.githooks/pre-push` exists; it is not a title check by name, but I did not read it (see NOT tested).
- "not rejected when the PR is opened": no workflow reads the PR title (0 hits above), so the repo shows no opening-time rejection. "Convention" is a claim of intent, which the sentence presents as such. "(KS-1320)" is the ticket reference only.
- "Feature PRs into develop stay squash" is unchanged pre-existing text.

**Q2 No new claim — yes.** `git diff --stat` base..head: 1 file, +3/-1 (`Blockchain/Dev/CONTRIBUTING.md`). Round-1 head..head: 1 file, +3/-3, same file. `git diff --name-only` between heads lists only that file. No hook, workflow, or script touched. 2 commits in develop..head. Both commits have no code.

**Q3 (partial):** title string counted 92/92/ASCII. Rest not measured (G181-N2).

**Q4 Merge.** `git merge-tree --write-tree 8f4e7452… eb2cef57…`: rc 0, tree `17da150e2b65ad1e9d5df2cd9d37fb1dc941dafa`. Merge base `ea5134d6b98c`. Develop has moved 3 commits since the base (KS-1343 docs a01e579ca; two KS-1868 code/test commits). Shared paths between develop's changes and the PR's changes: 0. Planted control: the same comparison of develop's change list against itself prints 24 paths, so the instrument can fire. CONTRIBUTING.md blob: base `0b7abad2`, develop `0b7abad2` (unchanged on develop), head `b26448b6`; the merge-tree's CONTRIBUTING.md blob = `b26448b6`. Expected squash tree: develop plus the one-file diff = `17da150e2b65…`, same as the merge tree (squash applies the same single-file diff to the same develop).

## NOT tested
- GitHub branch protection / rulesets (not readable without an identity), as commissioned. A ruleset could in principle check titles; the repo-side claim says "in this repository" for the checker but the "not rejected when opened" clause is unqualified, so a server-side rule is the one thing that could make it false.
- PR title and body as live on GitHub (G181-N2); no `@` or close-word check by me.
- The seat-side tool `subject_check_ks_v17.sh` (not run, not read).
- `systemTest/playwright/.githooks/pre-push` contents; markdown link check; any test; platform suites; Spark shadow (not run per commission).
- Squash tree is derived from merge-tree and blob comparison, not from performing a squash.

## Plain answer for Kam
This change only edits one paragraph in the contributor guide. The old wording promised that a merge gate would catch a PR title longer than 92 characters and that titles must be ASCII only; nothing in the repository does either. The new wording says 92 characters is a convention, and that nothing in the repository checks it. I checked the hooks and workflows and the new wording matches them. Merging changes no behaviour for users. Before merging, Wednesday should read the live PR title and body, which I could not open.

(Start/end pin: both identical, above.)
