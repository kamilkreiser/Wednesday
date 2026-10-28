@stuart.jamieson answering your question on the kintsugi provenance rows for KS-1717.

**BLUF:** neither of your two uploads has an `anchor` row on kintsugi. Each upload wrote `create` + `create:connector`; the only `anchor` row in that window is your re-anchor of `5008820d`. Rows 91-95 below, read-only from kintsugi's `action_provenance` on 28 Oct, plus the five rows that arrived after this morning's kintsugi deploy (10:07 AEDT) from dev-ps traffic.

**Rows 91-95** (all actor `connector:api-key`), oldest first:

| time (AEDT) | time (UTC) | action | document_id |
|---|---|---|---|
| 27 Oct 13:22:55 | 27 Oct 02:22:55 | create | bfeb86da-b7e4-450a-b2c2-3189a1536949 |
| 27 Oct 13:22:55 | 27 Oct 02:22:55 | create:connector | bfeb86da-b7e4-450a-b2c2-3189a1536949 |
| 27 Oct 20:17:56 | 27 Oct 09:17:56 | anchor | 5008820d-82c7-43fd-971c-bc4d99729a20 |
| 27 Oct 20:21:23 | 27 Oct 09:21:23 | create | e8ffc168-c0cf-4ad3-9e3a-394d3e398593 |
| 27 Oct 20:21:23 | 27 Oct 09:21:23 | create:connector | e8ffc168-c0cf-4ad3-9e3a-394d3e398593 |

**Since then (rows 96-100, after the deploy):**

| time (AEDT) | time (UTC) | action | document_id |
|---|---|---|---|
| 28 Oct 12:01:28 | 28 Oct 01:01:28 | version:sign-cert | e8ffc168-c0cf-4ad3-9e3a-394d3e398593 |
| 28 Oct 12:01:28 | 28 Oct 01:01:28 | create:connector | doc-1793149288396-3347e6ad |
| 28 Oct 12:01:28 | 28 Oct 01:01:28 | anchor | doc-1793149288396-3347e6ad |
| 28 Oct 12:57:15 | 28 Oct 01:57:15 | anchor | c03605de-3a3c-4221-85c2-403cad765fc4 |
| 28 Oct 12:57:15 | 28 Oct 01:57:15 | certify | c03605de-3a3c-4221-85c2-403cad765fc4 |

The two anchors since the deploy each have a matching confirmed, non-simulated record in `anchor_store`.

These are the rows as recorded; I have not drawn a KS-1717 conclusion from them.
