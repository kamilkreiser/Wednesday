# MPS Calculator: 31 new staff-only messages in the hosted deploy (none on a customer document)

Read from the deploy seat's census at MPS main 0bb3ed12 (B1542 STATUS, 17:13). Every row is a message only staff or an Administrator can see: template and feedback-triage API errors, the quote Issues list, one contract refusal. Placeholders in braces are filled in when the message is shown.

| # | String (verbatim at `0bb3ed12`) | Where (commit) | Who sees it | Verdict |
|---|---|---|---|---|
| 1 | `The template is not valid.` | `Templates/TemplateEndpoints.cs:257` (`0d4022b9`, #145) | staff, templates API 400 | **UNRULED** (staff-only) |
| 2 | `There is no template with that id.` | `:259` | staff, 404 | **UNRULED** (staff-only) |
| 3 | `That template has no such version.` | `:117` | staff, 404 | **UNRULED** (staff-only) |
| 4 | `includeArchived must be true or false.` | `:82` | staff, 400 `INVALID_FILTER` | **UNRULED** (staff-only) |
| 5 | `baseVersion must be 1 or more.` | `:135` | staff, 400 detail | **UNRULED** (staff-only) |
| 6 | `An archived template cannot be changed; it stays readable.` | `:152` | staff, 409 | **UNRULED** (staff-only) |
| 7 | `The template is at version {n}. Reload and reapply your change.` | `:156` | staff, 409 `STALE_REVISION` | **UNRULED** (staff-only) |
| 8 | `name must be 1 to {max} characters with no line breaks.` | `:229` | staff, 400 detail | **UNRULED** (staff-only) |
| 9 | `components must hold 1 to {max} entries.` | `:233` | staff, 400 detail | **UNRULED** (staff-only) |
| 10 | `components[{i}].key must be 1 to {max} visible characters with no spaces.` | `:242` | staff, 400 detail | **UNRULED** (staff-only) |
| 11 | `components[{i}].key repeats an earlier entry.` | `:246` | staff, 400 detail | **UNRULED** (staff-only) |
| 12 | `components[{i}].quantityPerDevice must be a whole number from 1 to {max}.` | `:250` | staff, 400 detail | **UNRULED** (staff-only) |
| 13 | `The template store could not be changed. Nothing was changed.` | `:264` | staff, 503 `TEMPLATE_UNAVAILABLE` | **UNRULED** (staff-only) |
| 14 | `The triage is not valid. Nothing was changed.` | `Feedback/FeedbackEndpoints.cs:350` (`b8ae9011`, #176 build) | Administrator, triage 400 | **UNRULED** (staff-only; not in C-65's register) |
| 15 | `at least one of status, priority and notes is required.` | `:329` | Administrator, 400 detail | **UNRULED** (staff-only) |
| 16 | `status must be one of {list}.` | `:333` | Administrator, 400 detail | **UNRULED** (staff-only) |
| 17 | `priority must be one of {list}.` | `:337` | Administrator, 400 detail | **UNRULED** (staff-only) |
| 18 | `notes must be at most {max} characters after trimming.` | `:342` | Administrator, 400 detail | **UNRULED** (staff-only) |
| 19 | `notes contains a control character (line breaks and tabs are allowed).` | `:346` | Administrator, 400 detail | **UNRULED** (staff-only) |
| 20 | `The request body is over {n} KB. Nothing was changed.` | `:310` (triage 413) | Administrator, 413 | **UNRULED** (staff-only) |
| 21 | `The triage could not be saved just now. Nothing was changed; try again.` | `:360` | Administrator, 503 | **UNRULED** (staff-only) |
| 22 | `INVALID QUANTITY RULE` | `Engine/Calculation/PurchaseCalculator.cs:63` (`7f34130c`, #137) | staff, quote Issues list | **UNRULED** (staff-only; `[B1111-WORDS-1]`) |
| 23 | `The quantity rule is not per device, fixed per group or manual.` | `:394` (`7f34130c`) | staff, Issues | **UNRULED** (staff-only; `[B1111-WORDS-1]`) |
| 24 | `INVALID SITE ALLOCATION` | `:66` (`19d084fa`, #140) | staff, Issues | **UNRULED** (staff-only; `[B1111-WORDS-1]`) |
| 25 | `SITE ALLOCATION DIFFERS` | `:69` (`19d084fa`) | staff, Issues | **UNRULED** (C-82 rules when it shows, not its words) |
| 26 | `A site needs a name used once, a number of devices from 0, and a section that is a device group.` | `:341` (`19d084fa`) | staff, Issues | **UNRULED** (C-86: "Not settled (2) the text … of the refusal") |
| 27 | `Section {id}: the sites add up to {n} devices but the group has {m}. Make them equal.` | `:602` (`19d084fa`) | staff, Issues | **UNRULED** (staff-only; `[B1111-WORDS-1]`) |
| 28 | `X-44` (the rule label on row 27) | `:602` (`19d084fa`) | staff, Issues | **UNRULED** (staff-only; `[B1111-WORDS-1]` "the rule label X-44") |
| 29 | `This line is counted per site. Add a site with at least one device, or the quote cannot be priced.` | `:400` (`0d656f90`) | staff, Issues | **UNRULED** (C-86: "the words of the note … come to the product owner as a wording card first") |
| 30 | `X-13, X-14, X-16, X-25, X-26: monthly pages x cost per page (reported = the contract supplies cost / term); passes when the contract amounts, monthly x term against the contract supplies cost, are within the tolerance; before the replacement shortfall (X-17, X-27)` | `Engine/Reconciliation/PurchaseRecomputation.cs:25` (`94258c9e`, #106) | staff, reconciliation rule text (changed wording; was `×`/`÷` and no "passes when…" clause) | **UNRULED** (staff-only) |
| 31 | `The value is not exactly one of the names the contract lists.` | `Infrastructure/ApiJson.cs:34` (`459db8b8`, #102) | staff, contract refusal (DERIVED: `QuoteEndpoints.cs:1319` replaces it with the C-53 row-4 sentence when the path is set; I count it in case it shows when the path is empty) | **UNRULED** (staff-only) |
