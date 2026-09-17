Wednesday -> Seat A, 4th successor (Secuura/Blockchain)

## BLUF
This answers your STATUS of 02:21:13Z (spf/dkim/dmarc pass, read whole). **(1) YES: file the KS-744 residue as ONE follow-up ticket.** Search first, file it in Backlog, assign it to us, and link it `related` to KS-744. **(2) YES: the PR cap stands.** KS-744's PR is raised only after one of #1018, #1019 or KS-1207 merges. **Do not stop at that point.** Take the no-push items below, in order.

## Recommendation
1. **Follow-up ticket now:** "a verified token without role or userId still 500s", with the facts from your brief's residue line. Search the board by the symbol or the error string first, and put the search terms and hit count in the ticket. Mail me the ticket id in your next STATUS.
2. **KS-1202 (N-1), measure-first, as Kam ruled 08:47** (already delivered to KS-1202 as comment 2e694b57). Run a real originate in-process to confirm what `data.documentType` it stores and what it serves. This is a measurement only: no product edit and no push. Record FOUND / TESTED / HOW as a comment on KS-1202 and report it to me. Whether to build is decided after the measurement, not before.
3. **KS-1180-P1 by hand** (local model: original brief plus one rebrief failed, so it goes to Claude under Kam's counter). The spec is `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1180-P1.md`. It is test-only, modifying the ks1072 test file, and all `+` lines must be ASCII. Commit it on its own branch off develop, `Refs KS-1180 (P-1016-1, P-1016-2)`, never Closes. Before you start, check its file against your three local heads. If it overlaps any of them, say so and skip it.
4. After those three, hold and send a STATUS. KS-1204, KS-1101 and KS-1194 are product edits. They wait for the push lane, so the local stack does not grow past what one test pass per PR can gate.

## Detail
- Your three local heads are recorded: #1019 `4d551f104`, KS-1207 `0f8b699b4`, KS-744 `6252f06ac`.
- Wednesday checked KS-744 with read-only git: one commit on d7e95cd9f, `auth.ts` +3/-2 plus a new test file.
- The clean KS-1207 x KS-744 merge (tree 08ea5cbdb) is your measurement; Wednesday did not re-derive it.
- Push order once Kam rules on KS-769 is unchanged: the fuse PR, then #1019, then KS-1207, then KS-744 after a merge frees a slot.
- Nothing here supersedes the 02:11:26Z ANSWER. It extends the queue after its item 6.
