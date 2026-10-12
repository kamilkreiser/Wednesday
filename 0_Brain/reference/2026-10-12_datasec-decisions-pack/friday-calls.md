# Friday's calls + source map: Datasec decisions pack, 2026-10-12

Datasec only (MPS Commercial Calculator, Security Composer, HPSM-POC). Built from the three lane tables in
`FRIDAY/2_Project_Files/friday/briefs_drafts/`:
- **MPS** = `2026-10-12_mpscalc_lanes_1919.md`
- **COMP** = `2026-10-12_composer_lanes_1919.md`
- **POC** = `2026-10-12_hpsmpoc_lanes_1919.md`

Re-read at source by this builder (read verbs only):
- MPS records repo: `main` `01ef803` (`BACKLOG.md`) and `records/b46` (`BACKLOG.md`).
- Composer records: `git show records/b133:BACKLOG.md` (`e04b0b13`).
- HPSM-POC: the B174 and B176 STATUS files in `1_Project_Definition/Briefs/`, and the 10-11 sort.
- **Not re-read:** HPSM analysis `bb1e888` is not in the local clone (local `origin/main` = `47565b8`), and I did not fetch it. The POC BACKLOG questions in the pack are the drafter's verbatim quotes. Jira was not read (no call).

Pack: `decisions-pack.html` / `.pdf`. 42 Kam decisions: MPS 11, COMP 19, POC 12.

---

## 1. Friday's own calls ([F] / NEEDS-FRIDAY), with the drafter's default

### MPS Calculator
| Row | Call | Drafter's default | Source |
|---|---|---|---|
| MPSCALC-61 CI/scanning | Dependency scanning and DAST are org settings | none given ("org settings") | MPS:81 |
| CodeQL ruleset did not block the first push | Org setting | none given | MPS:97 |
| Leak scanner not versioned | "Friday's call" (the row) | none given | MPS:110 |
| [B08A2-6] build servers | Shared SDK | none given | MPS:114 |
| [B38-N5] mark cost-bearing inputs Internal | "Friday's call" (the gate). Also gates MPSCALC-47 | none given | MPS:135, :69 |
| MPSCALC-56 Entra SSO | Proposed for Done on 10-11, still open: a Friday Jira write | move to Done | MPS:78, :192 |
| [B42-L4] duplicate JSON keys | Inside B53 | refuse | MPS:148 |
| B43-Q5 may need `Program.cs` (F2) | B53 tries route-local, else BLOCKED-BY-FILES | as briefed | MPS:194 |
| B27-H4 "503 while running" arm | Only routes whose contract lists 503, else BLOCKED-BY-FILES | as briefed | MPS:195 |
| Ports 6670–6689 | Friday's assignment overrides B41's note | as briefed (0 listeners at 19:22) | MPS:196 |

### Security Composer
| Q | Rows | Call | Drafter's default | Source |
|---|---|---|---|---|
| K-Q8 | 152, 178 | Spend migration 0022 now on two Low rows? | Hold; fold into the next migration round, with Lane RUNBOOK | COMP:87 |
| K-Q12 | 72 | Rename 7 `HPSM-light` comments now? | Now, as a one-commit chore after B134 merges | COMP:91, :73 |
| K-Q20 | 269 (file-name half) | Rename download file names by `policyTitle`? | No; B134 changes titles only | COMP:99 |
| K-Q21 | 159 | PDF-only template version `policy-document-pdf/2`? | Yes; join B134 by ADDENDUM | COMP:100 |
| K-Q23 | 66, 70, 71 | In-flight cap, per-address sign-in limit, mutant B37-M2 | Leave as built; close #71 as "keep" | COMP:102 |
| K-Q24 | 69 | 429 vs 401 on an expired token under flood | Web ends the session on that 429 when its token clock says expired | COMP:103 |
| K-Q25 | 157, 176 | Required properties on closed schemas | No change until an external consumer exists; close as noted | COMP:104 |
| K-Q26 | 197 | Monospace problem-code line vs the one-font rule | Allow monospace for codes in the token rule | COMP:105 |
| K-Q27 | 246 | `draftKeyLabel` unused | Leave it (never delete) | COMP:106 |
| K-Q28 | 313 | 0.011 px media overlap | Accept; B135 renames/strengthens #314's test only | COMP:107 |
| K-Q32 | 26, 34, 154 (font), 209 (b), 296 | §6 rows | #296 (a), the guard arm; #209 (b) refuse combining-mark-only names; rest hold | COMP:111 |
| K-Q30 (moved here) | 171 | Docker address pools on the laptop | Keep per-seat explicit subnets (what the briefs do) | COMP:109; BACKLOG b133:165 |
| — | 13 DONE-ALREADY rows | Close in records: #120, 202, 267, 262, 266, 268, 270, 283, 180, 79, 151, 222, 235 | close | COMP:113-126 |
| — | #269 scope | Worksheet read as a policy artefact, not the HPSM output | keep `worksheet.ts` in B134 | COMP:157-160 |
| — | records `main` behind `records/b133` | Briefs point to b133 | as briefed | COMP:155 |
| — | history.md not written this round | A change of practice; Friday folds history | as briefed | COMP:156 |
| — | Lane RUNBOOK and Lane APPROVER | Not briefed; third pane / next round | as drafted | COMP:22, :63 |

**Why K-Q30 is here, not in the pack:** row #171 names the fix shape as "Friday/Kam, not a seat". It was EASED by C-39 (networks 30 → 7), and the drafter's default (keep per-seat explicit subnets) needs nothing from Kam. If Friday wants the larger `default-address-pools`, that is a one-line ask to Kam in chat, not a decision.

### HPSM-POC
| Row | Call | Drafter's default | Source |
|---|---|---|---|
| HPSMPOC-154 (F) | Laptop showcase start-up seed: (a) close or (b) change `ShowcaseStartup.cs` | (a) close; the laptop showcase is single-user | POC:166 |
| HPSMPOC-245 (F) | Rule B189 notes N-1, N-2, N-4, N-5, N-6 | Accept N-1, N-2; ticket N-4–N-6 into the next BFF lane after B231 | POC:167 |
| HPSMPOC-246 (F) | Rule B193 notes N-2, N-4–N-7 | Accept N-2; deploy seat records N-4; rest to a timing lane after 13 Oct | POC:168 |
| HPSMPOC-248, -249 | Done by #144; Jira untransitioned | Friday transitions both | POC:65-66 |
| :105 gate B211 N-3 | Hash CHECK migration: when | Friday's call when (needs a deploy step) | POC:220 |
| HPSMPOC-229 R3-2 sweep | Sweep/reconcile of pending runs is out of B230 | stays on the ticket for Friday | POC:290 |
| B231 item 3 (228 N-9, S-N1) | Narrowest scope would drop it | keep in B231 (a measured tidy-up) | POC:289 |
| HPSMPOC-149 | Pinned-literal test | hold until B229 lands | POC:85 |
| HPSMPOC-152 | Hidden-character guard | build as an `infra/tests` rule (a workflow edit makes it Kam's) | POC:86 |
| Parked by ruling (92, 96, 117, 232, 234) | Reopening needs Kam or Friday | stay parked | POC:150-158 |

**HPSMPOC-224 is marked F/K** (POC:165). It went into the pack as **POC-2**, because it creates a new Azure resource that costs money and the drafter's own default says it "needs Kam's go for the resource". The design half (workspace-based resource, scrub before export) is Friday's.

---

## 2. Stale, mis-stated or dropped (not put to Kam)

1. **HPSMPOC-57 + HPSMPOC-29 (UAT): dropped as stale.** The lane table (POC:164) asks Kam whether to stand UAT up after 13 Oct or hold. But the 10-11 sort (`2026-10-11_hpsmpoc_open_ticket_sort.md:35`) records **C-52 (CLAR :555) as already RULED**: "a Lane A seat runs its Entra steps and deploy under Kam's login", and the spend (~A$49/month) is approved. What remains is **timing**, which Friday's HPSMPOC-232 ruling already governs (nothing changes before 13 Oct), plus Kam being present for the login steps. Friday: schedule it for 14 Oct and ask Kam for a login window in chat. Re-asking an approved spend is the wrong question.
2. **HPSMPOC-226 is internally inconsistent.** The lane table (POC:87) lists N-4, N-5 and N-7 as open API work. The 10-11 sort (`…hpsmpoc_open_ticket_sort.md:49`) says "N-4, N-5 and N-7 merged in #129 (3a9288a)". Re-check at `caa5a97` before you brief the Feedback-hardening lane. The Kam half (N-3, N-9) is in the pack as **POC-8**. Its wording comes from `HPSM-POC/1_Project_Definition/Briefs/2026-10-06_B174_STATUS.md:194-195, :205`. The lane table only said "Kam confirms", with no default; the pack's default "confirm both as built" is mine.
3. **MPS B46-Q2 (pack MPS-7): the default changed between sources.** The B46 brief's own default was "not possible (409); a later round adds it if Kam wants" (`records/b46:BACKLOG.md:685`). The lane table's default (MPS:179) is "an Approver may change or clear it". The pack uses the lane table's default. Friday may prefer the original.
4. **Composer K-Q1 (pack COMP-6): the default runs against the records.** BACKLOG #312 (b133:308) says "The records lean 'Datasec'" (the mock IdP models the auditor as Datasec staff, and C-35 moves auditors with consultants). The drafter's default keeps the id masked, which is the safer disclosure. The pack states the lean openly in the question.
5. **Composer K-Q29 and K-Q31 had no drafter default** ("Kam's word" / "as each row states"). The pack's default for both (COMP-16, COMP-17) is **hold / keep parked**, which means no change.
6. **MPS B46-R4 wording (pack MPS-11).** The lane table classes it D (fixed on b49, MPS:164), but the row says "the words are new, so Kam sees them before the deploy". BACKLOG b46:702 also names "1 days". B49's ruling covers only the two "quote" strings (`2026-10-12_B49_SEAT-A_gate-b48-fix-round.md:121`). "n days" is out of scope, and a due row is always more than 14 days, so the pack lists only the two quote forms.
7. **HPSM CI timeout (pack POC-1).** The 14m12s figure is Friday's read, not the drafter's (POC:64, :288; no `gh` login). If the real margin is wider, POC-1 is less urgent. B230's STOP rule protects the cap either way.
8. **Standing NEEDS-KAM rows: not re-asked.** None of them had a question with a default, and none changed since 10-11:
   - MPS: the 20 Q-register tickets (MPS:86, :189), plus 18, 23–25, 30–31, 35, 45, 52, 54, 58–60, 62, the W-defects, P-04, the DB-lane rows (B08A2-1/2/3/9), the spec .docx, MARGIN 12 dp and B40-R2.
   - HPSM: the 44 "Kam's own" Jira rows (POC:101-148), W1 rows 2 and 4, and B06 note 3 (POC:246-248).
   - Composer: none dropped. Every non-[F] K-Q is in the pack except K-Q30.
9. **MPS B46-R2 (Duplicate on the work queue)** is classed B (`QuoteList.tsx` held by F1) and needs "a new word for Kam". No word is drafted yet, so it is not in the words list.

---

## 3. Source map: every pack ID

### MPS (lane table `2026-10-12_mpscalc_lanes_1919.md`; BACKLOG = MPS records repo)
| Pack | Lane-table row(s) | Ticket / row ids | BACKLOG source |
|---|---|---|---|
| MPS-1 | :149, :181 (NK #3) | [B42-L5] (gate B41 N-12a) | main 01ef803 :581 |
| MPS-2 | :116, :186 (NK #8) | [B21-2] DEMO-S4 | main :215 |
| MPS-3 | :161, :180 (NK #2); :54 | [B46-R1] FR-DB-003; MPSCALC-28 | records/b46 :687 |
| MPS-4 | :118, :185 (NK #7) | [B21-4] default #6 | main :229 |
| MPS-5 | :133, :183 (NK #5) | [B38-N3] | main :439 |
| MPS-6 | :134, :184 (NK #6) | [B38-N4] | main :445 |
| MPS-7 | :160, :179 (NK #1) | [B46-Q2] | records/b46 :682 |
| MPS-8 | :140, :182 (NK #4) | [B40-R4] | main :496 |
| MPS-9 | :156-157, :187 (NK #9) | [B47-D3], [B47-D4]; Q-16 | main :694, :700 |
| MPS-10 | :86, :188 (NK #10) | MPSCALC-66 (Q-00), -81 (Q-15), -84 (Q-18) | 10-11 reconcile :101, :114, :117 |
| MPS-11 | :164 | [B46-R4]; B49 Row 6 ruling | records/b46 :702; B49 brief :121 |

### Composer (lane table `2026-10-12_composer_lanes_1919.md` §4; BACKLOG = `records/b133:BACKLOG.md`, line numbers in that file)
| Pack | Lane-table row | K-Q | BACKLOG rows (line) |
|---|---|---|---|
| COMP-1 | :93 | K-Q14 | #272 (:268), #252 (:248) |
| COMP-2 | :88 | K-Q9 | #35 (:39), #55 (:59), #30 (:34), #223 (:219), #226 (:222), #228 (:224), #231 (:227), #240 (:236); #108 (c) (:112) |
| COMP-3 | :81 | K-Q2 | #99 (:103), #182 (:176) |
| COMP-4 | :82 | K-Q3 | #95 (:99) |
| COMP-5 | :95 | K-Q16 | #300 (:296) |
| COMP-6 | :80 | K-Q1 | #312 (:308); cross-ref #177 |
| COMP-7 | :98 | K-Q19 | #106 (:110) |
| COMP-8 | :85 | K-Q6 | #172 (:166), #173 (:167) |
| COMP-9 | :84 | K-Q5 | #260 (:256), #285 (:281) |
| COMP-10 | :92 | K-Q13 | #278 (:274); C-62 |
| COMP-11 | :97 | K-Q18 | #104 (:108) |
| COMP-12 | :94 | K-Q15 | #282 (:278) |
| COMP-13 | :96 | K-Q17 | #42 (:46) |
| COMP-14 | :86 | K-Q7 | #131 (:132) |
| COMP-15 | :101 | K-Q22 | #158 (:152) |
| COMP-16 | :108 | K-Q29 | #227 (:223), #236 (:232) |
| COMP-17 | :110; §6 :131-140 | K-Q31 | #4 (:8), #41 (:45), #54 (:58), #73 change 5 (:77), #101 (:105), #108 (a) (:112) |
| COMP-18 | :90 | K-Q11 | #257 (:253), #259 (:255), #286 (:282), #287 (:283), #288 (:284), #306 (:302), #307 (:303) |
| COMP-19 | :89, :83 | K-Q10 + K-Q4 | #271 (:267) + #273 (:269), #277 (:273), #280 (:276), #281 (:277), #284 (:280), #304 (:300), #309 (:305); #129 (:130) |

### HPSM-POC (lane table `2026-10-12_hpsmpoc_lanes_1919.md`)
| Pack | Lane-table row(s) | Ticket / row ids |
|---|---|---|
| POC-1 | :64, :237 | CI `api` job timeout (`.github/workflows/ci.yml:35`); run 38191901218 |
| POC-2 | :165 | HPSMPOC-224 (F/K) |
| POC-3 | :239 | BACKLOG :47 (HSTS) |
| POC-4 | :238; :146 | BACKLOG :40 = HPSMPOC-218 (braces, C-44 exception) |
| POC-5 | :244 | B225 MN-3 / B227 (c) (F-3) |
| POC-6 | :241 | BACKLOG :165 (B220 N-3) and B227 (a) |
| POC-7 | :251, :88 | HPSMPOC-227 on-demand CI job |
| POC-8 | :250, :87 | HPSMPOC-226 N-3, N-9 (B174 STATUS :194-195, :205) |
| POC-9 | :240 | BACKLOG :63 |
| POC-10 | :243 | BACKLOG :168 (B220 N-4) |
| POC-11 | :245 | BACKLOG :181 (B220 S-N2) |
| POC-12 | :242, :249, :214-215 | B227 N-8 / B220 N-6 (409 title); HPSMPOC-228 N-7 (B176 STATUS :156-159); BACKLOG :96 and :76 (B231 reset words; proposed live sentence at B231 brief :139) |
