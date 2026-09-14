# BUILD REPORT — QA gate set for Secuura/Blockchain PR #874 (KS-926 campaign document), TIER 2, ROUND 1

Drafter: Wednesday-assistant DRAFTING subagent (Sonnet), 2026-09-14 ~18:26–18:37 AEST — the third, small
set in this commission (siblings: `2026-09-14_gate988/` for PR #988, `2026-09-14_gate879/` for PR #879;
this one added mid-commission after Wednesday's follow-up message at 18:14 AEST). Nothing launched,
nothing committed, nothing mailed. The Secuura checkout was touched with READ verbs only (`ls-remote`,
`log`, `show`, `diff`, `diff --numstat`, `ls-tree`, `cat-file`) against the existing read-only checkout at
`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`; no `fetch`/`checkout`/`worktree`/
`merge-tree` anywhere.

## FOUND

- PR #874 (KS-926 campaign document), branch `kamilkreiser/ks-926-checks-that-cannot-fail`, base `develop`
  M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`. Head `b244f4913c948b6d763a6abcf018dac301232345`,
  confirmed as a 5-commit chain directly (`git log --format='%H %P %cI %s'`): the four 09-06 authoring
  commits (`5e83eb28f` → `fe5225f31` → `bea418b02` → `6f7885602`, read from the coordinator's follow-up
  message and independently confirmed reachable) plus a `--no-ff` merge of develop M38. The document is
  BYTE-UNCHANGED by the merge-in — blob `e31f85cda8dfadf1d57f3cc975ad7f219b8966f8` confirmed identical at
  `6f78856` and at the head via `git ls-tree`.
- Diff vs develop M38 = exactly 1 file (`git diff --name-only`, `--numstat`, `ls-tree`, independently
  re-derived): `Blockchain/Dev/docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md`, new, +355. Control row
  `audit-baseline.json` confirmed identical (`03d1680e3…`) at both the head and develop M38 — the
  builder's READY notes the RAW 09-06 head carried a stale blob here that would have refused preflight
  legs 6/7; the merge-in fixed it, and this drafter confirmed the head's OWN blob is develop-matching.
- Read the full document (355 lines) directly via `git show`. Confirmed its opening claim
  ("Opened 2026-09-06 (s141b, seat A) at `develop` `066cff675`") resolves to a real commit
  (`git cat-file -t 066cff675` → `commit`). Spot-checked four load-bearing claims against the current
  tree/cited sources (seed census table in the brief) — explicitly flagged as NOT exhaustive: the document
  names TEN members and this drafting pass verified the document's own EXISTENCE and STRUCTURE, not every
  cited line number for every member. The brief commissions the gate to extend this census to all ten.
- **THE ARCHIVED-TICKET EXCEPTION**, handled as a first-class gate concern per Wednesday's follow-up
  message: KS-926 is Done + ARCHIVED (2026-09-14T02:17:17Z, after PR #918 landed as develop's M22) — an
  archived ticket refuses `commentCreate`. The launcher carries an EXTRA guard (unique to this set, exit
  21) that refuses to launch unless the brief states this exception explicitly — a defence against a gate
  session attempting the write and misreading Linear's "Entity not found" as "ticket does not exist."
- The builder's (s229) Test Evidence and NOT-covered block, plus the correction mail (`corr_874.txt`,
  08:11:47Z — one clause's two commit SHAs were blanked by an unquoted heredoc; the head, evidence, and
  exception are unaffected) — both read and quoted verbatim in the brief.

## TESTED / HOW

- **`--check` against the LIVE current develop tip and the live PR head**, run at close-out (~18:37 AEST):
  **rc 0**. Develop had already moved once during this commission's earlier sets' authoring (M38 →
  `e86bffee0f10809db30b8e0c08994f66ace96232`, 1 commit, 4 files) — the launcher judged this DISJOINT from
  the one PR file and proceeded, printing the move and its judgement. See the final `check.out`.
- **`controls_check.sh`** (`controls_check.out`): fetches the document + the audit-baseline control row at
  both the head and develop via the GitHub contents API, asserts the blob table, seven structural text
  anchors (the title, the campaign statement, the opening line, the headline census claim, the thesis
  quote, two Linear-issue links), a line-count sanity band (350–360, the doc is 355 added lines), a
  secret-shape census (`sk-`, `ghp_`, `-----BEGIN`, all expect 0) with a live markdown-link-syntax control
  (`](`, fires 10 times — proving the grep mechanism is live), and the raw-control-byte census. **First run
  clean, FAILS=0.**
- **`redproof.sh`** (`redproof.out`, work dir kept at `redproof.Fm6eoE/`): **23 cells (0–20, 8b, 21, 22),
  FAILS=0.** Every guard the launcher declares fires at its own distinct exit code
  (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22) plus `0` (green first and green again, pristine
  sha-identical). **This set has ONE extra guard beyond the standard family** (exit 21, the
  archived-ticket-exception statement in the brief) — cell 19 exercises it directly (tampering "KS-926 is
  Done and ARCHIVED" to "KS-926 is Done and closed" trips exit 21). Built directly from the gate879
  template with the DEVELOP_SHA-repin lesson already folded in (M37, one commit back, rather than a
  far-back merge-base that risks the launcher's own `len(files) > 250` UNJUDGEABLE cap) — **no debugging
  was needed this time; both live-data lessons from the two sibling sets were applied up front and the
  first full run was clean.**
- **Raw-control-byte census**: 0 across all five text/script files; the synthetic NUL positive control
  fires at its expected offset (`[16]`).
- **`bash -n`**: clean on the launcher.

## CAVEATS

- This drafter's own census of the document's ten members is EXPLICITLY a seed (4 rows), not exhaustive —
  the brief commissions the gate to extend it to all ten before reaching a verdict. This is the single
  most important scoping decision in this set: a docs-only PR still has real FAIL conditions (a citation
  that never held, a stale-and-uncaveated current claim), and this drafting pass did not have the budget to
  re-verify every line number the document cites against the current tree.
- The head may move if the PR is revised — the `HEAD_SHA` one-line mechanism is the designed remedy;
  `AHEAD_WANT`/`FILES_WANT` must be checked alongside it if the commit/file count changes.
- Live GitHub API calls under rapid repetition can time out transiently (observed once in the gate879
  sibling set's authoring pass) — a lone timeout on re-run is noise; a reproducible one is a finding.

## PINS (re-read live at close-out, ~18:37 AEST)

- Head: `b244f4913c948b6d763a6abcf018dac301232345` (`git ls-remote origin refs/pull/874/head` and the
  branch ref — identical).
- Base (as pinned in the brief/launcher): develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d`.
- Compare: `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=5 files=1` (GitHub compare API, live).
- **DEVELOP MOVED** (observed during this commission) to `e86bffee0f10809db30b8e0c08994f66ace96232` (1
  commit, 4 files) — judged DISJOINT from the one PR file by the launcher's own live `--check`, rc 0.

## `--check` RETURN CODE: **0** (live develop tip — now one commit past M38 — live PR head, no env overrides; the move was judged DISJOINT and re-stated, not silently ignored).

## Deliverables (this dir → install targets)

| file | install target |
|---|---|
| `2026-09-14_secuura-874-ks926-tier2.md` | `fleet/qa-agent/briefs/2026-09-14_secuura-874-ks926-tier2.md` |
| `2026-09-14_secuura-874-ks926-tier2.prompt.txt` | `fleet/qa-agent/briefs/2026-09-14_secuura-874-ks926-tier2.prompt.txt` |
| `launch_qa_secuura_874_ks926.sh` | `fleet/qa-agent/launchers/launch_qa_secuura_874_ks926.sh` |
| `controls_check.sh` (+ `controls_check.out`: FAILS=0) | this set |
| `redproof.sh` (+ `redproof.out`: 23 cells [0–20, 8b, 21, 22], FAILS=0; work dir `redproof.Fm6eoE/`, kept) | this set |
| `model/` — fetched-bytes copies from `controls_check.sh`'s own run | this set |
| `check.out` (final `--check`, rc 0, live develop move observed and judged DISJOINT) | this set |
| `SHA256SUMS.txt` — sha256 of every other top-level file in this set | this set |

**Not installed** — every path above is the eventual install target. The launcher's `BRIEF`/
`PROMPT_FILE`/`REAL_BRIEF` defaults currently point at THIS gateset directory (not the central one), so
`bash launch_qa_secuura_874_ks926.sh --check` passes rc 0 right now, in place, without an install step
first. **Install (when Wednesday is ready):** copy the brief + prompt into `briefs/`, the launcher into
`launchers/`, re-point the three path constants at the top of the launcher to the central `briefs/`
location, re-run `--check` once more to confirm, then:

```
cockpit.sh add "QA/Secuura-874" "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_874_ks926.sh"
```
