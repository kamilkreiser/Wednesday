Three commits on `d2aeecf8`; six paths. `backend/services/entraProvisioning.js` gains 14 lines and loses 3. `backend/routes/entraProvisioning.js` gains 10 and loses 2. `backend/simpleDb.js` gains 15 and loses 19. There are two new test files and the counts file. No workflow, helper, panel file or other file is changed, and nothing is deployed.

## RD-455: a SCIM mapping-only save keeps the stored bearer token
- Saving a group-mapping change in SCIM mode without generating a new token returned 400 `INVALID_SCIM_TOKEN`. The panel never holds the stored token (the GET reports only `scimTokenConfigured`), so every mapping edit forced a new credential.
- `validateProvisioningConfig` takes a new context flag, `canKeepScimToken`, which defaults to false. When the flag is exactly `true`, an omitted token (absent, `null`, empty or only spaces) is accepted. In that case the config carries no token key, so the route writes nothing and the stored token and its issue date stay byte for byte as they were.
- A token that is submitted is always validated. A short or non-string value is refused and is never read as omitted.
- The save route sets the flag from the stored configuration: the stored mode is already `scim` and a token is stored. This is the same predicate the GET reports as `scimTokenConfigured`, and it is read inside the router's existing exclusive section, after the version check.
- The keep does not apply in these cases. Each still needs a new token:
  - switching into SCIM from `off` or `graph` with a token left over from an earlier period. The persist step never clears a token on a mode change, so without this narrowing a mode change would silently re-arm an old credential;
  - a save after the token was revoked;
  - a save with no stored token.
- A stale-version save is still refused with 409 before anything is read.
- The audit row of a kept-token save still says `scimTokenConfigured: true`. It holds a boolean, never the value.
- New file `__tests__/rd455-scim-mapping-save-keeps-the-stored-token.test.js` has 14 cells:
  - V1 to V6 call the validator directly;
  - T1 to T8 drive the real router over a real settings store.
  V1, V2, T1, T2 and T6 read red before the change and green after. The other nine are controls that read green on both sides.

## RD-981: setQuickQuestions sends no INSERT after a failure
- `setQuickQuestions` (`backend/simpleDb.js`) replaced the table inside one transaction but queued every INSERT at once. When an early INSERT failed and the ROLLBACK was sent, INSERTs already queued behind it could still run afterwards outside the transaction and commit rows of the failed list.
- Each INSERT is now sent from the callback of the one before it, so nothing is queued behind a failed INSERT and the ROLLBACK is the last statement of a failed call.
- The rest is unchanged:
  - the empty list commits the delete;
  - a good list is stored in order;
  - a DELETE failure still rejects with the original error after a ROLLBACK;
  - a call still rejects only after its ROLLBACK has finished, at both failure sites.
- New file `__tests__/rd981-set-quick-questions-sends-no-insert-after-a-failure.test.js` has 6 cells. It counts the statements the call sends and models the late order deterministically, by holding every INSERT sent while another is still waiting until the call has settled. L1 to L3 read red before the change and green after. L4 to L6 are controls that read green on both sides.
- The server reaches the other store's method of the same name (`jsonStorage.setQuickQuestions`). A text search found no production caller of this method, so the change hardens a method that only tests reach today.

The counts file moves from 6634 tests in 419 suites to 6654 in 421. The project's own command wrote it.

## Choices made by the coordinator, not by the product owner
- One change for both tickets.
- The token keep applies only inside an existing SCIM configuration with a token stored. No recorded decision rules this shape, so it is the coordinator's default.
- The INSERTs are sent one after another, not as one multi-row statement. A long list could exceed SQLite's bound-variable limit, and this shape keeps the row order and ids.
- No trial loop for the real race, and no rate is claimed.

## Reviewed
An independent security review of the SCIM credential path (the review RD-455 asks for) re-ran both new files and RD-973's file at the base and at the head. It used two shapes: a Linux-like temp setup (`TMPDIR=/tmp` with a persistent `RUNNER_TEMP`) and this machine's own temp folder. The red cells at the base were exactly the ones named above, and every cell was green at the head. It also re-ran the eleven mutations of the two hunks and one mutation of its own. It checked these paths and found that none keeps a credential the admin meant to replace or clear:
- a switch into SCIM;
- a save after a revoke;
- a stored token that cannot be decrypted;
- a non-string or short token;
- the audit row;
- a save racing a revoke;
- the SCIM endpoint, which reads the stored token on every request and is unchanged.

gitleaks found nothing in the commits or their messages.

## Named limits (nothing is refused for these)
- The panel's save note for a kept token still tells the admin to paste the token into Entra.
- A token generated on the panel but never saved does not replace the stored one. A later save without it now keeps the old token, where it used to be refused.
- The route's second condition (a token is stored) is held by no cell. The stored mode is `off` after a revoke, so T5 is refused by the first condition. The stored state "mode scim with no token" is reachable only by a race between two processes or a hand edit. If the condition were dropped, that save would be accepted and leave SCIM with no usable token, so the endpoint would refuse every request.
- A COMMIT error in `setQuickQuestions` still rejects without a ROLLBACK, as before.
- A string or other array-like value passed to `setQuickQuestions` is now stored one item per row. Before the change it ended the process: the throw happened inside the sqlite callback. `null` or `undefined` still end the process, as before. No caller passes any of these.
- The rate of the real race inside a jest worker is not measured.
- The hosted `build` job of this pull request is the first run of the two new files on a real Linux machine. A red result there on a new cell is a fix round.

## Deploy
None. The merge touches `backend/` and `__tests__/`, which the Deploy demo workflow does not ignore, so a run starts on the push. Both of its jobs are expected to read skipped because the switch variable is not set.
