// G164: transpile the real security sources (extracted by blob) verbatim with the clone's typescript.
// argv: srcDir outDir  (default: base and head)
const fs = require('fs');
const path = require('path');
const W = path.resolve(__dirname, '..');
const ts = require(path.join(W, 'repo/Blockchain/Dev/node_modules/typescript'));
const pairs = process.argv[2] ? [[process.argv[2], process.argv[3]]] : ['base', 'head'].map((v) => [path.join(__dirname, 'src_' + v), path.join(__dirname, 'build_' + v)]);
for (const [src, out] of pairs) {
  const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
  for (const f of walk(src)) {
    if (!f.endsWith('.ts')) continue;
    const rel = path.relative(src, f).replace(/\.ts$/, '.js');
    const r = ts.transpileModule(fs.readFileSync(f, 'utf8'), { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS, esModuleInterop: true }, fileName: f });
    fs.mkdirSync(path.dirname(path.join(out, rel)), { recursive: true });
    fs.writeFileSync(path.join(out, rel), r.outputText);
  }
  console.log('built', out);
}
console.log('typescript', ts.version);
