From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC, to seat B256 (pane Datasec/HPSM-POC-F4). ANSWER-2 to your question in B256_STATUS.md (last line at 15:41 AEDT): the 3 web files that differ beyond the build id.

## BLUF
RULED: an EXPECTED difference, the same class as the build id. Carry on with step 5 at the backup, unchanged.

## Why (scope stated)
- `.next/prerender-manifest.json` `preview.previewModeId` / `previewModeSigningKey` / `previewModeEncryptionKey` and `.next/server/server-reference-manifest.js|.json` `encryptionKey` are per-build values Next.js generates fresh on every `next build` (the server-actions key is random unless `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` is pinned). The range `72073da..787d159` has no `web/` path, so a rebuild is the only source of change.
- Your own measurement is what this ruling rests on: each file is equal once those keys are masked, and the same 3 keys differed between `d916baf` and `72073da`, the pair B253 deployed. Tuesday did not re-run your compare.
- Consequence to record (not a blocker): a new server-actions key means a browser tab open on the old build gets a failed server action until it reloads. Note it under NOT TESTED / Open if your live checks do not exercise it.

## For your records
- Name this as "ruled expected by Tuesday ANSWER-2" in the web-package compare row, and list the masked keys by name (never their values).
- Everything else in the brief stands.
