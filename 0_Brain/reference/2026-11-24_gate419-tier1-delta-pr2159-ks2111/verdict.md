PR 2159: GO WITH NOTES (at head 3acc187676aa58cb433228e23cb3b5211150c5f7; tier 1 delta)

# QA GATE 419 — tier 1 delta, PR 2159 (KS-2111), fix round on G301-2159-1

Gate run 2026-11-24 15:25:31 to 15:41:45 AEDT (times from `date`). Model claude-opus-5-5. Findings only: nothing was fixed, pushed, commented, merged or deployed. Evidence is under `_work/evidence/` in this folder. My own clone is `_work/repo`, with worktrees `_work/h` (the head) and `_work/d` (develop). Node v26.8.1 (not an LTS line), Apple M2. Load1 was read before each heavy suite: 2.6 to 23.2. The spike at 15:36 came from another process, not from my runs.

## BLUF

**G301-2159-1 is closed on both halves.**

- **The page.** I derived the inherited names myself: 12 on this Node, plus `prototype`, makes 13. I also planted three inherited names that the list does not hold: a function, an object and an accessor. I probed every name on four paths (stored category, form category, stored field, form field):
  - The head pollutes nothing in 67 of 67 rows.
  - Controls on the same probe: gate 301's head pollutes in 25 rows, and develop in 29.
  - A stored FIELD named `toString`, `valueOf` or any of the other 10 round-trips as an own key.
- **The gateway.** Through the real body parser on loopback, all 13 names are refused with 400 VALIDATION_ERROR. So are the four escaped spellings that decode to a refused name. In each case the counters read: 0 database calls (no SELECT either), 0 Redis reads and 0 Redis writes. The control is develop: all 13 return 200 and are stored.
- **The merge commit is clean.**
  - `--remerge-diff` shows 0 lines. My planted control (a merge commit with one extra line) shows 9.
  - `merge-tree` gives eb6dac700976 in both orders.
  - A squash onto ce0a767a3fc4 puts exactly the six paths.
- **Every regression leg matches the builder's figures:**
  - api-gateway: 187 files, 2550 of 2550 (develop: 186 files, 2531).
  - ks1231 runner: 72 of 72.
  - packages/shared: only KS-278 fails, on both arms.
  - test-types: 15 in the baseline, 0 new.
  - tsc 0; eslint unchanged.
  - 9 of the builder's mutants re-run, all killed.

**No Blocker, no Major, no Medium.** Two Low findings and three Notes follow.

## Findings

### G419-1 (Low): no cell pins that the refusal comes "before the read"
- **FOUND.** Every word claims the refusal comes before the read: the admin.ts comment, the PR body, the cheat fragment ("before anything is read, merged, stored or refreshed") and the flow fragment ("before any read"). The code does refuse before the read; I measured it. But the KS-2111 test file never asserts it: G1 counts only non-SELECT database calls and Redis writes.
- **TESTED.**
  - Mutant GX2 (mine): the whole refusal block moved to after `readPlatformSettings` and before the merge. It compiles (tsc rc 0), and the KS-2111 file stays at 19 of 19. It **survived**.
  - For contrast, the builder's GM2 (refusal moved after the write) is killed.
  - The code at the head is right: my gateway probe reads db=0 and Redis get=0 for each of the 13 names.
- **HOW.** Evidence: `_work/evidence/mutants_g419.txt` (row GX2) and `_work/evidence/gw_rows_h.txt`. Planted by anchor (count asserted 1), restored by sha256 (True), porcelain empty.
- **Effect of a regression it would miss.** A refused body would then trigger a read. If the read failed, the caller would get 503 instead of 400.
- **Fix shape.** One assertion in G1 that reads count 0 (including SELECT and `getNotificationSettings`).
- **Where.** Test lines 116 to 120 of `Blockchain/Dev/services/api-gateway/src/__tests__/ks2111-settings-put-refuses-prototype-category-names.test.ts`. Code at `routes/admin.ts:1214-1230`.

### G419-2 (Low; an existing class, now wider): a stored dotted category such as `toString.x` refuses every page save
- **FOUND.**
  - The gateway accepts a category named `toString.x`. It is an exact-name test and this is not a refused name, so the probe gets 200 and the key is stored.
  - The page then flattens that category to the form key `toString.x.f`.
  - `buildSettingsUpdate` splits at the first dot and gets the category `toString`, which is on the list, so the key is refused.
  - From then on, every Save on the Settings page is refused with "These fields cannot be changed from this page: toString.x.f". This is not pollution: it is a lockout that a platform admin can plant.
- **The same class on develop.** `integrations.x` (a read-only category) measured the same on the head. Before this round, `toString.x` polluted instead: gate 301's head row E reads YES. So the fix turns pollution into a refusal, which is the safer outcome. But the set of prefixes that lock the page grows from four names to fourteen (the 13 plus `integrations`, and arrays).
- **A PR body sentence is too broad.** "the page no longer sends a stored one, so it cannot lock a page save out" is true for the gateway's 400. It is not true for this page-side refusal.
- **TESTED.**
  - Page probe row E: `_work/evidence/page_probe_head.txt` (`ok:false`, with that message).
  - Gateway probe row "LOOK toString.x (dotted)": 200, with the key stored.
- **HOW.** The same probe on gate 301's head and on develop gives the before-state (pollution).
- **Recommendation.** LIST as a sibling, outside the closed path list. One way out is for the gateway to refuse a category name that contains a dot, or the page could split such names differently.
- **Where.** `settingsSavePayload.ts:103-117` at the head.

### G419-3 (Note): an inherited ACCESSOR planted beforehand still receives the value
- **FOUND.** The own-key test stops `??=` from finding an inherited value. But `updates[category] = {}` and `target[field] = value` still call an inherited **setter** if one was planted on Object.prototype earlier.
- **TESTED.** The probe planted `zzG419acc` as a non-enumerable accessor:
  - 4 setter calls on the head (rows A to D). No shared object was mutated.
  - The same 4 calls on develop and on gate 301's head.
- **Threat model.** This needs an Object.prototype that is already polluted, so it is outside the threat model.
- **The words.** The comment "keeps any name the list does not hold from reaching an inherited property" (`settingsSavePayload.ts:112-113`) is true for data properties only. A null-prototype accumulator would close it, but the drafter measured that option costing cell Q5. No action is needed beyond knowing this.

### G419-4 (Note, words)
1. **The flow fragment miscounts.** It says "every other name Object.prototype inherits (toString, hasOwnProperty, valueOf and nine more)". There are 10 such names, so it should read "seven more".
2. **The PR title still names only three names.** It reads "...refuse a category named __proto__, constructor or prototype". A squash usually takes the title as the commit subject on develop, so develop's log would understate the change. The K merge seat should set the squash subject.
3. **The PR body contradicts itself.** Its "Touched: six paths, one commit" conflicts with its own two-commit account. The squash makes it one commit later.

Every other sentence I checked holds:
- The corrected code comments: the page's lines 110-113 and 122-124, and admin.ts lines 1214-1222.
- The test header: it no longer says tenant admins can plant today; it places that in the past and states that the PUT is platform-only since KS-2314.
- The fragments' figures: 39 and 72; 22 of 24; 29 of 33; 15 and 11 of 19; 2531 and 2550; 1747/1746/1; 15 and 0; admin 57, gateway 31.
- G301-2159-2's sentence is gone. The replacement ("Q1 to Q5 (with Q1b), Q7 and Q8 to Q11 run through leak(); Q0, Q6, Q12 plant nothing") is true by reading the file.
- The builder's correction of gate 301 (Q5 does use `leak()`) is true: at 7b54e7cbb6f0, line 473 is `const { out } = leak(...)`.
- I read the facts comment b42a29cf (KS-2111, 5717 characters) and the PR body (11128 bytes, sha1 29bb322b…) raw by urllib. Neither claims anything I could not reproduce, with two exceptions:
  - B arm "187 files, 2538": I did not run arm B whole.
  - "8 planted conflicts rc 1": I ran one planted remerge control, not the 8.

### G419-5 (Note, declared gate faults; no effect on any figure)
- **(a) A vitest run in the wrong directory.** My first gateway probe used `npm --prefix … exec -- vitest`, which ran vitest with root `/Volumes/DevMASTER/WEDNESDAY` (the wrong-cwd trap). It created `/Volumes/DevMASTER/WEDNESDAY/node_modules/.vite/vitest/<hash>/results.json` at 15:33.
  - I MOVED it (no rm) at 15:34:16 to `_work/quarantine_wrongcwd/WEDNESDAY_root_node_modules`.
  - A second copy of that run was stopped. It had started scanning the WEDNESDAY tree; no vitest process remained (checked with ps).
  - Every later run used `npm --prefix <pkg> run test`, with the vitest root printed in each output.
- **(b) One unlocked git status.** I ran one `git -C …/worktrees/s-w76-fix status --porcelain` without `GIT_OPTIONAL_LOCKS=0`. It is a read verb, the output was empty, but it may have refreshed that tree's index stat cache.
- **Donor check.** Every package.json and lock file was blob-checked against the head before the donor installs were cloned (cp -c) into my own trees: 97 of 97 equal. The planted one-byte control differed (ff1da2f2… vs 1ae1908f…).

## FOUND / TESTED / HOW by commission question

**1. Page closure.** Probe: `_work/probe/page_probe.mts`. It snapshots the own keys of Object.prototype, Object, Function.prototype, Array.prototype and String.prototype, and the own keys of every function on them, before and after each row. A mark cleanup between rows stops one row from masking the next.
- Names covered: the 13, plus the three planted ones (non-enumerable function, object and accessor), plus 3 dotted rows. That is 67 rows.
- Head: 0 polluted.
- Controls with the same probe:
  - Gate 301's head (7b54e7cbb6f0): 25 polluted, which is the 10 new names on rows A and B, the planted function and object on rows A and B, and E `toString.x`.
  - Develop: 29 polluted.
- Field path:
  - A stored field named any of the 10 inherited names, or a planted name, comes back as an OWN key of `general`, and `general`'s prototype is Object.prototype.
  - `__proto__`, `constructor` and `prototype` as fields are skipped on load and refused on save.
- The repo's own runner, at the head: 72 of 72.
  - Red-first with `SETTINGS_PAYLOAD_TS` set to gate 301's module: 50 pass, 22 fail (Q8×10, Q9×10, Q10, Q12).
  - With develop's module: 43 pass, 29 fail.
  - Develop's own runner: 39.
- `Settings.tsx` line 59 (a computed key spread into a fresh object) and lines 90 and 93 (reads) were read: no other writer.

**2. Gateway closure.** Probe: `_work/probe/g419_gateway_probe.test.ts`, run in my tree and then moved out. It uses the real router and the real `boundedJson` body parser on a 127.0.0.1 socket, with raw wire text. Results are in `_work/evidence/gw_rows_{h,d}.txt`.

| Input (raw wire text) | Head | Develop (control) |
|---|---|---|
| Each of the 13 names | 400 VALIDATION_ERROR, message names it; db 0, Redis get 0, Redis set 0 | 200, stored |
| `toString`, `__proto__`, `constructor`, `hasOwnProperty` | 400, decoded name in the message | 200 |
| Duplicate `toString` key | 400 | (not given) |
| `toString` together with an invalid integrations entry | 400 naming `toString` (refused before KS-1230) | KS-1230's message |
| `ToString`, `tostring`, `"toString "`, Cyrillic і, fullwidth ｔ, a zero-width suffix, `toStringify`, `toString.x` | 200 and stored, as the code says (exact name) | (not given) |
| `toString\u0000` | 400 from the control-byte guard, nothing stored | (not given) |
| Nested `general.{toString, valueOf, __proto__, constructor:{prototype:{…}}}` | 200 and stored (the stated narrowing) | (not given) |

- After the nested run, the server is not polluted: `({}).g419polluted` is undefined and `Object.prototype.toString.call` is still a function. The merge spreads top-level own keys only, with no deep merge.
- I searched the readers (`readPlatformSettings`, verification.ts, health.ts, redis.ts) and found no deep merge.
- An array body and a `text/plain` body give 200 (pre-existing behaviour, not this PR's).

**3. Admin build.**
- `tsc -p frontend/admin/tsconfig.json --noEmit` (tsc 5.9.3) gives rc 0 on both the head and develop.
- Control: a planted `Object.hasOwn` on line 125 gives rc 2 with `TS2550`. Restored by sha256.

**4. Regressions.**

| Leg | Head | Develop |
|---|---|---|
| api-gateway vitest whole | 187 files, 2550/2550 | 186 files, 2531/2531 |
| packages/shared whole | 1746/1747, 1 failure: KS-278 "accepts a valid wallet signature over the message" | same |
| check:test-types api-gateway | 15 in the baseline, 0 new | 15 in the baseline, 0 new |
| gateway tsc | rc 0 | rc 0 |

- **eslint per changed file:**
  - Module: 0/0 on both arms.
  - admin.ts: 16 `no-unused-vars` warnings on both arms.
  - ks2111 test: 0/0.
  - Cells `.mts`: IGNORED by the repo config on both arms. No gate lints this file.
  - Package totals: admin 57 and gateway 31 on both arms.
  - Control: a planted unused const gives +1 warning.
- **The builder's mutants re-run: 9 of 22**: PM1, PM2, PM4, PM5, PM6b, GM1, GM3, GM4, plus the GM2-class check through my GX2. All 8 sampled builder mutants were killed by the named cells.
- **My own mutants:**
  - PX1 (flatten uses the three-name set): killed by Q8×10.
  - PX2 (`category in updates`): killed by Q10.
  - PX3 (`toString` dropped from the list): killed by Q12, Q8 and Q9.
  - GX1 (`body[name] !== undefined`): killed by G1 and G4/G5-class.
  - GX2 survived (see G419-1).
- **Gateway red-first:** the head's KS-2111 file against develop's handler fails 15 of 19. Against gate 301's handler merged on develop (tree 74d51a7f1756) it fails 11 of 19 (G1×10, G7b).

**5. The merge commit.**
- 3acc187676aa has parents 93f729141c82 and ce0a767a3fc4, and tree eb6dac700976.
- `merge-tree --write-tree` gives eb6dac700976 in both orders (rc 0).
- `show --remerge-diff` shows 0 lines. My planted evil-merge control (commit 2bbd8d3d, in my clone only) shows 9 lines, including the planted one.
- develop..head is exactly the six paths. The merge-base of the head and develop is ce0a767a3fc4, so a squash adds exactly those six.
- Develop changed only `settingsSavePayload.ts` and `admin.ts` of the six since base 0115269abd11.
- At 15:41:18 ls-remote read develop = ce0a767a3fc4 and pull/2159/head = 3acc187676aa (unmoved).

**6. Words.** See G419-4.

## Closure table (name × page category / page field / gateway), measured at the head

| Name | Page: stored or form CATEGORY | Page: stored or form FIELD | Gateway PUT category |
|---|---|---|---|
| `__proto__`, `constructor`, `prototype` | skipped / refused, no pollution | skipped / refused | 400, nothing read or stored |
| `__defineGetter__`, `__defineSetter__`, `__lookupGetter__`, `__lookupSetter__`, `hasOwnProperty`, `isPrototypeOf`, `propertyIsEnumerable`, `toLocaleString`, `toString`, `valueOf` | skipped / refused, no pollution | round-trips as an OWN key, no pollution | 400, nothing read or stored |
| Planted inherited function or object (not on the list) | grouped into an OWN key, no pollution (the own-check) | own key, no pollution | 200 (not listed; harmless on the server) |
| Planted inherited accessor | the setter receives the value (G419-3; needs prior pollution) | the setter receives the value | n/a |
| Dotted `toString.x` | every page save refused (G419-2) | n/a | 200, stored |
| Nested field of any name | n/a | as the FIELD column | 200, stored (stated narrowing) |

## NOT TESTED (by anyone)
- A browser run of the real Settings page, and other engines (Firefox, Safari) whose Object.prototype may differ. The own-check covers extra names, and Q12 compares against Node only.
- A real gateway, then Redis, then a database. Every PUT ran against recording stubs.
- Live stored records, and whether any of them already holds a refused or dotted category.
- An LTS Node (everything ran on v26.8.1).
- The `frontend/admin/src/__tests__` runner. The repository names none: the admin package.json has dev, build, preview and lint only, and there is no vitest config there. So the KS-2314 Settings page test was not run.
- The pre-push hook legs 3, 4 and 8 (the builder's hook skipped them), Schemathesis, Akto, Playwright and k6.
- Things I did not run myself:
  - Arm B whole suites (the 2538 claim).
  - The builder's 8 planted merge conflicts (I ran one remerge control).
  - The remaining 13 of the 22 builder mutants.
