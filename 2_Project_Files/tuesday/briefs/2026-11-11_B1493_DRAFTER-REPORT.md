STARTABLE: YES

# B1493 DRAFTER REPORT: SEAT-R210, HPSM-POC records (guide 0.4, backup-copy deletion, two FOUND tickets)

Drafted 2026-11-11 13:35:20 to 13:48:08 AEDT (`date`). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1493_SEAT-R210_hpsmpoc-records-guide-delete-findings.md`, 121 lines (`wc -l`), sha256 prefix `18184d6286a08fb7`, with an identical `.pre-stamp` (`cmp` equal, same sha256).

## BLUF
- The kit follows the B1485 form exactly: the closed Jira list stated as a property, R206's scanner (word list as R206 left it, `builder` dropped), the dry run, read-backs, the snapshot diff, one records branch `records/b1493` and a pull request on the analysis repo that the seat lands itself, and ten Stamp slots plus the last line (11 lines with four underscores, measured).
- **E1 (expected C-339): the user guide DRAFT 0.4.** On-disk facts re-measured by me: full PDF 11,440,576 B, sha256 `8b514e7a..68c7`; e-mail PDF 4,041,342 B, `e124bc2e..da81`; both 80 pages A4; SOURCES has 87 figure rows. All of these equal the B1491 READY line. The commission is quoted verbatim, and the e-mail is recorded only through a GUIDE-SENT slot that you fill.
- **E2 (expected C-340): the deletion of `hpsmpoc-b1466-pre`** at 10:54:13 to 10:54:29 AEDT. It records the after-state ({hpsmpoc, master}, health 200/200), the activity log, and the way back now (point-in-time restore only, until about 2026-11-17). It cites C-335 as superseded and never edits it. The authority bullets are quoted by program with the card id withheld (D-2).
- **NT-A (walkthrough step 12) and NT-B (fifth unmarked record):** the file:lines are printed. Both texts scan clean (0 problems) on R206's own scanner, and the kit's templates, once filled, are byte-equal to the scanned texts. The duplicate search found no existing ticket on either item, so both are creates. A duplicate found at run time becomes one comment on that key.
- **No Jira comments or moves** for the guide or the deletion: no ticket owns either (D-3).

## Facts measured by the drafter (instrument, clock)
- Code main `009421a28616c8b31dde86b59d4c4ca674c288fa`; `compare 009421a2...main` reads `identical` (`gh api -X GET`, 13:35:58). Main check-runs: 21 success, 1 skipped.
- Analysis main `d4cc73ef2546412db31d1522e1d16c2620e3c1ec` (PR #193, 2 parents). Open pull requests: 0. `records/b1485` is present; `records/b1493` is absent (matching-refs listing). `pulls/99999` returns 404.
- `CLARIFICATIONS.md`, raw media type at `d4cc73ef` (13:36:06): 6019 lines, 1,970,668 bytes, sha256 prefix `4e194babf189aa19`. Newest heading `### C-338` at line 6011; `### C-263` appears once; `### C-339` appears 0 times. In C-335 the copy-state bullet is at line 5989. C-270 records the 2026-11-02 "keep Delivery phases and match the other places" ruling. C-191 records v0.3 at 42 pages and 56 figures. `grep -c -i -F` counts: `user guide` 11, `list-deleted` 0, `Delete it once I say` 0, `hpsmpoc-b1466-pre` 3, control `zzqqxx-never` 0.
- **NT-A code lines** (`awk NR==n` over raw files at `009421a2`, 13:43:36):
  - `steps.ts:143` is the step 12 title `Service offers: Assess / Implement / Optimize` (id `offers`; the 12th of the 14 ids, which start at line 49).
  - `steps.ts:212` is the screen-list label `Delivery phases`.
  - `steps.test.ts:29` pins the title.
  - `GlobalNav.tsx:50` is the menu label `Delivery phases`.
  - `WalkthroughPanel.tsx:134` renders `{step.title}` as the heading.
  - Code search for `"Service offers"` returns 6 files. Only `steps.ts` holds it as text a user sees; the others are 2 comments, 2 absence tests and the test pin, each read. Control `"Delivery phases"`: 17. Zero hits for `Service offers` in WalkthroughPanel.tsx/.test.tsx and the two walkthrough e2e specs, against the positive control in steps.ts.
- **NT-B code lines:**
  - `Caller.cs:51` (`SeesAllCustomers` is Admin or Consultant), `:231` (all customers returned for them), `:235` (Partner sees own, Demo sees seeded only).
  - `CustomerEndpoints.cs:47` (the list uses `CustomerScope.Visible`), `:90` (name stored as typed), `:111` (`SelfCustomerName`).
  - `ShowcaseSeeder.cs:114/115/120/125`: the four seeded names, each ending ` (sample)`. The mark is part of the stored name, not something the list adds.
  - `CustomerManagement.tsx:280` (the SampleNote), `:297` and `:333` (`{r.name}`).
- **Jira** (GET only; `/rest/api/3/search/jql` and issue GETs; credentials read in-process and never printed; 13:38:37 to 13:41:15):
  - 467 issues, highest HPSMPOC-467, 327 Done.
  - Marker phrases `REC-WALK12-11NOV` and `REC-UNMARKED-11NOV` return 0. Controls: `REC-RUL-6-10NOV` returns {100, 117, 180}; `REC-DEMO-ALIAS-11NOV` returns {467}.
  - NT-A searches: `"Service offers"` returns {456, 452, 412, 383, 369}; `walkthrough AND "Delivery phases"` 0; `"steps.ts"` {392}; `"step 12"` 0; `"Demo Walkthrough"` {455}.
  - NT-B searches: `"not marked"` returns {429, 49}; `"test record"` 0; `"sample mark"` 0; the five-word AND search {452, 25}.
  - I read 412, 450, 452, 455 and 392 in full. None names the step 12 title or an unmarked record, so none is the same item. 412 (Done) is the Home tile and sentence rename.
  - `"user guide"` returns {452} (phase 2); `"backup copy"` and `"hpsmpoc-b1466-pre"` return 0.
- **Records on disk:** B1491 STATUS is 181 lines, `a93455435acf8c39`; B1490 STATUS is 93 lines, `27db0d3d6d8aa153`. The brief copies in Briefs are `cmp`-equal to the TUESDAY copies (B1491 137 lines, `1f9f36e18bb350a2`; B1490 44 lines, `e7fb144968e08de0`). Section lines are printed by `grep -n -F` and are listed in the kit.
- **Deliverables:** 183 files, 36 MB. `git status` shows them as `??` (untracked), and the v0.3 folder is also untracked (`ls-files` empty). Analysis `.gitignore:16` is `*.pdf`.
- **Seat id R210:** a word scan of 172 non-`.pre-` brief files from 2026-11-10 and 11 finds 0; the control R209 is found in 3. Model row: `model-routing.md:97` (C7); model id `claude-sonnet-5-5` at `models_latest.json:23`; `brief_seat.sh:24` defaults to opus.
- **Kit self-checks:** 11 lines with four underscores (the ten slots and the last line). `@..@` slots: 0. Ban-list name hits: 0 (control fired). Card id in the kit: 0 (control: 1 in its own source line). Non-ASCII: 0.
- **Panes** (13:44): `%0 wednesday`, `%1 fleet-monitor`, `%19 Datasec/NexusAI-N123`, `%20` and `%21` unnamed. No HPSM-POC pane. load1 2.55.

## D-decisions (the kit's defaults; change at the stamp)
- **D-1 Labels `guide-finding` + `rec-2026-11-11`.** These are not review findings, so `review-finding` (HPSMPOC-467's label) would mislabel them. `guide-finding` is a new label; I did not check whether it already exists.
- **D-2 Authority "verbatim" with the card id withheld.** Your brief asked for the B1490 AUTHORITY section verbatim, but bullet 8 carries a board card id and DRAFTER_RULES rule 7 forbids card ids in kit or record text. The kit quotes bullets 8 and 9 by program, swapping only `Card` and the backticked id for "The board card (its id is not written),", which is the C-270 precedent. Bullet 10 (context) is relayed in words, because it holds a brief path, which the closing check bans outside the mandated lines.
- **D-3 No Jira comment for E1 or E2.** No ticket owns the guide or the copy. A deploy note on HPSMPOC-117 about the lost copy rollback is possible; the default is no.
- **D-4 Records item 4 (owed per the FOR TUESDAY sections), IN or OUT:**
  - B1490 line 91, the C-entry: IN (E2), including the PITR window until about 2026-11-17 and the `list-deleted` note.
  - B1491 line 173: mailing the PDF is OUT, because it is done and owned by you; E1 relays it via GUIDE-SENT.
  - B1491 line 173: the covering note is OUT, because it is a mail body, not a record.
  - B1491 line 173: committing the untracked deliverables is OUT. Earlier versions are untracked too, PDFs are gitignored, and it would be a write outside the records file.
  - B1491 line 173: "INVENTORY/SOURCES/CHANGES internal" is IN as one phrase in E1.
  - The other FOUND items are IN E1 as recorded with no ticket; their tickets are OUT (see Q-3).
- **D-5 Git identity.** If the fresh clone has no `user.email`, the kit has the seat copy the project analysis checkout's own configured name and email into the clone's repo-local config, as R206's clone carries them, and print before and after. Any other value is a STOP. I read this as using the repo's configured identity, not overriding it. If you read the new rule as banning even that, change the line to "STOP if the clone reads no identity".
- **D-6 A key outside a duplicate set is NOT a stop unless it is the same item or a marker hit.** This is looser than B1485's literal rule, which made its Deviation 1 a judgement call. A same-item key turns that create into ONE comment on it, as you asked.

## Q-questions for Tuesday (each with a default)
- **Q-1 GUIDE-SENT sentence.** Default: "On 2026-11-11 the coordinator e-mailed the e-mail PDF of draft 0.4 (80 pages) to the product owner." Your daily note line 61 records the send at about 12:13 with a receipt. I relayed only that the send happened; you attest it. No address.
- **Q-2 CREATE-A and CREATE-B.** Default: CREATE for both. Your 12:13 daily-note line lists both tickets as owed.
- **Q-3 Ticket for the person's first name on the Admin hub card and the Feedback dialog's first option** (B1491 FOUND line 170; masked in the guide's figures). Default: no ticket in this kit; E1 records it. It is a person's name shown on a site HP reviewers use, so you may want a separate card.
- **Q-4 NT-A fix shape.** It says "replace Service offers with Delivery phases", per the 2026-11-02 ruling (option a, match the other places). The done-when also allows "recorded as kept as the demo's own words", because the steps.ts header says the titles are the demo deck's own words. Default: keep both.

## UNMEASURED
- The fifth record's origin, owner, creation time and name. I never read it and the kit forbids reading or writing it.
- The review site today (no hosted request was made).
- Whether the mail reached the product owner.
- Jira `createmeta` for Task, and whether the label `guide-finding` exists (the seat re-reads createmeta).
- Whether CodeQL on the analysis PR behaves as on #193.
- The internal size figures inside B1491 STATUS (line 58 says 11,440,205 B; lines 164 and 173 say 11,440,576 B) are not reconciled. The kit writes only the READY line and the seat's own `shasum`.

## Outside-the-fences disclosure
- **One Bash call contained `cd /tmp`.** The no-cd hook refused the whole call before it ran, so nothing executed. This breaks DRAFTER_RULES fence 5 in intent; every call after it used absolute paths.
- **Scratch outside my two files:**
  - `/tmp/b1493d/` holds raw read caches: CLARIFICATIONS.md, code files, Jira search outputs, the git tree list.
  - My own GET-only Jira reader (`tools/jget.py`) and check scripts (`scancheck.py`, `kitcheck.py`, `cmpnt.py`) are also there. `scancheck.py` imports `.tools/b1485/scan1485.py` read-only; nothing in `.tools/b1485` was written.
  - The `.pre-stamp` copy was made with `cp -n`, not the Write tool.
- **Coordinator-tree reads:**
  - `0_Brain/daily_tuesday/2026-11-11.md` via a filtered grep, to learn whether the guide was mailed. It holds an address and a name; neither was copied.
  - One `git log -1` of the TUESDAY repo.
  - `model-routing.md:97`, `models_latest.json`, `brief_seat.sh` lines 20 to 28.
- **Project reads:**
  - B1490 STATUS. It holds subscription and tenant ids, a card id and a name; none was copied into the kit.
  - The R206 clone's `.git/config`, with the key path redacted in my print.
  - `git config user.email` of the project checkout and of `2_Project_Files`.
  - `gh auth status` (my terminal showed the account login; not written anywhere).
- **Network:** GitHub `gh api -X GET` only, including the code-search API. Jira GETs only. No hosted, UAT, demo or production host. No az, ssh or docker.
- **Path note:** DRAFTER_RULES still names `/Volumes/Laptop-DEV/...` paths. The B1485 precedent and this kit use `/Volumes/Datasec_DEV/...`, which is where the files are.
