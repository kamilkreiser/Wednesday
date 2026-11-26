Three commits on `e20b30cf`; six paths. `backend/services/scimProvisioning.js` gains one import line and changes two lines. `backend/services/cspReport.js` gains three lines (one refusal line under a two-line comment) and loses none. Two new test files, two changed lines in one existing test file, and the counts file. No workflow, no helper and no other file is changed, and nothing is deployed.

## RD-1023: the SCIM router's two audit entries record the full path
- `scim_rate_limited` (written by the limiter) and `scim_auth_failed` (written by the token check) recorded `req.path`. Inside the router mounted at `/scim/v2`, that is the path relative to the router (`/` or `/Users`).
- Both entries now read the path through `requestPath` from `backend/services/accessAudit.js`. The shared audit rows and the provisioning router's refusal entry already use this helper. It records the pathname as sent: no query string, no fragment, no host from an absolute-form target, and percent-encoding kept as sent.
- The entries keep exactly their three keys (`path`, `method`, `ip`). They carry no token material and nothing that says why a token failed. A correct token writes neither entry, and the other SCIM entries are unchanged.
- New file `__tests__/rd1023-scim-audit-entries-record-the-full-path.test.js` has 14 cells. It mounts the real router as the server does, and one cell reads the entry through the administrator's audit export on a real server. C1, F1 to F5, H1 and L1 to L3 read red before the change and green after. T1 and N1 to N3 are controls that read green on both sides.

## RD-759, the third shape: the CSP intake refuses a data: address that carries an at-sign
- The intake kept `data:text/plain,u:p@h` as sent, because the hostless userinfo strip looks only at the first path segment.
- `stripQueryAndFragment` now answers `null` for a `data:` address with no parsed host whose kept text (after the query string and the fragment are cut) holds a literal `@`. The field is not stored and not logged. A report with no other violation field is dropped as empty, and the route answers its own 400 for it. A report with a directive is kept with a null address.
- Every other `data:` address, `data` alone and every other scheme are unchanged. The two shapes of this ticket that landed earlier keep their own lines.
- New file `__tests__/rd759-data-address-with-at-sign-refused.test.js` has 12 cells. D1 to D5 and S1 read red before the change. K1, L1 and N1 to N3 are controls that read green on both sides.
- One existing cell, C-DATA in `__tests__/rd759-796-csp-intake-edges-and-typed-fields.test.js`, recorded this shape as unchanged. Its expectation is now the refusal. Only those two lines of that file change.

The counts file moves from 6504 tests in 409 suites to 6530 in 411. The project's own command wrote it.

## Choices made by the coordinator, not by the product owner
- One change for both tickets.
- The refusal is a field-level null, not a drop of the whole report.
- Only a literal at-sign counts.
- The one existing cell is turned rather than kept.

The refusal itself follows the recorded ruling on this ticket.

## Reviewed
An independent review re-ran the two new files and the changed cell, at the base and at the head, in two shapes: a Linux-like temp setup (`TMPDIR=/tmp` with a persistent `RUNNER_TEMP`) and this machine's own temp folder. The red cells at the base were exactly the ones named above, and every cell was green at the head.

It also ran its own eleven mutations of the two hunks, written independently: each turned red exactly the cells named for it. It drove request targets the new SCIM file does not cover, and every audit entry carried the mounted path in each:
- a mixed-case mount;
- double slashes, dot and encoded segments, and a matrix parameter;
- absolute-form targets with userinfo, a port or an upper-case scheme;
- a query or fragment on the base path.

gitleaks found nothing in the commits or their messages.

## Named limits (nothing is refused for these)
- A `%40` inside a `data:` payload is kept as sent.
- `blob:data:text/plain,u:p@h` answers `blob:null`.
- A `data:` address written in the authority form (two slashes) keeps an at-sign that follows the authority. This covers a parsed host (`data://h/a@b`), an unparseable one (`data://h:99999/a@b`) and an empty one: `data://@/a@b` answers `data:///a@b`. In every shape the userinfo is dropped. Conforming browsers report any `data:` violation as just `data` (CSP Level 3, "Strip URL for use in reports"), so these values come only from forged reports.
- The hosted `build` job of this pull request is the first run of the two new files on a real Linux machine. A red result there on a new cell is a fix round.

## Deploy
None. The merge touches `backend/` and `__tests__/`, which the Deploy demo workflow does not ignore, so a run starts on the push. Both of its jobs are expected to read skipped because the switch variable is not set.
