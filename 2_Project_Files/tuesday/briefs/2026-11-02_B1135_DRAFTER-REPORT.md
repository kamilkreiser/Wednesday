STARTABLE: YES, once Tuesday fills the seven four-underscore stamp lines (the ruling the kit needs is the product owner's 16:10:03 AEDT 2026-11-02 'Remove the 845 GiB, project by project', option a, as Tuesday gave it me; I did not read the card). Not launched, not stamped. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1135_SEAT-R139_mps-remove-old-lane-trees.md`, 15011 bytes (`wc -c`). B1135 and B1136 were free (`ls` of briefs, grep for B1135 to B1149: 0). Form, property, steps and fences are B1129's; differences are listed in D-decisions.

## BLUF
- The kit removes the 906 MPS objects of the report's eligible list (lane-worktree 703, dotnet-install 80, node_modules 50, build-output 73; 108.41 GiB by `awk` over the rows), one at a time, oldest first, each only if the 9-clause property holds at the moment of removal; failures go to a HELD list and stay.
- Expect a big HELD list: clause 5 as written (a Briefs token equals or lies under the path) holds 471 of 906 (lane 447). Beyond that: 27 trees whose owner repo has no GitHub origin (24 under five local-path clones, 3 under the root `.git`), 73 lane rows with no usable `.git` (72 none, 1 a `.git` directory), 4 under `_quarantine`, and every dirty or unpushed tree (3 of a sample of 25 were dirty).
- `Datasec/MPS-R137` (records seat, B1133) is live: Step 1d holds its kit's `.tools` paths; `.tools/b1120` and `.tools/b1133` are fixed exclusions. MPS has no hook wiring (`settings.local.json` 0 hook lines), so the kit predicts `rm -r` is not gated and says it is a prediction.

## Facts re-measured (instrument; `date` Mon 2 Nov 2026 16:12 to 16:24 AEDT)
- Report: `ls -l` 400545 bytes, mtime 15:06 (same as B1129's stamp). MPS rows = `grep -F '/Datasec MPS Commercial Calculator/'` over lines 151 to 2768 (first row line 155, last 2759, by `awk` on the extract). Counts by `awk`: lane 703, dotnet 80, node_modules 50, build 73 = 906. Control: the same extract with `/HPSM-POC/` prints 1425 (B1129's figure). GiB sums 98.16 / 5.46 / 4.76 / 0.03 = 108.41 (the report's heading says 108.6 from rounded rows). The path `Datasec%20MPS%20Commercial%20Calculator` (a stray dir beside the project, created 13 Oct, with one `.tools` entry; `ls -la`) does not match and is not on the list.
- Owner shapes: not a sample, ALL 703 lane rows by `[ -f p/.git ]`, `head -1`, `[ -e target ]`: 630 `.git` file (380 -> `2_Project_Files/.git`, 232 -> `.tools/b<NNN>/repo/.git`, 15 -> `.tools/qa-B57|B59|B68/clone/.git`, 3 -> project root `.git`), 72 no `.git`, 1 `.git` directory (`.tools/b538/wt-persist`); 0 dangling (targets all exist; control: `[ -e ]` on a made-up `/Users/kamilkreiser/1FILES TO SYNC/nope` printed DANGLING). 54 distinct owner repos.
- Origins: `git --git-dir=<owner> config --get remote.origin.url` on all 54: 48 `git@github.com:datasecau/MPS-Commercial-Calculator.git` (includes `2_Project_Files`, checked: github), 5 local path `.../2_Project_Files` (`.tools/b319/repo` 4 trees, `b332/repo` 5, `qa-B57/clone` 4, `qa-B59/clone` 6, `qa-B68/clone` 5 = 24), 1 empty (root `.git`, 3 trees).
- Sample, size 25 (every 25th of the 630 with a `.git` file): `git --no-optional-locks -C <tree> status --porcelain` non-empty 3, `rev-list HEAD --not --remotes` 1 in one tree (a local-origin clone) and 0 in 24, HEAD resolved 25. Control: a scratch repo in the session scratchpad with an untracked file printed `?? u.txt`.
- Records tokens: `grep -hoE '\.tools/[A-Za-z0-9._*-]+(/[A-Za-z0-9._*-]+)?'` over history.md, BACKLOG.md, CLAUDE.md, JIRA.md (files exist: 40208, 86358, 8103, 43311 bytes): 50 tokens; exact hits of the 906: 0. Control: the 21 MPS paths of the report's 'Named in project records (excluded)' section (lines 3183 to 3214) are each a token (21 of 21 by `grep -x -F -f`).
- Briefs: 981 files, same extraction 3802 tokens in 11 s (`date` difference). `awk` over the 906: 452 equal a token, 116 have a token beginning with path plus `/`; union by class: lane 447 of 703, dotnet 12 of 80, build 12 of 73, node_modules 0 of 50 = 471 held.
- Fixed rows by `grep -E` on the 906: 6 under `.tools/b562` (the jira helper `b562/jira.py` exists, 726 bytes by `ls -l`; only that file is excluded), 0 under `dotnet`, `b1120`, `b1133`, `wt-b1133-*`, `b1117*`, `b1116`, `b1118`, `b1125`, `b1128`, any `b<NNN>/scripts`; control: a probe path under `.tools/b1120/` matched. 4 rows under `.tools/_quarantine/2026-10-24_B568_scratch-rows/`. 0 rows contain `-rec`, `records` or `Briefs`. `ls -d .tools/b<NNN>/scripts`: 90 dirs. `.tools/b1135` absent (`ls` rc 2). No `.tools/.git-lock`, no `heavy-slot-*`.
- Live state 16:17 to 16:24: `tmux list-panes -a -F '#{@cockpit_name}'` Datasec panes: `Datasec/HPSM-POC-R136`, `Datasec/HPSM-POC-R138`, `Datasec/MPS-R137`. `lsof -nP -F n` 73,480 rows, 0 under `P/.tools/`; `ps -axo pid=,command=` 696 lines, one hit on the path (my own shell command line: the control). `df -k` avail 27,353,112 KiB at 16:18 (27,351,260 at 16:22), 99%; `uptime` load1 3.14 then 3.02.
- Hook: `P/.claude/settings.local.json` 136 bytes, `grep -c -i hook` 0, control `grep -c -i statusLine` 2; `ls -d P/2_Project_Files/fleet` rc 2. Pointers printed by `sed -n`: `model-routing.md:98` (C8, Sonnet), `models_latest.json:23` (`claude-sonnet-5-5`), `brief_seat.sh:24` (`LEVEL=${BRIEF_SEAT_LEVEL:-opus}`), `norm.py:11,41,52,56`, `settings.template.json:43`.
- Stamp slots: `grep -c -E '_''_''_''_'` on the kit prints 7 (STAMP, LAUNCH WINDOW, authority, Heads, SLOTS, RULING, last line); control: B1129 (stamped) prints 0, B1123's `.pre-stamp` prints 6. Kit size 15011 bytes.
- Reading B1134-ADDENDUM-1 (untracked): it withdraws R138's REFUSE on R136 and says R136 holds the paths of live kits; the same rule is in this kit's Step 1d.

## D-decisions (mine)
- D1: the property, REFUSE, SEVERITY tags, heartbeat, STATUS-NOW, hook paragraph, last-line forms and the 3-day clause are B1129's text with MPS names; the HPSM phase line is dropped.
- D2: clause 8 read strictly: origin must equal the GitHub URL, so the 27 local- or no-origin trees are HELD (the 'on GitHub' test cannot be met against a local clone's own refs).
- D3: ms-playwright is not an MPS row (it is a Composer and HPSM-POC row) and is excluded everywhere; the kit says so.
- D4: fixed exclusions for MPS: `.tools/dotnet`, `b1120`, `b1133`, `wt-b1133-*`, `b1117*` (R137 and its kit), `b1116`, `b1118`, `b1125` (helpers named by the closed M77/G283/G287 kits), `b562/jira.py`, `.git-lock`, own `b1135`, `_quarantine*`, every `b<NNN>/scripts`. 0 rows sit under any but b562 and `_quarantine`.
- D5: seat clocks READY 5 h, HARD STOP 6 h after Step 0 (906 objects, 108 GiB; B1129 gave 8 h and 10 h for 1425 and 730 GiB; no object has been timed).
- D6: Step 5 reconciles to 906; STOP-on-avail-falls-across-3-batches kept as in B1129.
- D7: launch by `cockpit.sh add` as B1129 (not the cool-gated waiter).

## Q-questions for Tuesday (default each)
- Q1: the 27 trees under local-path or no-origin repos (their commits could be on GitHub through the parent repo): keep HELD? Default: yes, HELD.
- Q2: clause 5 strict (471 held) or judged? Default: strict.
- Q3: `PLAIN-COPIES` for 73 trees without a usable `.git`? Default HOLD.
- Q4: launch R139 while R136 (HPSM-POC) is working, I/O on one volume? Default: yes, one object at a time each; start after R136's first batch is visible.
- Q5: seat clocks 5 h and 6 h. Default as written.

## UNMEASURED
- Seconds per object (no removal timed); freed space versus du (APFS sharing; 99% full).
- Dirty and unpushed state of the other 605 of the 630 (only 25 sampled); remote-tracking refs are as of each repo's last fetch (no fetch allowed), so 'on GitHub' may be stale.
- Objects needing `rm` (not a registered tree): node_modules 50, dotnet 80, build 73, plus up to 73 plain copies = up to 276, if the hook is wired.
- `.tools/b562/jira.py` use by a live seat (only R137 is live; it copies from `b1120`); env-variable users of dotnet homes; whether R137 adds a worktree under a listed parent during the run (Step 1d re-reads every batch).
- Whether the report's list changed after 15:06 (size is the only guard).

## Outside-the-fences disclosure
Read-only except scratch files in the session scratchpad (row extracts, token sets, `lsof`/`ps` snapshots, one `git init` in a scratch dir `ctl` for the status control; no project repo was written). Read: B1129 kit and report, the drive-room report, B1118/B1120/B1125/B1128/B1133/B1134 kits and addendum for helper names, B1123 pre-stamp, NEXT-PICKUP lines 13 to 15, hook scripts, MPS and Composer records files (grep), `.git` files, `config --get`, `status`, `rev-list` in 25 MPS trees. Two Bash calls were refused by the word-split hook (a bare `====`, a bare `==`) and re-issued. No `cd` typed, no removal, no git write verb in a project repo, no `du` over a `.tools`, no decision_queue, Jira, Azure, message.
