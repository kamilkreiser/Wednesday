STARTABLE: YES - main 37fb1bcb read at source, both tickets read whole, the frozen patch applies cleanly on a scratch copy (node --check rc 0, +20 -9), no existing test pins the old answer by a census that follows variables, slot 13 free, stamp_check rc 0 (229 of 229 claims measured)

# B1726 DRAFTER REPORT - SEAT-N155, NexusAI lane: 500 to 400 for two body shapes (RD-1005, RD-1007)

Drafter: an Agent-tool drafter for Tuesday (s291). Clocks from `date`: first 05:01:56, last 05:21:31 AEDT Thu 19 Nov 2026 (plus the final write of this report, after 05:21). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1726_SEAT-N155_nexusai-lane-500-to-400-body-shapes.md` (221 lines, ASCII, sha256 prefix 14aeba1452783646 at 05:21; 5 four-underscore lines: four slots and the last line). Sidecar beside it (`.measured`, 229 lines). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/d1726/`.

## BLUF
- One lane, one seat, serial, five commits: A5 (RD-1005, server.js +17 -8), A7 (RD-1007, server.js +3 -1), T5 and T7 (two new test files, made inside the chain), K (counts). Model C2 Sonnet (pilot), gate G1 Opus 5.5.
- RD-1005: the three `if (!message) {` lines in the chat region become `if (typeof message !== 'string' || !message) {` (a non-string answers the existing 400 `Message is required`), and the five client sinks of a thrown error's text (the `details` line and four stream error events) call one new 4-line helper `chatErrorText` that returns the constant `Error processing chat message`, EXCEPT an error coded `AI_ENDPOINT_REDIRECT_REFUSED`, whose words `rd523` C1 and E4 pin (found by the census; a blanket constant would have turned them red).
- RD-1007: the one destructuring line of the user add route reuses the RD-985 shared check: `isPlainRequestObject(req.body) ? req.body : {}`; an unparsed body then answers the route's own 400 `Email, name, and password are required`. The check is not widened: 30 other unguarded body reads are LISTED as a follow-up (a program, frame stated).
- The RD-994 guard (block :2801-:2893, mount :2904) is byte-unchanged and its sha256 prefix is a static check at every commit; `rd994`, `rd1000`, `rd523`, `rd969`, `rd691`, `rd765-766` are named readers that must stay green, and two plants (P5 on `rd523`, P8 on `rd969`) prove the pins are wired.
- The B1719 STATUS Corrections 1-12, the B1717 gate F5 (relative jest paths) and the B1724 gate F3 (a constant field) are prevented by name in HOLDS 24-35; the structural fix for Correction 8 is that the readers now run at the PRODUCT commits before any test file exists (chain step 2).

## THE RULING RECORD
No ruling needed. Why: both tickets are Low bugs whose own recommendation is "answer 400 instead of 500" (RD-1007) and "refuse a non-string with a 400 ... and stop sending internal error text" (RD-1005); the kit implements exactly that, with texts the routes already use. Tuesday's grant covers tickets agents can do with no new word. No decision card was read (none expected; `decision_queue.sh` was not run). What WOULD need the product owner's word: changing a ruled number or behaviour (RD-1000's 100000, RD-994's limits or its 400-before-403 order); a status other than 400 or a new user-facing message beyond the routes' existing ones if Tuesday wants new wording that a user of the dashboard would see in normal use; widening the shared body check to the other 30 routes (scope beyond both tickets); or removing the RD-523 named refusal from what a user sees. Note for Tuesday: one user-visible change sits inside RD-1005's recommendation, a failing stream shows `Stream error: Error processing chat message` in the chat bubble (`static/js/index.js:3510`-`:3512`) instead of the thrown text.

## FACTS RE-MEASURED (instrument -> result)
- `gh api -X GET .../branches/main` (05:02:25) -> 37fb1bcbec2e19f2404774633349da76b75120d3, tree f4bf8d71, parents 09811658 (#227 merge) and 6cecb6b3; open PRs -> 0; `compare/34bcd317...37fb1bcb` -> ahead 3, behind 0, HISTORY.md only; counts file -> 6009/380.
- Tarball of 37fb1bcb into scratch; `git hash-object backend/server.js` -> df442bc8ca1153bf8361f422a450a7913b20c6b7 = the contents API sha = #227 head blob (B1724 VERDICT row 1); 22774 lines.
- Jira GET (jget.py shape copied into scratch, project .env in-process): RD-1005 To Do Low Bug, labels records-pass-1118, security, 0 comments; RD-1007 To Do Low Bug, labels records-pass-1119, security, 0 comments; token pattern in output -> 0.
- `grep -n -F` at 37fb1bcb: chat routes :7175 / :7664 / :7864; `if (!message) {` count 3 (7179 7668 7867); the `details` line text count 5 (7170 7656 14573 19657 20759; the chat region holds 1); sinks :7851 :7858 :7977 :7984; users route :3597, destructure :3607 (count 1), 400 :3609-:3611, 500 :3658; `function isPlainRequestObject(` :20646 (count 1); rd691 :159/:167 pins count 1; RD-994 markers :2801/:2893, mount :2904; `alwaysPublicPaths` :2214.
- `azureOpenAIAdapter.js:102/:104/:110` -> code AI_ENDPOINT_REDIRECT_REFUSED and its message; server.js rethrows at :9004 :9391 :9658; rd523 :66 NAMED, C1 :546-:556, E4 :650-:655 assert error events include NAMED.
- census1726.py (two levels) -> chat readers 23, users readers 15; level 1 non-string request messages 0 (5 hits are stand-in reply objects, read); level 2: 50 call sites, 10 `object` hits are rd798 member values holding text (read), 8 unresolved (loop pairs of strings, read; uat-run.js not jest); content types other than JSON to the users route 0; controls fire (rd1000 found, rd523 error-event filter found, kind_of array/object/number/bound-array).
- bodycensus.py -> 31 unguarded single-line destructures of req.body in top-level routes, 3 with `|| {}` (control: users add present).
- apply1726.py on scratch copies -> A5 +17 -8 blob c8070d39, A7 +3 -1 blob 12676613, both +20 -9 blob dc23d449, A5-then-A7 cmp-equal to both; node --check rc 0 x3; non-ASCII bytes 3913 -> 3913. vmcheck.js -> helper extracted (4 lines) and behaves (TypeError -> constant; redirect -> its message; null/undefined/no-message -> constant); region counts oldIf 0, newIf 3, chatErrorText( 5, old sinks 0, the RD-523 branch kept 1.
- Inventory: docs/role-capabilities.json 203 rows; POST /api/chat, both stream routes 400 for viewer/admin/open; POST /api/auth/users admin 400; gate tokens (`role-capability-inventory.js:101`-`:109`) not among the added tokens. serverEnv :382-:391 (limiters true RAISES limits).
- Open alerts: 22 (13 on server.js); #229-#231 at :3609 and #232 at :3620 (js/user-controlled-bypass) on the users route; control state=fixed -> 100.
- Slot program (test-server.js:89-:94 formula) controls -> b1716 old45 10, b1719 old15 14, chk29 14, b1657 old51 16, b1603 old13 12, b1670 old10 1; scan of 221 non-.pre- files of 18-19 Nov -> slots named 0-4, 6-12, 14, 15, 17, 18; looser regex -> 16 in 4 files, 5 and 13 in 0; chosen 13, band 28320-28959, lsof 0 rows at 05:09 (control 12); trees old5 probe13 new31 mut38 v43 chk133 chk137 all 13.
- NexusAI STATUS files 17-19 Nov -> 21, every last line READY; RD-1005/RD-1007 named only by records seats B1718 and B1725; tmux panes -> no Datasec/NexusAI pane; b1726 heads 0 (main 1, b1719 1); gh login datasec count 1; node v26.13.0; `.tools` node count 0; build.yml :29 / :64 / :93; deploy-demo paths-ignore :29-:32; CLARIFICATIONS.md:2067 merge path printed; b1719 clone identity lengths 46 / 12 (not printed).

## D-DECISIONS (the drafter's)
- D-1 One lane, A5 before A7 (each ticket its own product commit; A5-then-A7 measured equal to both at once).
- D-2 Two new test files (one per ticket): different boot shapes (open shape with a model stand-in for chat; enforced shape with seeded admin and viewer for the user add) and separate records.
- D-3 RD-1005 refusal by widening the existing `if (!message)` guard (3 lines changed, no new text), placed before the RD-1000 length check and any other use.
- D-4 RD-1005 disclosure fix by ONE helper and five call sites, the RD-523 exception inside it, prefixes kept, the `details` key kept (development only, as today).
- D-5 RD-1007 in the route, reusing `isPlainRequestObject` (no new helper, no shared middleware, no other route).
- D-6 T files made inside the chain from measured kept lists (B1719 HOLD 28 form); H1/H2 (stream sinks after the stand-in closes) and R4 (no type, no body) are probe candidates, kept only if red at BASE for the property's reason.
- D-7 Readers at A7 run BEFORE red-first and before T exists (prevents B1719 Corrections 8 and 9).
- D-8 Gate G1 (security labels; admin route; disclosure; G2's own clause sends a follow-up on a G1 surface to Opus).

## Q-QUESTIONS FOR TUESDAY (each with a default; none is the product owner's word)
- Q-1 The non-string chat refusal text: DEFAULT reuse `Message is required` (the ticket's first-named option, no new string). Alternative: a new `Message must be text.` (the RD-994 wording form).
- Q-2 The constant client text for a thrown error: DEFAULT reuse `Error processing chat message` (:7636) and keep the prefixes `Stream error: ` / `Analysis error: `. Alternative: drop the prefixes.
- Q-3 The `details` key of the POST /api/chat 500: DEFAULT keep it in development with the constant (production unchanged: absent). Alternative: remove the key everywhere.
- Q-4 RD-1007's answer: DEFAULT the route's own 400 `Email, name, and password are required` (the ticket's proposal). Alternative: a distinct "body not parsed" text.
- Q-5 RD-1007's form: DEFAULT `isPlainRequestObject(req.body) ? req.body : {}` (the RD-985 shared check). Alternative: the `req.body || {}` idiom (3 lines use it). A shared middleware is rejected (widens to every route).
- Q-6 An unparsed body on POST /api/chat and POST /api/chat/stream (same class as RD-1007): DEFAULT left out (still 500 on /api/chat with the constant in `details`; POST stream still reaches the final error handler); on the follow-up list with the other 28.
- Q-7 Gate tier: DEFAULT G1, Opus 5.5.
- Q-8 Keep the RD-523 named refusal verbatim in the client text: DEFAULT yes (rd523 C1/E4 pin it; P5 proves it).
- Q-9 The 30 other unguarded body reads: DEFAULT a follow-up for the records seat to file (one ticket, the census list), not this lane.

## CHAIN INPUTS (each input produced by an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Step 0 | the kit, drafter report, B1719 STATUS/ANSWER-1, gate verdicts | BASE (files exist) |
| Step 1 | clone of 2_Project_Files, deploy key, b1719 clone config (identity) | BASE |
| Step 1b | the clone at BASE; census programs the seat writes | Step 1 |
| A5, A7 | apply script, msg-A5/msg-A7.txt, region counts | Step 1b(i), seat before lock |
| tools, plans | .tools/b1719 (and b1716/b1714/b1680) scripts, msg files | BASE + seat before lock |
| chain 0-1 | old5 at BASE, run list | Step 1b(iii), trees |
| chain 2 | new31 at A7, run list, step-1 per-file counts | A7, step 1 |
| chain 3 | probe13 at BASE + PROBE files from mkT.py --probe | mkT.py (before lock), BASE |
| chain 4 | kept lists from step 3, mkT.py --kept, msg-T5/T7 | step 3, before lock |
| chain 5-6 | new31 re-detached at T7, scanner list | step 4, Step 1b(iii) |
| chain 7 | mut38 at T7, plant specs, plants-predicted.json | step 4, before lock (HOLD 31) |
| chain 9-10 | chk133 / v43 at T7 | step 4 |
| chain 11 | counts file from v43, msg-K.txt | step 10 |
| chain 12 | chk137 at K | step 11 |

## UNMEASURED
- Every HTTP answer of the new cells (no server or jest run by the drafter): PREDICTED from source and RELAYED from the #225 and #227 gates (F3, F5); E1's BASE `details` text; whether H1/H2 reach a stream sink after the stand-in closes; whether R4 (no type, no body) reaches the route at BASE (CSRF and the gate order were not run).
- That `rd523` C1/E4 pass through the helper's exception (PREDICTED: the redirect error keeps its code through the rethrows); P5 measures it.
- The inventory check equality (PREDICTED, step 2 measures).
- The scanner list (the seat re-derives B1719's 45-file program); the readers per-file counts.
- The production setting's answers; CodeQL's reading of alerts #229-#232 after their two-line shift.
- Durations (RELAYED from B1719: verify about 23 minutes).

## REMAINING RISK OF THE OLD-ANSWER CENSUS (said plainly)
The program follows `const`/`let` bindings and a `message`/`prompt` parameter to its local call sites. It does not follow values built in helper modules (`__tests__/helpers/**`, `scripts/role-capability-inventory.js`), computed keys, values passed through more than one function, or browser tests. Its unresolved values were read by hand. Chain step 2 runs all 34 reader files at the product commits before any new file exists; a red there is a STOP with no T to redo.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote three files outside scratch: the kit, this report, and the kit's sidecar `.measured` (the sidecar is required by DRAFTER_RULES "MEASURED LITERALS" 1-2; it was first created by `stamp_check.py --init`, then rewritten by my program; an earlier sidecar from a pre-edit version of the kit was MOVED to scratch (`old1.measured`), not deleted). All three were written as temp files, then `os.replace`. The kit was written by Write into scratch (`kit.tmp`), then placed by `os.replace`.
- Downloaded the 80 MB tarball of 37fb1bcb (gh api -X GET) into scratch and extracted it there; copied jget.py's shape into scratch and edited my own copy's comment with `sed -i ''` (my scratch file only).
- Read-only reads outside Tuesday's tree: the NexusAI project's Briefs STATUS files (last lines and the two records seats' RD lines), `.tools/b1719/` listing, `git -C .tools/b1719/clone config --local --get user.email/user.name` (lengths only), `ls` of the lock base, `1_Project_Definition/CLARIFICATIONS.md` line 2067 only, `tmux list-panes`, `lsof`.
- No jest, no server, no `decision_queue.sh`, no Jira write, no push, no PR, no mail, no project file edited. Ran `node` only on scratch copies (`node --check`, a vm check of extracted text).
