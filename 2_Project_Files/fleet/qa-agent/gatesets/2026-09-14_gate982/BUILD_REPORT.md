# BUILD REPORT — QA gate set for Secuura/Blockchain PR #982 (KS-790), TIER 1, ROUND 1 — on `e62eab87a`

Built 2026-09-14 07:08–07:46 AEST by Wednesday's drafting subagent, in the OUTPUT DIR only. Nothing installed, posted, sent or
launched. **No git write verb was run anywhere** (read verbs only in the Secuura checkout: `ls-remote` ×2, `cat-file -t`, `log`,
`merge-base`, `rev-list`, `diff`, `show`, `ls-tree`, `grep`, `rev-parse`, `status --no-optional-locks`, `for-each-ref`;
`rev-parse`/`status` in six worktrees; no `fetch`/`pull`/`push`/`merge`/`worktree`/`checkout`/`reset`/`commit`/`stash`; no `cd` in any
tool call — the one `cd` in the set is the launcher's, written by the generator). **No credential value printed or written:** the
GitHub and Linear helpers source `GH_TOKEN` / `LINEAR_API_KEY` by NAME from the Secuura `.env` in-process; a credential-pattern sweep
over the whole OUTPUT DIR hits **0** files (positive control: the NAME `GH_TOKEN` in 28 files). **No file in this set carries a raw
control byte** (eleven deliverables/instruments censused in red-proof cell "census" with a synthetic NUL positive control at offset 16).
**The suite, any merge, any tamper were NOT run — this is a BUILD**; every runtime number in the brief is the builder's (s212), read from
its records and relayed as a claim to falsify; every tamper prediction is the drafter's, derived from the head bytes (`guards_sim.out`)
and marked `predicted-by: drafter`.

## FOUND

| pin | value | instrument (time AEST) |
|---|---|---|
| head | **`e62eab87a6263e25c41c9bb814d5831842bb6c7e`** at `refs/pull/982/head` AND the branch `feature/ks-790-oauth-authorization_code-token-exchange-uses-getuserbyid` at 07:08:36 and 07:45:10 — unmoved; = s212's READY head | `git ls-remote` ×2 (`lsremote_1.out`, `lsremote_2.out`); `/pulls/982` 07:11 |
| parent / merge-base | **`8861e62161466c40f08d2b10a30edeb203123993`** = M18 = origin develop: `git log -1 --format=%P` AND `/pulls/982/commits` AND `git merge-base` AND the compare API's `merge_base_commit`; `rev-list --left-right --count` = `0 1` | `git_read.out`, `gh_read.out` |
| develop | **M18 `8861e6216`** at 07:08:36, 07:11 (`/branches/develop`), 07:45:10 — unmoved through the whole build; the PR's parent IS develop | `ls-remote` ×2, REST |
| the stack | `refs/pull/983/head` `f62c975c1` (1 ahead of `e62eab87a`; touches the ks790 test file, `oauth.ts`, `jwt.ts`, a new ks823 test); `refs/pull/984/head` `d00a2015c`; `refs/pull/881/head` `8ac9db66f` (independent, `mergeable: blocked`) | `ls-remote`, `/pulls/983`, `/pulls/984`, `/pulls/881`, compare `e62eab87a...f62c975c1` |
| the delta | 3 files A/M/M, +280 −5: `oauth.ts` `4b03f555e` → `80e05458e` (+23 −5, 4 hunks, CODE −4/+3, 20 comment lines); NEW `ks790-token-pre-auth-user-lookup.test.ts` `cfed82d54` (249 lines); `ks820-821-…test.ts` `106c762f1` → `b998b5b7d` (+8 −0, ONE hunk = the mock entry + 4 comment lines; byte-identical elsewhere; 13 cells at both trees) — **ruling 1 verified at the bytes** | `git diff --numstat/--name-status`, the PR files API, `guards_sim.out`, `controls_check.out` |
| blobs / sha256 / lines | `oauth.ts` head `fc54cc5f1494ad48…` 1,260 / develop `cc4f4ac0df1b3393…` 1,242; ks790 `55c12270001fd653…` 249; ks820 head `d0883d41f8a38b96…` 377 / develop `4f66d57fd174c85b…` 369; `userRepo.ts` `822b3fcd8` / `jwt.ts` `d0d55c11b` / `index.ts` `edabbf871` blob-identical at both trees; migration 039 `9778af893` 271 lines | contents API + `git show`, both agree |
| the builder's numbers (relayed) | develop 50/685; red-first `4 failed \| 2 passed (6)`; head 6/6, 19/19, 51/691; T1 1/5, T2 1/5, T3 3/3 — **all three T3 reds are 400 "Invalid refresh token" (the require inside the try), NOT the 500 develop's placement gives** — the brief carries both placements as T3d / T3b | `5_Project_History/2026-09-13_s212/item2/*.out` (`records_read.out`) |
| docker | daemon DOWN at 07:14 ("Cannot connect to the Docker daemon") — the brief's docker rule: read it yourself; never start it; `qa982-*` only | `misc_read.out` |
| worktrees | live at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/` (a SIBLING of `2_Project_Files` — the exemplar's `<checkout>/worktrees/` wording does not hold here; the brief says so); `s212-ks790` ON the branch at `e62eab87a`, porcelain 0, `node_modules` 985, vitest 4.1.10, shared dist present — the farm source | `worktrees_read.out` |
| Linear | KS-790 In Progress High, attachments #982 + #812, 4 comments (`0dc34f52` = the READY record; `c93826d9` = the #972 seat's F-5 copy); the precondition tickets' columns; 27 symbol searches (`getUserByIdPreAuth` → KS-1132/1052(A)/999/943/790; `denylistRefreshJti` → KS-756; `ServiceUnavailableError` → KS-1018; `refresh token replay` / `rotate refresh` / `in-handler require` → 0) | `linear_read.out`, `linear_search.out`, `linear_titles.out` |
| checkout | HEAD `355d82c8b` on `feature/ks-597-b-caller-scoped-externalref`, porcelain 0, `.git/config` `e0fa706f4bdae277…`, 848 refs, 90 `.git/worktrees`, 88 `worktrees/` | `checkout_read.out` |

**Three things the drafter noticed that the builder did not say, written into the brief as Records to MEASURE, not findings against #982:**
(a) the authorization_code grant has NO status pin (`:809` is `if (!user)`; the refresh grant pins `ACTIVE` at `:868`) — pre-existing at develop
`:800`, reachable only now that the lookup works; (b) the refresh grant does not rotate/denylist the presented token (`:836` says "Verify and
rotate"; `/api/auth/refresh` rotates at `auth.ts:697-701`) — KS-823's neighbourhood; (c) the outer catch maps a `ServiceUnavailableError`
(503-class) from either lookup to 500 `server_error` (`:889-891`) — same class at develop. Board searched for each; none has a home by title.

## The deliverables (OUTPUT DIR → install targets)

| file | path (under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate982/`) | sha256 (16) | bytes | install to |
|---|---|---|---|---|
| brief | `2026-09-14_secuura-982-ks790-tier1.md` (RULED section verbatim; §2a table with `predicted-by`; tamper table with `predicted-by: drafter`; NOT COMMISSIONED; NOT TESTED; PROVENANCE with read times) | `c43c8e8eaddc74cb` | 74,887 | `…/fleet/qa-agent/briefs/` |
| prompt | `2026-09-14_secuura-982-ks790-tier1.prompt.txt` (opens `ultrathink`; names the brief path, the #972 report path, the head SHA, TIER 1, ROUND 1, MAIL YOUR VERDICT, the NEVER-push / no-memory / never-print-a-credential lines) | `e5e14dfe918ed452` | 14,205 | same `briefs/` dir |
| launcher | `launch_qa_secuura_ks790_982.sh` (chmod +x; `/bin/bash -n` rc 0 under 3.2.57; exit codes 2..18, 20, **21 = stdin not a TTY on the launch path**) | `f9c978c109e9ae31` | 12,241 | `…/fleet/qa-agent/launchers/` |
| §4 controls | `controls_check.sh` + `controls_check.out` (rc 0, **142 ok, 0 fail, `FAILS=0`**, 07:32) + `controls_check.neg-devashead.out` (head overridden to M18 → rc 1, 57 FAIL lines incl. "t790 ABSENT") + `controls_check.neg-headasdev.out` (develop overridden to the head → rc 1, 29 FAIL lines) | `f42ae2147b2fc5cc` | 15,053 | beside the launcher; **re-run at install** |
| red-proof | `redproof.sh` + `redproof.out` (FINAL 07:40:17–07:44:56, **32 cells ok, 0 FAIL, `FAILS=0`, rc 0**, pristine sha-identical) + `redproof.first-run-21a-slash-in-name.out` (the first run: 30 ok, cell 21a FAIL because the CELL NAME carried `/dev/null` and became a nested path — an instrument bug, renamed; every other cell identical) + work dirs `redproof.1vuyzY/`, `redproof.WuhzUa/` | `e3514509551177f0` | 18,318 | keep beside the set |
| `--check` | `check.out` (no overrides → rc 3 "brief missing" = nothing installed; overrides → rc 0, 12 guard lines; the launch path headless → rc 21) | — | — | — |
| generator | `gen_launcher_982.py` (from the INSTALLED #980 round-2 launcher, sha `200c7dfba7871b06`: 17 asserted substitutions, residual guard 32 tokens, 60 output controls, TTY-guard position asserted; `gen_launcher.out`; `gen_postheader.diff` = 61 lines — only the pins / names / GUARDED list / DEV_NOTE texts / TIER-ROUND strings / the removed exit-19 block / the added exit-21 line differ). **Three refusals on the way (`REFUSING: anchor … occurs 1 times, expected 2`; residual `980`; residual `exit 19`) — each an asserting edit doing its job; the anchors and the header wording were corrected, never the guard.** | `18d72b776ec1bd61` | 14,744 | — |
| instruments | `gh_read.py` + `.out`, `linear_read.py` / `linear_search.py` / `linear_titles.py` + `.out`, `guards_sim.py` + `.out` (88 ok, FAILS=0), `git_read.out`, `checkout_read.out`, `worktrees_read.out`, `misc_read.out`, `records_read.out`, `lsremote_{1,2}.out`, `gh/` (PR JSON, body, the linear[bot] comment, compares, the head commit), `linear/` (13 tickets + KS-790's description and 4 comments), `model/` (the five blobs at the two SHAs via `git show`, the six via the contents API, the diff, migration 039), `SHA256SUMS.txt` | — | — | — |

## TESTED / HOW (with controls)

- **Every §4 positive-control token EXISTS at the head tree with the stated count** — `controls_check.sh` reads the six files at both SHAs through the contents API (blob / bytes / lines / sha256 asserted), 33 exact line reads, 58 token counts (present / absent / exact), the ks820 insertion shape, the `oauth.ts` CODE delta (difflib: exactly 4 changed regions, −4/+3 code, −5/+23 raw), the ks860 `:433`/`:440` regexes over the new test file (offenders `[]`; guard controls 1 / 0), 0 raw control bytes: **142 ok, FAILS=0**. **It can refuse:** head:=develop → 57 FAIL (the new file ABSENT, every head anchor missing); develop:=head → 29 FAIL (the develop anchors missing, the two changed files byte-identical). Same instrument as `guards_sim.py` (88 ok over the `git show` copies) — two reads of the bytes agree.
- **The launcher's guards, each fired once at its own exit code on scratch copies (`redproof.out`):** 0 green (12 guard lines, the develop-still note, the head-SHA line, the TTY line) · 6 wrong head · 18 unknown develop (UNJUDGEABLE) · **18 pinned at M15 — the live M15..M18 delta hits the `services/auth/` PREFIX on the ks949 test, named** · 0 pinned at M17 (the corpus test under `packages/shared/` — NOT guarded — `MOVED … commits=1 files=1 — disjoint`) · 0 pinned at M16 (`commits=2 files=3 — disjoint`) · 0 at M15 with the prefix neutralised (`commits=3 files=6 — disjoint` — the prefix was what fired) · 18 at M15 with slot 2 aimed at the ks949 test (the EXACT arm) · 18 at M17 with the ks860 slot aimed at the corpus test (EXACT arm on a `packages/shared/` file) · 10 merge-base · 13 env file missing · 3 / 4 empty brief / prompt · 2 / 5 dirs missing · 7 ×2 tier · 15 ×2 round · 8 ultrathink · 9 brief path · 12 mail · 11 never-push · 14 no-memory · 17 credential · 20 ×2 head SHA · **21 headless override launch (the TTY guard) · 16 the SAME launch under a pty via `script(1)` (the override guard, one line later — the TTY guard does NOT fire on a terminal) · 16 with the TTY guard neutralised, headless (proves the guard is what stood between a Bash tool and the exec)** · 3 real launch (not installed) · census 0 control bytes with the NUL positive control · 20 distinct exit codes declared · `bash -n` ok · 0 green again, sha-identical. **32 cells, FAILS=0.**
- **`--check` three ways (`check.out`):** rc 3 without overrides (nothing installed — correct), rc 0 with overrides (12 lines), rc 21 on the launch path headless.
- **Provenance:** every pin in the brief was read in the same action as written (the `.out` files carry the timestamps); the template launcher's sha was read at generation (`200c7dfba7871b06` = the exemplar's installed copy).

## NOT DONE (and why)

- The suite was not run, no merge was built, no tamper landed — a build, not a gate; every number is the builder's, labelled.
- Linear was read, never written; GitHub was read, never written; no mail; nothing installed, committed or launched (Wednesday's step).
- The live-039 leg cannot be pre-verified here: the docker daemon is down; the brief carries the docker rule (read it yourself; never start it; `qa982-*`; NOT RUN with the blocker named if down; the stub-modelled leg with the REAL `userRepo` + `jwt` beside it).
- The T3b/T3d distinction (the builder's T3 read 400s, develop's shape reads 500s) is stated from the builder's own `tamper_T3.out` and the develop bytes; the gate measures both.
- `wait_subject.py` does not exist in `fleet/` (the exemplar's BUILD_REPORT named it) — no wait command is given; the verdict mail's subject is the signal (ruling 5).

## Install then

1. Copy the three files: brief + prompt → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/`; the launcher → `…/fleet/qa-agent/launchers/`.
2. `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate982/controls_check.sh` (expect rc 0, `FAILS=0`).
3. **`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks790_982.sh --check`** (expect rc 0 and TWELVE lines — the develop line reads either `origin develop still 8861e6216… (M18 …)` or `MOVED 8861e6216… -> <sha>: commits=N files=M — disjoint from the guard's six paths …`; **both are green**; **exit 18 means a later squash touched #982's files, ANYTHING under `Blockchain/Dev/services/auth/`, the ks860 guard file or migration 039, or the delta was unjudgeable** — then confirm the delta and re-pin `DEVELOP_SHA` in THREE places: launcher, brief TARGET "develop = M18 `8861e6216…`", prompt "origin develop = M18 8861e6216"; exit 20 = the brief or the prompt lacks the full head SHA).
4. Launch via `cockpit.sh add` — **in a pane; the launcher refuses a headless launch with exit 21.**
- Report dir the gate will write: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks790-982-e62eab87a-tier1-r1/` (absent at 07:14 — correct).
- Verdict subject: `[QA -> Wednesday] TIER 1 GATE #982 (KS-790) e62eab87a -- <GO|GO WITH FINDINGS|NO GO>`.
