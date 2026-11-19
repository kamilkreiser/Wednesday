This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. For lane A, P1P-GATE. It replaces the heavy-run COUNTING method for you; everything else stands.

# P1P-GATE — ADDENDUM 3: your slot counter starved you; run the rest now

**What Friday measured (about 04:31):** your driver (pid 63808, running 6 h 15 min) finished `check.sh` at 23:47 with `check exit=0`, then has written "wait red (count 6..10)" every minute since, because the count it uses (`pgrep -fl 'scripts/check.sh|red-controls-|…' | grep -v zsh | grep -vc 'bash -c'`) counts PROCESSES, not jobs: wrapper shells and the other seats' own waiting loops match the same text. The rule's text came from Friday's brief: the method was Friday's defect, not yours. Real heavy jobs at 04:31: two (`ps -ax -o command=` lines starting `bash scripts/…`), load 4.75 on 12 cores, 88 percent memory free.

**Do now:**
1. Stop your driver chain (your own pid 63808 and its children only; never another seat's process). Keep its logs.
2. Run the remaining steps of addendum 1 item 9 yourself, one at a time: `scripts/red-controls-daemon.sh` (exit code captured in the same command), `scripts/test-p1p.sh 3`, `scripts/test-p1p.sh --red`, `scripts/test-daemon.sh 1`. Your `check.sh` result at 23:47 stands only if your head has not changed since it ran; if it has, run `check.sh` again first.
3. **Count real jobs only**, before each run: `ps -ax -o command= | grep -E '^(/bin/)?bash scripts/(check\.sh|red-controls-[a-z]+\.sh|test-daemon\.sh|test-p1p\.sh)' | wc -l`. Start when it reads 2 or fewer (your addendum 2 third slot); otherwise wait and re-count every few minutes.
4. Then push, write the `READY FOR MERGE CHECK P1P-GATE r2` line as addendum 1 says. Note in STATUS which runs used which counting method.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
