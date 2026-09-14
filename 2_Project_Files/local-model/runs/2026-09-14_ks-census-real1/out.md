identifier | title | state name | state type | priority | assignee | updatedAt
KS-764 | Security: decideKeyRevoke has no organisation arm \u2014 an ORG_ADMIN can revoke a sibling orga | Done | completed | High | kamil.kreiser@secuura.ai | 2026-09-14T02:01:52.931Z
KS-773 | lockfile-cleanroom skips services/mcp-server for a reason its lock refutes \u2014 leg 2/9 claim | Done | completed | Medium | kamil.kreiser@secuura.ai | 2026-09-14T02:26:14.068Z
KS-777 | QA pass F-1/F-3/F-4/F-7: two vacuous guards, an unasserted statement tail, and an un-norma | Todo | unstarted | Medium | kamil.kreiser@secuura.ai | 2026-09-05T23:52:44.776Z
KS-780 | Two implementations of organisation-id normalisation, in two layers \u2014 move normaliseOrgId | Done | completed | Medium | kamil.kreiser@secuura.ai | 2026-09-14T03:12:48.859Z
KS-790 | OAuth authorization_code token exchange uses getUserById (post-auth) in a pre-auth flow \u2014 | Done | completed | High | kamil.kreiser@secuura.ai | 2026-09-13T23:01:39.428Z
KS-798 | The consent page posts the redirect URI in the client_id field \u2014 nobody can complete the O | In Review | started | High | kamil.kreiser@secuura.ai | 2026-09-14T03:09:08.608Z
KS-799 | The OAuth consent page cannot submit its own form \u2014 CSRF answers 403 before the route is r | In Review | started | Medium | kamil.kreiser@secuura.ai | 2026-09-13T23:16:33.905Z
KS-823 | Security: the /api/oauth/token `refresh_token` grant authenticates NO client \u2014 a confident | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-14T00:47:41.388Z
KS-835 | Security: OAuth consent is decorative \u2014 the granted scope never reaches the token, and the | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-14T00:47:40.987Z
KS-841 | Security: the rendered OAuth consent page cannot POST itself back \u2014 it emits the redirect | In Review | started | High | kamil.kreiser@secuura.ai | 2026-09-14T03:09:08.609Z
KS-926 | 17 of 20 `check-*.sh` guards run from NO live entry point \u2014 including SQL-injection and tr | Done | completed | High | kamil.kreiser@secuura.ai | 2026-09-14T02:17:17.298Z
KS-961 | The aggregate workspace suite never runs on a PR \u2014 wire it advisory (Kam: wire-nonblocking | In Review | started | Medium | kamil.kreiser@secuura.ai | 2026-09-14T02:41:35.124Z
KS-991 | A stale LOCAL `develop` runs the full platform preflight on an unrelated branch, which the | Done | completed | High | kamil.kreiser@secuura.ai | 2026-09-13T23:19:21.216Z
KS-1004 | A document with a txHash can never be marked anchor-failed \u2014 NOR healed forward to confirm | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-13T21:58:24.098Z
KS-1046 | `PREFLIGHT PASSED.` is printed identically whether 13 legs ran or 10 \u2014 the verdict has no | In Review | started | High | kamil.kreiser@secuura.ai | 2026-09-14T03:12:43.304Z
KS-1059 | anchorStateSync.ts:360 \u2014 removing `inFlight &&` from the KS-587 sim leg reddens 0 cells, o | In Review | started | Urgent | kamil.kreiser@secuura.ai | 2026-09-13T22:06:53.523Z
KS-1061 | F-926-2: all ten originate @secuura/shared mock factories were partial \u2014 build them from t | In Review | started | Medium | kamil.kreiser@secuura.ai | 2026-09-14T02:49:19.827Z
KS-1075 | CI gates: both PR security gates fail for CONFIG reasons, not findings \u2014 tsx driver missin | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-14T02:42:06.736Z
KS-1077 | Two npm-audit allow-lists disagree: CI's is EMPTY and cannot express an advisory-less carr | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-13T21:58:04.184Z
KS-1078 | SUPPLY CHAIN: the Code Security Gates job downloads an UNPINNED package from npm and execu | In Progress | started | Urgent | kamil.kreiser@secuura.ai | 2026-09-14T02:57:00.823Z
KS-1148 | CI-runner environment gaps (one class, two jobs): `Security Scanning` runs `audit:contract | Backlog | backlog | High | kamil.kreiser@secuura.ai | 2026-09-14T02:41:33.746Z
KS-1149 | A push whose pre-push gate runs past ~6 min dies with rc 141 after the gate PASSED \u2014 GitHu | Backlog | backlog | High | kamil.kreiser@secuura.ai | 2026-09-14T01:13:12.016Z
KS-1150 | OAuth /token grant hardening (measured by the #982 gate, pre-existing): the authorization_ | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-14T01:08:43.294Z
KS-1151 | Security: POST /api/auth/refresh re-mints an OAuth-bound refresh token as an UNBOUND, full | In Progress | started | High | kamil.kreiser@secuura.ai | 2026-09-14T00:58:14.882Z
KS-1152 | L5 gate records (#799/#880/#985): jwt.ts citation \u00d75, security log title, dist typeof disc | Backlog | backlog | Medium | kamil.kreiser@secuura.ai | 2026-09-14T01:54:16.221Z
KS-1153 | L7 gate records (#918/#924/#925): run-code-guards.sh --check-unreached advisory arm unpinn | Backlog | backlog | Low | kamil.kreiser@secuura.ai | 2026-09-14T02:10:03.622Z
KS-1154 | Root package-lock.json carries only rollup-darwin-arm64 \u2014 npm ci on ubuntu installs no Lin | Backlog | backlog | Medium | kamil.kreiser@secuura.ai | 2026-09-14T02:41:32.394Z
counts: backlog=5, completed=6, started=16, unstarted=1
