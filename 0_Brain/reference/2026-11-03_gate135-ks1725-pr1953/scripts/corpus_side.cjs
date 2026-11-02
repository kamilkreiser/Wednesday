// Gate 135: evaluate every z-expression in the REAL source of one tree (base or head),
// parse a generated corpus, and print issues (base: raw zod 3 issues; head: zod3Issues(zod 4 issues)).
// usage: node corpus_side.cjs <base|head> <DevDir> <outJson> [inputsJson]
const path = require('path'), fs = require('fs'), { createRequire } = require('module');
const [side, DEV, OUT, INPUTS] = process.argv.slice(2);
const req = createRequire(path.join(DEV, 'package.json'));
const ts = req('typescript');
let compat = null;
if (side === 'head') {
  compat = require(path.join(DEV, 'packages/shared/dist/validation/zod3-compat.js')); // installs the global map
  if (process.env.G135_FIX) { // gate 135 candidate fixes, applied in-process only (the repo is not edited)
    const zz = require(path.join(DEV, 'node_modules/zod')).z;
    compat.zod3Datetime = (options = {}) => { const re = compat.zod3DatetimeRegex({ precision: options.precision === undefined ? null : options.precision, offset: options.offset ?? false, local: options.local ?? false }); const m = options.message; return zz.stringFormat('datetime', (v) => re.test(v), m === undefined ? undefined : { error: (iss) => (iss.code === 'invalid_format' ? m : undefined) }); };
    const orig = compat.zod3Issues;
    const same = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
    compat.zod3Issues = (issues, prefix) => {
      const out = orig(issues, prefix);
      // F2: zod 3 never ran a length check after a type failure at the same path
      const typed = out.filter((i) => i.code === 'invalid_type' && i.expected !== 'integer').map((i) => i.path);
      let res = out.filter((i) => !((i.code === 'too_small' || i.code === 'too_big') && typed.some((p) => same(p, i.path))));
      // F3a: zod 3 put an array's own length issue before its elements' issues
      for (let k = 0; k < res.length; k++) { const i = res[k]; if ((i.code === 'too_small' || i.code === 'too_big') && i.type === 'array') { const first = res.findIndex((j) => j.path.length > i.path.length && same(j.path.slice(0, i.path.length), i.path)); if (first !== -1 && first < k) { res.splice(k, 1); res.splice(first, 0, i); } } }
      return res;
    };
  }
}
const zmod = req('zod'); const z = zmod.z || zmod;
req('@asteasolutions/zod-to-openapi').extendZodWithOpenApi(z);
let shared = {}; try { shared = require(path.join(DEV, 'packages/shared/dist/index.js')); } catch (e) { console.error('shared index load failed', String(e).slice(0, 200)); }
const ROOT = path.resolve(DEV, '..', '..');
const files = require('child_process').execSync(
  `git -C "${ROOT}" ls-files 'Blockchain/Dev/services/*/src/*.ts' 'Blockchain/Dev/services/*/src/**/*.ts' 'Blockchain/Dev/packages/shared/src/**/*.ts' 'Blockchain/Dev/packages/shared/src/*.ts' 'Blockchain/Dev/frontend/issuer/src/**/*.ts'`,
  { encoding: 'utf8', maxBuffer: 1 << 26 }).split('\n').filter((f) => f && !/__tests__|\.test\.ts$|\.spec\.ts$|\.d\.ts$|zod3-compat\.ts$/.test(f));
const isZroot = (n) => ts.isIdentifier(n) && n.text === 'z';
function rootOf(n) { while (ts.isCallExpression(n) || ts.isPropertyAccessExpression(n) || ts.isNonNullExpression(n)) n = n.expression; return n; }
function isZchain(n) { return (ts.isCallExpression(n) || ts.isPropertyAccessExpression(n)) && isZroot(rootOf(n)); }
const tr = (code) => ts.transpileModule(code, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.None, removeComments: true } }).outputText;
const results = []; const exprs = [];
for (const rel of files) {
  const src = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  if (!/\bz\./.test(src)) continue;
  const sf = ts.createSourceFile(rel, src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  // scope: top-level consts + enums
  const scope = Object.assign(Object.create(null), shared, { z, zod3Datetime: compat && compat.zod3Datetime, zod3Error: compat && compat.zod3Error });
  const stmts = sf.statements.filter((s) => ts.isVariableStatement(s) || ts.isEnumDeclaration(s));
  for (let pass = 0; pass < 2; pass++) for (const s of stmts) {
    try {
      if (ts.isEnumDeclaration(s)) { const js = tr(s.getText().replace(/^export\s+/, '').replace(/^const\s+enum/, 'enum')); new Function('scope', `with(scope){ ${js}; scope[${JSON.stringify(s.name.text)}] = ${s.name.text}; }`)(scope); continue; }
      for (const d of s.declarationList.declarations) {
        if (!ts.isIdentifier(d.name) || !d.initializer) continue;
        if (pass === 1 && d.name.text in scope) continue;
        const js = tr('(' + d.initializer.getText() + ')').trim().replace(/;$/, '');
        scope[d.name.text] = new Function('scope', `with(scope){ return ${js}; }`)(scope);
      }
    } catch (e) { /* unresolved import: skipped */ }
  }
  // every maximal z-chain
  let ord = 0;
  const visit = (n) => {
    if (isZchain(n) && !(n.parent && (ts.isPropertyAccessExpression(n.parent) && n.parent.expression === n || ts.isCallExpression(n.parent) && n.parent.expression === n))) {
      const text = n.getText(); if (/^z\s*\.\s*config\b/.test(text)) return; const line = sf.getLineAndCharacterOfPosition(n.getStart()).line + 1;
      let schema = null, err = null;
      try { const js = tr('(' + text + ')').trim().replace(/;$/, ''); schema = new Function('scope', `with(scope){ return ${js}; }`)(scope); if (!schema || typeof schema.safeParse !== 'function') { err = 'not a schema'; schema = null; } } catch (e) { err = String(e && e.message || e).slice(0, 120); }
      exprs.push({ id: `${rel}#${ord}`, rel, ord, line, text, schema, err });
      ord++;
      return; // do not descend: nested chains are inside this one
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
}
// ---------- corpus generation (base side only) ----------
const HEX64 = 'a'.repeat(64);
const PALETTE = [null, 0, 1, -1, -1.5, 1.5, 2 ** 53, -(2 ** 53), 1e21, true, false, '', ' ', 'x', 'X', '   padded   ', 'a'.repeat(300), 'a'.repeat(5001),
  'user@example.com', 'not-an-email', 'a@b', '"q"@example.com', 'user@[127.0.0.1]', 'user@sub.example.co', 'user.name+tag@example.com', 'us..er@example.com', "o'brien@example.com", 'user@-example.com', 'ü@example.com',
  'https://example.com', 'http//bad', 'ftp://example.com/x', 'javascript:alert(1)', 'mailto:a@b.c', 'https://localhost:3000/cb', 'example.com', 'https://', 'http://a',
  '12345678-1234-4234-8234-123456789abc', '12345678-1234-0234-8234-123456789abc', '12345678-1234-4234-c234-123456789abc', '00000000-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000000', 'ffffffff-ffff-ffff-ffff-ffffffffffff', '12345678123442348234123456789abc', '{12345678-1234-4234-8234-123456789abc}',
  '2026-11-02T10:00Z', '2026-11-02T10:00:00Z', '2026-11-02T10:00:00.123Z', '2026-11-02T10:00:00+10:00', '2026-11-02T10:00+10:00', '2026-11-02T10:00:00', '2026-11-02', '2026-02-30T10:00:00Z', 'not-a-date',
  HEX64, HEX64.toUpperCase(), 'g'.repeat(64), 'abc', '5', '-5', '1.5', 'Infinity', '-Infinity', '1e400', 'NaN', '0x10', 'true', 'false', '1', '0',
  [], ['x'], [1], ['a', 'b', 'c'], Array.from({ length: 60 }, (_, i) => 'v' + i), {}, { a: 1 }, { id: 'x' }, { id: 5 }, { '': 'x' }];
function unwrap3(s) { let d = s && s._def; for (let i = 0; i < 10 && d; i++) { const t = d.typeName; if (t === 'ZodOptional' || t === 'ZodNullable' || t === 'ZodDefault' || t === 'ZodCatch' || t === 'ZodReadonly' || t === 'ZodBranded') { s = d.innerType || d.type; d = s && s._def; continue; } if (t === 'ZodEffects') { s = d.schema; d = s._def; continue; } if (t === 'ZodPipeline') { s = d.in; d = s._def; continue; } if (t === 'ZodLazy') { s = d.getter(); d = s._def; continue; } break; } return s; }
function shapeOf(s) { const u = unwrap3(s); if (u && u._def && u._def.typeName === 'ZodObject') return u._def.shape(); return null; }
function fieldValid(fs_) { for (const v of PALETTE) { try { if (fs_.safeParse(v).success) return { ok: true, v }; } catch {} } return { ok: false }; }
function genInputs(schema) {
  const ins = [{ __undef: true }, null, 42, 'str', [], {}, true, -1.5, 'Infinity', 2 ** 53];
  const shape = shapeOf(schema);
  if (!shape) { for (const v of PALETTE) ins.push(v); return ins; }
  const keys = Object.keys(shape);
  const valid = {};
  for (const k of keys) { const r = fieldValid(shape[k]); if (r.ok && r.v !== undefined) valid[k] = r.v; }
  ins.push(valid);
  ins.push({ ...valid, __extra_key__: 1 });
  for (const v of PALETTE) { const o = {}; for (const k of keys) o[k] = v; ins.push(o); }
  for (const k of keys) {
    for (const v of PALETTE) { const o = { ...valid }; o[k] = v; ins.push(o); }
    const o = { ...valid }; delete o[k]; ins.push(o);
    const sub = shapeOf(shape[k]);
    if (sub) for (const v of [null, 1, '', 'x', -1.5, 2 ** 53, '2026-11-02T10:00Z', '12345678-1234-0234-8234-123456789abc', []]) { const so = {}; for (const sk of Object.keys(sub)) so[sk] = v; const oo = { ...valid }; oo[k] = so; ins.push(oo); }
  }
  return ins;
}
let inputs;
if (side === 'base') { inputs = {}; for (const e of exprs) if (e.schema) { try { inputs[e.id] = genInputs(e.schema); } catch (er) { inputs[e.id] = PALETTE; } } fs.writeFileSync(OUT.replace(/\.json$/, '.inputs.json'), JSON.stringify(inputs)); }
else { const raw = JSON.parse(fs.readFileSync(INPUTS, 'utf8')); const pm = process.argv[6] ? JSON.parse(fs.readFileSync(process.argv[6], 'utf8')) : null; inputs = {}; for (const e of exprs) { const bid = pm ? pm[e.id] : e.id; if (bid && raw[bid]) inputs[e.id] = raw[bid]; } }
const ser = (issues) => side === 'head' ? compat.zod3Issues(issues) : issues;
const out = {};
for (const e of exprs) {
  const rec = { line: e.line, text: e.text.length > 400 ? e.text.slice(0, 400) + '…' : e.text, err: e.err, cells: null };
  if (e.schema && inputs[e.id]) {
    rec.cells = inputs[e.id].map((inp) => {
      const v = inp && inp.__undef ? undefined : inp;
      try {
        const r = e.schema.safeParse(v);
        if (r.success) return 'OK ' + JSON.stringify(r.data === undefined ? '__undefined' : r.data);
        return 'ERR ' + JSON.stringify(ser(r.error.issues));
      } catch (er) { return 'THROW ' + String(er && er.message).slice(0, 200); }
    });
  }
  out[e.id] = rec;
}
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(side, 'files', files.length, 'exprs', exprs.length, 'evaluated', exprs.filter((e) => e.schema).length);
