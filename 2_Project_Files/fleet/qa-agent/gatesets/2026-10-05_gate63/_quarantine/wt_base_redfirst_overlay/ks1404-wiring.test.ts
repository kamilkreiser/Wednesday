/**
 * KS-1404 — the trust anchor is never DELIVERED to the running service, so every real RFC 3161
 * token is refused with `no trust anchor configured` whatever the TSA does.
 *
 * #1376 closed the forgeable paths in the VERIFIER. It left the anchor undelivered: nothing puts
 * `config/` into the timestamping runtime image, and nothing passes `TSA_TRUST_ANCHORS_PEM` to the
 * container. Measured on both live boxes 2026-10-05 (Seat D 8th, ITEM 1): `TSA_URL` PRESENT-EMPTY,
 * `TSA_TRUST_ANCHORS_PEM` ABSENT, `/app/config` ABSENT, and `/health` reporting D-Trust on both.
 * So `readTrustAnchorsPem()` returns undefined, 0 anchors parse, and rfc3161-verify.ts refuses.
 *
 * RED-FIRST. Cells A, B and C1 assert the POST-FIX state and FAIL at the base commit
 * (f01c1da5717f). C2, D and E are CONTROLS that pass at base AND head — they are here so that a
 * green run means "the fix landed", not "the file stopped looking".
 *
 * WHY C2 IS A CONTROL AND NOT A RED ARM, stated rather than blurred: the file-path branch of
 * `readTrustAnchorsPem()` already exists at base, so a cell that only exercises it would pass at
 * base and prove nothing about this change. What this PR changes is whether anything ever PUTS a
 * readable path into that variable. C2 pins the branch my wiring depends on — and it is worth
 * pinning, because the existing ks1404 suite only ever passes the anchor as INLINE PEM TEXT; the
 * `readFileSync` branch the compose default will exercise is untested today.
 *
 * NO ROUTE CELL AND NO DATABASE. The existing suite's cell 14 boots the service and does an HTTP
 * round trip; on a loaded shared machine its cold run took 7946ms against a 5000ms default and went
 * red (then 36/36 warm, and 420ms in isolation). Nothing here needs a server or a DB.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync, existsSync, mkdtempSync, writeFileSync } from 'fs';
import { resolve, join, basename } from 'path';
import { tmpdir } from 'os';
import { createHash } from 'crypto';
import { verifyTimestamp } from '../tsa/qualified-tsa';

// The tree under test, resolved from THIS file: src/__tests__ -> src -> timestamping -> services -> Dev
const DEV = resolve(__dirname, '..', '..', '..', '..');
const SERVICE_DIR = resolve(DEV, 'services', 'timestamping');
const COMPOSE = resolve(DEV, 'docker-compose.yml');
const DOCKERFILE = resolve(SERVICE_DIR, 'Dockerfile');

/** The D-TRUST Root CA 1 2017 SHA-256, as config/README.md records it. */
const DTRUST_SHA256 =
  '4d24807b9cad5110f40ed79d934346d7c9b0290431dc9b11a40bbb86fcf2aef6';

/** The timestamping service block of a compose file, by 2-space-indent key boundaries. */
function timestampingBlock(composeText: string): string[] {
  const lines = composeText.split('\n');
  const start = lines.findIndex((l) => l.startsWith('  timestamping:'));
  expect(start, "compose has a '  timestamping:' key at 2-space indent").toBeGreaterThan(-1);
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    const l = lines[i];
    if (l.startsWith('  ') && !l.startsWith('   ') && l.trim().endsWith(':')) { end = i; break; }
  }
  return lines.slice(start, end);
}

/**
 * Every `- NAME=value` entry of that block's `environment:` list.
 *
 * ⚠ The list is INTERLEAVED WITH COMMENTS at the same indent. An earlier version of this
 * function broke on the first non-`- ` line and so reported 9 of the 14 real entries, stopping at
 * the PII comment block. That is worse than a wrong count: a seat that added the variable AFTER
 * `TSA_AUTH_KEY` would have been told it was ABSENT. The list ends where the INDENT DROPS, not at
 * the first line that is not an entry.
 */
function environmentEntries(block: string[]): Map<string, string> {
  const out = new Map<string, string>();
  const envAt = block.findIndex((l) => l.trim() === 'environment:');
  if (envAt < 0) return out;
  for (let i = envAt + 1; i < block.length; i++) {
    const l = block[i];
    if (l.trim() === '') continue;                     // blank line inside the list
    const indent = l.length - l.trimStart().length;
    if (indent < 6) break;                             // the list ended (e.g. `    depends_on:`)
    if (l.trim().startsWith('#')) continue;            // a comment at list indent
    if (!/^\s{6}- /.test(l)) continue;                 // anything else at depth: not an entry
    const m = l.trim().replace(/^- /, '');
    const eq = m.indexOf('=');
    if (eq > 0) out.set(m.slice(0, eq), m.slice(eq + 1));
  }
  return out;
}

/** Resolve a compose `${VAR:-default}` to its default, the way the container would with no .env. */
function composeDefault(raw: string): string | undefined {
  const m = raw.match(/^\$\{[A-Z_]+:-(.*)\}$/);
  return m ? m[1] : undefined;
}

/** DER sha256 of every certificate in a PEM text. */
function certFingerprints(pem: string): string[] {
  const blocks = pem.match(/-----BEGIN CERTIFICATE-----[\s\S]*?-----END CERTIFICATE-----/g) ?? [];
  return blocks.map((b) => {
    const b64 = b.replace(/-----(BEGIN|END) CERTIFICATE-----/g, '').replace(/\s+/g, '');
    return createHash('sha256').update(Buffer.from(b64, 'base64')).digest('hex');
  });
}

describe('KS-1404 — the trust anchor reaches the running service', () => {
  const composeText = readFileSync(COMPOSE, 'utf-8');
  const dockerfileText = readFileSync(DOCKERFILE, 'utf-8');
  const block = timestampingBlock(composeText);
  const env = environmentEntries(block);

  it('cell A [RED at base]: compose passes TSA_TRUST_ANCHORS_PEM to the timestamping container', () => {
    const raw = env.get('TSA_TRUST_ANCHORS_PEM');
    expect(
      raw,
      `the timestamping environment list has no TSA_TRUST_ANCHORS_PEM entry. ` +
        `It currently passes: ${[...env.keys()].join(', ')}`,
    ).toBeDefined();
    const dflt = composeDefault(raw as string);
    expect(dflt, `TSA_TRUST_ANCHORS_PEM must carry a \${VAR:-default}; got ${raw}`).toBeDefined();
    // The default makes the anchor effective on a box with no .env edit, which is how both live
    // boxes are configured (measured: no box-level TSA override exists on either).
    expect(dflt).toBe('/app/config/tsa-trust-anchors-dtrust.crt');
  });

  it('cell B [RED at base]: the Dockerfile runtime stage ships config/ BEFORE the chmod', () => {
    const lines = dockerfileText.split('\n');
    // the LAST `FROM` begins the runtime stage; anything before it is a builder
    let runtimeStart = -1;
    lines.forEach((l, i) => { if (/^FROM /.test(l)) runtimeStart = i; });
    expect(runtimeStart, 'the Dockerfile has at least one FROM').toBeGreaterThan(-1);
    const runtime = lines.slice(runtimeStart);

    const copyAt = runtime.findIndex((l) => /^COPY --from=builder \/app\/config \.\/config\s*$/.test(l));
    expect(
      copyAt,
      'the runtime stage never copies config/. At base it copies only /app/dist, which is why ' +
        '/app/config does not exist in the running image on either box.',
    ).toBeGreaterThan(-1);

    const chmodAt = runtime.findIndex((l) => /chmod -R a\+rX/.test(l));
    expect(chmodAt, 'the runtime stage has a chmod -R a+rX').toBeGreaterThan(-1);
    // Order matters: the service runs as `nodejs`, so the anchor must be made readable AFTER it
    // arrives. Copying after the chmod ships a file the service cannot read.
    expect(copyAt, 'config/ must be copied BEFORE the chmod that makes it readable')
      .toBeLessThan(chmodAt);
  });

  it('cell C1 [RED at base]: the path compose names exists in the tree and is the D-Trust root alone', () => {
    const raw = env.get('TSA_TRUST_ANCHORS_PEM');
    expect(raw, 'cell A must pass before this one can mean anything').toBeDefined();
    const imagePath = composeDefault(raw as string) as string;

    // Map the IMAGE path onto the tree the way the Dockerfile does: /app/config <- services/timestamping/config
    expect(imagePath.startsWith('/app/config/'), `expected an /app/config path, got ${imagePath}`).toBe(true);
    const onDisk = join(SERVICE_DIR, 'config', basename(imagePath));
    expect(existsSync(onDisk), `compose names ${imagePath}, which maps to ${onDisk} — absent`).toBe(true);

    const fps = certFingerprints(readFileSync(onDisk, 'utf-8'));
    // ONE provider's root, per Kam's card (a): "pins that provider's published root".
    expect(fps.length, 'the per-provider anchor file holds exactly one certificate').toBe(1);
    expect(fps[0]).toBe(DTRUST_SHA256);

    // and it must be byte-for-byte a root the repo already committed — no new trust introduced here
    const bundle = readFileSync(join(SERVICE_DIR, 'config', 'tsa-trust-anchors.crt'), 'utf-8');
    expect(certFingerprints(bundle)).toContain(DTRUST_SHA256);
  });

  describe('the delivery mechanism and the guards (controls: these pass at base AND head)', () => {
    let pki: any;
    let buildToken: any;
    let toPem: any;
    const HASH = 'b'.repeat(64);

    beforeAll(async () => {
      const m = await import('./ks1404-pki');
      buildToken = m.buildToken;
      toPem = m.toPem;
      pki = await m.buildPki();
    });

    const verifyWith = async (token: string, anchor: string | undefined) => {
      const prev = process.env.TSA_TRUST_ANCHORS_PEM;
      if (anchor === undefined) delete process.env.TSA_TRUST_ANCHORS_PEM;
      else process.env.TSA_TRUST_ANCHORS_PEM = anchor;
      try {
        return await verifyTimestamp(token, HASH);
      } finally {
        if (prev === undefined) delete process.env.TSA_TRUST_ANCHORS_PEM;
        else process.env.TSA_TRUST_ANCHORS_PEM = prev;
      }
    };

    const genuine = () =>
      buildToken({ hashHex: HASH, signerCert: pki.tsa.cert, signerKey: pki.tsa.keys.privateKey });

    it('cell C2 [CONTROL]: an anchor delivered as a FILE PATH is read and used; unset fails closed', async () => {
      // This is the branch the compose default exercises and the existing suite never does:
      // it passes inline PEM TEXT everywhere. readTrustAnchorsPem() treats a non-PEM value as a
      // path and readFileSync's it.
      const dir = mkdtempSync(join(tmpdir(), 'ks1404-anchor-'));
      const file = join(dir, 'anchor-by-path.crt');
      writeFileSync(file, toPem(pki.root.cert));
      const token = await genuine();

      const viaPath = await verifyWith(token, file);
      expect(viaPath.error, 'a genuine token must verify through a FILE PATH anchor').toBeUndefined();
      expect(viaPath.valid).toBe(true);

      // the negative half: with nothing configured the SAME token is refused, fail-closed
      const unset = await verifyWith(token, undefined);
      expect(unset.valid).toBe(false);
      expect(unset.error).toMatch(/no trust anchor configured/);
    });

    it('cell D [CONTROL]: a DER token under an UNTRUSTED root is still refused', async () => {
      const token = await genuine();
      const wrongAnchor = toPem(pki.other.cert);
      const r = await verifyWith(token, wrongAnchor);
      expect(r.valid).toBe(false);
      expect(r.error).toMatch(/does not chain to a configured trust anchor/);
    });

    it('cell E [CONTROL]: a mock JSON token is still refused, with an anchor configured', async () => {
      const mock = Buffer.from(
        JSON.stringify({ mock: true, hash: HASH, tsaName: 'D-Trust GmbH (mock)' }),
      ).toString('base64');
      // base64 JSON starts "ey" — exactly the shape ITEM 1 found as demo's only ts_timestamps row.
      expect(mock.slice(0, 2)).toBe('ey');
      const r = await verifyWith(mock, toPem(pki.root.cert));
      expect(r.valid).toBe(false);
    });
  });
});
