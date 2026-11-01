STARTABLE: YES (after Tuesday stamps the seven slots and the last line; until then the kit's own REFUSE line on four-underscore runs fires, by design)

# B1075 drafter report (row C8, Sonnet), SEAT-G268, MPS tier-1 gate, round 1 of 2

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1075_SEAT-G268_mps-253-quantity-rules-gate-tier1.md` (70,376 bytes, 0 non-ASCII, no person name or login by an `-i` scan for the owner's name tokens, 0 card ids). Shape copied from the B1051 gate kit (read whole) and its STATUS (read whole); the builder kit B1062 (read whole, 137 lines) and its STATUS (read whole, 249 lines) are the inputs. Dates: it was Mon 2 Nov 00:0x AEDT when I measured; the file name keeps the commissioned `2026-11-01_B1075` prefix.

## BLUF
- Branch `b1062/mps-253-component-quantity-rules` is `8d6a6b51e4ca0dcfa626a4367f9d20f8bdc3dc06`, one commit on main `3496da33ab3d7d2c6b7d7ec2c3014ae03518e020`, 6 paths, +578 -12 (re-measured by `gh api -X GET compare` and by `rev-list --left-right --count` in the code repo: `0 1`). No PR, no hosted run. Round count: 71 `GATE VERDICT` first lines, 0 naming the class (control: 3 for the two adjacent classes). Round 1 of 2.
- The kit has the eight steps you listed, in your order, as steps 1 to 8, with the severity table, the verdict-line forms, the sweep property, the Stamp (7 slots plus the last line, all `____`), and the launch line through `launch_when_cool.sh` with `BRIEF_SEAT_LEVEL=opus` inside the quotes.
- Things in the kit that differ from the B1051 template on purpose: the squash bodies are forbidden to carry `NOT TESTED`, `NOT RUN`, `not scanned` or the word `hosted` (MPS #136's body ends `NOT TESTED: hosted CI and CodeQL.`, read from the merge commit); the web and python CI jobs are read and judged NOT RUN by reason (no changed path; local node v26.8.1 against CI's 24; python needs `az bicep`); the gate's times are `date` outputs and the 3 h / 5 h plan is written as a duration plus a labelled PLAN clock.

## Facts re-measured (instrument, control)
- Branch and main: `gh api` refs and `git ls-remote origin` agree (`8d6a6b51...`, `3496da33...`); `matching-refs/heads/b10` 62 (control for the 1-ref `b1062` read). Open PRs 121 and 120; `pulls?state=all&head=` 0; `actions/runs?head_sha=` 0; squash settings COMMIT_OR_PR_TITLE / COMMIT_MESSAGES; `ci.yml` blob `212b0da1...` at head.
- Commit message read whole: 10 body sentences by a full-stop-plus-capital split, one trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; unsigned.
- Diff read whole except the 533-line test file. Decision points the kit names: `extended` condition, the second textual read of the same predicate in the `lines` selection, `Enum.IsDefined` check, the carried-rule line, `QuantityOf` in the reconciler, two `JsonIgnore(WhenWritingDefault/Null)`, the enum order, one const and two literals.
- `InputHash.Compute` runs at `PurchaseCalculator.cs:151`, before `CheckPurchaseStructure` (so an undefined enum reaches the hash first; kit step 2n and the commit sentence "before any figure is formed" are aimed at it).
- Contract surface: `docs/api/openapi.json` `PurchaseBomLineInput` additionalProperties false, 13 properties, `quantityRule` absent (0 hits; control `pricingMethod` 4); `PurchaseMapping.cs:33-35` builds `PurchaseLine` with 13 positional arguments; `QuantityRule` in 6 files at head, 0 at main, 0 under `src/MpsCalc.Api`, `src/MpsCalc.Import`, `tools`, `web/src`. `Deserialize<(PurchaseQuoteInput|PurchaseLine|QuoteInput)>` is 0 at main and 3 at head, all in the new test file (:479, :481, :485): the builder says 0 for main, which is right; the kit states the 3.
- Real serializer options: `ReferenceStore.JsonOptions` (camelCase, indented, `JsonStringEnumConverter`), `ApiJson.Options` (`Disallow` at :23, `WhenWritingNull` at :24, `NumberHandling.Strict`), `InputHash` private options (no naming policy, `JsonStringEnumConverter`). The Engine test project references only the Engine (`.csproj:26`), which is why the builder's Correction 3 exists; the kit makes the gate measure them in its own harness.
- CI: four jobs (dotnet, web with node 24, python with `az bicep`, package needing all three). Local `node` v26.8.1, `npm` 11.19.0, dotnet SDK `.tools/dotnet/dotnet` 10.0.401, `/opt/homebrew/bin/gitleaks` 8.30.1.
- Headers read (not invoked): `launch_when_cool.sh` (args `<cockpit name> <command string>`; LOAD_MAX 7, MAX_WAIT 3600, GAP_MIN 120, one waiter, rc 4/5), `brief_seat.sh` (args `<project dir> <absolute brief path>`; `BRIEF_SEAT_LEVEL` defaults to opus, line 24).
- Rulings quoted from the project's file: C-45 words at `CLARIFICATIONS.md:660`; C-79 heading :1712, words :1714, settles :1716; landing rule :758 and :774 (both still read as the B1051 kit quotes them).
- Ports: none needed. Fallback block 9800-9809: `lsof -nP -iTCP:9800-9809 -sTCP:LISTEN` 0 rows (all listeners 12). Word-boundary scan of the 103 non-`.pre-` SEAT kits of 10-31 and 11-01 for `980[0-9]`: 2 files, both the text `9800-9999` in NexusAI records kits that bind nothing; control `974[0-9]` 10 files. `G268` and `B1075` in other kits: 0 (control `G265` 10).
- Panes at 00:00: `%0 tuesday`, `%19 HPSM-POC-G266`, `%18 MPS-G265`, `%17 NexusAI-G264`, `%16 HPSM-POC-R121`, `%15 MPS-R120`, `%14 Security-Composer-G263`, `%2 Security-Composer-J38`, `%1 fleet-monitor`. No `MPS-M66`, no `MPS-G268`. Partition lines for G265 and R120 read from their kits (grep lines), not their trees. B1074 does not exist yet in `tuesday/briefs/` (highest B1071 at 00:00), so the kit tells the gate to re-read panes and a builder's PARTITION line when one appears.
- Load: load1 2.96 at 00:00, 8.28 at 00:09 (above 7: the waiter handles it). `.tools/heavy-slot-1` flaps (listed at 00:00, gone at 00:01, listed then gone again later): another seat's; the kit says read the holder first.

## REFUSE and STOP lines tested against the live state (00:09:37 AEDT)
1. Four-underscore count in the kit: 8 (expected for an unstamped copy; control: one planted line gives 9). The REFUSE fires on this copy by design until stamped.
2. Last line `READ-WHOLE-BY-TUESDAY: ____`: does not match `DONE` (count 0), as intended.
3. Pane: `G268` listed 0 times; `-t %0` prints `tuesday`, `-t %18` prints `Datasec/MPS-G265`: the predicate separates panes.
4. Head: `git ls-remote origin refs/heads/b1062/...` `8d6a6b51e4ca...`; main `3496da33ab3d...`. Does not refuse.
5. PR for the branch, all states: 0. Does not refuse.
6. Main moved: `compare 3496da33...main` 0 files (control `compare 3496da33...8d6a6b51` 6). Does not refuse.
7. `.tools/b1075` / `wt-b1075-*`: 0 (control `b1062` / `wt-b1062-*`: 3). Does not refuse.
8. Builder STATUS last line begins with the exact READY text: 1 (control wrong sha: 0).
9. PRIOR WORK section: `27:## PRIOR WORK (at base 3496da33)`. Does not refuse.
10. `gh auth status` under the project config: active account true, protocol ssh.
11. Model: `models_latest.json:17` `"model_id": "claude-opus-5-5"`; the launch string carries `BRIEF_SEAT_LEVEL=opus bash` (count 1).
12. `records/*` in the code repo: `ls-remote --heads origin 'records/*'` 0 lines (control `main`: 1).
13. STOP lines: `.tools/.git-lock` absent (0); `/private/tmp/b1075-seat-tmp` absent (0); no listener in 9800-9809; dotnet and gitleaks versions print; 0 `az` in the kit's allowed commands.
Nothing refuses except the two unstamped-slot lines, which is correct. One count I could not make with the machine's `grep`: non-ASCII with `-P`; I counted it with `python3 -I -B` instead (0 of 70,376 bytes).

## D-decisions
- D-1: mutants are `GQ1`-`GQ34` (not `MQ`), so the gate's list never collides with the builder's `MQ` ids; GQ1-GQ26 re-derive MQ1-MQ22 plus the four splits the builder added; GQ27-GQ29 target the rows the builder admits have no mutant (`n2`, `o3`, `l2`); GQ30-GQ34 are mine (refusal text pinned, hash drop, reconciler read, non-group zero).
- D-2: the Done-when table is the five clauses of the builder kit (register rows, red-first per rule, fixed not multiplied, manual as typed, unknown refused), with the `PerDevice` red-first reading handed to the gate as a judgment with three named meanings.
- D-3: the two readings (N 0, tier pool) are step 3, measured with the alternative mutant beside each, graded only "does the build do what Q-6 and Q-7 stated"; the kit says in three places they are the coordinator's readings.
- D-4: "what a records seat should file" covers `perSite`, `usageOnly`, the Api/DTO/openapi/docs/API.md/web half, the spelling gap (`fixedPerGroup` vs `FixedPerGroup`), the committed row for the real store and Api options, and the reconciler's FleetTotal limit.
- D-5: the gate reads no Jira; the ticket acceptance is RELAYED from the builder kit.
- D-6: bodies for the squash may name X-35, X-40, X-41, X-42; the key MPSCALC-253 may appear in the title and subject only.

## Q for Tuesday (each with a default)
- Q-1: may MPSCALC-253 appear in `pr-title.txt` and `squash-subject.txt` (with ENGINE HALF), as -256 did? Default YES, neither body.
- Q-2: keep "web and python jobs NOT RUN by reason" (changed-path proof, node 26 vs 24, no `az`)? Default YES.
- Q-3: should the squash bodies avoid the word `hosted` entirely (the kit's program check counts it)? Default YES; the hosted facts live in STATUS and the lander's own reads.
- Q-4: a builder kit B1074 may launch beside the gate; the kit only asks the gate to re-read panes and name it. Default: no extra partition text until B1074 exists; if it does before the stamp, add its PARTITION line to S2.
- Q-5: candidate falsities I spotted and put to the gate as "read, not trusted", not as findings: (a) X-35's unchanged sentence "shared by N x quantity devices" for a FleetTotal line against X-41's "shared by the typed quantity"; (b) X-40's "each is an unknown rule today" (by name it is a deserialisation error, by integer 3 or 4 it is the engine's refusal); (c) the commit's "before any figure is formed" against the hash computed first; (d) `PurchaseRecomputation.cs:218` left short (builder Correction 8). Default: leave as the kit has them.

## UNMEASURED
- No build, test, harness or mutant was run; none of the builder's counts (555/193/3,165, 35,658 records, 40 of 40, 78 of 78, 6 of 6, "20 of 22") is re-measured, only quoted as claims.
- The test file contents (533 lines), the builder's `n2`, `o3`, `l2` meanings (the kit makes the gate read them after its predictions), and whether the tier thresholds in the book allow the three-way split of step 2h (the gate reads `TierForPool`).
- Whether `ApiJson.Options` can read an engine result at all (the -256 gate could not isolate it); whether `ExactEnumNameConverterFactory` handles the new engine enum.
- The 3 h / 5 h clocks (written as durations), the launch time, and the hosted CI and CodeQL results.

## Outside the fences
None broken. Reads: the two kits and two STATUS files named, `DRAFTER_RULES.md`, the B1070 and B1067 kits by grep (PARTITION and Stamp lines only), the B1050-B1071 file listing, `model-routing.md` lines 90-112, `models_latest.json`, the two script headers, CLARIFICATIONS lines by grep and short `sed`, `ci.yml` lines 28-100 raw by `gh api -X GET`, raw and `git show` reads in `2_Project_Files` at the two commits, the merge commit message of #136. No `decision_queue.sh`, no Jira, no staged-brief folder, no ledger, no non-Datasec tree, no HTTP outside `gh api -X GET`. One scratch file was written to the session scratchpad (the compare patch) and one tool-output spill file was written by the harness. One slip: an unquoted zsh variable did not split in one `ls`, so I re-ran it under `bash -c`; nothing was written by it. I wrote only the kit and this report.
