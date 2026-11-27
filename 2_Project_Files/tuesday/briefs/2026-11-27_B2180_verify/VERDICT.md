GATE B2180: GO WITH FINDINGS @ c02a04c on main d2aeecf

Gate G1 (Opus), round 1 of 2, on NexusAI lane 2 kit 3 (kit B2139, seat N182): RD-455 (a SCIM mapping save keeps the stored token, narrowed to a configuration that is already SCIM) and RD-981 (setQuickQuestions sends no INSERT after a failure). Read-only: no PR, no push, no Jira write, no cd. Clocks are from `date`: gate start 22:13:28, end 22:34:30 AEDT, Fri 27 Nov 2026.

**No Blocker and no Major. Two Minor findings, both coverage or wording. Five Info findings. Nothing blocks landing.** The landing still needs the hosted Linux build green (Q-8). Tuesday must also re-check the deploy switch first: see I-1, which corrects a premise of the commission.

## Lane, re-measured (gh api -X GET under the NexusAI GH_CONFIG_DIR, 22:13:46 and 22:34:30)
- main `d2aeecf8cda67265cc316646953c45d92b861f77` both times. `refs/heads/b2139/lane2-kit3` = `c02a04c528d954ef1cf78d3ceab346b0daf251f6`. Open PRs 0. `heads/b2175` = 0 (N186 has not pushed).
- compare main...head: `ahead 3 behind 0`; the control (the reverse) reads `behind 0/3`. Exactly six files: rd455 test 282/0, rd981 test 233/0, routes/entraProvisioning.js 10/2, services/entraProvisioning.js 14/3, simpleDb.js 15/19, verify-expected-counts.json 3/3. Commits A `91c0e76b`, B `0b1308d5`, K `c02a04c5`, each the parent of the next, on BASE = main.
- The 11 frozen files: sha256 equal to the kit's table, 11 of 11.
- The seat's STATUS was read: sections, Corrections, COMMITS, Verify, CodeQL (rc 0, KEPT 0 / NEW 0, head 29 = base 29), READY. The verify and CodeQL figures are RELAYED from STATUS. I did not re-run the whole suite or CodeQL; the commission did not ask for either.

## 1. The kit's own property, re-run by the gate (one acquisition)
- Tool: `nexusai-lock.sh jest b2180-gate`. The lock was acquired after a 965 s wait in the FIFO behind `b2175-linux-update`, which the gate did not jump. The run went from 22:33:28 to 22:34:08, then "jest lock released by b2180-gate" and `lock-wrapper rc=0`. NODE_OPTIONS was unset and Node was v24.22.2.
- Trees were the gate's own, all dot-free (dot-segment count 0): `g2180/t/base` (slot 15), `t/head` (slot 15) and `t/mut` (slot 11). The control, the seat's `run3`, computes slot 13 as the kit says. No listener was in either band beforehand. node_modules is a symlink to the seat clone's install, whose package-lock sha256 `37e5add354e539f9` equals the head's.
- Linux shape: `TMPDIR=/tmp`, `RUNNER_TEMP=g2180/rt`. Own shape: TMPDIR = `/var/folders/.../T/`.
- Blobs: base `792300f4 4674c7c4 c2e4274b`; head `369a3238 84864830 b260b3e1`, equal to the kit's STATE AT DRAFTING. The test blobs are `327fb65f` and `d147ffb0` in both trees.
- **Red-first at BASE:**
  - rd455 failed exactly V1, V2, T1, T2 and T6, in both shapes;
  - rd981 failed exactly L1, L2 and L3, in both shapes;
  - RD-973's file at BASE is green (the control).
- **Green at head:**
  - rd455 14/14 and rd981 6/6, in both shapes;
  - rd973 and rd913 green;
  - entra-provisioning-config and entra-provisioning-setup green (the existing "requires a bearer token" cell stays green).
- **Mutations: all 11 re-run, not only b01, b04, b08 and b11.** Every one read `jest rc=1`, and every revert restored the head blobs.
  - b01: T4.
  - b02: T1, T2, T6.
  - b03: V4, V5, plus T7 and V6.
  - b04: V3, T3, T4, T5.
  - b05: V2.
  - b06: T6.
  - b07: V1, V2.
  - b08: L1, L2, L3, and RD-973's R-ERR.
  - b09: all six L cells, and RD-973's R-CTL and R-ERR.
  - b10: RD-973's R-INS; the RD-981 file stays green.
  - b11 (the BASE block): L1, L2, L3.
  The b08 and b09 RD-973 columns read as "atleast", as ANSWER-1 ruled. The untouched files stayed green in every row.
- The gate's own mutation g3 drops the token half of `canKeepScimToken`. **Every cell stayed green** across rd455, entra-provisioning-setup and entra-provisioning-config. See M-1.
- Evidence: `gate-run.txt` in this folder, and the logs and JSON under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/g2180/logs/`.

## 2. Security review of RD-455 (the review its AC 1 asks for)
The question was whether an omitted token can ever keep a credential the admin meant to replace or clear. **No path found.**
- **Switch into scim with a leftover token (T4):** the stored mode is off or graph, so the flag is false and the save is refused 400. Held by T4, and b01 turns T4 red.
- **Save after a revoke (T5):** revoke writes token '' and mode 'off' inside `exclusive` (route :316-325), so both halves of the flag are false and the save is refused. Held by T5. Note that T5 is refused by the mode half; see M-1.
- **`canKeepScimToken` from the route** is `stored.mode === 'scim' && Boolean(stored.scimBearerToken)` (route :454), which is always a boolean.
  - The validator reads it only from `ctx`, never from the body (service :79, :198). A body field `canKeepScimToken` has no effect.
  - It accepts only `=== true`; V3 holds that `'true'` is refused.
- **Other callers of `validateProvisioningConfig`:** `git grep` over backend, static and scripts at the head finds the definition and export (service), the import (route :32) and the one call (route :456). In tests only two files call it: entra-provisioning-config and rd455.
- **Inner spaces and non-strings (V4, V5):**
  - Non-strings (123, {}, [], true) are not "omitted" and are refused, and `false` takes the same branch.
  - A spaces-only value is "omitted" (V2).
  - A token with inner spaces is a SUBMITTED token, validated on length and stored trimmed. That behaviour is unchanged and is not a keep path.
  - A short submitted token is refused with or without the flag (V4; b03 shows the cells hold it).
- **Undecryptable stored token** (the kit's limit (i)): `JsonStorage.getSetting` returns `null` when no key candidate decrypts (jsonStorage.js :3424-3431). So the flag is false and a new token is required. This fails closed and agrees with the GET's `scimTokenConfigured` (false).
- **The audit row:**
  - The spread passes the stored value only INTO `auditSafeSummary`, which emits `scimTokenConfigured: typeof === 'string' && length > 0`, a boolean (service :226-236).
  - No token text reaches the row. T6 asserts this with `JSON.stringify(auditCalls)`, and b06 turns T6 red.
  - The response and the GET carry no token (T1).
- **A concurrent save and revoke inside `exclusive`:**
  - Both handlers are chained on one in-process promise tail (route :198-203), and the flag is read after the version check inside the lock. A save queued behind a revoke is refused 409, because revoke moves the revision. A save queued ahead completes, and the revoke then clears it.
  - Across two processes (the code's own stated KNOWN LIMIT), the worst interleaving is a keep-save writing mode 'scim' after another process's revoke. That leaves scim with an empty token, which the endpoint refuses (`tokenMatches` rejects an empty expected value, scimProvisioning.js :49-53).
  - A keep-save writes no token, so it can never re-arm a revoked credential. That is strictly safer than the resubmit path at BASE.
- **The SCIM endpoint that uses the token:** `getEntraProvisioningConfig` (server.js :22401-22421) and the auth middleware (scimProvisioning.js :131-137) read the stored token on every request. Neither is changed, and a kept token is byte-equal (T1, T2). It is unaffected.

### Three shapes outside the property, graded
- **M-1 (Minor, does not block): the "a token is stored" half of the keep predicate is held by no cell.**
  - Gate mutation g3 replaces route :454 with `stored.mode === 'scim'`, and every rd455, setup and config cell stays green. T5 cannot hold it, because revoke also writes mode 'off'.
  - The guarded state, mode 'scim' with no token, is reachable only by a race between two processes, a hand edit, or an undecryptable token (getSetting returns null while the mode stays 'scim').
  - Without the half, that save would return 200 and leave scim with no usable token. The endpoint would then fail closed, so this is a misleading "Saved", not a credential leak.
  - Fix: one cell; candidate 1 in FOR-RECORDS.
- **M-2 (Minor, does not block): a token generated on the panel but never saved.**
  - The panel holds a generated token in page memory only (`state.generatedToken`, entra-provisioning-ui.js :1114) and sends it with any scim save (:1308-1310). So the keep never fires on the save that follows a Generate.
  - If the page is reloaded between Generate and Save, the new value is lost. At BASE the next save was refused, which forced a new token. At the head it is accepted and keeps the OLD token, while Entra may hold the never-stored new one, so provisioning fails with 401s (audited as `scim_auth_failed`).
  - The credential state is the same as at BASE (nothing new was ever stored), and the admin's way to kill a token is Revoke.
  - The owed part is the panel's save note for a kept token, the kit's LEFT FOR OTHERS 2. The current note still says to paste the token into Entra.
- **I-2 (Info): a scim save that omits `authoritative` writes false.** The scim branch always sets `authoritative: body.authoritative === true` (service :210-213). This is true at BASE too, and the panel always sends the field (:1303). The keep makes token-less API saves possible, so an API client sending only mappings resets the flag. Recorded as candidate 3.

## 3. RD-981
- **Can any INSERT be in flight when ROLLBACK is sent? No, for this call.** Each INSERT is sent only from the success callback of the one before it (simpleDb.js :636-656). The ROLLBACK is sent from a failed INSERT's callback, where no later INSERT of the call has been sent. L1 (1 sent) and L3 (26 sent) count the sends after `drained()`, so they cover "ever", not only "by rejection". L2 models the late order and reads red at BASE.
- **The empty list:** `insertFrom(0)` sends COMMIT straight away (L5).
- **A COMMIT error** rejects without a ROLLBACK, the same as at BASE (not changed, no cell). A named limit; I-3.
- **RD-973's property at both failure sites:** `this.db.run('ROLLBACK', () => { reject(err); })` at the DELETE failure (:629) and the INSERT failure (:649). RD-973's 5 cells are green at the head. b10 (reject before ROLLBACK) turns RD-973's R-INS red, so the property is held.
- **Production callers, dynamic dispatch included:**
  - `setQuickQuestions` (case-insensitive, untruncated `git grep`) appears in backend, scripts and static only in jsonStorage.js :3827, server.js :20763 (`jsonStorage.setQuickQuestions`) and simpleDb.js :620.
  - The server's `database` (SimpleDatabase, server.js :4820, :4976) goes to `seedDemoDataIfRequested` and the init return, and neither names the method.
  - Variable-key calls in backend/scripts (`x[y](`) count 2 (control: the pattern finds them): llm/tools.js :17, a comment about tool executors, and routes/sustainability.js :209, a logger level.
  - **No production caller.** The change is hardening.
- **I-4 (Info): non-array argument** (gate plain-node probe `tools/probe981s.js`, own mkdtemp folder):
  - At BASE a string or array-like argument ABORTS the node process: `FATAL ERROR: Error::ThrowAsJavaScriptException napi_throw`, rc 134, from a throw inside the sqlite native callback.
  - At the head the string 'abc' resolves true with rows `["a","b","c"]`, and the array-like resolves with its items.
  - `{}` at the head rejects with SQLITE_CONSTRAINT and leaves the pre-state.
  - `null` aborts the process at BOTH sides.
  - So the kit's sentence "a non-array throws inside the callback exactly as at main" is not right for strings and array-likes. The head is strictly less harmful, and no caller passes these. Candidate 2.
- **I-5 (Info): interleaving.** Between two sequential INSERTs another statement on the same connection can now run inside this transaction. It would be committed or rolled back with it. The window existed at BASE between the DELETE callback and the queued block, and is now wider. No production caller exists.

## 4. Secrets and committed text
- **gitleaks 8.30.1:**
  - control first: a runtime-generated `AKIA...` key and secret pair (not the docs' EXAMPLE keys) gave rc 1, `leaks found: 1`;
  - `git log -p BASE..head | gitleaks stdin`: rc 0, `no leaks found`;
  - the three commit messages: rc 0, no leaks;
  - `gitleaks git --log-opts=BASE..head` over the gate's clone: rc 0, no leaks.
- **Static scan** (`tools/scan2180.py`; the four names come from scanlib1114.py line 20 and are never printed), over 557 added lines and 2910 message bytes. Each scan's control fired.
  - names: 0 and 0;
  - build, seat, card and session ids: 0 and 0;
  - skips and `.only`: 0;
  - non-ASCII: 0 and 0;
  - `/Volumes/`, `/var/lib` and `/app/`: 0 (control: `path.join` 3).
  - Ruling words: one hit, "The gate fails on any difference" in K's message. That is the CI gate, the same wording as the form kit's K, and benign.

## 5. Landing
- `landing.txt`: a PR from the branch, landed by MERGE COMMIT pinned to `c02a04c5`. C-190 is CLARIFICATIONS.md line 2067, printed with awk.
- Checks to expect: 7 distinct names and 8 runs, read from PR 268 (head 61612323), all success.
- Code scanning: baseline 29 and 22 open. Alerts #145 and #146 sit in the changed route at the Test Connection Graph calls (:620, :644 at main), not on a changed line or flow.
- Counts file: if anything resizes the suite on main first (N186's lane will), the head cannot land as is. A seat merges main into the branch (never rebase, never "Update branch") and regenerates with the project's command in the Linux shape, which gives a new pin and a delta read. If this PR lands first, nothing changes.
- **I-1 (Info, but Tuesday must act on it before merging): the `demo` environment does not exist.**
  - `GET .../environments` reads total 1, `dev`, with 0 protection rules. `GET .../environments/demo` answers 404.
  - So there is NO reviewer gate on the deploy job today: GitHub creates a named environment on first use, without protection.
  - The ONLY thing that stops a merge to main from deploying is `CI_DEPLOY_ENABLED` being unset. Gate read: repo variables 0, organisation variables visible 0, dev environment variables 0. The last Deploy demo run, 45948221672 at d2aeecf8, has both jobs skipped.
  - landing.txt step 4 makes those three reads a pre-merge requirement. The C-224 hold (line 2412) stands.
- `pr-title.txt`, `pr-body.md` (no names, ids or cards; choices named as the coordinator's; named limits) and `FOR-RECORDS.md`:
  - RD-455 to Testing;
  - RD-981 to Testing;
  - RD-728 stays To Do;
  - three candidates.

## Not run by the gate
- The whole suite (relayed: the seat's linux-update and plain verify, each `6654/6654 tests passed across 421 suites`).
- CodeQL (relayed: rc 0).
- The 33-neighbour run (relayed: 35 suites, 649 tests, 0 failed).
- Real Linux.
- A real-race trial loop.
- Jira.

## State left
- Lock released: lock base lists only queue-docker, queue-jest and released.
- No gate process running (`pgrep -f g2180`: none).
- Scratch trees left at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/g2180/` (clone, t/base, t/head, t/mut with the mutation markers). Nothing was deleted. The project checkout and the seat's trees are untouched: read only.
