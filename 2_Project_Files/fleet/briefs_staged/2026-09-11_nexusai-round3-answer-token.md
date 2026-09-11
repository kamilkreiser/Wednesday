# Continue, and close the class at the logger

**BLUF.** **Do NOT stop. Your fix stands, and the report you sent before READY FOR QA was the right call.** **Add one more piece:** a class fix in the LOGGER, because the part you are leaving out is the dangerous part.

## Why the logger, not only `executeQuery`
- The token leaks because an error object carrying axios' `config.headers.Authorization` (or a `Bearer …` string) reaches `logger.*` **nested**, and `logger.js:36` only unwraps top-level `error`/`originalError`. You have fixed ONE source that produces such objects. **The ~150 raw-error log calls you name can each carry another axios client's error**, including Graph and token endpoints, and nobody has enumerated them. A per-call fix leaves exactly the unenumerated paths open.
- **One place covers them all:** in the production (and development) formatter, a **depth-limited, cycle-safe redaction** over the whole meta object. Redact any `authorization` / `proxy-authorization` header value, any `Bearer <token>` substring in strings, and values under keys matching `access_token|refresh_token|id_token|client_secret|password|secret`. Leave structure and status codes intact so the auth classifier keeps working.
- **Keep your `executeQuery` and `connectionTestLogMeta()` changes.** They are the precise fix; the logger redaction is the net under everything else.

## Proof owed
1. **A red cell through a path that does NOT go through `executeQuery`**: a nested axios-shaped error with an `Authorization: Bearer <stub token>` header logged via an ordinary `logger.error(msg, err)`. It must be RED at `e51d302` and GREEN after, in both NODE_ENV modes.
2. **A negative control:** a log line with no secret-shaped content comes out unchanged, so the redaction does not eat ordinary output.
3. Your existing 26 cells stay green, then full `npm run verify`, the image proof, and full-ID plus token counts across the whole run (all 0).

## Bound
If the logger redaction turns out to need more than the formatter (for example transports that bypass it), **stop at what the formatter covers, name the bypass in READY FOR QA, and do not chase it.** A token leak in the product is Kam's to hear, and Tuesday will tell him with the gate verdict. Put this at the head of READY FOR QA: **"pre-existing token leak in container logs; reachable from the package via MAJ-3; closed at the logger and at executeQuery"**, with what is NOT covered named.

Tuesday
