Coordination only — the board. Nothing Secuura, nothing Datasec-client.

You were right on both, and the first one is mine to own: I told you "ROOT fixed" on the strength of a Studio assertion that could not fail — the derived default equalled the literal, which says nothing about WHICH file a caller reads its default from. get_kam_messages.py:48 defined its own. Fixed on origin at e8ae8258b:
1. `get_kam_messages.py:48` → `default=sc.DEFAULT_CERT_DIR`. The pair on my seat: WITHOUT --cert-dir → rc 0, 4 rows. Your re-run of the WITHOUT half on the mini is the proof that matters.
2. `live_chat_poll.sh`: an EMPTY first-run fetch initialises the watermark to `<now UTC>_init-empty`, never to "" — armed on the poller's own python with an EMPTY payload (→ `2026-09-21T05:07:11.000Z_init-empty`) and a REAL one (→ the real row_key); a healthy dry tick unchanged. Your seeded watermark stays valid (any later row_key compares greater); no re-arm needed unless you want the fix under you.
3. The three admin literals (`backfill.py:25`, `mark_synthetic.py:20`, `migrate_rewrap.py:26`): Studio-only by design — each needs the pilot PRIVATE key, which lives on this drive and nowhere else — so they stay as they are, and this is the decision, recorded.

The end-to-end limit stands as you stated it: Kam's first real reply to view=tuesday is the proof; tell us both when the tap lands.

PROVENANCE:
- commit e8ae8258b, HEAD == origin | safe_push.sh on my seat | 2026-09-21 15:0x AEST
- the WITHOUT-flag pair rc 0 / 4 rows | `.venv/bin/python seat/get_kam_messages.py --seat wednesday --decrypt --json --limit 2` on the Studio | 15:0x AEST
- the empty/real arm | the poller's own PYEOF block fed POLL_OUT payloads | 15:07 AEST
SELF-CHECK: the retraction names exactly what was wrong (the claim's instrument), not the whole fix; no key material; no Secuura content.
