STARTABLE: YES

# B2003 DRAFTER REPORT (seat Datasec/OXPd2-R305, records): the re-cut of the unstamped kit B1995. It covers pull requests 33 to 40 and the product owner's five answers of 2026-11-23 (11:07, 14:41, 17:56 note, 17:58, 17:58)

**Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2003_SEAT-R305_oxpd2-r-records-wave1-and-2.md`
- Size: 171631 bytes, 858 line feeds, 0 bytes above 126.
- Contents: 40 frozen texts, 59 SOURCES rows (every row hashed), 141 REVIEW MAP rows, and 8 `____` lines (7 slots and the last line).
- Sidecar `.measured` sits beside the kit. `stamp_check.py <kit>` exits 0 with 325 claims, all 325 measured (283 by an instrument, 42 not a literal).
- The B1995 files are untouched; their mtimes are still 16:59 to 17:27.

**Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d2003/`
- Scripts: `gets.py`, `gets2.py`, `gets3.py`, `logs.py`, `codefacts.py`, `factcheck.py`, `probes.py`, `reviewmap.py`, `rm_new.py`, `jira_search.py`, `jira_ctx.py`, `make_texts.py`, `proto.py`, `build_kit.py`, `sidecar.py`.
- Copies of B1995's scripts were made with `cp -n` and then edited in d2003 only.
- Data and outputs: `texts.md`, `new_texts.md`, `texts_b1995.md`, `kit_template.md`, `dry/`, `get/`, `blobs/`, `jira/`, five card prints and `rulings.txt`.

**Drafted:** 20:08:15 to about 20:30 AEDT, Mon 2026-11-23, by `date`.

## BLUF
**Three record files, each written once by HOLD R, in this order (which is also the cut line):** `CLARIFICATIONS.md`, then `BACKLOG.md`, then `history.md`. The deviation register is not written.

**`CLARIFICATIONS.md`: five entries, C-72 to C-76 at drafting (PREDICTED; the seat finds the numbers by program).**

| Entry | His answer | Notes |
|---|---|---|
| C-PRINTER | 11:07, Agents drive it | Re-worded: the first run now rests on the probe (34) and on `oxpd1` (40, first-run step 1). |
| C-X1R3 | 14:41, Fix round now | Unchanged. |
| C-HPLIB | 17:56, his NOTE, verbatim | The note is the ruling. The store's key "a" is named as not his word. Option a's detail (the H6 email draft) is NOT copied. Its "what it settles" is your reading as posted on the board. It cites C-11 and C-58 paragraph 10, which `grep` found (see D3). |
| C-AZURE | 17:58, One Azure test resource now | NOT your recommendation b. What it settles: one small resource in the agent-controllable environment, with cost and tenant on a card first; nothing is created. |
| C-SIGNIN | 17:58, Test the panel on the M577 first | Needs a test tenant user from him. |

**`BACKLOG.md`:**
- **Kept from B1995:** ticks on items 45 and 65, and the evidence line on item 33.
- **New, two "Closed in part" lines; both items stay open:**
  - Item 36: F1 to F3 were closed by PR 7 (`0804860b`, an ancestor of main by GET), which the item never named. F6 was closed by PR 38.
  - Item 67: its PR-20 part (K8) was closed by PR 38.
- **Fourteen new items, 79 to 92 at drafting (PREDICTED):**
  - B1995's eight: TAROOT, PLAIN, SHOWN, DUP, IPTEXT, 503, X1TIME, REST5.

    | Item | Content |
    |---|---|
    | FKTEXT | B1998 FOUND 1 |
    | ECHO | B2000 FOUND 1 and B2002 FOUND 1: a pin, or the admin password, echoed by a usage error |
    | EXITS | B2000 FOUND 2 and B2002 FOUND 2 |
    | LABTEXT | `DeviceChannel.cs:37`, made untrue by L5; `CommandRegistry.cs:19`; the two exact-list cells |
    | REST3 | Every other record point of PRs 38 to 40 and the FOR RECORDS of B1993, B1992 and B1997 |
    | DESIGNREV | The B1996 review exists, where it is, that A1 to A4 and A16 are owed to a documents pass, and that none is applied |

**`history.md`:** one 17-line entry ending `(records seat)`. The kits B1992, B1993 and B1997 each forbid `history.md` to their seats (measured).

**Not done by the kit:** no Jira call, no register row, no design amendment, no Azure call, nothing to any person or to the printer.

**READY line:** `READY B2003: <40 hex> | C-72 C-73 C-74 C-75 C-76`.

## FACTS RE-MEASURED (instruments in scratch)
**Origin** (`gh api -X GET`, OXPd GH_CONFIG_DIR, 20:08:25 to 20:08:53):
- Main is `2e2feae85d5fe3b8ee07cf618e3005b0630f4ca0`. There are 40 PRs, 0 open, and all are merged.
- `pulls/41` and `pulls/99999` each return rc 1.
- The chain runs da8d64a8, then 126c95e8 (33), e193fb63, cad65b86, df762b28, d804de5e, 86473f8a (38), 57e9042a (39), 2e2feae8 (40), each with 1 parent.
- Heads 81ae47ed, 26f4b57a and f0cd57a3 equal the first lines of B1998, B2000 and B2002.
- The 8 live PR bodies equal the gates' `pr-body.md` byte for byte.

**Main push runs:** 8 `ci` runs, attempt 1, every job success.

| PR | Run | linux / windows total | Rules files |
|---|---|---|---|
| 38 | 45133195497 | 1945 | 629 |
| 39 | 45135840964 | 1971 | 635 |
| 40 | 45143388653 | 2007 | 643 |

- Every log reads failed 0.
- Controls: `total: 2008` is on 0 lines of all 24 logs. `failed Datasec.` is on 0 lines of all 24. The positive control (the C7 log) gives 1 stripped and 0 raw.
- Code scanning: 0 open alerts. The csharp analysis of each of the 8 merge commits has results 0.

**Code at 2e2feae8:**
- factcheck: every fragment at its line, 0 failures.
- B1995's line numbers moved for three texts, and those texts were re-cut:
  - Lab README `:19`/`:20` is now `:26`/`:27`, and `:28` is now `:35`.
  - The Oxpd1 README lines 46 to 50 are now 49 to 53.
- Every new finding is still live in code: `PrintCommand.cs:108`/`:55`, `Oxpd1Command.cs:133`/`:52`, `RunRecorder.cs:26`, `LabFiles.cs:17`/`:18`/`:24`/`:54`, `DeviceChannel.cs:37`, `CommandRegistry.cs:19`, and `ApplicationClient.cs:9`/`:10`.
- The record files still equal the B1970 manifest. There is no `.tools/b1995` and no B1995 STATUS.

**Jira OXPD2:** GET only, through `b1785.py` in place. 25 issues; the controls fired (200/404).
- No duplicate of any new item.
- "amendment" hits only OXPD2-1, on another subject (I read the context).

**The cards:**
- `decision_queue.sh show` was run once per id, 5 ids. The two older cards are byte-equal to B1995's prints.
- `kam_rulings_today.sh` was run with the marker in my scratch. It shows 12 rows, including the note's verbatim text, and `TAPPED-BUT-OPEN: none`.

**Prototype (dry/):**

| File | Line feeds | Added | Changed |
|---|---|---|---|
| CL | 720 → 798 | 78 | 0 |
| BL | 578 → 681 | 103 | 2 headings |
| HI | 234 → 251 | 17 | 0 |

- `scan_record` found 0 problems over 160 lines, with 6 controls fired.
- The green and race checks found 0, with their controls firing.

## D-DECISIONS (the drafter's)
- **D1: closed in part, not ticks, for items 36 and 67.** Both items keep other open parts: F4, F5, F7, D11, the runbook and the README for 36, and every other PR's points for 67.
- **D2: ECHO and EXITS each group two gates' findings.** B2002 says "same class as B2000 FOUND 1/2". One later round fixes both commands.
- **D3: C-HPLIB cites C-58.** `grep` found his earlier words "We have the commercial agreement" in C-58 paragraph 10. They are cited, not re-entered.
- **D4: BL-REST5 is amended.** "A lab command that calls this client is owed" now reads "was owed and is built by pull request 40".
- **D5: landing mechanics are not filed.** This covers B2000 item 8 (L5 after L4, consumed by the landing) and the stale PREDICTIONS block in the B1997 STATUS.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q1:** no Jira ticket; every Minor and Info becomes an owed item. Default: as frozen.
- **Q2:** the grouping of the 14 items. Default: as frozen.
- **Q3:** no register row. B1996 A15 proposes one; it is not applied. Default: none.
- **Q4:** the board minute (11:07, 14:41, 17:56, 17:58) plus the store's ruled_ts. Default: yes.
- **Q5:** the evidence line on item 33 rather than a new item. Default: yes.
- **Q6:** the first-printer-run rule is yours, in BL-PLAIN, H-WHO and C-PRINTER. Default: yes.
- **Q7:** no design amendment is applied, A11 included, and the review is recorded only as DESIGNREV.
  - The B1997 kit's FOR RECORDS says "A11 is the records lane's". Your commission says records applies none.
  - Default: follow the commission.
- **Q8:** C-HPLIB names the store's key "a" (label only) as not his word, and omits option a's detail, which proposes the H6 email his note makes unneeded. Default: as frozen.
- **Q9:** the kit pastes the 5 card prints whole, as the commission asks, so card ids appear in the kit 11 times (B1995's kit had 0). No record text holds one: S-CARD found 0 on the added lines. Default: keep.

## UNMEASURED / NEVER RUN
- Never run: the seat's helper and selftest, HOLD R and HOLD R2 on the live files, the numbers at the seat's run, and the three-write order.
- Whether PR 41 lands before launch (the kit STOPs on a merged 41).
- Every Linux and Windows behaviour the items relay.

## OUTSIDE THE FENCES (disclosure)
**Reads:**
- Read whole: the B1995 kit, report and commission; the B1998, B2000 and B2002 VERDICT and FOR-RECORDS files.
- Read by section: the FOR RECORDS sections of B1992, B1993 and B1997; B1996's BLUF and amendment table.

**Writes outside the kit:** none to the project, GitHub, Jira or mail.
- `gh api -X GET` only.
- Jira GETs only, through the project's reader loaded in place, with its write logger replaced by a refusal. No credential was printed.

**Hook advisories and refusals:**
- One echo separator was refused by the zsh word-split hook and re-issued as `----`.
- Grep advisories were noted; every absence claim was counted untruncated by program.

**Scratch edits:** `sed -i` was used on my own scratch scripts only.
