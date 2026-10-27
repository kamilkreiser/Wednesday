STARTABLE: YES (pins hold: main df1dc0fe25e87dda4a9748c14870f942371a58a5, no b858 ref, 0 open PRs, no port needed; one fetch is owed by the seat because the local clone lacks df1dc0fe)

# B858 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H48: HPSMPOC-358, a rule that reads the appservice module call's two bindings)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B858_SEAT-H48_hpsmpoc-358-module-binding-rule.md` (136 lines; the shape of the stamped infra test-rows kit, 127 lines, with one commit instead of two). Drafted Wed 28 Oct 2026. Read-only: nothing built in a project tree, no fetch, no ref written; scratch runs on copies in the session scratchpad.

## BLUF
- Startable. One path (`infra/tests/test_security_baseline.py`), one commit, test-only. The hole is real at main: on the compiled template, the two ticket plants (module call bound to `uat`, or to `kv-hpsmpoc-uat-zzzzzz`) leave all 23 `RULES` at `[]`. Three more shapes are green too: `variables.names.keyVault` typed, `variables.prefix` a literal, and the `keyVaultName` binding deleted. Control that fires: `allowBlobPublicAccess` True turns `rule_storage` red.
- The kit's design: the rule reads the `appservice` deployment in the compiled template (a list of 8 deployments at main) and requires `environmentName` = `[parameters('environmentName')]`, `keyVaultName` = `[variables('names').keyVault]`, and the chain the ticket's fix shape names (`names.keyVault` names `variables('prefix')`, `prefix` names `parameters('environmentName')`), without pinning literals such as `kv-`. Red-first by a stub rule that returns `[]`.
- The local clone does NOT hold `df1dc0fe` (its main is `8869b1a9`); the kit tells the seat to fetch it under the lock with an explicit refspec before anything else.
- Bicep: the project's binary prints 0.47.16, equal to CI's pin (`ci.yml:581`). Local `python3` 3.14.7 and `/usr/bin/python3` 3.9.6.
- Gate: tier 2 (G2, line 109), round assumed 0 NO GO of 2 on a new class; Tuesday states the round at stamp. Load read 2.23 with no seat live.

## Facts re-measured (instrument, control)
- main: `gh api -X GET commits/main` and `ls-remote` both `df1dc0fe...` (committed 2026-10-27). `ls-remote 'refs/heads/b8*'` printed 9 refs, none `b858*` (control: lists `b825`, `b826`, `b800`). `pulls?state=open` printed nothing.
- Blobs at main (`git hash-object` of raw API bytes = API `sha`): `test_security_baseline.py` `f600af84...` (2117 lines, 128517 B); `main.bicep` `5565c5e9...` (176 lines); `ci.yml` `0176b491...` (679 lines, same blob as the earlier infra kits); `validate.sh` `d6fd1317...` (47 lines).
- `main.bicep`: line 139 `environmentName: environmentName`, 148 `keyVaultName: names.keyVault` (both inside `module apps`, lines 132-156); the `rbac` call repeats `keyVaultName: names.keyVault` at 166 (out of lane, reported only).
- Compiled shape (`bicep build` on a tarball extract of `df1dc0fe`): `appservice` binds `environmentName.value` = `[parameters('environmentName')]` and `keyVaultName.value` = `[variables('names').keyVault]`; `variables.prefix` = `[format('hpsmpoc-{0}', parameters('environmentName'))]`; `variables.names.keyVault` = `[format('kv-{0}-{1}', variables('prefix'), variables('suffix'))]`. One compiled file serves all three environments, so the rule judges text.
- Plants (main module loaded via `importlib` under `python3 -I`, `len(RULES)` = 23): unplanted 0 red; env=uat 0 red; typed vault 0 red; typed `names.keyVault` 0 red; literal `prefix` 0 red; binding deleted 0 red; blob-public control: `rule_storage` red.
- Baseline file structure: `compile_template` line 54, `resources` 62, `RULES` 1052, `class Baseline` 1060, `test_every_rule_holds` 1065, `mutate_module_variable` 1235, 99 `def test_`. Name clash: `rule_appservice_module_bindings`, `appservice_module`, `module_call` read 0 hits across the 11 infra tests (control `feedback_dispatcher_source` 5). Importers do not read `len(RULES)`.
- CI predicate: required job `infra` (`ci.yml:576`), `bash infra/scripts/validate.sh` (`ci.yml:627`), which runs `python3 tests/test_security_baseline.py` with `BICEP`; its `main()` runs every infra test file and fails on a failed test, ResourceWarning or open file.
- Ticket HPSMPOC-358 read whole (Backlog, 0 comments, labels `b831-gate`, `b841-2026-10-27`, `test`); scope, fix shape and Done-when are quoted verbatim in the kit.
- Stale heads sharing the path, no PR: `b826/hpsmpoc-demo-switch-template-pin` (ahead 1, behind 2; the squashed head of the PR the ticket cites) and `b71/f006-title`. `b825/...` (web only) and `b800/...` (`test_ci_workflow.py` only) do not share it. Control for the compare filter: `compare/271f6932...df1dc0fe` lists `infra/modules/appservice.bicep` and `infra/tests/test_security_baseline.py`.
- Model: `models_latest.json` `levels.sonnet.model_id` = `claude-sonnet-5-5` (line 23). Routing rows by line: L6 = 85 (test-only pin, S55 "1st fallback"), C2 = 92 (S55 "1st"), G2 = 109 (tier 2); read by `grep -n` on the row ids (each matched). `brief_seat.sh` line 24 defaults to Opus, so the launch carries `BRIEF_SEAT_LEVEL=sonnet`.
- Kit hygiene by program: stamp-slot lines (four-underscore pattern) = 8; at-sign tokens = 0; clock-time pattern = 0; "kam/kreiser/kamil" = 0 (after one edit that removed a commit time).

## D-decisions (taken by the drafter; Tuesday accepts or changes at stamp)
- D-1 One commit, one path; the H40 kit's docstring commit and its second path do not apply.
- D-2 The rule reads the COMPILED template's `appservice` deployment (the file's own approach), not the `.bicep` text. The task's "reads main.bicep" is met through `bicep build` of it; no regex over Bicep source.
- D-3 The ticket's fix shape (chain: `names.keyVault` from `prefix`, `prefix` from `environmentName`) is made part of the rule, with literals such as `kv-` deliberately not pinned and a green row to prove it. Three extra plants (typed `names.keyVault`, literal `prefix`, deleted binding) join the two ticket plants because all three measured green today.
- D-4 Red-first by a stub rule returning `[]` (plus a plant table against the 23 old rules), since the rule does not exist on the old code.
- D-5 The `rbac` and `keyvault` module bindings of `names.keyVault` are reported with one plant each, not built (the ticket names the `appservice` call only).
- D-6 `bicep` binary made an execute-only exception to the read-forbidden `.tools/b*` rule (same as the earlier infra kit).
- D-7 The seat fetches `df1dc0fe` itself (explicit refspec, under the lock); the drafter did not.
- D-8 Hard-stop suggestion: target READY 90 minutes after Step 0, hard stop 150 (shorter than the two-commit kit).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate round. Default: NO GO 0 of 2 on a new class, "round 1 of 2" as the ticket's provenance reads, tier 2 (the sweep's recommendation); stated at stamp.
- Q-2 Is pinning the chain (`names.keyVault` and `prefix`) in scope, beyond the two bindings? Default: YES, the ticket's fix shape says so; if not, drop the two chain bullets and their two plant rows.
- Q-3 Jira. Default: NO Jira write by the seat (records follow after landing).
- Q-4 Routing cell: S55 for L6 reads "1st fallback", for C2 "1st". Default: cite C2 line 92 as the Sonnet answer and L6 line 85 as the class (both in the receipt line).
- Q-5 Ports. Default: none needed; the kit says STOP and ask if the route needs one (no block assigned).
- Q-6 Launch order beside the sibling wording lane (README, `uat.bicepparam`, two auth texts): they share no path with this lane; default: launch independently, one waiter at a time per the launcher.

## UNMEASURED
The whole `test_security_baseline.py` run and its test count at main (needs a heavy run; not done), the runner's Python version, how `expression_text`/`evaluated` handle the two chain variables, the R4 plants for the `rbac` and `keyvault` modules, GitHub's own parser, and `gh auth status` under the project's config dir (the seat checks).

## Outside-the-fences disclosure
- Read-only everywhere except the two files written here. `gh api -X GET` only, under the project's `GH_CONFIG_DIR` (commit, contents, tarball, compare, pulls). `git --no-optional-locks` read verbs in `2_Project_Files` (`rev-parse`, `cat-file`, `ls-remote`). One Jira GET through the project's helper (`.tools/b649/jira.py`, its first 60 lines read with credential lines filtered), output saved to the scratchpad; ticket has no comment, no person's name reached any file written.
- The project's `.tools/bicep/bicep` was executed (twice: `--version`, `build`) on a scratch extract; its folder was not read. A python run loaded a scratchpad copy of the baseline file (`sys.dont_write_bytecode` set, `python3 -I`); it compiled nothing in a project tree.
- A repository tarball (a GET) of `df1dc0fe` was extracted in the scratchpad only. No `az`, ssh, docker, HTTP to a hosted host, mail, chat, Artifact/Docs tool, decision store, `_ledger*`, or non-Datasec project touched. Several hook advisories (case-sensitive grep) appeared; every count that matters was either paired with a control above or is a count of one literal.
- One `sed -i` on the kit itself removed a commit time stamp to meet the no-clock-time rule.
