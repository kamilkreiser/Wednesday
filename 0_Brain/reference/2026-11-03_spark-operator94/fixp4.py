p='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94/gen/sites94.py'
L=open(p).read().split('\n')
assert L[103].startswith('I_O=') and L[104].startswith('I_N=')
L[103]=r'''I_O="  const name = (err as { name?: unknown } | null)?.name;\n"'''
L[104]=r'''I_N="  let name: unknown;\n  try {\n    name = (err as { name?: unknown } | null)?.name;\n  } catch {\n    return false;\n  }\n"'''
open(p,'w').write('\n'.join(L))
