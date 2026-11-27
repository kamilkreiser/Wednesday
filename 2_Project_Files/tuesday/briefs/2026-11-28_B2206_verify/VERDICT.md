GATE B2206: GO @ 24e94ef on main aa520ba

Gate G1, ROUND 2 OF 2 of lane AZ-1 (the text-only fix of the Bicep of the mock client environment's foundation), one
Opus reader (claude-opus-5-5), in-session, read-only, for Tuesday s337. Kit B2205 (seat X104; stamp S4: Q1 to Q3 "a" IN
WORDS; every choice the coordinator's, none the product owner's). Head `24e94ef2a9df278d0797fadc8954a5ff4e90ede3` on
`b2191/az1-bicep-foundation-r2`, ONE commit over HEAD0 `14896ed06f46536073a25a4d1388d4431ca04169` (one parent, a
fast-forward), tree `4340cacc762f349f37feae8e502b381f200d9644`, 764 files. Measured 2026-11-28 03:55:13 to 04:03:18 AEDT.
**I ran NO az command** (every Azure fact is read from X92's saved answers in `<project>/.tools/b2179-x92/logs/`, READ
ONLY, or RELAYED from gate B2204); no dotnet; no lock; nothing to any printer, device, tenant or person; no pull
request, no push, no Jira. Writes: this folder and the scratch `fleet/state/s337/g2206/` only (`repo/`: a clone of the
seat's clone, push URL `invalid://no-push`, detached at the head). Grades: **Blocker 0, Major 0, Minor 0, Info 7.**

## The lane re-measured (gh api -X GET, 03:55:25 and 03:57:58 AEDT)
- Branch ref ONE row `24e94ef2...` (= the seat's READY). `compare/14896ed0...24e94ef2`: ahead 1, behind 0, `modified
  deploy/azure/README.md +20/-8`, `modified deploy/azure/main.bicep +3/-1`. The head commit: one parent `14896ed0`,
  tree `4340cacc...`. Pull requests from the branch (state=all): 0. `.private` true.
- **MAIN MOVED TWICE since the kit.** `e1802e24` at 03:55:25; **`aa520ba5e23c8d3319733d8b649aea0617bbf7a7` at
  03:57:58** (PR #64, lane L3a, merged 2026-11-27T16:56:37Z = 03:56:37 AEDT; one parent `e1802e24`; tree `e9a3684d...`,
  780 files). `compare e1802e24...aa520ba5`: 12 files (6 added, 6 modified), all under `src/Datasec.Suite.Server/**`
  and `tests/Datasec.Suite.Server.Tests/**`; `compare d9f89115...aa520ba5`: 28 files, **0 under `deploy/`, 0 under
  `.github/`**. `compare aa520ba5...24e94ef2`: diverged, ahead 2, behind 2, merge base `d9f89115`, 2 files both `added`
  (disjoint paths). Open pull requests at 03:57:58: 0. The next pull request number is most likely **65** (#64 is the
  newest issue or pull request).
- The two files and the message fetched from the origin at the head (`contents?ref=24e94ef2`, raw): `main.bicep` sha256
  `97bb8cb18be31653a9d4c93322a63124549d7b077272981971f86460cd8972b1` (272 lines, 7744 bytes), `README.md`
  `1426ded7444a46cbb21e34fce6f8dfa3d72492b75fa3bfd22a85f8303cbe5422` (53 lines, 3439 bytes), message `12d83f7a...c7d7`
  (403 bytes, 3 lines, `cmp` equal to the frozen `commit-message.txt`): each equal to kit S8 and to my scratch clone.

## THE GATE list of the kit (FOR TUESDAY), whole
1. **`HEAD0..head`:** `diff --name-status` 2 rows, both `M`; against BASE `d9f89115` 2 rows, both `A`; `ls-files` 764.
   main.bicep: ONE hunk `@@ -44,7 +44,9 @@`, one `//` line out, three `//` lines in (47-49); nothing else.
   README: three hunks (`-4,7 +4,9`, `-25,10 +27,13`, `-36,6 +41,13`), all prose. `--numstat` `20 8` and `3 1`, equal
   with `--ignore-all-space` (no whitespace-only line). The stamp's frame (1): changed lines holding `/*` or `*/`: 0.
2. **The compiled hash, re-built by me** in `g2206/build/` with my copy of the pinned CLI (sha256
   `62cd5958c62fa1b738e9b69f24799fabddb90ed83fdb7d6d2563dde376ce479d`, `Bicep CLI version 0.48.1 (cec7951cf6)`), each
   `bicep build <file> --outfile <dir>/main.json`, rc 0, stdout 0 lines, stderr 0 lines:
   - the origin's head `main.bicep` -> `ba7a31d7e6c90eb1596fe7e83b01c7044eb4c8eacf1a0adf5c67645cbade8546` **EQUAL**;
   - HEAD0's `main.bicep` (`8a8d38f9...9274`, from my clone) -> `ba7a31d7...8546` (the same: the what-if-proven bytes);
   - control, the head file with `Region of the regional resources.` ending in `!` (a decorator text) ->
     `e22b3603d74d77fead34ee3be9e36f7df589d169bfb1fc88d68d2efb75187653`, DIFFERS (a compiled change shows).
   So round 1's what-if proof (gate B2204 items 2 to 6) carries to this head unchanged. The five mutants were not
   re-built by me (they are built from the same file by the seat's frozen edits; the seat's table, 5 of 5 equal, is
   RELAYED; check 7's OLD-text counts are unaffected: the edited line 47 is in none of them).
3. **Each changed sentence against B2204 and the template** (template lines by reading the origin's head file;
   group facts MEASURED by me in X92's saved answers, read only):
   - **F1 (MAJOR in round 1) CLOSED in text.** README 6-9 "an explicit rule that denies every inbound flow and two
     rules that allow outbound to the private endpoint subnet on 443 and 9400-9599; outbound traffic is not restricted
     by this template"; README 44-47 and main.bicep 47-49 "keeps Azure's default rules, which allow outbound to the
     whole virtual network and to the Internet". TRUE: template `securityRules` are exactly `deny-all-inbound` 4096
     Inbound Deny `*` (57-67), `allow-out-pe-443` 100 and `allow-out-pe-9400-9599` 110 Outbound Allow Tcp
     serverSubnet -> peSubnet (70-93); no outbound Deny. X92's `nsg.out` (`NewNSG.defaultSecurityRules`, read by
     program): `AllowVnetInBound` 65000, `AllowAzureLoadBalancerInBound` 65001, `DenyAllInBound` 65500,
     `AllowVnetOutBound` 65000 VirtualNetwork->VirtualNetwork, `AllowInternetOutBound` 65001 `*`->Internet,
     `DenyAllOutBound` 65500. So 4096 precedes both inbound allows (inbound: every flow denied, TRUE) and nothing
     precedes the outbound defaults but the two allows (outbound: unrestricted, TRUE). The "outbound only" sentence is
     gone (0 in both files). Not overclaimed the other way: the README does not say the two allow rules are useless
     or absent, and says "not restricted by this template", which is exact. See I4, I5 for wording.
   - **F2 (Minor) CLOSED.** README 30-34: NoChange, or Modify with every changed property NoEffect or one of six listed
     values; no Create, Delete, Deploy or Unsupported; Ignore only on undeclared, unowned resources. This is the judge's
     rule as B2204 read it (`whatif2189.py` 98-113, 177-283; the six PASS lines). The six named in words are exactly
     N1 (endpoint `ipVersionType`), N2-N5 (zone config `etag`, `id`, `provisioningState`, `type`), N6 (namespace
     `privateEndpointConnections`). Looser than the judge in one way only: the judge matches each value EXACTLY (type,
     name, path, change, before, after) and the IGNORE list is closed; the sentence says "listed values" and "resources
     the template does not declare and does not own". Not false; not a claim the check does not meet.
   - **F3 (Minor) CLOSED.** README 53: log store public access for ingestion and query. TRUE: main.bicep 254-255
     `publicNetworkAccessForIngestion: 'Enabled'`, `publicNetworkAccessForQuery: 'Enabled'` (B2204's 252-253 moved by 2).
   - **S1 (Minor) text CLOSED, decision open.** README 48-50: `RootManageSharedAccessKey`, rights Listen, Manage and
     Send; neither declared nor removed; key-based access not turned off. TRUE: X92's `relay-ns-sas.out` (program):
     ONE rule `RootManageSharedAccessKey ['Listen', 'Manage', 'Send']`; the template has no `authorizationRules`
     resource and no `disableLocalAuth` (`disableLocalAuth` 0 in every X92 relay answer). "does not turn off" claims
     nothing about whether the API can.
   - **S2 (Minor) text CLOSED, decision open.** README 51-52: public network access with no network rules, no purge
     protection, deleted items kept 7 days by default (`keyVaultSoftDeleteRetentionInDays`). TRUE: main.bicep 233
     `publicNetworkAccess: 'Enabled'`, 229 `softDeleteRetentionInDays: keyVaultSoftDeleteRetentionInDays`, 41 `param
     ... int = 7`, no `networkAcls`, no `enablePurgeProtection`; X92 `console-kv-show.txt` 15 `"enablePurgeProtection":
     null`, 22 `"networkAcls": null`, 25 `"publicNetworkAccess": "Enabled"`, 30 `"softDeleteRetentionInDays": 7`; the
     lane's parameters file sets no retention (its `value` lines: prefix, tags, names, zone), so 7 is the live value.
   - **Anything overclaimed the other way?** None found. Unchanged lines still true at this head: README 13 (vault
     RBAC, soft delete, no access policies), 10-12 (Relay public access disabled, client authorization on each), 38
     (nothing deployed from this folder). main.bicep 1 says the Relay meeting point is "locked down": true of its
     network path (public access Disabled, private endpoint only), and the README's known differences now qualify the
     key path; not graded.
4. **Words and the B-number count** (`words.py` my copy, sha256 `6f932dc5...`): `--control` `CONTROL FIRED: 13 of 13`;
   over the added lines `HEAD0..head` (23 lines, 2129 bytes), `BASE..head` (325 lines, 11183 bytes; both `cmp` equal
   to the seat's `scratch/checks/` files) and the message: `WORDS: clean (3 files)`, rc 0, non-ASCII 0. B-number
   pattern `(?<![A-Za-z0-9])B2[0-9]{3}(?![0-9])`: 0, 0, 0, and 0 over both whole head files; control: the lane's
   parameters file 1. Internal words words.py does not count, over the head files: `lane` 1 and 1 (the "server lane",
   I1), `seat` 0, `kit` 0, `brief` 0, `Datasec` 0.
5. **gitleaks 8.30.1, control FIRST:** a token-shaped value built by a program from two halves and 36 random
   characters (never printed) in `g2206/gl-control/`: `dir ... --no-banner --redact --ignore-gitleaks-allow
   --exit-code 1` rc 1, `leaks found: 1` (moved to `g2206/_quarantine/`). Then the origin's two head files and the
   message as `1.txt` to `3.txt`: rc 0, `no leaks found` (11586 bytes); `gitleaks git <scratch clone>
   --log-opts=14896ed0..24e94ef2`: rc 0, `1 commits scanned`, `no leaks found`.
6. **The hosted PASS line of the new head, re-read by me** with `hosted3.py` (my copy, sha256 `969fe376...`, GET
   only): `HOSTED 24e94ef2a9df278d0797fadc8954a5ff4e90ede3: PASS` at `--total 2539 --rules 764 --skipped-linux 4
   --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15`, rc 0 (run
   46036402215, push; linux, rules, secret-scan, windows each success, attempt 1; check runs beside the four 0).
   Control `--total 2540`: `FAIL 4` (rc 1).

## Tuesday's point 2 (Info, one sentence of judgement)
**I1 INFO:** a reader of the template alone WILL see that outbound is not restricted (README 8-9 in the first bullet
and 44-47 in known differences, the comment above the NSG), but the action is addressed to "the server lane, the change
that first puts compute in the server subnet", project wording a deploying client cannot act on, so the sentence a
client must act on ("add a rule that denies other outbound traffic before you put compute in the server subnet") is
not yet in client words; acceptable while this file is the mock environment's (Q1 a, and the Marketplace mainTemplate
is not decided), owed to the mainTemplate lane.

## Other Info (none blocks; each for a later lane)
- **I2 INFO (B2204 I3 not in the text):** the README now says `Modify` on the six values passes, and calls them values
  Azure sets itself (DERIVED, B2204 I3), but does not say what-if predicts `Delete` for each, nor that a real `create`
  over an existing group is UNMEASURED for them (N6 is the namespace's only endpoint connection). Guarded today by
  README 38 (nothing is deployed from this folder). For the first deploying lane.
- **I3 INFO (the owed rule's shape, DERIVED from the template):** the key vault (233) and the log store (254-255) are
  reached on public endpoints (no private endpoint for either in this template), so a deny-all outbound rule on the
  server subnet will also cut the server's path to them unless the server lane's brief lists the allows it needs. The
  README's "a rule that denies all other outbound traffic" is the right shape; its allow list is the server lane's.
- **I4 INFO (wording):** main.bicep 47-48 "Outbound is NOT restricted by this template: the group keeps Azure's
  default rules": "the group" means the network security group here, but the README uses "the group" for the
  resource group (22, 42). Not false; a later edit may say "the network security group".
- **I5 INFO (wording, UNMEASURED source):** "the whole virtual network" names the effect of `AllowVnetOutBound` on this
  isolated network. Azure's documented `VirtualNetwork` service tag also covers peered networks and connected
  on-premises ranges (Microsoft's service-tag documentation; NOT re-read in this session, so UNMEASURED here). It
  understates nothing that matters today (the operative sentence is "does not restrict outbound"); for the
  mainTemplate lane, where a client network may be peered.
- **I6 INFO:** CodeQL reads neither file (B2204 I5, RELAYED; the PR's Analyze rows are actions, csharp, python).
  Markdown rendering is read by no check (the stamp's frame 3, a named limit); I read the README as text, 53 lines,
  each list item and code fence closed.
- **I7 INFO (main moved):** the B2204 landing form is VOID (it pins `14896ed0` and main `d9f89115`); landing.txt in this
  folder is the new one, with MAIN MOVES (B) at main `aa520ba5` (PR 64): its own push-run numbers, rules count + 2.

## ADVERSARIAL: shapes outside the kit's properties (P1 compiled, P2 two files, P3 text true and clean)
| P | Shape | Covered or named limit |
|---|---|---|
| P1 | a compiled change hidden in comment edits | covered: my own build `ba7a31d7` equal; control `e22b3603` differs |
| P1 | another CLI or OS | named limit: one build, macOS arm64, CLI 0.48.1 pinned by hash (the seat's and mine agree) |
| P1 | the mutants | RELAYED (seat 5 of 5 equal); not re-built by me (named) |
| P2 | a third path, rename, delete | covered: `diff --name-status` 2 `M` (HEAD0) and 2 `A` (BASE); compare 2 files |
| P2 | whitespace-only change on an unchanged line | covered: `--numstat` equal with and without `--ignore-all-space` |
| P2 | the branch moved after the READY | covered: ref = `24e94ef2` at 03:55:25 (landing step 4 re-reads it) |
| P3 | a sentence still false | covered: each against its line above; `outbound only` 0 |
| P3 | a sentence now false the other way | covered: none found (item 3) |
| P3 | an id, word or secret a client must not see | covered: words, B-number, gitleaks (control first); "lane" named I1 |
| P3 | a client cannot act on a true sentence | named: I1 |

## SCANS OF THE LANDING TEXTS
`squash_scan.py` (head's, = main aa520ba5's, sha256 `d718569b...`) over the subject with `#65` and squash-body.txt:
`SQUASH-SCAN: clean` (control rc 1, found 2). `words.py` over subject, body, title: `WORDS: clean (3 files)`;
pr-body.md 0 in every class (its 4 non-ASCII bytes are the generated-by emoji). Details: FOR-RECORDS.md.

## MAIN AT THE END: aa520ba5 (MOVED from the kit's e1802e24)
Read 04:03:18 AEDT: main `aa520ba5e23c8d3319733d8b649aea0617bbf7a7` (unchanged since 03:57:58), the branch
`24e94ef2...` (unchanged), open pull requests 0; Analyze (csharp) on aa520ba5 now `completed success` (7 of 7 rows).
Main's own push run, re-read by me: `HOSTED aa520ba5...: PASS` at `--total 2564 --rules 780 --guard-linux 28
--guard-windows 29` (skipped 4 / 21, unit and floor 117): **the test total and BOTH guard counts moved with PR 64**
(2539 and 14/15 before). e1802e24 also PASS at 2539/774, 14/15. landing.txt MAIN MOVES (B) carries these numbers:
merge ref T 2564, RULES 782, guards 28/29; new main tree 782 files. `pgrep -fl 'Caskroom/azure-cli'` at 04:03: no line
(rc 1).
