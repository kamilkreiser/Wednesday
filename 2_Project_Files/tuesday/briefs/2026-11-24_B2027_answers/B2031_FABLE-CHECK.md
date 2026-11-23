# B2031 Fable check: meeting pack v4 against "don't include questions that have already been assigned, answered or actioned"

Reviewer B2031 (Fable), for Tuesday, 2026-11-24. Read-only quick check. Nothing was changed, sent or posted.

**Verdict: v4 is fit to go after two text fixes (F1, F2). No item is wrongly kept and no open item is wrongly dropped. F1 is the one that matters: a tap of his at 10:32 is not reflected in the pack or the map.**

What was read: pack v4 (.md whole; .docx by program), his answers file (whole), pack v3 (the rows of all dropped Part 1 items and 20 Part 2 rows), ANSWERS-MAP section 4 (whole), KAMIL-ACTIONS and HP-ASKS-TO-SEND (whole), JIRA-DRAFTS (ticket headings T-01 to T-29), and Tuesday's decision store for the eight OXPd cards of today (ids, choices, times).

Not checked: the PDF; the ticket bodies; ANSWERS-MAP sections 1 to 3; whether his file's ids q1, q12, q13 were written against pack v3's numbering (the map's own caveat, section 1).

---

## F1 (fix before sending). His 10:32 tap on KD-1 is missing from v4 Q9 and from the map's Q19 row

The decision store holds card `datasec-oxpd-kd1-azure-hpsm-subscription-1124`, ruled 10:32:56, choice **b: "No, keep the agent-controllable environment"** (option detail "Tuesday re-issues the steps."). It overrides the last sentence of his q12 ("Use the same subscription as HPSM-Poc").

Two places still say the opposite:

**(a) Pack v4, Answer Q9, "The choice left".** It reads: "Your words name the Azure Marketplace route and the HPSM-POC subscription for development; they pick none of (i), (ii), (iii)."

Replace with:

> Your words name the Azure Marketplace route. For development, your tap of 10:32 keeps the agent-controllable environment, not HPSM-POC's subscription ("b — No, keep the agent-controllable environment"). Neither picks one of (i), (ii), (iii). The choice left: (i), (ii) or (iii). By Tuesday's reading your words point to (i) or (iii).

**(b) ANSWERS-MAP section 4, row Q19.** It reads: "actioned: your q12 names the HPSM-POC subscription for development, carded KD-1 (reading)".

Replace with:

> answered by your tap of 10:32 on KD-1: "b — No, keep the agent-controllable environment"; test hosts in Azure go there, with the cost on a card first (reading)

The drop of Q19 itself stands (it is carded and ruled). KAMIL-ACTIONS KD-1 also lacks a RULED line for this tap; that file is outside this check, noted for Tuesday.

## F2 (small). v4 Q14, option (b), is garbled by the renumbering

It reads: "(b) Wait until Q14 of pack v3 (answered) to Q13 are settled."

Replace with:

> (b) Wait until Q11 to Q13 are settled (the tool itself is chosen: your q14).

---

## Check 1: is anything in v4 already answered, ticketed, carded or in H1 to H8?

No item is wrongly kept. All 48 were checked against his file, the eight taps, T-01 to T-29, KA-1 to KA-5, KD-1 to KD-3 and H1 to H8.

Six kept items have words of his or a card. Each is a defensible keep:

| v4 id (v3 id) | What exists | Why the keep stands |
|---|---|---|
| Q1 (Q1) | his q1: "Steve M ... will be in charge of testing" | names an owner, picks none of (a), (b), (c) |
| Q9 (Q12) | his q12, and the 10:32 tap | picks none of (i), (ii), (iii); fix F1 |
| Q10 (Q13) | his q13: "phase 1 needs to be a fully operational build" | names no packaging. His q12 ("through the Azure marketplace") points to (b); optional addition below |
| Q26 (Q32) | his q32: "left for kickoff" | he left it for tonight |
| W2 (W15) | his w15 | says where reports go, not Secure-only or all three |
| W6 (W29) | carded KA-3 | his tap of 10:35 chose "a: Take it in tonight's meeting" |

Optional, for Q10's "The choice left" (not required): add "By Tuesday's reading your q12 (\"through the Azure marketplace\") points to (b)."

Risk to say out loud: he may read Q1, Q9 and Q10 as already answered. The pack shows his words under each and says what is left, which is the honest form. No change proposed.

Not ticketed, checked by count: W14, W25 and W52 of pack v3 (v4 W1, W3 to W5, W7) have no line in his file and no ticket in JIRA-DRAFTS (0 mentions; positive control "T-01" found).

## Check 2: was anything still open dropped?

No. The five dropped on the author's own reading:

| v3 id | Verdict | Note |
|---|---|---|
| Q19 | drop stands | reason text is wrong; fix F1 (b) |
| Q35 | drop stands | his q34 ("Versions prior to OXPd 2 can be tested now") and the 10:19 tap together confirm the order. Better reason text: "answered in effect by your q34 and your tap of 10:19 (reading)" |
| Q36 | drop stands | owner is him (q34, KA-1); his tap of 10:36 on KA-1: "a: I'll send H5 and H3 now". No date exists, and H3 asks HP for it |
| Q40 | drop stands, marginal | a question to him about what HP said, not strictly answered. H1 item 2 and H3 ask HP for the signing route and dates in writing, and default (a) holds |
| Q41 | drop stands | H1's bracket "[When and how HP told us ...]" makes him state it when he sends |

Others sampled, all correctly dropped (20): S1 to S6, Q2, Q3, Q6, Q14, Q22, Q34, Q39, W5, W12, W13, W18, W44, W47, W50. Also W41 to W43: his tap of 10:35 on KA-5 was "b: Steve M's: ticket them", and T-27 to T-29 exist.

The counts hold: 66 left out (31 answered, 31 ticketed, 2 actioned, 2 sent to HP), 46 v3 items kept as 48 v4 items (W25 split in three). Counted by hand from section 4.

One open point that is in neither pack nor card, for Tuesday: the test tenant user with Authenticator (v3 W7, C-76). KAMIL-ACTIONS lists it as "already open and on you" but it has no card today. It is an action, not a meeting question, so it does not belong in v4.

Tap times in the map and pack differ from the store by a minute or two (map "10:34" for KA-5, store 10:35:06; HP-ASKS "10:33" and "10:35", store 10:35:12 and 10:36:35). Cosmetic.

## Check 3: one question each, with an answer box in the .docx

Pass. By program: 48 content controls, 48 unique ids, tags ans_Q1 to ans_Q41 and ans_W1 to ans_W7, none locked, and every item row holds one.

Each item is one question, with two that are compound in form and acceptable:
- Q25 asks approval of six deviations in one box (same as v3; "strike any by number" keeps it one decision).
- W6's "question left" is a conditional pair (does a runbook exist; if not, is the "format" advice current).

## Check 4: secret values

Pass. No password, key, token, GUID or long encoded string in the .md or the .docx text (pattern scan by program). The only address is kamil@datasec-rd.com, inside his own quoted words; it is an account name, not a secret.
