STARTABLE: YES

# B1317 drafter report (SEAT-N101, NexusAI RD-798, lane L-N1), drafted 2026-11-06 10:27 to 10:37 AEDT

## BLUF
The kit is startable. All five alerts are open on main `ffb67152` and sit on the lines the sweep printed; the red cells are reachable over HTTP (the validate-condition control-character check lets CR/LF through). Two things the ticket does not say, both put in the kit as measure-and-print items: `logSafe` removes CR/LF and truncates at 500, and a KQL query is multi-line and longer than 500 characters, so wrapping it changes the log text of an ordinary query. A merge of this branch DOES trigger the Deploy demo workflow (the path ignore does not match `__tests__/` or `backend/`); both its jobs skip because `CI_DEPLOY_ENABLED` is unset.

## Facts re-measured (instrument; control)
- Main: `gh api -X GET branches/main` = `ffb6715230d1f5533746343f997e00b9854434f9` at 10:27 and again at 10:30; open PRs 0.
- Alerts: `code-scanning/alerts/{174,177,181,182,183}` all `open`, `js/log-injection`, rule severity `error`, security `medium`, ref main, commit `ffb67152`, lines 6191, 6249, 6308, 6539, 6550. Control: alert 220 `fixed`.
- Lines printed by `awk NR==` over a raw fetch of `backend/server.js` at that sha (`cmp` equal to the tarball copy): all five print the quoted text (see the kit's table). 182 and 183 also interpolate `${key}`, left alone.
- `logSafe.js` read whole at the sha: `:34` signature, `:29` `DEFAULT_MAX = 500`, `:41` removes `\n|\r` (empty replacement), `:42` U+2028/9 to visible escapes, `:43` other controls to `\xNN`, `:44` truncation. `server.js:45` requires it; 26 `logSafe` hits in the file.
- Route: `/api/validate-condition` `:6836`; control-char regex `:6856` excludes TAB, LF, CR from refusal; AI gate `:6915`; `validateConditionWithAI` `:5982` (called `:6919`); `getRuleBasedSuggestion` `:6414` called at `:6224`, `:6285`; `generateKQLQueryForCondition` `:5105`, its sanitiser `:5109` keeps `\s`; `baseKQL` `:5117` is multi-line.
- Source-level guards: tarball of main extracted into the scratchpad, grep over `__tests__/*.js` (322 entries). Files naming `logSafe`: rd774 (comments only), rd801, rd802 (neither reads server.js). A scan for `logger`/`logSafe` beside match/length/count/RegExp found no exact-count guard. Control: `logSafe` found in 3 files; 15 files read server.js as source. The kit tells the seat to re-run the scan at its clone (the drafter's scan is a regex screen, not proof of zero).
- Deploy: `deploy-demo.yml` at the sha: trigger `:26`-`:28` push to main with `paths-ignore` `**.md`, `docs/**`, `tests/**`; jobs `:53` and `:91` gated on `vars.CI_DEPLOY_ENABLED == 'true'`; `:95` `environment: demo`. Live: variables `total_count` 0; environments `dev`; newest four push runs `completed/skipped` (`ef446f85`, `54000972`, `cc4666dc`, `f3ab00bd`), newest run's two jobs `skipped`; 211 runs total (control). `deploy.yml` is `workflow_dispatch` only; `build.yml` carries the verify gate (`:83`/`:84`).
- Landing: `CLARIFICATIONS.md:2067` "Never squash, never rebase", `:665` C-68 head pin, `:2062`/`:2080` C-190 and its addendum. The repo allows merge, squash and rebase (all true), so "merge commit, head pinned" is the project rule, not a repository setting. NexusAI `CLAUDE.md` has no line on merge method (grep for merge printed lines 222, 273, 310, none about method).
- Counts file at main: 5314 tests / 318 suites (`:4`, `:5`; `_updated` `2026-11-04T19:52:54Z`), blob `47470937`. server.js blob `c04a0f4e`, logSafe.js blob `dc0b0536`.
- Jira: RD-798 To Do, Medium, 2 comments, 0 links; `( key = RD-798 )` 1; `RD-99999999` 404; `( text ~ "zzqxnonexist" )` 0.
- Model: `model-routing.md:92` C2, `:93` C3, `:108` G1, `:109` G2 printed; `models_latest.json:23` `claude-sonnet-5-5`.
- Ports: block 9930-9939 chosen. `lsof -nP -iTCP:9930-9939 -sTCP:LISTEN` 0 lines (control 7000: 3); word-boundary scan of the 20 non-`.pre-` SEAT kits of 5 and 6 Nov: `993[0-9]` 0 files, control `991[0-9]` 7 files. Also `990[0-9]` hit 2 files (B1293, B1309) and `989[0-9]` hit B1294 only, so those blocks were passed over. Panes: `wednesday`, `fleet-monitor`. `N101`, `B1317`, `rd798` 0 files each (control `N100` 5 files).
- `refs/heads/b1317*` and `rd798*` on origin: none (`matching-refs` `b13` empty; control `b129` prints the b1294 branch).

## D-decisions
- D1: one commit by default (a cells-only commit is red by design, so no two-commit split unless Tuesday asks).
- D2: all five alerts in one seat, one branch (the ticket says one change); the three SQL log lines `:6184`, `:6242`, `:6301` are not in the alerts and are recorded, not edited.
- D3: no edit to `logSafe.js` (every caller shares it); the seat measures reachability per sink and STOPs on a sink no request reaches rather than inventing a cell.
- D4: red proof by swapping the product file back by blob in a probe tree, plus five single-sink plants, so a green-at-base cell cannot pass.
- D5: a route-body byte-equality cell (log only, no response change).
- D6: the counts arithmetic is 5314 plus the new file's tests over 319, asserted before the one `--update-counts`.

## Q-questions for Tuesday (each with a default)
- Q-1: `logSafe` default `max` is 500 and a KQL query is longer, so the default wrap would cut the logged query; the wrap also joins its lines. Pass an explicit named max (measured above the longest query the cells produce) so the log keeps the whole query. Default: yes, one named constant (that is the only allowed `server.js` line beyond the five wraps). Alternative: accept truncation.
- Q-2: if the seat proves a sink unreachable by any request (the 182/183 branch needs a model answer with no usable suggestion and an input that reaches the partial or overlap branch), may it wrap that sink without a red cell? Default: no, it STOPs and Tuesday decides.
- Q-3: gate: a separate G1 Opus seat after READY, as the sweep says (the surface is log output only, so Tuesday may tier it G2). Default: G1 Opus.
- Q-4: round count: no earlier verdict lines read (none exist for this class in the drafter's reads); the kit states no "n of 2". Default: Tuesday adds it at the stamp.
- Q-5: port block 9930-9939 (none typed; the harness reserves its own). Default: accept.

## UNMEASURED
- Whether a CR/LF value reaches each of the five sinks in practice, what the stand-in model host answers, and what the logged text looks like: the seat measures (MEASURE FIRST 1 and 2); the drafter did not run the server (read-only).
- Hosted CodeQL on the branch (and that the empty-replacement `logSafe` clears these five; `logSafe.js` says it is measured by a PR run, and sibling sinks in the same function already read `fixed`).
- Open branches touching `server.js` near these lines (the seat's Step 2 checks; the sweep's census is relayed).
- No decision card was read; no `decision_queue.sh` used.

## Outside-the-fences disclosure
Wrote only the three files (kit, slots, this report) plus scratch under the session scratchpad (a repo tarball of main extracted to `scratchpad/src`, `server.js`, `logSafe.js`, a Jira read script, `kits.txt`). Reads: DRAFTER_RULES, the B1294 kit pre-stamp and slots, the 1006 sweep, model-routing lines, models_latest, NexusAI `CLAUDE.md` (grep), CLARIFICATIONS lines 2062/2067/2080 and C-68 header, the project's lock script header (grep), `brief_seat.sh:24`, `status_watch.sh:56`. `gh api -X GET` only under the project's GH_CONFIG_DIR (branches, code-scanning, contents raw, tarball, actions workflows/runs/jobs/variables, environments, git matching-refs, pulls, repo). Jira GET only via `b774lib.py` (`issue`, `comments`, `search`). One git read in the project's stale checkout (`cat-file`, `rev-parse`, `ls-remote`, no ref write). No HTTP to any hosted host, no az, ssh or docker. Two early shell mistakes (a for-loop that did not split under zsh, a `cd` that the hook refused) were re-run correctly; no state changed.
