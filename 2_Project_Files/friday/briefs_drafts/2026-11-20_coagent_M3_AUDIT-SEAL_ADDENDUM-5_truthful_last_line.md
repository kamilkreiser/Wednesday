This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-SEAL only. It changes nothing in addenda 1-4 except how your LAST LINE is kept while your final runs go. Note under "## ADDENDUM 5" in your STATUS file that you read it.

# M3 AUDIT-SEAL — ADDENDUM 5: your last line must say what is true now

What Friday read (2026-11-20): your `scripts/check.sh` has been running in `worktrees/m3-audit-seal` since about 12:36 (process list and its working directory), while your last line still read "(12:34) … final runs on 7e9e45e queued (heavy count at 2, re-counted every 2 minutes)". Your queue started the run without the line changing.

Why it matters: two other seats now read YOUR last line before they start a heavy run, and they wait while it contains the words "heavy count at" (that is how you get the next free slot ahead of them). A stale line makes them wait on a slot that is free.

The rule, until your merge:
1. Now: rewrite your last line to the truth, for example `IN PROGRESS: (HH:MM) addendum 4 item 7: check.sh RUNNING on <head> since HH:MM; then the runner, then five seeds`.
2. The words `heavy count at` appear in your last line ONLY while you are blocked waiting for a slot, and never while one of your own heavy runs is going.
3. Make the line change in the same step that starts or ends each run: have the script that starts the run write the line (not only your next turn), and again when it ends.
4. Also new since your merge of main: `origin/main` moved twice today by the phase 1 preview (`b7e8da4…`, then `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`): daemon, hook and `preview/` files, nothing in the audit, roster, proto or crypto crates and no root Cargo change beyond the hook crate's member line and lock entry (Friday read the diff: `Cargo.toml` +1 member line, `Cargo.lock` the `coagent-hook` package). So that the final runs are done ONCE, on the head that will merge: stop your running `check.sh` on `7e9e45e` at a clean point now (your own process only; keep its partial log, named as stopped), `git fetch origin`, `git merge --no-edit origin/main` (expected conflict: `BACKLOG.md` only, keep both sides, main's entries first; anything else is `STOP Q<n> (Friday)`), then run addendum 4 item 7 in full (check.sh, the runner with fresh directories, the five seeds) on that merged head, and item 8 after it. If main moves again after that by files outside `crates/coagent-audit`, `crates/coagent-roster`, `crates/coagent-proto`, `crates/coagent-crypto`: merge again and re-run `scripts/check.sh` only. (This sentence SUPERSEDES the last two sentences of addendum 4 item 8: a later change to root `Cargo.toml` or `Cargo.lock` alone no longer repeats the runner and the seeds, because `check.sh` builds and tests the whole workspace against the new lock; a change inside the four crates named still repeats item 7 in full.)

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
