---
date: 2026-09-10
type: correction
source: two instances in one hour, both costing Kam, on the morning after a lesson that named the same gap
status: live
tier: W
---

# A message from Kam is a RECORD, not a string — reading `.text` and ignoring `view` and `attachments` is not reading the message

**The operative case, so the headline matches it:** a message from Kam has arrived on the panel and
Wednesday is about to act on it. **Before reading a word of it, read who it was addressed to and
what came with it.** A panel message carries `text`, `view` (which tab he typed it into) and
`attachments` (the files he sent with it). **Wednesday has been reading exactly one of those three
and treating it as the message.**

## The two, one hour apart, both to the principal

**1. His 08:58 message carried `view: "tuesday"`.** It said *"You will need to set up connection to
the NAS once you're ready. Let me know, and I'll enter the password."* Wednesday read `.text`,
answered it as its own, apologised for a late receipt, and promised to come back about the
password — **for an instruction typed at the other coordinator's tab.** Retracted at 09:0x.

**2. His 09:09 message was the four characters `now?` — with the document attached.** He had been
asked to re-send Peter's PR triage; he attached `pr-triage-2026-09-09.md`, 9,759 bytes, and typed
"now?" to ask whether the box was fixed. **Wednesday read `.text`, saw four characters, and told
him a four-character message "cannot tell me either way".** He then exported the whole thing to PDF
and sent it again. **The document had been sitting on the message the entire time.**

## Why this is its own lesson and not another representations row

The representations family says *I read representations and they read sources*. **This is
narrower and worse: the source was in my hand and I read one field of it.** Nothing was stale,
nothing was second-hand, no instrument failed. The record was complete and correct **both times**,
and the consumer took a substring.

**And it is a REGRESSION against a lesson written the previous day.**
[[2026-09-09_confirm-receipt-on-the-chat-board]] measured the `view` field, found it *"correct —
47 messages on 2026-09-09, 36 tagged wednesday, 11 tagged tuesday"*, and wrote the sentence
verbatim: ***"Nothing reads it. The routing data existed and was right; the consumer was
missing."*** **Twenty-four hours later the consumer was still missing, because that lesson
diagnosed the gap and built nothing.** That is the whole diagnosis: a lesson that names a missing
mechanism and does not build it will be re-earned at full price.

## How to apply

1. **Never read Kam's chat store with an ad-hoc `python3 -c` that prints `.text`.** Use
   `2_Project_Files/tools/kam_msgs.sh`, which prints `view` and `attachments` beside every message
   and shouts on both. Built and red-proofed the same session: it flags the exact 08:58 message
   that caused this, and stays silent on a clean one.
2. **`view` is an ADDRESSEE field and it decides whether the message is mine at all.** A message
   tagged `tuesday` is routed to her verbatim, never answered. **Answering another seat's mail is
   the cross-client failure shape in its mildest costume — and the mild costume is how the habit
   forms.**
3. **A short message with an attachment is a LONG message.** Length of `.text` says nothing about
   the size of what arrived. Ask what came with it before concluding a message is uninformative.
4. **Generalise past this store, because the class is not about chat:** an email has headers and
   parts; a webhook has a body and a signature; a ticket has a description, labels and an assignee;
   a commit has a message and a diff. **Wherever a record has fields, "I read it" means the record,
   and the field you skipped is usually the one carrying the authority or the payload.**
5. **When a lesson names a missing consumer, the consumer is the deliverable.** Writing down that
   nothing reads a field is not a fix; it is a description of the defect with a date on it
   ([[2026-08-07_a-promise-is-not-a-mechanism]]).

## What went right, kept so the record is honest

Both were caught in minutes, both were owned to Kam leading with them, and the second was caught
only because he worked around it — **which is the expensive kind of catch and the one to count.**
The retraction on the NAS message was made before he acted on it.

**Family:** [[2026-09-09_confirm-receipt-on-the-chat-board]] (**the file that measured this exact
gap the day before and built nothing — this is its unpaid half**) ·
[[2026-08-14_i-read-representations-they-read-sources]] (the parent; here the source was in hand) ·
[[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (**a single field is a frame, and an
unstated frame is invisible to the reader — including when the reader is me**) ·
[[2026-08-13_shared-bus-tag-filter-or-leak]] (filter on the RECIPIENT, not only the class — this is
that rule pointed at Kam's own channel) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]].
