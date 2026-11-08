import sys
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator107/gen')
import brieflib
TIP='2935f723109756a60cadc5521977c7a036ec322d'
TEST='''import { describe, it, expect } from 'vitest';

// KS-1973: two catches of the credential verifier (src/vc/verifier.ts) still read a thrown value unguarded. (A) the catch of
// verifyIssuerDID builds `Failed to resolve DID <did>: ${error}` with a bare template literal, so a DID resolver that rejects
// with a revoked Proxy, a Symbol or an object whose toString throws makes verifyIssuerDID REJECT (and so verify()). (B) the inner
// Ed25519 catch of verifySignature reads `verifyErr instanceof Error ? verifyErr.message : String(verifyErr)`, so a hostile value
// thrown by the key decode makes that catch throw into the outer catch and the entry reads `Signature verification error: ...`
// instead of `Ed25519 verification error: ...`. The DID resolver stand-in is a plain function; for (B) the resolver answers a
// document whose publicKey is a Proxy that throws the cell's value when Buffer.from reads it; no network, no key material.
import { VerifiableCredentialVerifier } from '../vc/verifier';

type Result = { valid: boolean; errors: string[] };
type Priv = {
  verifyIssuerDID(c: unknown): Promise<Result>;
  verifySignature(c: unknown): Promise<Result>;
};

const credential = (proofValue: string) => ({
  '@context': ['https://www.w3.org/2018/credentials/v1'],
  type: ['VerifiableCredential'],
  issuer: 'did:example:issuer',
  issuanceDate: '2026-01-01T00:00:00Z',
  credentialSubject: { id: 'did:example:subject' },
  proof: {
    type: 'SecuuraSignature2024',
    created: '2026-01-01T00:00:00Z',
    verificationMethod: 'did:example:issuer#key-1',
    proofPurpose: 'assertionMethod',
    proofValue,
  },
});

/** The result, or the string 'rejected' when the call rejects (an assertion can then fail on it). */
async function issuerLookup(value: unknown): Promise<Result | 'rejected'> {
  const verifier = new VerifiableCredentialVerifier({ didResolver: () => Promise.reject(value) });
  try {
    return await (verifier as unknown as Priv).verifyIssuerDID(credential('zAAAA'));
  } catch {
    return 'rejected';
  }
}

async function signatureWithKey(publicKey: unknown): Promise<Result | 'rejected'> {
  const verifier = new VerifiableCredentialVerifier({ didResolver: () => Promise.resolve({ publicKey }) } as never);
  try {
    return await (verifier as unknown as Priv).verifySignature(credential('zAAAA'));
  } catch {
    return 'rejected';
  }
}

const throwingKey = (value: unknown): unknown =>
  new Proxy(
    {},
    {
      get() {
        throw value;
      },
    },
  );

const revokedProxy = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};

const toStringThrows = (): unknown => ({
  toString() {
    throw new Error('toString boom');
  },
});

const lookupEntry = (text: string): Result => ({ valid: false, errors: [`Failed to resolve DID did:example:issuer: ${text}`] });
const ED = 'Ed25519 verification error: ';

describe('KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely', () => {
  it('control ks1973 C1 an ordinary Error from the DID resolver gives the lookup entry with its text', async () => {
    expect(await issuerLookup(new Error('resolver down'))).toEqual(lookupEntry('Error: resolver down'));
  });

  it('control ks1973 C2 a thrown plain string from the DID resolver gives the lookup entry with that text', async () => {
    expect(await issuerLookup('plain text failure')).toEqual(lookupEntry('plain text failure'));
  });

  it('control ks1973 C3 an ordinary key decode failure gives the Ed25519 entry', async () => {
    const out = await signatureWithKey('00');
    expect(out).not.toBe('rejected');
    const errors = (out as Result).errors;
    expect(errors.length).toBe(1);
    expect(errors[0].startsWith(ED)).toBe(true);
  });

  it('RED ks1973 R1 a revoked Proxy from the DID resolver gives the lookup entry with a constant reason', async () => {
    expect(await issuerLookup(revokedProxy())).toEqual(lookupEntry('unreadable thrown value'));
  });

  it('RED ks1973 R2 an object whose toString throws from the DID resolver gives the lookup entry with a constant reason', async () => {
    expect(await issuerLookup(toStringThrows())).toEqual(lookupEntry('unreadable thrown value'));
  });

  it('RED ks1973 R3 a thrown Symbol from the DID resolver gives the lookup entry with its text', async () => {
    expect(await issuerLookup(Symbol('ks1973'))).toEqual(lookupEntry('Symbol(ks1973)'));
  });

  it('RED ks1973 R4 a revoked Proxy thrown by the key decode gives the Ed25519 entry with a constant reason', async () => {
    expect(await signatureWithKey(throwingKey(revokedProxy()))).toEqual({ valid: false, errors: [`${ED}unreadable thrown value`] });
  });

  it('RED ks1973 R5 an object whose toString throws, thrown by the key decode, gives the Ed25519 entry with a constant reason', async () => {
    expect(await signatureWithKey(throwingKey(toStringThrows()))).toEqual({ valid: false, errors: [`${ED}unreadable thrown value`] });
  });
});
'''
spec=dict(
 key='ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw',
 ticket='KS-1973', tag='ks1973', tip=TIP, area='shared',
 title='shared: the issuer-DID lookup catch and the inner Ed25519 catch of `src/vc/verifier.ts` must still report when the thrown value cannot be read (SECURITY SURFACE: credential verification, tier 1 gate owed)',
 origin='Origin: KS-1973 (gate 177 finding G177-F2, LOW, pre-existing): two catches near the one KS-1868 pull request 1993 guards are still unguarded, so with a resolver that throws an unreadable value `verify()` still REJECTS. Every affected cell fails CLOSED (a rejection or `valid: false`); none is more permissive than the ordinary-Error outcome. The fix shape is the ticket\'s own and the house guard of the merged KS-1868 passes (read inside a `try`, the constant `\'unreadable thrown value\'` on throw), inline, no helper.',
 product='packages/shared/src/vc/verifier.ts',
 test='packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts',
 ref='packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts',
 runner='vitest', runcmd='npx vitest run src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts', rundir='packages/shared',
 ctxn=2,
 edits=[("""              const msg = verifyErr instanceof Error ? verifyErr.message : String(verifyErr);
""","""              let msg: string;
              try {
                msg = verifyErr instanceof Error ? verifyErr.message : String(verifyErr);
              } catch {
                msg = 'unreadable thrown value';
              }
"""),("""        errors.push(`Failed to resolve DID ${issuerDID}: ${error}`);
""","""        let reason: string;
        try {
          reason = String(error);
        } catch {
          reason = 'unreadable thrown value';
        }
        errors.push(`Failed to resolve DID ${issuerDID}: ${reason}`);
""")],
 reds=[('R1',),('R2',),('R3',),('R4',),('R5',)], controls=[('C1',),('C2',),('C3',)],
 test_body=TEST,
 test_note='The shape is copied from the merged sibling suite of this directory (`ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts`; pinned ref the same file): the two private methods are reached through a type cast and the DID resolver is a plain function. For the Ed25519 catch the resolver answers `{ publicKey }` where `publicKey` is a Proxy whose get trap throws the cell\'s value: `Buffer.from(didDoc.publicKey, \'hex\')` reads `valueOf` on it, so the value is thrown from inside the inner try; the proof value `zAAAA` selects the Ed25519 branch.',
 wrong='(A) `verifyIssuerDID` catches a DID resolver failure and builds `Failed to resolve DID ${issuerDID}: ${error}` with a bare template literal: a thrown value whose text cannot be read (a revoked Proxy, an object whose toString throws, a Symbol) makes the template literal throw INSIDE the catch, so `verifyIssuerDID` and `verify()` REJECT instead of answering the error entry. (B) the inner Ed25519 catch of `verifySignature` reads `verifyErr instanceof Error ? verifyErr.message : String(verifyErr)` unguarded: for a hostile value that read throws into the outer (already guarded) catch, and the entry reads `Signature verification error: ...` instead of `Ed25519 verification error: ...`. The fix is the house guard in both places: (A) read the text inside its own `try` with `String(error)` (the same text the template literal produced for every readable value), the constant `\'unreadable thrown value\'` on throw; (B) the existing expression moves unchanged into a `try` with the same constant on throw.',
 where='line 400-402 (the inner Ed25519 catch of `verifySignature`: the `const msg` line) and line 458-460 (the catch of `verifyIssuerDID`: the `errors.push` line). CALLERS: `verify()` awaits both. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the error entry (`Failed to resolve DID <did>: <text>` / `Ed25519 verification error: <message>`) is pushed and the result is `valid: false`. Today (hostile value): (A) the call rejects, (B) the entry carries the wrong prefix. After: both give their normal entry with the constant text. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the verifier answers its normal error entry (A) instead of rejecting and (B) with the Ed25519 prefix instead of the generic one; every readable value reads exactly as before. The verifier stays fail-closed (both outcomes are `valid: false`). SECURITY SURFACE (credential verification): TIER 1 GATE OWED before any raise.',
 cells_text="""- RED at the tip, GREEN after: `R1` (a revoked Proxy), `R2` (an object whose toString throws) and `R3` (a thrown Symbol) from the DID resolver at the issuer lookup (A), and `R4` (a revoked Proxy) and `R5` (an object whose toString throws) thrown by the key decode at the Ed25519 catch (B) (5 cells). At the tip (A) rejects and (B) reads the wrong prefix, so the assertion fails; after the edit the normal entry carries the constant or the symbol's text.
- GREEN at the tip and after: 'control ks1973 C1' (an ordinary Error at the issuer lookup), 'C2' (a thrown plain string at the issuer lookup) and 'C3' (an ordinary key decode failure at the Ed25519 catch: the entry starts with the Ed25519 prefix), all already true at the tip (3 cells).
""",
 premises='- Premise: `verifier.ts` lines 320-464 read at `2935f7231097` (git show): the inner Ed25519 catch at 400-403, the guarded outer catch at 417-425, `verifyIssuerDID` at 433-464.\n- Ticket KS-1973 (Backlog, 0 comments) read whole at source on 2026-11-09. The outer catch template (line 424) and the identus-client / service-client / health-dashboard sites are KS-1974 and are NOT touched.',
 unmeasured='A real resolver or credential stack was not run; whether the Node `Buffer.from` reads `valueOf` on a Proxy publicKey is proved only by the `--control` run of the golden. The vc-issuer routes were not driven.',
 scope='Refs KS-1973; does NOT close KS-1974 (the non-string-message gap across four files), and introduces no new helper.',
 started_ok='KS-1973_gate177_finding_G177-F2;_security_surface_(vc_verifier)_tier_1_gate_owed;_operator_107_screen;_status_not_read_by_operator;_open_PRs_(44_PRs_295_files_read_2026-11-09_by_op107,_planted_control_services/originate_in_16_entries)_checked;_live_lanes_beyond_PRs_not_checked',
)
brieflib.make(spec)
