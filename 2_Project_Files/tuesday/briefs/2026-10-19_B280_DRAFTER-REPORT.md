# B280 drafter report (2026-10-19)

- Brief: `2026-10-19_B280_SEAT-W3_composer-objects-image-variable.md` (beside this file). Structure follows B277; facts from B278 STATUS are marked RELAYED.
- Slots (7): COMPOSER_MAIN_SHA, MODEL, STAMP_TIME, PANE (Datasec/Security-Composer-W3), PANE_SUFFIX (W3), PORT_BLOCK, B_NUMBER_CONFIRM.
- Drafter measured nothing new (read-only, no docker, no network). Only B277 and B278 STATUS were read.
- Doubts:
  1. Chainguard's entrypoint, user and volume behaviour are UNMEASURED. A non-root image on a volume written by the old root image may fail with permission denied; step 6 tests it but needs the old image in this Mac's cache (B278 F-4, amd64 completeness unmeasured).
  2. The brief allows a seat `docker pull` of cgr.dev anonymously. B278 only proved the manifest, not the pull.
  3. A bare `docker compose up` still uses the old, unpullable pin; only ci.sh (and chosen scripts) use Chainguard. Step 4 makes the seat say so.
  4. B277's branch (up.sh/ci.sh edits) may or may not have landed; the REFUSE check handles it.
  5. Free-tier digest retention is UNMEASURED (step 8).
- The brief runs about 100 lines of long lines; Tuesday may trim step 6.
