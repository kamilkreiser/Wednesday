STARTABLE: NO

# B2161 DRAFTER REPORT: the OXPd records kit for pull request 58 plus the product owner's OXPd words of 2026-11-27 (seat R341; supersedes B2146)

I am the in-session, read-only drafter for Tuesday s334. `date` printed my first clock as `Fri 27 Nov 2026 17:48:14 AEDT` and my last before this report as `18:11:40`. No Stamp slot holds a typed clock.

**Why NO.** The kit is complete and self-consistent for his rows up to 18:05:53, but the board kept moving while I drafted. At 18:11:40 two newer OXPd rows of his stood, which the kit does not record:
- 18:10:35, a tap: `Decision datasec-oxpd-test-user-second-factor-1127: a — Agents do it via our own admin app`.
- 18:11:28, a message: "I think you don't like to purchase licenses.  you have my approval to do so but after the user has been created I can purchase the license if you put the link and preference on the board".

The second message makes the D2 ticket's line "Buying it is a purchase, so it is yours" and C-96/C-97's "only he makes" incomplete. It may change Q10 (whether the licence stays his ticket). The kit's own guard catches this: slot RULINGS-NEW must read `no OXPd row of his newer than 2026-11-27 18:05:53`, so the stamp would STOP.

**The fix is small:**
- add C-100 for his rows from 18:10;
- re-word K2-D/D2-D, the D2 lines of C-96 and C-97, H-JIRA and J-1 (or drop T-D2);
- re-freeze.

Tuesday may want to wait until he pauses before re-drafting.

## Files written (nothing else outside my scratch)
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2161_SEAT-R341_oxpd2-records-pr58-and-1127-rulings.md`
  - sha256 `c0b0f9a6...`; 170876 bytes; 637 lines; 0 bytes above 126.
  - 11 underscore slot lines are unfilled.
  - Lines over 2000 characters: 1, 3, 5, 7, 14, 17, 21, 22, 148, 169, 172, 303, 377, 378, 405, 566, 578, 596.
- **Its sidecar `.measured`:** sha256 `70bf8aaf...`; 156 claims, 0 TODO. `stamp_check.py <kit>` exits rc 0.
- **This report.**
- **Scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s334/d2161/`.
  - The kit is generated: `assemble.py` (B2146's kit source, `part1.md`, `part3.md`, `part4.md`, `rest.md`), then `dry.py`, then `fillkit.py`.
  - `quotes.py` holds P-W's 87 quote rows.
  - `side.py` writes the sidecar.
  - The older sidecar is in `_quarantine/`.

## BLUF of the kit
- **It supersedes B2146.** B2146 was never stamped and is not edited.
- **For the landing it does everything B2146 did:** ticks 54, 55 and 75, new items 161 and 162, and the history entry. Every landing fact was re-measured and is unchanged:
  - main is 760e1a64 and no PR 59 exists;
  - the tarball's sha256 equals B2146's copy, and the pointers are 56 of 56 (pointer table `cmp`-equal);
  - hosted3 PASS at 17:52:29, its control FAIL 4;
  - the job logs `diff`-equal;
  - the nine record files still equal B2140's manifest.
- **Seven C-entries:**
  - **C-93:** B2146's note, re-worded so that it says nothing false. Before the landing no ruling bore on it, and his evening words, C-94 to C-99, decide none of its choices.
  - **C-94 to C-96:** his terminal words. They are RELAYED from the coordinator's daily note and pickup, and each entry says so, because CLARIFICATIONS line 3 says entries are copied from the board export. The credential is never quoted, not even its user name.
  - **C-97:** his taps K3, K2, D4, D3 and D2.
  - **C-98:** his note on K11 (the rule that the project mirrors a client deployment, verbatim), the K7 and K6 taps, and his message of 17:54. The coordinator's reading that it supersedes C-72 for the M577 is marked as such. The board line before a firmware change or factory reset is recorded as the coordinator's own rule.
  - **C-99:** the 18:03 thanks for the designs; P-4 tap a with its note; the K11b note and the coordinator's entry of option c on it; K11 withdrawn.
  - P-W re-finds every quote at its source by program: `QUOTES 87 BAD 0`.
- **Jira: five POSTs.**
  - Three creates, each assigned to him (account 616503d4...), due 2026-12-07, label `oxpd-kamil-action`, Relates OXPD2-1: K3 (reader and test card), K2 (app registration and attribute set; the test user stays OXPD2-61), D2 (the Business Premium licence).
  - Comment J-61 on OXPD2-61 and comment J-1 on OXPD2-1.
- **The addendum is applied.** REFUSE 5 refuses only another `OXPd2-R` pane. X82 may run alongside. The PARTITION names X82's five repo paths from both sides and says a record line about X82's work is out of scope. An open PR 59 is not a stop; a merged one is.

## Facts re-measured (instruments, clocks)
- **GitHub:** `ghreads.py` at 17:51:34, `facts2.py` at 17:52:10, `logs.py` at 17:52:22, `hosted3.py` (sha256 969fe376) at 17:52:29 with its control at 17:52:43. `gh auth status` shows kamilDatasec. The refs for b2161, b2146 and b2153 each read 0 rows.
- **Jira (GET-only fence, which fired on POST, PUT, DELETE and PATCH), from 17:50:13:**
  - census 63; `oxpd-kamil-action` is OXPD2-56 to 61 and 63;
  - OXPD2-61 has 0 comments and no due date; OXPD2-1 has 19 comments, the newest 41547;
  - createmeta for type 10030 includes `duedate`; link type 10003 is Relates; the assignable user search found one row.
  - Phrase searches: K2/K3/D2 subjects find 0 issues; 'card reader' and 'app registration' find OXPD2-1 only.
- **Probes:** P-3 ran at 18:01:15 (and 18:08 for the C-99 probes). R341 is named only by the build kit B2162, as this seat. Panes at 17:53:53: none named OXPd2.
- **Dry build:** CLARIFICATIONS goes from 1236 to 1424 line feeds, with C-93 to C-99 at lines 1238 to 1394. BACKLOG goes from 1212 to 1229 line feeds (sha 74800003 to ec96eb8b). history goes from 410 to 419 line feeds. `scan_record` reports 0 problems; doubled words and groups are 0, with two named exceptions (below). Jira codes: K3, K2 and D2 are S-DQUOTE and S-NAME; J-61 is S-DQUOTE; J-1 has none.

## D-decisions
- **D1:** his terminal words are recorded with an explicit "relayed, not from the board export" sentence.
- **D2:** K2's ticket holds two of the three pieces, and OXPD2-61 gets comment J-61 rather than an edit.
- **D3:** the due date comes from his option label, "by 7 Dec".
- **D4:** two doubled-word exceptions are written into the kit:
  - his verbatim "this project.  This project";
  - C-99's "a, A machine", which is the option letter followed by its label.
- **D5:** the RULINGS-NEW slot was moved to 18:05:53.

## Q-questions (defaults as written in the kit)
- **Q1, Q2–Q8:** as in B2146, all defaults "as written".
- **Q9:** C-94 to C-99, grouped by subject and channel. Default: as written.
- **Q10:** three tickets (K3, K2, D2) and J-61. Default: as written. Now at risk from his 18:11 message.
- **Q11:** credential never quoted. Default: as written.
- **Q12:** OXPD2-60 not touched. Default: as written.
- **Q13:** due 2026-12-07. Default: as written.
- **Q14:** no CLAUDE.md edit for his standing rule. Default: as written; it is Tuesday's to decide.

## UNMEASURED / NEVER RUN
- The seat's helper, HOLD R and HOLD R2, the live ticks, and the five POSTs.
- The K2 click steps.
- Whether his newest rows change more than D2.

## Outside the fences (disclosure)
- **Board reads:** `kam_msgs.sh` with its read marker in my scratch, at 17:49:02, 17:56:01, 18:07:48 and 18:11:40.
  - Its print of a 2026-11-25 row of another project held a credential. It was never saved, quoted or copied. My saved rows file holds only rows of 2026-11-27 from 17:39, and `grep -c -i password` on it reads 0.
- **Cards:** `decision_queue.sh show` for 11 named ids only. No `list`.
- **Coordinator files read:** the pickup lines 10 to 24 and the daily note lines 86 to 95, plus a scan for a password before printing.
- **Not touched:** no write to the project, Jira, GitHub, cards or mail. No `cd`; nothing deleted (the old sidecar was moved to quarantine).
