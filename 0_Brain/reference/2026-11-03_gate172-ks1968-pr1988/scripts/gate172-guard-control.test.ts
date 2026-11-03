// Gate 172: positive control for the outbound guard INSIDE a vitest worker. Uses only the .invalid control host.
import { it, expect } from 'vitest';
import https from 'https';
const C = 'https://gate172-guard-control.invalid/range/00000';
it('guard fires on global fetch inside a vitest worker', async () => { await expect(fetch(C)).rejects.toThrow(/gate172 guard/); });
it('guard fires on https.get inside a vitest worker', async () => {
  const m = await new Promise<string>((r) => { try { https.get(C, () => r('NOT BLOCKED')).on('error', (e) => r(e.message)); } catch (e) { r((e as Error).message); } });
  expect(m).toMatch(/gate172 guard/);
});
it('the real password module, HIBP ON, with NO stub: the guard blocks the real host and it fails open', async () => {
  delete process.env.HIBP_ENABLED;
  const { isPasswordBreached } = await import('../services/password');
  expect(await isPasswordBreached('gate172-control-not-a-real-password')).toBe(false);
});
