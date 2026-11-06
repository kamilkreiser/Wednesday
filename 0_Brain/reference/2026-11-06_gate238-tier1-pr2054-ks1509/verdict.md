GO WITH NOTES
7bd7697c86ad29f2f5e3fc898e4bcc8935940704

# Gate 238: Secuura / Blockchain, PR 2054 (KS-1509), tier 1, round 1 of 2, narrow

Opus, row G1. Written 2026-11-06 22:46 AEDT. Findings only; nothing fixed, nothing posted, no box, no docker. This GO is about the SHA above; a commit voids it.
Evidence class on every finding: MEASURED AT RUNTIME / PROBED / READ ONLY.
Pins (ls-remote, branch names beside): 22:34:18 PR 2054 head 7bd7697c, develop b7d433fd. 22:42:23 PR 2054 head 7bd7697c, develop 76e8cf5d. 22:43:48 and 22:46:32 the same. **develop moved during this gate** (one commit, KS-1666, 3 files, none shared with this PR). The head did not move.

## BLUF

**Platform S, plainly: yes, this needs a word to Stuart's team. It does not, on what I found, need a ruling from Kam, but whether the word goes before the merge, before the deploy or at the wrap is Wednesday's or Kam's call, not mine or the seat's.** The word has one question in it, because the only Platform S I can read is about five months old (F2).

**Gate 235's F1 overstated the effect, and the stop line's worry does not hold on the page it named.** It read the Block row at `_VerifyResult.cshtml:92` and missed the guard above it at `:76`: the whole "Blockchain anchor" card shows only when `Anchored` or a transaction hash is present. All four blobs this PR writes have a null hash after presentation and no `anchored` key, so that page shows **no card at all, at develop and at the head**. "Block 0" was never on that page for these blobs, and nothing on that page changes.

**What does change in Platform S is a different page** that gate 235 did not reach: the admin anchor pages read `Block #` as `0` at develop and `—` at the head (F1). That is an improvement on a page that was wrong.

**The change that really did cross `0` to hidden on the verify page shipped a month ago, in KS-1333 (PR 1500, merged 2026-10-12)**, for documents with a hash and no height yet. Its commit body says the external reader was unverified. That reader has now been read, and the word to Stuart should carry it (F3).

**Null stays null is still right for the stored value** (Q4). But this PR does not cure "Block 0" for users: both Secuura portals still print 0 themselves, and the issuer portal prints 0 for every real anchor because it never reads the height (F4, F5). Neither is a regression and neither blocks this PR; both should be ticketed.

Merge tree clean on current develop 76e8cf5d (tree 19f04507).

## Q1. What each caller sees, pending document, develop then head

Blob as the 202 path stores it: `{txHash: null, blockHeight, anchoredAt, status: 'pending', anchorId}`. Row status is `anchored` (`documents.ts:1038`).

| Caller | Where | Field | develop | head |
|---|---|---|---|---|
| GET /api/documents/:id | `documents.ts:1224-1234` | `blockchain.blockHeight` | 0 | **null** |
| same | `:1228` | `blockchain.anchored` | true | true (unchanged, see F6) |
| GET /api/documents (list) | `documents.ts:347-358` | no blockchain, no height | none | none |
| POST /api/documents 201 | `documents.ts:1074,1091` | `txHash: null`, no height | none | none |
| POST /api/documents/:id/anchor 202 | `documents.ts:1871-1875` | `blockchain.blockHeight` | 0 | **null** |
| POST /api/verification/verify and file verify | `verification.ts:1272`, `:1061` | `blockchain.blockHeight` | 0 | **null** |
| same | `:1283`, `:1068` | `checks.isAnchored` | false | false |
| verify v2 list | `verificationV2.ts:398,483` (same blob, READ ONLY) | `blockchain.blockHeight` | 0 | **null** |
| chain-first branches | `verification.ts:967,1534`, `verificationV2.ts:210` | from the chain index, not these writes | n/a | n/a |
| Published spec | `docs/openapi/secuura-api.yaml:6862` (no type), `:12241-12256` is the VC route | document and verify height not specified | silent | silent |
| Verifier portal | `ResultPage.tsx:449,497` | "Block Height" | **0** | **0** (F4) |
| Issuer portal | `DocumentDetail.tsx:185-192,490` | card needs a hash | no card | no card |
| Admin, status, website, add-ins, demo overlay | 0 height readers (control: 17 anchor files in admin) | none | none | none |
| Extranet `api/`, `app/` | 0 `blockHeight` (control: 15 `secuura` files) | none | none | none |
| Platform S verify page, snapshot | `_VerifyResult.cshtml:76,92` | card, Block row | **no card** | **no card** |
| Platform S admin Details and Index, snapshot | `Details.cshtml:99`, `Index.cshtml:204`, via `CardanoAnchorService.cs:458` | Block # | **0** | **—** (F1) |

The same holds for the simulated, failed and retry blobs (`evidence/probe_output.txt`, MEASURED for the two real predicates, transcribed for the readers). The failed row's verifier line assumes `verified: true`, which a row left in draft would not have.

**Is "no response shape" true?** Yes, as to shape: the key stays and the spec does not type it. It is a value change, 0 to null, on three route families. The fragments' stronger wording is not true: the cheat's "no verify answer on these four paths" and the flow's "So no verify answer changes" hold for `isAnchored` but not for `blockchain.blockHeight` in the same answer (F8).

**What the snapshot can and cannot show (F2).** It shows the reader as of about June. It cannot show the deployed Platform S.

## Q2. Null against 0, in behaviour

Null is better for every reader I found. Nothing treats 0 or null as proof on these blobs:
- `verification.ts:145-146`: the only line where they differ (0 refused, null accepted), and it needs `settled` and a real hash first. MEASURED: `{confirmed, real hash, 0}` false, `{confirmed, real hash, null}` true. None of the four sites builds a settled blob.
- `anchorStateSync.ts:590-592` (`stored > 0`), `systemTest/.../anchor_honesty.py:143` (`bool`), `DocumentDetail.tsx:120` and `ResultPage.tsx:497` (`||`): alike.
- Platform S (snapshot): `_VerifyResult.cshtml:92` and the admin views are presentation only. Its refresher takes status and hash only (`CardanoAnchorService.cs:153-155`). `verified` and `Verified` do not read the height.
- Nothing treats either value as failure.

**Was a document at height 0 ever shown as anchored at block 0?** Yes, three ways, none on the page gate 235 named:
1. GET /api/documents/:id at develop: `anchored: true, status: 'pending', txHash: null, blockHeight: 0`. The systemTest docstring quotes that shape (`test_anchor_honesty.py:179`). This PR fixes the 0, not the `true`.
2. Platform S admin: row status `anchored` maps to `confirmed`, `Verified` yes (`CardanoAnchorService.cs:441,462`), `Block #` 0, hash "not yet on chain". This PR fixes the 0 only.
3. Verifier portal: "Blockchain Proof", "Block Height 0". Not fixed (F4).

The only way null is worse: a client outside what I can see that does arithmetic on the field, or a strict `number` type on it. Hence the word to Stuart's team. Rows stored with 0 stay (no migration), so readers must treat 0 and null alike for good; every reader above already does.

## Q3. Does a client team rely on this?

On the June reader, no behaviour Stuart's team relies on changes: the verify page is identical, the admin column improves. **It still needs a word, because that reader is not the deployed one.** Route, per `Blockchain/CLAUDE.md:185-193`: a BLUF comment on KS-772 mentioning `@stuart.jamieson` (not posted, this gate posts nothing). Suggested content, prose only:
- From this deploy, `blockchain.blockHeight` on GET document and on verify is null, not 0, until confirmation; old rows keep 0.
- KS-1333 already did this for documents with a hash (F3).
- One question: does current Platform S read `blockHeight` anywhere other than the verify card and the admin `Block #` column, or do arithmetic on it?

If the answer is "only those", nothing further is owed. If not, that is when a ruling arises.

## Q4. Is "null stays null" still right?

**Yes for what is stored; I would not reverse it.** A stored 0 is a false fact with no compensating use, and 0 never distinguished anything for any reader. Three honest limits on the direction, none wrong enough to hold this PR:
- It was given while Platform S's reader was unverified, and the check was then never made. The risk was real, though it fell out harmlessly on the June reader.
- It is a statement about storage and was treated as curing the defect. It does not: the display defaults in F4 and F5 survive, and `anchored: true` beside a null height (F6) is arguably the bigger claim. `toBlockHeight` also keeps a literal 0 or `'0'` (gate 235, MEASURED), so "unknown is null" is not "never 0"; the anchoring 202 carries no height, so that is unreachable here.
- One real asymmetry to keep in view: `isAnchorHeight` refuses 0 and accepts null (`verification.ts:145`), so a confirmed blob with unknown height now reads anchored where a 0 would have read not anchored. That is KS-1628's stated choice and these four sites do not reach it.

## Q5. routes/anchors.ts:79 and the seven

The count closes. Daily note 2026-10-12: five sites filed at 22:53, two heal sites added at 23:00, seven. Then: 1 merged as PR 1569 (daily 2026-10-18; `anchorStateSync.ts:243` carries the KS-1509 comment), 4 here, 2 gone (`persistHealedAnchor` survives only in comments, `verification.ts:714`, `blockHeight.ts:7`). I did not read the ticket itself (no API).

Census at the head over services, packages, frontend and sdk, non-test (control: the same regex finds all four sites at develop; 522 height lines in services alone). Three production zero defaults remain: `anchors.ts:79`, `DocumentDetail.tsx:120`, `ResultPage.tsx:497`.

`routes/anchors.ts:79` is a read default on the anchors table, not a stored document height, and the fragment's "no other height default" predicate misses it (F9). The gateway sends `/api/anchors` and `/api/anchoring` to the anchoring service (`proxy.ts:904-920`), whose own read says `|| null` (`anchoring/src/index.ts:1028`), so Platform S's anchor reads do not meet it. READ ONLY; a direct call to originate would, and I did not exhaust internal callers.

**Merge tree on develop 76e8cf5d7:** rc 0, tree 19f0450743cf, explicit base 4ccdc3b3e7cf (my fetch is shallow, so plain merge-tree refused: my instrument, not a conflict). 0 shared paths with the 3 files moved since b7d433fd. Against b7d433fd: tree 53e1a556, equal to gate 235's. KS-1695 must rebase on `documents.ts` (gate 235, READY).

## Findings

**F1 NOTE (client-visible). Platform S admin `Block #` goes 0 to —.**
`Views/CardanoAnchorAdmin/Details.cshtml:99`, `Index.cshtml:204`, fed by `CardanoAnchorService.cs:458` from GET /api/documents/:id for `doc-` references (`UseOriginateForUpload` defaults true, `CardanoAnchorSettings.cs:45`). FOUND reading the snapshot. TESTED by transcription in the probe. Roles: admin and power users (`CardanoAnchorAdminController.cs:20`). This corrects gate 235 F1, which named the wrong page. Same correction: `/Verify` is `[Authorize]` in the snapshot (`VerifyController.cs:18`), not public.

**F2 MAJOR (not of this code; of what anyone can claim). The Platform S snapshot is stale and says nothing about the deployed service.**
`/Volumes/DevMASTER/!CODING/Secuura/platform-s-main` is not a git repo; newest file in `ssd/` is dated 2026-06-16; highest PS ticket mentioned is PS-118. `anchoring/src/index.ts:501` says Platform S has been live sending `onBehalfOf` since 2026-08-21 under PS-616; the snapshot has 0 files with `onBehalfOf` (control: 20 files with `CardanoAnchor`). So deployed Platform S is later than this reader, by evidence. Every Platform S statement in this verdict is about June. No gate can close this; Stuart's team can.

**F3 MODERATE (process, already shipped). The verify page's real 0-to-hidden change came from PR 1500, and it was left unverified.**
Commit 037575399 (2026-10-12) moved the four `anchorStateSync` writers from `|| 0` to `toBlockHeight`; its body says "THE EXTERNAL READER IS UNVERIFIED". A blob with a hash and no height is the state that passes `:76`, so on the June reader "Block 0" became no row there (probe, last block). READ ONLY. I found no word to Stuart in the 2026-10-13 daily (0 height-related hits; control 9 `platform s` lines): that is one day's note, not proof none went. Whether it has reached Platform S's environment is UNMEASURED; the 2026-11-05 22:04 note implies demo carries it.

**F4 MODERATE (pre-existing, not cured). Verifier portal prints "Block Height 0" for a document with no block.**
`frontend/verifier/src/components/ResultPage.tsx:449,497`, `(blockHeight || blockNumber || 0).toLocaleString()`, inside a "Blockchain Proof" card shown on `verified`, which is true for a pending row. Same at develop and head, beside a failing "Anchored on blockchain" check. The ticket's defect, a claimed block 0, survives here. READ ONLY plus probe transcription. Fix-shape: hide the row when there is no height. Ticket it.

**F5 MODERATE (pre-existing, independent of this PR). Issuer portal shows Block 0 for every real anchor.**
`frontend/issuer/src/components/DocumentDetail.tsx:185-192` builds the anchor from `raw.blockchain` with `id, status, network, txHash, anchoredAt` and no height; GET returns no `anchors` key; so `:120` always falls to `|| 0` and `BlockchainCard.tsx:195` renders 0 whenever a hash exists, even once confirmed at a real height. READ ONLY, not run in a browser; whether the row is behind a collapsed section I did not read. Fix-shape: carry `blockHeight` through and hide when null. Ticket it.

**F6 NOTE (pre-existing). GET document says `anchored: true` for a pending document.**
`documents.ts:1228`: `anchored` is true for any blob not `anchor_failed`, so `anchored: true, status: 'pending', txHash: null, blockHeight: null` at the head. This PR removes the 0 and leaves the larger claim. Issuer `DocumentDetail.tsx:185` keys on it, saved only by the hash guard at `:490`. READ ONLY.

**F7 NOTE. Platform S says "Document verified ... anchored on the blockchain" for a pending document.**
`_VerifyResult.cshtml:27` on `Verified`, true for row status `anchored` (`verification.ts:89,1264`), which is written when anchoring is accepted. Deliberate on the K side per KS-563's comment (`verification.ts:83-87`), but the sentence is S's. Unchanged by this PR; worth one line to Stuart. READ ONLY, snapshot.

**F8 MINOR. Fragment wording.**
Flow `.2` "So no verify answer changes" and cheat "no verify answer": `isAnchored` yes, `blockchain.blockHeight` no. Flow and cheat "Platform S's reading ... not checkable from this repository": true of the repo, but it should now cite this gate and the snapshot's age. Stale figures "212 files / 2504 cells, develop 1b1b65c7415f" (gate 235, carried).

**F9 MINOR. The census claim is narrower than it reads.**
Cheat "found no other height default" over originate `src`: `routes/anchors.ts:79` is one, a read default rather than a store. Say so, or ticket it with F4 and F5.

**F10 MINOR (docs, pre-existing). Public examples show the height as a string.**
`docs/VERIFICATION.md:64` and `services/api-gateway/src/docs/developer-portal.html:202` show `"blockHeight": "4615780"`. Platform S's `long?` with `JsonOpts` (`CardanoAnchorService.cs:19-23`, no number-from-string handling) would fail to read that, and the verify page would fall to "temporarily unavailable" (`:332-340`). This PR's `toBlockHeight` moves in the right direction. READ ONLY, deserialisation not run.

## NOT tested

- Platform S running: `dotnet` is absent. Its readers were transcribed by hand into the probe, not executed. The deployed Platform S: unseen.
- Any real document, Postgres, stack or deployed environment. Portals not opened in a browser.
- The PR's 8 cells and the originate suite not re-run: gate 235's 8 of 8 and three tampers reused, on the same head. Its documents.ts is unchanged since.
- Ticket KS-1509, KS-772 and the PR body: no API. Whether Stuart has already been told anything.
- Internal callers of originate's own `/api/anchors`, and stored rows' real population of 0 against null.
- `carriedForward`'s full key list (read only as far as the two sites that restate height after it).

## My own conduct

- Network: `git ls-remote` via the Blockchain repo's configured remote, and one `git fetch` (depth 3, blobless) of develop into a bare repo in my own scratchpad, using that repo's configured `core.sshCommand` deploy key. Nothing else.
- Reused gate 235's clone read-only through `GIT_NO_LAZY_FETCH=1`. Two `git status` calls there may have refreshed its index; no other write. The first merge-tree used a private object directory; the rest ran in my bare repo.
- A hook refused my first fetch because it could not resolve a variable naming the target; I reran with the literal scratchpad path, which is what the refusal directs. Another refused an unquoted `=====` separator.
- Instrument errors, all mine, all caught: `$H:Projects` was eaten by zsh's `:P` modifier; two height censuses read falsely short (`\b` unsupported by `git grep -E`, then a regex that missed `|| 0`), caught because the control did not find all four develop sites; first Extranet `git grep` read 0 and 0 on a non-repo, redone with `/usr/bin/grep` and a control; probe's issuer line first took the raw blob and read "card, Block 0" for s1, corrected, rerun, marked in `probe.ts`.
- Stopped one of my own background greps that overran on `0_Brain/reference`. It was also the search for Stuart routing, which I then read from `Blockchain/CLAUDE.md`.
- The first run's leftovers `g238_*` in gate 235's scratchpad: seen, listed, not used, not touched. Evidence folder was empty as briefed.
- Wrote only this folder (`verdict.md`, `evidence/probe.ts`, `probe_output.txt` sha256/16 323f9919f78bef20 before this file, `pins.txt`) and my scratchpad (3 MB). DevMASTER 23 GiB free at the end; it was 24 at the start, and I do not attribute that to this gate. No commit on any head.
