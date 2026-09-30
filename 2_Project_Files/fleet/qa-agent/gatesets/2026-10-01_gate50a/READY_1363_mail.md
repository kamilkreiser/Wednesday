# [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 51st): #1363 (KS-1378) in-range lock refresh - legs 6+7+contract rc 0 at head, 13/13 cleared, 0 baseline rows touched, push rc 0 under lock-46; the gatelines VERDICT wording is a hazard; NEW ticket text attached UNFILED

# READY FOR QA (Seat B 51st): #1363 (KS-1378) — in-range lock refresh clears the 13 advisories that froze every push

## BLUF
**#1363 is up and the claim is met: legs 6, 7 and `audit:contract` are all rc 0 at head, where 6 and 7 were both rc 1 at develop. 13/13 advisories gone. No baseline row added, removed or changed.** This is the PR that unfreezes pushes on this repo for everyone, Peter included. **Nothing filed, nothing posted.** Please read my ctx.

## THE PR
- **#1363**, `https://github.com/Secuura/Distributed_Secuura/pull/1363`
- **HEAD read from origin in the same action as this mail (2026-09-30T21:21:14Z): `9e84e1fabafe1ecc1963953051759c4038f88db2`**
- base `develop`, state open, `mergeable_state: unstable`
- **4 changed files, +19/−19**, read back from the API: `frontend/admin/package-lock.json` +4/−4,
  `frontend/verifier/package-lock.json` +4/−4, `package-lock.json` +7/−7,
  `services/kyc/package-lock.json` +4/−4. **No manifest. Nothing that is not a lock.**
- Branch `feature/ks-1378-in-range-lock-refresh-axios-1-20-0-dompurify-3-4-16-b51-a`, reads **MINE**
  on `namecheck46` with three real-ref controls going the other way.
- Declared title **75 chars**; landed as written.
- PR body sha256 `d366bcab3f0045c8`, written by me, carrying the Test Evidence block.

## THE PUSH — one push, under `.push-lock-46`
- `origin heads for this branch: 0 (first push requires 0)` → satisfied.
- `LOCK TAKEN by Secuura/Blockchain b51 pid 84336` 21:08:16Z → `push rc=0` 21:14:42Z →
  `LOCK RELEASED by Secuura/Blockchain b51 pid 84336`. Released with the pid the **holder file**
  recorded. Cool-off stamp written.
- `ls-remote` after the push: `9e84e1fabafe1ecc1963953051759c4038f88db2` on my branch, one ref.
- `my own orphaned login_stub pids (cwd under .../s-b51-itemA): 0`.

**Preflight, quoted exactly as the hook prints it:**
```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
shell suites: 67 passed, 0 failed, 0 skipped (of 67)
OK — 13 code guards passed.
```
**Which three skipped: the hook does not say, by design.** `.githooks/pre-push:273` calls them
"the stack-dependent legs (the ones the preflight verdict lists as SKIPPED when the stack is down —
KS-1046; **not enumerated here, an enumeration drifts**)". The cause is the local stack being down,
which is expected: this round starts no stack, by your own hold. So I quote the ratio and name the
cause, and I do **not** invent the three leg names.

**Gate lines, and a WORDING HAZARD you should know about:**
```
  pre_push_hook_base.test.sh                   (28, 0)  OK
  pre_push_hook_base_fixture_guard.test.sh     (6, 0)  OK
  run_shell_suites.test.sh                     (49, 0)  OK
  VERDICT: MATCHES the declared fleet STOP condition
```
🔴 **That VERDICT line is the CLEAN one, and it reads like the opposite.** I did not take rc 0 as the
answer; I traced the string. It is not in the repo, the hooks or the scripts — it is emitted by
`gatelines46.py:57`, whose three states are `MATCHES the declared fleet STOP condition` (the counts
match the declared-good 28/0, 6/0, 49/0 → **good**), `NOT APPLICABLE (format gate only)`, and
`MISMATCH — STOP` (**the bad one**). So "MATCHES … STOP condition" means "matches the predicate the
fleet declared for deciding STOP", not "a STOP fired".
**Recommend re-wording it in the next generation.** That file's own comment at `:50` warns that a
wrong STOP "would let a seat learn to ignore the word STOP" — and this phrasing is the other half of
that risk: a seat skimming a clean push sees the word STOP and either halts for nothing or, worse,
stops reading the word. `FIXTURE BUILD FAILED` count: **0**.

## THE CLAIM, MEASURED
| leg | at develop `4f18c59a89db` | at head `9e84e1fabafe` |
|---|---|---|
| 6 `audit:gate` | rc **1** — `24 distinct advisories reported, 26 baselined` + FAIL 13 NEW | rc **0** — `11 … reported, 26 baselined` |
| 7 `audit:locks` | rc **1** — `18 advisories match, 6 already baselined` + FAIL 12 | rc **0** — `6 match, 6 already baselined` |
| `audit:contract` | rc **0**, 59 pass | rc **0**, 59 pass 0 fail |

**26 baselined before, 26 after.** The word `FAIL` is absent from both AFTER logs and present in the
BEFORE log, so the check that looks for it can find it.

## THE 13 → THE LOCK ENTRY THAT CLEARED EACH, so the gate can re-derive the set one to one
All thirteen: `before L6=True`, `after L6=False, L7=False`. **13/13.**

**axios → 1.20.0** in `package-lock.json` (root), `frontend/admin`, `frontend/verifier`,
`services/kyc` — all four from **1.18.1**:
| advisory | sev |
|---|---|
| `GHSA-c29m-xwm3-cm6r` | high |
| `GHSA-mghh-pgcx-3jjj` | high |
| `GHSA-x97p-jq2g-jp4f` | high |
| `GHSA-3pq3-5fj3-cg6v` | high |
| `GHSA-542g-h47m-68v8` | high |
| `GHSA-m8m8-qj5v-23w3` | high |
| `GHSA-r4gj-5m52-g5wh` | high |
| `GHSA-vh66-26gq-q6x8` | moderate |
| `GHSA-9fr6-4gfg-395g` | moderate |
| `GHSA-j8rh-479h-cp32` | moderate |
| `GHSA-4hqw-qxg8-jxx2` | moderate |
| `GHSA-44g4-m2mj-wpvx` | moderate |

**dompurify → 3.4.16** in `package-lock.json` (root) **only**, from **3.4.13**:
`GHSA-p98j-92pf-mc4p` (low). Its BEFORE reading was **L6=True, L7=False** — the asymmetry I
predicted from the pin census before running anything.

**Positive control:** leg 6 at head still names **15** distinct ids (the grandfathered residue), and
three were re-tested present by the same matcher. The 13 absences are absences, not a dead matcher.

## HOW THE MOVES WERE PROVED
- `refresh46.sh`, containerised `node:24-alpine`, **npm 11.19.0** — never host npm, because host npm
  has left an in-range `--package-lock-only` update INERT on this repo before (rc 0, nothing moved).
- Every move by `cmp` **plus a JSON lock parse**, never the `up to date` banner.
- **4 locks moved, 0 INERT, 0 skipped.** **0 lock entries ADDED or REMOVED in any lock:** root
  1968→1968 with 2 version moves; admin 329→329, verifier 308→308, kyc 262→262, 1 each.
- **Pristine control** `s-b51-itemActl` at the same base: still byte-identical at all four locks
  (`854f3a8b42ebd65f`, `36fcc79f8ccb9731`, `81dcee26401ef14c`, `bd0588ac8a0e5d2c`), `git status`
  **0 lines**, installed tree carrying the OLD axios 1.18.1 / dompurify 3.4.13. So "moved" is measured
  against a real before.
- Installed proof the lock took: root `node_modules/axios` **1.20.0**, `node_modules/dompurify`
  **3.4.16**.

## SUITES AND IMAGES
- `services/kyc` (`vitest run`): **rc 0, 6/6 files, 33/33 tests** — and **identically** in the
  pristine control with the OLD axios. No regression from the bump.
- `packages/shared` `npm run build` rc 0, `dist` 28 entries, both trees.
- Images, `docker compose -p b51probe build kyc admin-frontend verifier-frontend issuer-frontend`
  **rc 0**, all four, bounded as you approved (detached worktree, `-p b51probe`, build only; no
  `up`/`down`/`--rmi`/prune; **0 containers started**).
  🔴 **I checked what the builds actually did rather than accept four "Built" lines.** Only
  `b51probe-kyc` carried a new image ID; the three frontends showed older creation dates, which looks
  like a stale cache. It is not: `admin-frontend` and `verifier-frontend` genuinely **re-ran
  `npm ci` (5.8 s and 5.4 s)** because the changed lock busted their
  `COPY frontend/*/package*.json` layer, and `kyc` re-ran both stages. The final images are
  bit-identical because axios is imported by **zero** source files in admin and verifier and the
  nginx stage keeps only `dist/` (a `find` for an axios directory in the final images returns
  nothing), so Docker reuses the identical image object and reports its original date.
  `issuer-frontend` was correctly **CACHED** — its own lock never changed.
  `docker system df`: images 144 → **148**, build cache 1071 → **1093** (105.8 → 107.2 GB),
  containers 0 → **0**.

## NOT COVERED
- **No suite for the three frontends: they declare no `test` script at all** (`frontend/admin`,
  `frontend/verifier`, `frontend/issuer`). That is **KS 1391**, open. "Suites before and after" is
  **vacuous by construction** for them and I claim no pass.
- 🔴 **Nothing tests `frontend/issuer/src/utils/sanitize.ts`, the ONLY dompurify consumer.** Searched
  `frontend/`, `services/` and `packages/` for a spec naming sanitize or dompurify; the five hits are
  api-gateway, originate and shared tests, none of them issuer's. **The dompurify half of this PR is
  untested** and rests on the advisory's own patched range plus your gate reading. I am not letting
  the axios evidence stand in for it.
- No Schemathesis, Akto, Playwright or k6 — none reads a lockfile version.
- No deploy: not kintsugi, not demo.
- The pre-existing `packages/shared` resolve failure in the kyc suite (`BACKLOG.md`) — **proved
  pre-existing**, identical in the control tree with the old axios.
- The 3 skipped preflight legs, which the hook deliberately does not enumerate.

## KS-1378's SCOPE — MEASURED, AND IT DOES NOT COVER THIS BATCH
KS-1378 is *"Five new advisories block EVERY push: bump morgan, nodemailer, ip-address and undici
(Kam ruled (a))"*, In Progress. Its **Scope** reads: *"Bump, plus a per-advisory reachability read
recorded in the PR body (FOUND / TESTED / HOW). The proof is preflight legs 6 and 7 passing on the
PR. No baseline entry, no `--no-verify`."* It names five specific advisories — nodemailer, morgan,
ip-address ×2, undici — and its body says *"No baseline entry for any of the five"*.

**My 13 are axios ×12 + dompurify ×1: a different batch.** So the **method** transfers exactly (and
I followed it, FOUND / TESTED / HOW included), and I carry `Refs KS-1378` on the branch as #1356
did — but the **scope does not cover these 13**, and the batch has **no covering ticket** on the
board (`GHSA-c29m` → 0 hits, `1.20.0` → 0 hits, positive control `ip-address` → 5).

## THE PROPOSED NEW TICKET — for gate50a to read. NOT FILED, NOT POSTED.
Saved at `5_Project_History/2026-10-01_seatB-51st/itemA/`:
**title** sha256 `2dc03e152a5dbc13`, **description** 5648 B sha256 `aba779a9cdd444e0`.

**TITLE, verbatim:**
```
Thirteen advisories published 2026-09-30 block every push: axios 1.18.1 in four locks and dompurify 3.4.13 in the workspace root
```

**DESCRIPTION, verbatim:**
```
## BLUF

**The push preflight fails legs 6 and 7 on `develop`'s own dependencies, so no push on this repo succeeds until this is triaged.** Thirteen advisories published 2026-09-30 between 15:03:21Z and 15:37:57Z are absent from `scripts/audit/audit-baseline.json`. Measured at `develop` `4f18c59a89db16cb8b06b7850aeb64e6f81f95ee`: `npm run audit:gate` and `npm run audit:locks` from `Blockchain/Dev`, **both rc 1**; `npm run audit:contract` rc 0.

**None of these is one of KS-1378's five**, and none is one of the two KS-1395 names. This is a fourth, separate batch.

## The thirteen, verbatim from the gates

Twelve are **axios**, every one with `first_patched_version` **1.20.0** (GitHub advisory API). Seven high, five moderate:

| advisory | sev | summary |
| -- | -- | -- |
| `GHSA-c29m-xwm3-cm6r` | high | ReDoS in the `fromDataURI` `data:` URL parser freezes the Node event loop |
| `GHSA-mghh-pgcx-3jjj` | high | ReDoS (O(N²)) in `shouldBypassProxy` host normalization, reachable via untrusted redirect `Location` |
| `GHSA-x97p-jq2g-jp4f` | high | Prototype pollution gadget in `toFormData` options |
| `GHSA-3pq3-5fj3-cg6v` | high | HTTP/2 adapter bypasses the configured DNS lookup and proxy controls |
| `GHSA-542g-h47m-68v8` | high | DoS via an unhandled `error` event in HTTP/2 `ClientHttp2Session` initialization |
| `GHSA-m8m8-qj5v-23w3` | high | Node HTTP adapter prototype-pollution gadget allows request socket hijack via inherited `createConnection` |
| `GHSA-r4gj-5m52-g5wh` | high | `maxRedirects: 0` is not enforced by the fetch adapter, allowing redirect-based SSRF |
| `GHSA-vh66-26gq-q6x8` | moderate | Prototype pollution gadget in the fetch adapter can alter outbound requests |
| `GHSA-9fr6-4gfg-395g` | moderate | Prototype-pollution gadget in the default instance allows an inherited `Object.prototype` method to override the HTTP method |
| `GHSA-j8rh-479h-cp32` | moderate | Header injection via inherited `headers` after a minimal interceptor |
| `GHSA-4hqw-qxg8-jxx2` | moderate | Fetch adapter header injection via inherited `FormData` `getHeaders` |
| `GHSA-44g4-m2mj-wpvx` | moderate | CIDR-form `NO_PROXY` entries are ignored, causing proxy exclusion bypass for internal IP ranges |

One is **dompurify** `GHSA-p98j-92pf-mc4p` (low): `IN_PLACE` node-removing `afterSanitize` hook leaves detached subtree event handlers armed, causing DOM XSS. Vulnerable `>= 3.4.13, <= 3.4.15`; `first_patched_version` **3.4.16**.

## Where they are pinned — measured across all 45 tracked locks, not assumed

| lock | axios | dompurify |
| -- | -- | -- |
| `Blockchain/Dev/package-lock.json` (workspace root) | **1.18.1** | **3.4.13** |
| `Blockchain/Dev/frontend/admin/package-lock.json` | **1.18.1** | — |
| `Blockchain/Dev/frontend/verifier/package-lock.json` | **1.18.1** | — |
| `Blockchain/Dev/services/kyc/package-lock.json` | **1.18.1** | — |
| `Blockchain/Dev/frontend/issuer/package-lock.json` | 1.20.0 (already patched) | 3.4.16 (already patched) |
| `Blockchain/Dev/mobile/secuura-app/package-lock.json` | 1.13.2 | — |

**Four locks need the change, not the three leg 7 names.** The workspace root lock pins both packages and is covered by leg 6, not leg 7. `mobile/secuura-app` is out of scope under KS 769 (expires 2026-10-19).

**Why leg 7 never reported the dompurify advisory:** leg 7 scans the 43 standalone locks, and the only standalone copy of dompurify is `frontend/issuer`'s, which is already at the patched 3.4.16. The vulnerable copy is in the workspace root lock, which is leg 6's. Both instruments are behaving correctly.

## The route — an in-range lock refresh, not a manifest bump

Every affected manifest already admits the patched version, so no `package.json` changes:

* `frontend/admin` declares `axios ^1.6.5`
* `frontend/verifier` declares `axios ^1.6.2`
* `services/kyc` declares `axios ^1.8.2`
* `frontend/issuer` declares `dompurify ^3.4.13` (the root lock's copy is the workspace hoist of this)

Neither package is declared at the workspace root itself.

## Reachability

* `services/kyc`: **one** source file imports `axios`. A real service path, and the image ships `node_modules`.
* `frontend/admin`: **zero** source files import `axios`. `frontend/verifier`: **zero**. Declared but unused; their final images are nginx plus the built `dist/`, and the builder stage is discarded.
* `frontend/issuer/src/utils/sanitize.ts` imports `dompurify`. **No test anywhere covers that file** — searched `frontend/`, `services/` and `packages/` for a spec naming `sanitize` or `dompurify`.

## Done means

1. Legs 6 and 7 both rc 0 at the PR head, with `audit:contract` still rc 0, and **no baseline row added, removed or changed** (26 baselined before and after).
2. Each of the thirteen advisories shown absent from both legs, against the lock entry that cleared it.
3. Every lock move proved by `cmp` plus a lock parse against a pristine control tree at the same base — never by npm's `up to date` banner, which has read as success on this repo before while nothing moved.
4. Locks regenerated containerised in `node:24-alpine`, with the container's npm version recorded.
5. The images and suites that consume the moved locks built and run.

## Not in scope

* The three frontends declare no `test` script at all, so "suites before and after" cannot be satisfied for them — that is KS 1391.
* `services/kyc`'s suite needs `packages/shared` built first, or one file fails to load with `Failed to resolve entry for package "@secuura/shared"` — already recorded in `BACKLOG.md`.
* The fourteen grandfathered dead baseline rows the leg 6 cleanup list names on every run.
```

Team KS, state Backlog, assigned to the board account, no relation or label change on any other
ticket. **Filed only on your GO naming Seat B 51st, before the merge**, with the gate's amendments;
then the squash body refs the new key. **No comment on KS-1395** — it is Stuart's. No comment on
KS-1387, KS-1380, #1360, #1361, #1362, #920 or #1129.

## RESIDUE, carried word for word
The **14** grandfathered dead rows leg 6's cleanup names on every run: *dead grandfathered rows;
removal needs the contract floor `baseline-contract.test.mjs:217` revisited; Wednesday's to propose.*
(Measured as **13 undici + `GHSA-v2v4-37r5-5v8g`**; the brief's "12 undici" is one short, total still 14.)

## HOUSEKEEPING, not acted on
**16 orphaned `login_stub` listeners** are live — 8 from `s-b26-rc-base` and 8 from
`s-b26-rc-head`, oldest etime **05-11:37:51** (≈5½ days). That is the known 4-per-push preflight
leak. **None is mine** (`push46.sh` reaped 0 under my worktree, and it reaps only by cwd), so I left
every one of them. Their removal is yours to order.

## FUSE
**194.6 h, computed at 2026-09-30T21:21:14Z**, against 2026-10-09T00:00:00Z. Four rows at develop; three once ITEM 1
merges. mwp4 is dead to BOTH legs, so removing it changes no gate verdict. I re-date nothing.

## STATE
Holding for gate50a. ITEM 1's worktree `s-b51-mwp4` is untouched at `4f18c59a89db` with its
measurement banked (the removable set is `{mwp4}`), ready to rebuild on the merged develop.
Watcher, `ps` in the same action as this sentence:
```
38865       08:02 /bin/bash ./inbox_watch46.sh 2026-09-30T21:12:31.000Z 60
```
