GATE B1990: GO WITH FINDINGS @ 85e414d on main df762b2

Gate G1 (security surface: the admin password's path into the record), **round 3 of lane X1 (CodeQL at landing)**, one
Opus reader (claude-opus-5-5), in-session, read-only. Kit B1988 (seat X52; stamp S4: the lane stays open, Q1 = a in
words; the round opened by the product owner's ruling of card `datasec-oxpd-x1-codeql-round3-1123` = "Fix round now",
14:41:39; every direction inside it the coordinator's). Head `85e414d66dcd7336aaa13307a3d57a2438f6e50e` on
`b1976/x1-oxpd1-read-client` = ONE commit on `8f5813bf` (HEAD2). Read and measured 2026-11-23 15:23 to 15:45 AEDT
(clocks by `date`) in my own scratch `fleet/state/s316/g1990/`: `clone` (the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity; detached at the head; green, mutants, whole solution), worktrees `red` (HEAD2 +
`3-red.diff`, then + `4-fix.diff`), `mg` (`read-tree -m -u` to the merge with main), `probe` (the head + gate B1987's
probe unchanged + this gate's frame probe, never committed), `h2` (HEAD2 + gate B1987's probe, for a cost comparison).
Every dotnet job through the kit's `heavy.py` (sha256 `31adedc8...`, my copy) and the wave lock, ONE at a time (lock
waits 0 on every job; load1 3.3 to 6.9 at each job's start; one wait of load1 19.2 to 8.6 at 15:35 to 15:36 before
`mg-restore`); no other holder's lock touched; the lock absent at the end; 85 released lock folders in
`g1990/_quarantine/locks/`. Origin by `gh api -X GET` under the project GH_CONFIG_DIR at 15:26:51 and again at 15:41:00,
unchanged: main `df762b28`; `matching-refs/heads/b1976` one row `85e414d6`; `b1988`, `b1990` 0 rows; pull request 37
open, head `85e414d6`, base `df762b28`, mergeable true, `clean`; pull requests from the branch: 37 only; repository
private, push true. No write to the project, GitHub or Jira; no push, no pull-request edit, no re-run, no alert touched;
nothing deleted.

**BLUF.** The three CodeQL alerts are closed in code and CodeQL itself says so: pull request 37's csharp analysis of
`85e414d6` reads results 0 (CodeQL 2.27.5; the control, the analysis of `8f5813bf` on the same ref, reads 3), the
`CodeQL` check is success, alerts 1 to 3 read `fixed` on `refs/pull/37/head` (instance `fixed@8f5813bf`, none at the
head), the dismissed list is 0 and no suppression text is in the lane. Alert 3 is closed by a real change to what the
record holds (the setting's name is gone from the template and the arguments: re-measured on nine outcomes, none names
it). Alerts 1 and 2 were the query's name heuristic reading the non-secret replacement text as a password lookup; the
fix changes how that text is produced (a `static readonly` field instead of `DenyList.ReplacementFor("password")`), the
bytes a reader sees are unchanged, and no secret flows along that path before or after (FOUND 1, Info). The commit is
the two frozen patches byte for byte (HEAD2 + both = the head's tree `8cf35b46`). Red first reproduces (23 / 2, K15 and
K16, each an assertion); my independent mutant run reads 31 of 31 MATCH and undone; whole solution 1927 / 0 / 1923 / 4,
RULES 617, Ran 111; the merge with main df762b28 (tree `56867d5d`, equal to the pull request's own merge commit
`26213ac7`) 1942 / 0 / 1938 / 4, RULES 628. Gate B1987's FOUND 1 is FIXED, re-measured with that gate's own N probe:
the 25 escaped-character rows that read `Answered` at `8f5813bf` all read `MalformedAnswer` at the head, the 12
controls are unchanged, the other 63 probe rows are equal; FOUND 3 is FIXED (the bullet is gone); FOUND 2 is narrowed in
the README only. **Two documentation findings remain, neither a Blocker** (FOUND 2 Minor, FOUND 3 Info).

## FOUND (for the product-owner card: Blocker none; Minor-ship-with-ticket one (FOUND 2); Info two (FOUND 1, FOUND 3))

1. **Info (how alerts 1 and 2 were closed; the commission's "not by hiding it" test): the fix changes the SOURCE SHAPE
   of non-secret text, and that is the honest fix here, not a dodge.** The query library (`codeql/csharp-all` 7.4.2
   `semmle/code/csharp/security/SensitiveActions.qll`, read here; the hosted analysis ran 2.27.5) makes a source of any
   method call one of whose arguments has a constant value matching `%password%` (`SensitiveMethodAccess`,
   `isSuspicious(this.getAnArgument().getValue())`). At HEAD2, `Scrub` replaced each secret with
   `DenyList.ReplacementFor("password")`, whose value is the literal `[removed:password]` (`DenyList.cs:53`,
   `"[removed:" + className + "]"`); the query called that call's RESULT sensitive and followed it through
   `string.Replace` into `request` and `shown` at `Oxpd1Client.cs:238`. The head uses `Oxpd1Soap.Placeholder`
   (`Oxpd1Soap.cs:31`, `internal static readonly string Placeholder = "[removed:password]";`): the same bytes, from a
   field whose name matches no pattern and whose access carries no constant value. So for alerts 1 and 2 the record's
   bytes are UNCHANGED, and only the provenance of a non-secret placeholder changed. Why that is not "a rename whose
   only effect is to dodge a name pattern while the same value flows": the value that flows is not sensitive; the
   password itself never reached the record along that path at HEAD2 or at the head (Replace's OLD value, the secret,
   is what is removed; my probe and gate B1987's: every one of the 124 probe rows that scans a record reads clean: 64 in gate B1987's probe, 60 in mine). The alternative,
   dismissing two false positives, is forbidden by the rule. No suppression comment, attribute, `lgtm`/`codeql`
   marker, `SuppressMessage` or `#pragma` in the lane's `src/` or `tests/` (`git grep -i` count 0; control `Oxpd1Soap`
   in `Oxpd1Client.cs` 10); no `.github/**` or `build/**` path in the diff (`git diff --stat` 0 lines). The shape is
   pinned: K16 asserts `IsInitOnly && !IsLiteral` and byte-equality with the deny-list's text; mutants
   `mPlaceholderConst` and `mPlaceholderText` each redden K16 alone (my run). Alert 3 is different in kind: the record
   no longer carries `_options.AdminPasswordSetting` at all (template and arguments at `Oxpd1Client.cs:237` to `:239`,
   printed below). **No ticket needed;** recorded so the next reader knows two of the three alerts were heuristic.

2. **Minor, documentation, ship with a ticket (P4; residual of gate B1987 FOUND 2): the public XML doc of
   `Oxpd1ClientOptions.Timeout` still says the time-out bounds the whole call.** `Oxpd1ClientOptions.cs:86` to `:87`
   (unchanged by this commit, printed by `git grep -n` at the head): "The time one call may take, connection and answer
   included: positive, finite and at most `MaxTimeout`". The README this commit narrowed now says the opposite, correctly
   (`README.md:46` to `:50`: the connection, the request and the body read are bounded by `Timeout`; the parse, the
   mask and the record after the body are not). MEASURED here, the same input as gate B1987's K7 (90,000 attributes on
   one element, 889,180 bytes, `Timeout` = 1 s), alternated under the same load: head 8,764 ms and 6,786 ms, HEAD2
   8,913 ms and 9,306 ms (`Answered` each), so the namespace walk this commit adds costs nothing measurable and the
   README's "can take seconds" holds. An IntelliSense reader of the options sees the old, false promise. **Why not a
   Blocker:** one sentence of a doc comment, no code path; the behaviour is finite and fail-closed and the README is
   right. **Ticket:** narrow that summary to the README's words with the named follow-up (a cap on attributes per
   element, or the time-out token inside the copy).

3. **Info, documentation precision (P3 frame): "it names no setting" (`Oxpd1Client.cs:36`, `README.md:33`) and
   "Neither the name nor the value is recorded" (`Oxpd1ClientOptions.cs:59`) hold for every field the library itself
   writes, but the record also carries the device's masked answer, which can hold any text the device sends.**
   MEASURED (this gate's frame probe, R1 to R10, a synthetic setting name, record on): NoCredential, the tree answered,
   a SOAP read answered, a Fault 500 whose code holds the password, TimedOut, PinRefused, MalformedAnswer, HttpStatus
   404, the tree with the setting missing: the record names the setting in 0 of 9 rows, the word `SettingName` 0 of 9,
   the record scan clean 9 of 9 (the fault code reads the placeholder, never the password). R10, a device whose answer
   echoes the setting's NAME in a note: `Answered`, and the record holds the name (it is the device's text, inside the
   masked answer). The name is not a secret (CodeQL flagged it by its own name pattern, alert 3); the VALUE is never
   recorded in any row. **No ticket needed;** a future README line could say "the library writes no setting name; a
   device's answer is recorded as masked".

## THE GATE LIST OF THE KIT (B1988 FOR TUESDAY, verbatim items; each MEASURED here)

- **`8f5813bf..<head>` read whole.** `git diff --name-status 8f5813bf 85e414d6`: exactly 5 rows, all `M`:
  `src/Datasec.Suite.Adapters.Oxpd1/{Oxpd1Client.cs, Oxpd1ClientOptions.cs, Oxpd1Soap.cs, README.md}` and
  `tests/Datasec.Suite.Adapters.Oxpd1.Tests/ClientTests.cs`; nothing under `contracts/oxpd1/`, `src/Datasec.Suite.Logging/`,
  no slnx, no lock file. Head ONE parent `8f5813bf`, tree `8cf35b4624c10ca1790fb43bc772aff88e2e17fa` (GET and local).
  I read the whole diff and `Oxpd1Client.cs`, `Oxpd1Soap.cs`, `Oxpd1ClientOptions.cs` whole at the head, and K15/K16
  (no existing line of `ClientTests.cs` changed: +106 / -0). At the head, printed by `git show`:
      237:         _recorder.Information(
      238:             "OXPd 1.x read {Read} {Url} ended {Outcome} {Status}; request {Request}; answer {Answer}",
      239:             name, url.AbsoluteUri, outcome.ToString(), status, request, shown);
      Oxpd1Soap.cs:31:     internal static readonly string Placeholder = "[removed:password]";
- **The two patches against the commit by sha256.** My `gate/` is a copy of the kit's `<src>`
  (`fleet/state/s316/d1988/seat-tools/`): 12 of 12 sha256 equal to THE TOOLS (`3-red.diff` `47b7edd1...`, `4-fix.diff`
  `bfde370d...`, `commit-message.txt` `3f47a1bb...`, and the nine programs). In `red` (HEAD2): `apply --check` and
  `apply` of `3-red.diff` rc 0, then of `4-fix.diff` rc 0, `add -u`, `write-tree` = `8cf35b46...` = the head's tree:
  **EQUAL**. THE CODE's 5 files at the head: 5 of 5 equal to the kit's sha256 and line feeds (241, 114, 295, 81, 502).
  The stored message equals `commit-message.txt` byte for byte (254 bytes; `%B` adds one line feed).
- **The red first (2 of 23).** `red-restore` rc 0, lock files unchanged; `red-build` `0 Warning(s)`, `0 Error(s)`;
  `red-exe` **`Total: 23, Errors: 0, Failed: 2`**: `K15_... [FAIL]` / `character 38 N1 an unused prefix: Answered`;
  `K16_... [FAIL]` / `Assert.DoesNotContain() Failure: Sub-string found` (= THE CONTROLS); lines with "exception" 0.
  `g1990/logs/red-exe.log`.
- **Each mutant red on its cells (an independent run).** At the head (`g-exe` 23 / 0 first): `mutants_x3.py
  <g1990/clone> g1990/scratch/mutants run g1990 'B1990 gate g1990'`, one call, rc 0, every row `Total 23`:
  **`MUTANTS: 31 of 31 MATCH, 31 of 31 undone equal`** (`g1990/logs/mutants-run.log`; every row equal to the seat's;
  mDtd the named survivor, NONE; the seven new rows: mNsWalkOff, mDeclValueOff, mElementNsOff, mAttrNsOff K15 alone;
  mSettingBack, mPlaceholderConst, mPlaceholderText K16 alone). After it: `status --porcelain` 0 lines; `post-build`
  0 / 0, the library dll 15:34:19 later than the newest source (`Oxpd1Soap.cs`, 15:34:18); `post-exe` 23 / 0.
- **K15's 45 rows against the gate's own N probe at the head.** Gate B1987's `G1987Probe.cs` unchanged (sha256
  `d0e451c4...`, equal to its copy), built 0 / 0 in `probe` at the head beside this gate's `G1990Probe.cs`, run whole:
  `Total: 25, Errors: 0, Failed: 0` (the 23 cells and the two probes). Its 42 N rows beside its own output at
  `8f5813bf` (`g1990/scratch/ncompare.py`): the **25 escaped-character rows (N1 to N5 x `&`, `<`, `"`, LF, tab) read
  `Answered` at `8f5813bf` and `MalformedAnswer` at the head, 25 of 25**; the 5 plain-password rows `MalformedAnswer` at
  both; the 12 controls (text node, attribute value) `Answered` at both, no read of the answer holding the password
  (`ToString`, `OmitDuplicateNamespaces`, `Value`, names/namespaces, declaration value, raw attribute value, `WriteTo`
  with either new-line handling, the result's text, the fault code); record scan clean in all 42. Mapping to K15: probe
  N1 to N5 = K15 N1 to N5 (25 rows, same five characters, same shapes); probe N6/N7 = K15's two controls (10 of its
  rows); K15 N6/N7 (declared above the result, 10 rows) are beyond the probe, and this gate's U2/U3 extend them
  (declared on the Response element, used three levels below the Result or by the Result's own attribute: 10 of 10
  `MalformedAnswer`). The probe's other 63 lines (61 rows of sections A to F, P and K, and two marker lines) equal its `8f5813bf` output with
  timings removed, 63 of 63.
- **Whether any other path stores the setting's name or a constant keyed on a password word (the query library's two
  source shapes, over the lane's `src/` and `tests/`).** `g1990/scratch/shapes.py` (the qll's `suspicious()` and
  `nonSuspicious()` patterns, comments left out) over the 8 `.cs` files at the head. **`src/`:** identifiers:
  `password` (the local of `Oxpd1Client.cs:64`, `:73`, flowing to `basic`, `secrets` and the Authorization header only),
  `AdminPasswordSetting` (read only as the argument of the caller's `_readSetting` at `Oxpd1Client.cs:64`, `:73`; stored
  at `Oxpd1ClientOptions.cs:50`, declared `:60`), `adminPasswordSetting` (the constructor parameter, `:22`, `:26`, `:50`);
  string literals matching a pattern: ONE, the `Placeholder` initializer (a field initializer, not a call argument);
  `DenyList.ReplacementFor(` 2, both with a variable (`Oxpd1Soap.cs:243` `attrClass`, `:249` `elementClass`); no
  `const string` with a matching value (9 consts, none matches). The sinks: one `_recorder.Information(` (`:237`, its
  six arguments above); the 7 `throw new` sites hold fixed text (`Oxpd1ClientOptions.cs:29`, `:34`, `:42`, `:76`, `:95`,
  `Oxpd1Read.cs:86` adds the enum value, `Oxpd1Soap.cs:230`); no `Console`, `Debug`, `Trace`, `ILogger` or file write;
  the 14 `new Oxpd1ReadResult(` carry outcome, status, the masked answer, the record count and the scrubbed, cut fault
  code; `Oxpd1ReadResult.ToString` is outcome, status and fault code. So no other path stores the name or the password.
  **`tests/`:** `DenyList.ReplacementFor("password")` once (`ClientTests.cs:456`, K16, into `Assert` only),
  `PlantedRecordPassword` and `Password` in the stub (synthetic), literal `"[removed:password]"` in K12; CodeQL reads
  them clean (results 0).
- **`pr37.py` at the head (CodeQL success, results 0, the three alerts not open).** My copy, no `--wait` (all
  completed), 15:26:30: 12 runs under 8 names, every `CHECK` row `OK`, `OTHER NAMES: none`, `ANALYSIS
  /language:csharp | id 2226791285 | results 0 | tool 2.27.5`, actions and python 0, `CONTROL csharp analysis of
  8f5813bf results 3 (must be 3): FIRED`, `OPEN ALERTS on refs/pull/37/head: 0, of rule
  cs/cleartext-storage-of-sensitive-information: 0`, alerts 1 to 3 `instances on the ref 1 (fixed@8f5813bf); at 85e414d6
  0`, last line **`PR37 85e414d66dcd7336aaa13307a3d57a2438f6e50e: PASS`** (`g1990/logs/pr37/`). Beside it (GET): the
  `fixed` list on the ref holds 1, 2, 3; `dismissed` 0; each alert's `dismissed_by` and `dismissed_reason` null; main's
  alerts (all states) 0; main's csharp analysis of `df762b28` results 0.
- **The hosted push and pull-request runs.** `hosted3.py` (my copy, GET only, all completed): push run 45110633670 at
  `--total 1927 --rules 617 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan`: **`HOSTED
  85e414d6...: PASS`** (linux 1927 x2 / 1923 / 4, GUARD 10; windows 1927 x2 / 1906 / 21, GUARD 11; RULES 617).
  Pull-request run 45110640672 at `--total 1942 --rules 628 ... --guard-linux 14 --guard-windows 15`: **`PASS`**
  (linux 1942 x2 / 1938 / 4, GUARD 14; windows 1942 x2 / 1921 / 21, GUARD 15; RULES 628; secret-scan hardened rows OK,
  NEUTRAL-SCAN 1596 objects, `objects of this commit not among them 0`). Every job attempt 1. **Which tree the
  pull-request run built:** `pr_retrigger.sh --check datasecau/OXPd_2 45110640672 85e414d6... df762b28...` (read
  mode): `HEAD is now at 26213ac Merge 85e414d66dcd... into df762b287a89...`, `MATCH`; commit `26213ac7` (GET):
  parents `df762b28`, `85e414d6`, tree `56867d5d` = my `merge-tree`. K15 and K16 ran green on both hosted legs (the
  totals moved by exactly 2 from HEAD2's 1925 and 1940, the skips unchanged; DERIVED, the legs print no per-cell list).
- **`words.py` and gitleaks.** `words.py --control` `CONTROL FIRED: 13 of 13`; over the 168 `+` lines of
  `8f5813bf..85e414d6` and the stored message: `WORDS: clean (2 files)`. gitleaks 8.30.1 `--no-banner --redact
  --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token built by program, never printed, scanned alone): rc 1,
  `leaks found: 1`, moved to `g1990/_quarantine/` (a first control I built read rc 0 because its random characters fell
  outside the rule's base-32 alphabet; it was quarantined, rebuilt, and every scan below re-run after the firing
  control: DEVIATIONS 2); `dir` over 9 neutral files (the 5 head blobs, the two patches, the stored message, the added
  lines): rc 0, `no leaks found`; `git --log-opts=8f5813bf..85e414d6`: `1 commits scanned`, rc 0, `no leaks found`;
  `dir` over the clone at the head: rc 0.

## WIDER (commission item 2)

- **Closed by a change to what the record holds, not by hiding:** FOUND 1 (alert 3 a real change; alerts 1 and 2 a
  provenance change of non-secret text; no suppression; no `.github`/`build` change; CodeQL's own read is the proof).
- **Any other path storing the name, the password or a password-keyed constant into the record, a log, an exception or
  the returned answer:** none (the source-shape list above). MEASURED on every outcome the single sink writes (frame
  probe R1 to R9: no name, record clean) and on the 124 probe rows that scan a record (0 unclean).
- **The scrub text a reader sees is byte-equal to before (`[removed:password]`):** HEAD2 produced
  `"[removed:" + "password" + "]"` (`DenyList.cs:53`, a path this commit does not touch: `diff 8f5813bf 85e414d6 --
  src/Datasec.Suite.Logging` 0 lines); the head's `Placeholder` is that literal; K16 compares them by reflection
  (green). MEASURED at the head (frame probe S1 to S5 and R4): an attribute value, joined CDATA text, the Basic form in
  text and a deny-listed element read exactly `[removed:password]`; tree text and the fault code end in it; the record
  holds it in S1 to S5.
- **K15's 45 rows against the round-2 gate's N probe re-run at this head:** above (25 of 25 now refused, controls equal).
- **Every existing cell of rounds 1 and 2 still green:** 23 of 23 at the head three times (`g-exe`, `post-exe`, and
  inside the probe run), and inside the whole solution's 1927 and the merge's 1942.
- **An independent mutant run (31):** above, 31 of 31 MATCH.

## THE FRAME QUESTION (each "never / every / only / no" sentence this commit ADDS; three shapes outside the tested one)

| Sentence (head) | Tested shape | Three (or more) shapes outside it | Covered by |
|---|---|---|---|
| `Oxpd1Client.cs:36`, `README.md:33` "it names no setting" | K16: tree + SOAP read answered | NoCredential; Fault 500; TimedOut; PinRefused; MalformedAnswer; HttpStatus; tree with no setting | frame probe R1 to R9: 0 of 9 name it; one template for every outcome (DERIVED, `:237`); mutant `mSettingBack` |
| (same) | - | a device echoing the name in its answer | R10: recorded (the device's text) = **FOUND 3 (Info)**, no stated limit |
| `Oxpd1ClientOptions.cs:59` "Neither the name nor the value is recorded" | K12, K16 | the value in a fault code; the Basic form in text; the value with an escaped character in a namespace | R4 (fault code placeholder, record clean); S5; probe N rows + U7, record clean in all |
| `Oxpd1Soap.cs:176` to `:178`, `README.md:39` to `:40` "namespace names and attribute values ... compared as they are, unescaped, so a password holding `&`, `<`, a quote, a tab or a line feed is found there too" | K15: 5 characters x 7 shapes | a CR, `>`, an apostrophe, a non-ASCII character; inside a longer URI; declared on the Response and used three levels down or by the Result's own attribute; a prefix redeclared below; the tree root's default namespace; the Basic form in a namespace; an `xml:lang` value | frame probe U1 to U7 x 5 characters: 35 of 35 `MalformedAnswer`; U6 5 of 5 `Answered`, scrubbed; record clean in all; H37 (DERIVED in the kit) now MEASURED |
| (same) | - | a case variant; the password split across two namespaces | U8, U9: `Answered`, the exact password nowhere: **stated limit** (`README.md:74` to `:76`, "a case variant ... or a part of it") |
| `README.md:36` to `:37` "a scrubbed value reads `[removed:password]`" | K16: a note in the tree, the record | an attribute value; CDATA-joined text; the Basic form; a deny-listed element; the fault code | S1, S2, S4, S5 equal; S3 and R4 end in it; mutant `mPlaceholderText` |
| `Oxpd1Soap.cs:26` to `:30` "held here as a read-only field, not a constant and not a call keyed on a class name" | K16 reflection | changed to `const`; text changed; another `ReplacementFor` call with a constant | `mPlaceholderConst`, `mPlaceholderText` (K16 alone); source scan: the two remaining calls take variables |
| `README.md:46` to `:48` "The connection, the request and the reading of the body are bounded in time by `Timeout`" | K11 | TLS never answered; headers trickled; one body byte per 300 ms; a delay before the headers | probe C6, C6b `TimedOut` 1,001 ms; C8, C7 1,502 ms; frame R5 `TimedOut` |
| `README.md:48` to `:50` "The work after the body ... bounded by `MaxAnswerBytes` and the depth bound, not by `Timeout` ... can take seconds" | (named limit) | 90,000 attributes; 28,000 declarations; over the size bound | K7 6.8 to 9.3 s with `Timeout` 1 s (head = HEAD2); K1 5.9 s, K1t 5.3 s; K8 `TooLarge` 19 ms (B1987) |
| (residual) | - | the options' own doc | **FOUND 2** (`Oxpd1ClientOptions.cs:86` still says "connection and answer included") |

## MAIN MOVES

- **Main `df762b28` (unmoved at 15:41:00).** The head is not a merge of main (kit B1988 D6). The pull request's merge
  ref `26213ac7` (tree `56867d5d`) is exactly `git merge-tree --write-tree df762b28 85e414d6` (rc 0, one line) = gate
  B1987's (B) tree `7ad207ef` (re-computed here from `df762b28` and `8f5813bf`) plus exactly the 5 `M` paths. In `mg`
  (`read-tree -m -u`, `write-tree` equal, 628 files): locked restore rc 0, lock files unchanged; build 0 / 0, 34 ` -> `
  lines; `dotnet test` **`total: 1942`, `failed: 0`, `succeeded: 1938`, `skipped: 4`**, `Passed!`; `repo_rules.py`
  (never `--source-documents`; `test ! -e g1990/1_Project_Definition` rc 0) `RULES-NOTE: R5 hash half NOT RUN`,
  **`RULES: clean (628 files)`**. The head alone (`clone`): restore rc 0, lock files unchanged, build 0 / 0, 33 ` -> `;
  **`total: 1927`, `failed: 0`, `succeeded: 1923`, `skipped: 4`**; RULES 617; `unittest discover build/tests` `Ran 111
  tests`, `OK`. A squash of `85e414d6` onto `df762b28` gives main the tree `56867d5d` (DERIVED from the merge base
  `cad65b86`, the same inputs). Main's own push run (45104964428): `hosted3.py ... --total 1919 --rules 598
  --guard-linux 14 --guard-windows 15`: PASS (read 15:33).
- **Anything landing first:** landing.txt MAIN MOVES (B).

## LANDING TEXTS (this folder, RE-CUT for this head)

`landing.txt` (case (B) form: head-pinned SQUASH by `<project>/CLAUDE.md:82` at `85e414d6`, the 8 check names, the
merge-ref logs 1942, RULES 628, guards 14 / 15, csharp results 0, alerts 0, squash_scan, the after-checks with
hosted3.py since hosted2.py's fixed guards no longer fit); `pr-body.md` (the live body is still B1987's and is now false
in four places: head, cell count, two "Still open" items fixed; replace it); `pr-title.txt` (unchanged, equal to the
live title); `squash-subject.txt` and `squash-body.txt` (naming all three rounds' content: the client, the bounds, the
password path, the record without the setting's name, the scrub text, the unescaped namespace check, the narrowed
time-out); `FOR-RECORDS.md`. Who decided: the round's opening is the product owner's ruling of the card; every
direction in it is the coordinator's.

## NOT RUN

CodeQL locally (x86_64 extractor on arm64; the pull request's own analysis is the instrument, read above); any run on
Linux or Windows locally (the hosted legs ran the cells); this gate's frame probe on Linux or Windows; `run_step.py`'s
neutral scan locally (the seat ran it; the hosted secret-scan's hardened rows are OK on both runs); `repo_rules.py
--source-documents` (never); any device, simulator or address but 127.0.0.1; a profiler for the post-body cost; any
re-run, edit, comment or dismissal.

## DEVIATIONS

1. Copying the seat's `<project>/.tools/b1988/gate` into my scratch with `cp -Rc` was REFUSED by the `pathguard.py`
   hook (it read the source path as a write into another project). That action stopped there. I copied the kit's own
   canonical `<src>` instead (`fleet/state/s316/d1988/seat-tools/`, inside this tree; the folder kit B1988 names as
   THE TOOLS) and proved all 12 files by sha256 against the kit's table: equal. Nothing was written to the project.
2. My first gitleaks control read rc 0: the planted key's random tail used `[A-Z0-9]`, outside the AWS rule's base-32
   alphabet `[A-Z2-7]`. That control folder is in `g1990/_quarantine/`; I rebuilt it with the right alphabet (rc 1,
   `leaks found: 1`, quarantined) and re-ran every scan after it (`scans2.py`); the numbers above are the second run's.
3. The `gitleaks dir` over the clone at the head ran at 15:31 while the mutant run was applying mutants in that tree
   (a read only; the mutants differ from the head by one edit each, and the commit's own blobs were scanned separately).
4. I added a frame probe of my own (`G1990Probe.cs`, scratch only, never committed) and a cost A/B in a worktree at
   HEAD2 (`h2`), beyond the kit's list, to answer the frame question and FOUND 2 by measurement.

## TREES LEFT

`g1990/clone` detached at `85e414d6`, status clean, built (mutants undone and proved), push URL `invalid://no-push`;
worktrees `g1990/red` (HEAD2 + both patches staged = tree `8cf35b46`, never committed), `g1990/mg` (index and files =
`56867d5d`, never committed, built), `g1990/probe` (the head + untracked `G1987Probe.cs` and `G1990Probe.cs`, built),
`g1990/h2` (HEAD2 + untracked `G1987Probe.cs`, built); `g1990/gate` (the 12 tools, unedited); `g1990/scratch/**`
(scripts, `probe-out-g1987.txt`, `probe-out-g1990.txt`, `cost-*.txt`, `mutants/`, `gl-neutral-*`, `added.txt`,
`subject37.txt`, `pr37-body-live.md`); `g1990/logs/**`; `g1990/_quarantine/{locks (85), gl-control-* (2)}`. No process
left running; the wave lock not held by this reader (absent at 15:41).
