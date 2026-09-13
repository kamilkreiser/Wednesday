# BUILD REPORT — QA gate set for Secuura/Blockchain PR #983 (KS-823), TIER 1, ROUND 1 — a STACKED PR on #982, head `f62c975c1`

Built 2026-09-14 07:08–08:13 AEST by Wednesday's drafting subagent, in the OUTPUT DIR only
(`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate983/`). Nothing installed, posted, sent
or launched. **No git write verb was run anywhere** (read verbs only in the Secuura checkout: `ls-remote` ×2, `cat-file -t`,
`log`, `merge-base`, `merge-base --is-ancestor`, `rev-list`, `rev-parse`, `diff`, `show`, `ls-tree`, `grep`, `status
--no-optional-locks`, `for-each-ref`; `rev-parse` / `status --porcelain` in the four s212 worktrees; **no `fetch` / `pull` /
`push` / `merge` / `worktree` / `checkout` / `reset` / `commit` / `stash` / `clone`** — every file the set needed was read by
`git show <sha>:<path>` into `model/` or through the GitHub contents API; no `cd` in any tool call — the one `cd` in the set is
the launcher's, written by the generator). **No credential value printed or written**: the GitHub and Linear helpers source
`GH_TOKEN` / `LINEAR_API_KEY` by NAME from the Secuura `.env` in-process; a credential-pattern sweep over every top-level file
in the OUTPUT DIR hits 0 (positive control: the NAME `GH_TOKEN` in 4 files); the eight `eyJ…` prefixes the builder's vitest
assertion messages carry (tokens signed by the per-process TEST keypair, truncated) were REDACTED in my own read-out
`s212_records_read.out` (16 segments on 8 lines → `eyJ<test-keypair-JWT-redacted-by-drafter>`). **No file in this set carries a
raw control byte** (eight deliverables/instruments censused in the red-proof with a synthetic NUL positive control at offset
16). **The suite, any merge, any tamper were NOT run — this is a BUILD**; every runtime number in the brief is the builder's
(s212), read from its records and relayed as a claim to falsify; every prediction for the gate-designed rows is the
DRAFTER's from the head bytes (`predicted-by: drafter` on every §2a row and every tamper row) — Wednesday marks the ones it
re-derives.

## Two disclosures (not skipped)

1. **One `rm -f` ran, on my own zero-byte scratch artefacts.** The first `git show` loop into `model/` used
   `> file || rm -f file` as its fallback; the redirect created three EMPTY files for paths that do not exist at the ref
   (`ks790-…test.ts` at develop, `ks823-…test.ts` at develop and at the parent) and the fallback removed them. Nothing of
   anyone else's was touched; nothing non-empty was removed; no other `rm` in the build. Recorded because the standing line
   is "never delete", and a disclosed deviation is cheaper than a discovered one.
2. **The first `gh_read.py` run wrote the two `oauth.ts` files (routes/ and services/) to ONE colliding name** —
   `model/api.oauth.ts.<ref>` ended up holding `services/oauth.ts`. Fixed (path-derived names `api.routes_oauth.ts.*` /
   `api.services_oauth.ts.*`) and re-run; the four stale `api.oauth.ts.*` files are left in `model/` (gitignored, superseded,
   not deleted). The git-show copies (`model/oauth.ts.<ref>` = routes; `model/services_oauth.ts.f62c975c1`) are what the
   brief was written from.

## The deliverables (OUTPUT DIR → install targets)

| file | sha256 (16) | bytes | install to |
|---|---|---|---|
| brief `2026-09-14_secuura-983-ks823-tier1.md` | `10d6e4bfd39731b0` | 89,746 | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/` |
| prompt `2026-09-14_secuura-983-ks823-tier1.prompt.txt` (opens `ultrathink`, names the brief path, the head SHA, the MAIL line) | `54c3c4bd6bde71dc` | 17,018 | same `briefs/` dir |
| launcher `launch_qa_secuura_ks823_983.sh` (chmod +x; `/bin/bash -n` rc 0 under 3.2.57) | `42d74bf444f54e33` | 13,276 | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/` |
| §4 controls `controls_check.sh` + `controls_check.out` (rc 0, **213 ok / FAILS=0**, 07:24:55 AEST) + `controls_check.neg-parent-as-head.out` (rc 1, 95 FAIL) + `controls_check.neg-984-as-head.out` (rc 1, 44 FAIL) + `controls_check.neg-parent-as-develop.out` (rc 1, 15 FAIL) | `e2d59f2b169bd3a1` | 25,870 | beside the launcher; re-run at install |
| red-proof `redproof.sh` + `redproof.out` (FINAL, 08:08:36–08:12:52 on the final brief bytes, **32 cells ok / FAILS=0**) + `redproof.pre-brief-harness-range.out` (07:58:32–08:05:00, FAILS=0 on the brief before a one-range line-number correction in TARGET) + `redproof.pre-brief-worktree-line.out` (07:50:19–07:57:50, FAILS=0 on the brief before its worktree-drift line) + `redproof.first-run-22b-grep-miss.out` (07:44:37–07:49:48, FAILS=1 — every cell's rc correct; cell 22b's POST-CHECK grep looked for "command not found" where bash 3.2's exec says `exec: claude: not found`; the grep widened, not the cell) + work dirs `redproof.l1c7mJ/`, `redproof.Alegjd/`, `redproof.6rUAG3/`, `redproof.dFz12p/` | `a1a0ca40de14b0cd` | 19,222 | OUTPUT DIR only (keep beside the set) |
| `--check` `check.out` (07:41:29: no overrides → rc 3 "brief missing" = nothing installed; scratch overrides → rc 0, 12 guard lines; overrides + no TTY → rc 16, the override refusal fires before the TTY guard — by design) | — | 1,446 | OUTPUT DIR only |
| generator `gen_launcher_983.py` (from the INSTALLED #980 round-2 launcher `launchers/launch_qa_secuura_ks924_901_980_r2.sh`, sha `200c7dfba7871b06…` = its scratch copy, cmp IDENTICAL: the header replaced whole, 16 asserted substitutions, 1 asserted removal (the round-2 exit-19 report guard), 2 asserted insertions (the stack-parent guard exit 21; the no-TTY guard exit 22), residual guard of 49 tokens, 63 output controls; `gen_launcher.out`; `gen_postheader.diff` = the body diff vs the template, 82 lines, only the pins / names / GUARDED list / DEV_NOTE texts / the parent + TTY guards / the removed R1 block differ) + `launch_qa_secuura_ks823_983.sh.candidate` (the pre-control dump used to count tokens; byte-identical to the deliverable) | `bd00ec7a59b08cc1` | 17,918 | OUTPUT DIR only |
| instruments | `gh_read.py` (`62586a1b917ec233`) + `.out`, `linear_read.py` (`95a427290725ed37`) + `.out`, `linear_neighbours.out`, `devpins_probe.out`, `git_read.out`, `git_read2.out`, `checkout_read.out`, `s212_records_read.out` (redacted), `lsremote_1.out` / `lsremote_2.out`, `gh/` (PR JSON ×3, bodies, comments, compares ×4, the commit message), `linear/` (20 tickets + the named comments + descriptions), `model/` (the lane's files at develop / parent / head / #984 by `git show` and by the contents API; the 558-line delta diff), `SHA256SUMS.txt` | — | — | OUTPUT DIR only (`gh/`, `linear/`, `model/`, `redproof.*/` gitignored by `gatesets/.gitignore`) |

**Install then:** copy the three files; `bash <launchers>/controls_check.sh` (expect rc 0, `FAILS=0`, 213 ok);
`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks823_983.sh --check`
(expect rc 0 and TWELVE guard lines — the develop line reads either `origin develop still 8861e6216… (M18 …)` or `MOVED
8861e6216… -> <sha>: commits=N files=M — disjoint from the guard's five paths …`; both are green; **exit 18 means a later
squash touched anything under `Blockchain/Dev/services/auth/`, the ks860 loopback guard file, the api-gateway auth/scopes
middleware or the root lockfile — #982's OWN squash is the expected first mover (routes/oauth.ts) and means: re-pin
`DEVELOP_SHA` in THREE places (launcher, brief TARGET "develop = M18 `8861e6216…`", prompt "origin develop = M18 8861e6216")
and the brief's item 2 becomes a real three-way merge; exit 21 = `refs/pull/982/head` moved (a fix round on the parent —
rewrite); exit 20 = the brief or the prompt lacks the full head SHA; exit 22 = launched without a TTY — launch via
`cockpit.sh add`, never inside a Bash tool**).
Report dir the gate will write: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks823-983-f62c975c1-tier1-r1/` (absent at 07:14 — correct; 0 entries naming 983).
Verdict subject: `[QA -> Wednesday] TIER 1 GATE #983 ROUND 1 (KS-823) f62c975c1 -- <GO|GO WITH FINDINGS|NO GO>` — the mail is the wait signal (no `mail-subject.txt`).

## Pins (read 07:08:53 AEST at start, 07:58:05 at close — every one UNMOVED)

| pin | value | instrument |
|---|---|---|
| head | `f62c975c11ec97cdef04500fd98a43618e702763` at the branch `feature/ks-823-security-the-apioauthtoken-refresh_token-grant-authenticates` AND `refs/pull/983/head`, both reads | `git ls-remote origin` 07:08:53, 07:58:05 |
| stack parent | `e62eab87a6263e25c41c9bb814d5831842bb6c7e` = `refs/pull/982/head` = the ks-790 branch, both reads; = `git log -1 --format=%P f62c975c1`; = `/pulls/983/commits[0]` | ls-remote; log; REST |
| merge-base | `8861e6216` (M18) for the head AND for the parent; GitHub compare `develop...f62c975c1` `ahead` 2 / behind 0 / 5 files; `rev-list --left-right --count` = `0 2`; `merge-base --is-ancestor 8861e6216 f62c975c1` rc 0 → the merge onto M18 is a FAST-FORWARD (merged tree == head tree `db10aea98`) | `git merge-base` ×2; compare 07:12 |
| develop | **M18 `8861e62161466c40f08d2b10a30edeb203123993`** at 07:08:53, 07:12 (`/branches/develop`), 07:58:05 — unmoved through the build | ls-remote ×2; REST |
| #984 (stacked on this head, NOT this gate's) | `d00a2015c` at `refs/pull/984/head`; compare `f62c975c1...d00a2015c` ahead 1 / 6 files (touches oauth.ts, jwt.ts, the ks823 test +1 line) | ls-remote; REST |
| launcher pins | `HEAD_SHA` (exit 6), `STACK_PARENT` + `STACK_PARENT_REF='refs/pull/982/head'` (exit 21), `MERGE_BASE='8861e6216…'` (exit 10 via the compare API), `DEVELOP_SHA='8861e6216…'` (exit 18, disjointness-checked over five guarded paths), head-SHA-in-both (exit 20), no-TTY (exit 22) | `--check` rc 0; red-proof |

## The delta, verified (the tasking's "4 files +395 −22")

`git diff --numstat e62eab87a f62c975c1` = `6 2` ks790 / `276 0` ks823 / `82 10` routes/oauth.ts / `31 10` services/jwt.ts;
`--name-status` = M / A / M / M; the PR files API (5 files, the stack) and `/commits/f62c975c1` (4 files +395 −22) agree.
Blobs: routes/oauth.ts `4b03f555e` (develop, 1,242 lines) → `80e05458e` (parent, 1,260) → **`de00ffcea` (head, 1,332; sha256
`70c634fdad581d01`)**; jwt.ts `d0d55c11b` (develop AND parent — #982 does not touch it) → **`62b6db272` (head; `bad7e362c6ca68cb`)**;
ks823 test **`2c0135b6f` NEW (276 lines; `b4fc5dde6a66d4ad`)**; ks790 test `cfed82d54` (parent) → **`f98e8c806`** (head; +6 −2 in two
hunks; the 17 `expect(` lines byte-identical); ks820-821 `106c762f1` (develop) → `b998b5b7d` (parent AND head — #982's +8 hunk,
ruled ACCEPTED, untouched by #983). `types/index.ts` `9b0b4f08a`, `routes/auth.ts` `132d3b8d3`, `services/oauth.ts` `e9953d376`,
`userRepo.ts` `822b3fcd8`, `routes/wallet.ts` — blob-identical head ↔ develop. `packages/shared`: 0 files in `8861e6216..f62c975c1`
(control: `services/auth` 5); lockfiles 0. Test files under `services/auth/src/__tests__/`: 50 / 51 / 52 at develop / parent / head.
The commit message: 4,711 chars / 70 lines, KS ids KS-823 only, PR refs #825 #831, 1 at-sign = the Co-Authored-By e-mail;
the amend `1a26eb795` → `f62c975c1` (in the object store; not tree-compared by me — the brief tells the gate to check
`rev-parse 1a26eb795^{tree}` = `db10aea98`). PR body 5,953 chars, 0 at-signs, KS-823 only, refs #825 #831 #982.

## What the drafter read in the head bytes that the builder's evidence does not cover (the brief's gate-designed rows)

- **The refresh branch's ORDER** (identify `:879` < app `:883` < secret `:889` < verify token `:910` < denylist `:919` < binding
  `:931` < user `:938` < mint `:948`) — asserted from the source by `controls_check.sh` sim (2); no shipped cell pins the order
  → the brief's T7 (the block moved after the verification) + Tg-ORDER-1/-2 cells.
- **Two refusal mechanisms cover the deactivated CONFIDENTIAL app**: the null-app guard `:884-886` AND `verifyClientSecret`'s
  row-less `false` (`services/oauth.ts:161`) → the builder's `dead-1` cell is over-determined; the builder's T4 deleted the
  guard and reddened on a **500** (`tamper_T4.out`: `expected 500 to be 401` — a crash red). The cell that EARNS the guard is a
  deactivated / unknown PUBLIC client → the brief's T4' (non-crashing neutralisation) + Tg-DEADPUB / Tg-UNKNOWN (predicted
  401 at head, 200 WITH A TOKEN under T4') — a coverage gap to report as a described regression test (Minor).
- **The two BINDING cells share status + message** (`400 invalid_grant`; only the description differs, unread) → under T5
  (the refresh-half claim removed from jwt.ts) the wrong-client cell stays green for the fail-closed reason — a Record.
- **`readClientId` body-wins / `readClientSecret` Basic-first-when-the-userid-matches** (`:699-700`, `:723`) → Tg-MIX (401),
  Tg-MIX2 (Basic wins over a correct body secret → 401, a boundary), Tg-EMPTY / Tg-ARRAY (400) — all re-derived in Python by
  the controls sim (4) from the head semantics.
- **The service mounts `express.urlencoded` (`index.ts:86`) and `/api/oauth/token` is the ONE path in the gateway's
  `FORM_ALLOWED_PATHS` (KS-836)** — the shipped harness is JSON-only → Tg-FORM.
- **No `denylistRefreshJti(` on the OAuth path** (head AND develop) → Tg-REUSE (200, 200 — pre-existing, KS-756's family).
- **HUNT THE CLASS: the sibling `POST /api/auth/refresh` (`routes/auth.ts:658-699`, blob-identical head ↔ develop)** accepts any
  valid refresh token (cookie or body) with NO client, `getSession(payload.sessionId)` resolves the OAuth grant's real session,
  and re-mints with TWO arguments (`:689`) → an OAuth-BOUND token launders into an UNBOUND pair. Predicted READ ONLY; the brief's
  item 6 measures it with a develop control and states BOTH readings (pre-existing class exposure for a ticket — nearest
  KS-756 (Backlog High), whose scope item 2 drops `verifyRefreshToken` from that route; and: after #983 the binding can be
  stripped by one round-trip). Disposition Wednesday's; the drafter's reading: not a NO GO on `f62c975c1`.
- **The access half now carries `client_id`** — 0 readers in the gateway middleware (`client_id` / `clientId` 0; control
  `authMethod` 3); exactly ONE reader in `services/` (`oauth.ts:931`); no strict claim parser (`JwtPayload` in 3 auth files only).
- **The ks790 hunk is REQUIRED by the fix**: the builder's own `green_auth_all.out` (first full run) reads `3 failed | 699
  passed (702)` with `client_id is required` — the parent's ks790 bytes against the head product → the brief's item 2(e) pair.

## Red-proof (`redproof.out`, FINAL run 08:08:36–08:12:52 AEST on the final brief bytes; work dir `redproof.dFz12p/`)

**32 cells, FAILS=0, every cell LANDED.** Green asserted first (cell 0: rc 0, "all guards pass", exactly 12 guard lines, the
develop note `origin develop still 8861e6216… (M18 …)`, the stack-parent line, the head-SHA line); one red per guard at a
DISTINCT exit code — **every code 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 20 21 22 exercised, plus the 127 pass-through**
(the launcher declares exactly those plus 0; 19 is deliberately absent — round 1); green re-asserted last on the sha-identical
pristine set (cell 25: launcher `42d74bf444f54e33`, brief `10d6e4bfd39731b0`, prompt `54c3c4bd6bde71dc`). **The develop
guard's arms on the LIVE deltas to M18 (`devpins_probe.out`):** 2 unknown sha → `UNJUDGEABLE` → 18; **2b pinned to M15 with
the SHIPPED list → `GUARDED …ks949-platform-admin-seed-identity.test.ts` (the ONE services/auth file in M15..M18) → 18** (the
PREFIX arm on a real squash); **2c M15 with the prefix neutralised → `MOVED 1c38077ba -> 8861e6216: commits=3 files=6 —
disjoint from the guard's five paths` → 0** (the "moved by a non-guarded squash" arm, on the real delta); **2d M12 with the
prefix neutralised → `GUARDED …ks860-test-listeners-bind-loopback.test.ts` ALONE → 18** (the EXACT arm on the widened guard,
isolated); 2e M12 with the prefix AND the ks860 entry neutralised → `commits=6 files=9 — disjoint` → 0 (the control that the
ks860 entry alone made 2d red); 2f M15, prefix neutralised, the api-gateway `auth.ts` slot AIMED at `startup-migrations.ts` (in
the delta) → 18 (the exact arm works for another slot). **21** the stack parent tampered to a zero SHA → 21 with the reason
line. **22** a launcher copy whose DEFAULT brief/prompt point at the scratch set, no overrides, stdin `/dev/null` → every guard
passes, the DEV_NOTE is echoed, the TTY guard refuses → 22; **22b the same under `script` (a pty) with claude ABSENT → the TTY
guard passes, `cd`, `exec claude` → `exec: claude: not found` → 127** — the pass path reaches the exec line. Exit 20 both arms
(20a the prompt, 20b the brief carrying only the 9-char SHA). LANDED = asserting python replace (anchor must exist) +
`grep -cF` of the new marker ≥ expected + `cmp` non-identical to the pristine copy; env cells = the override/empty file
asserted. Every cell under `env -i` with a PATH holding git/python3/grep/perl/cmp/script but NO `claude` (asserted absent;
`git` asserted present as the positive control), `GH_TOKEN` unset, 120 s `perl alarm` per cell, under **bash 3.2.57**
(printed). Cell 24 (real launch, no overrides) refused on the REAL brief path with rc 3 — proves nothing is installed.
`/bin/bash -n` on the launcher: ok (asserted in-run).

## `controls_check.sh` (§4 positive-control tokens — derived from #983's OWN files at `f62c975c1`, `e62eab87a` and M18)

**213 ok, FAILS=0, rc 0** (07:24:55 AEST): 22 contents-API fetches (20 blob-id rows, 14 sha256 rows, 12 line-count rows,
10 byte-count rows asserted) + 3 ABSENT-as-required fetches (the ks823 test at parent and develop; the ks790 test at develop);
12 byte-identity rows (`jwt.ts` parent == develop; head DIFFERS; routes/oauth.ts differs at every step of the stack; ks820-821
head == parent, parent != develop; the five untouched neighbours head == develop; ks790 head != parent); 51 exact-LINE
controls (routes/oauth.ts head `:698 :714 :723 :734 :777 :844 :856 :879 :880 :883 :884 :887 :889 :910 :919 :931 :938 :939 :948`;
the parent's `:754 :755 :818 :876`; jwt.ts `:28 :32 :166 :178 :195 :206 :219 :229 :367 :368`; the ks823 test `:71 :125 :131 :228`;
the ks790 test head `:115 :193` and parent `:113 :189`; routes/auth.ts `:658 :665 :689 :698`; services/oauth.ts `:133 :158 :161
:266 :340 :374`); 74 token counts (the tamper anchors ×1 at head; the parent's world absent at head and present at the parent;
develop's `getUserById` ×2 / no `readClientId`; jwt.ts's new symbols ×1/×2/×3 and `client_id` ×6, all absent at the parent;
the 11 cell titles ×1; the loopback bind; the real minter (`vi.mock('../services/jwt'` absent); the ks790 6 cells / 17 `expect(`
at head AND parent; the sibling's 4 two-argument mints and 0 `client_id`); the 17-row Python sim (the ks790 `expect(` set
identical 17 → 17 and +4 lines; the refresh-branch ORDER offsets ascending `[1466 … 6044]` and the parent's branch lacking
every client token; the minter census 5 + 2 = 7 and `routes/auth.ts`'s five `const tokens = generateTokenPair(`; six
Basic-vs-body shapes through a Python transcription of `readClientId` / `readClientSecret`; the binding predicate on
absent / foreign / own; the sibling's mechanism; the mock's three SQL discriminators verbatim in `services/oauth.ts`; the
app-row column names; 0 raw control bytes with the synthetic NUL control). **Negative controls:** `QA983_HEAD=e62eab87a…`
(the parent as head) → rc 1, **95 FAIL**; `QA983_HEAD=d00a2015c…` (#984's head) → rc 1, **44 FAIL** (oauth.ts 1,338 lines,
jwt.ts 406, the ks823 test `db9744c97`); `QA983_DEVELOP=e62eab87a…` → rc 1, **15 FAIL**. **Three first-draft errors corrected
against the real bytes BEFORE the recorded run** (none reached a `.out` that is kept as green): the parent's refresh mint is at
`:876` not `:867` (hunk arithmetic); `mapAppRow`'s `appType` line is `:374` not `:372`; three `$1`/`$2` placeholders inside
double-quoted `lineis` arguments expanded under `set -u` (escaped). One structural error found by the first RUN and fixed: the
ORDER sim sliced the branch up to the FIRST `} catch (error: any) {` in the file (which precedes the branch) → an empty slice,
every offset −1; fixed to the first catch AFTER the branch start; and `routes/auth.ts` has FIVE `const tokens =
generateTokenPair(` (four one-line + the multi-line `:448`), not four — asserted as 5.

## Measured target facts (instrument beside each)

| fact | value | instrument |
|---|---|---|
| PR #983 state | open, not draft, not merged, kksecura, base develop `8861e6216`, created 14:26:20Z, updated 14:26:39Z (2026-09-13), 2 commits, 5 files +673 −25, `mergeable: true / unstable`, 0 reviews, 0 review comments, 1 issue comment (linear[bot], the mirrored ticket; its 1 at-sign = the `@ \`sha\`` idiom) | REST `/pulls/983`, `/reviews`, `/comments`, `/issues/983/comments` 07:12 |
| PR #982 / #984 (neighbours) | #982 open head `e62eab87a` 1 commit 3 files +280 −5, body 0 at-signs KS-790 only; #984 open head `d00a2015c` 3 commits 8 files +1049 −28, body 0 at-signs refs #982 #983 | REST |
| KS-823 | In Progress, High, kamil.kreiser, attachments #983 + #831, 4 comments (newest `e64ec267` 14:26:49Z — s212's READY record, names both SHAs, 0 at-signs, 0 mention nodes), relation → KS-1003; description 2,075 chars (1 at-sign = the idiom); `branchName` = the PR's branch | Linear GraphQL 07:13 |
| board search by symbol | `verifyRefreshToken` → KS-756 only; `readClientId` / `OAuthTokenClaims` / `OAuthMintOptions` / `readClientSecret` / `token binding` → 0; `getAppByClientId` / `verifyClientSecret` / `grant_type=refresh_token` → KS-823 only; `/api/auth/refresh` → KS-983, **KS-756**, KS-561, KS-515, KS-242; `denylistRefreshJti` / `rotateSessionRefreshToken` → KS-756; `client_id` → 13; `refresh_token` → 11; `invalid_client` → KS-841, KS-840 | Linear `searchIssues`-shaped filter (title OR description, includeArchived) 07:13–07:14 |
| KS-756 | Backlog, High, 0 attachments, 0 comments; "Wire up the opaque refresh token that createSession already mints — one write site, zero read sites"; scope item 2 = `/api/auth/refresh` looks up by handle and drops `verifyRefreshToken`; item 4 names `routes/oauth.ts`'s own refresh path | `linear_neighbours.out` |
| the builder's records | `2026-09-13_s212/item3/` 25 files (the four tamper outputs' `Tests N failed \| M passed` lines: 2/9, 2/9, 1/10, 1/10 — T4's red `expected 500 to be 401`); `red_at_head_v2.out` `7 failed \| 4 passed (11)` with the 200-with-a-token messages; `green_auth_all.out` `3 failed \| 699 passed (702)` (the parent's ks790 bytes vs the head product); `green_auth_all_v2.out` 52/702; `tsc_*.out` 0 lines; `push4-ks823/` 12 files; `HANDOVER-s212-laneL1-oauth.md` 7,056 B; SHA256SUMS 208 rows | `ls`, `/usr/bin/grep -n` (`s212_records_read.out`, redacted) 07:14–07:16 |
| the checkout | HEAD `355d82c8b` on `feature/ks-597-b-caller-scoped-externalref`, porcelain 0 at 07:14 AND 07:58; `.git/config` `e0fa706f4bdae277`; 848 refs both reads; **`.git/worktrees` 90 → 94** (`s214-ks926-r2`, `s214-ks991-r2`, `s216-ks764-r3`, `s217-ks1004-r2` — OTHER seats, live during the draft; none mine — I ran no `worktree`/`clone`); `worktrees/` dir 88 → 92; local develop = origin/develop = `8861e6216`; the local ks-823 branch ref `f62c975c1` | `checkout_read.out`, `lsremote_2.out` |
| the builder's worktree | `worktrees/s212-ks823` ON its branch at `f62c975c1`, porcelain 0; node_modules 985, vitest 4.1.10, shared dist 28, auth node_modules 8; the four lane files' sha256 == the head blobs' | read verbs 07:14 |
| ks860 loopback guard | blob `e0dfadb9c` at head AND develop (784 lines; `WALK_ROOTS = ['services', 'packages']` `:98`; site regex `:433`; host check `:440`; the 🔴 cell `:463`); both new test files bind `127.0.0.1` (`ks823:131`, `ks790:140`); both 0 raw control bytes | `git show`, contents API |
| index.ts | `express.json({ limit: '10mb' })` `:85`, `express.urlencoded({ extended: true })` `:86`, `app.use('/api/oauth', oauthRouter)` `:115`, `await initJwtKeys()` `:241` inside `start()` which runs only when `NODE_ENV !== 'test'` `:303` | `git show f62c975c1:…/index.ts` |

## NOT DONE (deliberately, or could not)

- **No vitest, tsc, eslint, merge or tamper was RUN** — this is a build; the gate runs them in its own clone. Every "predicted"
  number in the brief is the drafter's from the bytes or the builder's relayed measurement, labelled which.
- **No `git clone --shared` into the OUTPUT DIR** — every object the set needed was reachable by `git show <sha>:<path>` in the
  read-only checkout (all five SHAs present) or by the contents API, so `model/` is a by-SHA file copy, not a clone; the
  brief tells the gate to clone.
- **`1a26eb795`'s tree was not compared to `db10aea98`** by me (the amend's "tree identical" is the builder's claim, relayed;
  the brief's item 5 asks the gate to `rev-parse 1a26eb795^{tree}`).
- **Linear's `comments(first:50)`** read client-sorted; KS-823's 4 comments all listed — no paging needed.
- **The `.candidate` dump** of the launcher is left beside the deliverable (byte-identical; inspection artefact); the four
  stale `model/api.oauth.ts.*` files are left (gitignored; superseded).
- **The tier-1 exemplar named first in the context (`launch_qa_secuura_ks1004_912.sh`) was READ but not used as the
  template** — it predates the disjointness-checked develop pin, the env-override test seam and the exit-20 guard; the #980
  round-2 launcher (the newest carrying all three) was the substitution base, with the round-2-only guard removed and the two
  new guards inserted, as the header and `gen_launcher_983.py` state.
