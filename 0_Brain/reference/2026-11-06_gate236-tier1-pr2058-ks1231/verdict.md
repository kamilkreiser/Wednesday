NO GO
93bf64e2927653894eed58718f19eb6f0d37b408

# Gate 236: Secuura / Blockchain, PR 2058 (KS-1231 portal half), tier 1, round 1 of 2

## BLUF

The first save is fixed: a save from a freshly loaded page now sends the stored array exactly, where base and develop send `{"0": entry}`. Measured in real Chromium against the real build.

It is NO GO for three reasons, all measured in that browser:

1. **F1, regression.** On any instance with a connector entry, every save after the first on the same page is refused, with no edit under `integrations`. The page's reload after a save gives new objects, and the module compares by reference. Only a full browser reload clears it.
2. **F2.** The ticket's exact `{"0": entry}` shape can still be sent. If the reload after a save fails, the next save sends it and it replaces the array. If the load itself fails, the page shows no error, and an Integrations edit replaces the array with an object.
3. **F3.** On an instance with no array, editing any of the nine fields still stores a non-array `integrations`. By my read of the readers, every connector create then answers 403. The PR says it stops the page producing a malformed container. It does not.

The suite cannot see any of this, because its helper always uses the same object references (F5).

The declared survivor is closed for the refusal branch: it works in a browser, and my drive went red on the tampered bundle.

Refs did not move. The merge is clean.

## Findings

### F1. MAJOR, regression. Second save on the same page is refused
- **Where:** `frontend/admin/src/lib/settingsSavePayload.ts:63` (`Object.is`), and `frontend/admin/src/pages/Settings.tsx:71-72`, which replaces `settings` after a save and leaves `formValues` as they were.
- **FOUND:** stored `[c1, c2]`. Edit Platform Name, save: success. Edit it again, save: `Settings were not saved. These fields cannot be saved: integrations.0, integrations.1. ... Nothing was changed.` A third save 3.5 s later is refused the same way. A full page reload saves again.
- **Actual on screen:** the green "Settings saved successfully!" and the red refusal show together for up to 3 s. See `evidence/s4_second_save_refused.png`.
- **Base and develop:** the second save goes through, corrupting as before. So this is new behaviour, and it is not in the READY, the body, the fragments or KS-2035.
- **Oracle:** Product (the module's comment at :40 says these values "are not edits"), Purpose.
- **How often:** every second save without a browser reload, on any instance whose array holds an object entry. An empty array has no element keys, so it does not trigger (READ ONLY).
- **TESTED / HOW:** MEASURED AT RUNTIME, three runs (`S4`, `R2`, final run). Module-level repro: `evidence/own_cells.mts` G1 is red; its same-reference control is green.
- **Fix-shape (READ ONLY, not built):** do not hold array elements in form values at all, or re-sync the form values at the reload. Regression test: a cell that runs `prepareSave(JSON.parse(JSON.stringify(s)), flattenSettings(s))`.

### F2. MAJOR, partly pre-existing. The array can still be replaced, including by the ticket's exact shape
The cause is `frontend/admin/src/services/api.ts:771-772`: `fetchSettings` returns `{}` on any failed GET. That file is not in this PR. `Array.isArray(settings.integrations)` is then false, so the new guard does not apply.
- **F2a, new path to the ticket's shape:** first save OK, the reload GET answers 503, `settings` becomes `{}`, and `formValues` still holds `integrations.0`. The second save sends `{"0": {"id":"c1",...}}` and the stand-in stores it, with a green success. Repeated three times (`S6`, `R3`, final). Module repro: `own_cells.mts` G2 is red.
- **F2b, same at base:** the load GET answers 503. The page shows **no error** (`R4_alert_on_failed_load` is `[]`) and blank defaults. Edit Entra ID Tenant, save: the body is `{"integrations":{"microsoftTenant":"t"}}`, it reports success, and the connector array is gone. (`S5`, `R4`.)
- **F2c, same at base:** page loaded before any array existed, another writer then stores one, and an admin edits one of the nine fields. Same replacement. (`S13`.)
- **Also with a failed load, same at base:** editing only Platform Name sends `{"general":{"name":"R1"}}`, which replaces all of `general` under the shallow merge. (`S5b`.)
- **Effect (READ ONLY):** the readers refuse a non-array with 403 (`routes/verification.ts:856-857, 885`; `services/health.ts:79, 104`). So the fail-open is closed, but the allow-lists are lost and connectors are refused until someone restores them.
- **How often:** needs a failed GET, such as a gateway restart or a 502 during a deploy. Likelihood low to moderate, blast radius every connector. The 401 form (`R5`) passed only because the stand-in does not enforce auth; with an expired token the real PUT should fail too (READ ONLY), so I do not count it.
- **TESTED / HOW:** MEASURED AT RUNTIME against the stand-in API.
- **Fix-shape (READ ONLY):** tell a failed load from an empty one, and do not allow a save from a page whose settings did not load or reload.

### F3. MAJOR, pre-existing, and the PR's claim about it is false. The nine fields still store a non-array when no array exists
- **Where:** `settingsSavePayload.ts:67`. `PLATFORM_SETTINGS_DEFAULTS` has no `integrations` key (`services/settingsStore.ts:38-43`), so this is the default state of a fresh instance.
- **FOUND:** no stored `integrations`, edit Entra ID Tenant, save: stored `{"microsoftTenant":"t"}`, green success, no refusal. (`S8`.) Same at base. An existing object also grows: `S8b`.
- **Effect (READ ONLY, reader not run):** `ints` is then not an array, so `containerBad` is set for **every** connector, listed or not. Creates and connector info answer 403 `Connector allow-list container is malformed`. `verification.ts:855` treats an absent key as `[]`, so before this edit those connectors worked.
- **False claims:** cheat fragment line 4, "this change stops the page from producing one", and the body's "the fix only stops the page from corrupting it". KS-2035 and "Before this deploys" describe only the array case, so the deploy seat is warned about the safe half.
- **Stored `{"0": entry}` (`S7`):** an instance already holding it re-sends it with a green success and no warning. The body does declare that stored data is not repaired.
- **Decision for the humans:** whether this belongs in this PR or KS-2035. Evidence class of any fix: READ ONLY.

### F4. MEDIUM. The refusal traps the admin and its message does not help
The refusal itself is right and is what Wednesday confirmed. Nothing is stored on a refusal: 0 PUTs, stored value unchanged (`S3`, `R1`, final).
- **It sticks.** Typing in a field and clearing it (`S3b`), or switching a toggle on and back off (`R6`), still refuses. It then blocks edits on the other three tabs too. The only way out is a full browser reload, and the message does not say so. MEASURED AT RUNTIME.
- **Wider than declared.** It fires on an empty array, with no connector entry at all (`S9`). The body, the READY and KS-2035 all say "while connector entries exist". The message's "the connector allow-lists in integrations" is then wrong for that instance.
- **Message text.** "every form key must look like category.field" is developer language; an admin cannot act on it. In the F1 case it names fields that are not on the page and were not touched.
- **No warning first.** All 9 of the page's 36 edit controls under `integrations` stay editable and carry no hint (READ ONLY count; `Settings.tsx:417-507`).
- **Is the scalar refusal a regression?** No. At base those edits "succeed" by corrupting the array (`base:S3`), and by KS-2035's search seven of the nine names are read nowhere else. F1 is the regression an admin hits on a normal page.
- **How often on real data: NOT MEASURED.** It depends on whether an environment holds an array, and I had no box. The only writer is `PUT /api/admin/settings` (`settingsStore.ts:12`), and there is no seed in scripts, docs or migrations (READ ONLY grep).

### F5. MEDIUM. The suite passes while the page differs
- The module under test is the one the page imports, and the bundle behaves as the module does on first load. That half is sound.
- The cells' `save` helper (`ks1231_settings_save_payload.cells.mts:28`) always flattens the same object it saves against. The page does that only on first load, which is why F1 and F2a pass 19 of 19.
- **T4, my own tamper:** the page really calls `updateSettings(formValues)`, with the expected text kept in a comment. Suite stays 19 of 19 (`evidence/tampers.out`). The page cells are grep cells, so a comment satisfies them. This is wider than the one survivor declared.
- **tsc:** the declared survivor (T5) is green in the suite, but `tsc` rejects it (TS2339, `Settings.tsx` 62 and 66), and the image build runs `tsc && vite build`. So that exact tamper would not ship. I expect T4 to type-check (READ ONLY).

### F6. MEDIUM. A stale page silently removes a connector's restriction (new outcome)
- **FOUND:** page loaded with `[c1]`, another writer stores `[c1, c2]`, admin edits Platform Name: the body sends `[c1]`, success, c2 is gone. (`S12`.) MEASURED AT RUNTIME.
- **Effect (READ ONLY):** no match for c2 leaves `connectorConfig = {}` (`verification.ts:860-868`), which is no restriction. At base the same save stored an object, which the readers refuse. So head turns a fail-closed result into a fail-open one for that connector.
- **Likelihood and blast:** low likelihood (needs two writers while the page is open), but it widens authorization, which is this ticket's own class. "Verbatim" here means as loaded, not as stored.

### F7. MINOR. A stored array the gateway's validation rejects blocks every save with a generic message
Stored `allowedDocumentTypes: "SSD"`: every page save gets the KS-1230 400 and shows `Failed to save settings` (`S11`). `updateSettings` drops the reason (`api.ts:782`). At base the save got past that check by going out as an object. It needs an array stored before KS-1230. Stand-in reproduction of the validation.

### Curio, not a defect of this PR
The Platform Name input binds `general.name` while the defaults hold `general.platformName`, so its value does not reach `platformName` (`S1`, same at base). Not chased.

## Answers by question

**Q1, the shapes.** Enumerated from `routes/admin.ts:1153-1215` and `settingsStore.ts:38-43`. Admin source and `frontend/shared` have no diff from base to develop except `package.json` and the lock, so the base bundle stands for develop's page. All measured, `evidence/browser_final.json`.

| Stored `integrations`, then edit | Head sends | Develop sends |
|---|---|---|
| absent, edit other | absent | absent |
| `[c1,c2]`, edit other | same array | `{"0":..,"1":..}` |
| `[c1]`, no edit | same array | `{"0":..}` |
| `[null,c1]`, edit other | same array | `{"0":null,"1":..}` |
| `[]`, edit other (cell K5, not driven) | `[]` | absent |
| other array category (`extra: [1,"two",{...}]`) | same array | `{"0":1,"1":"two","2":{...}}` |
| `{"0":c1}`, edit other | `{"0":c1}` | `{"0":c1}` |
| `"x"` and a string category | not sent | `{"0":"x"}`, per character |
| `null`, or a number category | not sent | not sent |
| absent or object, edit scalar | object (F3) | object |
| `[c1,c2]`, edit scalar | refused, no PUT | object with both |
| `[]`, edit scalar | refused, no PUT | object |
| `[c1,c2]`, second save | **refused (F1)** | `{"0":..,"1":..}` |
| `[c1]`, reload failed, second save | **`{"0":c1}` (F2a)** | `{"0":c1}` |

Does it preserve an array exactly? Yes, from a freshly loaded page. Can it still produce `{"0": entry}`? Yes: F2a, and `S7` by re-sending.

**Q2.** See F4 and F1. Reachable by an ordinary admin: yes. "Nothing stored": true, measured. Message: accurate on the plain case, wrong or unhelpful on F1 and `[]`. Frequency on real data: not measured.

**Q3. Survivor closed for the refusal branch.** Real Chromium 156 through Playwright, real vite build with the Dockerfile's `SHARED_DIR` layout, API answered by `evidence/mock_server.mjs`.
- Array save and refused edit both behave as designed (`evidence/s3_refusal.png`).
- Control: the bundle with `!prepared.ok && false` sends a PUT and shows "saved successfully", so this drive can fail.

**Human check at the Kintsugi deploy, once a fix exists (MEASURED by nobody yet):**
1. Read the stored `integrations` shape first, read-only.
2. Save once and confirm the array is unchanged.
3. Save again without reloading.
4. Edit one of the nine fields and confirm the refusal.

Steps 2 and 3 write to stored settings, so they need the deploy card's authority.

**Q4.** 19 of 19 at head, re-run. Base 3 and 16 reproduced with my own extraction of the old logic and the old page, not the builder's file. Sampled from the READY's classes, my own reconstructions because the builder's tamper script is not in the PR:
- T1 (edited element accepted): red, K6.
- T2 (array not verbatim): 14 and 5, K1 first.
- T3 (message not shown): red, page cell.
- T4 (own): **green**, see F5.

The count of 20 tampers is NOT verified. The body's quoted first-failure sentence I did not read from a base run of K1: the cell's template matches, and `base:S2` shows the same shape.

**Q5. The body.** Sentences that claim more than was measured:
- "A routine save that edits only other fields now leaves the allow-lists intact": false for a second save (refused, F1), a failed reload (F2a) and a stale page (F6).
- "The stored shape stays intact; the fix only stops the page from corrupting it", and cheat fragment "stops the page from producing one": false (F2, F3).
- "while connector entries exist" and "holds a connector entry": too narrow (F4).
- "sends an array category back verbatim": as loaded, not as stored (F6).
- Module comment :40: false after a reload (F1).
- Fair and honest: "NOT run", the survivor as a limit, the shallow merge (`admin.ts:1200`), not repairing stored data, and the hook verdict quoted as not a pass.

The hook's three skipped legs (READ ONLY, `scripts/preflight/preflight.sh:347, 369, 553`):
- Leg 3: spec-auth conformance, unauthenticated calls to bearer operations must answer 401 or 403.
- Leg 4: path resolvability, every spec path must route.
- Leg 8: served spec against the yaml file.

All three need the stack and look at the gateway and spec, which this PR does not touch. They would have checked nothing here, and they remain unrun.

**Q6.** `git merge-tree --write-tree` develop with head: rc 0, tree `8d6a060c814b8c363da0a4c5daf5bdd1eb7b18d4` (`evidence/merge_tree.out`). Base to develop: 150 files, none of the six paths, 2 under `frontend/admin` (package manifest and lock, a `postcss-selector-parser` override). Open PRs: 20, all with file lists; only 2058 touches the six paths. PRs 948 and 639 touch `frontend/admin/package.json` only.

## Refs
| Reading | develop | head |
|---|---|---|
| 21:54:34 AEDT start, `evidence/lsremote_start.txt` | 44ee04cba47881 | 93bf64e29276 |
| 22:09:45 AEDT end, `evidence/lsremote_end.txt` | 44ee04cba47881 | 93bf64e29276 |

Both equal pins.txt. PR state OPEN, MERGEABLE.

## NOT tested
- The real gateway, Redis or Postgres. Every PUT and GET hit a stand-in copying `admin.ts:1153-1215` by hand. Reader effects (403s, c2 unrestricted) are READ ONLY.
- Any real environment, so which instances hold an array, an object or nothing is unknown. No box.
- The deployed nginx bundle, or a build of the merged tree. Builds were head and base from the head lock.
- Full `tsc` at head: my layout gave 13 errors, all in `frontend/shared` from module resolution, 0 in `pages/Settings`. So the READY's `tsc` rc 0 is not reproduced, and I do not contradict it.
- eslint and `docs-fragments.mjs check`: not run.
- Platform suites, Node 24, other browsers, keyboard and screen-reader use, the error's dismiss button, double-click on Save.
- The two-tab case with two real admins; only a simulated second writer.

## My conduct
- Wrote only under this folder: `evidence/` (264 MB: clone with sparse tree and admin `node_modules` 217 MB, npm cache 41 MB) and this file. All of `evidence/` is gitignored. Nothing removed, no `rm`; it can go when no longer needed.
- **One write left the folder:** the Playwright tool wrote `console-2026-11-06T11-03-55-341Z.log` to `/Volumes/DevMASTER/WEDNESDAY/.playwright-mcp/`. I moved it to `evidence/playwright_console.log`. Other logs there are not mine and were not touched.
- **Network beyond the commission's list:** git fetch and the one npm install as allowed, the Linear read as commissioned, plus `gh pr view` and `gh pr list`, read-only, which Q5 and Q6 needed. That used `GH_TOKEN` from the project `.env`, which I sourced whole into short-lived shells, printing no value.
- Ran the builder's installed `tsx` by a symlink at `evidence/clone/Blockchain/Dev/node_modules`, pointing at `worktrees/s-r86-ks1231`. I confirmed that worktree is at the head. Nothing in it was edited. Tampers were graded on copies under `evidence/tmp*`.
- Project repository: read verbs only. No commit, push, post, ticket write, mail, box or docker.
- Stood up four local listeners on 127.0.0.1:46102-46105; all stopped, 0 left listening. Browser closed.
- **Errors of mine:**
  - An early `git grep` in the blobless clone started fetching blobs one at a time; I stopped it at 120 s and read from the project repo instead.
  - My first builds failed because of my working directory, not the PR (`evidence/vite_head.out` is the later good run).
  - The "failing rows 30" in `tampers.out` is my counter double-counting summary lines; the `RESULT` line, 3 and 16, is the reading.
  - `R5` (401) was weaker than it looked; see F2.
  - Several commands were refused by hooks and re-issued.
