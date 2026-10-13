**VERDICT: GO WITH NOTE**: 0 Major, 3 Minor, 9 Info. Bound to head `50f0552ce011ac9d8c4caddf67bc747a7fed2d5b` only (PR #1545, KS-998 item 3), measured against live develop `026c2d1614065c79fc8d96007ac0d80f19fb9363`.
Report sha256/16: `4cb85c41ae671c0e` (recipe: delete this line 2 only, run `shasum -a 256` over the rest of the file, keep the first 16 hex characters).

# QA gate: Secuura Platform K PR #1545 (gate 1532 Minor 3 + Info 3/5, and the four Minors of gate 1540), Opus tier 1

- **Head under test:** `50f0552ce011ac9d8c4caddf67bc747a7fed2d5b`. I read `refs/pull/1545/head` with my own `ls-remote` (19:59:09 AEDT, `logs/lsremote_1.txt`) and fetched it into a scratch `clone --shared` (push URL `DISABLED`), using the project's `core.sshCommand`. It matches the brief.
- **Develop:** my own `ls-remote` read `026c2d1614065c79fc8d96007ac0d80f19fb9363` (PR 1542 / KS-1119, one commit on top of `405e33a1`), matching Wednesday's read. `405e33a1` is an ancestor of both develop and the head; merge-base(head, develop) = `405e33a1`.
- **This is a re-launch.** The first session left `logs/merge_scope.txt`. I did not rely on it. I re-derived every number in it (`logs/merge_scope_relaunch.txt`). One line in it, `NEITHER+theirs ... security.openapi.ts`, was an artefact of its own string concatenation: my per-path blob check shows every path of the merge equals parent 1 or parent 2.
- **Instruments:** macOS 27.0.1; `/bin/bash` 3.2.57(1) (the only bash; `/bin/sh` is that bash); `/bin/dash`; perl 5.34.1; node v24.7.0; npm 11.5.1; git 2.51.0; `sandbox-exec`; python3 `perf_counter` for timings. The load average was 5 to 18 throughout (other gates were running), so every timing is a loaded-machine timing.
- **Write scope:** no git write verb ran in `!CODING` (only `ls-remote`, `for-each-ref`, `rev-parse`, `rev-list` there). Nothing was pushed. Nothing was written to GitHub or Linear. No Docker and no remote box were used, and none of Postgres ports 55414, 55418, 55436 or 55419 was touched. I wrote only to this folder and my scratchpad. During the run, `evidence/tools/tmp_link_no_uuid` was a symlink to my scratchpad, used as a `TMPDIR` whose path has no UUID (see Info 1). I moved it out to my scratchpad when the runs finished. `evidence/tools/tamper_*.py` are verbatim copies of the author's runners. Nothing was deleted by me; displaced fixture trees were `mv`'d into `_quarantine` dirs. **One stray write, disclosed:** the first run of `tools/cache.sh` (20:23:51) left `gate1545-probe-dep-1.0.0.tgz` in `/Volumes/DevMASTER/WEDNESDAY/` (the project root) from `npm pack <dir>`. It is the EVIL probe tarball, 367 bytes, and its postinstall only appends one line to a scratchpad log. Wednesday flagged it. I moved it, without deleting it, to `evidence/stray_root_write_gate1545-probe-dep-1.0.0.tgz`. Every later pack used an absolute `--pack-destination` inside my scratchpad. No other file outside this folder and my scratchpad changed (`find -newer GATE_BRIEF.md` over the root, excluding `0_Brain/`: none besides the harness's own `.claude/settings.local.json`).
- **Evidence** is under `evidence/` (`logs/`, `mutants/`, `tools/`). File names below are relative to it.

## Why GO WITH NOTE

The PR does what it says for all four 1540 Minors and for most of 1532 Minor 3. Each claim was reproduced red on develop and green on the head:
- **False refusals are gone.** R4 (a tag on an already-pushed commit) and R12b (`origin/develop:refs/heads/rel2`) now land with a note and no banner. A tag on a not-pushed, not-checked-out commit is still refused, and so is the same commit pushed to a second remote that lacks it.
- **Tree mode can no longer be blinded.** `export-ignore` from a pushed `.gitattributes`, from `.git/info/attributes` and from `core.attributesFile` is now caught. Develop gives `format:check OK` in all three. A non-ASCII package is caught; develop prints nothing and returns rc 0.
- **The move-back window never deletes a foreign tree.** On develop the foreign tree is deleted (0 copies anywhere). On the head it is put back, set aside, or kept in a marked stage, depending on the shape.
- **Most of the lock check holds.** Bad lock entries were refused with 0 requests to the listener in all 14 shapes I tried. A control in the same run was fetched and its script ran.
- **The environment scrub works for the names it targets.** None of 16 planted credential variables reached a real lifecycle script.

None of the three Minors lets an unformatted commit through on a configuration that exists today. None is worse than develop, which has no lock check, no scrub and no already-on-the-remote logic. They are:
1. **The lock-source check can be bypassed by a package-level `.npmrc`.** The gate copies it into the stage. With `registry=` pointing elsewhere, npm fetches the tarball from that host even though every `resolved` in the lockfile passed the check, and the tarball's postinstall runs. Measured.
2. **"Already on the remote" trusts local remote-tracking refs, and treats "the remote has this commit" as "this commit was judged".** A stale tracking ref (the branch was deleted or force-moved at the remote) lets a RED commit the remote no longer has land unjudged. That contradicts the code's own comment ("never to a pass"). Separately, fast-forwarding an existing branch such as `develop` to a RED commit already on another remote branch now lands with no format gate and no preflight. Develop refuses both. Measured.
3. **Two mutant survivors are test gaps.** X14 (one of the six 1540 Minor 4 gaps this PR says it closed) and my own Y07 both survive. CASE 48 cannot kill X14, and I built the cell that does.

## Merge scope (`logs/merge_scope_relaunch.txt`, tool `tools/merge_scope.sh`)

| Check | Result | Control |
|---|---|---|
| Develop moved since `405e33a1` | 1 commit, `026c2d161` KS-1119. Its paths are `originate/src/routes/verification.ts` and one ks1119 integration test | — |
| Paths PR (`405e33a1..head`) | exactly 7: `.githooks/pre-push`, `.gitignore`, `Blockchain/Dev/CONTRIBUTING.md`, the hook suite, `systemTest/CLAUDE.md`, the gate suite, the gate. 798+/48− | three-dot `develop...head` gives the same 7 |
| **Overlap** (develop since `405e33a1` ∩ PR paths, `comm -12` of sorted `git diff --name-only`) | **0** | A planted commit on top of develop that edits `.gitignore`: overlap **1** |
| **`git merge-tree --write-tree 026c2d161 50f0552ce`** | **rc 0, tree `7486f5937dfadaa38f5c048842c3c561cb075811`**. It differs from the head tree only by develop's 2 KS-1119 paths, and from develop only by the PR's 7 paths. Every path equals head or develop | A develop-side edit of hook line 52 (a line the PR rewrites) against the head: **rc 1, CONFLICT in `.githooks/pre-push`** |
| Evil-merge check of the head's merge `7b0631668` (p1 `039945795`, p2 `405e33a1`) | Re-merging the parents conflicts in exactly 4 paths (CONTRIBUTING.md, systemTest/CLAUDE.md, gate suite, gate). The merge differs from that auto-merge only on those 4. Every path in the merge equals p1 (the 4, `--ours`) or p2 (19 develop paths). **0 NEITHER** | — |
| Blob claim: is `--ours` lossless? | For all 4 conflicted paths, develop(`405e33a1`) blob = the 1540 head `c6d103ff` blob (e9a3d081c, dbbc62d4f, a0afa3a9c, 7e694574f). `c6d103ff` is an ancestor of p1. `diff c6d103ff 405e33a1 -- <the 4>` is empty | — |
| `h1540..head` | 26 paths, because develop's squash brings in 19 unrelated paths. Against develop, only the 7 | — |

## Suites (`logs/suites/SUMMARY_suites.txt`; instrument: each suite's own `N passed, M failed` trailer)

| What | Head | Control that can fail |
|---|---|---|
| Gate suite (435 cells), my scratchpad `TMPDIR` | 433/2, 433/2, and 433/2 with QUIT+INT ignored | C1 (gate `exit 0` at line 2): **182/253** |
| Gate suite, `TMPDIR` with no UUID in its path | **435/0 ×3** (the three shard controls of the author's runner) and **435/0 with QUIT+INT ignored** (`G_head_QUIT_INT_ignored_noUUID.log`) | same C1 |
| Head's gate suite against develop's gate (red) | **347/88, 347/88** | — |
| Develop's own gate suite on develop | 306/0 ×2 | — |
| Hook suite `ks998_pre_push_judges_the_push` (74) | **74/0, 74/0**; **dash 74/0**; **/bin/bash 3.2.57 74/0**; QUIT+INT ignored 74/0 | C3 (hook `exit 0`): **34/40**. A `[[ ]]` bashism injected under dash: **35/39** |
| Hook suite against develop's hook+gate (red) | **63/11, 63/11** | — |
| stale_base_hint 21 / hook_base 33 / fixture_guard 6 / ks884 10 | all green ×2 on head and green on develop | C3: 11/10, 16/17, 5/1, 6/4 |
| current_develop 4 | 4/0 ×2, develop 4/0 | C3: **4/0, so it cannot fail** (pre-existing, 1540 Info 5) |
| leg_comment 4, stack_legs_comment 4 | 4/0 ×2, develop 4/0 | text checks, no control |
| `ks998_format_gate_push_label_is_literal` 8, `..._stdin_isolated` 9 | 8/0 ×2, 9/0 ×2 | C1: 1/7, 1/8 |

The 2 head failures in my scratchpad are an artefact of the test environment, not of the gate (Info 1). The author's red numbers (68/398 for (A), 8/67 and 11/431 for (B)) were taken on earlier suite revisions. Mine are taken on the final suites.

## (A) The lock check (`logs/A1_lock_sources.txt`, `A2_lock_bypass_pkg_npmrc.txt`, `A2b_…`, `A5_…`, `A6_…`)

These runs used the real gate at the head, real npm 11.5.1 and a local HTTP(S) listener that logs every request. The probe dependency's postinstall records where it ran.

| Shape (default allow list unless stated) | rc | listener GETs | script ran |
|---|---|---|---|
| **C0 CONTROL**, resolved on the listener, `FORMAT_GATE_LOCK_ALLOW=<listener>/` | 1 | **1** | **1** |
| L1 other host; L2 `http://registry.npmjs.org/`; L3 `git+ssh`; L3b codeload tarball; L4 no integrity; L5 `file:`; L6 link `../../..`; L7 `https://registry.npmjs.org@127.0.0.1:…`; L8 `registry.npmjs.org.evil.example`; L8b upper-case host; L9 v1 `dependencies` on another host | 1 each, **REFUSED by name** | **0** | **0** |
| L5b `file:` with `FORMAT_GATE_LOCK_ALLOW=file:` (control: the override really replaces the default) | 1 | 0 | 1 |
| L10 v1 lock with a benign `packages` and an evil `dependencies`; L10b v2 with empty `packages` | npm itself fails (old-lockfile metadata fetch from the configured registry), so **nothing is fetched from the evil host** | 0 | 0 |
| F1 allow list written into a package `.npmrc`, a repo-root and a package `.env`, `package.json` `config`; F2 into `git config` | 1, refused | 0 | 0 |
| R1 the root package's own `postinstall`; R2 an in-repo `link` target's `postinstall` | lock accepted | 0 | **1 each**. R2 runs with cwd `systemTest/linked`, in the developer's working tree, outside the stage |
| **B1 lockfile all `https://registry.npmjs.org/…` + package `.npmrc` `registry=https://<other host>/` (+ `strict-ssl=false`, only because my listener is self-signed)** | 1 | **1** (npm's log: `GET 200 https://127.0.0.1:…/gate1545-probe-dep/-/…tgz`) | **1** (Minor 1) |
| B2 same, without `strict-ssl=false` | TLS refusal (self-signed cert; a real host would have a valid one) | 0 | 0 |
| B3 CONTROL same lock, no `.npmrc` | GET 404 from the real registry.npmjs.org | 0 | 0 |
| B1 against two candidate fixes: no `.npmrc` copied into the stage / `--replace-registry-host=never` | | **0** each | 0 |

**The real four lockfiles** (instrument: node over `packages`): akto 413, api-explorer 344, performance 271, playwright 217 entries, for **1,245**. Two of them are links, both `../../observability`, inside the repo. 0 entries are off the registry, 0 lack an integrity, 0 are sha1. All four are lockfileVersion 3. `_check_lock_sources` accepts all four (rc 0, median 52 to 58 ms each, including bash start-up). The same akto lock plus one planted `evil.example` entry is refused.

**The real gate on the real four packages**, tree mode, `--all`, empty cache, scrubbed `env -i`, real registry (`A5_real_four_packages.txt`): **rc 0 in 20.4 s wall**. Installs took 2.5 / 2.1 / 6.0 / 1.4 s. All four were format-checked OK. Afterwards there were 0 stage/tree/aside dirs and 0 marker files, prettier was executable in all four, the lockfiles were byte-identical and `git status` showed 0 lines. Before: 0 `node_modules`, 0 cache files. With the network denied (`sandbox-exec`): both SKIP, NOTHING CHECKED, rc 1 (control: `curl` gives 000 inside the sandbox, 200 outside).

## (A) The install environment (`logs/A3_install_env.txt`, `A4_cache_fallback.txt`)

A real lifecycle script under the real gate. The developer shell held 40 planted variables.
- **Withheld:** NPM_TOKEN, GITHUB_TOKEN, GH_TOKEN, NODE_AUTH_TOKEN, AWS_ACCESS_KEY_ID / SECRET / SESSION, AZURE_CLIENT_SECRET, SSH_AUTH_SOCK, GIT_ASKPASS, NODE_OPTIONS, DATABASE_URL (userinfo password), `npm_config__authToken`, `_auth`, `_password`, `NPM_CONFIG_PASSWORD`, `certfile`, `keyfile`, `apikey`, `api_key`, `passwd`, and `Npm_Config_Mixed` (mixed case is outside the `npm_config_*|NPM_CONFIG_*` arms).
- **Received:** `HOME=<stage>/.home`, `TERM=dumb`, LANG, TMPDIR, PATH, `MY_EXTRA` (named in FORMAT_GATE_INSTALL_ENV_PASS), `npm_config_cache=<the developer's ~/.npm>`, and `npm_config_userconfig=<stage>/.home/.npmrc` (set by npm). Also received, so names the six patterns miss: **`npm_config_otp`** (a real npm credential key), `npm_config_username`, `npm_config_email`, `npm_config_ca`/`cafile` (public), and the not-npm-keys `bearer`, `jwt`, `pat`, `session`, `cookie`, `pwd`, `private`, `sig`, `signature`, `credential_helper`. **Wednesday's case 1:** `npm_config_registry=http://user:pw@…`, `npm_config_proxy`, `npm_config_https_proxy` and `HTTPS_PROXY` with userinfo all reach the script verbatim (Info 2).
- **A token in the developer's `~/.npmrc` reached the script's environment 0 times.** The script still learns the real home from `os.userInfo().homedir` (`/Users/kam_code`), and can read any file there by absolute path. That is the stated limit, and it is true.
- `FORMAT_GATE_INSTALL_ENV_PASS` names `A-B`, `1ABC`, `A=B`, `$(id)` and `A*` each give exit 2 naming the variable. `OK ALSO_OK` is accepted.

**Cache (Wednesday's case 2, the author's (b)).** These runs used the real gate and real npm, with `npm_config_cache` unset and `HOME/.npm` present, and two tarballs with the same name@version, BENIGN and EVIL.

| Row | GETs | Script that ran |
|---|---|---|
| K1 cold developer cache (the gate passed `~/.npm`) | 1 | benign. The cache gained 1 index key, the tarball URL. **0 packument requests** |
| K2 cached content overwritten in place with EVIL | 1 (refetch) | **benign** |
| K3 a cache index entry for the same URL pointing at EVIL content (metadata poisoning) | 1 (refetch) | **benign** |
| K4a another lock (EVIL integrity) fills the cache; K4b this lock (BENIGN integrity, other URL) | 1, 1 | EVIL, then **benign** |
| K4c CONTROL: the EVIL integrity again | **0** (served from cache) | EVIL, which proves the cache is consulted |
| K5 `~/.npm` mode 555 (a cache owned by another user is not buildable here; no sudo) | 1 | none. REFUSED "npm ci exited 243" with npm's own `chown` remedy. Same as a manual `npm ci` |

The script also **wrote a file into the developer's `~/.npm`** (`cacheWrite=yes`). That is the author's stated consequence. Since the cache is content-addressed by the lock's integrity, I found no way for a poisoned entry to be served to a later locked install. A script could still poison packument entries for a later *unlocked* `npm install` elsewhere, but it can do that by absolute path anyway.

## (B) The four 1540 Minors

**Minor 1: real `git push` to bare remotes** (`logs/B1_push_matrix_{HEAD,DEVELOP}_{1,2}.txt` + `_full.log`, tool `tools/push_matrix.sh`). Two runs, identical on every row that the two runs share.

| Row | Head | Develop |
|---|---|---|
| R4 tag on an already-pushed BD commit, HEAD=main | **lands, note "already on the remote (origin)", no banner** | refused |
| R4c tag on a NOT-pushed, not-checked-out BD commit | refused | refused |
| R4d tag t4 to the SECOND remote `fork`, which lacks it | **refused** (judged against fork) | refused |
| R12b `origin/develop:refs/heads/rel2` | **lands, note, banner 0** | refused, after printing "UNCONDITIONALLY" |
| R12c / R12d already-pushed feature commit to a new branch on origin / on fork | lands with note / **refused** | refused / refused |
| **R20** HEAD=develop fast-forwarded to an already-pushed RED feature commit (BD + systemTest), `push origin develop` | **rc 0, develop moves to the RED commit, no gate, no preflight** | **refused, gate FAILED** |
| **R21** `f21:develop`, RED systemTest commit already on `origin/f21` | **rc 0, lands unjudged** | refused, gate FAILED |
| **R22** STALE: branch f22 (RED, BD) deleted at the remote, local tracking ref kept; `push f22:again`, HEAD=main | **rc 0, lands**, prints "already on the remote" although **0 remote branches contained it** | refused |
| **R22b** the same with HEAD = f22 | **rc 0, lands** | refused, gate FAILED |
| R22c CONTROL R22 after `fetch --prune` | refused | refused |
| **R23** STALE: f23 (RED) force-moved at the remote; push f23 as n23 | **rc 0, lands** | refused, gate FAILED |
| R23b CONTROL R23 after `fetch` | refused, gate FAILED | refused, gate FAILED |
| R30 three refs, one RED / R31 deletion / R32 detached HEAD BD / R33 dirty: commit green, WT red / R33b commit red, WT green / R34 HEAD branch with upstream (X04 shape) | same as develop: refused / lands silently / preflight+banner / lands / refused / preflight runs | same |
| R35 unborn HEAD | refused, now "HEAD is not a commit yet (an unborn branch)" | refused, "HEAD is HEAD" |

**Minor 2: tree mode** (`logs/B2_tree_mode.txt`, tool `tools/tree_mode.sh`; head, the q12 mutant, develop):

| Shape | Head | Develop |
|---|---|---|
| T1a pushed `.gitattributes export-ignore` on the red file / T1b `.git/info/attributes` / T1c `core.attributesFile` | **FAILED ×3** | **OK ×3 (false pass)**. Control without attributes: FAILED on both |
| T2 red file in `systemTest/pkgé` | **FAILED** | silent, rc 0 |
| T3 symlink to an outside red file / dangling symlink / red file 5 dirs deep | FAILED ×3 | FAILED ×3 |
| T4a red blob + a DEVELOPER-configured smudge filter `bad→good` (pushed attribute + local driver) | OK | OK (archive applies it too). Control without the driver: FAILED (Info 4) |
| T4b green LF blob with pushed `text eol=crlf` / T4c `core.autocrlf=true` / T4d `ident` | FAILED (false refusals, the fixture's check sees CRLF / `$Id$` expanded) | FAILED, the same |
| T5a non-cone sparse checkout excluding `src/` (package.json and node_modules present) / T5b cone + sparse index | FAILED / FAILED (red caught) | FAILED / FAILED |
| T6 private index `<tree>/.idx` present during the check | 1 | 0 (archive) |
| T6 SIGINT / TERM / HUP / QUIT mid-check: tree dirs left | 0 / 0 / 0 / 0 | 0 |
| T6 SIGKILL: tree dirs left; next run (red, exit 1) sweeps it | 1, then 0 | 1, then 0 |
| T7 real `.git/index` unchanged, no `index.lock` | yes, 0 | yes, 0 |

**Minor 3: the move-back window** (`logs/B3_move_back_window.txt`, tool `tools/minor3.sh`). An npm stub embeds its stage path. A node shim plays another actor at the worst moments.

| Shape | Head | Develop |
|---|---|---|
| SWAP=0 control (nothing foreign) | mvbroken, nothing left | same |
| SWAP=1 a foreign NON-EMPTY tree replaces `node_modules` just before the back rename (1540 M1c) | **put back in the package** (1 copy), "nothing of theirs was deleted" | **deleted (0 copies anywhere)** |
| SWAP=2 + a third tree appears before the put-back | **foreign tree LEFT in `.format-gate-aside.*`**, named in the refusal, gitignored | not reachable on develop (deleted at SWAP=1) |
| SWAP=3 + the aside `mv` fails | **stage kept with `.format-gate-keep`**; the next run keeps it and still sweeps an ordinary dead stage; 1 copy survives | — |
| Window: the node process that performs one `rename(2)` | min/median/max 34.5 / 35.8 / 38.2 ms (30 runs) | 32.3 / 34.1 / 37.8 |

"About 40 ms" is right.

**Minor 4: the six X-cells** (my mutants on the head, `mutants/mine/batch2.log`): **X02 killed** (hook 71/3), **X04 killed** (72/2), **X09 killed** ("SIGINT … exit 130"), **X10 killed** ("SIGHUP … exit 129"), **X15 killed** ("…remedy is 'check out what you push'"), and **X14 SURVIVED** (435/0, 74/0) (Minor 3).

**Info items claimed fixed:** the doc says 435 and 74, and both counts match. Deletion R31 lands silently. The unborn-HEAD wording is fixed (R35). The no-perl remedy names perl (CASE 49 green). Info 1 (n15/n17a) is now killed by name in the author's runner (see Mutants).

## Mutants

**The author's runners on the exact head** (`tools/tamper_gate4.py`, `tools/tamper_hook3.py`; logs and JSON in `mutants/author_runner/`). The gate runner ran in 3 shards, each preceded by its own unmutated control, all three **435/0 GREEN**:
- **Gate: 146 mutants, 136 KILLED-BY-NAME, 10 SURVIVED-BY-DESIGN, 0 unexplained** (instrument: the runner's verdict per mutant, re-tallied from the three `results.json`). The survivors are m13a, m23, m25, m35, n03b, p30, p35, p38, q11 and q12: the author's ten.
- **n15 and n17a are now KILLED-BY-NAME**, so 1540 Info 1 is closed.
- **Hook:** control [(74,0),(21,0),(33,0)] GREEN, then **33 of 33 KILLED-BY-NAME**.

**My judgement of the five non-1540 survivors:**
- **p30** (REDUNDANT): agree. An empty prefix with an absolute path leaves `rest` with a `/`, which the single-component guard refuses. p32 (both guards dropped) is killed.
- **p35** (UNREACHABLE): agree. `read -r -a` never yields an empty word.
- **p38** (EQUIVALENT on POSIX): agree. `path.relative` never returns an absolute path on POSIX.
- **q11** (UNREACHABLE): agree by reasoning. A package is selected only if it is found in the commit's tree. I built no cell.
- **q12**: EQUIVALENT in the two sparse shapes I could build (T5a, T5b: head, q12 and develop all FAILED the red file). The author's stated reason is wrong; see Minor 3.

**Mine** (`tools/my_mutants.py`, `tools/my_mutants2.py`; `mutants/mine/`). Each mutant is an exact-once edit run through the real suites with a UUID-free `TMPDIR`. Gate mutants ran the gate suite and the hook suite; hook mutants ran the three hook suites.

| Mutant | Result: suite counts, first failing cell |
|---|---|
| Y00 gate, comment only (CONTROL) | **reddens nothing**: 435/0, 74/0 |
| Y00h hook, comment only (CONTROL) | **reddens nothing**: 74/0, 21/0, 33/0 |
| **Y02 lock check moved after the install** (brief) | KILLED 432/3: "...the listener was NEVER contacted (0 requests)" |
| **Y03 credential-name test not case-folded** (UPPER-case names slip) | KILLED 434/1: "the install does NOT see NPM_CONFIG_PASSPHRASE" |
| **Y05 aside rename replaced by a delete** (brief) | KILLED 432/3: "...the foreign tree is LEFT in a gitignored .format-gate-aside dir, not deleted" |
| **Y07 `~/.npm` fallback appended even when `npm_config_cache` is set** | **SURVIVED** 435/0, 74/0 (Minor 3) |
| **Y13 onremote skip removed** | KILLED 69/5 (hook suite) |
| **Y15 onremote direction inverted** (`--merged` instead of `--contains`) | KILLED 38/36, 11/10, 19/14 |
| **Y16 a bad source passes when it carries an integrity** | KILLED 406/29: "a lock entry resolved to a LOCAL HTTP listener ... REFUSED naming the entry" |
| **Y18 put-back failure reported as put back** | KILLED 431/4: "...LEFT in a gitignored .format-gate-aside dir" |
| Y01 prefix becomes a substring match (brief; = author p05) | KILLED 434/1: "an allowed prefix appearing LATER in the URL does not count" |
| Y04 private HOME removed (brief; = p19) | KILLED 433/2: "HOME is a private directory inside the stage" |
| Y06 npm-shrinkwrap.json not checked (= p09) | KILLED 432/3: "a bad entry in npm-shrinkwrap.json only ... REFUSED" |
| Y08 extraction without NUL (= q13 + q02 partly) | KILLED 434/1 and hook 71/3: "tree mode: the red non-ASCII package is discovered and FAILS" |
| Y09 onremote reads EVERY remote (brief; = h22) | KILLED 73/1 |
| Y10 remote name fixed to origin (= h23) | KILLED 73/1 |
| Y11 banner before the refusal (= h24) | KILLED 71/3 |
| Y12 quotePath dropped at the third diff site (= h28) | KILLED 72/2 |
| X02 / X04 (1540's, on the head) | KILLED 71/3 / 72/2 |
| X09 / X10 / X15 (1540's) | KILLED: "SIGINT ... exit 130", "SIGHUP ... exit 129", "...remedy is 'check out what you push'" |
| **X14 (1540's)** | **SURVIVED** 435/0, 74/0 (Minor 3). The distinguishing cell is `tools/x14_cell.sh` |

The first eight rows in bold (Y02, Y03, Y05, Y07, Y13, Y15, Y16, Y18) are not in the author's list. Seven are killed by name and one survives.

## Findings

### Minor 1: a package-level `.npmrc` redirects the install to a host the lock check never allowed

**Where:** `systemTest/scripts/check-package-format.sh:485` copies `.npmrc` into the stage, and `:494` runs `npm ci` with npm's default `replace-registry-host=npmjs`. `_check_lock_sources` (`:351`) validates only `resolved`. The docs claim "nothing is fetched or run" at `:153`, `:350`, `systemTest/CLAUDE.md:494` and `Blockchain/Dev/CONTRIBUTING.md:401`.

**Shape (B1):** a lockfile in which every entry is `https://registry.npmjs.org/…` with an integrity passes the check. A `systemTest/<pkg>/.npmrc` with `registry=https://attacker/` arrives on the same branch. npm rewrites the registry host and **fetches the tarball from the attacker** (listener: 1 GET), and its postinstall **runs** (1). The integrity is the attacker's own, because they wrote the lock. `strict-ssl=false` was needed only because my listener is self-signed (B2); `.npmrc` can set it too, as well as `https-proxy`, `ca`, `cafile`. Control B3, without the `.npmrc`: the fetch goes to registry.npmjs.org.

This is the same threat model the code states ("content that arrives on a branch or in a merge the developer did not author"). No `systemTest/*/.npmrc` exists today (`git ls-files`: only `Blockchain/Dev/.npmrc` and `Blockchain/Dev/packages/shared/.npmrc`). Develop has no lock check at all, and the same attacker can reach script execution through a package published on the allowed registry (the stated limit). That is why this is Minor and not Major. But it defeats the PR's headline sentence.

**Minimal fix:** do not copy `.npmrc` into the stage, or refuse (`lockbad`) when a package `.npmrc` sets `registry`, `*:registry`, `replace-registry-host`, `strict-ssl`, `proxy`, `https-proxy`, `ca` or `cafile`. Also pass `--replace-registry-host=never`, so that npm fetches exactly the URL that was checked. Both candidates gave 0 GETs on B1 (`logs/A2b_lock_bypass_fix_candidates.txt`). One cell: B1.

### Minor 2: "already on the remote" trusts local tracking refs and treats "the remote has it" as "it was judged"

**Where:** `.githooks/pre-push:120`, which runs before step 1 (the existing-branch diff) for every ref. The comment at `:116-119` says a stale ref "can only MISS a commit the remote has … never to a pass". The docs say "sends nothing new" (`CONTRIBUTING.md:417`, `systemTest/CLAUDE.md:530`).

**Shapes (`B1_push_matrix_*`):**
- **Stale tracking ref (R22, R22b, R23).** The branch was deleted (for example after a squash merge) or force-moved at the remote since the last fetch. A RED commit **the remote no longer has** lands on a new branch with rc 0, under a note saying it is already on the remote. Develop refuses all three. The controls after `fetch --prune` are refused on head too. In the real project clone, 4 of 789 tracking refs are already stale (`git ls-remote` vs `for-each-ref`).
- **Existing branch moved to an already-pushed commit (R20, R21).** `push origin develop` after a fast-forward onto a RED feature commit that sits on another remote branch lands with no gate and no preflight. Develop judges `remote_sha..tip` and refuses.

Both need the RED commit to have reached the remote once already: through `--no-verify`, a developer whose clone has no `core.hooksPath`, or a web edit. GitHub branch protection probably makes direct `develop` pushes moot. That is why this is Minor. The cost of the check is fine: 12 to 362 ms over 790 tracking refs.

**Minimal fix:** apply the `onremote` skip only to refs the remote does not have yet (`_jr_rsha` empty or zero), after step 1, so that updates of existing branches keep their `remote_sha..tip` judgement. Correct the comment and the docs ("a tracking ref is only as fresh as your last `git fetch --prune`; a deleted or force-moved remote branch can make the hook skip a commit the remote no longer has"). Optionally confirm with one `git ls-remote <remote>` before skipping. One cell each: R20, R22.

### Minor 3: two surviving mutants are test gaps, one of them a gap this PR says it closed

| Mutant | Result | Distinguishing cell |
|---|---|---|
| **X14** (ancestor-config names listed from HEAD instead of the pushed commit) | survives the gate and hook suites (435/0, 74/0). CASE 48 keeps `.prettierrc` at both commits with different content. The content is extracted from the pushed commit's private index either way, so CASE 48 cannot kill it | `tools/x14_cell.sh`: the pushed commit has `.prettierrc`, HEAD has **deleted** it. Head: rc 0. X14: **rc 1**. With both present (CASE 48's shape): 0 and 0 (`logs/B4_x14_distinguishing_cell.txt`) |
| **Y07** (the `~/.npm` fallback appended even when `npm_config_cache` is set, so `env -i` takes the last value and a developer's chosen cache is ignored) | survives (435/0, 74/0) | a cell with `npm_config_cache=X` and `HOME/.npm` present that asserts exactly one `npm_config_cache=X` in the install's environment |

The author's stated reason for q12 is also inaccurate. A sparse working tree can keep the package and its `node_modules` (T5a: `src/` excluded, `package.json` present), so the run does not end in `notintree`. The mutant is still **equivalent** in both sparse shapes I built, because `read-tree` without `-u`/`-m` applies no skip-worktree bits: head, q12 and develop all FAILED the red file.

### Info

1. **Two gate cells fail when the fixture path contains a UUID.** "the install's npm userconfig is the stage's private HOME…" and "…npm_config_userconfig=<file> opts a userconfig back in" call `npm config get userconfig`. npm 11.5.1 refuses that ("The userconfig option is protected") when the value contains a UUID-shaped string, which @npmcli/redact treats as a token. My scratchpad path has one. Through a UUID-free `TMPDIR`: 435/0. This is a harness fragility on any runner whose temp path holds a UUID. **Fix:** have the stub derive the userconfig from `node -p 'require("os").homedir()'`, or assert on `HOME` alone.
2. **Wednesday's case 1, credentials in values and names the patterns miss.** Userinfo in `npm_config_registry`, `npm_config_proxy`, `npm_config_https_proxy` and `HTTPS_PROXY` reaches every install script verbatim, and so does `npm_config_otp`. For that credential the scrub does not help. The PR body says so, and the code comment (a script "can still read files by absolute path") is honest. `CONTRIBUTING.md:403-405` ("without your shell's secrets") and `systemTest/CLAUDE.md` do not say it. **Fix:** a doc sentence, and add `otp` to the patterns.
3. **What still runs from the repository:** the package's own lifecycle scripts (R1) and an in-repo `link` target's scripts (R2), the latter **with cwd in the developer's working tree** (`systemTest/linked`). Covered by "lifecycle scripts still run", but not spelled out.
4. **checkout-index applies the developer's conversions (the author's (c)).** A developer-configured smudge filter makes a red blob pass (T4a), and `eol=crlf` / `core.autocrlf` make a green LF blob fail (T4b/c). Both happen identically on develop (`git archive` applies them too), so this is not a regression. LFS was not testable (no git-lfs).
5. **`FORMAT_GATE_LOCK_ALLOW` without a trailing slash** (`https://npm.example.com`) accepts `https://npm.example.com.evil.example/…` (`logs/A6_…`). The default has the slash. The docs should say "end the prefix with `/`".
6. **The aside and kept stages are never swept**, by design. They accumulate in `systemTest/` and are gitignored and named. Nothing cleans them up.
7. **Not-writable `~/.npm` (K5):** refused with npm's own `chown` remedy. That is the same behaviour as a manual `npm ci`.
8. **PR body and Linear not verified.** The repository is private. Neither this seat's nor the project's `gh` config is logged in, and I have no Linear access. I read the author's draft `tools/pr/body_item3_final.md`: it has `@@…@@` placeholders, "Refs KS-998", and **0 closing keywords** (control: "KS-998" found 1×). The 28 commit messages in `405e33a1..head` have 0 closing keywords (control: "gate" found 47×). The commit-by-finding table matches the commits: (A) `236f07441` + cells `b21fd5e56` / `047d43003`; Minor 1 `3b7e96581`; Minor 2 `935231162` + `5888621bb`; Minor 3 `cae5ee837` + `031240fa9`; Info 4 `a8d58d1a0` + `6ff70eec2`. The PR's commit list also carries 1540's unsquashed commits and the merge; the diff does not.
9. **Pre-existing, unchanged:** `pre_push_hook_current_develop` cannot fail on a dead hook (C3 4/0). Submodules are not checked in tree mode (1540 Info 3, not retested).

## NOT tested, and whether it could hide a Major

- **Linux / GNU userland:** none installed (no gnubin), no Docker, no remote box allowed. BSD `xargs` and GNU `xargs` both run the command once on empty input, and the `[ -d … ]` check catches an empty extraction. The hook ran under dash on macOS only.
- **Preflight legs 3, 4 and 8, and a full real push through the preflight:** not run (the stack is needed). The author's 9 min 29 s push was not re-measured.
- **A registry mirror or proxy end to end, and a private authenticated registry:** not run. Only the override semantics (L5b, A6) and the `.npmrc` redirect (B1) were measured.
- **A cache owned by another user:** no sudo. The nearest case (mode 555) is K5.
- **Submodules, LFS:** not run (no git-lfs).
- **Exec-bit preservation (T3c):** the fixture's mode line did not reach the gate output. I make no claim.
- **The live PR body and the Linear attachment** (Info 8).

None of these could hide a Major on the evidence above. Every refusal path is fail-closed. The two pass-through shapes (Minor 1 and Minor 2) need either repository content that does not exist today or a commit that was already on the remote once.

## Recommendation to Wednesday

**GO WITH NOTE** on `50f0552ce011`, merged onto develop `026c2d161` (merge-tree clean, 0 overlap). This is developer tooling: merge only on Wednesday's head-bound GO, and do not deploy anything. Minor 1 (drop or refuse the package `.npmrc`, plus `--replace-registry-host=never`) and Minor 2 (keep the `remote_sha..tip` judgement for existing branches, and correct the stale-ref claim) are small and should follow fast. Each is a few lines plus one cell. Minor 3 is two cells.
