// shared hostile thrown values. Each entry: [label, factory]. SECRETVAL must never appear in any log.
export const SECRETVAL = 'S3CR3T-VALUE';
export function hostile(): Array<[string, () => unknown]> {
  return [
    ['revoked Proxy', () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }],
    ['Error w/ throwing message getter', () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } })],
    ['obj w/ throwing getter on message', () => ({ get message() { throw new Error('g'); }, k: SECRETVAL })],
    ['obj w/ throwing getter on name', () => ({ get name() { throw new Error('g'); }, k: SECRETVAL })],
    ['obj w/ throwing getter on constructor', () => ({ get constructor() { throw new Error('g'); }, k: SECRETVAL })],
    ['null-prototype obj', () => Object.assign(Object.create(null), { token: SECRETVAL })],
    ['Symbol', () => Symbol(SECRETVAL)],
    ['BigInt', () => BigInt(123456789)],
    ['obj toString throws', () => ({ k: SECRETVAL, toString() { throw new Error('ts'); } })],
    ['obj Symbol.toPrimitive throws', () => ({ k: SECRETVAL, [Symbol.toPrimitive]() { throw new Error('tp'); } })],
    ['obj toString returns secret', () => ({ k: 1, toString() { return SECRETVAL; } })],
    ['obj toJSON returns secret', () => ({ k: 1, toJSON() { return SECRETVAL; } })],
    ['Proxy ownKeys throws', () => new Proxy({}, { ownKeys() { throw new Error('ok'); } })],
    ['Proxy ownKeys returns secret-ish names', () => new Proxy({ a: 1 }, { ownKeys() { return ['field_a']; }, getOwnPropertyDescriptor() { return { value: SECRETVAL, enumerable: true, configurable: true }; } })],
    ['array of secrets', () => [SECRETVAL, SECRETVAL]],
    ['function', () => function secretFn() { return SECRETVAL; }],
    ['thrown string (the value)', () => SECRETVAL],
    ['Error subclass message=secret', () => new (class X extends Error {})(SECRETVAL)],
    ['Error w/ secret in non-message field', () => Object.assign(new Error('plain'), { token: SECRETVAL })],
    ['boolean', () => false],
    ['empty object', () => ({})],
  ];
}
