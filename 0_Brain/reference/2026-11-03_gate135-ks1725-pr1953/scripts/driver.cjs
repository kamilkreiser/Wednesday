// Runs the REAL packages/shared middleware validateBody -> next(err) -> REAL errorHandler, and the REAL
// validation.validateBody (400 path), with each tree's own zod + shared dist. Prints status + body per case.
const path=require('path'); const DEV=process.argv[2], side=process.argv[3]; const {createRequire}=require('module'); const req=createRequire(path.join(DEV,'package.json'));
if (side==='head') require(path.join(DEV,'packages/shared/dist/validation/zod3-compat.js'));
const shared=require(path.join(DEV,'packages/shared/dist/index.js'));
const mw=require(path.join(DEV,'packages/shared/dist/middleware/index.js'));
const val=require(path.join(DEV,'packages/shared/dist/validation/index.js'));
const {z}=req('zod');
const cases={
  control_missing:[z.object({name:z.string()}),{}],
  F1_date_null:[z.object({startDate:shared.isoDateTimeSchema.optional()}),{startDate:null}],
  F1_date_number:[z.object({startDate:shared.isoDateTimeSchema.optional()}),{startDate:20261102}],
  F2_array_into_min_string:[z.object({title:z.string().trim().min(3).max(200)}),{title:['a','b','c','d']}],
  F2_string_into_min_array:[z.object({ids:z.array(z.string()).min(2)}),{ids:'x'}],
  F3a_array_min_bad_elems:[z.object({ids:z.array(z.string().uuid ? z.string().min(3) : null).min(2)}),{ids:['a']}],
  F3b_array_over_max_bad_elems:[z.object({ids:z.array(z.string().min(3)).max(2)}),{ids:['a','b','c']}],
  F4_nativeEnum_number:[z.object({tier:z.nativeEnum({HOT:'hot',COLD:'cold'})}),{tier:1}],
  T1_safe_int:[z.object({n:z.number().int()}),{n:2**53}],
};
const out={};
for (const [k,[schema,body]] of Object.entries(cases)) {
  for (const [label,mwfn] of [['mw.validateBody+errorHandler',mw.validateBody],['validation.validateBody',val.validateBody]]) {
    let status=0, json=null; const res={status(s){status=s;return this;},json(j){json=j;return this;},setHeader(){},getHeader(){},headersSent:false,locals:{}};
    const rq={body, headers:{}, method:'POST', path:'/x', originalUrl:'/x', url:'/x', ip:'127.0.0.1', get(){return undefined;}, header(){return undefined;}};
    let nextErr=null; mwfn(schema)(rq,res,(e)=>{nextErr=e||null;});
    if (nextErr) { try { shared.errorHandler(nextErr, rq, res, ()=>{}); } catch(e){ json={THROW:String(e)}; } }
    out[k+' | '+label]={status, body: json, nextOk: !nextErr && status===0};
  }
}
require("fs").writeFileSync(process.argv[4], JSON.stringify(out,null,1));
