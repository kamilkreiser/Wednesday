STARTABLE: YES (stamp, then launch at load1 below 7; three Q-questions below, each with a default)

# B826 drafter report: HPSM-POC demo switch + key references pinned in the infra template (SEAT-H47)

## BLUF
- The kit is 95 lines, 8 stamp slots (`_{4}` count 8, as unstamped kits read), in the shape of the B814 builder kit.
- **The brief's premise is partly off, and the kit says so.** At origin main `271f6932` the template ALREADY carries the switch and both key references, keyed on `'uat'`; `HPSM_ENVIRONMENT` is already `environmentName`. So (1) "UAT stays off" cannot be literal: UAT's switch is ON today and must compile unchanged; (2) FOUR demo values change (API `Auth__UatOpen__Enabled`, API `Auth__UatOpen__Key`, web `HPSM_UAT_OPEN_SIGNIN`, web `HPSM_UAT_OPEN_KEY`), not three; `HPSM_ENVIRONMENT` needs no edit.
- **The bigger work is the guard, not the template.** `infra/tests/test_security_baseline.py` hard-codes "uat only" (`UAT_ONLY` 573, `KV_SECRETS` 611, `UAT_ONLY_KV*` 621-657, rule list 875-876, rows ~1024-1087, and a regex that parses the exact compiled `if(equals(...'uat'...))` shape). Any template edit turns these red, so the kit makes the builder rewrite them as per-environment own-secret rules (Property R), not loosen them.

## Facts re-measured (instrument; control)
- origin main = `271f69328c8506c38243066a2853d9eee2ed9e0f` (`gh api -X GET branches/main`). `compare bf4a7bdd...271f6932` lists `RequestTimingLogTests.cs` and `infra/tests/test_ci_workflow.py` only: the infra files I read are unchanged since the B814 kit's reads.
- Compiled with the local `.tools/bicep/bicep`: `--version` = `Bicep CLI version 0.47.16` = CI pin `ci.yml:581` (`v0.47.16`). `build main.bicep` rc 0; `build-params` dev/uat/demo rc 0 (scratch copies only, files fetched by `gh api -X GET` at `271f6932`). One `main.json` serves all environments; the five settings sit at main.json lines 1389/1393/1483/1487/1491 as `if(equals(parameters('environmentName'), 'uat'), ...)`. `demo-open-key` count in the compiled template 0; control `uat-open-key` 2.
- B810 STATUS (RELAYED): the live demo got `Auth__UatOpen__Key` (reference to `demo-open-key` in `kv-hpsmpoc-demo-en46o7`), web `HPSM_UAT_OPEN_KEY` (same), `HPSM_ENVIRONMENT=demo`, then the two switches; last line "template pins the switch off".
- Model: row C3 line 93 (auth/security surface, Opus first) rather than C2 line 92; gate G1 line 108 (tier 1); G-cap 111; opus id `claude-opus-5-5` (`models_latest.json` line 17). `brief_seat.sh` defaults to Opus; the launch line still carries `BRIEF_SEAT_LEVEL=opus` inside the quotes.
- Ports 7660-7669: `lsof -nP -iTCP:7660-7669 -sTCP:LISTEN` empty (rc 1); the word-boundary scan of 2026-10-26/27 non-`.pre-` SEAT kits hit no file (controls: `x 7661 y` 1, `x 17661 y` 0). No positive lsof control run (no listener bound by me): the zero is weaker than B814's. Panes: `tuesday`, Security-Composer-J26, MPS-M47, MPS-M44, MPS-M40, NexusAI-M21, `fleet-monitor`. No `matching-refs/heads/b826` (0; control `b709` 1).
- Landing: `rules/branches/main` = `deletion,non_fast_forward,code_scanning,required_status_checks`; no merge-method rule; one squash precedent only (taken from the B814 kit's read of `CLARIFICATIONS.md:138`, not re-read by me).
- Seat name H47: highest HPSM-POC builder name in the briefs folder is H45; I skipped H46 for sibling B825 (builder names are not otherwise reserved).

## D-decisions
- D-1: Opus builder, tier-1 gate (row C3 + G1), because the change flips an authentication switch and rewrites security assertions.
- D-2: Scope is the template plus the baseline rules/rows, two files; README only under Q-1.
- D-3: "UAT unchanged" is proved by compiling base and head with the local Bicep and evaluating the five settings per environment with the baseline's own evaluator (no az, no what-if), with a planted-edit control.
- D-4: Demo key reference names the secret `demo-open-key` in the environment's own vault; each environment may only name its own secret (new guard rule).
- D-5: Branch name `b826/hpsmpoc-demo-switch-template-pin`, a NEW ref; no PR (Tuesday opens it).

## Q-questions for Tuesday (each with a default)
- Q-1: `infra/README.md` ("UAT review copy: no sign-in") may state that the switch is UAT-only. Default: the builder may edit that ONE sentence if it is now false, and reports it as a third path.
- Q-2: Is the ruling's "UAT stays off" meant as "UAT unchanged (switch on)"? Default: yes, the kit says so; if the product owner meant UAT's switch turned off, that is a different ruling and a UAT behaviour change, STOP before stamping.
- Q-3: Sonnet instead of Opus? Default: no (row C3, security surface; B810 ran on Opus).

## UNMEASURED
`validate.sh` end to end and the baseline test count (not run: needs the full tree); `bicep lint` on the future form; whether the open-PR list is truly empty (`pulls?state=open` printed nothing, no control); the runner's Python; the live demo's settings and the `demo-open-key` secret (no az, RELAYED only); whether `UAT_ONLY_KV_IF` is the only parser tied to the compiled shape (I read lines 566-670 and 1020-1090, not the whole 1819-line file).

## Outside-the-fences disclosure
Read-only: wrote only the kit and this report. Fetched ~16 infra files plus ci.yml and the baseline test to the session scratchpad via `gh api -X GET` (project `GH_CONFIG_DIR`); ran `.tools/bicep/bicep --version/build/build-params` on scratch copies only (local binary; no az, no HTTP to any hosted host). One `git ls-remote` attempt failed on a missing deploy-key path (no effect, and I switched to `gh api -X GET`). `tmux list-panes`, `lsof`, listings of the briefs folder and of `.tools`. No decision queue, ledger, scoreboard, `briefs_staged`, WEDNESDAY/FRIDAY tree or other project was read. Card ids appear in this report only inside quoted source comments? No: none quoted; the kit holds none.
