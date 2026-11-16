Docs only: `docs/ENGINE.md` and `docs/API.md`. No code, contract, setting or customer-facing word changes.

- **ENGINE.md (MPSCALC-390):** row X-33 states which lines reach the INVALID MARGIN check (not Included, no sell override, no catalogue sell; a numeric cost with no percent answers MARKUP NOT SET first). Row X-46 states that the importer adds a panel option only for a device the catalogue map does not already pair with that panel.
- **API.md, Validate (MPSCALC-394):** how source version ids are compared (case of A-Z and a-z, canonically equal Latin accent spellings) and what stays a different id; the refusal is the existing `DUPLICATE_SOURCE_VERSION_ID` issue.
- **API.md, template store (MPSCALC-371):** a write is refused (503 `TEMPLATE_UNAVAILABLE`) when the file's event count is lower; which requests re-read the file under the lock and which never reach the store; a stray copy left by a kill is never loaded or deleted, while a write that fails without a kill removes its own temporary file.
- **API.md, input range (MPSCALC-195):** names the two fields refused below their own lower bound (`opportunityDeviceCount`, 400 `INPUT_OUT_OF_RANGE`; a purchase line's `quantity`, 400 `BAD_REQUEST`).

Every added sentence was checked against the code line it describes. No CI job reads these two files.

Nothing is deployed by this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
