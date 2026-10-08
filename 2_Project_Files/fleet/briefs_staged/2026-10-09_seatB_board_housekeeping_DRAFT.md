LAUNCH BRIEF (Seat J 1st, proposed; Q-LANE-J): a NEW lane, pane `Secuura/Blockchain-J`. **A BOARD seat. It writes to Linear ONLY: three facts-only comments and three state moves to Done (KS-1387, KS-1172, KS-1175).** It does NOT close KS-1173 or KS-577. No code. No git write anywhere except its own scratch clone. No lock, no worktree, no push, no PR. Model: **Opus 5.5**. Ends at a WRAP after every write has been read back by id.

> Filename note: Wednesday staged this as `seatB_board_housekeeping`. "B" here meant "board". **Lane B is the unsuffixed `Secuura/Blockchain` pane (B 66th and earlier), so this brief does not use B as the lane letter.** See Q-LANE-J.

# LAUNCH BRIEF: Seat J 1st, Secuura/Blockchain, lane J (pane `Secuura/Blockchain-J`). From Wednesday.
Drafted by Wednesday's brief-drafting sub-agent 2026-10-09 ~09:40-10:10 AEDT. Every value carries its instrument. Every value marked "drafter" is the drafter's own measurement: you RE-MEASURE it before you rely on it.

## MODEL
- Kam, 2026-10-09 ~09:4x, verbatim: *"for now, use Opus 5.5 for all sub agnets"* (`0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md`, top block. It supersedes the same file's Sonnet half).
- Your launcher pins an older Opus. Wednesday switches your pane with `/model claude-opus-5-5` right after launch and confirms by mail.
- Add the line `MODEL: <as your session reports it>` to every STATUS and WRAP mail.

## USAGE AUTHORITY
- The weekly allowance renewed this morning. `usage_gate.sh --check` read 0% at 09:15 AEDT and 1% at 09:2x (F 6th's and R 21st's SEND AMENDMENTs).
- **The normal 90% stop applies.** No `WED_USAGE_STOP` is set.
- Authority for the writes: Kam's standing week instruction (2026-10-04, renewed to Sun 11 Oct): *"do as much work with the spark and claude agents on the secura projects as you can"*. The close-by-residue precedent is card `secuura-fourteen-merged-own-pr-tickets-never-moved` (= `close-by-residue`, ruled 2026-09-14T08:11:55+10:00): a seat reads each ticket, moves it to Done where nothing remains, and holds the rest with the residue named.

## BLUF
- **Up to three tickets close (KS-1387 only on Q-1360). Each gets ONE facts-only comment, then a state move to Done.** In each case the merged work is on develop and live evidence is already on the ticket:
  - **KS-1387 (clean build).** The fix is KS 1380's PR #1358: merge commit `a5ab2ca9aa114b5a096329fca674329b91784d97`, which carries the fix commit `6cf5c3629cd6268c3891f8aec01acfa7d7cae6cf`. Live evidence: Stuart's comment `6cffd57f` (2026-10-02T04:14Z): "35 of 35 services built, 0 failed" on a rebuilt slot-3 stack at develop `88e8877a2`, his instrument. 🔴 **But a REVERT of #1358 is still OPEN:** PR #1360 (Peter's request, head `d0e99f181a4e`). It is attached to KS-1380 with `status: inReview`, and origin still serves `refs/pull/1360/merge` (`40af17408166`), a ref GitHub keeps only for open PRs (drafter, Linear + `ls-remote`). **KS-1387 is HELD on Q-1360**; it moves only on Wednesday's ruling.
  - **KS-1172 (note + verified verbs).** #1059 squash `0fd21361d2100421a140328ea1e37fb616fdb9c7`. Live evidence: Stuart's comment `ee1e9431` (2026-09-29T09:21Z): Kintsugi's served spec lists `note`, `certified` and `verified`, his instrument.
  - **KS-1175 (identity anchoring).** #1105 squash `cbae988dbe90ebe556459ada2cb437eaf80e2402` and #1116 squash `910687394db563ec032229692724aef26203bfd4`. Live evidence: the ruling-executed comment `c0f62102` (2026-09-22T09:18Z): Kintsugi deployed and the first anchor made.
  - Drafter: every sha above is an ancestor of develop `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0` (`merge-base --is-ancestor` rc 0 each; the reverse control rc 1; a fabricated sha does not resolve). **You re-measure all of this in YOUR clone.**
- **NOT closed, NOT written to:**
  - **KS-1173** has two residues. (1) Stuart's cross-organisation `verified` question (is a verifier org's anchor on the certifier's K document acceptable under the KS 480 ownership model?), unanswered since 09-15. (2) The "ping on DEPLOY, not merge" promise: demo-pk lacked the verbs on 09-29, and today's demo-pk spec is UNMEASURED.
  - **KS-577** is kept open by Kam (09-14) and by Stuart (`357c6ece`). Peter's items 3-5 await Kam's accept/decline line.
- **Every ticket is assigned to our board account** (`kamil.kreiser@secuura.ai`): drafter, Linear by id, 22:40:09Z. None is on Peter or Stuart. Stuart CREATED KS-1387, KS-1172, KS-1173 and KS-1175, but creator is not owner. **A ticket assigned to Peter or Stuart stays theirs.** Re-read the assignee in the same action as each write; if it is not the board account, write nothing to that ticket and mail.
- **All three closes are LEAVES** (0 children each). KS-1175's parent is KS-772 (`Todo`, 17 open children, 0 done; drafter), so closing it cannot complete the parent. The team auto-close fields read `null`. **Archive nothing** (Q-ARCHIVE).
- **Ctx budget:** mail the plan by ~20% ctx. HARD CEILING 65%: WRAP COLD and name what you hold.
- **Never end a turn on a "next up" line with nothing running** (STANDING_LINES `:342`).

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** Where your tool and this brief disagree, **THE TOOL WINS**: run nothing on the disputed point and mail.

**WAKE:** your re-keyed inbox watcher (from G 5th's `inbox_watchg1.sh`, see TOOLS), armed in the background at boot with `timeout: 7200000`.
- It EXITS when it fires. Re-arm it IN THE SAME ACTION that reads each mail, with `SINCE` = the newest mail you have READ (STANDING_LINES `:403`).
- Before your first Linear write and after your last one, LIST the inbox by API.
- Name a watcher pid only from a `ps` FILE read immediately before.
- Stop every watcher before WRAP, and prove 0 live with a positive control.

## THE PARTITION (one checkout, one inbox `secuura-blockchain@agentmail.to`)
Live floor (drafter, `tmux list-panes -a`, 22:4xZ): `%0 wednesday` · `%1 fleet-monitor` · `%2 Secuura/Blockchain-F` = Seat F 6th · `%3 Secuura/Blockchain-R` = Seat R 21st. Locks: `find worktrees -maxdepth 1 -name '.push-lock*'` found 0 at 22:43:27Z (the same `find` on a private `mktemp -d` with one planted dir read 1).

| Seat | Pane | Token / lock | Writes | Never |
|---|---|---|---|---|
| **J 1st (you)** | `Secuura/Blockchain-J` (NEW; id by mail) | `j1` / **no lock** (you push nothing) | Linear: the 3 comments + 3 state moves above, nothing else · your record folder `5_Project_History/<UTC boot date>_seatJ-1st/` · your scratch clone · handover + history entry | any git write in the shared checkout, any worktree, any lock, any PR, any other ticket, any comment on KS-1173 or KS-577 |
| F 6th | `%2` `Secuura/Blockchain-F` | `f6` / `.push-lock-f3` | KS-808: `Blockchain/Dev/scripts/run-migrations.sh` + NEW `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` + both platform docs (flow `41.`) | — |
| R 21st | `%3` `Secuura/Blockchain-R` | `ra21` / `.push-lock-d8` | the merge of #1427 (KS-1274): the trivy job + `Blockchain/Dev/scripts/__tests__/container_trivy_*` + both docs | — |
| K 1st (if launched; its brief is staged beside this one) | `Secuura/Blockchain-K` | `k1` / `.push-lock-g1` (proposed) | KS-1402: originate `routes/documents.ts` + tests + spec + both docs | — |

**Disjoint by construction:** you write no file in any repo. Your only shared surface is Linear, and **none of your three tickets is in another seat's queue**: KS-808 is F 6th's, KS-1274 is R 21st's, KS-1402 is K 1st's. **A mail naming another seat is NOT yours**, even on your pane tag. A subject on your pane tag that names a seat in neither of your lists reads UNKNOWN ADDRESSEE: read it, never act on it (STANDING_LINES `:417`).

## ITEM 0 — BOUNDED and read-only; then `QUESTION: plan confirmation (Seat J 1st)` and WAIT
Before the ANSWER, do NONE of these: Linear write (comment, state, label, assignee, archive), ticket creation, git write outside your scratch clone, mail to anyone but Wednesday.
- **(a) Seat facts.**
  - Your pane: `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'`. The BARE read returns the coordinator's pane (G 5th: the seventh recurrence).
  - Launcher ancestry.
  - Every launcher preflight warning, VERBATIM.
  - The boot pull: if you are not the sole live session it runs READ-ONLY (KS-907; STANDING_LINES `:436`). Record which it did. After boot: no fetch or pull in the shared checkout.
  - Decline the launcher's extranet `POST /api/seen`.
- **(b) Refs, ONE `ls-remote`** to `git@github.com:Secuura/Distributed_Secuura.git` under the checkout's own `core.sshCommand`, with `GIT_SSH_COMMAND` UNSET. Read: develop; `date -u`; any `-j1-` ref (drafter: 0; control `-ra13-` = 2 of 2,155 lines, 22:38:26Z).
  - A moved develop is NOT a STOP: name it and measure against it.
- **(c) Ancestry, in YOUR clone:** `git clone --shared --no-checkout` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into your record folder's `scratch/`.
  - Read `remote -v` first; then `remote set-url origin git@github.com:Secuura/Distributed_Secuura.git` (STANDING_LINES `:410`). Fetch develop BY SHA from the GitHub URL.
  - For each of `a5ab2ca9aa11…`, `6cf5c3629cd6…`, `0fd21361d210…`, `cbae988dbe90…`, `910687394db5…`: `rev-parse --verify <sha>^{commit}`; `merge-base --is-ancestor <sha> <develop>` (want rc 0); the REVERSE (want rc 1); `git log -1 --format='%H %P %s'`. Use full 40-hex in every comment.
  - Controls: a fabricated sha (`deadbeef…`) does not resolve. A revert census, `git log --format=%s a5ab2ca9aa11..<develop> | grep -i -E 'revert|KS-1380|KS 1380'`, must show NO revert of #1358 (drafter: 1 hit, `3f9ff4e1e` "KS-938: MFA disable and revert NULL…", which is the word "revert" in an unrelated subject, i.e. the control fired). The census matters because card `secuura-ks1380-peter-reverting-1358` (= b, 2026-10-01) records Peter opening a revert, #1360, and leaves its direction to him.
  - PR numbers come from each squash subject's `(#n)` and, for #1358, from the merge commit's subject "Merge pull request #1358 from …".
- **(d) Linear, read-only, by id** (`LINEAR_API_KEY` from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, sourced transiently, never printed, never in argv). Read KS-1387, KS-1172, KS-1175, KS-1173, KS-577 and KS-772. For each:
  - state (name + type), assignee email, creator, labels, project, parent, `children`, relations, attachments (`metadata.status`, `mergedAt`), `archivedAt`;
  - `comments(first:50)`, **sorted client-side**: count, newest (author, timestamp), and the id + first 120 characters of each evidence comment cited above.
  - The fabricated-key control: **KS-99999 in its OWN query**, which must answer "Entity not found: Issue".
  - The team's state list, to resolve the `Done` state id by NAME and type `completed`, never by a hard-coded id.
- **(e) THE PER-TICKET PREDICATE**, printed as a table with one row per ticket and one column per clause. A ticket is writable only if ALL clauses hold:
  1. assignee == `kamil.kreiser@secuura.ai`;
  2. `children` count == 0 (a LEAF);
  3. state type is not `completed` / `canceled` / `duplicate`;
  4. `archivedAt` is null;
  5. the merged sha(s) are ancestors of the develop you read (c);
  6. the cited live-evidence comment exists with the cited id and author.
  - **Red-prove it, ONE arm per clause** (STANDING_LINES `:256`): feed the predicate a copy of a real record with exactly ONE field flipped. For example `assignee=stuart.jamieson@secuura.ai`, one planted child, `state.type=completed`, a non-null `archivedAt`, a non-ancestor sha, an absent comment id. Each arm must refuse AT ITS OWN clause, with the asserting line recorded (STANDING_LINES `:444`), plus one positive control that passes.
  - The predicate must also refuse KS-1173 and KS-577 by NAME (an exclusion list in code, not a judgement), with a control showing the list is read.
- **(f) The three comment bodies, composed and NOT posted.** Use the templates below, with your measured values. Show each body's byte count, sha256 and key census:
  - hyphenated keys == `{the ticket's own key}` only;
  - every foreign key de-hyphenated (`KS 1380`, `KS 1173`, `KS 1385`, `KS 1284`, `PS 862`);
  - the BROAD closing regex `(clos(e|es|ed)|fix(es|ed)?|resolv(e|es|ed))\s+KS-\d+` reads 0, with a planted control that fires;
  - 0 `github.com/` links outside `Secuura/`, 0 `owner/repo#N`, 0 @-mentions.
  - Why the bodies are held: a client-visible text is gated before it is posted (STANDING_LINES `:356`). They go IN the plan mail.
- **Your plan confirmation carries:** (a)-(f) one block each; the launcher lines VERBATIM; the three bodies VERBATIM with their sha256s; your restatement of the QUESTIONS; a ctx read request.

## THE THREE BODIES (templates; `<…>` are YOUR measured values. Every sentence names its instrument.)
- **KS-1387:**
  `Moving to Done. The build fix is KS 1380's PR #1358, merge commit <a5ab… 40-hex>, which carries <6cf5… 40-hex>; both are ancestors of develop <develop 12-hex> (git merge-base --is-ancestor, rc 0, read <UTC>). Live evidence is Stuart's 2026-10-02T04:14Z comment on this ticket: 35 of 35 services built, 0 failed, on a rebuilt slot-3 stack at develop 88e8877a2 (his measurement). No revert of #1358 is on develop (git log census, read <UTC>). A revert of #1358, PR #1360, is open (read <UTC>); if it lands, this build needs re-checking.`
  (The last sentence is Q-1360's recommendation. Drop it only if the ANSWER rules otherwise.)
- **KS-1172:**
  `Moving to Done. PR #1059 landed as <0fd2… 40-hex>, an ancestor of develop <12-hex> (git merge-base --is-ancestor, rc 0, read <UTC>). The same PR carried KS 1173's verbs. Live evidence is Stuart's 2026-09-29T09:21Z comment on this ticket: Kintsugi's served spec lists note, certified and verified (his measurement). The demo-pk deploy ping and the cross-organisation verified question stay open on KS 1173.`
- **KS-1175:**
  `Moving to Done. PR #1105 landed as <cbae… 40-hex> and PR #1116 as <9106… 40-hex>, both ancestors of develop <12-hex> (git merge-base --is-ancestor, rc 0, read <UTC>). Live evidence is the 2026-09-22T09:18Z comment on this ticket: Kintsugi deployed and the first anchor made, under Kam's ruling secuura-ks1175-kintsugi-deploy-and-first-anchor. The open follow-on, identity forwarding on the originate-fronted endpoints, is tracked on KS 1385.`
- **Why each close meets the project's Done rule.** SKILL §5f (`:540-552`) says a runtime change does not move to Done on offline green; it needs live evidence. Each body names live evidence already on the ticket. **If your re-read finds that comment missing, or saying something different, that ticket does NOT move: mail it.**

## QUEUE (after the ANSWER, which must carry the literal `WRITE (Seat J 1st)` and the three body sha256s)
For each ticket in the order **KS-1387, KS-1172, KS-1175**, in ONE action per ticket:
1. **BEFORE:** a by-id read; the predicate (e) re-run on THIS read; the body's sha256 == the one the ANSWER named. Any mismatch: STOP for that ticket and mail.
2. **WRITE 1:** `commentCreate` with the body byte-for-byte.
3. **WRITE 2:** `issueUpdate` to the `Done` state id resolved by name in ITEM 0. **Change nothing else:** not assignee, label, project, priority or parent, and no archive.
4. **READ-BACK by id, the same action:**
   - exactly one new comment;
   - its body sha256 == the sent body's;
   - state `Done` (type `completed`) with `completedAt` set;
   - assignee, labels, project, parent and `children` unchanged from BEFORE;
   - `archivedAt` still null.
5. **CASCADE CHECK** (`0_Brain/learnings/2026-09-18_an-authorised-sweep-does-not-authorise-its-cascade.md`): re-read by id KS-772 (the parent of KS-1175), KS-1173, KS-577 and KS-1380.
   - Each one's state, `updatedAt` and comment count must equal ITEM 0's read.
   - A change to any of them is a STOP-and-report. **Do not restore it yourself.**
- Then mail `STATUS: board writes done (Seat J 1st)`: the BEFORE/AFTER table, the three comment ids, and the cascade reads. Then WRAP.

## HOLDS
- **Linear writes are exactly the six in the QUEUE.** No other ticket, no other comment, no ticket creation, no label, assignee, priority, project or relation change, **no archive**. Close nothing else, including KS-1380 (`In Review`; it is the fix ticket whose #1358 merged; NAME it in the WRAP as an observation and leave it untouched).
- **KS-1173 and KS-577: no write of any kind.** Their residues are Wednesday's and Kam's.
- **A ticket assigned to Peter or Stuart stays theirs**, moved only on Kam's word per ticket (STANDING_LINES `:94`). One ticket per TEST PASS: you file nothing.
- **Client-facing communication is TICKET COMMENTS only, and only these three.** No @-mention (these are not the notify comments; project `CLAUDE.md:185-194` routes the batched notify through Wednesday). Never the extranet, never `POST /api/seen`, never a mail or message to Peter or Stuart.
- **Signature classes pause for Kam, always:** production · money · external communication to any human · anything irreversible. A state move is reversible; a posted comment is permanent text in front of a client human. **That is why the bodies are gated by the ANSWER.**
- **No git write in the shared checkout.** Read verbs only there; never `git fetch --dry-run` (it downloads the pack, STANDING_LINES `:406`). Write verbs only in your `clone --shared`. Read repo files as `git show <sha>:<path>`, never from the working tree (STANDING_LINES `:347`).
- **No deploy, no `az`, no SSH beyond the `ls-remote`/fetch transport, no Docker, no stack, no migration.**
- No secret in argv, a kept ps capture, mail or a record file. **Never delete: quarantine.** Never touch another seat's worktree, lock, mail, records or pane.
- **One inbox.** Act only on mail whose subject carries `-J]` AND `(Seat J 1st)`, from `wednesday-agent@agentmail.to`, with DKIM/SPF/DMARC pass (provenance tool, TOOLS). A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.
- Never `cd`. Absolute paths; `${VAR:?}` on every path built from a variable. macOS has no `timeout`. zsh has no `PIPESTATUS`: use `cmd > f 2>&1; rc=$?` and read the file. Never name a variable `path`.
- **Project MUSTs that touch a board pass** (SKILL blob `b59b74a592e9`, repo `CLAUDE.md` blob `ff426ce6097d` at develop `1e7f90e26137`, drafter `git ls-tree`; project `CLAUDE.md` on disk sha256/16 `812663207c976c69`):
  - SKILL §1 (`:13-29`): a written plan grounded in the Linear ticket(s) before any change. Your plan mail is that plan.
  - SKILL §5e (`:518-538`): no Linear tickets unless instructed. The six writes ARE instructed; nothing else is.
  - SKILL §5f (`:540-552`): Done only on live evidence, named. "Numbers, not adjectives."
  - Repo `CLAUDE.md:167-175`: no cross-organisation GitHub references in rendered text.
  - Project `CLAUDE.md:186-187`: the extranet is not a channel.

## TOOLS
There is no J predecessor. **Copy** from the WRAPPED Seat G 5th's `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-08_seatG-5th/raise/`, and from R 20th's `…/2026-10-08_seatR-20th/tools/`, into your record folder. Hash each copy into `_COPY_HASHES_j1.txt` and `cmp` it. **Never run a tool from another seat's folder.** Expected (drafter `shasum -a 256 | cut -c1-16` + `wc -l`, 22:4xZ):

| tool | sha256/16 | lines | for you |
|---|---|---|---|
| G 5th `inbox_matchg1.py` | `1361f23c2cd1f034` | 432 | `inbox_matchj1.py`, RE-KEYED |
| G 5th `inbox_watchg1.sh` | `b69109d9b223882e` | 162 | `inbox_watchj1.sh`, `WATCHJ1_*`, banner |
| R 20th `provenance_ra20.py` | `d215ce0275a6e3f9` | 91 | `provenance_j1.py` (carries no lane token) |

- **The matcher re-key** (G 5th's handover `HANDOVER-seatG5-2026-10-08.md:8-37`, 174 lines, sha256/16 `0eb5baa656c4cf1b`; read items 1-2 THERE, whole). Parsed by the drafter with `ast` (no import):
  - `MINE` = `'g 5th'` at `:102` (DOUBLE quotes in the file);
  - `OTHER_SEATS` at `:212`: 141 entries, 141 distinct, including `f 6th`, `e 12th` and `g 6th`; **ABSENT: `r 21st`, `k 1st`, `j 1st`, `g 5th`**;
  - `MY_PANE` = `'secuura/blockchain-g]'` at `:261`.
- For J:
  - `MY_PANE` -> `secuura/blockchain-j]`.
  - ADD `g 5th`, `r 21st`, `r 22nd`, `f 7th`, `k 1st`, `k 2nd` and FORWARD-ADD `j 2nd`, each with its `seat …` form. Keep `g 6th`.
  - `MINE` = `"j 1st"`, with the double quotes kept.
  - Keep `(Seat G 9th)` in NEITHER list as the untagged-clause arm (STANDING_LINES `:415`).
  - Edit by byte span from the AST; never re-render the list. Verify with `ast.literal_eval`. Exercise `tag()` from source truncated at its `end_lineno`, because importing the module RUNS its poll (F lane ruling 2).
- **Drive it on FULL-LENGTH real subjects from the API, 2x2 where it applies** (STANDING_LINES `:417`). Your own brief reads FOR ME. A real `(Seat F 6th)` subject and a real `(Seat R 21st)` subject read FOREIGN. An unlisted ordinal on your tag, `(Seat J 9th)`, reads UNKNOWN ADDRESSEE. Choose subjects with no foreign ordinal in their prose (G 5th handover item 1).
- **Namespace forms of your token:** `j1`, `-j1-`, `seatj1`, `Seat J 1st`, `j 1st`. `j` is not a hex digit, so `j1` cannot occur inside a sha. Still state counts as raw / bounded (STANDING_LINES `:368`).
- **Your Linear writer is YOUR script, in your record folder:** a quoted heredoc; the key from env, never printed; every call's HTTP status and GraphQL `errors` written to a FILE and read back. Drive it once against the fabricated key KS-99999 (it must refuse, with the error text) before any real write.

## MAIL FORMATS (to `wednesday-agent@agentmail.to`; prefix `[Secuura/Blockchain-J -> Wednesday] `; every subject names `(Seat J 1st)`)
- `QUESTION: plan confirmation (Seat J 1st)` · `QUESTION: ctx read (Seat J 1st)` · `QUESTION: <topic> (Seat J 1st)`. One question per mail; body Context / Question / Meanwhile / Needed-by.
- `STATUS: board writes done (Seat J 1st)`.
- `WRAP (Seat J 1st): …`. Include:
  - BLUF;
  - `MODEL:`;
  - 0 watchers live, proved;
  - EVERY WRITE: the three comment ids + sha256, the three state moves, BEFORE/AFTER;
  - the cascade reads;
  - the KS-1380 observation;
  - UNMEASURED;
  - drive hygiene (your scratch clone: quarantine or remove your own only; GB freed);
  - your handover `5_Project_History/HANDOVER-seatJ1-<date>.md`, opening "FOR J 2nd, THE FIRST THREE THINGS";
  - the history entry at the TOP of `5_Project_History/history.md`, insert-only proved by strip-and-compare;
  - "this seat = 1 Claude launch, clause: board (carrying 0 Spark tasks)".

## QUESTIONS (OPEN; Wednesday rules at the ANSWER; each HOLDS only what it names)
- **Q-LANE-J (HOLDS the launch).** Lanes used so far: A, B, C, D, E, F, G, H, L, M, R. K was briefed but never launched (`2026-10-06_seatK1402_build.md`); its brief is staged beside this one. Instrument: `grep -o -i` over `history.md`, the briefs and the daily notes; 0 hits for `Seat J <n>` or `Blockchain-J` with `Blockchain-R` = 301 as the control.
  - **Recommend:** **J**, token `j1`, pane `Secuura/Blockchain-J`. It is unused, and it is not a hex digit. It avoids S (Platform S), P (Peter / PS-), O and I (they read as digits), Q (the question labels) and W (Wednesday).
  - **Default:** J.
- **Q-ARCHIVE (binds the QUEUE).** The 2026-09-13 20:42 precedent chose Done + archive for our own-PR tickets. These three were created by Stuart and carry his conversation, and archiving hides them from his board view.
  - **Recommend:** Done, NO archive.
  - **Default:** Done only.
- **Q-ORDER (binds the QUEUE).**
  - **Recommend:** comment first, then the state move, so the reason is on the ticket before it changes state.
  - **Default:** as recommended.
- **Q-1360 (HOLDS KS-1387 only).** KS-1387's fix (#1358) is on develop, but Peter's revert of it, PR #1360, is OPEN (Linear attachment on KS-1380 `inReview`; `refs/pull/1360/merge` present at origin; head `d0e99f181a4e` is not an ancestor of develop). If #1360 merges, the KS-1387 build break returns.
  - **Recommend:** close KS-1387. The ticket's own ask (a clean build at develop) is met and Stuart confirmed it live. The comment names the open revert as a fact (the template's last sentence), so the next reader sees the dependency.
  - **Alternative:** hold KS-1387 open until #1360 is closed or merged, and close KS-1172 and KS-1175 only.
  - **Default if the ANSWER is silent:** HOLD KS-1387, write the other two.
- **Q-1380 (HOLDS nothing).** KS-1380 reads `In Review`. Its PR #1358 merged on 09-30 (`a5ab2ca9aa11`, an ancestor of develop, drafter), and its revert PR #1360 is open (Q-1360).
  - **Recommend:** observe only. It is not on Stuart's list and not in this brief. Its close is a separate class-h read (Peter opened a revert, #1360, and card `secuura-ks1380-peter-reverting-1358` = b leaves the direction to him).
  - **Default:** untouched.

## UNMEASURED (by the drafter; you measure or say so)
- Your pane id, your launcher (a `-J` pane has never been launched), whether you are the sole session, your ctx.
- Today's demo-pk spec (the KS-1173 residue; not yours).
- Whether any of the three tickets changes between the drafter's 22:40Z read and your ITEM 0.
- The re-keyed matcher and watcher: unbuilt.
- Whether Linear fires any automation on a state move (team `autoCloseParentIssues` / `autoCloseChildIssues` read `null`; the CASCADE CHECK reads the result).

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE (restate, do not ask)
- `comments(first:50)` sorted client-side for "newest" (F lane ruling 4, 2026-10-08).
- The `$TMUX_PANE` pin for your identity (F lane ruling 5).
- A side-effecting module is verified by `ast.literal_eval` + `tag()` from truncated source, never by import (F lane ruling 2).
- Declining the launcher's `POST /api/seen` is RIGHT (R 20th's ANSWER_plan).
- True duplicates are ours to close (STANDING_LINES `:252`). **That is NOT the authority here:** these are merged-work closes under `close-by-residue`, not duplicates.

PROVENANCE:
- KS-1387 Backlog (backlog) · board account · creator Stuart · label Bug · 0 children · no parent · 0 attachments · 4 comments, newest `6cffd57f` 2026-10-02T04:14:23Z Stuart ("Clean build confirmed … 35 of 35 services built, 0 failed") · inverse relation KS-1380 In Review | Linear GraphQL by id, `comments(first:50)` sorted client-side; control KS-99999 in its own query = "Entity not found: Issue" | read 2026-10-09 (UTC 2026-10-08T22:40:09Z)
- KS-1172 In Review (started) · board account · creator Stuart · 0 children · no parent · attachments #1059 `merged` 2026-09-18T23:19:38Z + platform-s #877 · 4 comments, newest `ee1e9431` 2026-09-29T09:21:11Z Stuart (Kintsugi lists note/certified/verified) | same instrument and control | read 2026-10-09 (UTC 22:40:09Z)
- KS-1173 In Review (started) · board account · creator Stuart · 0 children · #1059 attached · 3 comments, newest `0fc0e8ee` 2026-09-29T09:21:13Z Stuart ("not yet on demo-pk") | same | read 2026-10-09 (UTC 22:40:09Z)
- KS-1175 In Progress (started) · board account · creator Stuart · 0 children · parent KS-772 (Todo) · attachments #1105 `merged` 2026-09-20T15:20:39Z, #1116 `merged` 2026-09-20T22:23:32Z · 4 comments, newest `c0f62102` 2026-09-22T09:18:19Z board account (ruling executed) | same | read 2026-10-09 (UTC 22:40:09Z)
- KS-577 In Review · board account · creator board account · labels Bug, Decision · parent KS-772 · #880 `merged` · 13 comments, newest `670b00cb` 2026-09-29T09:21:22Z Stuart (doc drift) | same | read 2026-10-09 (UTC 22:40:09Z)
- KS-772 Todo · board account · 17 children: 10 unstarted, 4 started, 3 backlog, 0 completed; team KS `autoCloseParentIssues` / `autoCloseChildIssues` = null; the team state list holds `Done` (completed) | Linear GraphQL by id + `team{…}` | read 2026-10-09 (UTC 22:4xZ)
- KS-1380 In Review (started) · board account · creator Peter · 0 children · no parent · attachments #1358 `merged` and #1360 "revert #1358 (15 lockfiles) at Peter's request" `inReview` · 3 comments, newest 2026-09-30T07:44:15Z Peter · updated 2026-10-05T06:54:45Z | Linear GraphQL by id, `comments(first:50)` sorted client-side; control KS-99999 in its own query (22:40Z) = "Entity not found: Issue" | read 2026-10-09 (UTC 2026-10-08T22:50:11Z)
- #1360: `refs/pull/1360/head` `d0e99f181a4e23fcadcb8fdf7c81e4065e6d63f7` ("KS-1380: revert #1358 (merge a5ab2ca9a) at Peter's request", 2026-09-30), `refs/pull/1360/merge` `40af17408166` present; head not an ancestor of develop (rc 1) | the 22:38:26Z `ls-remote`; `git log -1`, `merge-base --is-ancestor` in the drafter's clone | read 2026-10-09 (UTC 22:5xZ)
- develop `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0`, main `54b2a5c26d75`; 2,155 lines; highest `refs/pull` 1434; `-j1-` / `-k1-` 0, `-ra13-` 2 | `env -u GIT_SSH_COMMAND git -c core.sshCommand=<checkout's> ls-remote git@github.com:Secuura/Distributed_Secuura.git`, rc 0 | read 2026-10-09 (UTC 2026-10-08T22:38:26Z)
- Ancestry: `a5ab2ca9a…` (Merge pull request #1358, parents `3a0d98122…` + `6cf5c3629…`), `6cf5c3629…` (KS-1380 fix, 1 parent), `0fd21361d…` (#1059), `cbae988db…` (#1105), `910687394…` (#1116), each `merge-base --is-ancestor` rc 0 against develop `1e7f90e26137`; reverse `1e7f90e26137` vs `6cf5c3629` rc 1; `deadbeefdeadbeef` ABSENT; revert census `a5ab2ca9a..develop` = 1 hit, unrelated (`3f9ff4e1e`, KS-938) | drafter `clone --shared --no-checkout` at `…/scratchpad/brief_hk1402/clone`, origin set to the GitHub URL, develop fetched by sha, `rev-parse`, `merge-base`, `log --merges --ancestry-path` | read 2026-10-09 (UTC 22:4xZ)
- card `secuura-fourteen-merged-own-pr-tickets-never-moved` = close-by-residue, `ruled_ts=2026-09-14T08:11:55+10:00`; card `secuura-ks1380-peter-reverting-1358` = b @ 2026-10-01T08:43 | `decision_queue.sh show` rc 0; R 21st brief's ruled list | read 2026-10-09
- Lane census: `Seat J <n>` 0, `Blockchain-J` 0, `Seat K <n>` 10 (all in the 10-06 K brief), `Blockchain-R` 301 (control); worktrees `s-j*`/`s-k*` 0 | `/usr/bin/grep -c -i -E` over Secuura `history.md` + `0_Brain/daily/*.md` + `fleet/briefs_staged/*.md`; `ls worktrees` | read 2026-10-09
- Floor `%0 wednesday`, `%1 fleet-monitor`, `%2 Secuura/Blockchain-F`, `%3 Secuura/Blockchain-R`; 0 `.push-lock*` (private `mktemp -d` control read 1); 0 `s-f6-*` / `s-ra21-*` worktrees yet | `tmux list-panes -a`, `find -maxdepth 1`, `ls` | read 2026-10-09 (UTC 22:43:27Z)
- G 5th matcher: `MINE` `:102` `'g 5th'`, `OTHER_SEATS` `:212` 141/141 (present `f 6th`, `e 12th`, `g 6th`; absent `r 21st`, `k 1st`, `j 1st`, `g 5th`), `MY_PANE` `:261`; tool hashes in TOOLS; handover 174 lines, 14,496 B, `0eb5baa656c4cf1b` | `python3 -I` `ast.literal_eval` (no import); `shasum -a 256`, `wc -l`, `wc -lc` | read 2026-10-09
- Project MUSTs: SKILL blob `b59b74a592e9` (659 lines, §1 `:13`, §5e `:518`, §5f `:540`), repo `CLAUDE.md` blob `ff426ce6097d` (498 lines, `:167-175`), project `CLAUDE.md` 306 lines `812663207c976c69` (`:185-194`) | `git ls-tree` + `git show` at develop `1e7f90e26137` in the drafter's clone; `shasum` | read 2026-10-09
- Model: Kam's "for now, use Opus 5.5 for all sub agnets", top block of `0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md` | `cat` | read 2026-10-09
- Cascade lesson `2026-09-18_an-authorised-sweep-does-not-authorise-its-cascade.md` sha256/16 `b21eac94ef140cc2` | `sed -n`, `shasum` | read 2026-10-09
- REPORT `0_Brain/reference/2026-10-09_stuart-list/REPORT.md` (141 lines; dispositions B for KS-1387/1172/1175, B + carry-out for KS-1173, keep-open for KS-577) | Read whole | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-09 10:08
