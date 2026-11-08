# Gate 256: Secuura / Blockchain, PR 2058 (KS-1231 portal half), tier 1, round 2 of 2

| PR | Head | Verdict |
|---|---|---|
| 2058 | 527d67b1852e4226b91851562d925cbaaff134d0 | **GO WITH NOTES** (no finding blocks) |

## BLUF

Round 1's F1 to F7 and Q5 are closed at this head. I checked them myself, and three of the seat's browser scenarios reproduce in my own drive. S5 (failed load), S12 (stale page) and S14 (gateway 503 text) all pass in real Chrome 156 against my own `tsc && vite build` of this head (rc 0), served by a stand-in I wrote from my own read of `routes/admin.ts:1153-1215`. The same drive against a build of develop fails all three, so the drive can fail. The suite is 39 of 39 at head.

The changed contract holds on develop. A category missing from the body is kept as stored on every PUT path: a Redis hit, a Redis miss read from the DB row, and an unreadable store, which answers 503 and writes nothing.

The seat's two FOUND-NOT-FIXED items are measured and unchanged from develop. Neither blocks. Both should be ticketed, and the eviction one is security-relevant. The other notes are factual slips in the PR body, a fragment, and suite gaps.

Merging this is clean. Develop changed 13 files since the merge base and none of them is one of this PR's 7. No other open PR (45 counted) touches the 7 paths.

## Refs (re-read at start and end)
| Reading | develop | PR 2058 head |
|---|---|---|
| 21:49:04 AEDT start, `git ls-remote` | a2c3ec7f3f98f97b886eb789cc2745182b627f6f | 527d67b1852e4226b91851562d925cbaaff134d0 |
| 21:57:47 AEDT end, `git ls-remote` | a2c3ec7f3f98f97b886eb789cc2745182b627f6f | 527d67b1852e4226b91851562d925cbaaff134d0 |

Both readings equal the commission's pins. The head equals the READY.

## Findings

### N1. MINOR, does not block. False toolchain sentence in the PR body and the flow fragment
- **Where:** PR body "Test plan", and the flow fragment `.1 What proves it` "Measured on:". Both say "vite 7.3.7".
- **FOUND:** the admin build runs vite 8. The seat's own `evidence/admin_build_round2.out` prints `vite v8.3.4`. My workspace-layout build prints `vite v8.2.1`. The root install holds vite 7.3.6, not 7.3.7, and the admin build does not use it.
- **TESTED:** READ ONLY plus my build log (MEASURED). Fix: correct the version in the body and the fragment.

### N2. MINOR, does not block. A sentence is duplicated in the PR body
The "Browser walk" bullet says "real Chromium 156.0.8078.80, a real vite build of the head, API answered by a stand-in that copies admin.ts:1153-1215." It then says the same thing again with more detail. It is an editing slip, not a false claim. READ ONLY.

### N3. MINOR, does not block. The suite cannot see four of my own planted page defects, and one cell goes red on an equivalent form
I planted each defect in a copy under my clone and ran the suite with `SETTINGS_TSX`, `SETTINGS_API_TS` or `SETTINGS_PAYLOAD_TS` (MEASURED):
- O1: the "Reload settings" button does nothing (`onClick={() => undefined}`). **39/39, survives.**
- O2: a reload replaces `settings` but keeps the old `formValues` (the `setFormValues` line in `loadSettings` deleted). **39/39, survives.**
- O3: `fetchSettings` accepts a top-level array as settings (`|| Array.isArray(settings)` removed). **39/39, survives.**
- O10: `saving` stays true after a refused or failed save, so the Save spinner sticks. **39/39, survives.**
- O8, control for the module: `flattenSettings` uses `&&` instead of `||`. **Red on K4, K6 and K9**, as expected.
- O11, not a defect: `disabled={saving || !settings}`. **P5 goes red** (38/39), because P5 matches the text `settings === null`. That is a red for the wrong reason, so P5 is tied to one way of writing the check.

These are the same class as the seat's three declared survivors: page state that only a browser shows. The module logic is well covered (the seat's 30 tampers, and my O8). Fix shape: browser cells for the Reload button and for the Save button state after a refusal, or a jsdom render cell. They are not added here.

### N4. MAJOR class, PRE-EXISTING, unchanged by this PR, does not block. After an eviction, a save writes the defaults over the stored values (commission item 3)
- **Where:** `routes/admin.ts:1155` (develop a2c3ec7f3f98). GET reads only Redis, `getNotificationSettings('platform-settings') || {}`. When Redis is down, `services/redis.ts:687-692` reads the in-process Map instead, which is just as empty. PUT reads through `readPlatformSettings` and so gets the DB record (`admin.ts:1188-1200`).
- **FOUND, measured at module level:** `g256drive/proto_evict_g256.mts` sets up a record with `security.mfaRequired: true` and a Slack webhook. GET answers the defaults, the admin edits only Platform Name and saves. The body carries all four default categories, and the merge stores `security.mfaRequired: false` and `notifications.webhookUrl: ''`. `integrations` is kept.
- **Head vs develop:** the bodies are **byte-identical** (`bodies identical head vs develop: true`). The PR neither adds this nor makes it worse. Its only effect here is good: `integrations` is never sent. In my S5 the body after a reload also carries all four categories, as at develop.
- **Severity:** a silent downgrade of security settings (MFA, password policy) after an LRU eviction. It belongs in its own ticket on the gateway GET, for example a GET that reads through `readPlatformSettings`. Evidence class: MEASURED on a model of the merge, READ ONLY on the real gateway.

### N5. MINOR to MEDIUM, PRE-EXISTING, same at develop, does not block. A stored category named `__proto__` pollutes the admin page's `Object.prototype` (commission item 4)
- **Where:** `settingsSavePayload.ts:84`, `(updates[category] ??= {})`. Develop's inline grouping `if (!updates[category]) updates[category] = {}` does the same.
- **FOUND (MEASURED, tsx, the head module vs develop's logic copied):** I planted the wire document `{"settings":{"general":{...},"__proto__":{"g256polluted":"yes"}}}`. JSON.parse makes `__proto__` an own key. A control read before each run gives `({}).g256polluted = undefined`. After one save build it is `"yes"` at **both head and develop**. The body itself does not carry the key (`ownProtoKeyInBody=false`).
- **Can it be stored?** Yes. The gateway's spread `{...defaults, ...existing, ...body}` keeps an own `__proto__` key (`gateway-style spread keeps own __proto__: true`), so any caller of `PUT /api/admin/settings`, which means an admin, can plant it. Every admin who opens and saves the page is then polluted. I found no gadget, and I did not look for one.
- Fix shape: skip `__proto__`, `constructor` and `prototype` categories, or build the body on `Object.create(null)`, and refuse the key at the gateway. Ticket it.

### N6. NOTE, PRE-EXISTING. A stale page still overwrites another writer's changes inside the object categories
In my S12 the body carries `general`, `security`, `notifications` and `blockchain` whole, as they were loaded. So another writer's change to, say, `security` is reverted by any unrelated save. Connectors are now safe, which was this PR's F6. The other categories are as they were at develop. MEASURED (S12 body).

### N7. NOTE for the humans. Wednesday's ruling is wider than Kam's card
Kam's card `secuura-ks1231-nine-fields-share-integrations-key-1106` = a, read with `decision_queue.sh show`, covers the nine fields: "read-only ... No gateway change". The rule "never send ANY array category" is Wednesday's F6 ruling, and the body labels it as Wednesday's. Today it is harmless, because the only array category in the defaults, the readers or the page is `integrations`. It would quietly drop a future array category from every save.

## Per question

**1. F1 to F7 and Q5, by my own read and run.**
- **F1, closed.** Array categories and `integrations` give no form values (`settingsSavePayload.ts:50`). The body never carries them (`:80-82`). Cells G1 and G3 reload through JSON. MEASURED (suite), READ.
- **F2, closed.** `fetchSettings` throws on a failed GET and on a reply with no settings (`api.ts` round-2 hunk). `settings === null` turns Save off. **S5 MEASURED:** load 503: the error "Redis unavailable" is shown, the not-loaded notice is shown, Save is disabled, and a click sends 0 PUTs. Reload settings then clears the notice, Save is enabled, and an edit saves with no `integrations` in the body. The stored `[c1]` is unchanged. F2a (a reload fails after a save) is covered by cell G4 and the `saved-not-reloaded` branch. I did not drive F2a in the browser.
- **F3, closed by read.** The nine controls are `disabled`, with no `onChange`. The note names KS 2035. P4 and P6 are green. Matches Kam's card a. I did not drive this in the browser.
- **F4, closed.** The refusal text is plain. By my read no control produces a refused key, because the nine are disabled and arrays are not flattened. A failed load offers Reload (S5).
- **F5, closed in part.** Gate 236's T4 is red on P2, per the seat's tamper record. My O1, O2, O3 and O10 survive (N3).
- **F6, closed.** **S12 MEASURED:** the page loads `[c1]`, another writer stores `[c1,c2]`, and an unrelated save sends no `integrations`. The store keeps `[c1,c2]`.
- **F7, closed.** **S14 MEASURED:** the PUT answers 503 `{error:{code,message}}`. The page shows "Platform settings could not be stored; nothing was changed" with no `[object Object]`. Save stays enabled and the not-loaded notice does not appear. A retry succeeds (2 PUTs, a success banner). Develop shows "Failed to save settings".
- **Q5, closed**, except for N1 and N2. The four false sentences gate 236 named are gone from the module comment, the body and both fragments.

**2. The changed contract (develop a2c3ec7f3f98).** `merged = {...PLATFORM_SETTINGS_DEFAULTS, ...existing, ...body}` (`admin.ts:1200`) keeps any category missing from the body as `existing`. `existing` comes from `readPlatformSettings(…, {refill:false})`:
- Redis hit: the cached value.
- Redis miss: the DB row.
- No readable row (`db-unavailable`, `db-row-missing`, `db-read-failed`, `db-row-not-an-object`): `unreadable`, answered 503 with nothing written.
- A thrown read: 503.

There is one PUT route, so creating and updating share this path. A fresh instance's first save reads the row seeded by migration 057. One caveat comes from KS-1256, not this PR: an eviction before the first backfill reads the seed, which has no `integrations`. Then `integrations` is "kept" as the seed has it, that is, absent (`settingsStore.ts:24-27`).

Who else writes these settings:
- PUT `/api/admin/settings` (the DB, then Redis).
- Migration 057's seed.
- `backfillSeedRow`, which copies Redis over the seed row once.
- `readPlatformSettings`, which refills Redis from the row.
- `PUT /api/admin/notifications` refuses the key `platform-settings` (`admin.ts:1618`).

originate's `/api/admin/settings` (`adminConfig.ts`) is a separate store, the `admin_settings` table. The only caller of `fetchSettings` and `updateSettings` is `pages/Settings.tsx`. I searched `frontend`, `packages`, `scripts`, `tests` and `systemTest` at head with `git grep`. A first search with `\b` returned zero, failing its own positive control, and I re-ran it without `\b`.

**3.** See N4. Unchanged from develop, so it does not block.

**4.** See N5. The same at develop, so it does not block.

**5.** 39/39 at head, MEASURED with the root install's tsx 4.23.1 and typescript 5.9.3 on Node v26.8.1. My planted defects are in N3. One killed as expected (O8). Four survive, and those four are what the browser walk is for. P5 goes red for the wrong reason on an equivalent form (O11).

**6. Body, both fragments, and ticket comment 74414f5b.** I read the files the seat posted from: `push/pr_body_pr2058_r2.final.md`, the fragments at head, and `push/comment_pr2058_r2.md`. The seat's read-back record says the live body matches, `body_sha1 c04a886e…`. **I did not read the live PR or the Linear comment over the network** (git-only rule).

Checked true at this head:
- 7 files, +766/-64.
- `admin.ts:1200` is the merge, `:1187-1198` is the 503 path, `:1155` is the Redis-only GET.
- The only caller is `Settings.tsx`.
- The not-loaded, Reload and Save-off behaviour (S5).
- The gateway's reason is shown (S14).
- The readers answer 403 for a malformed container (`verification.ts:857-886`, `health.ts:79-105`, READ ONLY).
- The nine fields are read-only, with a note naming KS 2035.
- Kam's card a, quoted correctly.
- tsx 4.23.1 and typescript 5.9.3.
- `tsc && vite build` rc 0 (my build).

False: "vite 7.3.7" (N1). Not verified by me:
- eslint "0 errors, 58 warnings".
- `docs-fragments.mjs check` OK.
- The seat's 30 tampers (I read the record, I did not re-run them).
- The 9/30 red-first count.
- The other 17 browser scenarios.

The ticket comment carries no false sentence I could find. It leaves out the `__proto__` item, which the body has. That is acceptable for client wording.

**7. Merge.** `merge-tree` was refused by this session's hook in the clone, so I worked it out with read verbs. The merge base is 9ede880539f3, an ancestor of develop. Develop changed 13 paths since then and the PR changed 7. Their intersection is **0**, and the control (the PR's paths against themselves) is 7. So the 3-way merge is conflict-free by construction. The seat recorded a `merge_tree_pr2058_r2.out`, which I did not re-run.

Open PRs: `ls-remote refs/pull/*/merge` lists **45**, the same count as the seat. I fetched all 45 heads and diffed each against its merge base with develop:
- Only 2058 touches the 7 paths (the self-control is 7).
- Neighbours under `frontend/admin` or the gateway's admin route, with no shared path:
  - 639 and 948 change `admin/package.json` only.
  - 2060 changes `admin/src/store/authStore.ts` and `routes/admin.ts` hunks at lines 603-650, not the settings route.
  - 2091 (KS-528) moves admin to react-router 7 across 11 admin files. `Settings.tsx` imports no router.
- No merge order is required. If 2091 merges first, the admin bundle is rebuilt on new dependencies, and this PR's browser evidence is then for the old ones.

## NOT tested
- A real gateway, Redis or Postgres. Both stand-ins are hand copies. Mine is `drive/standin_g256.mjs`, written from my own read, not the seat's mock. Reader 403s are READ ONLY.
- Any real environment, so the stored shapes are unknown.
- F2a, F3, S4 and the other 17 seat scenarios in a browser. I drove only S5, S12 and S14, plus the develop control.
- The Dockerfile-layout build. I built in the workspace layout, symlinking the shared checkout's installed `node_modules` read-only, with vite 8.2.1 where the seat had vite 8.3.4 via `npm ci`. I checked for a second React only indirectly, by the page rendering and working.
- The deployed nginx bundle.
- eslint and `docs-fragments.mjs check`.
- Re-running the seat's 30 tampers or its 9/30 red-first count.
- The live PR body and the live Linear comment (network).
- `merge-tree --write-tree` (refused by the hook; replaced by path disjointness).
- Node 24, other browsers, keyboard and screen readers, two real admins.
- A gadget for N5.

## My conduct
- **Clone:** `/private/tmp/g256`, blobless, on the boot volume. **198 MB** at the end, mostly the two `dist` builds and the archive extracts. Left in place under the no-rm rule. Inside it are `head/` and `base/` (`git archive` extracts), `tamper/` (my planted copies), `drive/` (the stand-in and walk outputs `walk_head.json` and `walk_base.json`) and `head/Blockchain/Dev/g256drive/` (the drive and the N4/N5 script). I set `core.sshCommand` in the clone's own config to the project deploy key.
- **Symlinks, read-only use of the shared checkout:** `head/Blockchain/Dev/node_modules`, `head/.../frontend/admin/node_modules`, `base/Blockchain/Dev/node_modules` and `base/.../frontend/admin/node_modules` point at `2_Project_Files/Blockchain/Dev/{,frontend/admin/}node_modules`. Nothing was written there. vite writes its `dist` into my clone.
- **Network:** `git ls-remote` and `git fetch` only (the PR head and the 45 open PR heads). No npm, no gh, no Linear.
- **Hooks refused**, and I re-issued each command:
  - `git checkout`: I switched to `git archive`.
  - A stray `cp $A/../../../..` in one command: a typo of mine, refused before it ran, nothing written.
  - `merge-tree`: replaced as above.
  - An `ln` whose target sat inside the shared checkout: I moved the drive file instead.
  - A `=====` separator.
  - `git fetch` through a variable: re-issued with the literal clone path.
- **Listeners:** 127.0.0.1:46256 and 46257 were stopped, and 0 are left listening. Headless Chrome (channel `chrome`, 156.0.8078.80) was closed.
- Load stayed between 5.3 and 6.8. DevMASTER held 23 GiB free at the start and at the end.
- No commit, push, post, ticket write, mail, box or docker. The only file I wrote outside my clone and the scratchpad is this verdict.
