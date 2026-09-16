// parser_proof.cjs — #1005: is the ONE product line the only non-comment delta in verification.ts? (1) transpileModule removeComments byte
// compare; (2) AST leaf walk (childless nodes, kind + text; JSDoc and EOF excluded). SUBJECT S0 = base vs head (must DIFFER: the product line);
// SUBJECT S1 = base vs head-with-ONLY-the-product-line-restored-to-base (must be IDENTICAL on both: every other delta is comment).
// Controls on the same instrument. Usage: node parser_proof.cjs <clone tree> <base.ts> <head.ts>
const [TREE, BP, HP] = process.argv.slice(2);
const ts = require(TREE + '/Blockchain/Dev/node_modules/typescript'); const fs = require('fs');
console.log('parser_proof', new Date().toString(), 'typescript', ts.version);
const tr = s => ts.transpileModule(s, { compilerOptions: { removeComments: true, target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS }, reportDiagnostics: false }).outputText;
function leaves(s) { const sf = ts.createSourceFile('x.ts', s, ts.ScriptTarget.Latest, true); const out = [];
  (function walk(n) { const k = n.getChildren(sf); if (k.length === 0) { if (!ts.isJSDoc(n) && n.kind !== ts.SyntaxKind.EndOfFileToken) out.push(ts.SyntaxKind[n.kind] + ':' + n.getText(sf)); } else k.forEach(walk); })(sf);
  return { out, diags: sf.parseDiagnostics.length }; }
let all = true;
function cmp(label, a, b, eTr, eAst) { const la = leaves(a), lb = leaves(b); const trS = tr(a) === tr(b);
  const astS = la.out.length === lb.out.length && la.out.every((x, i) => x === lb.out[i]);
  const ok = trS === eTr && astS === eAst; all = all && ok;
  console.log(`${label} | transpile identical ${trS} | AST leaves identical ${astS} (${la.out.length}/${lb.out.length}) | parse diags ${la.diags}/${lb.diags} | raw identical ${a === b} | expected tr=${eTr} ast=${eAst} -> ${ok ? 'OK' : 'MISMATCH'}`); }
function once(s, a, b) { const n = s.split(a).length - 1; if (n !== 1) throw new Error('anchor count ' + n + ' for ' + a.slice(0, 80)); return s.replace(a, b); }
const B = fs.readFileSync(BP, 'utf8'), H = fs.readFileSync(HP, 'utf8');
const PL_H = "      (persistedStatus === 'confirmed' || (persistedStatus == null && (doc as any)._source !== 'anchor_store')), // KS-1073: carve-out tier-1 only; anchor-store rows are never statusless\n";
const PL_B = "      (persistedStatus === 'confirmed' || persistedStatus == null),\n";
console.log('product line: head count', H.split(PL_H).length - 1, '| base line in base count', B.split(PL_B).length - 1);
const H1 = once(H, PL_H, PL_B);
console.log('== SUBJECTS');
cmp('S0 base vs head (the product line is present: must differ)', B, H, false, false);
cmp('S1 base vs head-with-product-line-reverted (every other delta comment-only: must be identical)', B, H1, true, true);
console.log('== CONTROLS (on head)');
cmp('C1 code: predicate conjunct !== -> ===', H, once(H, "(doc as any)._source !== 'anchor_store'", "(doc as any)._source === 'anchor_store'"), false, false);
cmp('C2 added line comment', H, once(H, "    const persistedAnchored = Boolean(\n", "    // qa inert\n    const persistedAnchored = Boolean(\n"), true, true);
cmp('C3 type-only: (doc as any) -> (doc as unknown as any) in the product line (transpile blind spot)', H, once(H, "(persistedStatus == null && (doc as any)._source", "(persistedStatus == null && (doc as unknown as any)._source"), true, false);
cmp('C4 string literal edit in code', H, once(H, "_source: 'anchor_store',  // marker", "_source: 'anchor_storeX',  // marker"), false, false);
cmp('C5 code smuggled after // on a new line', H, once(H, "// KS-1073: carve-out tier-1 only; anchor-store rows are never statusless\n", "// KS-1073: carve-out tier-1 only; anchor-store rows are never statusless\nvoid 0;\n"), false, false);
cmp('C6 comment text edit inside the rewritten tier-2 blob comment', H, once(H, "hash and height do not earn the claim on this tier.", "hash and height DO earn the claim on this tier."), true, true);
cmp('C7 a string edited INSIDE a comment-looking line that is code (the trailing // after the product line is comment: edit it)', H, once(H, "anchor-store rows are never statusless", "anchor-store rows are sometimes statusless"), true, true);
console.log('ALL CONTROLS AND SUBJECTS AS EXPECTED:', all);
