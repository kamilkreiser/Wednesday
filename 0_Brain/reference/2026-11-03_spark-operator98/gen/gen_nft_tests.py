import sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator98/gen/'
# k: (msg, status text, method, path, which service+member, async?, req expr)
S={
'p2':('Error fetching certificate','Failed to fetch NFT certificate','get','/certificates/:id',('minting','getNFTCertificate',True),"{ params: { id: 'c1' }, query: {}, body: {} }"),
'p3':('Error fetching certificates','Failed to fetch NFT certificates','get','/certificates',('minting','getUserNFTCertificates',True),"{ user: { userId: 'owner-ks1868' }, params: {}, query: {}, body: {} }"),
'p4':('Error fetching tiers','Failed to fetch storage tiers','get','/tiers',('minting','getQuickEstimate',False),"{ params: {}, query: {}, body: {} }"),
'p5':('Error estimating cost','Failed to estimate cost','post','/estimate',('minting','estimateCost',False),"{ params: {}, query: {}, body: { storageTier: 'basic', chain: 'cardano' } }"),
'p6':('Error verifying transaction','Failed to verify transaction','post','/verify/transaction',('verifier','verifyTransaction',True),"{ params: {}, query: {}, body: { txHash: 'a'.repeat(64) } }"),
'p7':('Error verifying asset','Failed to verify asset','post','/verify/asset',('verifier','verifyAsset',True),"{ params: {}, query: {}, body: { policyId: 'p1', assetNameHex: '6162' } }"),
'p8':('Error pinning CID','Failed to pin CID','post','/ipfs/pin',('ipfs','pin',True),"{ params: {}, query: {}, body: { cid: 'bafy1' } }"),
'p9':('Error unpinning CID','Failed to unpin CID','post','/ipfs/unpin',('ipfs','unpin',True),"{ params: {}, query: {}, body: { cid: 'bafy1' } }"),
}
for k,(msg,st,meth,path,(svc,member,asy),req) in S.items():
    fn = "() => Promise.reject(h.toThrow)" if asy else "() => {\n        throw h.toThrow;\n      }"
    mint = "{ %s: %s }"%(member,fn) if svc=='minting' else "{}"
    ver = "{ %s: %s }"%(member,fn) if svc=='verifier' else "{}"
    ipf = "{ %s: %s }"%(member,fn) if svc=='ipfs' else "{}"
    t=f"""import {{ describe, it, expect, vi }} from 'vitest';

// KS-1868: the nft-certificate router (src/routes/nft.routes.ts), handler `{meth.upper()} {path}`, logs a failure as
// `logger.error('{msg}', {{ error: error instanceof Error ? error.message : String(error) }})` and answers 500. The read is
// unguarded. When the thrown value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws)
// the catch itself throws, so the async handler REJECTS and no reply is sent. The services and the logger are plain stand-ins
// (the service call throws the cell's value); the handler is read off the router stack; no server, no network.
const h = vi.hoisted(() => ({{ toThrow: undefined as unknown, errors: [] as Array<[string, unknown]> }}));

vi.mock('../services/minting.service', () => ({{ nftMintingService: {mint} }}));
vi.mock('../services/blockchain-verifier.service', () => ({{ blockchainVerifier: {ver} }}));
vi.mock('../services/ipfs.service', () => ({{ ipfsService: {ipf} }}));
vi.mock('../services/cost-estimator.service', () => ({{ costEstimatorService: {{}} }}));
vi.mock('../services/metadata-builder.service', () => ({{ metadataBuilderService: {{}} }}));
vi.mock('../utils/logger', () => ({{
  logger: {{
    error: (m: string, meta: unknown) => {{
      h.errors.push([m, meta]);
    }},
    info: () => undefined,
    warn: () => undefined,
    debug: () => undefined,
  }},
}}));

import router from '../routes/nft.routes';

type Out = {{ rejected: boolean; code: number | undefined; body: unknown; logged: Array<[string, unknown]> }};

async function call(value: unknown): Promise<Out> {{
  h.toThrow = value;
  h.errors = [];
  const layer = (router as unknown as {{ stack: Array<{{ route?: {{ path: string; methods: Record<string, boolean>; stack: Array<{{ handle: (...a: unknown[]) => unknown }}> }} }}> }}).stack.find(
    (l) => l.route?.path === '{path}' && l.route.methods['{meth}'],
  );
  const handle = layer!.route!.stack[0].handle;
  const out: Out = {{ rejected: false, code: undefined, body: undefined, logged: [] }};
  const res = {{
    status(c: number) {{
      out.code = c;
      return res;
    }},
    json(b: unknown) {{
      out.body = b;
      return res;
    }},
  }};
  try {{
    await handle({req}, res);
  }} catch {{
    out.rejected = true;
  }}
  out.logged = h.errors;
  return out;
}}

const revokedProxy = (): unknown => {{
  const {{ proxy, revoke }} = Proxy.revocable({{}}, {{}});
  revoke();
  return proxy;
}};

const getterThrows = (): unknown =>
  Object.create(Error.prototype, {{
    message: {{
      get() {{
        throw new Error('getter boom');
      }},
    }},
  }});

const reply = {{ success: false, error: {{ code: 'INTERNAL_ERROR', message: '{st}' }} }};

describe('KS-1868 nft router {meth.upper()} {path} reads a thrown value safely', () => {{
  it('control ks1868 C1 an ordinary Error is logged with its message and answered 500', async () => {{
    const out = await call(new Error('service boom'));
    expect(out.rejected).toBe(false);
    expect(out.code).toBe(500);
    expect(out.body).toEqual(reply);
    expect(out.logged).toEqual([['{msg}', {{ error: 'service boom' }}]]);
  }});

  it('control ks1868 C2 a thrown plain string is logged as text and answered 500', async () => {{
    const out = await call('plain text failure');
    expect(out.rejected).toBe(false);
    expect(out.code).toBe(500);
    expect(out.body).toEqual(reply);
    expect(out.logged).toEqual([['{msg}', {{ error: 'plain text failure' }}]]);
  }});

  it('RED ks1868 R1 a revoked Proxy is logged with a constant reason and answered 500', async () => {{
    const out = await call(revokedProxy());
    expect(out.rejected).toBe(false);
    expect(out.code).toBe(500);
    expect(out.body).toEqual(reply);
    expect(out.logged).toEqual([['{msg}', {{ error: 'unreadable thrown value' }}]]);
  }});

  it('RED ks1868 R2 an Error whose message getter throws is logged with a constant reason and answered 500', async () => {{
    const out = await call(getterThrows());
    expect(out.rejected).toBe(false);
    expect(out.code).toBe(500);
    expect(out.body).toEqual(reply);
    expect(out.logged).toEqual([['{msg}', {{ error: 'unreadable thrown value' }}]]);
  }});
}});
"""
    open(G+f't98_{k}.ts.txt','w').write(t)
