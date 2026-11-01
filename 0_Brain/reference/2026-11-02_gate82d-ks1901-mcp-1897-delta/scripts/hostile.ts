export const SECRETVAL = 'S3CR3T-VALUE';
export function hostile(): Array<[string, () => unknown, boolean]> {
  // third field: true = primitive/non-Error, the secret must be in no log line
  return [
    ['thrown string S3CR3T-VALUE', () => SECRETVAL, true],
    ['thrown number 31337', () => 31337, true],
    ['thrown Symbol(S3CR3T)', () => Symbol('S3CR3T-VALUE'), true],
    ['thrown BigInt', () => BigInt(123456789), true],
    ['thrown boolean', () => false, true],
    ['thrown null', () => null, true],
    ['thrown undefined', () => undefined, true],
    ['thrown empty string', () => '', true],
    ['thrown NaN', () => NaN, true],
    ['thrown String object', () => new String(SECRETVAL), true],
    ['array of secrets', () => [SECRETVAL], true],
    ['obj with secret value', () => ({ k: SECRETVAL }), true],
    ['function', () => function f() { return SECRETVAL; }, true],
    ['revoked Proxy', () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }, true],
    ['Error (message logged by design)', () => new Error('plainmsg'), false],
  ];
}
