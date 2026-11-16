## Summary

- **RD-771** (CodeQL js/incomplete-url-substring-sanitization, four alerts): `static/js/index.js` and `static/js/settings.js` decided `IS_PRODUCTION` by asking whether the host name *contains* `azurewebsites.net` or `azure-api.net`. They now ask whether it *ends with* `.azurewebsites.net` or `.azure-api.net`, the form the setup page already uses. The third clause (a host without `localhost` is production) is byte-equal, so the answer moves only for host names that contain `localhost` and merely contain a cloud domain; for those, debug logging now stays on. `127.0.0.1` reads as production before and after (unchanged here).
- **RD-805** (alerts #145 and #146, defence in depth): the Entra connection test (`POST /api/setup/entra-provisioning/test`, graph mode) builds the sign-in address from the stored tenant id and each directory address from a stored group id. A stored tenant id that is not a GUID now gets the route's existing not-configured answer, with no token request. A stored group id that is not a GUID is not requested; its row reads `ok: false` with the save route's existing words, "Invalid Entra group ID", and the loop goes on. The check is the provisioning service's own exported GUID pattern (anchored, fixed width, no new pattern). A GUID tenant and GUID groups take the same requests and get the same answers as before.
- Test counts regenerated: 5846 tests in 376 suites (was 5828 in 374): two new suites, 18 cells.

No new user-facing sentence, no route or permission change, no migration, nothing deployed.

## CodeQL

A local CodeQL 2.27.4 run (security-extended and code-scanning suites) on the base and on this head: the four RD-771 rows are gone, no new row in either suite, every other row unchanged. #145 and #146 are still reported: CodeQL does not read the GUID check as a barrier, so this change hardens those paths without closing those alerts. Main's analysis of the merge commit decides the tickets. The other RD-805 and RD-804 rows (Log Analytics query body, Monday GraphQL variables, Marketplace activate body, Graph checkMemberGroups body) are stored configuration sent as the body to a fixed service. They are left open and unchanged, and no alert is dismissed.

## Test plan

- [x] New `__tests__/rd771-static-page-production-host.test.js` (9 cells): each page's own statement over an 18-host table; red at the base on the changed cells, green on the pins.
- [x] New `__tests__/rd805-entra-test-route-guid-path-parts.test.js` (9 cells): GUID control, four non-GUID tenants (byte-equal not-configured answer, zero requests), non-GUID group beside a GUID group (one request, existing words); red at the base on the changed cells, green on the pins.
- [x] Related suites green; role-capability inventory `--check` 203/203; full `npm run verify -- --maxWorkers=2` PASS 5846/376 on this head.
- [ ] Hosted Build and CodeQL on this PR.
- [ ] After merge: CodeQL on main shows the four RD-771 rows fixed; the Deploy demo run reads skipped.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
