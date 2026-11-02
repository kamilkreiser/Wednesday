// constructs the corpus could not evaluate from source: nativeEnum, MFA union, discriminated-ish union of literals, record, passthrough union
const path=require('path'); const H=process.argv[2], B=process.argv[3]; const {createRequire}=require('module');
const compat=require(path.join(H,'packages/shared/dist/validation/zod3-compat.js'));
const z4=createRequire(path.join(H,'package.json'))('zod').z; const z3=createRequire(path.join(B,'package.json'))('zod').z;
const Tier={HOT:'hot',COLD:'cold'}; const Num={A:0,B:1, 0:'A',1:'B'};
const mk=(z)=>({
  nativeEnum:z.object({t:z.nativeEnum(Tier)}),
  nativeEnumNum:z.object({t:z.nativeEnum(Num)}),
  mfa:z.object({c:z.union([z.string().regex(/^\d{6}$/),z.literal('')])}),
  levels:z.object({l:z.union([z.literal(1),z.literal(2),z.literal(3)]).optional()}),
  issuer:z.object({i:z.union([z.string(),z.object({id:z.string()}).passthrough()])}),
  url_or_empty:z.object({u:z.string().url().optional().or(z.literal('')).or(z.null())}),
  rec:z.object({r:z.record(z.string(),z.unknown())}),
  strictNested:z.object({o:z.object({a:z.string()}).strict()}),
  boolCoerce:z.object({b:z.coerce.boolean()}),
  enumArr:z.object({e:z.array(z.enum(['x','y'])).min(1)}),
});
const s3=mk(z3), s4=mk(z4); let diffs=0, n=0;
const vals=[undefined,null,'','12','123456','hot','HOT','warm',0,1,2,4,'1',true,[],{},{id:5},{id:'x',extra:1},'not a url','https://e.com',{a:'x',z:1},{a:1},['x'],['z'],'x'];
for (const k of Object.keys(s3)) for (const v of vals) { n++;
  const key=Object.keys(s3[k].shape)[0]; const inp=v===undefined?{}:{[key]:v};
  const a=s3[k].safeParse(inp), b=s4[k].safeParse(inp);
  const A=a.success?'OK '+JSON.stringify(a.data):JSON.stringify(a.error.issues), Bv=b.success?'OK '+JSON.stringify(b.data):JSON.stringify(compat.zod3Issues(b.error.issues));
  if(A!==Bv){diffs++; console.log(k,JSON.stringify(v)); console.log('  z3',A.slice(0,400)); console.log('  z4',Bv.slice(0,400));}
}
console.log('cells',n,'diffs',diffs);
