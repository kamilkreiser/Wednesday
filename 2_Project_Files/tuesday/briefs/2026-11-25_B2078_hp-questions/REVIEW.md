# B2078 REVIEW: every state decision, its source line, and what could not be established

Clock printed at start: `Wed 25 Nov 2026 10:01:36 AEDT`. Read-only toward every project, Jira and the NAS. Nothing sent. Writes only in this folder and in the scratch folder `fleet/state/s326/b2078/`.

Pointer forms: `SEND` = `tuesday/briefs/2026-11-24_B2027_answers/HP-ASKS-TO-SEND.md` (24 Nov, 276 lines). `KA` = `.../KAMIL-ACTIONS.r1.md`. `AM` = `.../ANSWERS-MAP.r1.md`, and `AM0` = `ANSWERS-MAP.md`. `PK4` = `.../pack-v4/2026-11-24_OXPd-kickoff-meeting-pack_v4.md`. `DRAFT` = `OXPd_2/1_Project_Definition/Registers/HP_QUESTIONS_DRAFT.md` (20 Nov 13:29, 450 lines). `QBO` = `.../Registers/QUESTIONS_BY_OWNER.md` (20 Nov 16:10, 1,077 lines). `QBO2` = `QUESTIONS_BY_OWNER_v2_2026-11-20.docx` (20 Nov 21:23; text extracted with textutil to scratch `qbo_v2.txt`, 1,332 lines). `CL` = OXPd_2 `CLARIFICATIONS.md` (1,114 lines). `BL` = OXPd_2 `BACKLOG.md`. `REG` = `TUESDAY/0_Brain/reference/2026-09-27_hpsmpoc-hp-requests/HP_REQUESTS_REGISTER.md` (mtime 16 Oct).

## 1. Which list is authoritative (Tuesday's addendum)

Four documents carry the same H1 to H8 numbering. In date order:

| Document | Date | What it is | Who cites it |
|---|---|---|---|
| DRAFT | 20 Nov 13:29 | The first copy-ready H1 to H8, 38 points | KA:24 and KA:38 ("as drafted in `Registers/HP_QUESTIONS_DRAFT.md`"); AM0:147 and AM:137 (source column); Jira OXPD2-57 description; DRAFT itself says "DRAFT, nothing sent" (:1) |
| QBO | 20 Nov 16:10 | Says of itself: "**This file replaces `registers/HP_QUESTIONS_DRAFT.md` as the working document.** That draft is kept unchanged as a record; nothing in it should be sent as it stands, because three of its blocks are reworded here" (QBO:3). Rewords H1, H2 and H6 after Kam's statement of ownership (QBO:15-19, :498-507). The Jira OXPD2-1 comment of 20 Nov 16:12 says the same ("It replaces HP_QUESTIONS_DRAFT as the working document") | QBO2 (its LIST C header: "The full copy-ready messages are in the earlier document, unchanged") |
| QBO2 | 20 Nov 21:23 | The same asks split into answer-box sub-ids (H1-0 ... H8-9), 63 HP items, none answered (QBO2 text, LIST C header) | PK4 source tags ("QUESTIONS_BY_OWNER v2 P1-1 to P1-5"; pack v3 Q40) |
| SEND | 24 Nov (mailed to Kam 10:38) | The send-ready texts after Kam's 24 Nov taps: q39 "everything goes out now", the "Send with the three edits" tap (CL:962), the "I'll send H5 and H3 now" tap (CL:970) | PK4:5 ("the eight HP asks (H1 to H8), which you are sending"); daily_tuesday 2026-11-24.md:50 |

**Ruling used for this PDF:** SEND is authoritative for H2 to H8. It is the newest, and it alone carries Kam's 24 Nov edits. **H1 is the exception.** SEND's H1 (SEND:92-126) is DRAFT's H1 word for word (DRAFT:26-57, with the brackets replaced by the sign-off). It brings back point 1, "Is an OXPd solution ... acceptable to HP", and the line "my understanding was that HP is comfortable with this approach". QBO had struck both 20 hours earlier (QBO:16, :500; table row QBO:889, "Fell away (C-45)"). The cause is that KA and OXPD2-57 point at DRAFT, the superseded register, not at QBO. So H1 in the PDF uses QBO's wording (QBO:513-541) with SEND's sign-off. **Tuesday decision 1 below.**

**Numbering reconciliation.** H1 to H8 mean the same ask in all four documents. Point numbering differs:
- H1: DRAFT points 1, 2, 3 become QBO and PDF points (struck), 1, 2. In QBO2 they are H1-1 and H1-2. SEND keeps DRAFT's three points.
- H2: DRAFT/QBO point 1 is QBO2 H2-1 to H2-4. SEND point 1 keeps only H2-1, the enrolment's scope; H2-2 is moot because Datasec is enrolled. H2-3 is answered by w45 (AM:177). H2-4, "how long", is kept in SEND point 1 as "how long do they usually take". Point 2 is H2-5/H2-6. Point 3 is H2-7, point 4 is H2-8, point 5 is H2-9.
- H3 points 1 to 6 are H3-1 to H3-6 everywhere. H4 points 1 to 4 are H4-1 to H4-4 everywhere.
- H5: point 1 is H5-1/H5-2, point 2 is H5-3/H5-4, point 3 is H5-5 to H5-7, and point 4 is H5-8 to H5-10. SEND drops the optional "[We have an HP <model>]" line (SEND:12).
- H6: point 1 is H6-1, 2a is H6-2, 2b is H6-3, 3 is H6-4, **4 is H6-5 (the only point SEND keeps)**, 5 is H6-6, and 6 is H6-7/H6-8.
- H7: SEND adds a new point 1 ("any OXPd 1.x SDK newer than 1.8.4.1"). DRAFT/QBO points 1 to 4 become SEND points 2 to 5 (QBO2 H7-1 to H7-7).
- H8 points 1 to 6 are QBO2 H8-1/2, H8-3/4, H8-5, H8-6/7, H8-8, H8-9.
- The pack ids are not HP asks. Q39 is "which of H1 to H8 do you send" (AM:137). Q40 and Q41 are questions to Kam about what HP told him (pack v3 r1:302-303).

## 2. OXPd: state per ask

"Sent?" evidence, common to all eight. KA:36: "**Nothing has gone to HP yet**". OXPD2-57, read today by GET: status Backlog, updated 2026-11-24T12:02:19; its description says "Nothing has gone to HP yet, by the project's records", and it has no comment. OXPD2-56: status Backlog, updated 2026-11-24T12:02:15, no comment. Daily notes 2026-11-24 and 2026-11-25: grep -i for H1-H8, "to HP", "HP ask", "sent HP" and "HP repl" finds no line saying anything was sent or answered. Positive control: the same grep finds 11-24.md:50 (the SEND e-mail to Kam). In the OXPd records, every history entry after 24 Nov says "nothing sent to HP" (history.md:7 to :56). **Not establishable from records:** whether Kam sent H5/H3 himself after his 10:35 tap ("I'll send H5 and H3 now", CL:970). His mailbox and the HP portal were not read. So the state is "not sent, per the records", and Kam must confirm.

| Ask | State | Decided from | Notes |
|---|---|---|---|
| H5 | CURRENT | SEND:18-51; CL:970; OXPD2-56 | Still true: the simulator is not downloaded and its guide was refused (DRAFT:14; QBO2 A21-9 OPEN). Bracket: account e-mail. Kam holds the developer account (QBO2 A21-1, his words: "We will use my access during the dev process") |
| H3 | CURRENT | SEND:53-90; CL:970 | No HP date found in any source read |
| H2 | CURRENT | SEND:128-158; CL:962; KA:42; AM:176-177 | Point 1 already reflects w44 "yes" and w45 |
| H1 | CHANGED | QBO:16, :500, :511-541, :889 against SEND:92-126 | See section 1. The bracket is still open: P1-1 to P1-5 are OPEN in QBO2 (text lines 233-262), and pack v3 Q40/Q41 are unanswered (AM0:221-222) |
| H4 | CURRENT | SEND:160-192 | SEND's "[adjust if this has changed]" was removed. Basis: Kam's q34 words "Versions prior to OXPd 2 can be tested now" (OXPD2-56 description), and the M577 on FutureSmart 5 (CL:1044, firmware file `cljM577_fs5.10...`). No FS6 printer or simulator appears in any 11-24/11-25 record (daily-note grep for simulator, FS6, "FutureSmart 6": no acquisition line) |
| H7 | CURRENT | SEND:213-239; CL:922; AM0:37 | Small wording drift: OXPD2-57 calls the edit "anything more recent than OXPd 1.9", while SEND asks for "newer than 1.8.4.1". SEND matches Kam's tap (1.9 = our 1.x line, CL:922), so SEND was used |
| H6 | CURRENT (reduced) | SEND:194-211; CL:758; CL:962; KA:41 | Only the beta-confidentiality point survives |
| H8 | CURRENT | SEND:241-276; DRAFT:375-388 | No phase-0 OXPd 2 test has run, so no point is settled at home |

Counts, OXPd: CURRENT 7, CHANGED 1, ANSWERED 0, SUPERSEDED 0 (as whole asks), UNKNOWN 0. Sent 0 by the records; all 8 are with Kam.

Points struck or answered inside asks (PDF Part 2):
- H1 old point 1 and the "comfortable" line: SUPERSEDED (QBO:16, :889).
- H2 "are we enrolled": ANSWERED by Kam, w44 "yes" (AM:176). H2 "who holds master admin": ANSWERED by Kam, w45 (AM:177).
- H6 points 1, 2 (a and b), 3, 5, 6: SUPERSEDED by Kam's note of 23 Nov 17:56, "our license / commercial agreement allows us to use HP code as part of our code" (CL:758), and his 24 Nov tap (CL:962; KA:41).
- H7 subject and scope: CHANGED (CL:922; SEND:8).
- Twelve factual rows: ANSWERED by HP's documents (DRAFT:403-420; QBO:870). Not re-checked against HP sources.

Candidates (not in Part 1):
- Development CA in the OXPd 1.x CA store: UNKNOWN. BL:756-760, owed item 103, open: "the question goes to HP through the master list OXPD2-1 and the product owner ... this item stays open until the step-3 kit settles it or HP answers". It has never been drafted as an ask.
- HP Token Proxy: optional line (DRAFT:105; QBO:592).
- Interim firmware for older printers: deliberately not asked (QBO:873; DRAFT:436).

Jira search (GET only): `project = OXPD2 AND text ~ "HP"` returned 15 issues. HP-ask issues are OXPD2-56 and OXPD2-57 (Kam's actions), OXPD2-10 (WP0.5, its comment says the draft exists and nothing was sent), and OXPD2-1 (master list; its 11 comments were read and none records sending or an HP reply). OXPD2-62, -52, -38, -34 and -29 are printer and Workpath questions for Steven Molnar, not HP asks. Credentials came from OXPd_2 `4_Credentials/.env` (keys JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN), read in-process and never printed. The script is in scratch `jira_get.py`.

## 3. HPSM-POC (appendix)

- **Location differs from the commission.** No `HP_REQUESTS_REGISTER.md` exists under `!CODING/Datasec/HPSM-POC/`. Its `Registers/` holds only `2026-09-23_jira-seed-log.json`. The HPSM CLARIFICATIONS line 163 names it as "Friday's notes, HP_REQUESTS_REGISTER.md". The file is REG, in Tuesday's brain reference folder, and two scratch clones of it exist under `fleet/state/s310/`. REG was read whole (153 lines) and was not changed. Nothing else of HPSM-POC was read beyond CLAUDE.md lines 1-40 and the one CLARIFICATIONS grep.
- **States, all from REG's summary table (REG:14-36) and its two update notes (REG:89-90, :148-149):** HP-1, 2, 7, 9, 10, 11, 12, 15, 16, 17, 18, 19 and 20 are CURRENT ("not yet sent to HP"). HP-4 is CHANGED (REG:36, :149). HP-6 is CHANGED (REG:36). HP-13 is CHANGED (REG:28). HP-5 is ANSWERED in part (REG:149). HP-8 is ANSWERED mostly (REG:36). HP-14 is ANSWERED (REG:29). HP-3 is SUPERSEDED (REG:18, :89-90). Candidates C-1 and C-2 (REG:38-42). Counts: 13 / 3 / 3 / 1.
- **Not established:** anything after 16 Oct. The HPSM records (CLARIFICATIONS, history, Jira HPSMPOC) were not read, per the commission. So "CURRENT" here means "open per a register 40 days old". Whether HP-9 (the PO) or HP-10 (the account) has since moved is unknown.

## 4. Rendering

`2_Project_Files/tools/md2pdf/md2pdf.sh` (pandoc then headless Chrome; the same Creator, HeadlessChrome, as pack v4's PDF per `pdfinfo`). Its stylesheet is neutral navy and grey with no client palette. Output: `HP-QUESTIONS_2026-11-25.pdf`, 14 pages (the script's count). Pages 1, 2, 3, 7, 11, 12 and 13 were checked as PNGs at 50 dpi. Three fixes were made after the first render: State/Source split into separate paragraphs, the HPSM ids made non-breaking, and one source line that carried a fleet folder name rewritten. The PDF text was grepped for `B20nn`, "seat" and "tuesday": 0 hits after the fixes. The positive control ("card" in H8) hit.

## 5. For Tuesday to decide

1. **H1 wording.** The PDF uses the 20 Nov rework, not the text Kam approved on 24 Nov. His "send with the three edits" never weighed this difference. Confirm with Kam, or revert to SEND:92-126.
2. **H6 lost a validation question.** Kam's strike was aimed at the licence points. It also removed QBO H6 point 2b: "Does HP validation and signing require, or check for, HP's own client library?" That is about HP's validation, not licence, and which client ships is still an open kick-off choice (PK4:123, K-1). Re-add it to H2 or leave it struck?
3. **Records errors to correct (the records seat's, not mine):** (a) PK4:5 and AM0:221-222 count Q40/Q41 as "sent to HP". They are questions to Kam and nothing was sent. (b) KA:24, KA:38 and OXPD2-57 point Kam at `HP_QUESTIONS_DRAFT.md`, the superseded register. (c) OXPD2-57's H7 wording.
4. **Owed item 103 (development CA):** draft it as H9, or leave it to the lab test?
5. **Ask Kam whether H5/H3 went out after 10:35 on 24 Nov.** Nothing in the records shows it.
