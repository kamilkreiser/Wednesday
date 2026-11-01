# Build Q2 probes from the PR's own register/login harness (everything before `describe(`), with a recording describe.
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911'
T=G+'/repo/Blockchain/Dev/services/auth/src/__tests__/'
tail='''
import { appendFileSync } from 'fs';
const KINDS: Record<string, () => unknown> = {
  none: () => undefined,
  ordinary: () => new Error('bus down'),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};
describe('gate93 q2 probe', () => {
  for (const k of Object.keys(KINDS)) {
    it(k, async () => {
      h.publishRejects = k !== 'none'; h.toThrow = KINDS[k]();
      const res = await fetch(baseUrl + PATH, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: BODY });
      const text = await res.text();
      await settled();
      const sc = res.headers.get('set-cookie');
      appendFileSync(process.env.PROBE_OUT as string, JSON.stringify({ case: k, status: res.status, body: text,
        setCookie: sc ? sc.replace(/=[^;]*/g, '=<v>') : null, unhandled: h.unhandled, lines: LINES().map((c) => c[1]) }) + '\\n');
    });
  }
});
'''
for name,src,path,body in [
  ('q2_register','ks1868-auth-register-publish-event-unreadable-throw.test.ts',"'/register'","JSON.stringify({ email: 'ks1868-register@example.com', password: 'Tr0ub4dor&3-horse-staple', name: 'Ann Lee' })"),
  ('q2_login','ks1868-auth-login-publish-event-unreadable-throw.test.ts',"'/api/auth/login'","JSON.stringify({ email: LOGIN_EMAIL, password: 'pw-correct-horse' })")]:
    s=open(T+src).read(); top=s[:s.index("describe('KS-1868")]
    open(G+f'/scripts/{name}.test.ts','w').write('// QA GATE 93 Q2 probe (NOT part of the PR): the PR test harness, recording full responses.\n'+top+f'const PATH = {path};\nconst BODY = {body};\n'+tail)
    print(name,'ok')
