STARTABLE: YES (after Tuesday fills the 8 stamp lines; no blocker found)

# B1247 drafter report (SEAT-G330, tier-2 gate of HPSMPOC-440 branch b1245/hpsmpoc-440-word-joiner-order-pin @ 1db146df). Drafted Tue 3 Nov 2026 23:47 to 23:53 AEDT (`date` at first read 23:47:06, last check 23:52:43).

## BLUF
- Kit: `2026-11-03_B1247_SEAT-G330_hpsmpoc-440-gate-tier2.md` (97 lines by `wc -l`, 8 four-underscore lines = 7 slots + last line, 0 non-ASCII). Shape copied from the B1178 gate kit (G306). Gate G2 on Sonnet, `model-routing.md:109`; drafter row C8 `:98`; G-cap `:111`. Pane `Datasec/HPSM-POC-G330`, launch carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- The diff is smaller than B1178's: 1 commit on main 69338b64, 1 path, +2 -0, product blob `0c53005e` EQUAL at base and head. So the kit drops B1178's emitted-JS / 2000-entry meaning check (one version of the product file only) and replaces it with blob equality plus a one-sentence argument (C1 (f)).
- New plants that the earlier gate did not have, because the question is now "what do the word-joiner rows pin": qJ / qJV / qJS (reversal limited to U+2060, both / VC / ES), qB (limited to U+200B, keeping U+2060 correct), qT (SHOWS_NOTHING stops matching U+2060 only, for the real-date word-joiner row), and the two reversals Tuesday asked for as the gate's own: the one that keeps U+200B but reverses U+2060 (qJ, and qW), and the ones that keep U+2060 correct but reverse another class (qN: U+200E / U+2800 only; qM2: a mixed string holding U+2060). Predicted survivors: qN and qM2 (0 red). They are graded Note/Minor with a behaviour proof, because SCOPE-440 said "one more shape".
- The kit makes the gate measure the ticket's "before" (a word-joiner reversal at base reads 0 red) so the commit's "all 110 tests green" sentence is tested, not trusted.
- Landing rule quoted with source: `CLARIFICATIONS.md:3617` of `datasecau/HPSM-POC-analysis` main `0e098d1f`.

## Facts re-measured (instrument; control)
1. Branch head `1db146df080fa9919f549236d8486a989bac8a14`; main `69338b6476e2f9d0b5eaeb04742ca9181607121d` (`gh -X GET git/ref/heads/...`, 23:47:26). Control: `matching-refs/heads/b1245` length 1, `b1247` length 0.
2. `compare 69338b64...1db146df`: ahead 1, behind 0, total_commits 1, parent `69338b64`, ONE file test.ts +2 -0 blob `077df018` (base blob `706f4877`). Instrument: `gh api compare --jq`; control: raw file blobs by `git hash-object` equal the compare sha (`077df018`, `706f4877`).
3. Product file blob `0c53005e` at both shas by `git hash-object` over raw contents (control: the test file's two blobs differ). `ci.yml` raw at both shas `cmp` equal, 679 lines; `package.json` 52 lines both, `"test"` at `:12`.
4. `diff` of the two raw test files: `220a221`, `222a224` only. Non-ASCII byte count (`LC_ALL=C grep -c '[^ -~]'`) 0 at base and head. Head lines printed by `grep -n -i`: describe `:215`, `CASES` `:218`, added `:221` and `:224`, `];` `:225`, it.each `:227` and `:231` and `:235`, source row `:239`, `readFileSync` `:240`, `saveEntry` `:246`. (Control: the builder kit's own lines for the same text at base were 220/222; the head moved them by +1/+2 as the diff says.)
5. Product `:24`, `:28-:30`, `:44`, `:47`, `:48`, `:49` by `grep -n -i` over the raw head file.
6. Head commit: tree `040e4d15`, verified false, author and committer email HOSTS both `users.noreply.github.com` (host part only printed). Commit message read by the drafter (not by the gate before its hash): it carries plant counts and "114 tests / 110 tests" sentences; the kit says the gate grades them after its hash. check-runs at head 0, at main 19 (control).
7. Open PRs 0 (control: `pulls?state=all&per_page=3` lists 280, 279, 278 closed); PRs for the head 0. `matching-refs/heads/b12` lists 9 refs, `b1245/...` the only one new since the builder's scan.
8. Ticket HPSMPOC-440 by `.tools/b1007/jira.py` once (9 lines, 0 comments): finding, fix shape, Done-when quoted in the kit as three clauses (one more shape; a reversal limited to it turns a row red; no behaviour change), plus the ticket's byte-order-mark sentence turned into a scratch row.
9. Round count: 601 STATUS files, 150 gate lines; remediation filter prints 2 (B1156 other class, B1178 this class, GO WITH FINDINGS); control `B1178` 1, zero control 0. So NO GO 0 before on 'remediation register tests and titles'.
10. Rules/routing: `model-routing.md` rows G2 `:109`, G1 `:108`, G-cap `:111`, C2 `:92`, C8 `:98`; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus; `status_watch.sh:56` case line lists `VERDICT:*` and `STOPPED:*`. All by `grep -n`.
11. Builder STATUS 97 lines; `tail -n 1 | grep -c -F 'READY FOR QA: B1245 ... @ 1db146df...'` = 1 (control 0); `## PRIOR WORK` count 1. I did not read any plant line from that file. The plant counts in the kit's CLAIMS paragraph (PJ 2, PJV 1, PJS 1, PW 2, PA 8, PX 66, PU 55, P0/PC 0, unit 3907 vs 3903) are Tuesday's relay in the commission, marked RELAYED in the kit.
12. Panes (`tmux list-panes -a`, 23:49): `%0 tuesday`, `%182 Datasec/NexusAI-N96`, `%1 fleet-monitor`. No HPSM-POC pane. N96's non-`.pre-` kits: B1223 and B1238 (NexusAI). Ports: `lsof -iTCP:9600-9699 -sTCP:LISTEN | wc -l` 0; none assigned. `.tools/b1247` absent (`ls -d` error); `.tools/b1245` and `.tools/b1178` EXIST (control: the same `ls` listed `b1245`, `b1175`).
13. Load 3.30 4.93 6.27 (`LC_ALL=C uptime` 23:48).
14. `CASES` count guards: `CalledTimes|CASES\.length` only `:311` (cookieWrites, other subject); `CASES` on 3 lines.

## D-decisions (mine, in the kit)
- D-1 No emitted-JS or 2000-entry scratch comparison: the product blob is equal, so those two instruments would compare a file with itself. Blob equality plus C1 (f) instead. Keeps the gate cheaper and shorter.
- D-2 Plant budget 24 (the B1178 kit allowed 20); the extra room is for qJ/qJV/qJS/qB/qT/qN/qM2. qMf, qD, qR, qXm are cut-first.
- D-3 Row labels D/R/W/S with `-e`/`-z`/`-j` suffix, so predictions and results name rows without full titles.
- D-4 The gate tests the TICKET's before-claim at the base tree (qJ at base must read 0 red), so the "all 110 green" sentence and the ticket's "leaves all 11 rows green" are both measured.
- D-5 Unpinned shapes (direction mark, braille blank, mixed strings) are stated as a closed list "at least these" and graded Note (Minor only if a behaviour proof shows the evidence field marked), because the Done-when says "one more" and SCOPE-440 says word joiner only.
- D-6 The kit forbids the gate to touch `.tools/b1245` and `.tools/b1178` (both exist), uses `.tools/b1247`, and copies helper scripts from `.tools/b1175` as text (as the earlier gate copied from older seat trees); this is a decision because the builder's helper copies are in a forbidden tree.
- D-7 Round wording: "NO GO 0 of 2 before; round 1 of 2" with the B1156 class explicitly excluded.

## Q-questions for Tuesday (each with a default)
- Q-1 Should the gate also be allowed to run a ticket-text BEFORE measurement at the base tree (qJ at `wt-b1247-base`)? Default YES (D-4; one more plant run).
- Q-2 May the PR title and squash subject carry `HPSMPOC-440`? Default YES (as HPSMPOC-437 did).
- Q-3 Plant budget 24 instead of 20? Default YES.
- Q-4 Is `.tools/b1175/lock.sh` etc. an acceptable copy source for the gate (the builder's own copies in `.tools/b1245` are forbidden)? Default YES; if you prefer, say so and I would point at `.tools/b1178` instead (also another seat's tree).
- Q-5 Launch window and hard stop: default target READY 90 / HARD STOP 150 minutes after Step 0, launch_when_cool load1 below 7, one waiter; no NexusAI gate was live at drafting, a gate G329 may start later (the kit says its kit text is tested, not its name).

## UNMEASURED
Every test outcome and count at base and head (the 3903 and 3907 are relayed or from the commit text); hosted CI, CodeQL; whether the plants' predicted red counts hold (they are my hypotheses, to be hashed by the gate first); the file's total test count (110/114 are from the commit text); rows' behaviour under real load; `.tools/b1245` contents; the card store (no `decision_queue` read made); whether any branch created after 09:19:02Z names the test file (the kit makes the gate scan; I only listed `b12*` refs); `usage` gauge and launch-time load.

## Outside-the-fences disclosure
- Read the commit message of `1db146df` (it carries plant counts); the kit tells the gate NOT to read it before its hash, so the gate's independence is preserved; mine is not a gate.
- Ran `.tools/b1007/jira.py HPSMPOC-440` once into the session scratchpad (a read helper, the project's own). Wrote Jira text into scratch only.
- Wrote raw copies of five files and a gates list into the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/61369a4c-4d88-4c4f-abe5-b2005e1d5509/scratchpad/`.
- Read the B1178 STATUS plant table and its evidence landing files (`pr-body`, `squash-body`, titles) as templates (the project folder, read only). Read the B1245 STATUS only for `wc -l`, a last-line count and a PRIOR WORK count.
- Ran the first-lines loop over 601 STATUS files (read only), `ls` of the project `.tools` names, `tmux list-panes`, `lsof` (read), `gh api -X GET` only under the project `GH_CONFIG_DIR`. No git in any project repo, no HTTP to hosted hosts, no `cd`, no `decision_queue.sh`, no Artifact/Docs/mail tool. Wrote only the two files.
