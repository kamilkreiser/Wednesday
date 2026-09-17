# DRAFTER REPORT: #1033 (KS-763 PR-7, mysql2 override → 3.23.1) tier-1 gate set, 2026-09-17 22:46–23:12 AEST

**BLUF**
- **Head unmoved, develop moved.**
  - Head `2cab54988` re-read at 22:46:44, 22:50:15, 23:02:00 and 23:11:31 (ls-remote), and by the PR API at 22:56:29.
  - **Develop moved after Wednesday's 22:43:43 read:** `bb848b828` → **`27e53ec3a`** (#1029: 1 api-gateway test file, 0 of the 5 PR paths). The merge-base is still `bb848b828`.
- **Runtime reach, MEASURED (host npm 11.5.1 AND node:24-alpine npm 11.19.0; no image build):**
  - The originate runtime tree (Dockerfile `:79 npm ci --ignore-scripts --omit=dev`) moves **mysql2 3.15.3 → 3.23.1, adds sql-escaper 1.5.2, and drops seq-queue 0.0.5 and sqlstring 2.3.3. Nothing else moves.**
  - 96 files differ: 95 inside those 4 dirs, plus `.package-lock.json`.
  - The FULL `:30` install (positive control) shows the same 4 moves. Determinism head vs head2 is 0/0 on both routes.
  - **Only originate's runtime tree carries mysql2:** 2 of 45 locks carry it, and of 37 Dockerfiles only originate's installs either lock.
- **Load, MEASURED:** an in-process `node dist/index.js` in the Dockerfile-shaped runner (host + alpine, base + head) exercised the Prisma adapter-pg path. /health answered 503 (DB unreachable).
  - It loaded **0 mysql2 files**; controls @prisma/client, adapter-pg, pg, express and ioredis were loaded.
  - **Positive control:** the same hook sees `require('mysql2')` (82 files at head).
  - `npx prisma generate` also loads 0 mysql2 files.
  - **PREDICTED, not measured:** NODE_ENV=production, post-connection paths, and prisma CLI commands other than generate (Studio imports `mysql2/promise` for a `mysql` adapter).
- **Pin conflict, MEASURED:** the override holds everywhere measured.
  - `npm ci` on originate's own lock: rc 0 without `--legacy-peer-deps`.
  - `npm ls mysql2`: `overridden`, not `invalid`. FULL tree: 0 invalid.
  - `prisma generate` rc 0 and tsc rc 0.
  - originate jest `--runInBand`: **63/63, 656/656** at base and head, on host and alpine (4 runs).
- **Gates, MEASURED:**
  - head + 29 rows: audit-gate rc 0 (28/29), audit-locks rc 0 (27/27).
  - head + 31 rows: CLEANUP names exactly the 2.
  - **NEGATIVE CONTROL** (base + base baseline minus the 2 rows; bytes equal head's baseline): **both scripts rc 1, each naming exactly GHSA-3f6p + GHSA-rgwj** (audit-locks: services/originate).
  - Teed ranges: rgwj `<=3.23.0`, 3f6p `<3.22.0`. 3.23.1 is outside both under the shipped semver 7.8.5.
- **Scope / merge, MEASURED:**
  - Scope by parse: 4 entries per lock, class drift 0, `packages[""]` unchanged, manifests only `overrides.mysql2`, baseline exactly −2.
  - 11 edges per lock, **1 BAD = the ruled prisma → mysql2 "3.15.3"**.
  - `merge-tree(9fd3cb924, bb848b828)` = head tree `e52244863`; the merge moved exactly develop's 45-file delta; per-entry and per-row both-sides = 0.
  - **Merged tree over 27e53ec3a = `ae3624597bdcb59edf8dc81b7042a9d73b916f9a`.**
- ⚠ **NEW, MEASURED: the READY's root-lock recipe is npm-version dependent.**
  - Under npm 11.19.0, `npm update mysql2 --package-lock-only --ignore-scripts` reproduces head's root lock `646c19f6f` **byte-identically**, and the trap and no-override controls behave as the READY says.
  - Under **host npm 11.5.1** the same command leaves mysql2 at 3.15.3 **and** rewrites 12 flag fields (`86c3685d8`).
  - A gate on host npm would have reported "does not reproduce" as a seat defect. Launcher guard 28 makes brief and prompt carry this.
- **Launcher `--check` rc 0** (23:09:15–23:09:25, and again after the listener-wording edit to brief and prompt at 23:13:30, `out/check_launcher_1033.out`): `27e53ec3a = the draft pin: 20 of 20 guarded paths at their merge-base blobs`. **16/16 controls PASS** both times (fixtures regenerated; last run 23:13–23:16:52).
- **Predicted verdict: GO WITH FINDINGS**, all RECORD-class:
  - the npm-version dependency;
  - the READY's load-trace gap (now largely closed);
  - the edge count 9 vs 11;
  - a bundled mariadb@3.4.5 (not mysql2) in @prisma/query-plan-executor.
  - Nothing measured blocks the merge.

## Files

| file | sha256[:16] | bytes |
|---|---|---|
| brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1033-ks763-mysql2-tier1.md` | `18b72f21ea7672eb` | 36,737 |
| prompt `…/briefs/2026-09-17_secuura-1033-ks763-mysql2-tier1.prompt.txt` | `93a790b934a06126` | 17,419 (under ~19,800) |
| launcher `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1033.sh` (mode 755, 221 lines) | `d567c6070abdc009` | 17,711 |

- **Launcher generation:** `gen_launcher_1033.py` built it from the #1030 launcher. 30 asserted substitutions + 2 asserted segment replacements (JUDGED, AUDIT); pins re-read from the checkout with `git rev-parse`; 74 output controls; residual guard clean; `bash -n` rc 0 (`out/gen_launcher.out`, 23:03:53).
- **Guard = PATH BLOBS, never develop's SHA.** Guarded paths:
  - the 4 non-audit PR paths;
  - **3 reach paths** with no #1033 blob: originate Dockerfile `ac2fb91bf`, `prisma/schema.prisma` `96c3342fa`, `packages/shared/package-lock.json` `5cf24ef21`;
  - all 13 `scripts/audit/` files (the listing must name exactly those).
- **Guard verdicts:** all paths at base → OK; all 5 PR paths at their #1033 blobs → 19; anything else → 18.
- **Other guards:** the compare is asserted as `bb848b828 ahead=2 files=5` (exit 10).
- **Content guards changed on purpose vs #1030:**
  - 26 now requires `name it uniquely` + `--runInBand` + load average. Containers are allowed here, so #1030's "Docker is NOT available" guard would be false.
  - 27 requires `RUNTIME REACH FIRST`.
  - **New 28** requires `npm-version dependent`.
- **Controls** (`check_launcher_1033.sh`, fixtures in `fixtures/` from `make_fixtures_1033.py`):
  - CUR_DEV `bb848b828` → 0;
  - `2cab54988` → 19;
  - `9fd3cb924` → 18 (2 unpinned: root lock e30939c65, baseline 2fe8d78fc);
  - `75ad0e55c` → 18;
  - **Dependabot #949 head `7ee1a26e6` → 18** (prisma bump: root lock, originate lock + manifest);
  - HEAD=`9fd3cb924` → 6;
  - prompt fixtures → 22, 23, 24, 26, 12, 11, 28;
  - brief fixtures → 25, 27, 20.

## Lead questions (MEASURED / READ / PREDICTED)

| # | question | drafter | class · instrument |
|---|---|---|---|
| 1 | Runtime mysql2 | 3.15.3 → 3.23.1; +sql-escaper 1.5.2, −seq-queue, −sqlstring; 304→303 pkgs; 96 files (1 outside = `.package-lock.json`); same on alpine; host/alpine package sets identical | MEASURED · `drafter_runtime_1033.py` P0/P1 (anchors 18/18 at both trees), `drafter_container_1033.py` |
| 1 | Controls | FULL `:30` moves the same 4; determinism 0/0 host (full+rt) and alpine (rt); presence express/@prisma/client/prisma; jest/ts-jest/eslint absent (typescript 5.9.3 present at both, pre-existing) | MEASURED |
| 1 | Other runtime trees | 2 of 45 locks carry mysql2 (root, originate) at head/base/curdev, control express 28; of 37 Dockerfiles only originate copies `services/originate/package*.json`; none installs the root lock | MEASURED (parse) + READ (Dockerfiles) · `drafter_setup_1033.py` G |
| 1 | Bundled code (cause side) | `mysql_clear_password` outside mysql2: 1 file = `@prisma/query-plan-executor` 7.2.0 bundling **mariadb@3.4.5** (not mysql2), via @prisma/dev (devOptional), byte-identical base/head, not loaded at start; `compressed_protocol` outside 0 | MEASURED · `drafter_regen_1033.py` C |
| 2 | Loads mysql2? | host + alpine, base + head: 0 mysql2 / sql-escaper / sqlstring files on an in-process start (adapter-pg path ran; /health 503; ended by SIGTERM to verified pid / my own container's busybox timeout); positive control 82 (host) / 164 (alpine) mysql2 path records | MEASURED |
| 2 | prod / post-connection / Studio | not traced; prisma 7.8.0 `build/index.js` imports `mysql2/promise` only in a `mysql` Studio executor; migrations job uses psql | PREDICTED (nothing loads it) · READ |
| 3 | Pin conflict | `npm ci` rc 0 w/o `--legacy-peer-deps` (host + alpine); `npm ls mysql2` "overridden"; FULL `npm ls --all` 0 invalid (3 overridden head / 2 base); runtime `npm ls --all` rc 1 at base AND head (missing devDeps, instrument); generate rc 0; tsc rc 0; jest 63/656 ×4 | MEASURED (host load1 12.3; alpine loadavg 0.9–1.7) |
| 4 | Gates | H1 0/0 (28/29; 27/27) · H2 CLEANUP exactly the 2 (audit-gate) · B1 NEGATIVE 1/1 exactly the 2, "pinned: 3.15.3", "in 1 lock(s): services/originate" · B0 base+31 0/0 | MEASURED · `drafter_audit_1033.py` (load1 7) |
| 4 | Ranges | rgwj moderate `<=3.23.0`, 3f6p high `<3.22.0` (teed from audit-locks' own bulk fetch); semver 7.8.5: 3.22.0 in rgwj / out of 3f6p; 3.23.1 out of both | MEASURED |
| 5 | Scope | root 1970→1969, originate 655→654, exactly 4 changed each; out-of-subtree 0; class drift 0; `packages[""]` unchanged; manifests exactly `overrides.mysql2`; baseline 31→29 exactly the 2; 11 edges/lock, 1 BAD (ruled) | MEASURED; planted controls fire (the devOptional→dev plant on mysql2 is WEAK — same diff set as the real move; the brief tells the gate to plant on an unmoved entry) |
| 6 | Merge-in | tree `e52244863` both ways; 45 files = develop delta, patch-id `866e99d2096e` equal; both-sides = root lock + baseline, merge-tree blob == head blob; per-entry 43 dev / 4 change / 0 both / 0 mismatch (control fires); baseline regeneration byte-equal; root regeneration byte-equal **only under npm 11.19.0**; originate regeneration byte-equal on host 11.5.1 | MEASURED · `drafter_setup_1033.py` B, `drafter_regen_1033.py`, `drafter_npmver_1033.py` |
| 6 | Merged tree | over `27e53ec3a`: `ae3624597bdcb59edf8dc81b7042a9d73b916f9a`, delta = 1 api-gateway test file; audit inputs == head's | MEASURED |
| 7 | Linking | pull/1033 → KS-763 contributes open only (controls pull/1030 → KS-1211, pull/99999 → 0); 0 closing phrases in title/body/2 commits/1 comment; KS-763 In Progress, completedAt null; KS-751 archived 2026-09-05T06:48Z (Tested Not Deployed), 0 attachments to pull/1033 | MEASURED · `api_read_1033.py` 22:56 |
| 8 | Dependabot | 10 on the root lock (#949 #948 #947 #946 #945 #649 #639 #635 #575 #572); #949 prisma 7.10.0 + originate manifest, still pins mysql2 3.15.3 (`npm view` 23:02); #575 originate manifest; #945 + #920 root package.json | MEASURED (record) |

## Defects / imprecisions in the builder's claims (all RECORD-class; nothing contradicts a seat number)

1. **Root recipe "BYTE-IDENTICAL" omits the npm version.** It is true under npm 11.19.0 and false under host npm 11.5.1. On 11.5.1 the command is inert and drifts 12 flags: 11 `lightningcss-*` gain `dev`, and `magicast` goes devOptional→dev. On 11.5.1 even the "trap" install is not byte-identical.
2. **"No runtime load trace"** is now largely closed by the drafter's host + alpine trace. Production mode and post-connection paths remain open.
3. **"Ranges checked … (9)"** vs 11 edges per lock. The difference is instrument counting (the peer `@types/node` and nested iconv-lite). The single BAD edge agrees.
4. **Import-grep controls** (ioredis 16 / pg 44 / @prisma/client 1) differ from the removed row's own (73 / 50 / 3). The command shapes differ; the drafter did not re-grep.
5. **Not in the READY:** bundled mariadb@3.4.5 in @prisma/query-plan-executor ships in the runtime tree. It is outside both advisories' package scope, unmoved and unloaded.
6. **Verified equal to the READY:**
   - the 4 entries per lock, sql-escaper 1.5.2, flag class devOptional;
   - 2 of 45 locks carry mysql2;
   - 28/29 and 43 lockfiles;
   - the negative control naming exactly the 2 in services/originate;
   - prisma generate rc 0 and jest 63/656 in alpine;
   - merge tree e52244863;
   - the originate regeneration command;
   - the KS-763 In Progress walk (history API: GitHub In Review → In Progress 12:33:23Z);
   - KS-751 archived;
   - 21 open PRs and the Dependabot overlap.

## HOLDs I came near
- **Writes:** all write verbs, installs, builds and container runs happened only under `/private/tmp/claude-501/drafter1033/` (5.2 GB; nothing removed).
  - Scratch trees: clone + worktrees `setup_iaknii1n/`, host trees `runtime_nytkp4px/`, container sources `container_pq4jot2t/`, npm-version copies `npmver_*`.
  - The regen worktrees carry the head manifests by design.
- **Containers:** 6, each named `drafter1033-*`, run sequentially (3 step-replay + 3 npm-version) and removed by exact name (`docker rm` rc 0). 0 remain (23:11:31).
- **Launcher:** `--check` only, 34 invocations (2 × (1 plain + 16 controls)). Never a launch.
- **Listeners:**
  - My 2 host traced starts bound 127.0.0.1 only, 1 LISTEN row each. They were ended by SIGTERM to the verified child pid (argv `node dist/index.js`, pid > 1) and exited 0; 0 remained.
  - The 4 `login_stub.mjs` listeners seen at 22:56 had cwd under `worktrees/raise-0916-a` (Seat A, ppid 1, started 22:55:13–17). They were not mine and I did not touch them. By 23:11:56 none remained, ended by someone else.
- **Self-correction:** my 23:11:31 close reading first counted `login_stub 3 / drafter1033 2 / dist/index.js 2`. Those were self-matches of the reading shell's own argv (echo text). I re-read by full argv at 23:11:56 and got 0 each; the correction is appended in `out/close_readings.out`.
- **Secuura checkout readings:**
  - 22:50:15: porcelain 0, config `f9ef2cb7e4b9fa5a`, refs 941, worktrees 112, branch `feature/ks-597-b-caller-scoped-externalref`;
  - 22:50:50: same;
  - 23:11:31: porcelain 0, config `f9ef2cb7e4b9fa5a`, **refs 942**, worktrees 112, same branch.
  - The +1 ref is not attributed. My clone is `--shared` and writes no refs into its source, and I ran only read verbs there. Other seats are active.
- **Nothing else:** no rm, cd, mail, comment, commit or push. No credential was echoed.
- **Bounds deviation:** 3 `npm view` registry reads (prisma 7.10.0 / 7.8.0 deps, mysql2 dist-tags) at 23:02:00, `out/registry_read.out`.

## NOT measured (the gate must, or must say it did not)
- **Image and runtime:**
  - any image build;
  - the amd64 image npm (my container is linux/arm64);
  - `apk` (`:23`) and native module builds (install scripts are off at `:30` and `:79` anyway).
- **Load trace:**
  - `NODE_ENV=production` (exits without PII_ENCRYPTION_KEY);
  - any path after a live DB connection;
  - any request beyond /health;
  - prisma CLI commands other than `generate` (Studio's `mysql2/promise`) inside the image.
- **Launcher controls:** no develop control isolates a single REACH path. All three guard arms are proven, but the reach rows are covered only by the shared judge logic.
- **Suites not run:** packages/shared; other members; lockfile-cleanroom; the in-hook preflight; the READY's host `npm ci` root-install run of originate. I ran originate's suite on the standalone lock, which is the route the Dockerfile ships.
- **Not re-derived:** the READY's import-grep counts; whether the 12 host-npm flag drifts (item 1) ever reached a committed lock elsewhere.
- **Linear/GitHub:** not re-read after 22:56:48 (except ls-remote at 23:11:31).

## Read before launching
1. **Queue:** per Wednesday's receipt, this gate runs after #1031 and #1032, one at a time. Re-run `launchers/launch_qa_secuura_ks763_1033.sh --check` immediately before launch.
   - Exit 18 most likely means a Dependabot root-lock PR landed, #949 (prisma 7.10.0) above all. Re-pin.
   - Exit 19 means #1033 landed.
   - Exit 10 means Seat B merged develop in again or the head moved.
2. **Nothing found means the gate should not launch as drafted.** Develop's move to `27e53ec3a` touches none of the guarded paths, and `--check` reads OK against it.
3. The gate shares the 8 GB Docker VM with any other gate running containers. The brief caps it at `--runInBand` and sequential containers.
