# HPSM-POC class C word pack (2026-10-22)

Read-only draft for the product owner. Code read at `origin/main` = `a93b926ac8534bd0c9ae67fe63229ede46c39fd4` (`git ls-remote origin main`, same as the local `origin/main` ref). Jira read today with comments sorted newest-first. Paths are under `2_Project_Files/` unless they start `1_Project_Definition/`.

## BLUF

- **11 small rulings on 6 tickets.** 148, 177, 178, 187, 204 are one ruling each. 310 is six rulings (items 3 to 8), so 6 + 5 = 11 (item 5 is one of the six).
- **Nothing is dropped.** No ruling exists for any of the six: `clarifications_register.md` has no line for these tickets, and `CLARIFICATIONS.md` has no entry for them (grep for each ticket number and for the topic words: 0 hits; positive control below).
- **No ticket leaves the pack for needing HP.** One option does: 310 item 5, option 5c (re-issue the HP deck text in Australian spelling). It is marked and not recommended.
- **Recommended set, one line:** `148 b · 177 a · 178 a · 187 a · 204 b · 310: 3b 4a 5a 6a 7a 8a`.
- **How to rule from a phone:** reply with the line above, or change any letter. Every option below shows the exact words.
- **One correction to an earlier proposal:** the filed words for 148 ("This plan was discarded in another session") read as false on the screen that did the discarding. Option 148 b replaces them.

---

## HPSMPOC-148 (C-2): the discard screen's words

**The one decision.** What should the notice say when someone discards their plan and a newer plan from another session is then shown under it?

**Words today.** `web/src/components/partner/ActionPlanScreen.tsx:95`:
`<Alert tone="success" title="The plan was discarded" live="status">`, body `Your readiness results are kept.` and, when a newer plan is shown, a button `Make a plan from your results` (`:98`).
The problem (ticket, gate B87): the notice sits above another session's five rows, so it reads as if those rows were discarded.

**Already done on this ticket** (so it is not asked again): C-3 (`At most 1 follow-up can be open at once; withdraw one first.`, approved) and N-9 (the mock's 404 detail, deployed). Only C-2 is open (Jira comment 2026-10-21 13:58).

**Options.**
- **a. Use the filed words.** Title `This plan was discarded in another session`. (From `1_Project_Definition/Briefs/2026-10-13_B241_STATUS.md:92`, marked PROPOSED, never approved.) Weakness: on the screen that did the discarding it says something untrue.
- **b. Say what is on screen.** When a newer plan is shown: title `Your plan was discarded. A newer plan is shown below.` Body unchanged. When no plan is shown the title stays `The plan was discarded`.
- **c. Leave it.** Record "leave as is" and close the item.

**Recommendation: b.** It is true on every screen and tells the reader why other rows are there.

**Builder after each option.**
- a: `ActionPlanScreen.tsx:95` (one string), `ActionPlanScreen.test.tsx:165,184`, the two e2e specs that look for `The plan was discarded` (`playbook-partner.spec.ts`, `playbook-action-plan-live-api.spec.ts`). Small.
- b: the same files, plus one branch on `loaded` at `:95`, and a new test row for the "newer plan shown" case. Small.
- c: a CLARIFICATIONS entry and a Jira comment. No code.

**Needs HP or a human?** No.

---

## HPSMPOC-177: invisible characters in the feedback comment

**The one decision.** Should the feedback comment refuse the same hidden characters that follow-up notes already refuse (the ruling C-36 C), and what should the refusal say?

**What is refused today.** Control characters and text-direction overrides only. A comment of visible text plus a byte-order mark (U+FEFF) or a TAG character (U+E0000 to U+E007F) is accepted and stored. The set C-36 C adds: U+E0000 to E007F, U+2028, U+2029, U+FEFF, U+FFF9 to FFFC, U+206A to 206F. Kept allowed: zero-width joiner and non-joiner, no-break space, soft hyphen, U+200B, U+2060 to 2064.

**Words today.** `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackEndpoints.cs:240-241` (the ticket says `:119`; the code has moved):
`"The comment holds control or text-direction characters."` (code `feedback.comment-invalid`). The web shows the API's first message as is (`web/src/components/feedback/feedbackApi.ts:58`).
The same rule for a follow-up note says (`api/src/HpsmPoc.Modules.Assessment/Endpoints/Requests.cs:212`): `The note holds a hidden control or text-direction character (often from copying and pasting); type it again as plain text.`

**Options.**
- **a. Refuse the same set, with the matching sentence.** `The comment holds a hidden control or text-direction character (often from copying and pasting); type it again as plain text.`
- **b. Refuse the same set, keep today's sentence.** `The comment holds control or text-direction characters.` Weakness: the sentence no longer names what was found.
- **c. Leave it.** Record that feedback comments may hold these characters.

**Recommendation: a.** One rule and one sentence across notes and comments; the reviewer is told how to fix it.

**Builder after each option.**
- a: `FeedbackEndpoints.cs:240` (use the same set, from `api/tests/HpsmPoc.Api.Tests/FollowUp/invisible-characters.json`), the message at `:241`, rows in `GateRound2Tests.cs:288` / `FeedbackApiTests.cs:106` for each added character, the contract note at `openapi.yaml:1922`. Small. Tier 1 or 2 is the seat's call: it changes what an API accepts.
- b: the same without the message change. Small.
- c: a CLARIFICATIONS entry. No code.

**Needs HP or a human?** No.

---

## HPSMPOC-178: invisible characters in a customer name

**The one decision.** Should a customer name refuse hidden and text-direction characters, as notes do?

**Words today.** There is no refusal. The name is checked only for length 1 to 120 (`api/src/HpsmPoc.Modules.Assessment/Endpoints/Requests.cs:137`, message `name takes 1 to 120 characters.`) and not blank (`CustomerEndpoints.cs:77,196`, `name is blank.`). A name with U+202E, a TAG character, a byte-order mark or BEL is stored. The client sees it as `For <customer name>` (`web/src/components/followup/ClientFollowUpScreen.tsx:151`).

**Options.**
- **a. Refuse the C-36 C set plus control and text-direction characters, on create and rename.** New code `customer.name-invalid`, field `name`, message: `The name holds a hidden control or text-direction character (often from copying and pasting); type it again as plain text.`
- **b. Refuse only the characters that can disguise a name** (control characters and text-direction overrides and isolates, U+202A to 202E and U+2066 to 2069). Same message. Hidden but harmless characters stay allowed.
- **c. Leave it.** Record the risk (low to medium; the partner types the name, so the risk is a paste).

**Recommendation: a.** The name is printed for a client, and one set across notes, comments and names is one rule to explain.

**Builder after each option.**
- a: `Requests.cs:137` (`Shape.Customer`) with `FollowUpShape.HasControl` (`FollowUpModels.cs:193`), checked before any trim; both endpoints in `CustomerEndpoints.cs`; the web mock's customer create and rename in step (file not located, UNMEASURED); a contract note; tests over every refused scalar like `InvisibleCharacterTests.cs`. Medium (API plus mock plus contract).
- b: the same with a smaller set. Medium.
- c: a CLARIFICATIONS entry. No code.

**Open after this ruling (not part of it).** The ticket lists other free-text fields never probed (industry, evidence text, finding notes, plan titles, review notes). a or b could be extended to them later as one rule; that is a separate question.

**Needs HP or a human?** No.

---

## HPSMPOC-187 (second half): the executive-summary template text

**The one decision.** When several priority findings share one action, how should the offline (template) summary say it?

**Status of the first half.** Built: the customer's name replaces the first "the organisation" when the summary is drawn (ruling C-48, PR #95). The opening line itself is unchanged: `Providers.cs:66-67` `The assessment of the organisation produced an overall current score of {score}…`.

**Words today.** `api/src/HpsmPoc.Modules.Reporting/Narrative/Providers.cs:75` writes one paragraph per priority finding (up to five), built at `:94-101`:
`{Title}. This is a {severity}-severity finding. Recommended action ({bucket}): {action}.`
With the DRAFT content, five findings carry the same action, so the same action sentence appears five times on the first page of the executive PDF. The text sits under the rule "report-content: keep the defaults" (C-13), so new words need the product owner.

**Options.**
- **a. Group findings that share an action.** One paragraph per shared action: `{N} findings share this action: {Title 1}; {Title 2}; {Title 3}. The highest severity among them is {severity}. Recommended action ({bucket}): {action}.` A finding with its own action keeps today's sentence.
- **b. Keep one paragraph each; shorten repeats.** After the first, the action reads `Recommended action ({bucket}): the same as above.`
- **c. Leave it** until real approved content arrives. The repeat comes from DRAFT content, where actions were copied.

**Recommendation: a.** The showcase uses DRAFT content and this is the first page an HP reviewer reads.

**Builder after each option.**
- a: `Providers.cs:75,94-101` (group by action, cite all the finding ids in one paragraph; the "Further priority findings" paragraph already cites several), then re-issue the golden narrative files (`api/tests/HpsmPoc.Modules.Reporting.Tests/Fixtures/b66-exec/*.base-output.json`) and the paragraph-cap row. Medium.
- b: `Providers.cs:94-101` and the same goldens. Small.
- c: a CLARIFICATIONS entry. No code.

**Needs HP or a human?** No.

---

## HPSMPOC-204: the PDF profile caption

**The one decision.** What should the caption under the Customer Profile table say, now that the organisation, staff, sites and printers rows show the record as it is now, while the answer rows show what was given at submission?

**Words today.** `api/src/HpsmPoc.Modules.Reporting/Report/ReportModelBuilder.cs:141-142`:
- submitted: `The profile as it stood when the assessment was submitted ({date}), which is the context the rules used.`
- not submitted: `The profile as it stood when the assessment was scored, which is the context the rules used.`
After a rename or a fact change this tells the reader something the table does not show.

**Options.**
- **a. The ticket's suggested sentence.** `Organisation and profile as recorded when this report was made; the rules used the answers given at submission.` (Drops the date.)
- **b. Name which rows are which, keep the date.** Submitted: `Organisation, staff, sites and printers are as recorded when this report was made. The other rows are the answers given when the assessment was submitted ({date}); the rules used those answers.` Not submitted: the same with `when the assessment was scored` in place of `when the assessment was submitted ({date})`.
- **c. Leave it.**

**Recommendation: b.** It stays true after a rename and the reader can tell which rows can change.

**Builder after each option.**
- a, b: the two strings at `ReportModelBuilder.cs:141-142`; no test names these words (only that file holds them at main), so add one test row for each caption; check the PDF golden outline (page count) still holds. Small. Changes report bytes, so the seat sets the tier.
- c: a CLARIFICATIONS entry. No code.

**Needs HP or a human?** No.

---

## HPSMPOC-310: word pack items 3 to 8 (six rulings)

Items 1 and 2 (product name, spelling) were ruled and built (PR #176). The six below come from the hosted reviewer walk (1_Project_Definition/Briefs/2026-10-21_B377_STATUS.md items 13, 15, 16, 17, 18, 19). The ticket proposes no words; the options are mine.

### Item 3: times show no time zone
**The decision.** Should a time on screen say its zone?
**Words today.** `web/src/lib/dates.ts:19` `formatMoment` gives `25 Sept 2026, 7:51 pm`; also `formatTime` (`:26`), e.g. `Report issued 10 Oct 2026, 9:51 pm`.
- **3a. Leave it.**
- **3b. Add the zone name to every time**, in the reader's own zone: `10 Oct 2026, 9:51 pm AEDT`.
- **3c. Add it on the report page only.**
**Recommendation: 3b.** One format everywhere; HP reviewers may sit in other zones.
**Builder.** 3b: `dates.ts` (add the short zone name to the time options) plus every test and screenshot that asserts a time string (count not measured). Small to medium. 3c: the report component only. Small. 3a: no code.

### Item 4: "Home" in the menu, "Partner Dashboard" on the page
**The decision.** Which name should the landing page carry?
**Words today.** Menu `Home` (`web/src/components/shell/GlobalNav.tsx:27` region, `/home`); page title `Partner Dashboard` (`web/src/components/partner/PartnerDashboard.tsx:50`). The menu is shown to every role.
- **4a. Page title becomes `Home`.**
- **4b. Menu item becomes `Partner Dashboard`.**
- **4c. Leave both.**
**Recommendation: 4a.** Every role sees this page, and "Partner" is wrong for an administrator.
**Builder.** 4a: one string plus tests that look for the heading. Small. 4b: the menu entry and breadcrumbs (`ActionPlanScreen.tsx` has a `Home` crumb) plus tests. Small.
**Not part of this ruling:** the "Customers" menu item goes to `/workspace` while `/customers` shows the same list. That is a routing choice, not words. Left out.

### Item 5: US and UK spelling mixed
**The decision.** Do we change the American forms on screen?
**Words today.** On our own screens: `web/src/components/home/phase-flow.ts:21` `optimize`, `:37` `Prioritized roadmap`, `:54` `Optimize`. In the shipped playbook content, version 0.6.1 holds 18 lines with these forms (for example `Phase 3 – Monitoring & optimization`, `Prioritized security roadmap`, `Centralized visibility…`, `block unauthorized code`). These read as HP's deck wording (origin UNMEASURED; the walk's counts are relayed, not re-counted).
- **5a. Leave it and record why** (HP deck wording; our own text is already `-ise`).
- **5b. Change only the three strings in `phase-flow.ts`** to `optimise`, `Prioritised roadmap`, `Optimise`. Weakness: the home page then disagrees with the playbook pages.
- **5c. Change the playbook content too.** **Needs HP:** the deck text is theirs. Not in this pack.
**Recommendation: 5a.** 5b would create a mismatch between the home page and the playbook pages.
**Builder.** 5a: no code. 5b: `phase-flow.ts` plus tests naming the phase `Optimize`. Small. 5c: a new content version (medium) and HP's approval first.

### Item 6: "Your tools (coming later)"
**The decision.** What should the greyed placeholder say?
**Words today.** `web/src/components/home/phase-flow.ts:28` label `Your tools (coming later)`, beside `HP-backed tools`. The placeholder was the product owner's own instruction (B200, "add this as a placeholder, grey it out"); the label words were left for him to rule.
- **6a. `Your tools (planned for a later phase)`.** Says what and makes no date promise.
- **6b. `Your tools`** greyed, with no suffix.
- **6c. Leave it.**
**Recommendation: 6a.** The reviewer objected to "coming soon" text; this says it is planned and keeps the placeholder he asked for.
**Builder.** 6a/6b: one string, plus any test that names the label (not counted). Small.

### Item 7: a visitor with no link
**The decision.** What should a client see when the page is opened with no valid link?
**Words today.** Title `These questions cannot be shown` (`web/src/components/followup/ClientFollowUpScreen.tsx:83`); body `Your session has ended. Open the link again.` (`web/src/components/followup/api.ts:120`, every 401).
- **7a. `Open the link your partner sent you. If it has stopped working, ask your partner for a new one.`**
- **7b. Keep the body and add a second sentence:** `Your session has ended. Open the link your partner sent you again.`
- **7c. Leave it.**
**Recommendation: 7a.** It is right for a visitor who never had a link and for one whose link ran out.
**Builder.** 7a/7b: `api.ts` has one shared function (`followUpFailure`) used by the partner screens too, so put the new sentence in `clientFailure` (`api.ts:85`), the client-only wrapper, and keep the partner's words. Small. The missing page heading and the console 401 (B377-18) are separate fixes, not words.

### Item 8: "Customer not found"
**The decision.** What should the page for an unknown customer say?
**Words today.** `web/src/components/shell/CustomerShell.tsx:124`, under the title `Customer not found`: `The customers service does not know this customer (it may have been removed, or the demo was reset).`
- **8a. `We could not find this customer. It may have been removed, or the demo may have been reset.`**
- **8b. `This customer is not in your list. Go back to customers and choose another.`**
- **8c. Leave it.**
**Recommendation: 8a.** Same meaning in plain words; "the customers service" is internal talk.
**Builder.** One string at `CustomerShell.tsx:124` and `CustomerShell.notfound.test.tsx`. Small. The missing page heading (B377-19) is a separate fix.

**Needs HP or a human?** Only 5c. Items 3, 4, 6, 7, 8 and options 5a/5b do not.

---

## FOUND

- No existing ruling covers any of the six (register and CLARIFICATIONS checked).
- 148: only C-2 is open; C-3 and N-9 are done and deployed. The filed C-2 words read as untrue on the discarding screen.
- 177: the code moved from `:119` to `FeedbackEndpoints.cs:240-241`; the rule is unchanged.
- 178: the customer name still has no content check, only length and blank.
- 187: the first half is built (name at draw time); the repeat comes from DRAFT content.
- 204: the caption string is held in one file only.
- 310: `followUpFailure` is shared between the partner and client screens, so item 7 must be a client-only change. Item 5's US forms are HP deck wording on the content side.

## TESTED

- Read-only: Jira description and every comment for 148, 177, 178, 187, 204, 310 (newest first), and the quoted code at `a93b926…` with `git show` and `git grep` (positive controls: `Partner Dashboard` 2 hits in `PartnerDashboard.tsx`; the register `/usr/bin/grep -F 'Datasec/HPSM-POC'` returned 5 lines, none for these tickets; `CLARIFICATIONS.md` has 192 lines and a grep for "Partner Dashboard" and the six ticket numbers returned 0).
- Quoted strings were copied from `git show` output, not from memory.

## HOW

Lane plan section 4 first; each ticket re-read from Jira; code at the `ls-remote` sha; gate files `2026-10-13_B241_STATUS.md`, `2026-10-21_B377_STATUS.md` and `2026-10-21_B407_STATUS.md` read for the words they already name.

## NOT TESTED

Nothing was run: no build, no screen, no test. No option was tried in code.

## UNMEASURED

- Whether the web mock rejects a hidden character in a customer name today, and where the mock's customer create lives (178).
- The number of tests and screenshots that assert a time string (item 3), and which tests name the "Your tools" label (item 6).
- How a zone name renders for a reader outside Australia (item 3).
- Whether the real approved content repeats actions as the DRAFT content does (187).
- The origin of the American spellings (the walk's counts are relayed; only the lines at main were counted).
