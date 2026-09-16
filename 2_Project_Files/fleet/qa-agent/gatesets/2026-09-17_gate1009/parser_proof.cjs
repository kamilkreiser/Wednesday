// parser_proof.cjs — #1009 P-1007-1 neutrality: typescript 5.9.3 transpileModule + AST on base (0308b7a04) vs head (6ec0cb198) ks864a/b.
// Proves (1) every it()/describe() call text is identical base vs head; (2) the TS2741 typing edit alone is type-only (transpile identical,
// with a control: a runtime edit differs); (3) the JS delta is exactly the import move + the dropped Promise arg.
const ts = require(process.argv[2]); const fs = require('fs'); const GS = process.argv[3];
const tr = (s) => ts.transpileModule(s, { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
function calls(src, names) { const sf = ts.createSourceFile('x.ts', src, ts.ScriptTarget.ES2022, true); const out = [];
  (function walk(n) { if (ts.isCallExpression(n) && ts.isIdentifier(n.expression) && names.includes(n.expression.text)) out.push(n.getText(sf)); ts.forEachChild(n, walk); })(sf); return out; }
const TYPE_OLD = 'let server: http.Server; let port = 0;'; const TYPE_NEW = "let server: ReturnType<ReturnType<typeof express>['listen']>; let port = 0;";
for (const f of ['ks864a-dead-estate-helper.test.ts', 'ks864b-dead-estate-portals.test.ts']) {
  const b = fs.readFileSync(`${GS}/src/base.${f}`, 'utf8'), h = fs.readFileSync(`${GS}/src/head.${f}`, 'utf8');
  const ib = calls(b, ['it']), ih = calls(h, ['it']); const eb = calls(b, ['expect']), eh = calls(h, ['expect']);
  console.log(f, '| it() calls base/head', ib.length, ih.length, 'identical', JSON.stringify(ib) === JSON.stringify(ih), '| expect() calls', eb.length, eh.length, 'identical', JSON.stringify(eb) === JSON.stringify(eh));
  if (b.split(TYPE_OLD).length !== 2) { console.log('  TYPE anchor count != 1'); continue; }
  const bt = b.replace(TYPE_OLD, TYPE_NEW);
  console.log('  type-only edit applied to base: transpile identical to base', tr(bt) === tr(b), '| source differs', bt !== b);
  const ctl = b.replace(TYPE_OLD, 'let server: http.Server; let port = 1;');
  console.log('  CONTROL runtime edit (port = 1): transpile identical', tr(ctl) === tr(b), '(must be false)');
  const jb = tr(b).split('\n'), jh = tr(h).split('\n'); const onlyB = jb.filter((l) => !jh.includes(l)), onlyH = jh.filter((l) => !jb.includes(l));
  console.log('  JS lines only in base:', JSON.stringify(onlyB)); console.log('  JS lines only in head:', JSON.stringify(onlyH));
  // Rebuild head from base by the two runtime edits only; after transpile it must equal head's
  const IMP = "const router = (await import('../routes/system-status')).default;\n\n";
  let r = bt.replace(IMP, '').replace('beforeAll(async () => {\n', "beforeAll(async () => {\n  const router = (await import('../routes/system-status')).default;\n").replace('r(); }); }, 10_000);\n}, 10_000);', 'r(); }); });\n}, 10_000);');
  console.log('  base + (type edit, import moved into beforeAll, dead arg dropped) === head source', r === h, '| transpile equal', tr(r) === tr(h));
}
