# DRAFTER REPORT: #1022 (KS-1211 hono ×3) tier-1 round-1 gate set, 2026-09-17 17:57–18:20 AEST

**BLUF**
- **Files:**
  - brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.md` (38.7 KB, sha256 `f71fc8ab1469f75b…`)
  - prompt: `…/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.prompt.txt` (9.3 KB, `0c90b73553a26d86…`; under the #1019r2 ceiling of 19.8 KB)
  - launcher: `…/launchers/launch_qa_secuura_ks1211_1022.sh` (`035bc84f85dbf909…`), from `gen_launcher_1022.py`. Template: the #1020 tier-2 launcher. 24 asserted substitutions (including `TIER 2` → `TIER 1`), 70 output controls, `#1022` enumerated at 12 first, residual guard clean, `bash -n` rc 0 (`gen_launcher.out` 18:15:52). The first enumerate refused on my own wording ("the #1020 merge" tripped the residual guard) and wrote nothing (`gen_launcher.enumerate.first-run-…out`).
- **`--check` 18:15:52 (`check.out`): rc 0.** The develop arm judged 18 blobs = base, and origin develop was still `581c9db0d` = the #1019 squash (not the PR parent).
- **Negative controls, `--check` only (`controls_check.out`, 18:16–18:19):** each exited with its expected code, ALL PASS.
  - head override: 6
  - brief without the full SHA: 20
  - brief without TIER 1: 7
  - prompt without MAIL: 12
  - prompt without the push/preflight ban: 11
  - prompt without ROUND 1: 15
- **Verdict subject in the brief and prompt:** `[QA -> Wednesday] TIER 1 GATE #1022 (KS-1211) 58684e653 — <GO | GO WITH FINDINGS | NO GO>`, sent from coagent@ to wednesday-agent@. Time-box: 40 min.
- **Origin did not move.** ls-remote at 17:57:05, 17:58:35, 18:11:01 and 18:19:51 read `refs/pull/1022/head` = `58684e653` and develop = `581c9db0d`.

## Launcher design (what is new against the #1020 / #1021 launchers)
- **Compare assert:** `f8c7aaa39 ahead=1 files=4`. `behind` is not asserted; it is 1 today because develop has #1019.
- **`DEVELOP_SHA` is `581c9db0d`, which is not the PR parent.** The OK line says so.
- **JUDGED covers 18 blobs:**
  - the 4 PR files, each with its own-blob mapped to LANDED, exit 19;
  - the Dev, mcp-server and originate `package.json`;
  - audit-gate, audit-locks, lock-discovery and baseline-contract;
  - `scripts/audit/package.json`, `preflight.sh`, `lockfile-cleanroom.sh`;
  - both service Dockerfiles;
  - **mcp-server `src/http-server.ts` and `src/index.ts`**, because the runtime-reach prediction rests on them.
- **GUARDED prefixes:** `scripts/audit/`, `scripts/preflight/`, `services/mcp-server/`, the Dev `package.json` and root lock, the originate `package.json`, lock and Dockerfile, and `.githooks/pre-push`. DEV_CONTENT_ALLOWED is empty.
- **#1021 landing first makes this launcher exit 18, by design.** The second PR has to merge develop in and gets a new head, so the gate would be about a different SHA.

## Wednesday's six lead questions: what the drafter measured
**1. Runtime reach. The premise is false at source, and the answer is measured.**
- **What the service wires:**
  - `src/index.ts` connects `StdioServerTransport`.
  - `src/http-server.ts` is plain express and imports no SDK module.
  - The image runs `CMD ["node", "dist/http-server.js"]`.
  - No mcp-server source imports `streamableHttp`, `sse`, `hono` or `@hono/*`.
- **Inside SDK 1.29.0:** only `server/streamableHttp.js` touches the hono family. It imports `@hono/node-server`, whose index does not import `hono`.
- **Install shape.** The first install was wrong: `npm ci` inside `services/mcp-server` silently installed from the workspace ROOT lock. It is quarantined by rename and carried as method lesson 2. The corrected install is Dockerfile-shaped and outside the workspace, in `img-<tree>/{shared,build,prod}`: every `npm ci` rc 0, lock sha unchanged, build rc 0. The runtime stage has hono 4.13.8 at head and 4.13.0 at base.
- **The three probes, each with a per-process `module.registerHooks` census, base and head (`runtime/run_runtime.out` 18:07):**

  | probe | what it drives | hono resolutions | other census counts | base vs head |
  |---|---|---|---|---|
  | A | stdio `dist/index.js` via the SDK `Client`: initialize, `tools/list` (9), hash tool call, fail-closed tool call, unknown tool, bad argument | **0** | — | identical |
  | B | image CMD `dist/http-server.js` on 127.0.0.1:0 (loopback-pin preload), 7 HTTP routes | **0** | express 28 | identical; ended by pid (SIGTERM) |
  | C | SDK `StreamableHTTPServerTransport` with the real tools (**not shipped**) | **0** | `@hono/node-server` 1 | identical |

  The control `import('hono')` on probe C's census counted hono 39 at base and 43 at head.
- **The advisory behaviour on the shipped bytes (`runtime/run_hono_advisory.out`):**
  - crvj: `?a=1` placed after `#` is read as `"1"` on 4.13.0 and as null on 4.13.8, both through `getQueryParam` and through `@hono/node-server`. The control is unchanged.
  - g6gw: `parseBody` on a depth-5000 dotted key returns 200 on 4.13.0 and `Nesting limit exceeded` on 4.13.8. The depth-3 control returns 200 on both.
  - gqvv (`toSSG`) was not probed.
- **originate (`drafter_originate_omit.out`, `runtime/run_prisma_census.out`):**
  - Its runtime `npm ci --omit=dev` **installs hono 4.13.8** (devOptional); the dev-only control packages are absent. **hono ships in two images, not one.**
  - Reach: 0 files under originate `src` import it. Only `@prisma/dev` imports hono, reached only by the `prisma dev` CLI.
  - Census: `prisma --version` and `prisma migrate --help` resolve hono 0 times.
- **What I could not predict:**
  - originate's own `dist/index.js` start under the census (needs a generated prisma client and a database URL);
  - a CJS positive control on the census;
  - a mid-run LISTEN census. The lsof census read 0 node listeners at start and end, but there was no mid-run positive control.

**2. The advisories are gone (`drafter_audit.out` 18:08:47–18:09:00; raw output in `out/`).**
- **H1** (head, its own baseline): gate rc 0, 33 reported / 35 baselined, 0 CLEANUP. Locks rc 0, 43 scanned.
- **H2** (head with develop's baseline): gate rc 0, with CLEANUP listing exactly the 3 hono rows. Locks rc 0, no CLEANUP.
- **B0** (base, its own baseline): gate and locks both rc 0; the gate reports 36 / 38.
- **B1** (base with head's baseline): gate rc 1 and locks rc 1. Each names exactly the 3, pinned at 4.13.0 in mcp-server and originate.
- **Advisory data:**
  - `npm audit --json` gives each `via.range` as `<4.13.5`, moderate.
  - The same bulk URL that `audit-locks` uses returns `<4.13.5` ×3. Shipped semver: 4.13.0 is in range, 4.13.8 is not.
  - 4.13.8 is inside `^4.11.4`, `^4.12.8` and `^4`; the 5.0.0 control is outside.
  - I re-POSTed from a scratch script. The brief tells the gate to tee the in-process response instead.
- **Severity is moderate on every feed.** The "HIGH" worry in Seat B's brief came from reason text about Kam's authority, not from the advisories.

**3. Scope by parse (`drafter_parse.out`).**
- Each lock moves only `node_modules/hono` (version, resolved, integrity).
- **Service locks:** 0 other changes. The planted-version control detected 1.
- **Root lock:** exactly the 12 ruled entries, all flag-only, 0 version fields. The planted control (an unruled dev flip plus a version change) counted 2 "other".
- 0 manifests.
- **Baseline:** 38 → 35, exactly the 3 hono rows removed, 0 added, 0 altered. The planted-alteration control detected 1.

**4. Clean-room and builds (`drafter_cleanroom.out`).**
- `lockfile-cleanroom.sh services/originate services/mcp-server`: head rc 0 (2/2), base rc 0.
- Control: `zod ^9.0.0` planted in mcp-server gave rc 1 FAIL mcp-server; restored sha-identical.
- mcp-server tsc build rc 0 on head and base.
- **Not measured:** originate build and jest vs base, shared 851, and mcp-server's placeholder vitest. The seat's figures are relayed only.

**5. Merge (`drafter_setup.out`).**
- `merge-tree 581c9db0d 58684e653` = **`b475cfbe1`**, the same as the seat's tree. It differs from head by #1019's 3 files and from develop by the 4 PR files.
- **Overlap with #1021.** With either PR squashed first (scratch `commit-tree`), merging the other is clean. **Both orders give tree `1b03e6951`**, whose baseline has 34 rows (the 3 hono rows and colord removed). The hono rows are the last 3 entries of `accepted`, so the hunks are not adjacent. "The second PR re-measures" is a process rule, not a conflict.

**6. linkKind (`api_read.out` 17:57:27).**
- `attachmentsForURL(pull/1022)` = KS-1211 `contributes`, open; `completedAt` null. Control pull/99999 = 0.
- 0 closing phrases in title, body, commit and comment; the planted controls hit.
- KS-1211 is In Progress, with #1021 and #1022 both `contributes`.
- `SKILL.md:526` §5f text confirmed at develop. The brief tells the gate to keep KS-1211 In Progress, to rule whether a shipped-but-unloaded dependency counts as a §5f runtime change, and to name originate beside mcp-server in the sweep owed.

## Where the READY disagrees with what I measured (all RECORD-class predictions, carried in the brief)
1. **"hono ships at runtime … prod in mcp-server":** it ships but is never loaded, not even by the SDK HTTP transport. Seat B's wording "via @modelcontextprotocol/sdk" is right about the dependency and silent on load.
2. **"devOptional in originate":** that is right about the flag, but `--omit=dev` keeps devOptional, so hono ships in the originate image too.
3. **The seat and Wednesday's lead question both assume mcp-server uses the SDK HTTP transport.** At source it does not.

## Wednesday must read before launching
- **The lead question's premise is false** (point 3 above). The brief keeps the runtime item but reframes it: prove non-load with controls, then exercise 4.13.8 directly on the advisories. If Wednesday wanted the gate to drive an HTTP MCP endpoint the service actually exposes, there is none. Probe (c) is labelled NOT shipped.
- **The §5f sweep owed should name originate as well as mcp-server.** Whether an unloaded dependency counts as a runtime-behaviour change is left for the gate to rule.
- **#1021 landing first makes this launcher refuse (exit 18).** That is intended.
- **The launcher's `--check` makes 18 GitHub contents GETs and takes about 35 s.**

## Holds I came near
- **Network call.** `prisma dev --help` fetched from the network ("Fetching latest updates…"). I ran it once, and only as a census probe, before noticing; nothing was written outside scratch. It is carried as method lesson 5, with "never run `prisma dev`" in the bounds.
- **The wrong install:**
  - `npm ci` in the member dir wrote `node_modules` into my scratch worktree's workspace root. I quarantined both dirs by rename; nothing was deleted.
  - As a result, `git status` in `wt-head` and `wt-base` shows 2 untracked quarantine dirs each. That is scratch only.
- **Probe C hung** on an SSE stream. The runner killed it at 120 s, and I verified with pgrep that no process was left. The hung run's outputs are quarantined by rename.
- **Clean boundaries:**
  - **Secuura checkout** (read-only git only): porcelain 0 at 17:58:35 and at 18:19:51. `.git/config` sha256 `d7e7298b02c45f52…` both times. `.git/worktrees` 112 → 112. Refs 923 → 925, which is other sessions fetching; I never fetched.
  - No docker, no stack, no push. No Linear or GitHub writes. No mail sent.
  - Every listener bound 127.0.0.1:0 and was closed or SIGTERMed by its own pid. At the end: 0 node listeners and 0 `login_stub.mjs` processes; pgrep for my probe names rc 1.
  - The launcher was run only with `--check`.
- **Scratch:** `/private/tmp/claude-501/drafter1022/clone-rew8njcr/` (the clone, `wt-{head,base,develop}`, `img-{head,base}`, `orig-omitdev`).
