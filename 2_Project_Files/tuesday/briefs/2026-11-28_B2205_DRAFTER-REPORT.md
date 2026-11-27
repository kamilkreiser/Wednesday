STARTABLE: YES (after the stamp; Q1 to Q3 are answerable by default)

# B2205 DRAFTER REPORT: kit for seat X104, lane AZ-1 text-only round 2 (fix of gate B2204 F1, F2, F3, S1, S2)

Drafted by a read-only in-session drafter (Opus 5.5) for Tuesday s337 under commission B2205 and DRAFTER_RULES.md.
First `date`: Sat 28 Nov 2026 03:26:18 AEDT; last `date` before this report: Sat 28 Nov 2026 03:38:00 AEDT.
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2205_SEAT-X104_oxpd2-az1-r2-text.md`
Sidecar: `...SEAT-X104_oxpd2-az1-r2-text.md.measured` (102 claims, `stamp_check.py` rc 0: "102 measured, 0 not measured").
Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2205/` (seat tools in `seat-tools/`, evidence in `evidence/`).

## BLUF
- The seat adds ONE fast-forward commit on `b2191/az1-bicep-foundation-r2` on top of `14896ed0` (no rebase, no force),
  changing only `deploy/azure/README.md` (41 -> 53 lines) and the comment at `main.bicep:47` (one line -> three
  comment lines 47-49). No az, no login, no lock, no dotnet.
- **Compiled-hash proof (MEASURED, pinned Bicep CLI 0.48.1, sha256 62cd5958...):** HEAD0's `main.bicep` ->
  `ba7a31d7e6c90eb1596fe7e83b01c7044eb4c8eacf1a0adf5c67645cbade8546`; the revised `main.bicep` ->
  `ba7a31d7e6c90eb1596fe7e83b01c7044eb4c8eacf1a0adf5c67645cbade8546` (EQUAL); control (one `@description` text
  changed) -> `e22b3603d74d...7653` (differs). The five mutants built from the revised file each equal X99's table.
- `checks2205.py` (my narrowed copy of `checks2189.py`, 10 checks): 10 of 10 PASS, 10 controls fired on the staged
  revision; control-tested on two planted faults (HEAD0's bytes: 5 of 10; a `priority 4095` edit: 7 of 10).

## The text change (frozen in `seat-tools/deploy/azure/`)
- F1: README bullet now says the NSG holds an explicit deny-all inbound rule and two outbound allow rules to the PE
  subnet, and "outbound traffic is not restricted by this template"; a new known difference says Azure's default
  rules allow the whole VNet and the Internet, and that a deny-all outbound rule is owed to the server lane. Bicep
  comment lines 47-49 say the same.
- F2: the check sentence is the judge's rule (NoChange, or Modify whose every changed property is NoEffect or one of
  six Azure-set values, named in words); `Modify` removed from the forbidden list.
- F3: "The Log Analytics workspace allows public network access for ingestion and for query."
- S1: the Relay rule named (`RootManageSharedAccessKey`, rights Listen, Manage and Send) and "does not turn off
  key-based access to the namespace" (a fact of the template; whether the live namespace allows it is not claimed).
- S2: the vault: "no network rules", "keeps deleted items for 7 days by default (`keyVaultSoftDeleteRetentionInDays`)".
- Gate line pointers below `main.bicep:47` shift by +2 (MEASURED by `grep -n`: 252-253 -> 254-255, 225/232 -> 227/234).

## Facts re-measured with instruments (03:26 to 03:38 AEDT)
- Origin (`gh api -X GET`): branch ref ONE row `14896ed06f46536073a25a4d1388d4431ca04169`; main
  `e1802e24d87bf8663f3f904ff478a833d483268f` (parent d9f89115, tree 58145d4f); `compare main...branch` ahead 1,
  behind 1; `compare d9f89115...e1802e24` 16 files, 0 under `deploy/`, 0 under `.github/`; open PRs 0 (#63 merged);
  `matching-refs/heads/b2205` 0; private true, push true.
- HEAD0 files from the origin: main.bicep `8a8d38f9...9274` (7538 B, 270 lines), README `20c35ef9...600d` (2359 B,
  41 lines), message `e4ca4a3a...33f7`: equal to gate B2204's values.
- HEAD0's hosted run (my `hosted3.py`): `HOSTED 14896ed0...: PASS` at --total 2539 --rules 764 (skipped 4/21, guards
  14/15, floor 117); control --total 2540 `FAIL 4`. Run 46030871938 took about 4 minutes.
- Local on my staged scratch clone (`<d>/repo`, a `--no-hardlinks` clone of X99's clone, push URL invalid, tree of
  HEAD0 equal to the origin's `0f84e8d9...`): `RULES: clean (764 files)` rc 0; gitleaks 8.30.1 control rc 1, blobs
  and message rc 0, dir rc 0; `words.py` control 13 of 13, `WORDS: clean (3 files)` over added.txt (325 lines),
  added-fix.txt (23 lines), the message; B-number count 0/0 (control 1); `whatif2189.py --selftest` over the revised
  template 72 of 72; `list` 13 declared, 7 ignore, 6 noise, 5 mutants.
- Seat tools (ten files): six byte-equal to kit B2191's (`cmp`), four new; hashes in the kit's THE TOOLS (03:31:39).

## Chain inputs (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, stamp S1-S8 | Tuesday |
| 1 | `seat-tools/` (exists), the CLI (exists), `<repo>` local git values, origin HEAD0, HEAD0's push run | scratch, project, GitHub |
| 2 | clone at HEAD0, `L/gate/deploy/azure/*` | Step 1 |
| 3 | gate files, `L/bicep/bicep`, parameters file | Step 1 |
| 4 | staged tree, `L/whatif/green/*` | Step 3 |
| 5 | the commit, the branch ref, `run_step.py`, `hosted3.py` | Step 5(a), GitHub, Step 1 |

## D-decisions (in the kit)
D1 text only (comment lines and README); D2 fast-forward on HEAD0, no rebase, base stays d9f89115; D3 the F1 owner
named "the server lane" in repository text; D4 the six values in words, no N-ids; D5 a new commit message (403 B,
3 lines, words-clean).

## Q-questions for Tuesday (each with a default)
- Q1: the repository text names "the server lane" as owing the deny-all outbound rule. Default a (built). Alt b: no
  owner in the repository text.
- Q2: the six Azure-set values named in words in the README. Default a (built). Alt b: "a closed list" unnamed.
- Q3: the round-2 gate tier. Default a: G1 (security statement; `model-routing.md:108`). Alt b: G2 docs tier (:109),
  since nothing that compiles changed.
- Q4: windows READY Step 0 + 75 min, push by + 45; pane `Datasec/OXPd2-X104`; launch now.
- (Not a stamp question, for Tuesday's landing) the B2204 landing form pins `--match-head-commit 14896ed0`: it is
  void for the new head; the round-2 gate writes a new one (MAIN MOVES (B), main e1802e24).

## UNMEASURED / NOT RUN
- The seat's commit, its neutral scan (`run_step.py`: needs a commit; literal forms RELAYED from X99's log lines 4,
  6, 9), the push line form (git's documented form, NOT RUN), the new head's hosted run (PREDICTED 2539/764).
- `clone.py` REF line: DERIVED from its line 42 and the origin ref; I did not run `clone.py`.
- `build/tests` not run (the commission's check list omits it; the hosted `rules` job runs it; the OXPd wave lock
  `wave1-heavy.lock.d` was held at 03:28, and I ran no test).
- Every README claim about the live group is RELAYED from gate B2204 (X92's saved NSG answer, rule rights); no az.
- Azure's NSG default-rule semantics ("allow the whole virtual network and the Internet") are as gate B2204 states
  them (MEASURED rule names in X92's answer, DERIVED semantics from Azure's documented NSG model).

## Outside-the-fences disclosure
- Writes: the kit, its `.measured`, this report (briefs folder); everything else under
  `fleet/state/s337/d2205/` only. No write to any project file, lane or repo.
- `git clone --no-hardlinks --no-checkout` FROM X99's clone (`.tools/b2191-x99/clone`) into my scratch: a read of
  that repository (the same method gate B2204 used); X99's clone `status --porcelain` 0 lines after. A first attempt
  with a variable path was refused by the no-cd hook before running.
- Read (no write) from X99's lane: the six `whatif/*/main.json` hashes, the STATUS tail and section headers, and
  `logs/neutral-scan.log` lines 4, 6, 9. The kit forbids the SEAT from reading that lane.
- No az, no lock, no dotnet, no Jira, no mail, no Artifact/Docs, no `decision_queue.sh`, no Source_Documents, no
  credential read (`GH_CONFIG_DIR` used for `gh` only). The pinned Bicep CLI was run only in my scratch.
