// F1: zod3Datetime({message}) vs zod 3 .datetime({message}); and the candidate fix
const path=require('path'); const H=process.argv[2], B=process.argv[3]; const {createRequire}=require('module');
const compat=require(path.join(H,'packages/shared/dist/validation/zod3-compat.js'));
const z4=createRequire(path.join(H,'package.json'))('zod').z; const z3=createRequire(path.join(B,'package.json'))('zod').z;
const M='Invalid RFC 3339 date-time';
const s3=z3.object({d:z3.string().datetime({offset:true,message:M})});
const s4=z4.object({d:compat.zod3Datetime({offset:true,message:M})});
const re=compat.zod3DatetimeRegex({precision:null,offset:true,local:false});
const s4fix=z4.object({d:z4.stringFormat('datetime',(v)=>re.test(v),{error:(iss)=>iss.code==='invalid_format'?M:undefined})});
let diffs=0, fixdiffs=0;
for (const v of [undefined,null,5,true,[],{}, '', 'x','2026-11-02T10:00Z','2026-11-02T10:00:00+10:00','2026-13-01T00:00:00Z']) {
  const inp = v===undefined?{}:{d:v};
  const f=(s,ser)=>{const r=s.safeParse(inp); return r.success?'OK':JSON.stringify(ser(r.error.issues));};
  const a=f(s3,x=>x), b=f(s4,compat.zod3Issues), c=f(s4fix,compat.zod3Issues);
  if(a!==b) diffs++; if(a!==c) fixdiffs++;
  console.log(JSON.stringify(v===undefined?'<missing>':v)); console.log('  zod3 ',a); if(a!==b) console.log('  HEAD ',b,' <-- DIFF'); if(a!==c) console.log('  FIX  ',c,' <-- DIFF');
}
console.log('head diffs',diffs,'fix diffs',fixdiffs);
