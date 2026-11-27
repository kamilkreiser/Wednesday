# FOR-RECORDS: RD-455 and RD-981, for the records pass AFTER the landing (RD-728 stays To Do)

After the landing, fill in `<n>` (the pull request number) and `<M>` (its merge commit). Take the Deploy demo line from landing.txt step 4 and the gate line from the first line of VERDICT.md. This gate did NOT read or write Jira; the seat's Jira GET at 21:05 AEDT read all three tickets To Do with 0 comments. Before writing each comment, the records seat reads the ticket's current comments and state. No person's name and no card, seat or build id goes in a comment. Name every choice as the coordinator's default.

## Ticket state, read against the project's rule
The project rule is `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/CLAUDE.md` line 302, under "When completing work": a code change goes to `Testing`.
- **RD-455: move to Testing after the landing.** Its acceptance criteria are all met:
  1. "Decide and record whether an omitted token in mode scim means 'keep the stored token' ... the change gets a security review." Decided as kept, narrowed to an existing SCIM configuration with a token stored (the coordinator's default; no recorded decision rules the shape). The G1 gate is the security review.
  2. "a mapping-only Save with a stored token succeeds and the stored token is unchanged (byte-equal before/after); a Save with no stored token and no submitted token is still refused with an explanation." Cells T1, T2 and T3.
  3. "Cells red at origin/main, green at head; tier-1 gate." Met; the gate ran both sides itself.
- **RD-981: move to Testing after the landing.** The recommendation's steps are met:
  - a cell red on the old file for a long list with a null first row (L1, L2, L3);
  - no INSERT of a failed list can run after the ROLLBACK (sequential sends; L2 models the late order deterministically);
  - an independent review (this gate);
  - the production-caller question, answered as the coordinator's reading below.
  The real-race rate was not measured, and no trial loop was asked for as a gate.
- **RD-728: leave To Do, untouched.** It is a follow-up to RD-628's branch, which is not on main. Its target test file is absent at main, and so is the phrase it rewords in `backend/encryptionService.js`. It becomes buildable when RD-628 lands. Optionally add one comment saying so; no move.

## RD-455: comment
Pull request <n> landed as merge commit <M>, the merge of the reviewed head `c02a04c5` (three commits; `91c0e76b` is this ticket's).

**Decision (coordinator's default):** an omitted SCIM bearer token means "keep the stored token", but only when the stored mode is already `scim` and a token is stored. A switch into SCIM from `off` or `graph` with a leftover token still needs a new token. The persist step never clears a token on a mode change, so without this narrowing a mode change would silently re-arm an old credential.

**What changed:**
- `validateProvisioningConfig` (`backend/services/entraProvisioning.js`) takes `ctx.canKeepScimToken` (default false). When it is exactly `true`, an omitted token (absent, null, empty or only spaces) is accepted with no token key in the config. A submitted token is always validated: a short or non-string value is refused.
- The save route (`backend/routes/entraProvisioning.js`) computes the flag inside its exclusive section, after the version check, from the stored mode and token. This is the same predicate the GET reports as `scimTokenConfigured`. For a kept token the route writes nothing, so the stored token and its issue date are byte-equal.
- The audit row keeps `scimTokenConfigured: true` (a boolean, never the value).

**Tests:** new file `__tests__/rd455-scim-mapping-save-keeps-the-stored-token.test.js`, 14 cells.
- V1, V2, T1, T2 and T6 were red at the base and green at the head, in a Linux-like temp shape and the machine's own (the gate ran both).
- V3 to V6, T3, T4, T5, T7 and T8 are controls, green on both sides: no keep without the flag; a short or non-string token; a valid token replaces; no stored token; a switch into SCIM; after a revoke; a new token replaces; a stale version.
- Seven mutations of the hunk each turned their named cells red (the gate re-ran them).

**Security review (G1 gate):**
- A save after a revoke, a switch into SCIM and a stored token that cannot be decrypted (read as no token) all still need a new token.
- The flag cannot come from the request body.
- The validator has no other caller in product code.
- A save and a revoke are serialised by the router's exclusive section, and a save from a page read before a revoke is refused with 409.
- The SCIM endpoint reads the stored token on every request and is unchanged.

**Named limits:**
- The panel's save note for a kept token still says to paste the token into Entra (owed wording).
- A token generated on the panel but never saved does not replace the stored one; a later save without it keeps the old token.
- The route's "a token is stored" condition is held by no cell (a gate mutation dropping it turned no cell red). The state it guards (mode scim, no token) needs a race between two processes or a hand edit, and the endpoint refuses every request in that state.

Hosted build of the pull request: <the `VERDICT: PASS` line, the first Linux run>. Deploy: none; Deploy demo run for <M>: <conclusions>. State: Testing.

## RD-981: comment
Same landing; `0b1308d5` is this ticket's.
- `setQuickQuestions` (`backend/simpleDb.js`) now sends each INSERT from the callback of the one before it. A failed INSERT leaves nothing queued behind it, and the ROLLBACK is the last statement of a failed call.
- The empty list commits the delete, and a good list is stored in order.
- At both failure sites (DELETE, INSERT) the call rejects only from the ROLLBACK's callback, so RD-973's property is unchanged. RD-973's five cells and RD-913's S4 pass at the head.

**Tests:** new file `__tests__/rd981-set-quick-questions-sends-no-insert-after-a-failure.test.js`, 6 cells.
- L1 (one INSERT sent for a null first row), L2 (the late order modelled: every concurrent INSERT held until the call settles) and L3 (26 INSERTs for a null at index 25) were red at the base and green at the head, in both shapes.
- L4 (a good 50-row list, which also proves the instrument sees INSERTs), L5 (the empty list) and L6 (a DELETE failure) are green on both sides.
- Four mutations each turned their named cells red (the gate re-ran them). Two of them are also caught by RD-973's own cells.

**Production caller (coordinator's reading, not a ruling):**
- The server calls `jsonStorage.setQuickQuestions`, the other store's method.
- The name `setQuickQuestions` appears in no backend, scripts or static file other than `jsonStorage.js`, `server.js` (the jsonStorage call) and `simpleDb.js`.
- The two variable-key calls in `backend/` dispatch on LLM tool names and logger levels.
- No production path reaches this method, so this is hardening.

**Named limits:**
- A COMMIT error rejects without a ROLLBACK, as before.
- Between two INSERTs another statement on the same connection can now run inside the transaction (no caller does this today).
- A string or array-like argument is now stored one item per row. It used to end the process with a throw inside the sqlite callback (gate probe: node aborted, rc 134). `null` and `undefined` still end the process.
- The real-race rate was not measured.

State: Testing.

## Ticket candidates (dup-check RD-455, RD-388, RD-428, RD-973, RD-981 neighbours before filing)
1. **RD-455 follow-up (Minor): pin the "a token is stored" half of the keep predicate.** The route's `canKeepScimToken = stored.mode === 'scim' && Boolean(stored.scimBearerToken)`: a gate mutation that drops the second half turned no cell red (gate log `g3-gmut-tokclause`). Add a cell that stores mode `scim` with an empty or undecryptable token (for example through a store whose token setting is set to `''` while the mode stays `scim`) and asserts a mapping-only save is refused 400 `INVALID_SCIM_TOKEN`. Fold in the panel's save-note wording for a kept token (LEFT FOR OTHERS 2).
2. **RD-981 follow-up (Info, only if wanted):** `SimpleDatabase.setQuickQuestions` takes any value with a `length`. A string is stored one character per row; before the change it aborted the process. `null` and `undefined` abort the process both before and after the change, because the throw happens inside a native sqlite callback. A guard before `BEGIN`, `if (!Array.isArray(questions)) return reject(new TypeError(...))`, would close all of these. No caller passes a non-array.
3. **Info, no ticket unless wanted:** a SCIM save in mode `scim` that omits `authoritative` writes `authoritative: false` (the validator's scim branch always sets it). This was true before the change; the panel always sends the field. The change makes token-less API saves possible, so an API client that sends only the mappings resets the flag.
