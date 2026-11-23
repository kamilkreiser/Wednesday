STARTABLE: YES

# B1988 DRAFTER REPORT: kit `2026-11-23_B1988_SEAT-X52_oxpd2-x1-round3.md` (OXPd_2 lane X1, round 3, CodeQL at landing)

Drafter: Opus (claude-opus-5-5), in-session, read-only toward the project, Jira and GitHub. Drafted 14:23:31 to 14:54 AEDT (clocks by `date`). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1988/` (below `<d>`). Commission card: `datasec-oxpd-x1-codeql-round3-1123` (default a, "Fix round now", NOT yet ruled by the product owner at drafting; the kit's REFUSE list stops the seat if S4 says the lane was stopped).

## BLUF
1. **One fast-forward commit on `8f5813bf` (HEAD2), two frozen patches, 5 files `M`, nothing in `src/Datasec.Suite.Logging/`, `contracts/oxpd1/` or the slnx.** The record drops `{SettingName}` and `_options.AdminPasswordSetting` (alert 3). `Scrub` uses a new `internal static readonly string Placeholder = "[removed:password]"` in `Oxpd1Soap` instead of `DenyList.ReplacementFor("password")` (alerts 1 and 2). What a reader sees stays byte-equal.
2. **Why it should clear CodeQL (DERIVED, not run).** I read the local `codeql/csharp-all` 7.4.2 `SensitiveActions.qll`. A source is either a variable or property whose name matches `%password%`, or a method call with any constant argument matching `%password%`. Each alert matches one of these. After the fix neither shape reaches the record. `Placeholder` is `static readonly`, not `const`: a `const` access carries its constant value and would make `string.Replace(v, Placeholder, ...)` a source again. K16 and mutant `mPlaceholderConst` pin this. **Whether CodeQL 2.27.5 agrees is UNMEASURED until the seat reads PR 37 after its push.** A remaining flag means the seat STOPS with no second commit.
3. **Gate B1987's three Minors are all fixed in the same commit:**
   - (i) `Holds` now walks every element's and attribute's namespace name and every attribute value (declarations included), unescaped. New K15 has 45 rows: 5 characters x (N1 to N5, plus N6 and N7, namespaces declared above the result) plus 2 controls. N6/N7 are my addition, and mutants `mElementNsOff` and `mAttrNsOff` show they are needed.
   - (ii) The README is narrowed to what `Timeout` bounds. No code bounds the parse; that is a named follow-up.
   - (iii) The false "Not built by the solution yet" bullet is removed.
   - None of the three threatened the CodeQL fix, so none was deferred.
4. **Measured on the prototype** (fresh worktree of a draft clone at HEAD2):
   - Red: 23 / 2 (K15 and K16, each by an assertion). Green: 23 / 0.
   - `MUTANTS: 31 of 31 MATCH, 31 of 31 undone equal`.
   - Whole solution: `total: 1927`, `failed: 0`, `succeeded: 1923`, `skipped: 4`. `RULES: clean (617 files)`. `Ran 111 tests`.
   - The PR merge (`7ad207ef` + patches): `total: 1942`, `RULES: clean (628 files)`.
   - checks3, gitleaks and words are clean, each control fired.
5. **New tools were needed because PR 37 is open, and the kit says so.**
   - Kit B1984's `hosted2.py` now FAILs on HEAD2 with "a job name twice among the check runs" (push run plus pull_request run).
   - `hosted3.py` adds `--event` and the GUARD counts. On HEAD2 it reads push 1925/617 PASS and pull_request 1940/628 with guards 14/15 PASS.
   - `pr37.py` reads the 8 checks, the csharp analysis, the open alerts and alerts 1 to 3. Its control fires on HEAD2: results 3, `FAIL 6`.

## FACTS RE-MEASURED (instrument; control)
- PR 37 (`gh api -X GET pulls/37`, 14:25 and 14:52): open; head `8f5813bf7825d989dac9c6681f930f66196192ef`; base `df762b287a8992a2f33865a5755c4defbcbb2d6b`; `mergeable_state blocked`. Exactly one PR from the branch (#37). `matching-refs/heads/b1976` is one row = HEAD2. `b1988` has 0 rows.
- Check runs of HEAD2: 12 runs under 8 names. `CodeQL` is failure; the other 7 are success (`pr37.py` control run, `<d>/logs/pr37-control.txt`).
- Code scanning on `refs/pull/37/head`: 3 open alerts, all `cs/cleartext-storage-of-sensitive-information` (high), all at `Oxpd1Client.cs:238`:
  - alert 3 at cols 64-93 (`_options.AdminPasswordSetting`)
  - alerts 1 and 2 at cols 95-102 (`request`) and 104-109 (`shown`)
  - Alert texts are in `<d>/logs/alerts-pr37.tsv`.
- csharp analysis 2226572773 at HEAD2 reads results 3 (CodeQL 2.27.5); main `df762b28` reads 0. Each alert's instance on the ref reads `open@8f5813bf`. The top-level alert `state` is empty for these PR-only alerts.
- `compare/cad65b86...df762b28`: ahead 1, 16 files (slnx, root README, Server, Server.Tests), none under the X1 folders. `merge-tree df762b28 HEAD2` gives rc 0 and one line, `7ad207ef`, which equals gate B1987's (B) tree.
- Line pointers at the prototype head, each printed by `grep -n`:
  - `Oxpd1Soap.cs:31` Placeholder; `:180` Holds; `:193` the walk; `:213` AnyIn; `:289` the Replace
  - `Oxpd1Client.cs:237` sink, `:238-239` template and arguments
  - `Oxpd1ClientOptions.cs:59` the doc line
  - `DenyList.cs:53` the replacement
  - `DenyList.ReplacementFor("password")` in `Oxpd1Soap.cs` counts 0 (control: `DenyList.ReplacementFor(` counts 2).
- Toolchain: dotnet `10.0.404`, gitleaks `8.30.1` (`<d>/logs/toolchain.txt`). `.tools/b1988` absent and the wave lock free at 14:53. The pane name `OXPd2-X52` appears in 0 of 49 SEAT kits of 11-22/11-23 (control `OXPd2-X50`: 1).
- Sources by sha256:
  - commission `56e39873f5fbcff368604cacdc9584b0e85bf456b35f374836ae84134481acaf`
  - VERDICT B1987 `9592bb7418746059650315635042a6c48f9f44039762f9904cb7882dfedc2e39`
  - kit B1984 `da486fbd3cbaa1b4e8d693844620f44338d315b8125e3e66e492ffc91a985f7f`
  - DRAFTER_RULES `1c51fc0f10a7a28bcd63af537396e767b8406284fe53c4b9add7f9ab00b25e86`
  - project CLAUDE/CLARIFICATIONS/RUNBOOK as printed in the kit
- `stamp_check.py <kit>`: 124 claims, 124 measured, rc 0.

## STOP-SEVERITY CHECKS ON THE PROTOTYPE
| Check | Result | Control |
|---|---|---|
| REFUSE slot count | 8 on the unstamped kit | fires as intended |
| PRIOR-WORK `git grep` (Placeholder, AnyIn at HEAD2) | rc 1 | `Oxpd1Soap` counts 10 |
| pr37 control on HEAD2 | FAIL 6, CONTROL FIRED | the read itself |
| Red | 23/2 | (none listed) |
| Green | 23/0 | (none listed) |
| Mutants | 31/31 | (none listed) |
| Whole solution | 1927/0/1923/4 | (none listed) |
| Lock files | unchanged | (none listed) |
| unittest | 111 | (none listed) |
| RULES | 617 | (none listed) |
| checks3 | 5 rows M, fenced 0 | A row and Logging row each count 1 |
| ASCII | clean | U+200B counts 1 |
| gitleaks | rc 0 | `leaks found: 1`, quarantined |
| words | clean | 13 of 13 |
| hosted3 push and PR on HEAD2 | PASS | hosted2 FAIL 1; hosted3 PR with default guards FAIL 2 |

**NEVER RUN, marked so in the kit:** the commit, `run_step.py` neutral scan, the push, CodeQL itself, `pr37.py`/`hosted3.py` on a head of this round, any Linux/Windows leg.

## CHAIN INPUTS (each input produced earlier or present at base)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, Stamp slots | Tuesday |
| 1 | `<src>` (12 files), `<repo>` local git values, origin (HEAD2, MAIN, PR 37 + code scanning) | `<d>/seat-tools` (exists), `<repo>`, GitHub |
| 2 | clone at HEAD2, `3-red.diff`, package cache | Step 1, `<project>/.tools/nuget-packages` |
| 3 | `4-fix.diff`, `mutants_x3.py`, red tree built | Step 1, Step 2 |
| 4 | green tree, mutants undone | Step 3 |
| 5 | staged tree, `checks3.py`, `words.py`, message | Step 4, Step 1 |
| 6 | checked tree, `run_step.py` | Step 5, Step 1 |
| 7 | pushed sha, `hosted3.py`, `pr37.py` | Step 6, Step 1 |

## D-DECISIONS (all the coordinator's defaults; in the kit as D1 to D6)
- **D1:** drop the setting from the record and log no flag. **D2:** a `static readonly` `Placeholder` equal to the deny-list text. **D3:** a namespace walk in `Holds`, with N6/N7. **D4:** README narrowing only. **D5:** remove the false bullet. **D6:** one commit and no merge of main. PR 37's own runs build the merge, which was measured at 1942/628.
- **Pacing:** READY = Step 0 + 100 min; push by Step 0 + 50. My mutant run took about 9 minutes at load1 up to 7.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS):** a = one commit with both patches, then pr37; b = Minors as a second commit; c = CodeQL fix only. Default a. S4 must also say whether the card left the lane open.
- **Q2:** drop the setting entirely (default), or log a `SettingConfigured` flag.
- **Q3:** walk in `Holds` with N6/N7 (default), or have `Mask` refuse the declaration (that misses N6/N7).
- **Q4:** pr37's read is this round's CodeQL landing condition; the post-squash main analysis is Tuesday's (default).
- **Q5:** Opus, X52, 100/50, gate G1 round 3, hard stop 18:30 (default).
- **New tools:** accept `hosted3.py`, `pr37.py`, `mutants_x3.py` and `checks3.py` as the seat's tools (they are in the kit's TOOLS table by sha256).

## UNMEASURED
- Whether CodeQL 2.27.5 clears the three alerts, or raises another. My reasoning is from the 7.4.2 qll in the local 2.27.4 bundle; the hosted version may differ.
- What GitHub lists as the instance state of a FIXED PR-only alert. `pr37.py` therefore fails only on `open` instances or on the open list, and decides on the CodeQL check, csharp results 0 and 0 open rows of the rule.
- K16 holds one `DenyList.ReplacementFor("password")` call in test code. Its value flows only into `Assert` calls (no storage sink, DERIVED), but CodeQL's reading of tests is unmeasured.
- K15/K16 on Linux and Windows. Whether `main` moves before the push (the kit handles it: the PR-run numbers come from S2, or `failed: 0` is required).

## OUTSIDE-THE-FENCES DISCLOSURE
- One Bash call contained a `cd` by mistake (a no-op `cd /dev/null`). The `pretooluse_no_cd.sh` hook REFUSED it before anything ran; I re-issued the read without it.
- In my OWN scratch clone I ran `switch --detach`, `worktree add` (seat, seat2, seat3, mg), `read-tree`, `apply`, `add` and `merge-tree --write-tree`. None of this touched the project checkout or any project repo; the push URL is `invalid://no-push`.
- I ran heavy dotnet jobs through `heavy.py` and the wave lock, one at a time. Each job had 0 lock waits; load1 was 1.9 to 7.0. No other lane held the lock while I did. The commission allows this by name.
- I read Tuesday's local CodeQL query pack (`2_Project_Files/tools/codeql/...`); it is not a project file. All GitHub reads were `gh api -X GET` under the OXPd `GH_CONFIG_DIR`. I made no alert action, no comment and no re-run.
- I quarantined the gitleaks control folder and the sidecar draft into `<d>/_quarantine/` and deleted nothing.
- **Trees left:**
  - `<d>/clone` (detached at HEAD2, both patches unstaged)
  - worktrees `<d>/seat` and `<d>/seat2` (earlier iterations)
  - `<d>/seat3` (both patches staged)
  - `<d>/mg` (merge tree + patches staged)
  - none committed
- No process is left running. I wrote only the kit, its `.measured` sidecar and this report under `briefs/` (plus my own scratch).
