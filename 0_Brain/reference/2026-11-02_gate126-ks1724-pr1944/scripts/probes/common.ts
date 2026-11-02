// QA GATE 126 probe helpers (not part of the PR). Copied next to each probe for the run only.
import crypto from 'crypto';
import http from 'http';
import type { AddressInfo } from 'net';
import express from 'express';
import { appendFileSync } from 'fs';
import { vi } from 'vitest';

export const OUT = process.env.PROBE_OUT as string;
export const TREE = process.env.PROBE_TREE as string;
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
export const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
export const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
export function token(claims: Record<string, unknown>): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ iat: now, exp: now + 600, ...claims })));
  return `${header}.${payload}.${b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM))}`;
}
export function setJwtEnv() {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL; delete process.env.DATABASE_URL;
  for (const n of ['JSON_BODY_MAX_ARRAY_LENGTH', 'JSON_BODY_MAX_NODES', 'JSON_BODY_MAX_DEPTH']) delete process.env[n];
}

/** Count JSON values: every value once (the cap's definition). */
export function countNodes(v: unknown): number {
  let n = 0; const st: unknown[] = [v];
  while (st.length) { const x = st.pop(); n += 1; if (x && typeof x === 'object') for (const k of Object.keys(x as object)) st.push((x as any)[k]); }
  return n;
}
export const nest = (n: number): unknown => { let v: unknown = []; for (let i = 1; i < n; i += 1) v = [v]; return v; };
/** max container nesting (root container = 1). */
export function containerDepth(v: unknown): number {
  let best = 0; const st: Array<[unknown, number]> = [[v, 1]];
  while (st.length) { const [x, d] = st.pop()!; if (x && typeof x === 'object') { best = Math.max(best, d); for (const k of Object.keys(x as object)) st.push([(x as any)[k], d + 1]); } }
  return best;
}
/** valid + pad, sized so the WHOLE body has exactly `total` values; no array over 1000, depth 3. */
export function padToNodes(valid: Record<string, unknown>, total: number): Record<string, unknown> {
  const base = countNodes({ ...valid, pad: [] }); // root..fields + the pad array itself
  let need = total - base; const pad: number[][] = [];
  while (need > 0) { const take = Math.min(1000, need - 1); if (take <= 0) { pad.push([]); need -= 1; break; } pad.push(Array(take).fill(1)); need -= take + 1; }
  const out = { ...valid, pad };
  if (countNodes(out) !== total) throw new Error(`padToNodes: ${countNodes(out)} != ${total}`);
  return out;
}
/** the standard shape family over a route-valid body. */
export function shapes(valid: Record<string, unknown>): Record<string, unknown> {
  const s: Record<string, unknown> = {
    normal: valid,
    array_at_1000: { ...valid, pad: Array(1000).fill(1) },
    array_over_1001: { ...valid, pad: Array(1001).fill(1) },
    nodes_at_20000: padToNodes(valid, 20000),
    nodes_over_20001: padToNodes(valid, 20001),
    depth_at_32: { ...valid, pad: nest(31) },
    depth_over_33: { ...valid, pad: nest(32) },
  };
  if (containerDepth(s.depth_at_32) !== 32 || containerDepth(s.depth_over_33) !== 33) throw new Error('depth shape wrong');
  return s;
}

export type Booted = { server: http.Server; base: string };
export async function boot(importApp: () => Promise<any>): Promise<Booted> {
  vi.spyOn(express.application, 'listen').mockReturnValue({ keepAliveTimeout: 0, headersTimeout: 0, close: () => undefined, on: () => undefined, address: () => ({ port: 0 }) } as unknown as http.Server);
  const app = (await importApp()).default;
  const server = http.createServer(app);
  await new Promise<void>((r) => { server.listen(0, '127.0.0.1', r); });
  return { server, base: `http://127.0.0.1:${(server.address() as AddressInfo).port}` };
}
export async function close(b: Booted) { (b.server as any).closeAllConnections?.(); await new Promise<void>((r) => b.server.close(() => r())); }

/** capture console lines that mention the structural cap */
export function captureCapLines(): { lines: string[]; restore: () => void } {
  const lines: string[] = [];
  const orig = { warn: console.warn, log: console.log, error: console.error, info: console.info };
  for (const k of ['warn', 'log', 'error', 'info'] as const) {
    (console as any)[k] = (...a: unknown[]) => { const s = a.map(String).join(' '); if (/structural/i.test(s)) lines.push(`${k}: ${s}`); };
  }
  return { lines, restore: () => Object.assign(console, orig) };
}

export async function send(b: Booted, path: string, raw: string | undefined, headers: Record<string, string>, method = 'POST') {
  const t0 = Date.now();
  const res = await fetch(`${b.base}${path}`, { method, headers, body: raw });
  const text = await res.text();
  return { status: res.status, body: text.length > 400 ? text.slice(0, 400) + `...(+${text.length - 400})` : text, ms: Date.now() - t0 };
}
export function record(row: Record<string, unknown>) { appendFileSync(OUT, JSON.stringify({ tree: TREE, ...row }) + '\n'); }
