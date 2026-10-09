/**
 * =============================================================================
 * POSTGRES ERROR CLASSIFICATION (KS-445)
 * =============================================================================
 * Originate's raw queries run through Prisma, which wraps the underlying
 * Postgres error: the SQLSTATE is NOT on `err.code` (that holds Prisma's own
 * `P2010`) but on `err.meta.code`, and sometimes only inside the message text
 * ("Raw query failed. Code: `42804`. ..."). The bare pg driver, by contrast,
 * puts the SQLSTATE directly on `err.code`. This helper normalises all three
 * shapes (same matching approach as the KS-255 fix in routes/certifications.ts)
 * so route handlers can map constraint/type failures to an honest 4xx instead
 * of leaking a raw 500.
 * =============================================================================
 */

/** SQLSTATE is exactly 5 chars, digits + uppercase letters (e.g. 22P02, 23503). */
const SQLSTATE_PATTERN = /^[0-9A-Z]{5}$/;

/** Prisma's own error codes (P2010 etc.) also match the 5-char shape — exclude them. */
const PRISMA_CODE_PATTERN = /^P\d{4}$/;

/**
 * The SQLSTATEs the write-path handlers map to 4xx responses. Kept as an
 * explicit list so the message-text fallback can't false-match arbitrary
 * 5-char tokens in an error string:
 *   22P02 invalid text representation (bad ::uuid cast)
 *   22001 string data right truncation (value longer than VARCHAR(n))
 *   22007 / 22008 invalid / out-of-range datetime
 *   22021 invalid byte sequence (non-UTF-8 input)
 *   22P05 untranslatable character (e.g. \u0000 inside a jsonb value)
 *   23502 not-null violation
 *   23503 foreign-key violation (e.g. userId not in users)
 *   23505 unique violation
 *   23514 check-constraint violation (value outside an allowed set)
 *   42804 datatype mismatch (bound parameter of the wrong type)
 */
const KNOWN_PG_CODES = /\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/;

/**
 * Extract the Postgres SQLSTATE from an error of any of the shapes originate
 * sees: bare pg driver (`err.code`), Prisma-wrapped (`err.meta.code`), or
 * message-embedded ("Code: `42804`").
 *
 * @param err - the caught error (unknown shape — bare pg, Prisma wrapper, or a
 *   re-thrown Error whose message still carries the code text).
 * @returns the 5-char SQLSTATE (e.g. '23503') when one is identifiable,
 *   otherwise undefined (caller should fall through to its 500 path).
 * @example
 * const pgCode = extractPgCode(err);
 * if (pgCode === '23503') return res.status(404).json(...);
 */
export function extractPgCode(err: unknown): string | undefined {
  const e = err as
    | { code?: unknown; meta?: { code?: unknown }; message?: unknown }
    | null
    | undefined;

  // Structured fields first: bare pg puts the SQLSTATE on `code`, Prisma on `meta.code`.
  for (const candidate of [e?.code, e?.meta?.code]) {
    if (
      typeof candidate === 'string' &&
      SQLSTATE_PATTERN.test(candidate) &&
      !PRISMA_CODE_PATTERN.test(candidate)
    ) {
      return candidate;
    }
  }

  // Fallback: Prisma sometimes surfaces the pg code only inside the message text.
  if (typeof e?.message === 'string') {
    const match = e.message.match(KNOWN_PG_CODES);
    if (match) return match[1];
  }

  return undefined;
}
