#!/bin/bash
# drafter_probe1278.sh <scratchpad> — PREDICTIONS for gate27 (never evidence): #1278's REAL head readYamlRouting.ts (extracted byte-for-byte from
# the scratch clone by blob, sha printed) imported under node 24's type stripping, with `typescript` resolved READ-ONLY from the Secuura checkout's
# systemTest/performance/node_modules through a SYMLINK that lives in the scratchpad (nothing is written into the checkout). Shapes are fed to the
# real parserImportSites / callsReadYaml. NOT inside vitest; the gate re-measures every row through the real cells.
set -u
SP="$1"; CL="$SP/g27_sp/clone.git"; W="$SP/g27_probe1278"; H=18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8; D=e6056de7ed640e3a441bc7e33853601bf9040084
mkdir -p "$W/pkg/tests/unit/support"
[ -e "$W/pkg/node_modules" ] || ln -s '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/systemTest/performance/node_modules' "$W/pkg/node_modules"
printf '{"type":"module"}\n' > "$W/pkg/package.json"
git --git-dir "$CL" show "$H:systemTest/performance/tests/unit/support/readYamlRouting.ts" > "$W/pkg/tests/unit/support/readYamlRouting.ts"
git --git-dir "$CL" show "$D:systemTest/performance/runner/config_loader.ts" > "$W/config_loader.develop.ts"
echo "reader blob: head $(git --git-dir "$CL" rev-parse "$H:systemTest/performance/tests/unit/support/readYamlRouting.ts") | extracted $(git --git-dir "$CL" hash-object "$W/pkg/tests/unit/support/readYamlRouting.ts") | typescript $(python3 -c 'import json;print(json.load(open("'"$W"'/pkg/node_modules/typescript/package.json"))["version"])') | node $(node --version)"
cat > "$W/pkg/drive.mts" <<'JS'
import { parserImportSites, callsReadYaml, SEMICOLON_IN_BRACES_LINE_COMMENT as S6B, SEMICOLON_IN_BRACES_JSDOC as S6D, PRETTIER_WRAPPED_IMPORT as PW } from './tests/unit/support/readYamlRouting.ts';
import { readFileSync } from 'node:fs';
const cl = readFileSync(process.argv[2], 'utf8');
const rows: [string, string, string][] = [
  ['S0 the captured prettier fixture', PW, '1'],
  ['S6b line comment with ; in braces (fixture)', S6B, '1'],
  ['S6d JSDoc with ; in braces (fixture)', S6D, '1'],
  ['IE1 import-equals `import y = require(...)`', "import yaml = require('js-yaml');", 'UNKNOWN'],
  ['CR1 createRequire alias', "import { createRequire } from 'node:module';\nconst req = createRequire(import.meta.url);\nconst y = req('js-yaml');", 'UNKNOWN'],
  ['TPL dynamic import of a template literal', 'const y = await import(`js-yaml`);', '1'],
  ['NS namespace import', "import * as y from 'js-yaml';", '1'],
  ['EXS export * from', "export * from 'js-yaml';", '1'],
  ['SUB a subpath specifier', "import { load } from 'js-yaml/dist/js-yaml.mjs';", '1'],
  ['A4 the gate plant inside the REAL develop config_loader.ts', "import {\n    load, // the raw parser; do not use\n    dump,\n} from 'js-yaml';\n" + cl, '1'],
];
for (const [k, s, want] of rows) { const r = parserImportSites(s); console.log(`${k.padEnd(62)} hits=${r.length} want=${want}  ${JSON.stringify(r).slice(0, 110)}`); }
const a2c = cl.replace(/return readYaml\(([^)]*)\);/, 'return JSON.parse(String($1)) as unknown;');
const calls: [string, string, string][] = [
  ['L0 develop config_loader.ts unchanged', cl, 'true'],
  ['A2c the only real call replaced (doc comments left)', a2c, 'false'],
  ['AL1 an alias `const r = readYaml; r(p)`', "import { readYaml } from '../utils/yaml';\nconst r = readYaml;\nexport const f = (p: string) => r(p);", 'UNKNOWN'],
  ['AL2 `readYaml.call(null, p)`', "import { readYaml } from '../utils/yaml';\nexport const f = (p: string) => readYaml.call(null, p);", 'UNKNOWN'],
  ['DEAD a call inside a never-invoked function', "import { readYaml } from '../utils/yaml';\nfunction never(p: string) { return readYaml(p); }\nexport const f = (p: string) => JSON.parse(p);", 'UNKNOWN'],
];
for (const [k, s, want] of calls) console.log(`${k.padEnd(62)} callsReadYaml=${callsReadYaml(s)} want=${want}${k.startsWith('A2c') ? ' (plant applied: ' + (a2c !== cl) + ')' : ''}`);
JS
node --no-warnings "$W/pkg/drive.mts" "$W/config_loader.develop.ts"
echo "rc $?"
