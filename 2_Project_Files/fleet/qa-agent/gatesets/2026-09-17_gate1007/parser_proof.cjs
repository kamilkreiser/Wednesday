// parser_proof.cjs — #1007 Q5: the _azureServiceName rename, by the TypeScript parser (typescript required by path from the drafter's farmed tree).
// For base and head blobs: getServiceUrl's declaration (exported? params), every CallExpression whose callee is getServiceUrl (arg count, arg kinds,
// any object-literal argument = "by name"), every Identifier reference to the 3rd parameter's name inside the body, and every reference to
// getServiceUrl anywhere. Then a structural compare: head vs base with Part A+B applied TEXTUALLY is not attempted; instead the head helper body's
// statement kinds are listed beside base's. Controls: a synthetic source with an object-literal call and a used 3rd param must be detected.
const path = require('path'); const fs = require('fs');
const paths = JSON.parse(fs.readFileSync('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007/drafter_paths.json', 'utf8'));
const ts = require(path.join(paths.trees.head, 'Blockchain/Dev/node_modules/typescript'));
const GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007';
console.log('parser_proof', new Date().toString(), 'typescript', ts.version);
function analyse(label, text) {
  const sf = ts.createSourceFile(label + '.ts', text, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  const diags = sf.parseDiagnostics.length;
  let decl = null; const calls = []; const refs = []; let exported = false;
  const exportsFound = [];
  function visit(n) {
    if (ts.isVariableStatement(n)) {
      for (const d of n.declarationList.declarations) if (ts.isIdentifier(d.name) && d.name.text === 'getServiceUrl') { decl = d; exported = !!(n.modifiers || []).some(m => m.kind === ts.SyntaxKind.ExportKeyword); }
      if ((n.modifiers || []).some(m => m.kind === ts.SyntaxKind.ExportKeyword)) exportsFound.push(n.declarationList.declarations.map(d => d.name.getText()).join(','));
    }
    if (ts.isExportAssignment(n)) exportsFound.push('default=' + n.expression.getText());
    if (ts.isExportDeclaration(n)) exportsFound.push('exportDecl=' + n.getText().slice(0, 60));
    if (ts.isCallExpression(n) && ts.isIdentifier(n.expression) && n.expression.text === 'getServiceUrl') {
      calls.push({ line: sf.getLineAndCharacterOfPosition(n.getStart()).line + 1, argc: n.arguments.length, kinds: n.arguments.map(a => ts.SyntaxKind[a.kind]), objectLiteralArg: n.arguments.some(a => ts.isObjectLiteralExpression(ts.skipOuterExpressions(a))), spreadArg: n.arguments.some(a => ts.isSpreadElement(a)), third: n.arguments[2] ? n.arguments[2].getText() : null });
    }
    if (ts.isIdentifier(n) && n.text === 'getServiceUrl' && !(ts.isVariableDeclaration(n.parent) && n.parent.name === n) && !(ts.isCallExpression(n.parent) && n.parent.expression === n)) refs.push('NON-CALL reference at line ' + (sf.getLineAndCharacterOfPosition(n.getStart()).line + 1));
    ts.forEachChild(n, visit);
  }
  visit(sf);
  const fn = decl && decl.initializer; const params = fn ? fn.parameters.map(p => ({ name: p.name.getText(), optional: !!p.questionToken, type: p.type ? p.type.getText() : null })) : [];
  const third = params[2] ? params[2].name : null; let thirdUses = 0; const bodyKinds = [];
  if (fn && fn.body) {
    (function walk(n) { if (ts.isIdentifier(n) && n.text === third && !(ts.isParameter(n.parent))) thirdUses++; ts.forEachChild(n, walk); })(fn.body);
    if (ts.isBlock(fn.body)) for (const s of fn.body.statements) bodyKinds.push(ts.SyntaxKind[s.kind] + (ts.isIfStatement(s) ? '(' + s.expression.getText() + ')' : ''));
  }
  const summary = { label, parseDiagnostics: diags, declFound: !!decl, exported, moduleExports: exportsFound, params, thirdParamUsesInBody: thirdUses, bodyStatements: bodyKinds,
    calls: calls.length, argcHistogram: calls.reduce((h, c) => (h[c.argc] = (h[c.argc] || 0) + 1, h), {}), objectLiteralArgs: calls.filter(c => c.objectLiteralArg).length, spreadArgs: calls.filter(c => c.spreadArg).length,
    thirdArgKinds: [...new Set(calls.filter(c => c.third).map(c => c.kinds[2]))], nonCallRefs: refs };
  console.log(JSON.stringify(summary));
  return { summary, calls };
}
const base = analyse('base', fs.readFileSync(GS + '/src/system-status.base.ts', 'utf8'));
const head = analyse('head', fs.readFileSync(GS + '/src/system-status.head.ts', 'utf8'));
const same = JSON.stringify(base.calls.map(c => [c.argc, c.kinds, c.third])) === JSON.stringify(head.calls.map(c => [c.argc, c.kinds, c.third]));
console.log('call sites base vs head: identical argument lists (count, kinds, 3rd-arg text), line numbers aside:', same);
// (first run missed the object literal under `as any`: the detector now unwraps outer expressions — kept as parser_proof.first-run-*.out)
// Controls: the instrument must SEE a by-name (object literal) call, a spread call, a used 3rd parameter and a non-call reference.
const ctl = analyse('control', "const getServiceUrl = (envVar: string, localPort: number, _azureServiceName?: string): string => { return _azureServiceName ?? envVar + localPort; };\nconst a = getServiceUrl({ envVar: 'X' } as any, 1);\nconst b = getServiceUrl(...(['X', 1, 'y'] as [string, number, string]));\nexport const f = getServiceUrl;\n");
console.log('CONTROL detects: objectLiteralArgs', ctl.summary.objectLiteralArgs === 1, '| spreadArgs', ctl.summary.spreadArgs === 1, '| thirdParamUsesInBody', ctl.summary.thirdParamUsesInBody === 1, '| nonCallRefs', ctl.summary.nonCallRefs.length === 1, '| exported-module list non-empty', ctl.summary.moduleExports.length === 1);
