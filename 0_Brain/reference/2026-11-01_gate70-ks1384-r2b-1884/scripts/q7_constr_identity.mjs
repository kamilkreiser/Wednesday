// Gate 70 Q7: is the Constr the test constructs the same class the serializer applyParamsToScript uses checks against?
import { createRequire } from 'module';
const anchoringDir = process.argv[2];
const req = createRequire(anchoringDir + '/src/__tests__/x.js');
const lucidPath = req.resolve('@lucid-evolution/lucid');
const utilsPath = req.resolve('@lucid-evolution/utils');
const lucidReq = createRequire(lucidPath);
const utilsReq = createRequire(utilsPath);
console.log('lucid  ->', lucidPath);
console.log('utils  ->', utilsPath);
console.log('plutus as lucid resolves it ->', lucidReq.resolve('@lucid-evolution/plutus'));
console.log('plutus as utils resolves it ->', utilsReq.resolve('@lucid-evolution/plutus'));
const lucid = await import(lucidPath);
const plutusOfUtils = await import(utilsReq.resolve('@lucid-evolution/plutus'));
console.log('lucid.Constr === utils-plutus Constr:', lucid.Constr === plutusOfUtils.Constr);
