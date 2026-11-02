STARTABLE: YES, only after the product owner rules card `datasec-drive-27gib-remove-old-trees-1102` option a or b and Tuesday fills the `RULING` slot. Not launched, not stamped. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1129_SEAT-R136_hpsmpoc-remove-old-lane-trees.md`, 14267 bytes (`wc -c`). B1129 was free (`ls` of briefs showed B1126 to B1128 only).

## BLUF
- The kit removes the 1425 HPSM-POC objects of the report's eligible list (718.0 + 10.8 + 1.0 + 0.3 = 730.1 GiB by du), one at a time, oldest first, each only if the 9-clause property holds at the moment of removal; failures go to a HELD list and stay.
- Expect the HELD list to be big. Two findings: (1) trees belong to MANY repos: 684 to `2_Project_Files/.git`, about 540 to per-lane clones, 23 to a dangling `/Users/kamilkreiser/1FILES TO SYNC/...` path (HELD), 77 trees without `.git`; so `git worktree remove` must run against each tree's own repo (`rev-parse --git-common-dir`), not the root. (2) the clause "no Briefs file names a path inside it" held by a crude probe about 500 of 1425.
- Hook: `git worktree remove` passes `norm.py`; `rm -r -- <path>` is refused wherever the hook is wired. For an HPSM-POC seat the wiring path `$CLAUDE_PROJECT_DIR/2_Project_Files/fleet/hooks/` does not exist and its `settings.local.json` has 0 hook lines, so probably not gated; the kit calls that a prediction and says: on refusal, record, stop that class, route nowhere.

## Facts re-measured (instrument; `date` Mon 2 Nov 2026 14:41 to 14:45 AEDT)
- Per-class counts of HPSM-POC rows in report lines 151 to 2768: `awk` sum 1323 / 18 / 33 / 51 = 1425; control: equals the report's table (1323, 18, 33, 51) and its "HPSM-POC: 1425 trees" line.
- `[ -f "$p/.git" ]` over the 1323 lane rows: 1246 file, 77 none, 0 dir. `gitdir:` targets: 684 root repo, 23 under `/Users/kamilkreiser/...` (`ls -d` of that path: absent), rest lane clones or `*.git`.
- `rev-list HEAD --not --remotes` over 8 sampled trees: 0,0,0,0,0,1,0,0 (the 1 = `wt-b747-merge`); origin url github `datasecau/HPSM-POC` for 7, `HPSM-POC-analysis` for 1.
- Records re-derivation: the `.tools/<seg>(/<seg>)?` tokens of history.md, BACKLOG.md, CLAUDE.md, JIRA.md: 26; the five HPSM-POC paths of the report's 'Named' section are each found once (control fires); exact hits of the 1425 list in those 26: 0 (the list is already post-exclusion).
- Briefs extraction: 7009 tokens, 24 s; 1047 of 1425 equal a token, about 502 have a token beginning with their path plus `/`.
- `df -k` avail 28,637,724 KiB (14:44); load1 17.21 then 14.58 (`uptime`, `sysctl vm.loadavg`); `lsof -nP -F n` 0.37 s, 1241 rows under `.tools/`; `ps` 26 lines; no `heavy-slot-*`.
- Hook pointers printed by `grep -n`: `norm.py:11` scratch prefix, `:41` rm/unlink, `:52` git rm, `:56` find -delete; wiring `settings.template.json:43`. `model-routing.md:98` (C8), `models_latest.json:23` (sonnet id), `brief_seat.sh:24`.
- Ports: none assigned, none used. Kit stamp-slot lines: 7 four-underscore lines (`grep -c`).

## D-decisions (mine)
- D1: the property is clauses 1 to 9; "named in records" = the four record sources exactly as the report did; "names a path inside it" = literal prefix test over Briefs tokens (strict, large HELD).
- D2: owning-repo removal via `rev-parse --git-common-dir`; dangling pointer = plain copy = HELD.
- D3: `_quarantine*` paths HELD (9 in the HPSM list; the report asked whether parking was deliberate).
- D4: the shared `.tools/.git-lock` not taken (a worktree removal is not a ref write, per DRAFTER_RULES); seat-local `.tools/b1129/removal.lock` is.
- D5: stop figure = avail rise over the Step-0 avail (60 s re-read), not a du sum.
- D6: live-kit paths = kits of live pane ids (not all 130 kits, which name thousands of paths); generic globs ignored.
- D7: launch via `cockpit.sh add`, not `launch_when_cool.sh` (load is 14 to 17; a cool-gated launch would not start).

## Q-questions for Tuesday (default each)
- Q1: Your load line ("pause below load1 12 only if a heavy gate needs it") I read as: pause up to 10 min per batch when load1 >= 12 AND a heavy slot exists or a gate pane is live. Default: that reading.
- Q2: Clause 5 strict or "figure lives" judged? Default: strict (HELD), widen later by a slot.
- Q3: `PLAIN-COPIES` HOLD or REMOVE? Default HOLD (77 trees without `.git` plus 23 dangling, up to 100 objects).
- Q4: Rows not in the 3-day window are re-tested at removal. Default: yes, stated.
- Q5: Hook gate absent for HPSM-POC; do you want the seat run from a TUESDAY-launched pane instead? Default: no, run as launched, report any refusal.
- Q6: Seat hard stop 10 hours (ALL). Default 10 h; card b (200 GiB) should finish far earlier.

## UNMEASURED
- Seconds per object (no removal timed; a 1.2 GiB tree with node_modules under load 14 to 17 is unknown), so the 15-minute first batch is a target, not a measure.
- Freed space versus du (APFS clone sharing; 99% full makes purge lag possible).
- Dirty / unpushed state of the 1425 (only 8 sampled, `status --porcelain` not run on any); remote-tracking refs may be stale (no fetch is allowed), so "on origin" is as of the last fetch.
- Env-variable users of `dotnet-home` (a process with `DOTNET_CLI_HOME` but no cwd or open file there).
- The ~100 objects that `rm` needs if the hook is wired; the lane-clone `repo/` dirs themselves (not on the list).
- Whether the report's list has changed since 14:40 (size is the only guard).

## Twin kit for MPS and Composer: what would change
- Project dir, pane (`Datasec/MPS-<ID>`, `Datasec/Security-Composer-<ID>`), seat id, STATUS and `.tools/b<NNN>` names, `gh` config irrelevant (no gh used).
- List rows and counts: MPS 906 objects, 108.6 GiB (703 lane, 80 dotnet, 50 node_modules, 73 build); Composer 265, 3.9 GiB (257 lane, 6 build, 1 node_modules, 1 ms-playwright, and the playwright class needs a ruling). ms-playwright is in the ruling's class list but excluded here.
- Composer: records trees (`-rec`, 29, 87.8 GiB) are a hard exclusion with Briefs copies; add `.tools/composer-heavy.lock` check (absent) and `.tools/b1041/scripts`; the project root has ~250 `_wt_*` / `_quarantine_*` outside the report (UNMEASURED).
- MPS: different live-kit tokens (G283/G287 kits), different fixed helper names; drop the HPSM-POC phase line.
- Worktree owner shapes must be re-measured (the 684/540/23 split is HPSM-specific).

## Outside-the-fences disclosure
Read-only only. Read: DRAFTER_RULES, both learnings, the report by range, B1123 and B1127 pre-stamp kits, hook scripts, HPSM-POC records and Briefs (grep), `.git` files and `rev-list` in 8 trees, `lsof`/`ps`/`tmux`/`df`/`uptime`. Scratch files only under the session scratchpad (`hp.txt`, `q.txt`, `named*.txt`). Two of my first Bash calls were refused by hooks (a `cd`, an `=====` word); re-issued without them. No decision_queue, Jira, Azure, message, or removal. I did not read the card.
