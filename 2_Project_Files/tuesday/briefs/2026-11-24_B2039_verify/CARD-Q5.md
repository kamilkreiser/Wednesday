# Q-5: does a viewer keep the Data Sources tab's list? (RD-1021)

**BLUF.** After this change, a viewer who opens the Data Sources tab on the admin page sees an error box that reads `HTTP 403` instead of the list of sources and their live connection status. Administrators see the tab as before. The first-run wizard is unchanged.

**Who decided.** Refusing the viewer here is the coordinator's (Tuesday's) default, not your choice. It follows the ticket's own proposal and the form already used on the four sibling routes. Your own ruling on record is C-311 (2026-11-20). It covers only RD-1011's two reads, describe-table and discover-tables, which you kept administrator-only.

**Why the list call is refused.** For every enabled source, `GET /api/setup/data-sources` decrypts the stored sign-in details and runs a live connection test with them. Before this change, any signed-in viewer could trigger that.

**Where the 403 shows.** In `static/js/admin.js`, `loadDataSources()` calls `fetch('/api/setup/data-sources')` at line 182. Line 183, `if (!r.ok) throw new Error('HTTP ' + r.status);`, turns the 403 into an error. Lines 193-194 put the text `HTTP 403` into the tab's `sources-error` box. This was read from the source, not seen in a browser.

**Worth knowing.** A viewer can still read the list of sources without a test through `GET /api/data-sources`. It returns names, workspace ids, auth modes, tenant ids and client ids, with the secret masked, and it makes no connection. The admin tab does not use that route today.

**Options**
- **a. Keep refusing (default; what lands).** A viewer gets 403 on the tab, the same as on the neighbouring administrator tabs.
- **b. A viewer-safe list without the connection test, as a follow-up ticket.** The tab would show viewers the sources without a live status. One way is to serve the tab from the non-testing list for non-administrators. Reversing just the refusal means changing three lines in the setup handler, two inventory rows and three test cells.
- **c. Something else.** Tell us what.
