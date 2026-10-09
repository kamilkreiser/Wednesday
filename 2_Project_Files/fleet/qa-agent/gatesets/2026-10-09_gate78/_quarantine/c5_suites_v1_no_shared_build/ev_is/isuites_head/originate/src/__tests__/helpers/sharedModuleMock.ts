/**
 * Build a `@secuura/shared` mock from the REAL module's export list.
 *
 * QA finding F-926-2. Every `jest.mock('@secuura/shared', () => ({ ... }))` in
 * this service used to be a hand-written object literal listing only the
 * handful of exports its author happened to need. Everything else came back
 * `undefined`, so the first cell to reach an unlisted export died on a
 * TypeError that had nothing to do with what it was testing — and the omission
 * was invisible until then. `ks444-webhooks-create-description-guard` shipped
 * three keys and no `safeOutboundRequest`; the sibling suite covering the same
 * routes shipped five. Nothing reconciled them.
 *
 * `makeSharedMock` starts from `Object.keys(jest.requireActual(...))`, so the
 * mock's surface is the module's surface by construction. Functions become
 * inert `jest.fn()`s (never the real implementation — these are unit suites and
 * must not acquire live behaviour by accident); everything else — constants,
 * classes, namespaces like `z` — passes through as the real value. Callers
 * override only what they need to assert on.
 *
 * Forgetting an export is no longer possible. Stubbing one that no longer
 * exists throws, which is the same drift caught from the other side.
 */
export function makeSharedMock(
  overrides: Record<string, unknown> = {},
): Record<string, unknown> {
  const actual = jest.requireActual('@secuura/shared') as Record<string, unknown>;

  const base: Record<string, unknown> = {};
  for (const key of Object.keys(actual)) {
    const value = actual[key];
    base[key] = typeof value === 'function' ? jest.fn() : value;
  }

  const unexported = Object.keys(overrides).filter((key) => !(key in base));
  if (unexported.length > 0) {
    throw new Error(
      `makeSharedMock: override(s) not exported by @secuura/shared: ${unexported.join(', ')}. ` +
        'Either the export was renamed/removed and this stub is now dead, or the name is a typo.',
    );
  }

  return { ...base, ...overrides };
}
