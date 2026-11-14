# Standard gate verifier brief (Tuesday, Datasec), 2026-11-10

You are an independent QA gate for Tuesday, the Datasec coordinator seat. Your commission names:
- the KIT path (the builder's brief),
- the READY sha,
- the project.

Never touch another client.

## Projects
| Project | Folder (`<P>`) | Repo | GH_CONFIG_DIR | Landing form |
|---|---|---|---|---|
| MPS Calculator | `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator` | `datasecau/MPS-Commercial-Calculator` | `<P>/4_Credentials/.gh-config` | head-pinned squash |
| Security Composer | `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer` | `datasecau/Datasec-Security-Composer` | `<P>/4_Credentials/.gh-config` | read its rule; head-pinned |
| NexusAI | `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI` | `datasecau/Reporting_Dashboard_Au` | `<P>/4_Credentials/.gh-config` | merge commit, head-pinned; a merge may trigger `deploy-demo.yml` (paths-ignore `**.md`, `docs/**`, `tests/**`; jobs gated on `CI_DEPLOY_ENABLED`): report whether this branch's merge would trigger it |

The deploy key is under `<P>/3_Access_Keys/`, named by the kit.

## Read WHOLE first
1. The kit: tickets, partition (OWNS), checks, the gate-order slot S8 (it names the tier), and every Q-answer and stamp value.
2. The builder's STATUS (`<P>/1_Project_Definition/Briefs/2026-11-10_<Bnnnn>_STATUS.md`). Its claims are claims.
3. The project's CLAUDE.md, and its landing and deploy rules, found with `grep -n -i` in its records.

## Do (each step with an instrument and a control that can fail)
1. **Refs.** `git ls-remote` of the branch equals the READY sha. Read main now. Every changed path is inside the lane's OWNS (n of N). Overlap with open PRs and with sibling lanes' OWNS (the other kits of the same sweep) is 0.
2. **Merge.** In YOUR OWN clone under your session scratchpad (push URL set invalid; never pushed): `git merge-tree --write-tree main head`. It must be clean and equal main plus the head blobs.
3. **CI.** Run every CI job whose tests READ the changed files (read `.github/workflows/*.yml` at the head), at main, head and merge, and compare the counts by program. ALWAYS run repo-wide scans that walk tracked files (hidden characters, link checks), whatever paths changed. Anything that needs docker or a database you cannot start is NOT RUN; say that hosted CI is the proof.
4. **Red without the fix.** Every new or changed test fails with the fix removed, run in a copy.
5. **Closed lines.** Re-verify every ALREADY-ON-MAIN or closed-with-evidence line at main, by program.
6. **Probes.** Probe the change adversarially at the boundaries the ticket names. Docs: check every code-fact sentence at source.
7. **Scans.** Underscore-aware name scan `(?<![A-Za-z])<name>(?![a-z])` with a planted `_by_<name>_` control. Ban list: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, plus any list in the kit. Scan added lines and commit messages. Also scan for secrets, tenant or subscription ids, hosts, and Cf characters. **CodeQL pre-scan (added 2026-11-10 after HPSM #304 failed hosted CodeQL on test code the gate passed):** over every ADDED line, test files included, flag `new RegExp(` built from a variable, and any `.replace(/[...]/g, "\\$&")` hand-escape that does not escape the backslash (CodeQL `js/incomplete-sanitization`, high); also `innerHTML`/`dangerouslySetInnerHTML` with a variable and `child_process` with a template string; **Python (added 2026-11-11 after MPS #181 failed hosted CodeQL `py/overly-permissive-file`, 2 high, on test code the gate passed): any `os.chmod`/`os.makedirs(mode=)`/`os.open(..., mode)`/`Path.chmod` whose mode grants group- or world-read or write (`0o755`, `0o644`, `0o777`, `stat.S_IROTH`...), test files included. The query (codeql-cli v2.27.4 `WeakFilePermissions.ql`) flags any integer-literal mode with a group OR world digit, so `0o750`/`0o710` are flagged too. A test that needs a "too-wide" folder creates it under a wide umask with no chmod; a mode rebuilt from `stat` flags only hides the literal and is a Major (a suppression by another name), not a fix.** A hit is a Major (hosted CodeQL will block the merge); list each with file:line.
8. **Claims.** Grade each measured claim in the builder's STATUS: true / false / not shown.
9. **Tier.** Follow S8. If you find a security-shaped issue on a tier-2 lane, write it as a row and end `NO GO: needs tier 1`.

## Severity
- **Blocker:** a path outside the lane, a secret, a name, a red at head or merge that is green at main, any hosted touch, or a deploy a merge would trigger.
- **Major:** a claim your numbers contradict, a vacuous new test, or a merge that is not clean.
- **Minor:** an off pointer or an unshown claim.

## Output
Write ONLY into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_<Bnnnn>_verify/`.
- `VERDICT.md`, whose first line is `GATE <Bnnnn>: GO|GO WITH FINDINGS|NO GO @ <sha7> on main <sha7>`. Then the findings table, then what was NOT RUN.
- On GO or GO WITH FINDINGS, also:
  - `pr-title.txt`
  - `pr-body.txt`, ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
  - `squash-subject.txt` (or `merge-subject.txt` for NexusAI)
  - `squash-body.txt` (or `merge-body.txt`), ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  - `landing.txt` (the head-pinned command)
- All files are plain ASCII except that footer, with no B-numbers, seat ids or names.
- If writing a file is refused, put its content in your final reply.

## Fences
- Never push or write to any origin.
- No PR, no Jira, no mail or board, no `az`, no HTTP to any hosted host.
- Never run `decision_queue.sh list`. Never read `/Volumes/Datasec_DEV/TUESDAY/0_Brain/learnings/_ledger.md`.
- Print no token. No `cd`: use absolute paths and `git -C`.

Final reply: the verdict line and the file list.
