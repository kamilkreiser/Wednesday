STARTABLE: YES

# B1223 drafter report (SEAT-N96, NexusAI RD-922 round 2, test only)

## BLUF
Kit is 70 lines (target 60; the round-1 shape, REFUSE and STANDING LINES kept, so not cut further). One more commit on `b1215/nexusai-rd922-reset-wipes-risk-rules` @ `98b00901`, adds a second `test(` R2 in the same file: a BEFORE DELETE trigger on risk_conditions with RAISE(ABORT) makes `:36` fail; asserts exit 1, `Failed to clear database`, the planted text, no success line, risk_conditions still 2. Red-first is the mutant: the product is right, so R2 cannot be red at the head; MH (await removed) is the red, run 3 times. Also fixes the 2 em dashes. No product change.

## Facts re-measured (17:30 AEDT, at drafting)
- `gh api -X GET git/ref/heads/main` = 0835221808f9007e5b17ec492765af067515edb9; branch ref = 98b009012742684c62f4b498456662a122d3cd96; open PRs 0; `matching-refs/heads/b1223` 0 (control `heads/b1215` 1).
- Raw files at 98b00901 by `gh api -X GET contents?ref=` into the scratchpad, `git hash-object`: clear_db.js 18a96745 (55 lines), test 624022d1 (176 lines). Pointers printed by `cat -n`: `:36` statement, `:35` comment, `:40` VACUUM, `:46`-`:49` catch (`:47` the console.error line, `:48` process.exit(1)); test `:2` and `:140` em dashes, helpers `:55 :66 :72 :78 :98 :111 :129`, `describe :139`, R1 `:140`-`:175`. Counts blob 98f4f9d6 and pair 5300/316 are RELAYED from the gate's STATUS (not re-read: no clone allowed).
- Stamp slot count 9 (grep `_''_''_''_`); worktrees/session-tools/.tools b1223 absent (ls rc 2 each); ports 8500-8599 listener scan rc 1 (empty); kit scan for N96/b1223 0 files, control NexusAI-N95 3 files; live panes: tuesday, fleet-monitor, HPSM-POC-G321, -H111, MPS-G318. Model row `model-routing.md:94` C4, id `models_latest.json:17` claude-opus-5-5.
- Gate evidence read: STATUS whole; residue.md and card-input.txt whole. probe.js is at `session-tools/b1219/bin/probe.js` (not in the evidence folder as the task said); its trigger line (`:90`): `CREATE TRIGGER b1219_fail BEFORE DELETE ON risk_conditions BEGIN SELECT RAISE(ABORT, ...); END`. MH.js is not in `session-tools/b1219/mutants/` (MA-MG only), so the kit has the builder make MH itself from the described one-edit.

## D-decisions
- D1 same file, second test, not a new file: counts 5300/316 -> 5301/316 (branch), 5301/316 vs main = +2/+1, as asked. Counts diff vs the head is two lines (`_updated`, `tests`), vs main three.
- D2 `seed(dbFile, opts)` optional option adds the trigger before the final count; R1's call is untouched.
- D3 R2 also asserts risk_conditions 2 after and HOME empty; no cell for the five older statements (the gate said it would pin them; out of scope, recorded as D8).
- D4 added-line bound 40 on the test file (Q-1).
- D5 MA/MB/ME re-run on R1 only; R2 under MA/MB recorded, not predicted (the trigger never fires).

## Q-questions for Tuesday
- Q-1 bound of 40 added test lines OK? Default: yes.
- Q-2 "P0 0 red" is not defined in the files I was allowed to read; I read it as "no red anywhere except the intended mutants". Default: that reading.
- Q-3 launch line is the drafter-rules `cockpit.sh add` form; B1215 stamped a `launch_when_cool.sh` line instead. Default: Tuesday replaces it at the stamp.
- Q-4 a rejected fast-forward push is a STOP in the kit (never force). Default: keep.

## UNMEASURED
Counts blob/pair at the head (relayed); MH red on R2 (predicted from the gate's probe: uncaught rejection, no catch line, 3 of 3 with the planted trigger); the CodeQL result on the new lines; hosted Build.

## Outside-the-fences disclosure
Read: DRAFTER_RULES, the B1215 kit, the B1219 STATUS (it lives in the NexusAI project Briefs folder), B1219 evidence files, `session-tools/b1219/bin/probe.js` by grep only, model-routing, models_latest, `nexusai-lock.sh` header (`sed -n 1,40p`), `tmux list-panes`, `lsof` scan. No git write, no fetch, no clone, no mail/Jira call, no HTTP except `gh api -X GET` on the project repo. Only the two output files written; scratch copies of the raw files sit in the session scratchpad.
