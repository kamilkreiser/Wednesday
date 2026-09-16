// parser_proof.cjs — READ ONLY (require of the checkout's typescript; files read from the gate set's src/ copies).
// P1: the ragged indentation is behaviour-neutral: head verification.ts vs a RE-INDENTED copy (lines 995-1011 of the Promise wrapper
//     body shifted to consistent depth) — transpileModule(removeComments) byte compare + AST leaf walk (kind + text), diagnostics.
// Controls: C1 whitespace-only (the re-indent itself) must be IDENTICAL; C2 resolveStatus moved INSIDE the 'end' listener must DIFFER
//     on both; C3 type-only (`forwardStatus: number` -> `forwardStatus`) transpile IDENTICAL, AST DIFFERS (the transpile blind spot);
//     C4 the 502 `status: forwardStatus` key removed must DIFFER on both.
// P2: the READY hunk's -/+ lines for verification.ts vs the applied diff's -/+ lines (multisets, whitespace kept).
const ts = require('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules/typescript');
const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008';
console.log('parser_proof', new Date().toString(), 'typescript', ts.version);
const head = fs.readFileSync(G + '/src/verification_head.ts', 'utf8');
function emit(src) { const r = ts.transpileModule(src, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, removeComments: true }, reportDiagnostics: true, fileName: 'v.ts' }); return { out: r.outputText, diags: (r.diagnostics || []).length }; }
function leaves(src) { const sf = ts.createSourceFile('v.ts', src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS); const a = []; (function w(n) { const k = n.getChildren(sf); if (k.length === 0) { if (n.kind !== ts.SyntaxKind.EndOfFileToken) a.push(n.kind + ':' + n.getText(sf)); } else k.forEach(w); })(sf); return a; }
function cmp(label, a, b, want) {
  const ea = emit(a), eb = emit(b), la = leaves(a), lb = leaves(b);
  const tEq = ea.out === eb.out; let aEq = la.length === lb.length && la.every((x, i) => x === lb[i]);
  const got = (tEq ? 'T=' : 'T!') + (aEq ? 'A=' : 'A!');
  console.log(label.padEnd(58), 'transpile', tEq ? 'IDENTICAL' : 'DIFFERS', '| AST', aEq ? 'IDENTICAL' : 'DIFFERS', la.length + '/' + lb.length, '| diags', ea.diags + '/' + eb.diags, '| expected', want, got === want ? 'OK' : 'UNEXPECTED');
}
const L = head.split('\n');
// 1-based lines 994..1012 are the wrapper; print them with visible indentation widths
for (let i = 994; i <= 1012; i++) console.log(String(i).padStart(5), String(L[i - 1].match(/^ */)[0].length).padStart(3), L[i - 1]);
const re = L.slice();
for (let i = 996; i <= 1011; i++) re[i - 1] = '  ' + re[i - 1];   // shift the wrapper body one level deeper
re[1003 - 1] = re[1003 - 1].replace(/^ +/, ' '.repeat(12));       // resolveStatus to the callback-body depth
const reindented = re.join('\n');
fs.writeFileSync(G + '/src/verification_head_reindented.ts', reindented);
for (let i = 994; i <= 1012; i++) console.log('RE' + String(i).padStart(3), String(re[i - 1].match(/^ */)[0].length).padStart(3), re[i - 1]);
cmp('P1/C1 head vs re-indented copy (whitespace only)', head, reindented, 'T=A=');
const anchorC2a = "              resolveStatus(proxyRes.statusCode || 0);\n";
const anchorC2b = "              log('info', 'Workflow approved — document forwarded to originate', { documentId });\n";
if (head.split(anchorC2a).length !== 2 || head.split(anchorC2b).length !== 2) { console.log('ANCHOR COUNT != 1 for C2'); process.exit(3); }
const c2 = head.replace(anchorC2a, '').replace(anchorC2b, anchorC2b + '              resolveStatus(proxyRes.statusCode || 0);\n');
cmp('C2 resolveStatus moved inside the end listener', head, c2, 'T!A!');
const a3 = 'const forwardStatus: number = await'; if (head.split(a3).length !== 2) { console.log('ANCHOR COUNT != 1 for C3'); process.exit(3); }
cmp('C3 type-only: `: number` removed', head, head.replace(a3, 'const forwardStatus = await'), 'T=A!');
const a4 = ', status: forwardStatus } });'; if (head.split(a4).length !== 2) { console.log('ANCHOR COUNT != 1 for C4'); process.exit(3); }
cmp('C4 502 body `status` key removed', head, head.replace(a4, ' } });'), 'T!A!');
// P2
const ready = fs.readFileSync('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1087_ornith35b-q4_PASS-7of7_2026-09-15.diff.md', 'utf8');
const rv = ready.split('--- /dev/null')[0];
const applied = fs.readFileSync(G + '/diff_U0_verification.patch', 'utf8');
function pm(t) { const m = [], p = []; for (const l of t.split('\n')) { if (l.startsWith('---') || l.startsWith('+++')) continue; if (l.startsWith('-')) m.push(l.slice(1)); else if (l.startsWith('+')) p.push(l.slice(1)); } return { m, p }; }
const R = pm(rv), A = pm(applied);
console.log('READY verification.ts hunk: -%d +%d | applied (git diff -U0 develop..head): -%d +%d', R.m.length, R.p.length, A.m.length, A.p.length);
const cancel = R.m.filter(x => R.p.includes(x));
console.log('READY lines both removed and re-added (cancel as context):', JSON.stringify(cancel));
function strip(arr, rm) { const a = arr.slice(); for (const x of rm) { const i = a.indexOf(x); if (i >= 0) a.splice(i, 1); } return a; }
const Rm = strip(R.m, cancel), Rp = strip(R.p, cancel);
const eq = (x, y) => JSON.stringify(x.slice().sort()) === JSON.stringify(y.slice().sort());
const eqOrder = (x, y) => JSON.stringify(x) === JSON.stringify(y);
console.log('READY minus cancelled vs applied: minus multiset', eq(Rm, A.m) ? 'EQUAL' : 'DIFFERS', '| plus multiset', eq(Rp, A.p) ? 'EQUAL' : 'DIFFERS', '| plus in order', eqOrder(Rp, A.p) ? 'EQUAL' : 'DIFFERS');
// control: a one-byte change to one applied + line must read DIFFERS
const Ap2 = A.p.slice(); Ap2[0] = Ap2[0] + ' ';
console.log('P2 control (one trailing space on the first applied + line):', eq(Rp, Ap2) ? 'EQUAL (UNEXPECTED)' : 'DIFFERS (OK)');
