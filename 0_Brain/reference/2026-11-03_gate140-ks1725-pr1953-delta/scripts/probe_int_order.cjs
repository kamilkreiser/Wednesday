// Gate 140: MF2b survived. Is the F2 `.int()` exclusion load-bearing? A length/size check DECLARED BEFORE .int()
// (zod 3 ran both and reported both). Also two length checks on one array (MF3e). Real zod 3.25.76 vs head zod3Issues.
const path=require('path'); const H=process.argv[2], B=process.argv[3]; const {createRequire}=require('module');
const compat=require(path.join(H,'packages/shared/dist/validation/zod3-compat.js'));
const z4=createRequire(path.join(H,'package.json'))('zod').z; const z3=createRequire(path.join(B,'package.json'))('zod').z;
const mk=(z)=>({
  min_then_int:[z.object({n:z.number().min(5).int()}),{n:1.5}],
  positive_then_int:[z.object({n:z.number().positive().int()}),{n:-1.5}],
  nonneg_then_int:[z.object({n:z.number().nonnegative().int()}),{n:-0.5}],
  max_then_int:[z.object({n:z.number().max(3).int()}),{n:4.5}],
  int_then_min:[z.object({n:z.number().int().min(5)}),{n:1.5}],
  coerce_min_then_int:[z.object({n:z.coerce.number().min(1).int()}),{n:'0.5'}],
  two_len_checks:[z.object({a:z.array(z.string()).min(1).min(3)}),{a:[]}],
  len_and_min:[z.object({a:z.array(z.string()).length(4).min(5)}),{a:['x']}],
  two_len_checks_elems:[z.object({a:z.array(z.string().min(2)).min(2).min(3)}),{a:['x']}],
});
const s3=mk(z3), s4=mk(z4); let d=0;
for (const k of Object.keys(s3)) { const [a,inp]=s3[k], [b]=s4[k]; const ra=a.safeParse(inp), rb=b.safeParse(inp);
  const A=ra.success?'OK':JSON.stringify(ra.error.issues), Bv=rb.success?'OK':JSON.stringify(compat.zod3Issues(rb.error.issues));
  const eq=A===Bv; d+=!eq; console.log((eq?'EQUAL ':'DIFF  ')+k); if(!eq){console.log('  z3  ',A); console.log('  head',Bv);} }
console.log('diffs',d);
