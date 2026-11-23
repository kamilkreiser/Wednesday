STARTABLE: YES

# B1995 DRAFTER REPORT (seat Datasec/OXPd2-R305, records): OXPd records of the five wave-1 landings (pull requests 33 to 37) and the product owner's two card answers of 2026-11-23

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1995_SEAT-R305_oxpd2-r-records-wave1.md` (109196 bytes, 507 line feeds, 0 bytes above 126, 0 card ids, 0 hits for the project scanner's name list).
- It holds 26 frozen texts, 42 SOURCES rows (every row hashed), 78 REVIEW MAP rows and 8 `____` lines (7 slots and the last line).
- Its sidecar `.measured` is beside it. `stamp_check.py <kit>` exits 0 with 208 claims, all 208 measured.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d1995/`. It holds the scripts `gets.py`, `logs.py`, `codefacts.py`, `factcheck.py`, `probes.py`, `reviewmap.py`, `jira_search.py`, `jira_ctx.py`, `proto.py`, `build_kit.py`, `sidecar.py`, plus `texts.md`, `kit_template.md`, `dry/`, `get/`, `blobs/`, `jira/`, the two card prints and `rulings.txt`.
- Drafted 17:00:56 to about 17:27 AEDT Mon 2026-11-23, by `date`.

## BLUF
- **Three record files, each written once by HOLD R, in this order (which is also the cut line):** `CLARIFICATIONS.md`, then `BACKLOG.md`, then `history.md`. The deviation register is not written. It is hashed before and after the write and must be unchanged.
- **`CLARIFICATIONS.md`: two entries, C-72 and C-73 at drafting (PREDICTED).** The seat finds the numbers by program.
  - **C-PRINTER** is his 11:07 tap "Agents drive it".
  - **C-X1R3** is his 14:41 tap "Fix round now".
  - Both follow the form of C-70: no card id, then the title, the coordinator's recommendation, the label and detail, and the store's ruling time. Each has a "What it settles, read from the option's detail" sentence.
  - His 10:10 message is already C-71, written by R304. It is cited in H-OWNER and not entered again.
- **`BACKLOG.md`:**
  - **Two ticks.** Item 45 is closed: PR 33 wrote its last open line, the `TryGet` doc comment, and PR 36 made the host binding the item names. Item 65 is closed: PR 33's README states the `finally` limit.
  - **One evidence line on open item 33.** The root README's layout list is behind the solution.
  - **Eight new items, 79 to 86 at drafting (PREDICTED):**

    | Item | Content |
    |---|---|
    | TAROOT | B1979 FOUND 1 and INFO 2 |
    | PLAIN | B1982 FOUND 1, carrying the coordinator's first-printer-run rule |
    | SHOWN | B1982 FOUND 2 |
    | DUP | B1982 FOUND 3 |
    | IPTEXT | B1983 FOUND 2 |
    | 503 | B1986 FOUND 1, B1981 FOUND 2 as narrowed, and the 209-character line |
    | X1TIME | B1987 FOUND 2 and B1990 FOUND 2 |
    | REST5 | every other record point of the eight reviews |

  - Each item's Jira line states the search made before filing: BACKLOG.md by the seat (P-3 probes), and Jira OXPD2 by my GET.
- **`history.md`: one 14-line entry ending `(records seat)`.** Only the records seat writes `history.md` this round. Today's build kits B1972, B1985 and B1988 each forbid it to their seat. P-5 STOPs rather than write above an entry by another seat.
- **What the kit does not do:** no Jira call (Q1), no register row (Q3), and nothing to the printer or to any person.
- **READY line:** `READY B1995: <40 hex> | C-72 C-73`, so you can run `--delivered` for both cards.
- **Sizing and hard stop:** no build, no test and no lock. RECORDS DONE is at Step 0 + 60 and HARD STOP at Step 0 + 90, and every hard stop is at or before 23:30 AEDT.

## FACTS RE-MEASURED BY THE DRAFTER (instruments in scratch)
- **Origin (`gh api -X GET` under the OXPd GH_CONFIG_DIR, 17:05:16 to 17:05:34):**
  - Main is `d804de5e303d62a78a8bcd677ec2cd66940b91f4`. There are 37 PRs, 0 open, and every one is merged.
  - `pulls/38` and `pulls/99999` each return rc 1 (404).
  - Each landing has 1 parent, in a chain da8d64a8, 126c95e8 (PR 33), e193fb63 (34), cad65b86 (35), df762b28 (36), d804de5e (37).
  - Heads: 4d4e933c, 8dc7390d, ea0df6c0, 0c65be47 and 85e414d6. Each equals the head in the first line of that PR's LAST review.
  - Commits per PR are 1/1/1/3/4 and changed files 11/19/10/16/31.
- **Main push runs:**
  - Five `ci` runs (45097073295, 45097688311, 45099054678, 45104964428, 45113802756), each attempt 1, success, with all four jobs success.
  - Counted in the logs with colour stripped (`--allow-escape-sequences` is needed; without it gh exits 1):

    | Landing | Total, linux and windows | RULES | GUARD (linux / windows) |
    |---|---|---|---|
    | 33 | 1837 | 562 | 10 / 11 |
    | 34 | 1874 | 580 | 10 / 11 |
    | 35 | 1904 | 587 | 10 / 11 |
    | 36 | 1919 | 598 | 14 / 15 |
    | 37 | 1942 | 628 | 14 / 15 |

  - Every leg reads failed 0, skipped 4 on linux and 21 on windows. The rules job reads Ran 111 at the floor of 111.
  - Control: `total: 1943` is on 0 lines of all 15 logs. `failed Datasec.` is on 0 lines of all 15. Its positive control (the old C7 log, stripped) gives 1, and 0 unstripped.
  - Open alerts on main: 0. Main's csharp analysis of d804de5e has results 0.
- **The live PR bodies of 33 to 37 equal the gates' `pr-body.md` byte for byte**, including the "Still open" sections that the owed items rest on.
- **Code at d804de5e (GET raw, factcheck.py: 23 fragments at their lines, 10 counts with controls, 0 failures):**
  - Every finding the items file is still live in code.
    - `DeviceTokenClient.cs` lines 43, 62 and 76; `DisableCertificateDownloads` on 0 lines.
    - Lab `README.md` lines 19, 20 and 28; `ProbeCommand.cs:158`.
    - `Masking.cs` lines 16 and 44; `ArgumentException` on 0 lines.
    - `IppTransportException.cs:13`; Transport `README.md:30-31`.
    - Server `README.md:21-22`, and line 25 is 209 characters.
    - `Oxpd1ClientOptions.cs:86`.
  - The tick facts hold. "fresh array" is at `IDeviceSecretVault.cs:14` and on 0 lines at da8d64a8. `finally` is at Adapter `README.md:166`, 1 line, and 0 at da8d64a8. PR 36 added `SecretStoreDeviceVault.cs`.
  - The slnx has 34 Project rows (17 src, 17 tests), and the transport line is present, so B1983 FOUND 1 is closed.
  - The message of df762b28 holds "while the vault answers" once.
- **Project files:**
  - All four record files equal `.tools/b1970/READY.manifest`. `CLAUDE.md` is 1a2e5629.
  - Owed items run 1 to 78, 22 of them ticked. C headings run 1 to 71.
  - P-3 probes on the live files: every new-content probe reads 0, with controls that fired.
  - `TaskCanceledException` is on 1 line of BACKLOG (item 68) and `ArgumentException` on 1 (item 43). Both are written into the Jira lines as such. My first BL-IPTEXT draft said 0 for TaskCanceledException; probes.py caught it and the text was corrected before freezing.
- **Jira OXPD2 (GET only, through the project's own reader `b1785.py` loaded in place):**
  - 25 issues. The controls fired: OXPD2-1 returns 200, OXPD2-99999 returns 404, and the phrase "CI/CD skeleton" hits 7 issues.
  - There is no duplicate of any new item. "masked", "probe" and "OXPd 1.x" hit only OXPD2-1, the master list; I read the context, and it is other subjects. "503" hits only OXPD2-16, the Graph layer.
  - "pin" read 0 issues, which may be a search-tokenising artefact. It is not used in any text.
- **The cards:** `decision_queue.sh show <exact id>` was run once per card, each into scratch (1 id line each).
  - Printer route: ruled a, `ruled_ts 11:08:35.821067`, recommended a.
  - X1 round 3: ruled a, `ruled_ts 14:55:56.528642`, recommended a, and the card's default is a.
- **His rows today:** `kam_rulings_today.sh` at 17:09:50 shows 9 rows, with `TAPPED-BUT-OPEN: none`. The 11:07 and 14:41 rows are the two taps. The 11:06 "looks great. please build and deploy" is NexusAI (Tuesday's note line 117).
- **Panes, tools and disk:**
  - Panes: `%0 tuesday` and two unnamed panes. There is no `Datasec/OXPd2-` pane.
  - Model: CLAUDE.md line 7 (newest Opus) wins over routing row C8 (line 98). The model id is `claude-opus-5-5` (`models_latest.json` line 17).
  - Python is `/opt/homebrew/bin/python3` 3.14.10. `df` shows 951 GiB available.

## PROTOTYPE (dry/, scratch only, from the live bytes)
| File | Line feeds | Added | Changed | Other |
|---|---|---|---|---|
| `CLARIFICATIONS.md` | 720 → 752 | 32 | 0 | The old bytes are a prefix of the new file. C headings run 1 to 73; the new ones are at lines 722 and 738. The card-id rule fires on 0 added lines and 80 old ones. |
| `BACKLOG.md` | 578 → 637 | 59 | 2 headings, one character each | TK-45 is at line 310, TK-65 at 467 and EV-33 at 221. The new item headings are at 565, 572 and so on to 614. Ticked goes 22 → 24 and the owed list runs 1 to 86. |
| `history.md` | 234 → 248 | 14 | 0 | Every old line stays in order. |

**Scans:** `scan_record`, from the project's own `b1785.py`, ran over 90 added or replaced lines (CL 16, BL 61, HI 13).
- It found 0 problems, 0 bytes above 126 and 0 leftover fills.
- Six controls fired (name `_by_kam_`, card id, coordinator path, a byte above 126, a leftover fill, a URL) and a clean line stayed quiet.
- The green and race check found 0, with its controls firing and its quiet line quiet.

**A proof defect found and fixed in my own prototype:** my first BACKLOG proof removed the inserted lines by matching their text. BL-REST5's `    - Jira: none` line equals many old lines, so that proof read false. The proof now removes lines by their inserted position. The kit tells the seat to do the same, and its selftest must show the text-matching form failing on this kit's own text.

## STEP INPUT TABLE (each input made by an earlier step or present at BASE)
| Step | Inputs | Made by |
|---|---|---|
| 0 | the kit and its sidecar; the live record files; the scanner `b1785.py` | BASE |
| 1 | `b1970.py` (model, read only); the scanner copy | BASE; Step 0 |
| 2 | THE SOURCES files; origin GETs; the `before/` copies | BASE; Step 0 |
| 3 | the frozen texts; the fills from the live files; the scanner copy; the helper | the kit; Step 2; Step 0; Step 1 |
| 4 | the dry builds' checks; the live bytes, re-read inside the writing process | Step 3; BASE |
| 5 | the proofs and figures | Steps 0 to 4 |

## D-DECISIONS (the drafter's)
- **D1: owed items, not tickets.** The project states no "Minor becomes a ticket" rule. CLAUDE.md:66 governs a ticket's form (BLUF, WP and F number), not when one is made. The BACKLOG header and practice settle it: 60 `- Jira:` lines, every gate Minor filed as an owed item, and tickets created only where a ruling's label named one (B1816 and B1900). So I filed none (Q1).
- **D2: the grouping.** I made one item per FOUND that a later round fixes on its own.
  - The AIA Info goes with B1979 FOUND 1, because it is the same file and the same round.
  - B1981 FOUND 2 (the logging filter) and the 209-character line go with B1986 FOUND 1, because it is the same README.
  - B1987 FOUND 2 and B1990 FOUND 2 go together, because they are the same follow-up.
  - The remaining record points go into REST5. Landing mechanics consumed by the landings are not filed: merge-tree no-conflict notes, MAIN MOVES, landing texts, scans.
  - Findings closed before landing are recorded as closed in REST5 and the history entry: B1980's four, B1987 FOUND 1 and 3, B1981 FOUND 1 and 3, and B1983 FOUND 1, closed by PR 36.
- **D3: the item 33 evidence line, not a new item.** The commission says to add evidence to an existing item rather than file a duplicate. Item 33 already owes "the one README pass after the wave (the layout ...)" (Q5).
- **D4: ticks.**
  - Item 45 is ticked whole. The 11-23 pass said "closes it but for the doc-comment line of limit (10)", PR 33 wrote that line (measured), and F1981 and F1986 say the host binding is "the records lane ticks it".
  - Item 65 is ticked whole. Its kept-open part was "the README holds no line with the word finally". PR 33's README now states the limit at lines 166 to 168, and F1979 says "BACKLOG item 65's open part closed".
  - No other item is touched. Item 43(4) waits for the first real probe (F1982 item 6).
- **D5: board minutes in the C-entries.** C-70's form, and the rulings reader, give the minute only. Of the commission's 11:07:45 and 14:41:39, only 14:41:39 is printed by an instrument (the reader's freshness line). Both entries carry the minute plus the store's ruled_ts (Q4).
- **D6: the first-printer-run rule.** The commission and your note line 126 call B1982 FOUND 1 a HARD RULE for the first printer run. I wrote it as the coordinator's rule in BL-PLAIN, H-WHO and C-PRINTER: no run passes `--plain-discovery-tree` without `--pin` while item PLAIN is open (Q6).
- **D7: the history writer.** Wave-1 build kits forbid `history.md` to their seats, and the wave-2 kits are not yet written. P-5 makes any non-records entry above line 3 a STOP. REFUSE 5 lets build-seat panes run beside the records seat, because their own scope lines decide.
- **D8: who is credited for the C-56 reading.** The HP description files of PR 37 under `contracts/oxpd1/` stand on the coordinator's reading of C-56 with leave to correct (F1980 item 9). This is relayed in REST5 and H-WHO, with no register row.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q1: Jira tickets for the Minors?** B1986 and B1990 grade their findings "Minor, ship with a ticket". Default: **no Jira call; each is an owed item** (D1). The alternative is a CREATE slot with frozen ticket texts scanned by `scan_jira`, which bans backticks, double quotes, B-numbers and the words lane, gate and seat. That needs a re-cut.
- **Q2: the grouping of the eight items.** Default: **as frozen** (D2).
- **Q3: a deviation-register row for the `contracts/oxpd1/` files under the C-56 reading, or for any landing?** Default: **no row.** No FOR-RECORDS line names one.
- **Q4: board time to the minute (11:07, 14:41) plus the store's ruled_ts?** Default: **yes** (D5). If you want 11:07:45, you print it with your raw reader and the text is re-frozen.
- **Q5: an evidence line on item 33 rather than a ninth item for the root README layout list?** Default: **the evidence line.**
- **Q6: the first-printer-run rule in the records as the coordinator's?** Default: **yes**, in BL-PLAIN, H-WHO and C-PRINTER. Say so if you want it out of the C-entry.

## UNMEASURED
- **Never run on a real output** (named so in the kit): the seat's helper and selftest, HOLD R and HOLD R2 on the live files, the numbers at the seat's run, and the three-write order with its stop after a partial write.
- Whether a pull request 38 lands before the seat runs. The kit STOPs on a merged 38 or higher.
- The board seconds of the 11:07 tap (D5).
- Every Linux and Windows behaviour the items relay as UNMEASURED.

## OUTSIDE THE FENCES (disclosure)
- **Reads in parts:**
  - VERDICTs V1979, V1982, V1983 and V1990 were read whole. V1986 was read through line 119 (BLUF, FOUND, INFO and the frame table); the overflow went to a tool file that I then read whole.
  - V1980, V1981 and V1987 were read in parts: their FOUND and INFO sections, located by program. Their findings are all closed or carried by the later rounds' FOR-RECORDS, which I read whole.
  - All eight FOR-RECORDS files were read whole.
- **The rulings reader:** I ran `kam_rulings_today.sh` with `KAM_READ_MARKER` pointed at my scratch (`d1995/kam_read_marker_drafter`), so your `kam_read_tuesday` marker did not move.
- **The cards:** `decision_queue.sh show` was run twice, once per exact id, into scratch (read-only).
- **Jira:** GET only, through the project's `b1785.py` loaded in place with `importlib` under `python3 -I -B`, never run as a program. Its write logger was replaced in-process by a refusal. No credential was printed.
- **GitHub:** `gh api -X GET` only.
- **No writes outside my scope:** nothing to the project, Jira or mail.
- **How the kit and sidecar were written:** by my scratch programs (`build_kit.py`, `sidecar.py`, and `stamp_check.py --init` for the skeleton), the same way as the B1970 form, not by the Write tool. This report was written with Write.
- **Hook advisories:** the guards printed advisories (grep with cut, case) on some reads, and I complied. One echo separator was refused by the zsh word-split hook and re-issued as `----`; that was the same read, not a workaround.
- **Other drafters:** nothing of the three wave-2 drafters (d1992 to d1994) was read or touched.
