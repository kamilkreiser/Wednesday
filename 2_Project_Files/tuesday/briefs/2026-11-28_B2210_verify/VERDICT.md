GATE B2210: GO WITH FINDINGS @ 713cf2d on main c3e87d6

Gate G1, ROUND 1 OF 2 of lane L1x (the OXPd 1.x context calls), one Opus reader (claude-opus-5-5), in-session,
read-only, for Tuesday s338. Kit B2186 (seat X95; S4: Q1 "a" guest IN WORDS, Q2 "a" dry run and undo IN WORDS, Q3-Q9
the defaults; S8 the canonical runner 31adedc8; every choice the coordinator's). Head
`713cf2da1ca1f946cbbb3e30d589ac3d777176c0` on `b2186/x95-oxpd1-context-calls`, ONE commit, one parent
`7ca5e4cefb315f57f4490ce245e1fb762dbf9f6d` (PR 65), tree `e82e14864856433ebddafdb7b06f7446f175bd46`, 784 files;
`diff --name-status 7ca5e4ce 713cf2da`: exactly two rows, both `A` (`src/Datasec.Suite.Adapters.Oxpd1/Oxpd1Context.cs`
+360, `tests/Datasec.Suite.Adapters.Oxpd1.Tests/ContextTests.cs` +441), re-measured by `gh api -X GET` at 04:51:29
(compare ahead 1, behind 0, 2 files added; `matching-refs/heads/b2186` one row = the head; open PRs 0).
**Main MOVED during the gate** (read 05:34:54): PRs 66 (L1 agent host, `249560b9`), 67 (Teams, `46bbf00a`), 68
(SharePoint, `c3e87d6f84ffb7dda611efd192515931a17a9463`, tree `9bdd889e`, 805 files). `compare 7ca5e4ce...c3e87d6f`:
31 files under `src/Datasec.Suite.Adapters.Oxpd1.Agents/`, `tests/...Oxpd1.Agents.Tests/`, SharePoint and Teams only:
NO overlap with the two owned paths, nothing under `src/Datasec.Suite.Adapters.Oxpd1/` or its tests. The gate built the
squash on c3e87d6f (landing.txt).
Measured 2026-11-28 04:51 to about 05:50 AEDT in scratch `fleet/state/s338/g2210/` (`clone`: clone.py `draft`, push URL
`invalid://no-push`, no identity, detached at the head; `wt-checks`: worktree at 7ca5e4ce with the head's two files
staged, its write-tree = the head's tree `e82e1486`; `sq`: c3e87d6f's tarball indexed (control: its write-tree =
main's `9bdd889e`) plus the head's two blobs). Every heavy job through my copy of the kit's `heavy.py` (8 of 8 tool
hashes equal THE TOOLS; heavy.py `31adedc8...` = S8) under the OXPd wave lock, one at a time; released lock folders
in `g2210/_quarantine/locks/`; no other holder's `owner.txt` touched; no time-bound kill (no rc 124), so no orphan to
end. Nothing to any printer, device, tenant, Azure, Microsoft host or HP (every socket was 127.0.0.1 inside a test
process); no Jira; no write to the project checkout, the seat's lane or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 2, Info 6. Nothing blocks landing; no fix round required.

**F1 MINOR (Tuesday's point c; the seat's R17d is a DEFECT, not only a limit): a reserve whose returned id the client's
mask changes throws out of `CallAsync` AFTER the request was sent, with no result and no undo.** FOUND (read):
`Read` checks `IsNonce` on the RAW answer (`Oxpd1Context.cs:312`); then the landed `JudgeGuest` masks the result
(`Oxpd1Client.cs:312`, `Oxpd1Soap.Scrub` puts `[removed:password]` in place of every occurrence of the password and of
the base64 credential); `CallAsync` takes `result.Answer?.Value` (`:294`) and hands it to the undo factory
`ReleaseAuthenticationContext` (`:297`), which throws `ArgumentException` for a text holding `[`. TESTED (probe PB,
`evidence-probes.txt`): setting `Synthetic0001` and a reserve answered with a 32-character nonce ending in it ->
`EXCEPTION ArgumentException out of CallAsync`, stub seen 1; setting equal to the whole nonce -> the same; control
(same setting, a nonce without it) -> `Answered`, id and release of that id; control (setting `removed`, which the
placeholder itself holds) -> `MalformedAnswer` via `Holds` (no throw). NOT TESTED: a real device's nonce alphabet or
the M577's admin password (UNMEASURED). Why a defect: the class's own summary promises "an executed call sends ONE
request and ends in one outcome", and P4 ("a result carries its undo whenever the call may have taken effect"); on
this path a sign-in has been started on the panel and the caller gets neither an id nor an outcome. Trigger is narrow
(the setting's value must occur inside the device's id; a long password makes it vanishingly rare, a short numeric one
against a hex nonce does not), so Minor. Fix shape (in-lane, one line): take the id only when
`Oxpd1ContextCatalogue.IsNonce(result.Answer?.Value)`, else end `MalformedAnswer`, `Applied Unknown`, no id, no undo
(R11's form). The real fix (the id unmasked) is a client change, OX-A's path.

**F2 MINOR (Tuesday's point a; the kit's Q1 cost text is wrong): the "guest" credential carries the device ADMIN
password's value.** FOUND (read): `SendGuestAsync` reads `_options.AdminPasswordSetting` (`Oxpd1Client.cs:142`) and
sends `Basic base64("guest:" + that value)` (`:149`, `:162`). TESTED (probe PA1, each of the six executed): user word
`guest` 6 of 6, scheme Basic, ONE request each, and the password half equal to the client's AdminPasswordSetting value
6 of 6. So the user is the least credential, but the secret on the wire is the admin password in every case; the
kit's Q1 alternative b's cost ("the admin password then travels on every sign-in and card call") is equally true of
the built default a. Mitigated: the request goes only to the pinned device (no redirect followed, PA3), which owns that
password. HP's "password={anything}" for guest is quoted in the landed echo summary (`Oxpd1Echo.cs:174`) and module
README, not in any committed contract file (`grep -rn -F 'password={anything}'` over `contracts/`: 0 rows; control:
`src/` 4 rows). The landed guest sender's choice (PR 51), not a line of this commit; this lane multiplies its uses
(every sign-in and card call of lane L1). For the coordinator: an OX-A item (a separate, non-secret guest value), and
a correction to the Q1 reasoning in the records.

**F3 INFO (Tuesday's point a): no path sends without `Execute`; no credential but guest's.** FOUND (read): the only
network call is `_client.SendGuestAsync(` (`Oxpd1Context.cs:287`), after `if (!call.Execute)` (`:282`); the envelope
and URL built before it touch no setting and no socket; checks_l1x check 7: `SendAdminReadAsync(` 0, `SendWriteAsync(`
0, `HttpClient` 0, `.Authorization` 0. The only public surface (PA4, reflection): `Oxpd1ContextCaller(Oxpd1Client)` +
`CallAsync`; `Oxpd1ContextCall` constructors private (the record's copy constructor private), its only setters the
init-only `Execute` and `CallbackTimeoutSeconds` (checked in `init`), so `with` cannot change a kind or an id;
`Oxpd1ContextResult` constructor internal. The caller's one field is `readonly Oxpd1Client _client`: no state across
calls. TESTED: PA2 each of the six dry -> seen 0, setting reads 0; each undo as returned (`Execute` False) sent through
`CallAsync` -> still a dry run, seen unchanged; PA3 a 307 to a second stub -> `HttpStatus 307`, `Unknown`, undo close,
second stub seen 0 (no credential forwarded); PA5 two concurrent reserves on one caller -> both `Answered`, each its id,
seen 2. Mutants `mDryRunSends`, `mAdminUser` and the gate's `gUndoSentByDefault` (undo made with Execute true) each
turn their cells red.

**F4 INFO: a caller's cancellation while an executed call is in flight throws, after the request left.** TESTED (PA6):
executed open, the caller cancels at 0.5 s, the stub answers at 2 s -> `TaskCanceledException`, stub seen 1, no
result, no undo. The landed `SendAsync` maps only its own time-out to `TimedOut` (`Oxpd1Client.cs:190`), as for every
write. Not a defect of this lane (the writer has the same form); owed to lane L1: an exception from an executed open
or start means "may have taken effect" (the host holds the accessory id and can send the close / stop).

**F5 INFO (Tuesday's point b): every partial or variant nonce form is refused; case variants are accepted by design.**
TESTED (probe PB, 51 shapes, each one request): ACCEPTED with that id and its release: 32 mixed, 32 lower, 32 upper, 32
digits, 33, 127, 128, and four XML encodings of the same 32 ASCII characters (split by a comment, by a processing
instruction, in CDATA whole or in part, with a character reference): the parser drops comments and PIs
(`Oxpd1Soap.cs:105-106`) and the text is the same id, so correct. REFUSED as `MalformedAnswer`, `Applied Unknown`, no id,
no undo: 129, 256, 4096, 200000 (and 2000000 -> `TooLarge` at the 1 MiB bound); a valid nonce followed by `-tail`, by
` word`, by 128 more letters (prefix matches); trailing space, tab, LF, CR LF, leading space, LF both sides, trailing
U+00A0, U+200B, `&#0;`; 32 fullwidth A, e-acute, Arabic-Indic digits, Cyrillic a, Kelvin sign; `&amp;` inside;
`xsi:nil` or `xml:space` on the result; two results; the result unqualified, or in a lookalike namespace; the response
in a lookalike namespace; an empty result; two bodies; a good answer with status 500 (`MalformedAnswer`) or 202
(`HttpStatus`); a fault at 200 (`Fault`). The response prefixed in the right namespace is accepted (correct). HP's
`Nonce` restricts `xs:string` (whitespace preserve; `common.xsd:576-579`), so refusing surrounding white space is HP's
own rule, not over-strict. Under the gate's `gReadKeepsAnyText` (the nonce test removed from `Read`) N05 goes red.

**F6 INFO: a fault code is passed on unscrubbed of ids (seat R17e, confirmed).** TESTED (PC1): an open faulted with the
accessory id as the code value -> `FaultCode` holds the id True, the result's `ToString` holds it True. The code is the
device's own text, scrubbed of the password only (as for every landed write). Named limit; P6 holds for every text the
class itself makes (N10, `mIdInToString`, the gate's `gResultToStringId`).

**F7 INFO: argument shapes beyond N09 (seat R17b, R17f confirmed).** TESTED (PD): accepted: callback IPv6 literal,
port 0, loopback IPv4 port 1, `%40` in the path, a fragment, plain http, exactly 256 characters, server context id of
256, an all-ones agent id; refused: a surrogate pair or a lone surrogate in the server context id (per UTF-16 unit),
a fullwidth or space-trailed context id. A callback holding `\@` never reached the factory (`new Uri` throws
`UriFormatException`): not tested. The callback is the device's report target chosen by the host; the same test as
the landed echo (`Oxpd1Echo.cs:121-122`). Named limits, as the seat says.

**F8 INFO (the seat's D-2: mutants and the pin not re-run after the rebase): covered by this gate.** On the pushed head
713cf2da the gate ran the pin (OXPd 1.x `Total: 172, Errors: 0, Failed: 0`), the whole solution (`total: 2603`,
`failed: 0`, `succeeded: 2599`, `skipped: 4`), and all eight kit mutants plus eight of its own. `mHidCloseUndoLost`
also reds N10 (its `Assert.NotNull(open.Undo)`), inside the suite's cells: MATCH by the tool's rule, as the seat says.

## The kit's gate list, each question

| Question | Answer | How |
|---|---|---|
| `<BASE>..<head>` read whole | yes: 2 files, both A, 801 added lines | Read tool, both files whole; `diff --name-status` |
| the pin run and each mutant's reds | pin 172/0 failed; MUTANTS 16 of 16 MATCH, 16 of 16 undone equal (kit's 8 + gate's 8); post-mutants rebuild 172/0 | `mutants_c3.py run` through heavy.py; `evidence-mutants.txt`, rows `evidence-gate-mutant-rows.json` (sha256 91271829...; the kit's 8 rows equal the seat's rows file: True) |
| any of the six sent without `Execute` | no | F3 (read, PA2, mDryRunSends, gUndoSentByDefault) |
| a credential other than guest's | user always guest; its password is the admin setting's value | F2 (PA1), F3 |
| a reserve returning an id not of HP's nonce form | no id ever returned that is not a nonce; but one path THROWS instead (F1) | F5 (51 shapes), F1 |
| a refused call carrying an undo | no | N07 green; `mForbiddenApplied`, gate `gUndoOnRefused` red N07 |
| a ToString or fault code carrying a context id, agent id or password | none the class makes; a device's own fault code can (F6) | N10, mIdInToString, gResultToStringId, PC1 |
| a comment asserting a device behaviour as fact | none: every HP statement cites the wsdl (quotes re-found: "reset button press" 2 rows, "explicitly stopped before closing" 1, "Must use an HTTP or HTTPS scheme" 2); every device answer is labelled an ASSUMPTION or UNMEASURED; the guest-password quote's source is the landed echo, not a contract file (F2) | grep -o -i -c over the committed descriptions |
| the hosted run on both legs | `HOSTED 713cf2da...: PASS` at --total 2603 --rules 784, guards 28/29; control `--total 2604` -> FAIL 4 rc 1 | gate's hosted3.py (`evidence-hosted-head.txt`) |
| words.py and gitleaks over the added lines and the message | `CONTROL FIRED: 13 of 13`; `WORDS: clean (2 files)`; B-number count 0 and 0 (control: the kit 19); gitleaks control rc 1 (leaks found 1, moved to quarantine), the two blobs + message rc 0, `gitleaks git` over 7ca5e4ce..713cf2da rc 0 | gl-control, gl-scan, gl-git in scratch |
| checks_l1x.py | `CHECKS: 9 of 9 PASS`, every control FIRED (staged tree over 7ca5e4ce) | `g2210/checks/` |
| CodeQL | NOT RUN locally (kit FACTS 6); the PR's own run is the check; main c3e87d6f csharp/python/actions results 0, open alerts 0 | gh api GET |

## Tuesday's own points
- (a) F3 (no path without Execute; only SendGuestAsync; no redirect followed) and F2 (the guest password is the admin value).
- (b) F5: every partial, padded, over-long or Unicode-lookalike form refused, printed per shape; ASCII case variants accepted (HP's pattern allows both cases).
- (c) F1: a defect (Minor), not only a limit.

## NOT TESTED
Anything against a device; CodeQL locally; the seat's R12 (an undo of a call that did not take effect) beyond reading
HP's text; the `\@` callback shape (see F7); a whole-solution hosted run of the squash on c3e87d6f (the PR's run is that).

## Landing texts (this folder)
landing.txt (squash on c3e87d6f MEASURED: tree 8cd196ac, 807 files, whole solution 2739 / failed 0 / succeeded 2735 /
skipped 4, OXPd 1.x 172 / 0; expect 8 distinct check names; nothing deploys: ci.yml read by GET), pr-title.txt,
pr-body.md, squash-subject.txt (`#PRNUM`), squash-body.txt, FOR-RECORDS.md; evidence-*.txt/json. words.py over the
subject (with #69), squash-body.txt and pr-title.txt: 0 hits; pr-body.md names the coordinator once (as the B2194 and
B2196 bodies do); gitleaks over the subject, the squash body and the PR body rc 0. At the end: wave lock free, no
process of this gate running, scratch clone porcelain 0 rows (probe file moved to g2210/_quarantine/probe-file/).
