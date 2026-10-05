/**
 * Real RFC 3161 TimeStampToken verification — KS 1404.
 *
 * REPLACES the hash-presence walk in `qualified-tsa.ts`'s `verifyRealToken`, which returned
 * `valid: true` for ANY token merely CONTAINING the expected digest as an OCTET STRING, with no
 * signature check, no certificate chain, no TSTInfo parse and no algorithm-OID check.
 *
 * WHAT IS CHECKED (RFC 3161 Sec 2.4.2 + RFC 5652):
 *   1. strict DER: definite, minimal lengths, no trailing bytes;
 *   2. ContentInfo is id-signedData, and SignedData's eContentType is id-ct-TSTInfo;
 *   3. TSTInfo is PARSED, and the message imprint is read FROM `messageImprint.hashedMessage` —
 *      never searched for in the tree — with its hash-algorithm OID recognised;
 *   4. exactly one SignerInfo, whose signed attributes carry contentType = id-ct-TSTInfo and
 *      messageDigest = digest(eContent);
 *   5. the signature over the signed attributes re-encoded as SET OF, against the signer cert's
 *      public key;
 *   6. the signer certificate carries EKU id-kp-timeStamping and is valid at genTime, and chains to
 *      a CONFIGURED trust anchor.
 *
 * FAIL-CLOSED. With no anchor configured the answer is `valid: false`, reason
 * `no trust anchor configured`. Kam's ruling (card secuura-ks1404-tsa-trust-and-library-1004, option
 * a) is to trust the authority each environment's `TSA_URL` already points at. The published roots
 * ARE committed, at `config/tsa-trust-anchors.crt` (D-TRUST Root CA 1 2017 and DigiCert Assured ID
 * Root CA, with their source URLs, SHA-256 fingerprints and read time recorded in
 * `config/README.md`). The verifier reads them ONLY when `TSA_TRUST_ANCHORS_PEM` points at that
 * file, or inlines its text; NOTHING is wired into any environment by this change. Until an
 * environment sets the variable, every real DER token verifies false there. Stored tokens continue to verify through the
 * DB-row branch in `index.ts`, which this change does not touch.
 *
 * NOT CHECKED, deliberately, and named in the PR body: CRL/OCSP revocation, a TSA policy-OID
 * allowlist, and `accuracy`/`ordering`.
 */
import { webcrypto } from 'node:crypto';
import * as asn1js from 'asn1js';
import * as pkijs from 'pkijs';

const OID = {
  signedData: '1.2.840.113549.1.7.2',
  tstInfo: '1.2.840.113549.1.9.16.1.4',
  contentType: '1.2.840.113549.1.9.3',
  messageDigest: '1.2.840.113549.1.9.4',
  timeStamping: '1.3.6.1.5.5.7.3.8',
  extKeyUsage: '2.5.29.37',
  // KS-1404: the ESS signing-certificate attributes. PRIOR BEHAVIOUR: neither OID appeared in this
  // file at all, so probe PF8 ACCEPTED a token carrying no binding between the SignerInfo and the
  // certificate used to check it (RFC 3161 Sec 2.4.1, RFC 5816).
  signingCertificate: '1.2.840.113549.1.9.16.2.12',
  signingCertificateV2: '1.2.840.113549.1.9.16.2.47',
  // KS-1404: subjectKeyIdentifier, the second legal form of SignerIdentifier.
  subjectKeyIdentifier: '2.5.29.14',
  // KS-1404: signature algorithms the pinned providers measurably use. PRIOR BEHAVIOUR: absent from
  // SIG_ALG_BY_OID, so an rsaEncryption SignerInfo (PF6/PF11) and anything issued under the
  // rsassaPss-signed D-TRUST root were refused as "unsupported signature algorithm".
  rsaEncryption: '1.2.840.113549.1.1.1',
  rsaPss: '1.2.840.113549.1.1.10',
  sha1: '1.3.14.3.2.26',
} as const;

/**
 * KS-1404: hashes legal for an ESS certHash, kept SEPARATE from HASH_ALG_BY_OID on purpose.
 * HASH_ALG_BY_OID governs the MESSAGE IMPRINT, and SHA-1 must not become acceptable there. ESS v1
 * (`signingCertificate`) is defined as SHA-1 by RFC 2634, so the binding must be able to read one
 * without widening what a token may use to commit to the document.
 */
const ESS_HASH_BY_OID: Record<string, string> = {
  '1.3.14.3.2.26': 'SHA-1',
  '2.16.840.1.101.3.4.2.1': 'SHA-256',
  '2.16.840.1.101.3.4.2.2': 'SHA-384',
  '2.16.840.1.101.3.4.2.3': 'SHA-512',
};

const HASH_ALG_BY_OID: Record<string, string> = {
  '2.16.840.1.101.3.4.2.1': 'SHA-256',
  '2.16.840.1.101.3.4.2.2': 'SHA-384',
  '2.16.840.1.101.3.4.2.3': 'SHA-512',
};

interface SigAlg { importParams: webcrypto.AlgorithmIdentifier | webcrypto.EcKeyImportParams | webcrypto.RsaHashedImportParams; verifyParams: webcrypto.AlgorithmIdentifier | webcrypto.EcdsaParams; }
const SIG_ALG_BY_OID: Record<string, SigAlg> = {
  '1.2.840.113549.1.1.11': { importParams: { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, verifyParams: { name: 'RSASSA-PKCS1-v1_5' } },
  '1.2.840.113549.1.1.12': { importParams: { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-384' }, verifyParams: { name: 'RSASSA-PKCS1-v1_5' } },
  '1.2.840.113549.1.1.13': { importParams: { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-512' }, verifyParams: { name: 'RSASSA-PKCS1-v1_5' } },
  '1.2.840.10045.4.3.2': { importParams: { name: 'ECDSA', namedCurve: 'P-256' }, verifyParams: { name: 'ECDSA', hash: 'SHA-256' } },
  '1.2.840.10045.4.3.3': { importParams: { name: 'ECDSA', namedCurve: 'P-384' }, verifyParams: { name: 'ECDSA', hash: 'SHA-384' } },
};

/**
 * KS-1404: resolve the SignerInfo signature algorithm, including the two forms the fixed table above
 * cannot express. PRIOR BEHAVIOUR: a bare `SIG_ALG_BY_OID[oid]` lookup, so these were refused.
 *
 * `rsaEncryption` (1.2.840.113549.1.1.1) names RSA PKCS#1 v1.5 WITHOUT naming the digest, so the
 * digest comes from the SignerInfo's own `digestAlgorithm` field. DigiCert's published timestamping
 * CAs use rsaEncryption keys (measured 2026-10-04: 4 of the 5 published certificates read).
 *
 * `rsassaPss` (1.2.840.113549.1.1.10) carries its parameters, and they are PARSED here rather than
 * defaulted: RFC 4055's DEFAULTs are SHA-1 with a 20-byte salt, which is NOT what any current
 * authority uses, so silently defaulting would verify a signature against the wrong parameters or
 * refuse a valid one. An absent or unreadable parameter block is a refusal, not a guess. The pinned
 * D-TRUST Root CA 1 2017 is itself rsassaPss/4096 (measured), so every certificate it issues is
 * PSS-signed; pkijs 3.4.1's chain engine verifies such an issuer signature (measured, with a
 * tamper control that fails).
 */
function resolveSigAlg(si: pkijs.SignerInfo): { alg?: SigAlg; reason?: string } {
  const oid = si.signatureAlgorithm?.algorithmId;
  if (!oid) return { reason: 'SignerInfo carries no signature algorithm' };
  const fixed = SIG_ALG_BY_OID[oid];
  if (fixed) return { alg: fixed };

  if (oid === OID.rsaEncryption) {
    const dOid = si.digestAlgorithm?.algorithmId;
    const hash = dOid ? HASH_ALG_BY_OID[dOid] : undefined;
    if (!hash) {
      return { reason: `rsaEncryption SignerInfo has an unsupported digestAlgorithm (${dOid})` };
    }
    return {
      alg: {
        importParams: { name: 'RSASSA-PKCS1-v1_5', hash },
        verifyParams: { name: 'RSASSA-PKCS1-v1_5' },
      },
    };
  }

  if (oid === OID.rsaPss) {
    const raw = si.signatureAlgorithm?.algorithmParams;
    if (!raw) return { reason: 'rsassaPss signature carries no parameters (they are never defaulted)' };
    let params: pkijs.RSASSAPSSParams;
    try {
      params = new pkijs.RSASSAPSSParams({ schema: raw });
    } catch (e) {
      return { reason: `rsassaPss parameters did not parse: ${(e as Error)?.message ?? e}` };
    }
    const hOid = params.hashAlgorithm?.algorithmId;
    const hash = hOid ? HASH_ALG_BY_OID[hOid] : undefined;
    if (!hash) return { reason: `rsassaPss uses an unsupported hash algorithm (${hOid})` };
    const saltLength = params.saltLength;
    if (typeof saltLength !== 'number' || saltLength <= 0) {
      return { reason: `rsassaPss saltLength is absent or not positive (${String(saltLength)})` };
    }
    return {
      alg: {
        importParams: { name: 'RSA-PSS', hash },
        verifyParams: { name: 'RSA-PSS', saltLength } as webcrypto.AlgorithmIdentifier,
      },
    };
  }

  return { reason: `unsupported signature algorithm (${oid})` };
}

/**
 * KS-1404: the ESS signing-certificate binding. PRIOR BEHAVIOUR: not checked at all, so a token
 * could nominate one certificate in its SignerIdentifier and carry a different one, and probe PF8
 * accepted exactly that.
 *
 * pkijs 3.4.1 exports no SigningCertificate/ESSCertID classes (verified against the installed
 * package), so the attribute is parsed from its ASN.1 directly rather than through a helper that
 * does not exist.
 *   SigningCertificateV2 ::= SEQUENCE { certs SEQUENCE OF ESSCertIDv2, policies ... OPTIONAL }
 *   ESSCertIDv2 ::= SEQUENCE { hashAlgorithm AlgorithmIdentifier DEFAULT sha256,
 *                              certHash OCTET STRING, issuerSerial IssuerSerial OPTIONAL }
 *   ESSCertID   ::= SEQUENCE { certHash OCTET STRING, issuerSerial IssuerSerial OPTIONAL }  (SHA-1)
 * Only the FIRST ESSCertID(v2) is binding on the signer (RFC 5035 Sec 5.4).
 */
function parseEssFirstCertId(
  attrValue: unknown,
  isV2: boolean,
): { hashAlg?: string; certHash?: Buffer; serial?: asn1js.Integer; reason?: string } {
  const top = attrValue as { valueBlock?: { value?: unknown[] } } | undefined;
  const certsSeq = top?.valueBlock?.value?.[0] as { valueBlock?: { value?: unknown[] } } | undefined;
  const first = certsSeq?.valueBlock?.value?.[0] as { valueBlock?: { value?: unknown[] } } | undefined;
  const parts = first?.valueBlock?.value;
  if (!Array.isArray(parts) || parts.length === 0) {
    return { reason: 'ESS signing-certificate attribute carries no ESSCertID' };
  }
  let idx = 0;
  let hashAlg = isV2 ? 'SHA-256' : 'SHA-1';
  const head = parts[0] as { idBlock?: { tagNumber?: number }; valueBlock?: { value?: unknown[] } };
  // A leading SEQUENCE is the OPTIONAL hashAlgorithm (v2 only); otherwise the DEFAULT stands.
  if (isV2 && head?.idBlock?.tagNumber === 16) {
    try {
      const ai = new pkijs.AlgorithmIdentifier({ schema: parts[0] as never });
      const mapped = ESS_HASH_BY_OID[ai.algorithmId];
      if (!mapped) return { reason: `ESSCertIDv2 uses an unsupported hashAlgorithm (${ai.algorithmId})` };
      hashAlg = mapped;
    } catch (e) {
      return { reason: `ESSCertIDv2 hashAlgorithm did not parse: ${(e as Error)?.message ?? e}` };
    }
    idx = 1;
  }
  const hashNode = parts[idx] as { valueBlock?: { valueHexView?: Uint8Array } } | undefined;
  const view = hashNode?.valueBlock?.valueHexView;
  if (!view || view.length === 0) return { reason: 'ESSCertID certHash is absent or empty' };
  const certHash = Buffer.from(view);

  // issuerSerial is OPTIONAL. When present it is SEQUENCE { GeneralNames, CertificateSerialNumber }.
  let serial: asn1js.Integer | undefined;
  const isNode = parts[idx + 1] as { valueBlock?: { value?: unknown[] } } | undefined;
  const isParts = isNode?.valueBlock?.value;
  if (Array.isArray(isParts) && isParts.length >= 2) {
    serial = isParts[1] as asn1js.Integer;
  }
  return { hashAlg, certHash, serial };
}

export interface Rfc3161VerifyResult {
  valid: boolean;
  reason?: string;
  timestamp?: string;
  tsaCertificate?: { subject?: string; issuer?: string; validFrom: string; validTo: string };
}

const refuse = (reason: string): Rfc3161VerifyResult => ({ valid: false, reason });

/**
 * Any node anywhere in the tree encoded with BER indefinite length.
 *
 * 🔴 WHY THIS IS A SEPARATE, EXPLICIT CHECK rather than a canonical re-encoding test. asn1js RECORDS
 * the encoding form on `valueBlock.isIndefiniteForm` and REPRODUCES it on re-encode, so a GENUINE,
 * properly signed token re-wrapped as `30 80 ... 00 00` round-trips byte-identically. Measured
 * during red-first: a canonical-only guard ACCEPTED that forgery — it was vacuous for exactly the
 * case it was written to stop. The base accepts such a token too (node-forge's `asn1.fromDer` reads
 * BER), which is a widening of KS 1404 found while building the cells, not in the ticket's text.
 */
function findIndefinite(node: unknown, depth = 0): boolean {
  if (!node || depth > 40) return false;
  const vb = (node as { valueBlock?: { isIndefiniteForm?: boolean; value?: unknown[] } }).valueBlock;
  if (vb?.isIndefiniteForm === true) return true;
  if (Array.isArray(vb?.value)) {
    for (const kid of vb.value) if (findIndefinite(kid, depth + 1)) return true;
  }
  return false;
}

/** Strict DER. RFC 3161 tokens are DER: definite, minimal lengths, and nothing after the token. */
function parseStrictDer(der: Buffer): { asn?: asn1js.FromBerResult; error?: string } {
  if (der.length === 0) return { error: 'empty token' };
  if (der[0] !== 0x30) return { error: 'token is not a DER SEQUENCE' };
  const asn = asn1js.fromBER(der);
  if (asn.offset === -1) return { error: 'ASN.1 parse failed' };
  if (asn.offset !== der.length) return { error: `trailing bytes after the token (${der.length - asn.offset})` };
  if (findIndefinite(asn.result)) {
    return { error: 'token uses BER indefinite-length encoding; RFC 3161 tokens must be DER' };
  }
  const reencoded = Buffer.from(asn.result.toBER(false));
  if (!reencoded.equals(der)) return { error: 'token is not canonical DER (non-minimal length encoding)' };
  return { asn };
}

/**
 * CMS eContent is an OCTET STRING that may be CONSTRUCTED (segmented). pkijs then leaves
 * `valueBlock.valueHexView` EMPTY and puts the chunks in `valueBlock.value`.
 *
 * 🔴 Reading only the direct view sees ZERO bytes on a perfectly good token. Measured: a genuine
 * token is constructed, `valueHexView` 0 bytes, one 92-byte chunk. That made the GREEN control fail
 * AND made seven refusal cells pass for the wrong reason, all reporting "carries no eContent"
 * instead of the property they claim to test.
 */
function readEContent(e: unknown): Buffer | null {
  if (!e) return null;
  const vb = (e as { valueBlock?: { valueHexView?: Uint8Array; value?: Array<{ valueBlock: { valueHexView: Uint8Array } }> } }).valueBlock;
  const direct = vb?.valueHexView;
  if (direct && direct.byteLength > 0) return Buffer.from(direct);
  const chunks = vb?.value;
  if (Array.isArray(chunks) && chunks.length > 0) {
    return Buffer.concat(chunks.map((c) => Buffer.from(c.valueBlock.valueHexView)));
  }
  return null;
}

/** Parse a PEM bundle of trust anchors. A malformed anchor is skipped, not fatal. */
export function parseTrustAnchors(pem: string | undefined): pkijs.Certificate[] {
  if (!pem || !pem.trim()) return [];
  const out: pkijs.Certificate[] = [];
  for (const m of pem.matchAll(/-----BEGIN CERTIFICATE-----([\s\S]*?)-----END CERTIFICATE-----/g)) {
    const der = Buffer.from(m[1].replace(/\s+/g, ''), 'base64');
    const a = asn1js.fromBER(der);
    if (a.offset === -1) continue;
    try { out.push(new pkijs.Certificate({ schema: a.result })); } catch { /* skip a bad anchor */ }
  }
  return out;
}

export async function verifyRfc3161Token(opts: {
  tokenBase64: string;
  expectedHashHex: string;
  trustAnchorsPem?: string;
}): Promise<Rfc3161VerifyResult> {
  const anchors = parseTrustAnchors(opts.trustAnchorsPem);
  if (anchors.length === 0) return refuse('no trust anchor configured');

  let der: Buffer;
  try { der = Buffer.from(opts.tokenBase64, 'base64'); } catch { return refuse('token is not valid base64'); }
  const parsed = parseStrictDer(der);
  if (parsed.error || !parsed.asn) return refuse(parsed.error ?? 'token did not parse');

  let sd: pkijs.SignedData;
  try {
    const ci = new pkijs.ContentInfo({ schema: parsed.asn.result });
    if (ci.contentType !== OID.signedData) {
      return refuse(`ContentInfo is not id-signedData (${ci.contentType})`);
    }
    sd = new pkijs.SignedData({ schema: ci.content });
  } catch (e) { return refuse(`not a CMS SignedData: ${(e as Error)?.message ?? e}`); }

  if (sd.encapContentInfo?.eContentType !== OID.tstInfo) {
    return refuse(`eContentType is not id-ct-TSTInfo (${sd.encapContentInfo?.eContentType})`);
  }
  const eContent = readEContent(sd.encapContentInfo.eContent);
  if (!eContent || eContent.length === 0) return refuse('SignedData carries no eContent');

  if (!Array.isArray(sd.signerInfos) || sd.signerInfos.length !== 1) {
    return refuse(`expected exactly one SignerInfo, found ${sd.signerInfos?.length ?? 0}`);
  }
  const si = sd.signerInfos[0];

  let tst: pkijs.TSTInfo;
  try {
    const inner = asn1js.fromBER(eContent);
    if (inner.offset === -1) return refuse('TSTInfo did not parse');
    tst = new pkijs.TSTInfo({ schema: inner.result });
  } catch (e) { return refuse(`TSTInfo did not parse: ${(e as Error)?.message ?? e}`); }

  const algOid = tst.messageImprint?.hashAlgorithm?.algorithmId;
  const hashAlg = algOid ? HASH_ALG_BY_OID[algOid] : undefined;
  if (!hashAlg) return refuse(`unsupported message-imprint hash algorithm (${algOid})`);

  // The imprint is read from THIS field. That is the defect KS 1404 names.
  const imprint = Buffer.from(tst.messageImprint.hashedMessage.valueBlock.valueHexView);
  const expected = Buffer.from(opts.expectedHashHex, 'hex');
  if (imprint.length !== expected.length || !imprint.equals(expected)) {
    return refuse('message imprint in TSTInfo does not match the document hash');
  }

  const attrs = si.signedAttrs?.attributes ?? [];
  if (attrs.length === 0) return refuse('SignerInfo carries no signed attributes');
  const attr = (t: string) => attrs.find((a: pkijs.Attribute) => a.type === t);
  const ctAttr = attr(OID.contentType);
  if (!ctAttr || ctAttr.values?.[0]?.valueBlock?.toString() !== OID.tstInfo) {
    return refuse('signed contentType attribute is absent or not id-ct-TSTInfo');
  }
  const mdAttr = attr(OID.messageDigest);
  if (!mdAttr) return refuse('signed messageDigest attribute is absent');
  const declared = Buffer.from(mdAttr.values[0].valueBlock.valueHexView);
  const actual = Buffer.from(await webcrypto.subtle.digest(hashAlg, eContent));
  if (!declared.equals(actual)) return refuse('signed messageDigest does not match digest(eContent)');

  const certs = (sd.certificates ?? []).filter(
    (c: unknown): c is pkijs.Certificate => c instanceof pkijs.Certificate);
  if (certs.length === 0) return refuse('token carries no signer certificate');

  // KS-1404: select the signer by an EXACT SignerIdentifier match, in both legal forms.
  // PRIOR BEHAVIOUR: `... ?? certs[0]`, so a token whose SignerIdentifier matched NOTHING it carried
  // silently fell back to whatever certificate happened to be first, and the rest of the walk then
  // checked that certificate instead of the nominated one (kit doubt D5).
  const sidSerial = si.sid?.serialNumber;
  const bySerial = sidSerial
    ? certs.filter((c: pkijs.Certificate) =>
        c.issuer.isEqual(si.sid?.issuer) && c.serialNumber.isEqual(sidSerial))
    : [];
  // The second legal form, RFC 5652 Sec 5.3: subjectKeyIdentifier. `si.sid` is then an OCTET STRING.
  const sidSki = !sidSerial
    ? Buffer.from((si.sid as unknown as { valueBlock?: { valueHexView?: Uint8Array } })
        ?.valueBlock?.valueHexView ?? new Uint8Array())
    : Buffer.alloc(0);
  const bySki = sidSki.length > 0
    ? certs.filter((c: pkijs.Certificate) => {
        const ext = c.extensions?.find((e: pkijs.Extension) => e.extnID === OID.subjectKeyIdentifier);
        const v = ext?.parsedValue?.valueBlock?.valueHexView as Uint8Array | undefined;
        return !!v && Buffer.from(v).equals(sidSki);
      })
    : [];
  const matches = bySerial.length > 0 ? bySerial : bySki;
  if (matches.length === 0) {
    return refuse('SignerInfo identifies no certificate carried by the token');
  }
  const signer = matches[0];

  // KS-1404: the ESS signing-certificate binding. PRIOR BEHAVIOUR: absent, so nothing tied the
  // signed attributes to the certificate the signature was checked against, and PF8 accepted a token
  // with no binding at all. RFC 3161 Sec 2.4.1 requires it; RFC 5816 makes V2 the current form.
  // EXACTLY ONE of the two must be present: carrying both is ambiguous about which is binding.
  const scV2Attr = attr(OID.signingCertificateV2);
  const scV1Attr = attr(OID.signingCertificate);
  if (scV2Attr && scV1Attr) {
    return refuse('signed attributes carry BOTH signingCertificate and signingCertificateV2');
  }
  const essAttr = scV2Attr ?? scV1Attr;
  if (!essAttr) {
    return refuse('signed attributes carry no signingCertificate or signingCertificateV2');
  }
  const ess = parseEssFirstCertId(essAttr.values?.[0], !!scV2Attr);
  if (ess.reason || !ess.certHash || !ess.hashAlg) {
    return refuse(ess.reason ?? 'ESS signing-certificate attribute did not parse');
  }
  const signerDer = Buffer.from(signer.toSchema().toBER(false));
  const signerHash = Buffer.from(await webcrypto.subtle.digest(ess.hashAlg, signerDer));
  if (!signerHash.equals(ess.certHash)) {
    return refuse('ESS certHash does not match the hash of the selected signer certificate');
  }
  // issuerSerial is OPTIONAL; when present it must agree with the certificate it commits to.
  if (ess.serial && !signer.serialNumber.isEqual(ess.serial)) {
    return refuse('ESS issuerSerial does not match the selected signer certificate serial number');
  }

  const eku = signer.extensions?.find((e: pkijs.Extension) => e.extnID === OID.extKeyUsage);
  const purposes: string[] = eku?.parsedValue?.keyPurposes ?? [];
  if (!purposes.includes(OID.timeStamping)) {
    return refuse('signer certificate does not carry EKU id-kp-timeStamping');
  }

  const genTime = tst.genTime instanceof Date ? tst.genTime : new Date(tst.genTime as unknown as string);
  if (Number.isNaN(genTime.getTime())) return refuse('TSTInfo genTime is not a valid time');
  if (genTime < signer.notBefore.value || genTime > signer.notAfter.value) {
    return refuse('TSTInfo genTime falls outside the signer certificate validity window');
  }

  // The signature, verified DIRECTLY over the signed attributes re-encoded as SET OF.
  // RFC 5652 Sec 5.4: the signature covers the DER encoding of SignedAttributes with the IMPLICIT
  // [0] tag REPLACED BY SET OF, so byte 0 goes from 0xa0 to 0x31.
  //
  // 🔴 NOT pkijs's own SignedData.verify(): measured, it raises "TSTInfo wrong ASN.1 schema" on a
  // GENUINE token, because it re-reads eContent through the same direct `valueHexView` that is empty
  // for a constructed OCTET STRING. Delegating would have failed the GREEN control and made several
  // refusal cells pass for the wrong reason.
  // KS-1404: resolved through resolveSigAlg so rsaEncryption and rsassaPss are accepted with their
  // real parameters. PRIOR BEHAVIOUR: a bare table lookup, which refused both.
  const resolved = resolveSigAlg(si);
  if (!resolved.alg) return refuse(resolved.reason ?? `unsupported signature algorithm (${si.signatureAlgorithm?.algorithmId})`);
  const sigAlg = resolved.alg;

  const attrsDer = Buffer.from(si.signedAttrs!.toSchema().toBER(false));
  if (attrsDer.length === 0 || attrsDer[0] !== 0xa0) {
    return refuse('signed attributes are not encoded as IMPLICIT [0]');
  }
  const signedBytes = Buffer.concat([Buffer.from([0x31]), attrsDer.subarray(1)]);
  const signature = Buffer.from(si.signature.valueBlock.valueHexView);
  if (signature.length === 0) return refuse('SignerInfo carries no signature');

  let pubKey: webcrypto.CryptoKey;
  try {
    pubKey = await webcrypto.subtle.importKey(
      'spki',
      signer.subjectPublicKeyInfo.toSchema().toBER(false),
      sigAlg.importParams,
      false,
      ['verify'],
    );
  } catch (e) { return refuse(`signer public key could not be imported: ${(e as Error)?.message ?? e}`); }

  let sigOk = false;
  try {
    sigOk = await webcrypto.subtle.verify(sigAlg.verifyParams, pubKey, signature, signedBytes);
  } catch (e) { return refuse(`signature verification failed: ${(e as Error)?.message ?? e}`); }
  if (!sigOk) return refuse('signature over the signed attributes did not verify');

  // KS-1404: build the chain from the token's OWN certificates. PRIOR BEHAVIOUR: `certs: [signer]`,
  // so every intermediate the token carried was DROPPED and a signer issued by an intermediate could
  // never reach an anchor (probe PF5). Both pinned authorities issue through intermediates, so a
  // GENUINE token would never have verified — fail-closed, but non-functional.
  // `trustedCerts: anchors` stays the ONLY trust: an intermediate carried inside the token is
  // untrusted input, never an anchor, so adding them cannot make an unpinned chain verify.
  // 🔴 ORDER IS LOAD-BEARING: pkijs treats the LAST element of `certs` as the end-entity. Its own
  // documented example is `certs: [rootCa, intermediateCa, leafCert]`. Written `[signer, ...inters]`
  // the engine validates an INTERMEDIATE as the leaf, and a token whose signer chains to nothing is
  // ACCEPTED as long as some carried intermediate chains to an anchor. Cell CHAIN-3 caught exactly
  // that: it passed with the wrong order and refuses with this one.
  const intermediates = certs.filter((c: pkijs.Certificate) => c !== signer);
  const engine = new pkijs.CertificateChainValidationEngine({
    trustedCerts: anchors, certs: [...intermediates, signer], checkDate: genTime,
  });
  let chain: { result: boolean; resultMessage?: string };
  try { chain = await engine.verify(); } catch (e) {
    return refuse(`certificate chain did not validate: ${(e as Error)?.message ?? e}`);
  }
  if (!chain?.result) {
    return refuse(`signer certificate does not chain to a configured trust anchor${chain?.resultMessage ? `: ${chain.resultMessage}` : ''}`);
  }

  const cn = (x: pkijs.RelativeDistinguishedNames | undefined) =>
    x?.typesAndValues?.find((t: pkijs.AttributeTypeAndValue) => t.type === '2.5.4.3')
      ?.value?.valueBlock?.value as string | undefined;

  return {
    valid: true,
    timestamp: genTime.toISOString(),
    tsaCertificate: {
      subject: cn(signer.subject),
      issuer: cn(signer.issuer),
      validFrom: signer.notBefore.value.toISOString(),
      validTo: signer.notAfter.value.toISOString(),
    },
  };
}
