STARTABLE: YES (after your stamp; two stamp decisions needed: Install authority and the order against B703, see Q-1 and Q-2)

# B702 drafter report (NexusAI lane N-LOCK, RD-847), drafted 2026-10-25 23:3x-00:0x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B702_SEAT-M12_nexusai-847-lock-script.md` (113 lines). Seat `Datasec/NexusAI-M12`, ports 9680-9689 (none bound), model C2 Sonnet `claude-sonnet-5-5` (`model-routing.md:92`), gate G2 (`:109`), launch carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes and `WED_USAGE_STOP=100`. Unstamped slot count 9 (control: the B689 pre-stamp kit reads 9 with the same grep); `@[A-Z_]+@` count 0.

## BLUF
- **The script is NOT under version control.** `session-tools/` is a sibling of the repo `2_Project_Files/` (ls-files 685 paths, 0 with `session-tools`; control `scripts/verify-suite.sh` count 1; `git rev-parse` fails in the project root). So there is no branch, commit, push or PR in this lane. The project's own durable route exists in its records (C-63 `:589-593`, ruling `:569`, C-141 addenda 4 and 6): candidate file, arms on a scratch base, atomic `mv`, old kept as `.pre-<tag>`, evidence under `session-tools/<seat>/`. The kit uses exactly that and invents no repo route.
- **The change is one line (79):** default base `/Volumes/KK_T9_External_HDD/.../locks` becomes `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017`, plus comments only. The T9 is not mounted (`ls /Volumes` = Laptop-DEV, Macintosh HD, Recovery). `locks-laptop-1017` is the base every launching kit and the previous seat's handover (`HANDOVER-S100O.md:10`) already use; the stale `locks/` is deliberately NOT chosen (it would split the mutex, which is the ticket's own risk).
- **Hash pin consequence:** every NexusAI kit REFUSE-checks `3c33f5ae...` (verified: B689, B697 line 53). The install changes the live hash, so any kit launched after it STOPs until you restamp. B703 (N-COUNTS, M13) runs jest through this tool: order matters (Q-2).

## Facts re-measured (instrument, control)
| Fact | Reading | Instrument | Control |
|---|---|---|---|
| live script | 386 lines, 18330 B, `-rwxr-xr-x` uid 501 gid 20, inode 153965298, sha256 `3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792` | `shasum`, `stat`, `wc` | equals the value B689 pins |
| line 79 | `BASE="${NEXUSAI_LOCK_BASE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks}"`; `KK_T9` appears once in the file | `grep -c -F`, `grep -n -F` | other tools' hit list shows the grep fires (5 other tools) |
| not in git | 0 of 685 tracked paths contain `session-tools` | `git --no-optional-locks ls-files` | `scripts/verify-suite.sh` count 1 |
| main | `8ae0a87f564b72fc1f9082cd89013740e7162d58` | `ls-remote` | matches your tonight's landing of #116 |
| RD-847 | To Do, labels operations/s99o/tooling, 0 comments, ask quoted in kit | Jira GET via HPSM-POC helper (read whole first) | JQL `project = RD AND ( text ~ "KK_T9" )` returns exactly RD-847; nonsense string returns 0 |
| sweep row | `SWEEP:137` (S, Sonnet, "do it when no jest or docker lock is held"), lane `:194` | sed by line | grep for `RD-847` hits both lines |
| live base | `locks-laptop-1017/`: `queue-jest/` empty, `released/` 695 entries, no `*.lock` dir at 23:50 | `ls -la` | `locks/queue-jest` lists 11 old tickets, so the listing fires |
| T9 | not mounted | `ls /Volumes`, `ls -d /Volumes/KK_T9*` fails | n/a |
| lock processes | none | `ps -axo pid,etime,command` filtered on `nexusai-lock` | UNCONTROLLED by me this time; the kit makes the seat run a planted `nexusai-lock-probe` control (Step 5.1) |
| panes | `tuesday`, `Datasec/MPS-G131`, `Datasec/Security-Composer-G130`, `fleet-monitor`; no NexusAI pane | `tmux list-panes -a -F '#{@cockpit_name}'` | n/a |
| name | next free builder name is M12 (highest M11; M99 scratch control matched) | `NexusAI-M[0-9]+\b` over 149 non-`.pre-` SEAT kits of 24 and 25 Oct | scratch `x NexusAI-M99 y` matched |
| ports 9680-9689 | free; word-boundary scan hits B618, B619, B620, B672, B678 (finished MPS and Composer kits, prose or ranges) | `lsof -nP -iTCP:9680-9689 -sTCP:LISTEN` rc 1; scan | scratch `x 9680 y` matched |
| load | 3.16 3.47 5.09 at 23:50 | `uptime` | n/a |
| model | `claude-sonnet-5-5` | `models_latest.json` `levels.sonnet.model_id` | row text at `model-routing.md:92`, `:109` |
| landing rule | `CLARIFICATIONS.md:2067` merge path (never squash, never rebase), `:2068` no dismissal, C-68 `:665` | sed by line | quoted in kit STANDING LINE 11; this lane has nothing to land |
| other tools still naming the T9 | `nexusai-lock-fifo-arms.sh`, `c57-id-superset.sh`, `marketplace-package-build.sh`, `release-image-2.1.0.sh`, `shots-2.1.0.sh` | `grep -l -F KK_T9` over `session-tools/*.sh,*.py` | the lock script itself is listed |
| arms script stale | `nexusai-lock-fifo-arms.sh:15` `LIVE_DIR` is the T9, `:16` `ROOT` is a dead 17-Sep scratchpad | file read | n/a; kit has the seat copy and adapt two lines |

## Landing rule
Nothing lands via git here. Quoted in the kit for any later change that does: `CLARIFICATIONS.md:2067` "Merge path: open a PR from the gated branch, wait for CodeQL (a background wait that EXITS), then land the SAME commit. Never squash, never rebase ([[C-68]])." The lane's own equivalent: a gate verdict is valid only for the exact sha256 it measured.

## D-decisions (mine; each recorded in the kit)
- D1 Default is `locks-laptop-1017` (the one live mutex), absolute path (a derived-from-script-dir path would give a moved or scratch copy of the tool a different base, which is the ticket's stated risk). Cost recorded: another move of the project means another edit.
- D2 No branch, no PR: the kit ends at READY FOR QA with a sha256 pair, diff and arms logs instead of a pushed branch.
- D3 Install is gated by a Stamp slot ("Install authority": `STAGE ONLY` or `INSTALL WHEN IDLE`), with idle rule checked twice (no process, no live ticket, no lock dir, no other NexusAI pane) and the atomic same-directory `mv`; rollback is a copy of the kept pre-copy through a `.new-847` file and another `mv` (the pre-copy is never consumed).
- D4 No guard, no new behaviour (one line plus at most six comment lines); a "fail loudly when the base's parent is missing" guard is left out (Q-3).
- D5 Arms are shell, on scratch bases only, no jest ticket; the only live-mutex touch is one `b702-probe` ticket with the variable UNSET after the swap (and a second with it set). Arms 8-14 cover every caller shape found: jest/docker kinds, explicit base, `--after`, `--replace`, merge-first, SIGTERM and dead-holder takeover, default-path mechanics (on a sed'd copy, since running the real default would touch the live base), empty-variable fallback, `bash <path>` vs direct exec vs `/bin/bash` 3.2, and old-waiter-alongside-new interop. Mutants M1-M4 with controls. A base directory with a `!` in its name is used once to prove the path form.
- D6 Target READY 2 h, HARD STOP 4 h after Step 0 (light shell work; the only wait is the idle rule, up to 60 minutes).
- D7 Gate after: G2 tier 2 (Sonnet, tooling), see Q-1.
- D8 STATUS filename and PRIOR WORK must list what the change PRESERVES (ticket name shape, FIFO, 30 s grace, `--after`, `--replace`, merge-first and its tag convention, TERM clean path, the explicit override), each tied to an arm number.

## Q-questions for Tuesday (each with a default)
- Q-1 Install authority and gate tier. The tool is a machine-wide mutex for every NexusAI jest run. Default: stamp `INSTALL WHEN IDLE` (it follows C-63's install-then-tier-2-gate order, a kept pre-copy gives a one-`mv` rollback, and the idle rule plus the arms are in the kit) and tier 2 (G2). Choose `STAGE ONLY` if you want the gate to pass before anything live changes; the kit then hands you the exact commands.
- Q-2 Ordering against B703 (NexusAI-M13, N-COUNTS, being drafted in parallel). B703 uses this lock and will pin `3c33f5ae...`. Default: launch M12 first on its own (no NexusAI pane is live now, the lock is idle), wait for READY (installed or staged), then restamp B703's hash line (and any other pending NexusAI kit) with the new live sha256 before launching it. If you want both at once, stamp M12 `STAGE ONLY`.
- Q-3 A guard for a missing volume (fail loudly if the base's parent directory does not exist, instead of `mkdir -p` creating a stray `/Volumes/KK_T9...` on the boot volume). Default: NOT in this ticket (the sweep calls it a one-line default); I flagged it in the kit as a possible later change. I did not test whether that `mkdir -p` would succeed here.
- Q-4 Records: should the project record the new default as a short CLARIFICATIONS line in C-63's style? Default: yes, by the records seat after the gate; the kit forbids this seat to touch records.

## UNMEASURED
No script copy, arm, install, `mkdir` in a lock base or probe was run. In particular: that the FIFO arms pass on the current script once the two stale lines are adapted (kit Step 4.1 is the control); that every caller shape works under the new default on `/bin/bash` 3.2 (arms 8-14); whether any process other than kit-launched seats calls the tool without the variable (the live process list at install is the only complete census; my caller census is text only); whether HPSM-POC calls it (`2026-10-18_B263` mentions it by name); whether `mkdir -p` under a missing `/Volumes/KK_T9_External_HDD` succeeds here; whether other pending kits beyond B689/B697 pin the hash; the T9 coming back and being synced over `session-tools/`.

## Outside-the-fences disclosure
- Jira GET only, through `HPSM-POC/.tools/b653/jira.py`: I ran its `show` path once for RD-847 and loaded it as a module from a scratch script `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/6f80c94e-470c-4377-ae7f-3813322bdb2a/scratchpad/q.py` for three JQL searches, each `project = RD AND ( ... )`. That helper reads the HPSM-POC project's `.env` in-process; nothing printed. The scratch file is the only file I created beside the two outputs.
- `git --no-optional-locks` in the shared NexusAI repo: `ls-files`, `rev-parse --show-toplevel`, `ls-remote origin refs/heads/main`. No `gh` call at all this time. No git in any other tree.
- Read-only reads of the NexusAI project folder: `session-tools/nexusai-lock.sh` (whole), `nexusai-lock-fifo-arms.sh` (header, grep), directory listings of `session-tools/`, `locks/`, `locks-laptop-1017/` and `queue-jest/`, `CLARIFICATIONS.md` by line, `HANDOVER-S100O.md`/`S101O` by grep and one line, `.gitignore` grep (no output), `JIRA.md` key line. `ps -axo`, `tmux list-panes`, `lsof`, `uptime`, `ls /Volumes`, `stat`, `shasum`.
- Read the Tuesday kit tree: the B689 kit and drafter report (template), the sweep lines 150-205, `model-routing.md` by line, `models_latest.json`, `DRAFTER_RULES.md`, the briefs directory listing and greps over non-`.pre-` SEAT kits. No `decision_queue.sh` call, no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree, no other client's project, no HTTP to a hosted host.
- One Bash call was refused by a hook (a bare `===` word) and one drew an advisory about a case-sensitive grep; nothing harmful ran. Wrote only the two output files (plus the scratch query file named above).
