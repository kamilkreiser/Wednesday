STARTABLE: YES

# B712 drafter report (Composer, lane C-GUIDED, PCOMP-24 = gate finding B146-N1)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B712_SEAT-J19_composer-pcomp24-guided-target-lock.md` (130 lines; 8 stamp slots + last line = 9 lines hold four underscores, measured by `/usr/bin/grep -c -E '_''_''_''_'`, control: the same pattern in a scratch file with four underscores reads 1).
Drafted 2026-10-26 07:52 to 08:0x AEDT (clock `date`). Read-only; nothing run in the project.

## BLUF
- Startable now: main `0b52848c` (ls-remote), no `b712*` ref, ports 9790-9799 free (lsof rc 1), no open PR touches `engagements.ts` or a `b712` test (#92, #94, #91, #86, #85: 0 each).
- Fix chosen: REFUSE (409 `POLICY_TARGET_ALREADY_CHOSEN`, the existing sentence, reused from `setPolicyTarget`; no new word, code, status or contract edit). Two files only: `apps/api/src/routes/engagements.ts` and one new `apps/api/test/b712-setup-target-locked.db.test.ts`.
- The defect is exactly as ticketed: `completeExpertSetup` (`engagements.ts:826-917`) writes the target at `:892-894` without ever reading `pc.policy.policy_target_key`; `setPolicyTarget` reads and refuses it at `:944-953`.
- Regression = plant R2 (key + E8 selection + revision bump), via the harness's `h.admin`; the kit demands a RED-at-base proof, three consecutive greens, and four mutants M1-M4 each red by name.
- One documentation gap left alone on purpose: the contract's notes for `completeExpertSetup` (`document.ts:1675` via `B103_SETUP :136`) do not mention the new refusal (the 409 status is already declared at `:1668`).

## Facts re-measured (instrument; control)
- Main and branches: `git ls-remote origin refs/heads/main 'refs/heads/b712*' 'refs/heads/b7*'` printed `0b52848cab57...` for main and b72/b74/b75/b79 branches, nothing for `b712` (control: the b72/b74 rows prove the glob fires).
- Open PRs (`gh api -X GET pulls?state=open`): #94 `99585f7d`, #92 `f2245db0`, #91 `301991a8`, #86 `fd24426d`, #85 `85105729` (draft). `pulls/<n>/files --paginate --jq '.[].filename' | grep -c -x -E 'apps/api/src/routes/engagements.ts|apps/api/test/b712.*'` printed 0 for all five (control: weak; the kit makes the seat plant a line and re-run; I did not plant one).
- Panes (`tmux list-panes -a -F '#{@cockpit_name}'`): `tuesday`, `Datasec/NexusAI-M13`, `Datasec/Security-Composer-G133`, `fleet-monitor`.
- Ports: `lsof -nP -iTCP:9790-9799 -sTCP:LISTEN` rc 1, nothing. Word-scan `grep -l -w -E '979[0-9]'` over the 2026-10-25/26 `*SEAT*` kits (non-`.pre-`) hit 7 files: B629, B649, B657, B666, B682, B686, B687. All finished seats or other projects (B629 states the block as its own; B686 says "reserved and NOT USED"). Live Composer pane G133 (B707) is not in the list. The scan's glob also covered today's B705/B706/B707 kits: no hit.
- Source: `engagements.ts` at `0b52848c` is 1430 lines / 66880 bytes (`wc`; sweep says 66,880). `completeExpertSetup` 826-917; stale pin + lockDraft 857-863; approver INSERT loop 864; target write 892-894; `setPolicyTarget` 927; its select 944-947; refusal 948-953; constant :284. The refusal sentence occurs once in `engagements.ts` (`grep -c -F` 1; control `zzz-no-such-string-7f3a` 0). `POLICY_TARGET_ALREADY_CHOSEN` occurs 19 lines in 11 files at main (`git grep -c`).
- Contract (read only): `completeExpertSetup` `problems: [...COMMON, 409, 412, 428, 422]` (`document.ts:1668-1675`), so no status change; notes silent on the new refusal.
- Neighbour test: `b144-set-target-pending.db.test.ts` 197 lines, 8806 bytes, 5 tests (the header comment names a person and a card slug, so the kit tells the seat not to copy it). Its harness, helpers (`guidedStart`, `completeSetup`, `written`, `e8Level`, `newerApp`) are reusable. `git ls-tree` of main has no `apps/api/test/b712*` path.
- Jira PCOMP-24 read whole with the HPSM-POC `jira.py` (GET only): Backlog, labels composer-seed-1023 / plan-comp-316, 0 comments; text matches the sweep and the gate row `B146_STATUS.md:75`.
- Model rows: `model-routing.md:92` C2 (Sonnet "1st"), `:108` G1 (Tier 1). Model id from `models_latest.json` `levels.sonnet.model_id` = `claude-sonnet-5-5`.
- Landing rule quoted from CLARIFICATIONS C-101 (heading line 1797, option text line 1799: squash-merge pinned to head, after re-reading CodeQL and the checks), plus lines 582, 855, 1802, 1823 (each names a squash). Fix rounds: ONE new commit on the same branch, never rebase or force-push; cap two NO-GO rounds (`B146_STATUS.md:16`).
- CI: no `.github/workflows` paths at main (tree count 0; control: `scripts/ci.sh`, `scripts/test-db.sh` listed). `scripts/ci.sh` lines 116-118 run the node step and the db step; the pass predicate (exit 0) is written into the kit.
- Load at drafting: 7.91 7.33 6.57 (kit tells the seat to wait for load1 < 7).

## D-decisions (mine; Tuesday may strike at the stamp)
- D1: REFUSE, not keep. Reasons in the kit: same rule and same sentence as `setPolicyTarget`; the earlier B144 fix refused rather than ignored for the same "silently changes" reason; "keep" would answer 200 while ignoring a field the contract says is recorded; both need no new sentence.
- D2: the SAME key as the planted one is refused too ("chosen once"), matching `setPolicyTarget`.
- D3: a set-up WITHOUT a key on a planted start stays 200 and keeps the target (row 4, and mutant M3 pins it).
- D4: check position after the stale-pin/draft lock and before the first write, so the existing error order (422 unknown key, 409 stale pin, 412/428) is unchanged and the refusal writes nothing.
- D5: suggested lifting the `setPolicyTarget` check into one helper so the sentence stays ONE literal (kit check 9(c)); inline is allowed if the seat states why.
- D6: plant via `h.admin` in one transaction (policy key, E8 selection, version revision bump), re-reading the engagement ETag after the plant; the seat must report if a trigger or grant blocks it.
- D7: tier 1 gate as commissioned; Sonnet builder, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes.
- D8: the kit path for tools is project-root `.tools/b671/scripts/` (not `2_Project_Files/.tools/`); copied the B688 read-only-source list with b671 only (no regen script needed).

## Q-questions for Tuesday (each with a default)
- Q-1: The contract notes for `completeExpertSetup` do not say the new refusal exists (the 409 status is declared). Adding a sentence is NEW WORDS and the kit forbids it. Default: leave it; the seat reports it as a Note and Tuesday files a words ticket if wanted.
- Q-2: Unit step needs the SOW text bind mount (read-only, `--network none`, at the path the copied `unit.sh` names, as in B688). Default: YES.
- Q-3: Refuse vs keep (D1). Default: refuse. If Tuesday prefers keep, the kit's property block, rows (1)-(3), mutants and the commit text must change; do not flip it at the stamp without editing those.
- Q-4: Hard stop. Default: target READY 2.5 h and hard stop 3.5 h after the seat's own Step-0 date (more than B688 because of the red proof and four mutants).
- Q-5: Ports 9790-9799. Default: accepted (free; finished-seat mentions only).

## UNMEASURED
No build, test, container, plant or mutant ran. Not measured: that `h.admin` can write `pc.framework_selection` and `pc.policy_version` (precedent only for `pc.policy`, `b103-policy-target.db.test.ts:378`); the baseline counts at `0b52848c` (80 files / 1492 tests is relayed from the previous lane at the commit before); that the scripts of `.tools/b671/scripts/` run under a rename (read `dbone.sh` and `common.sh` only, not `heavy.sh`, `dbtest.sh`, `unit.sh`, `names.py`); that no existing test expects a keyed set-up on a policy that holds a target (the gate found no API route to make one); whether the web set-up card handles the new 409 usefully (the web already maps the code for the Details screen only); the intersection control (planted line) was not run by me; that #92 landing around 09:00 changes only a file count.

## Outside-the-fences disclosure
- Wrote only the kit and this report. Scratch files under the session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/336882f6-01f8-4ed9-82d4-bb25116330ef/scratchpad/`): raw copies of `engagements.ts`, `document.ts`, `harness.ts`, `flows.ts`, the b144 test, the tree listing, and a small Jira read driver `jr.py`.
- Read outside the TUESDAY tree: project `1_Project_Definition/CLARIFICATIONS.md`, `Briefs/*B144*/B146*/B688/B671/B695* STATUS` last lines and B146 lines 16/34/75; `.tools/b671/scripts/{dbone,common}.sh`; HPSM-POC `.tools/b236/jira.py` (executed in-process by `python3 -I`, GET only, token not printed).
- `gh` was `-X GET` under the Composer `GH_CONFIG_DIR`; git was read verbs with `--no-optional-locks` (`ls-remote`, `cat-file`, `grep`, `ls-tree`). No fetch, no ref write, no az/ssh/docker, no HTTP to any hosted host, no decision-queue, no `_ledger.md`, no WEDNESDAY/FRIDAY tree read.
- Two hook advisories on case-sensitive phrase greps; the counts that mattered carry a positive control or an exact-string `-F` count.
- One slip in the first draft (guessed line numbers off by 5-8 for `completeExpertSetup`) and the "15 lines" count were corrected from the file before finishing; every line number in the kit was re-read from the fetched file.
