// drafter_commentonly.js — item 4 by PARSER: TypeScript printer with removeComments over the r1 (616c766a5) and r2 (9ba0caf78) blobs; node-kind sequence
// compare as a second instrument. Controls: a TYPE-ONLY edit must be flagged; a comment-only edit must not. Run with cwd inside the drafter clone
// (require('typescript') resolves from its farm). Reads the blobs saved by git_read.sh (src/R1.* and src/H.*). Writes nothing.
const ts = require(require.resolve('typescript', { paths: [process.cwd()] })); const fs = require('fs'); // QA-EDIT-RESOLVE-FROM-CWD (cwd = the drafter clone)
const S = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2/src/';
const pr = ts.createPrinter({ removeComments: true });
const print = (name, text) => pr.printFile(ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS));
const kinds = (name, text) => { const out = []; const sf = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS); const walk = (n) => { out.push(ts.SyntaxKind[n.kind] + (ts.isIdentifier(n) || ts.isStringLiteral(n) || ts.isNumericLiteral(n) ? ':' + n.text : '')); ts.forEachChild(n, walk); }; walk(sf); return out.join('|'); };
const same = (a, b, n) => ({ printed: print(n, a) === print(n, b), kinds: kinds(n, a) === kinds(n, b) });
const count = (s, a) => s.split(a).length - 1;
console.log('typescript', ts.version, new Date().toString());
const e1 = fs.readFileSync(S + 'R1.services_enforcement.ts', 'utf8'), e2 = fs.readFileSync(S + 'H.services_enforcement.ts', 'utf8');
console.log('enforcement.ts r1 vs r2 (raw equal?', e1 === e2, ')', JSON.stringify(same(e1, e2, 'e.ts')));
const A1 = 'export function meetsVerificationLevel(userLevel: string, requiredLevel: string): boolean {';
if (count(e2, A1) !== 1) throw new Error('anchor A1 count ' + count(e2, A1));
const eType = e2.replace(A1, 'export function meetsVerificationLevel(userLevel: string | undefined, requiredLevel: string): boolean {');
console.log('CONTROL type-only edit (userLevel: string | undefined) flagged:', JSON.stringify(same(e2, eType, 'e.ts')), '(expect both false)');
const A2 = '// unchanged; so is an unknown REQUIRED level (KS-1190).';
if (count(e2, A2) !== 1) throw new Error('anchor A2 count ' + count(e2, A2));
const eCom = e2.replace(A2, '// unchanged; so is an unknown REQUIRED level (KS-1190). QA comment-only control.');
console.log('CONTROL comment-only edit not flagged:', JSON.stringify(same(e2, eCom, 'e.ts')), '(expect both true)');
const t1 = fs.readFileSync(S + 'R1.ks1176.test.ts', 'utf8'), t2 = fs.readFileSync(S + 'H.ks1176.test.ts', 'utf8');
console.log('ks1176 test r1 vs r2 whole file:', JSON.stringify(same(t1, t2, 't.ts')), '(expect false: describe F is code)');
// the header = everything before the first import; hybrid = r1 with r2's header — must print identically to r1
const H1 = t1.slice(0, t1.indexOf('import ')), H2 = t2.slice(0, t2.indexOf('import '));
console.log('header chars r1', H1.length, 'r2', H2.length, 'header lines all comments r2:', H2.split('\n').every((l) => l.trim() === '' || l.trim().startsWith('//')));
const hybrid = H2 + t1.slice(t1.indexOf('import '));
console.log('ks1176 test: r1 with r2 header vs r1:', JSON.stringify(same(t1, hybrid, 't.ts')), '(expect both true: the header change is comment-only)');
// the rest of the r1->r2 test delta, by printed statement set
const stm = (t) => ts.createSourceFile('t.ts', t, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS).statements.map((s) => pr.printNode(ts.EmitHint.Unspecified, s, ts.createSourceFile('x.ts', '', ts.ScriptTarget.Latest)));
const s1 = stm(t1), s2 = stm(t2); const added = s2.filter((x) => !s1.includes(x)), removed = s1.filter((x) => !s2.includes(x));
console.log('top-level statements r1', s1.length, 'r2', s2.length, '| changed/added in r2:', added.length, '| removed from r1:', removed.length);
for (const a of added) console.log('   + ' + a.replace(/\s+/g, ' ').slice(0, 150));
for (const r of removed) console.log('   - ' + r.replace(/\s+/g, ' ').slice(0, 150));
const v1 = fs.readFileSync(S + 'R1.routes_verification.ts', 'utf8'), v2 = fs.readFileSync(S + 'H.routes_verification.ts', 'utf8');
console.log('verification.ts r1 vs r2:', JSON.stringify(same(v1, v2, 'v.ts')), '(expect false: the fix is code)');
