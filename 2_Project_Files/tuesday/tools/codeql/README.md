# pr_codeql_check - local PR CodeQL check for gates

Owed by the 2026-11-19 ledger row: gate B1727 counted CodeQL result ROWS ("0 new") and hosted CodeQL then blocked
NexusAI PR 229 with five alerts that main already held. The hosted PR check keeps any result whose data-flow path
touches a line the PR ADDS. This tool reproduces that rule locally, before a push.

## Use

```
pr_codeql_check.sh --repo <owner/name> --checkout <local clone, read only> --base <sha> --head <sha> \
                   --lang <javascript|python|csharp|java|go|ruby|cpp|swift> --work <scratch dir> [--allow-empty] [--fresh] [--threads N]
```

Exit: 0 pass, 1 would block (Major / landing blocker), 2 tool error. Only `javascript` is proven (see below);
the other languages use the same suite name pattern and are untested.

**A scratch clone is the normal path.** Other projects' checkouts are read-only to this seat and often lack the PR
objects (the NexusAI checkout lacked even the base sha). Clone into the scratch dir and point `--checkout` at it:

```
GH_CONFIG_DIR='<project>/4_Credentials/.gh-config' gh auth status     # must show the client's account first
GH_CONFIG_DIR='<project>/4_Credentials/.gh-config' gh repo clone <owner/name> <scratch>/clone -- --no-checkout
```

The tool only runs `git --no-optional-locks` read commands in the checkout (`rev-parse`, `archive`, `diff`); it never
checks out, fetches or writes there.

## What it does
1. Resolves both shas (rc 2 with git's own error if either is missing).
2. `git archive` each sha into `<work>/trees/<sha>`; builds a CodeQL DB per sha (`<work>/db/<sha>-<lang>`, reused when its
   marker file names the same sha and language; `--fresh` rebuilds), CLI 2.27.4 at `2_Project_Files/tools/codeql/codeql/codeql`.
3. Analyzes each DB with `<lang>-security-extended.qls` to `<work>/sarif/`. Strictly one CodeQL process at a time.
4. Diff pack: added-line ranges of head vs base (`<work>/diff/added_ranges.json`).
5. Post-filter on the HEAD SARIF: a result is KEPT when the START line of its primary OR any related location is an added line.
6. Compares (ruleId, file, primaryLocationLineHash) multisets head vs base: NEW and GONE.
7. Verdict table; rc 1 if KEPT(high+) > 0 or NEW(high+) > 0. A run with 0 results on one side and >0 on the other is rc 2
   unless `--allow-empty`.

All outputs go to `--work`. Nothing generated is written under this directory (`.gitignore` here also blocks db/sarif/trees).

## Severity rule
HIGH+ means: the rule's `security-severity` >= 7.0 (GitHub's "high" band); a rule with no security-severity counts only if
its `problem.severity` is `error`. This mirrors the repo ruleset (`security_alerts_threshold: high_or_higher`,
`alerts_threshold: errors`). The table lists KEPT results of every severity but only HIGH+ decides the rc. Hosted said
"5 new alerts including 4 high": `js/http-to-file-access` (6.3) is listed but does not block on its own.

## What it does NOT reproduce (the residual)
- It is an approximation. The hosted run at landing stays the authority.
- Hosted default-setup runs its own CodeQL bundle and queries; locally it is the CLI version here with the packs it has.
  Drift in either changes results.
- The post-filter is the START-line rule, inferred from one case (PR 229 round 1: reproduces the hosted five exactly;
  a span rule would add two `js/missing-token-validation` alerts hosted did not list). Whether hosted uses anything
  beyond that for labelling alerts "new" is unmeasured.
- Hosted analyzes the PR merge ref context / a diff-informed query run; this analyzes the head commit tree, not a merge with
  a moved base. Pass the PR's real base sha; a stale base can differ.
- Only the languages and build modes listed are wired; csharp/java use `--build-mode=none`. Non-JS languages are unproven.
- Hosted SARIF fingerprints were compared by hand in B1728 (equal on main and PR head); this tool compares local-to-local only.
