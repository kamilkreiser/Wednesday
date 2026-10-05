/**
 * gate63 RUNTIME PROBE (#1388, KS-1404 wiring) — a QA instrument, NEVER committed to the repo.
 *
 * The gate COPIES this file into ITS OWN scratch worktree as
 *   Blockchain/Dev/services/timestamping/src/__tests__/zz_gate63_probe.test.ts
 * runs it with vitest, and then QUARANTINES the copy (never rm) and proves `git status --porcelain` clean.
 *
 * What it measures (the security read the brief asks for; the PR's own cells do not cover these):
 *   P1  the REAL per-provider file, delivered as a FILE PATH, PARSES to >= 1 anchor inside the verifier:
 *       a synthetic genuine token is refused with "does not chain to a configured trust anchor"
 *       — NOT "no trust anchor configured" (which would mean the file was read but 0 anchors parsed).
 *   P2  parseTrustAnchors() on the real file: exactly 1 certificate, DER sha256 == D-TRUST Root CA 1 2017;
 *       CONTROL the two-root bundle parses to 2 (the instrument can count past 1).
 *   P3  TSA_TRUST_ANCHORS_PEM names a MISSING file (the compose default's exact string, on a host / an image
 *       that lacks /app/config): FAIL CLOSED — valid false, "no trust anchor configured", NO throw — and
 *       logger.error is called with "could not be read" (the only signal an operator gets; it is per-verify,
 *       never at boot).
 *   P4  a DIRECTORY path: fail closed, no throw.
 *   P5  a readable file holding NON-PEM text: fail closed, no throw.
 *   P6  whitespace-only value: fail closed.
 *   P7  CONTROL: a synthetic root delivered by file path VERIFIES true — so P1/P3-P6's refusals are not a
 *       defect of the probe's token.
 *   P8  INFO: the two-root BUNDLE as the path (what a box .env override to the old file would do):
 *       parsed (refusal reason "does not chain", not "no trust anchor").
 * Every cell records its captured values (console.log AND, when G63_PROBE_OUT names a file, one JSON line
 * per cell there) so the gate quotes values, not verdicts. Run: G63_PROBE_OUT=<evidence>/probe.jsonl npx vitest run …
 */
import { describe, it, expect, beforeAll, vi } from 'vitest';
import { readFileSync, mkdtempSync, writeFileSync, appendFileSync } from 'fs';
import { resolve, join } from 'path';
import { tmpdir } from 'os';
import { createHash } from 'crypto';
import { verifyTimestamp } from '../tsa/qualified-tsa';
import { parseTrustAnchors } from '../tsa/rfc3161-verify';
import { logger } from '../utils/logger';

const SERVICE_DIR = resolve(__dirname, '..', '..');
const DTRUST_FILE = join(SERVICE_DIR, 'config', 'tsa-trust-anchors-dtrust.crt');
const BUNDLE_FILE = join(SERVICE_DIR, 'config', 'tsa-trust-anchors.crt');
const DTRUST_SHA256 = '4d24807b9cad5110f40ed79d934346d7c9b0290431dc9b11a40bbb86fcf2aef6';
const COMPOSE_DEFAULT = '/app/config/tsa-trust-anchors-dtrust.crt';
const HASH = 'c'.repeat(64);
/** captured values go to G63_PROBE_OUT (JSON lines) — vitest may swallow console output; the gate quotes this file */
const rec = (cell: string, v: unknown) => {
  const line = cell + ' ' + JSON.stringify(v);
  console.log(line);
  if (process.env.G63_PROBE_OUT) appendFileSync(process.env.G63_PROBE_OUT, line + '\n');
};

describe('gate63 probe — the anchor as the wired path delivers it', () => {
  let pki: any; let buildToken: any; let toPem: any; let token: string;

  beforeAll(async () => {
    const m = await import('./ks1404-pki');
    buildToken = m.buildToken; toPem = m.toPem; pki = await m.buildPki();
    token = await buildToken({ hashHex: HASH, signerCert: pki.tsa.cert, signerKey: pki.tsa.keys.privateKey });
  });

  const verifyWith = async (anchor: string | undefined) => {
    const prev = process.env.TSA_TRUST_ANCHORS_PEM;
    if (anchor === undefined) delete process.env.TSA_TRUST_ANCHORS_PEM; else process.env.TSA_TRUST_ANCHORS_PEM = anchor;
    try { return await verifyTimestamp(token, HASH); }
    finally { if (prev === undefined) delete process.env.TSA_TRUST_ANCHORS_PEM; else process.env.TSA_TRUST_ANCHORS_PEM = prev; }
  };

  it('P7 CONTROL: a synthetic root by FILE PATH verifies true (the probe token is genuine)', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'g63-probe-'));
    const f = join(dir, 'synthetic-root.crt'); writeFileSync(f, toPem(pki.root.cert));
    const r = await verifyWith(f);
    rec('P7', { path: f, valid: r.valid, error: r.error });
    expect(r.valid).toBe(true);
  });

  it('P2: the real per-provider file parses to exactly 1 anchor at the D-Trust digest; CONTROL bundle -> 2', () => {
    const one = parseTrustAnchors(readFileSync(DTRUST_FILE, 'utf-8'));
    const two = parseTrustAnchors(readFileSync(BUNDLE_FILE, 'utf-8'));
    const fp = one.map((c: any) => createHash('sha256').update(Buffer.from(c.toSchema().toBER(false))).digest('hex'));
    rec('P2', { file: DTRUST_FILE, count: one.length, fingerprints: fp, bundleCount: two.length });
    expect(two.length, 'CONTROL: the instrument counts the two-root bundle as 2').toBe(2);
    expect(one.length).toBe(1);
    expect(fp[0]).toBe(DTRUST_SHA256);
  });

  it('P1: the REAL file delivered by path is read AND parsed (refusal is "does not chain", not "no anchor")', async () => {
    const r = await verifyWith(DTRUST_FILE);
    rec('P1', { path: DTRUST_FILE, valid: r.valid, error: r.error });
    expect(r.valid).toBe(false);
    expect(r.error).toMatch(/does not chain to a configured trust anchor/);
    expect(r.error).not.toMatch(/no trust anchor configured/);
  });

  it('P3: the compose default naming a MISSING file fails CLOSED, does not throw, and logs once per verify', async () => {
    const spy = vi.spyOn(logger, 'error');
    const before = spy.mock.calls.length;
    let threw: unknown = null; let r: any = null;
    try { r = await verifyWith(COMPOSE_DEFAULT); } catch (e) { threw = e; }
    const logged = spy.mock.calls.slice(before).map((c) => String(c[0]));
    spy.mockRestore();
    rec('P3', { path: COMPOSE_DEFAULT, threw: threw ? String(threw) : null, valid: r?.valid, error: r?.error, loggedErrors: logged });
    expect(threw).toBeNull();
    expect(r.valid).toBe(false);
    expect(r.error).toMatch(/no trust anchor configured/);
    expect(logged.some((m) => /could not be read/.test(m))).toBe(true);
  });

  it('P4: a DIRECTORY path fails closed, no throw', async () => {
    let threw: unknown = null; let r: any = null;
    try { r = await verifyWith(join(SERVICE_DIR, 'config')); } catch (e) { threw = e; }
    rec('P4', { threw: threw ? String(threw) : null, valid: r?.valid, error: r?.error });
    expect(threw).toBeNull(); expect(r.valid).toBe(false); expect(r.error).toMatch(/no trust anchor configured/);
  });

  it('P5: a readable NON-PEM file fails closed, no throw', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'g63-probe-'));
    const f = join(dir, 'garbage.crt'); writeFileSync(f, 'this is not a certificate\n');
    let threw: unknown = null; let r: any = null;
    try { r = await verifyWith(f); } catch (e) { threw = e; }
    rec('P5', { threw: threw ? String(threw) : null, valid: r?.valid, error: r?.error });
    expect(threw).toBeNull(); expect(r.valid).toBe(false); expect(r.error).toMatch(/no trust anchor configured/);
  });

  it('P6: a whitespace-only value fails closed', async () => {
    const r = await verifyWith('   ');
    rec('P6', { valid: r.valid, error: r.error });
    expect(r.valid).toBe(false); expect(r.error).toMatch(/no trust anchor configured/);
  });

  it('P8 INFO: the two-root bundle as the path is parsed (a box .env override would trust DigiCert too)', async () => {
    const r = await verifyWith(BUNDLE_FILE);
    rec('P8', { path: BUNDLE_FILE, valid: r.valid, error: r.error });
    expect(r.error).toMatch(/does not chain to a configured trust anchor/);
  });
});
