GATE B2204: GO WITH FINDINGS @ 14896ed on main d9f8911

Gate G1, ROUND 1 OF 2 of lane AZ-1 (the Bicep of the mock client environment's foundation, proved by what-if), one
Opus reader (claude-opus-5-5), in-session, read-only, for Tuesday s337. Kit B2191 (seat X99; stamp S4: Q1 to Q4 "a" IN
WORDS, Q5 to Q11 the defaults; every choice the coordinator's, none the product owner's). Head
`14896ed06f46536073a25a4d1388d4431ca04169` on `b2191/az1-bicep-foundation-r2`, ONE commit, one parent = main
`d9f89115333bbed2ade723e4c11d523b2a9cd079` (PR 62's squash), tree `0f84e8d9b812a45d09046b4e15a0ffa1b0487e49`, 764
files. Measured 2026-11-28 03:14:00 to 03:21 AEDT. **I ran NO az command** (every Azure fact below is read from the
seat's saved answers in `<project>/.tools/b2191-x99/logs/`, or from X92's/X98's saved answers, READ ONLY); no dotnet
job; nothing to any printer, device, tenant or person; no pull request, no push, no Jira. Writes: this folder and the
scratch `fleet/state/s337/g2204/` only (`repo/`: a clone of the seat's clone, push URL `invalid://no-push`, detached at
the head). `pgrep -fl 'Caskroom/azure-cli'`: no line at 03:20 (rc 1).

## The lane re-measured (gh api -X GET, 03:14:07 and 03:20:10 AEDT)
- main `d9f89115...` both times (tree `aa53e949...`, one parent `cf224e1f`); branch ref ONE row `14896ed0...`;
  `compare/main...14896ed0`: ahead 1, behind 0, 2 files, `added deploy/azure/README.md`, `added deploy/azure/main.bicep`;
  `contents/deploy?ref=main` Not Found. The head commit: one parent `d9f89115`, tree `0f84e8d9...`.
- **Open pull requests: 0 at 03:14, 1 at 03:20: #63** (`b2185/x94-oxpd1-contracts-l1c` at `f4aacb5e`, 16 files under
  `contracts/oxpd1/**` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/**`, 0 under `deploy/`). Disjoint from this lane;
  if it lands first, landing.txt MAIN MOVES (B) applies.
- The two files and the commit message fetched from the origin at the head: sha256 `8a8d38f9...9274` (main.bicep, 7538
  bytes), `20c35ef9...600d` (README.md, 2359 bytes), `e4ca4a3a...33f7` (message, 289 bytes): each equal to stamp S8 and
  to the seat's lane copies (no D2 edit). My scratch clone: `git diff --name-status d9f89115 HEAD` = 2 rows, both `A`;
  `ls-files` 764 (= BASE's 762 + 2).
- Hosted run of the head, re-read by me with the lane's `hosted3.py` (sha256 `969fe376...`, GET only, logs into my
  scratch): `HOSTED 14896ed06f46536073a25a4d1388d4431ca04169: PASS` at `--total 2539 --rules 764 --skipped-linux 4
  --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15` (run 46030871938:
  linux succeeded 2535, windows 2518, GUARD 14 / 15, `RULES: clean (764 files)`, `UNIT-TEST FLOOR: ran 117, floor 117`,
  `NEUTRAL-SCAN ... objects of this commit not among them 0`, 25 of 25 planted); control `--total 2540`: `FAIL 4` (rc 1).

## THE GATE list of the kit (FOR TUESDAY), whole
1. **`BASE..head` read whole** (main.bicep 270 lines, README.md 41 lines, message 3 lines): 13 declared resources, API
   versions as D5, no parameter default holds an id; `tenantId: subscription().tenantId`; four outputs. See F1, F2, F3.
2. **The template against X92's ledger** (`2026-11-27_B2179_SEAT-X92_STATUS.md`, sha256 `039cca53...8e96`, its 19
   `MADE` lines 159-177 and its read-backs): every MADE label has a carrier and every declared resource a MADE line
   (nsg + 3 rules -> serverNsg with priorities 4096/100/110; vnet + 2 subnets with 10.232.0.0/24, /26, 10.232.0.64/28 and
   the NSG on snet-server; relay-ns + relay-pna -> Standard, publicNetworkAccess Disabled; hc-site/server/admin ->
   requiresClientAuthorization true; pdns-zone, pdns-link (registration off); pe (groupIds namespace, snet-pe); pe-dzg;
   kv (standard, RBAC, soft delete 7, no purge protection); law (PerGB2018, 30 days, cap 0.16); dns-zone). Equal to the
   seat's `reading.md` map. The live payloads in `wi-green.out` agree (NoChange on 10 of 13; the 3 Modify rows hold only
   N1-N6).
3. **NOISE against X98's `wi-green-deltas.txt` and the seat's own green answer**: N1 = deltas line 3, N2 = 7, N3 = 8,
   N4 = 9, N5 = 10, N6 = 12, each in type, name, path, change type, before and after (read by me against
   `whatif2189.py` lines 98-113). **The seat's `wi-green.out` is byte-equal to X98's** (both sha256
   `f899db449bed840dbbe3cd065cf3afad207b82ae15cd0076a7f4cf46143cd800`), so the six values were still exact at 03:01. My
   independent count over all six answers (not the judge's code): the ONLY non-NoEffect leaves in green are the six
   NOISE leaves; in each mutant, the six plus exactly the planted leaves; `status Succeeded`, `error None`,
   `potentialChanges 0`, `diagnostics 0` in all six.
4. **Every D2 edit against its DELTA line**: none; green passed on the first set (`final-set.txt` = `green`; green's
   `main.bicep` byte-equal to the origin's).
5. **The green and five mutant judge lines, re-run by me** from the saved answers with the lane's `whatif2189.py`
   (sha256 `83345514...`, `python3 -I -B`), every print saved in `g2204/judge/`, each BYTE-EQUAL to the seat's
   `logs/judge-wi-*.txt`:
   - `WHATIF wi-green green: PASS (declared NoChange 10, NoEffect-only 0, noise-only 3, noise leaves 6, expected rows 0, ignore listed 2)`
   - `WHATIF wi-mrelaypublic mRelayPublic: PASS (declared NoChange 10, NoEffect-only 0, noise-only 2, noise leaves 6, expected rows 1, ignore listed 2)`
   - `WHATIF wi-mhcauth mHcAuth: PASS (declared NoChange 7, NoEffect-only 0, noise-only 3, noise leaves 6, expected rows 3, ignore listed 2)`
   - `WHATIF wi-mdenyinbound mDenyInbound: PASS (declared NoChange 9, NoEffect-only 0, noise-only 3, noise leaves 6, expected rows 1, ignore listed 2)`
   - `WHATIF wi-mvaultrbac mVaultRbac: PASS (declared NoChange 9, NoEffect-only 0, noise-only 3, noise leaves 6, expected rows 1, ignore listed 2)`
   - `WHATIF wi-mnewhyco mNewHyco: PASS (declared NoChange 10, NoEffect-only 0, noise-only 3, noise leaves 6, expected rows 1, ignore listed 2)`
   - also `--selftest` `SELFTEST: 72 of 72 PASS`; `list` `LIST: 13 declared, 7 ignore, 6 noise, 5 mutants`; the judge
     over X98's answer the same PASS line; `INVENTORY inv-before: PASS (11 listed, 11 expected, rc 0)` and the same for
     `inv-after`. Each mutant's set differs from green by exactly its frozen edit (by `difflib`: one bicep line each,
     mNewHyco one parameters line split in two); the main.json hashes equal the seat's table.
   - **Nothing written in the lane:** `ls -laTR` of `<lane>` sha256 `11724217...81d7` (7451 lines) before and after; of
     `<x98>` `f12b87c2...b55b` before and after; content hash of `<lane>/logs` and `<lane>/gate` equal before and after;
     no `__pycache__` in `<lane>/gate` (`ls -d`: No such file or directory). The selftest's temp folder went to my
     scratch (`TMPDIR`).
6. **The two SAME lines**: `SAME inv-before inv-after: PASS (11 rows and 11 rows)`, `SAME dep-before dep-after: PASS (0
   rows and 0 rows)` (re-run, byte-equal to the seat's). Stronger than `same` (which compares type, name, state and tags
   only): `inv-before.out` and `inv-after.out` are BYTE-equal (8874 bytes), and both deployment lists are `[]`.
7. **The README's known differences and its sentence on `Modify` (Q5)**: F2 and F3.

## Grades (round 1 of 2): Blocker 0, Major 1, Minor 4, Info 8. Nothing blocks landing; the Major is a wording owed to
the next AZ lane (or a narrow round 2, Tuesday's choice): see F1.

**F1 MAJOR (a security claim in the landed text that the environment does not meet; owed to a later lane, NOT a change
to what exists): "outbound only to the private endpoint subnet" is false while the NSG keeps Azure's default outbound
rules.** README lines 6-7 ("denies every inbound flow and allows outbound only to the private endpoint subnet on 443 and
9400-9599") and main.bicep line 47 (the same in a comment). MEASURED (X92's saved create answer
`.tools/b2179-x92/logs/nsg.out`, read only): the NSG carries the default rules `AllowVnetOutBound` (65000, VirtualNetwork
to VirtualNetwork), `AllowInternetOutBound` (65001, to Internet) and `DenyAllOutBound` (65500); the template (and the
live group: green NSG NoChange) has no outbound deny rule. DERIVED from Azure's documented NSG model (lower priority
number first; default rules apply unless a custom rule of higher precedence matches): outbound from snet-server is
ALSO allowed to the whole VNet on any port and to the Internet, so the two allow rules add nothing today. Inbound is as
stated (`deny-all-inbound` 4096 precedes `AllowVnetInBound` 65000 and `AllowAzureLoadBalancerInBound` 65001). No VM
sits in the subnet yet (D1, kit and README), so nothing is exposed today; but this file is the base of the Marketplace
mainTemplate and the lane rule is "follow all security ... rules". Owed: the server lane (the first lane that puts
compute in snet-server) either adds a `deny-all-outbound` rule (a change to what exists: its own what-if, then a create
under its brief) or the README and comment are reworded to what exists. Not a reason to change THIS commit (the kit
froze both files; D1 holds: the template describes what exists exactly).

**F2 MINOR (Q5, raised as the kit invited): the README's check sentence is stricter than the check that passed.**
README lines 28-30: "every resource ... reads `NoChange`, no resource reads ... `Modify` ...". The accepted green has
three `Modify` rows (NOISE-ONLY: the endpoint's `ipVersionType`, the zone group's config, the namespace's endpoint
connection). A later lane rewords it to the judge's rule (NoChange, or Modify whose every leaf is NoEffect or on the
closed NOISE list). The kit's default (README unchanged) stands for this commit.

**F3 MINOR (the README's known differences are incomplete): the log store's public access is not named.** main.bicep
lines 252-253 state `publicNetworkAccessForIngestion: 'Enabled'` and `publicNetworkAccessForQuery: 'Enabled'` (live
equal: green NoChange; payload read by program). README's "Known differences" names the vault only. Also unnamed: the
Relay namespace's public access is Disabled but its `RootManageSharedAccessKey` (Listen, Manage, Send) is the one
standing credential path (named, see S1). Owed to the rewording lane of F2.

**Tuesday's point (b), security of what the template DESCRIBES (each a finding for a LATER lane; D1 holds for this
commit):**
- **S1 MINOR: the Relay namespace's `RootManageSharedAccessKey`** (rights Listen, Manage, Send; MEASURED by X92,
  `relay-ns-sas`, its keys never read) is not declared and reads `Ignore` (IGNORE_OK). `disableLocalAuth` is absent from
  the namespace at API `2021-11-01` (X92 MEASURED); whether a newer Relay API offers it is UNMEASURED. A namespace-level
  shared key with Manage defeats per-connection client authorization for anyone holding it; private-only network access
  (publicNetworkAccess Disabled, MEASURED live) is the present mitigation. Later lane: decide local-auth off (API move)
  or name the rule's custody; never in this commit.
- **S2 MINOR: the key vault: public network access Enabled, no `networkAcls`, no purge protection, soft delete at the
  minimum 7 days** (template lines 225-232; live equal). README names public access and purge protection. A later lane
  decides; **enabling purge protection is irreversible** (approval-class for that lane's brief).
- **S3 INFO: the log store's public ingestion and query Enabled** (F3). Data-plane access is by resource permissions only
  (`enableLogAccessUsingOnlyResourcePermissions: true`, see I4).
- What holds well (read): Relay `publicNetworkAccess: 'Disabled'`, every hybrid connection `requiresClientAuthorization:
  true` (no hybrid-connection rule, X92), vault RBAC with `accessPolicies: []`, `enabledFor*` all false, NSG inbound
  denied, private DNS link `registrationEnabled: false`. The public DNS zone is public by nature (NS and SOA only).

**Tuesday's point (c), values a client deployment must not see: NONE in the two files.** By program over the origin's
files: 0 GUIDs (no subscription, tenant or object id; the vault's tenant is `subscription().tenantId`), 0 e-mail
addresses, 0 `/subscriptions/` paths, 0 B-numbers, 0 names of the company or its domain; the only addresses are the
RFC 1918 defaults `10.232.0.0/24`, `10.232.0.0/26`, `10.232.0.64/28` (parameters with defaults; I7). The commit
message: one e-mail, the co-author trailer `noreply@anthropic.com`. **The lane's parameters file**
(`gate/whatif/mock-client.parameters.json`, sha256 `87c93108...`, never committed: `checks2189.py` check 1 and my diff)
holds no subscription, tenant or object id and no IP (its only dotted number is `contentVersion` `1.0.0.0`); it does
hold deployment-specific values that rightly stay outside the repository: `namePrefix` `oxpd2-mock`, the tags
(`created_by` = the agent login's name, `brief` = an internal build id, `project`, `purpose`), the three hybrid
connection names and the zone `mock.datasec-rd.com`.

**Tuesday's point (a), the NSG rule order (the seat's R12 b): the judge does NOT match rules by name; it has no array
logic at all, and the green NSG row passed because what-if itself answered `NoChange`.** Code read (`whatif2189.py`
lines 177-188, 200-283): `leaves()` only flattens what-if's own `delta` tree, joining paths with what-if's indices; a
`NoChange` row is passed on its `changeType` without reading its delta. MEASURED in the saved answers: what-if's `after`
(its predicted state) lists the rules `allow-out-pe-443` (100), `allow-out-pe-9400-9599` (110), `deny-all-inbound`
(4096): NOT the template's order (deny first) but the live order; so what-if normalised the template's array before
comparing (by name or by priority: both orders coincide here, UNMEASURED which), and `mDenyInbound` printed
`properties.securityRules.2.properties.priority | Modify | 4096 -> 4095` against that normalised order. A pure reorder
is therefore invisible, and that is correct for an NSG (rule evaluation is by priority, not array position). A rename or
any field change cannot hide behind the order: MEASURED by the gate's synthetic answers through the judge's own
`judge_doc` (`g2204/probes.txt`): a renamed rule (`securityRules.0.name Modify`), an added element (`Create`), a removed
element (`Delete`), a rename shown as Delete + Create at a shifted index, and an `Array` leaf without children each
print `DELTA ... PROTECTED` and FAIL green (every path under `properties.securityRules` is PROTECTED). The only ways
through are what-if's own: a `NoChange` row carrying an effective leaf PASSES (probe a7; I1), and an Array whose
children what-if marks `NoEffect` PASSES (probe a6). The trust root is what-if's answer; the judge adds no pairing of
its own that could mis-pair.

**I1 INFO (judge limit, named): a declared row reading `NoChange` is passed without reading its delta.** MEASURED in
the real answers: each of the six holds exactly one NoChange row with a non-empty delta (the log store's
`properties.features` `NoEffect`, I4); probe a7 (a planted `Modify` leaf on a NoChange NSG row) PASSES. What-if does not
print such a row today (UNMEASURED that it never does).

**I2 INFO (judge limit, named): a mutant's expected row is matched by a path PREFIX for mDenyInbound**
(`^properties\.securityRules`): probe p5, the real mDenyInbound answer with a second planted change (`access Deny ->
Allow` on the same rule) still reads `PASS`. The green set would FAIL such a leaf; this only weakens what a mutant
proves (R7 is the kit's named limit).

**I3 INFO (for the first lane that DEPLOYS this template, not this commit): what-if predicts `Delete` on the NOISE
leaves.** N6 is the namespace's ONLY private endpoint connection (`Auto-Approved`), N2-N5 the zone config's Azure-set
fields, N1 the endpoint's `ipVersionType`. The kit's reading (values Azure sets itself, not sent by a PUT) is DERIVED;
what a real `create` of this template over the live group does to them is UNMEASURED (nothing was deployed, by design).
Losing N6 would cut the namespace's only network path. Any lane that runs a `create` from this file over an existing
group must first prove N6 survives (e.g. in a throwaway group), never infer it from the NOISE list.

**I4 INFO (a stated property what-if cannot confirm): the log store's `features.enableLogAccessUsingOnlyResourcePermissions:
true`** reads `NoEffect` with `before null` (the live GET returns no `features`), so whether the live workspace holds
`true` is UNMEASURED by this lane (X92's `law-show` did not read it either).

**I5 INFO: the PR's CodeQL will not read these files.** The Analyze rows of PRs 60-62 are `actions`, `csharp`,
`python` (MEASURED, check-runs by GET); CodeQL has no Bicep or Markdown analysis (Microsoft's documented language
list; not run here). The security read of this change is this gate plus the repo-wide `rules` and `secret-scan` jobs.

**I6 INFO: no Marketplace template test was run** (ARM template test toolkit, Partner Center validation): NOT RUN by any
seat; the kit's NOT DECIDED 1 (whether the mainTemplate is this Bicep) stands. Bicep's own linter printed 0 warnings
(seat's build logs, six sets).

**I7 INFO: the address defaults are this environment's** (`10.232.0.0/24` and its two subnets): parameters, but a
client deploying with defaults could collide with its own ranges; the file's comments and README still say "mock client
environment". For the mainTemplate lane.

**I8 INFO: NOISE life.** Each tuple holds only while a fresh answer still prints it exactly: N2's etag changes when the
zone group is written; N6 changes if a second connection or a state change appears; N1 leaves if the endpoint's API
moves (Q3 b). Proven conservative by the gate's look-alikes (`g2204/probes.txt`, each FAIL): N6 with a second
connection, N6 `Pending`, N2 with another etag, N3-N5 at index 1, N1 as `Modify` to `IPv6`, N4 `Failed`, a NOISE row
plus a protected leaf, N1 on another endpoint; and the selftest's own 20 NOISE checks (72 of 72).

## ADVERSARIAL: three shapes outside each property (kit REQUIRED SECTION P1-P6)
| P | Shape | Covered or named limit |
|---|---|---|
| P1 | another Bicep CLI | covered: `build` refuses a CLI whose sha256 is not `62cd5958...` (code `BICEP_SHA256`) |
| P1 | the Marketplace test toolkit's rules (API age, location parameter, outputs) | named limit I6 (NOT RUN) |
| P1 | a build on another OS or CLI release | named limit: one build, macOS arm64, CLI 0.48.1 |
| P2 | a property what-if cannot see (`before null`) | named limit I4 (the log store's `features`) |
| P2 | a NoChange row carrying an effective leaf | named limit I1 (probe a7 PASSES) |
| P2 | an undeclared child that a deploy would touch (the auth rule, the zone A record) | covered while it reads `Ignore` on the closed IGNORE_OK list; the auth rule as `Delete` FAILS (probe p4); a row in another group FAILS (p3); `potentialChanges` FAILS (p1); `Unsupported` FAILS (p2) |
| P3 | a second change beside the planted one in a mutant | named limit I2 (probe p5 PASSES for mDenyInbound; for mVaultRbac a purge-protection leaf beside it FAILS, p6) |
| P3 | a declared resource removed from the template | covered: a missing declared row FAILS (probe a8; selftest), a doubled one FAILS (a9) |
| P3 | the other declared properties | the kit's named limit R7 (D6), unchanged |
| P4 | a property change invisible to `same` (type, name, state, tags only) | covered here: `inv-before.out` and `inv-after.out` byte-equal |
| P4 | what-if leaving a deployment record | covered: `dep-before` and `dep-after` both `[]` |
| P4 | a write outside the group (subscription scope, role assignments, activity log) | named limit: the tool lists 0 write verbs (`LIST: 14 entries (8 what-if, 6 read, 0 write)`); `role assignment list` and the activity log were not read (UNMEASURED) |
| P5 | a third path in the commit | covered: compare 2 files; my `diff --name-status` 2 rows `A`; head tree = BASE + 2 |
| P5 | a secret in the message or a blob | covered: gitleaks (below), the hosted neutral scan |
| P5 | an id, name or word a client must not see | covered: point (c) above, `words.py` and the B-number count (below) |
| P6 | a second endpoint connection on the namespace | covered: FAILS (n1) |
| P6 | the same leaf at another array index or on another resource | covered: FAILS (n4, n9) |
| P6 | a NOISE value whose real deploy effect is destructive | named limit I3 (N6) |

## SCANS
- gitleaks 8.30.1, control FIRST: a token-shaped value built by a program (never printed) in `g2204/gl-control/`:
  `gitleaks dir ... --no-banner --redact --ignore-gitleaks-allow --exit-code 1` rc 1, `leaks found: 1`. Then:
  `gitleaks git <scratch clone> --log-opts='d9f89115..14896ed0'` rc 0, `1 commits scanned`, `no leaks found`; the two
  origin blobs and the commit message as `1.txt` to `3.txt`: rc 0, `no leaks found`.
- `words.py` (the lane copy, sha256 `6f932dc5...`) `--control`: `CONTROL FIRED: 13 of 13`; over the added lines of
  `d9f89115..14896ed0` (311 lines, 9897 bytes, `cmp` equal to the seat's `scratch/checks/added.txt`) and the commit
  message: `WORDS: clean (2 files)`, rc 0. B-number pattern `(?<![A-Za-z0-9])B2[0-9]{3}(?![0-9])`: 0 and 0; control: the
  lane's parameters file 1.
- Landing texts: see FOR-RECORDS.md and landing.txt (squash_scan and words over the subject, body and title).

## MAIN AT THE END: MOVED
`d9f89115...` at 03:14:07 and 03:20:10; **at 03:23:44 main is `e1802e24d87bf8663f3f904ff478a833d483268f`** (PR #63's
squash, merged 2026-11-27T16:20:23Z = 03:20:23 AEDT; tree `58145d4f...`; one parent `d9f89115`). `compare
d9f89115...e1802e24`: 16 files, **0 under `deploy/`, 0 under `.github/`** (so ci.yml is unchanged and nothing deploys);
`compare e1802e24...14896ed0`: ahead 1, behind 1, 2 files. The branch is unchanged (`14896ed0...`); open pull requests
0. The gate's reading of the two files and every Azure answer stands (no path of this lane moved); only the hosted
numbers of the merge ref change: landing.txt MAIN MOVES (B) applies, with e1802e24's own push-run PASS line (its
windows leg was still `in_progress` at 03:24:18; the other six rows success). No merge with e1802e24 was built by the
gate (DERIVED: disjoint paths, no conflict possible). Lane listings: no file in `<lane>` or `<x98>` newer than the
gate's first script (`find -maxdepth 6 -newer`: 0 rows; the `ls -laTR` hash of both lanes moved only by the `..` line,
the shared `.tools` folder's time, 03:24:07, written by other seats). No az process.
