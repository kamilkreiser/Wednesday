KS-1321 originate ks1293/ks978 cell: the dedicated-route verb check matches SUBSTRINGS, so the ordinary word "version" reds it
state In Progress

## BLUF

`DESCRIPTIONPOINTSATSOURCE` (in `ks978-published-contract-organizationuuid.test.ts`, landed by #1252) forbids a dedicated-route verb appearing in the published `LifecycleEventRequest.action` description by **substring** match: `dedicatedVerbs.filter((verb) => description.includes(verb))`.

Several dedicated-route verbs are ordinary English words — `version`**,** `anchor`**,** `verify`. So a description containing "a new version of this list is not kept here" reds the cell, although it names no route.

**Confirmed by the tier-2 gate on #1252** (report `2026-09-26-batch1249-t2b`, finding **N-1252-a**, PROBED): the probe received `["version"]`. Polish, and the **safe direction** — the check is too wide, never too narrow, so it cannot miss a real relabel; it can only refuse innocent prose.

## Why it is worth fixing rather than leaving

The whole point of KS-1275 was to stop the published description being load-bearing prose that drifts. A cell that reds on an ordinary word invites the next editor to work around the cell rather than fix the prose — which is how the pin stops being trusted.

## Fix shape (the gate's, verbatim)

A word-boundary or route-token match — `/(^|[^a-z-])verb([^a-z-]|$)/` — against a `/`-delimited or back-quoted form, rather than a bare `includes`.

## Done when

- [ ] a description containing "a new version" stays GREEN
- [ ] a description containing a route token (e.g. a back-quoted or `/`-delimited `version`) still REDS
- [ ] both arms present as cells, so the widening cannot silently return

## Board search before filing

Literal match over 1,310 issues incl. archived and 3,687 comments: `DESCRIPTIONPOINTSATSOURCE` → 1 hit, KS-1275's own merge comment (this finding, recorded there); `dedicatedVerbs` → 0; `description.includes` → 0. **0 open hits with a home.** Controls: `withTenant` → 12, `ZZZNOSUCHSYMBOLZZZ` → 0.

Raised from the #1252 merge (develop `49bc69abae1528d8da76018aaa68b04749e5d93b`).
