// mount_ast.cjs — READ ONLY: parse api-gateway index.ts at head with the checkout's typescript (require only) and report the
// chain of enclosing statements around every call to createVerificationRoutes / createAdminRoutes, plus a control call (createHealthRoutes) and a POSITIVE control: the log('warn', 'Mock endpoints enabled…') call that IS inside if (ENABLE_MOCK_ENDPOINTS).
const ts = require('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules/typescript');
const fs = require('fs');
const file = process.argv[2];
const src = fs.readFileSync(file, 'utf8');
const sf = ts.createSourceFile(file, src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
console.log('mount_ast', new Date().toString(), 'typescript', ts.version);
function visit(n, chain) {
  if (ts.isCallExpression(n) && ts.isIdentifier(n.expression) && (['createVerificationRoutes', 'createAdminRoutes', 'createHealthRoutes'].includes(n.expression.text) || (n.expression.text === 'log' && /Mock endpoints enabled/.test(n.getText(sf))))) {
    const line = sf.getLineAndCharacterOfPosition(n.getStart()).line + 1;
    const ifs = chain.filter(c => ts.isIfStatement(c)).map(c => 'if(' + c.expression.getText(sf) + ')@' + (sf.getLineAndCharacterOfPosition(c.getStart()).line + 1));
    const kinds = chain.filter(c => ts.isBlock(c) || ts.isIfStatement(c) || ts.isFunctionLike(c)).map(c => ts.SyntaxKind[c.kind] + '@' + (sf.getLineAndCharacterOfPosition(c.getStart()).line + 1));
    console.log(n.expression.text, 'line', line, 'enclosing ifs:', ifs.length ? ifs.join(' > ') : 'NONE (top level)', '| enclosing blocks/functions:', kinds.length ? kinds.join(' > ') : 'none');
  }
  ts.forEachChild(n, c => visit(c, chain.concat([n])));
}
visit(sf, []);
