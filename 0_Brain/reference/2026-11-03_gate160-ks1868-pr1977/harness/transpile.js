// G160: transpile the real base/head auth sources (extracted by blob) verbatim with the clone's typescript.
const fs = require('fs');
const path = require('path');
const W = path.resolve(__dirname, '..');
const ts = require(path.join(W, 'repo/Blockchain/Dev/node_modules/typescript'));
for (const v of ['base', 'head']) {
  const src = path.join(__dirname, 'src_' + v);
  const out = path.join(__dirname, 'build_' + v);
  const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
  for (const f of walk(src)) {
    const rel = path.relative(src, f).replace(/\.ts$/, '.js');
    const r = ts.transpileModule(fs.readFileSync(f, 'utf8'), {
      compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS, esModuleInterop: true },
      fileName: f,
    });
    fs.mkdirSync(path.dirname(path.join(out, rel)), { recursive: true });
    fs.writeFileSync(path.join(out, rel), r.outputText);
    console.log(v, rel, r.outputText.length);
  }
}
console.log('typescript', ts.version);
