# BUILD REPORT — QA gate set for Secuura/Blockchain PR #881 (KS-798 / KS-841 / KS-799), TIER 1, ROUND 2 — on `8ac9db66f`

Built 2026-09-14 07:05–07:55 AEST by Wednesday's drafting subagent, in the OUTPUT DIR only. Nothing installed, posted, sent or
launched. **No git write verb was run in the Secuura checkout** (read verbs only: `ls-remote` ×2, `cat-file -t`, `log`, `merge-base`,
`merge-base --is-ancestor`, `rev-list`, `diff`, `show`, `ls-tree`, `grep`, `rev-parse`, `status --no-optional-locks`, `for-each-ref`;
`rev-parse`/`status` in six worktrees; `ls` of `.git/worktrees` and `worktrees/`). The ONE write verb of the build — `git merge-tree
--write-tree` — ran in a `--shared --no-checkout` clone under this set's `model/clone881` (the hook refused it against the checkout
first, with a variable path; re-issued literal into the clone). No `cd` in any tool call (the one `cd` in the set is the launcher's,
written by the generator). No credential value printed or written: the GitHub and Linear helpers source `GH_TOKEN` / `LINEAR_API_KEY`
by NAME from the Secuura `.env` in-process; a credential-pattern sweep over the set hits 0 files (control: the NAME `GH_TOKEN` in 28).
**No file in this set carries a raw control byte** (nine deliverables/instruments censused in the red-proof with a synthetic NUL
positive control at offset 16). **The suite, any tamper, any Express app, jsdom were NOT run — this is a BUILD**; every runtime number
in the brief is the builder's (s212), read from his records and relayed as a claim to falsify; every tamper prediction is the drafter's,
derived from the files at head and from jsdom 29.1.1's source in the builder's worktree (`predicted-by: drafter` on every row).

## The deliverables (set paths → install targets)

| file | path (under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate881r2/`) | sha256 (16) | bytes | install to |
|---|---|---|---|---|
| brief | `2026-09-14_secuura-881-ks798-841-799-tier1-r2.md` | `68fc3d8b016e60fb` | 94,890 | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/` |
| prompt | `2026-09-14_secuura-881-ks798-841-799-tier1-r2.prompt.txt` (opens `ultrathink`, names the brief path AND the two round-1 read files) | `87e7171e0bb6f2e9` | 14,825 | same `briefs/` dir |
| launcher | `launch_qa_secuura_ks798_841_799_881_r2.sh` (chmod +x, `/bin/bash -n` rc 0 under 3.2.57) | `030cbb8add3c1746` | 14,486 | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/` |
| §4 controls | `controls_check.sh` + `controls_check.out` (rc 0, **227 ok, `FAILS=0`**, 07:4x AEST) + `controls_check.neg-r1.out` (head overridden to `787771b97` → rc 2: the new test file is UNREADABLE there — a refusal) + `controls_check.neg-306dev.out` (develop overridden to the round-1 base `306d0db92` → rc 1, **6 FAIL**: gateway `index.ts`/`proxy.ts`/nginx blobs differ) | `e8002ef5a3a119b1` | 24,176 | beside the launcher; re-run at install |
| red-proof | `redproof.sh` + `redproof.out` (FINAL, 07:47:18–07:52:54 AEST, **38 cells, FAILS=0**, every cell LANDED) + `redproof.first-run-cell-names-with-slashes.out` (the first run: two cell NAMES carried a `/`, so their output redirect failed and read rc 1 — an instrument slip, not the launcher's; kept under its honest name) + work dirs `redproof.1g0Xmj/`, `redproof.U8HEDh/` | `3757a0b5afb7ea50` | 20,417 | set only (keep beside) |
| `--check` | `check.out` (no overrides → rc 3 "brief missing" = nothing installed; env overrides → rc 0, 13 guard lines, 07:36 AEST) | — | — | set only |
| generator | `gen_launcher_881r2.py` (from the INSTALLED #980 round-2 launcher, sha `200c7dfba7871b06`: 16 asserted substitutions + ONE asserted insertion (the exit-21 TTY guard, order-asserted `--check` < TTY < override < exec), residual guard of 41 tokens — it REFUSED twice before writing (`877` inside `787771b97`; then a wrong stated count) and wrote nothing each time — 74 output controls; `gen_launcher.out`, `gen_postheader.diff` = 73 lines: only the pins / names / the 15-entry GUARDED list / DEV_NOTE texts / the tier grep / the R1_READ block / the TTY guard differ) | `7b7e5bc40a45fdb6` | 18,099 | set only |
| instruments | `gh_read.py` + `.out`, `linear_read.py` + `.out`, `linear_search.py` + `.out`, `linear_titles.out`, `git_read.out`, `blobs.out`, `anchors_head.out`, `csp_chain_read.out`, `checkout_read.out`, `merge_tree.out`, `diff_oauth_r1_to_fix.patch`, `diff_ks799csrf_r1_to_fix.patch`, `lsremote_{1,2}.out`, `gh/` (PR JSON, body, the three comments, compares, the two commit messages), `linear/` (14 tickets + the named comments), `model/` (the 13 model files at head/r1/develop via `git show`, the API copies, `csrf.ts`, and `clone881/`), `SHA256SUMS.txt` | — | — | set only (`gh/`, `linear/`, `model/`, `redproof.*/` are gitignored) |

**Install then:** copy the three files; `bash <set>/controls_check.sh` (expect rc 0, `FAILS=0`); **`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks798_841_799_881_r2.sh --check`**
(expect rc 0 and THIRTEEN indented lines — the develop line reads either `origin develop still 8861e6216… (M18, …)` or `MOVED 8861e6216… -> <sha>:
commits=N files=M — disjoint from the fifteen guarded paths …`; **both are green**; **exit 18 means a later squash touched a guarded path** — the six
PR files, ANYTHING under `Blockchain/Dev/services/auth/`, the four gateway files (`middleware/csrf.ts`, `specRouteMap.ts`, `index.ts`, `routes/proxy.ts`),
the nginx conf, the spec, anything under `packages/shared/src/__tests__/`, or the root lockfile — or the delta was unjudgeable; then confirm the delta
and re-pin `DEVELOP_SHA` in THREE places: launcher, brief TARGET "develop = M18 `8861e6216…`", prompt "develop = M18 8861e6216"; exit 19 = the round-1
READ (Peter's comment on disk + the review id `5140256072`) not named in the brief / not on disk; exit 20 = the brief or the prompt lacks the full head
SHA; **exit 21 = a real launch with stdin not a TTY — launch via `cockpit.sh add`, never inside a Bash tool; `--check` is exempt**).
Report dir the gate will write: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks798-841-799-881-8ac9db66f-tier1-r2/` (absent at 07:53 — correct).
Verdict subject: `[QA -> Wednesday] TIER 1 GATE #881 ROUND 2 (KS-798 KS-841 KS-799) 8ac9db66f -- <GO|GO WITH FINDINGS|NO GO>`.
Verdict wait: the MAIL (ruling 5 — no `mail-subject.txt`); `wait_subject.py "TIER 1 GATE #881 ROUND 2"` if that is Wednesday's instrument.

**Template:** the INSTALLED #980 round-2 launcher (sha `200c7dfba7871b06`) — the newest carrying the disjointness-checked develop pin, the exit-19
round-1 guard and the exit-20 head-SHA-in-both guard; same guards/exit codes 2..20 re-pointed, **plus exit 21 (TTY)** — the first launcher in
`launchers/` to carry it (0 of the 40 tracked launchers grep `-t 0`/`tty`; the 2026-09-13 ledger names the guard as a candidate). The tier-1 exemplars
(`launch_qa_secuura_ks950_962_973_r2.sh`, `launch_qa_secuura_ks1004_912.sh`) were read for their tier-1 header framing (what the change REACHES).

## Round 1: NO QA report exists for #881 — the round-1 read is Peter's review

`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/` (124 dirs) searched for `pull/881` → 0, `PR #881` → 0, `787771b97` → only other
gates' `refs-*.txt` dumps, `ks-798` → refs dumps + the s125–s128 KS-781/797 reports naming it as a neighbour; control `pull/980` → 3 files. The one dir
named `ks881` is ticket KS-881 (PR #860). **So the exit-19 guard pins the round-1 READ instead of a report:** Peter's comment 5583115315 on disk at
`5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.md` (11,080 chars, byte-identical to the API body — checked in `controls_check.sh`
and by hand) plus his review id 5140256072 named in the brief. The brief's PRIOR ROUND block says so; every leg is written as a first pass of the tier-1
class (no delta re-read), with KS-798/KS-841/KS-781-n1 as Peter-signed-off CONTROLS.

## Pins (read 07:10:02 AEST at start, 07:15 by REST, 07:53:20 at close)

| pin | value | instrument |
|---|---|---|
| head | `8ac9db66f6fd0d751f74ecc95bb314210a31ec52` at the branch AND `refs/pull/881/head` at both reads (= the READY's head — no STOP) | `git ls-remote origin` 07:10:02, 07:53:20; `/pulls/881` 07:15 |
| the commits | `787771b97` (Peter's head) → **`ffcea35cb`** (parent `787771b97`, tree `12dd42b2e`, 13:26:39Z, ids KS-799 only, `#881` once, 1 at-sign = Co-Authored-By, 4,160 chars / 62 lines) → **`8ac9db66f`** (parents `ffcea35cb` + `8861e6216`, tree **`136e6c8cc`**, 13:32:33Z, 55 chars, 0 ids) | `git log -3`, `/pulls/881/commits`, `/commits/{sha}` |
| merge-base | **`8861e6216` = develop M18 itself** (`git merge-base`; `--is-ancestor` rc 0; `rev-list --left-right --count` = `0 5`; GitHub compare `develop...head` `ahead` 5 / 0, 6 files) | git + REST |
| develop | **M18 `8861e62161466c40f08d2b10a30edeb203123993`** at 07:10, 07:15 (`/branches/develop`; compare `M18...develop` `identical`), 07:53 — **unmoved through the build** | `ls-remote` ×2; REST |
| the merge | `git merge-tree --write-tree 8861e6216 ffcea35cb` = `136e6c8ccce47c0787d71398dd41010298ac8e17` = `8ac9db66f^{tree}` EXACTLY; control with `787771b97` → `b78c33c39…` (different) | the `--shared` clone under `model/clone881` (`merge_tree.out`; re-asserted in `controls_check.sh`) |
| launcher pins | `HEAD_SHA`, `MERGE_BASE='8861e6216…'` (exit 10), `DEVELOP_SHA='8861e6216…'` (exit 18, disjointness-checked over 15 guarded paths), `R1_READ` + `5140256072` (exit 19), head-SHA-in-both (exit 20), TTY (exit 21) | `--check` rc 0 |

## The delta, verified

`git diff --numstat 787771b97 ffcea35cb` = `21 10` csrf-submit test · `414 0` the NEW csp test · `105 57` `oauth.ts` (the GitHub compare `787771b97...ffcea35cb`
says the same: `ahead` 1 commit, 3 files). `git diff --name-status 8861e6216 8ac9db66f` = the SIX PR files (`/pulls/881/files` = compare `develop...head` = the same
six: `ks781-n1` M +14 −21 · `ks798` A +201 · `ks799-consent-form-csrf-submit` A +164 · `ks799-consent-script-csp-and-execution` A +414 · `ks841` A +152 · `oauth.ts` M
+150 −3). `git diff --numstat ffcea35cb 8ac9db66f | wc -l` = 448 = develop's own side of the merge — named in the brief so it is never read as the PR's. **Blobs:**
`oauth.ts` `01c2d320f` (r1; 1,341 lines, 66,571 B, sha256 `4416d681c5d5eefb`) → **`ffb573842`** (fix = head; 1,389 lines, 69,496 B, `11669c67e982213a`); develop's
`4b03f555e`; the csp test **`995ee34ce`** (414 lines, 22,640 B, `75fd750616f520f9`; ABSENT at r1 and at M18); the csrf-submit test `08803feb2` → **`a83594c38`** (164
lines, `da8490dbdc8f1666`); **`ks798` `d5143dc3f`, `ks841` `380ea51a4`, `ks781-n1` `5e390443f` identical at r1, fix and head** (develop's `ks781-n1` is `5d5d490eb`,
320 lines — round 1's flip). The four gateway files, auth `index.ts`, the nginx conf and the spec are blob-identical at head and M18 (`blobs.out`; `csrf.ts`
`1f16e2f89`). **The moved bytes:** r1's inline body (`:1286-1333`, 48 lines) == head's `CONSENT_SUBMIT_SCRIPT` body (`:561-608`, 48 lines) with leading whitespace
normalised (`controls_check.sh`, with a one-token control that makes them differ). The page template literal (`:1270-1384` at head) carries exactly ONE live
`<script>` element, `src="/api/oauth/consent.js"`, empty body; r1's carries exactly one INLINE element (2,195-char body). 0 raw control bytes in the six.

## What the predictions rest on (drafter's reads — `predicted-by: drafter` on every row)

The two KS-799 test files read WHOLE at head (every cell's assertion line cited in the brief's TARGET); jsdom 29.1.1 read in the builder's worktree's
`node_modules/jsdom/lib/jsdom/living/nodes/`: `HTMLScriptElement-impl.js:83` reads the script response's `content-type` for charset ONLY (→ **Tg-A reds C2
alone**); `:143-148` `_eval` returns without fetching when the `type` attribute is not a JS MIME string (→ **Tg-B reds C4 + the four C3 rows + the text cell, C1/C2
green**); `HTMLFormElement-impl.js:118-131` `requestSubmit` fires `submit` and, if not cancelled, `notImplementedMethod(window, "HTMLFormElement", "requestSubmit")`
(→ **Tg-C reds C3 happy via the `:363` `/HTMLFormElement/` filter, plus C2 and the text cell**); `window/navigation.js:79` "navigation to another Document" (the
C3 cross-origin row). The builder's T1/T2/T3 predictions (3/3/2) were re-derived from the assertions and AGREE with his `tamper_T{1,2,3}.out`. The CSP chain
re-read at head: auth `index.ts:68` `helmet()`, gateway `index.ts:253-270` (KS-245 block), `:387-390` (CSRF mounted only when `NODE_ENV !== 'test'` — the brief
tells the gate to mount `createCsrfMiddleware` itself), `:1044-1090` (the spec gate falls through on unmatched paths), `proxy.ts:369` (no gateway auth on
`/api/oauth`), `csrf.ts` (protected methods, `validateOrigin`'s non-prod leniency at `:245`, the four 403 codes), `nginx-production.conf:281` + `:347` (server-level
CSP inherited by `/api/`; `style-src-elem 'self'` → the inline `<style>` Record), the spec's `/api/oauth/authorize` GET `security: []` and no `consent.js`.

## Red-proof (`redproof.out`, FINAL 07:47:18–07:52:54 AEST on the final set bytes; work dir `redproof.U8HEDh/`)

**38 cells, FAILS=0, every cell LANDED.** Green first (cell 0: rc 0, "all guards pass", exactly 13 guard lines, the develop note `still 8861e6216… (M18 …)`, the
round-1 read line, the head-SHA line, the TIER 1 / ROUND 2 line, the TTY note); one red per guard at a DISTINCT code — 6 · 18 (×6 arms: unknown SHA UNJUDGEABLE;
the round-1 base `306d0db92` UNJUDGEABLE `files=300` (the API's cap; >250); M17 pin → GUARDED `entrypoint-corpus.test.ts` (the packages/shared tests PREFIX arm);
M15 pin with that prefix neutralised → GUARDED `ks949-platform-admin-seed-identity.test.ts` (the **services/auth/ PREFIX arm** — the one that guards the 703 ratio);
M17 pin, prefix neutralised, the `oauth.ts` slot aimed at `entrypoint-corpus.test.ts` → the EXACT arm) and the two DISJOINT passes (M17 pin prefix-neutralised →
rc 0 `MOVED … commits=1 files=1 — disjoint from the fifteen guarded paths`; M15 pin both prefixes neutralised → rc 0 `commits=3 files=6 — disjoint`) · 10 · 13 ·
3 · 4 · 2 · 5 · 7 (×2) · 15 (×2) · 8 · 9 · 12 · 11 · 14 · 17 · 20 (×2 arms) · 19 (×3 arms: path renamed in the brief; review id removed from the brief; file named
but missing on disk) · **21 (override launch HEADLESS — the message `stdin is not a TTY`) · 16 (the same launch under `script(1)`'s pty — the override guard, i.e.
the TTY guard PASSED with a pty and sits before 16)** · 3 (real launch, not installed) · the control-byte census (9 files, 0; synthetic NUL at 16) · 21 distinct exit
codes declared · `/bin/bash -n` ok · green again on the sha-identical set (launcher `030cbb8add3c1746`, brief `68fc3d8b016e60fb`, prompt `87e7171e0bb6f2e9`).
Every cell under `env -i` with a PATH lacking `claude` (asserted), `GH_TOKEN` unset, a 120 s alarm, stdin `/dev/null` (so "headless" is real).

## TESTED / HOW (with controls) — what THIS build measured

- **Read verbs only in the checkout** — the hook refused the one `merge-tree` aimed at it (variable path); the clone under `model/` took it. Checkout porcelain 0 at start and close; refs 848 → 848; `.git/worktrees` 90 → 93 (s214/s216/s217 registered worktrees during the build — other seats'; a `--shared --no-checkout` clone registers none); `worktrees/s212-ks799-r2` porcelain 0 at both reads, `oauth.ts` sha `11669c67e982213a`.
- **controls_check.sh**: 227 ok / 0 FAIL — 28 contents-API reads at four SHAs (blobs, sizes, lines, sha256), 4 ABSENT reads, 12 blob-equality pairs, 3 must-DIFFER pairs, 10 sha256, 11 line counts, 5 byte counts, 72 `lineis` exact-line pins across 8 files, 67 `chk` token counts (present / absent / exact), the moved-bytes diff with its control, the one-live-tag parse at both heads, the merge-tree equality with its control, merge-base = M18, the six-file name-status, the three-file numstat, the round-1 read == API body, 0 control bytes ×6. **Two negative controls refuse** (rc 2 on the r1 head; rc 1 with 6 FAIL on the round-1 base as develop). Five instrument slips were found by the first run and corrected (three guessed counts; the tag parser run over the TS source instead of the template literal — fixed to slice `:1270-1384`); the world did not move.
- **gen_launcher_881r2.py**: 16 asserted substitutions + 1 asserted insertion; the residual guard refused twice before the first write (`877` ⊂ `787771b97` — token tightened to `ks877`/`KS-877`; then a stated-count mismatch — counts re-derived from the rendered text, not guessed); 74 output controls; guard-order assertion.
- **`--check`**: rc 3 with no overrides (nothing installed), rc 0 with overrides — 13 lines (`check.out`); re-run as red-proof cell 0 on the final bytes.

## NOT DONE (deliberately, or could not)

- **No suite, tamper, Express app, jsdom, tsc, eslint, audit run** — a build, not a gate. The 4/8 · 12/12 · 24/24 · 613 · 703 · 3/3/2 figures are the builder's (`item1/*.out`, read and quoted); the gate re-derives them.
- **The cross-package import of `csrf.ts` under auth's vitest was NOT tried** — the brief says so twice and gives the gate a NOT-RUN path (never a copy). The jsdom behaviours behind Tg-A/B/C were READ from 29.1.1's source, not run — the brief names both as "the two places most likely wrong".
- **Linear was read, not written**; the board searches (19 symbols) are relayed to the gate as Wednesday's; the four Records the brief pre-names are unfiled candidates (`consent.js` 0 · `validateOrigin` 0 · `CSRF_ORIGIN_INVALID` 0 · `style-src-elem` only KS-40(A) · `CORS_ORIGINS` only the unrelated KS-1096).
- **No mail, no launch, no install, no write outside the OUTPUT DIR** (the scratchpad holds nothing of this set; the clone lives under `model/`, gitignored).
- **Peter's re-review** is his; the brief tells the gate not to request it.
- The `.git/worktrees` growth 90 → 93 during the build is other seats' and was not investigated beyond naming the three entries.
