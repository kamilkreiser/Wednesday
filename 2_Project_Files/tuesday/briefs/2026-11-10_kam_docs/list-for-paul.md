# Open questions for Paul (HPSM-POC)

**For Kam: check these three things before you send (then delete this box)**
- Item 6: the 8 October send covered nine questions. Whether the longer lab list (device simulator, firmware feed, FTA back end) also went out is not on record. If it did, cut the extra line in item 6.
- Item 15: it is not on record whether your HP contractor account is active again. If it is, delete item 15.
- Three tickets are left out because they no longer wait on HP or Paul: HPSMPOC-83, -163 and -164. REPORT.md says why for each.

---

Hi Paul,

This is everything on our side that is waiting on HP, on you, or on an HP tool. There is one line per open question, with what we need back. The next-phase items at the end are for your information only. Nothing there needs an answer now.

## A. Questions for HP

1. **HPSMPOC-82, HPSMPOC-181**: Security Manager API. Can HP send the current API and SDK reference (endpoints, data formats, how sign-in works, which parts are stable), and give us access to the wiki where it is kept? Can HP also confirm that partners are supported in using the API?
   *We need:* the documents, wiki access, and a yes or no on support.
2. **HPSMPOC-181**: Devices in our Security Manager. Our copy (3.16, 10-device licence) works, but it has no supported devices. Can HP give us a device simulator or demo database, or instructions for creating virtual printers? Failing that, can we have clearance to connect one or two real HP Enterprise printers?
   *We need:* one of those three options, and what Security Manager needs before it treats a device as supported.
3. **HPSMPOC-86, HPSMPOC-181, HPSMPOC-166**: Fleet Threat Assessment. Can we have the latest demo build and the steps to switch it on inside our Security Manager? We would also like the promo video and the demo assets, and the December route for partners to buy Security Manager with Fleet Threat Assessment.
   *We need:* the build and setup steps, the video and assets, and the purchase route.
4. **HPSMPOC-94, HPSMPOC-181**: Expert remediation guidance. Who owns HP's expert remediation knowledge base? Can we have a session with that team and a named expert to line our guidance up with theirs? Can Fleet Threat Assessment draw on that content? Please also send the spreadsheet of syslog events it supports.
   *We need:* an owner, a session date, a contact, and the spreadsheet.
5. **HPSMPOC-85**: Firmware Security Service. Is it included in our not-for-resale Security Manager licence? What does Security Manager send to HP when it runs? Are there terms to accept?
   *We need:* yes or no on the licence, a list of what is sent, and any terms.
6. **HPSMPOC-241**: The four Fleet Threat Assessment questions still open from 16 October:
   (a) Do the Alerts and Devices exports include every matching row, and can the Alerts export carry the reference, status, rule ID and MITRE ID?
   (b) Do real PDF reports carry a "Confidential" footer, and may a customer share them with a partner's tool?
   (c) For SIEM forwarding, which certificates does it trust, can we add a private CA, and can it present a client certificate?
   (d) Can the Devices export include serial number and firmware?
   Also, if not already sent: the lab questions on device simulators, firmware data sources and the Fleet Threat Assessment back end.
   *We need:* an answer to each of (a) to (d).
7. **HPSMPOC-167**: Partner deck. Can HP send the current generic partner deck, without a partner's branding? Does it replace deck v3?
   *We need:* the deck, and a yes or no on whether it replaces v3.
8. **HPSMPOC-162**: AI security at the printer. Can HP share what it has done to secure AI at the printer, and the draft HP paper on agentic AI in enterprise printing? Until we have them, the Playbook says only what the customer's own answers support.
   *We need:* the facts HP is happy for us to state, with their source, and the paper if it can be shared.
9. **HPSMPOC-97**: Services SOW template. HP offered a template services SOW from its services team on 29 September. Is it still available?
   *We need:* the template, or a no.
10. **HPSMPOC-84**: Control Hub. We now treat Control Hub as reference material only, not as something we integrate with. Is that right? If so, we will close our access request.
    *We need:* yes, or tell us why we still need access.
11. **HPSMPOC-166**: Fleet Threat Assessment messaging. HP was correcting its wording so that it no longer claims automatic remediation or policy-drift detection. Is the corrected wording published?
    *We need:* the corrected wording or a link, so the Playbook text matches it.

## B. Questions for Paul

12. **HPSMPOC-242**: Showcase feedback. Can you send your detailed notes from the 7 October showcase and your follow-up testing?
    *We need:* your notes, in any form, or "no further points".
13. **HPSMPOC-165**: First "good" consulting package. The offer sheets and service names stay as placeholders until HP's review. When can we settle the first package with you (the list of services and what each tier includes, with no prices)?
    *We need:* a date, or your first draft.
14. **HPSMPOC-168**: Customer fit. On 1 October the stronger-fit fleet size was noted as both "about 250" and "about 2,500" devices. Which is it? And are healthcare, financial services and the public sector the right three sectors to name?
    *We need:* one number, and a yes or a correction on the sectors.
15. **HPSMPOC-166**: My HP contractor account. It was frozen, which blocks my HP sign-ins. Has it been reactivated?
    *We need:* yes, or who to follow up with.

## C. Waiting on an HP tool (no separate question; these start when items 1, 2 and 5 are answered)

16. **HPSMPOC-191**: Connecting our Security Manager to the Playbook. This needs devices (item 2) and confirmation that the API is supported (item 1).
17. **HPSMPOC-220**: Importing Security Manager's device list and results as evidence for the assessment. This needs devices in Security Manager (item 2).
18. **HPSMPOC-240**: Re-testing the Firmware Security Service on our copy. This needs one supported HP device (item 2) and the licence answer (item 5).

## D. Next phase (for information only; not built in this phase)

19. **HPSMPOC-92**: Leading into more sophisticated engagements: beyond print, importing Security Manager and Fleet Threat Assessment exports, and a deeper AI assessment.
20. **HPSMPOC-96**: A voice or conversational way to take the assessment.
21. **HPSMPOC-259**: Designing for HP's tool answers. Integration with HP tools is designed now and built in the next phase. The answers to item 6 feed into it.

Thanks,
Kam
